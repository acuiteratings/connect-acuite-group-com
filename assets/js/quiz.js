(function attachQuizArena() {
  const DIFFICULTY_LABELS = {
    amateur: "Amateur",
    enthusiast: "Enthusiast",
    professional: "Professional",
    expert: "Expert",
  };

  const state = {
    lobby: null,
    match: null,
    selectedInvitees: [],
    candidateResults: [],
    searchQuery: "",
    difficulty: "amateur",
    pollTimer: null,
  };

  let elements = {};

  document.addEventListener("DOMContentLoaded", () => {
    void initQuizArena();
  });

  async function initQuizArena() {
    elements = {
      headStatus: document.getElementById("quiz-head-status"),
      difficultySummary: document.getElementById("quiz-difficulty-summary"),
      playerSummary: document.getElementById("quiz-player-summary"),
      stageTitle: document.getElementById("quiz-stage-title"),
      stageMeta: document.getElementById("quiz-stage-meta"),
      stage: document.getElementById("quiz-stage"),
      alert: document.getElementById("quiz-alert"),
    };
    if (!elements.stage) {
      return;
    }
    document.addEventListener("click", handleClick);
    document.addEventListener("input", handleInput);
    await loadLobby();
  }

  async function loadLobby() {
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest("/api/quiz/lobby/");
      state.lobby = payload;
      const openMatch = payload.viewer_active_match || payload.incoming_invites?.[0] || payload.outgoing_invites?.[0] || null;
      if (openMatch) {
        await loadMatchState(openMatch.id);
      } else {
        state.match = null;
        render();
      }
    } catch (error) {
      showAlert(error.message || "Could not load Quiz Arena.");
    }
  }

  async function loadMatchState(matchId) {
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest(`/api/quiz/matches/${matchId}/state/`);
      state.match = payload.match || null;
      render();
      syncPolling();
    } catch (error) {
      state.match = null;
      showAlert(error.message || "Could not load the quiz match.");
      render();
    }
  }

  async function searchCandidates() {
    if (state.searchQuery.trim().length < 2) {
      state.candidateResults = [];
      render();
      return;
    }
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest(`/api/quiz/candidates/?q=${encodeURIComponent(state.searchQuery.trim())}`);
      state.candidateResults = Array.isArray(payload.results) ? payload.results : [];
      render();
    } catch (error) {
      showAlert(error.message || "Could not search colleagues.");
    }
  }

  function render() {
    renderSummaries();
    renderStage();
  }

  function renderSummaries() {
    if (!elements.difficultySummary || !elements.playerSummary) {
      return;
    }
    if (!state.match) {
      elements.headStatus.textContent = "No live quiz match";
      elements.difficultySummary.innerHTML = `
        <p class="widget-kicker">Difficulty</p>
        <h3>${escapeHtml(DIFFICULTY_LABELS[state.difficulty])}</h3>
        <p>The host chooses one level before the invite is sent.</p>
      `;
      elements.playerSummary.innerHTML = `
        <p class="widget-kicker">Players</p>
        <h3>${escapeHtml(String(state.selectedInvitees.length + 1))} selected</h3>
        <p>Invite between 1 and 3 colleagues. A quiz starts with at least 2 accepted players.</p>
      `;
      return;
    }

    elements.headStatus.textContent = state.match.status_label;
    elements.difficultySummary.innerHTML = `
      <p class="widget-kicker">Difficulty</p>
      <h3>${escapeHtml(state.match.difficulty_label)}</h3>
      <p>${escapeHtml(`${state.match.total_questions || 10} questions in this match`)}</p>
    `;
    elements.playerSummary.innerHTML = `
      <p class="widget-kicker">Players</p>
      <h3>${escapeHtml(String((state.match.participants || []).filter((item) => item.status === "accepted").length))} active</h3>
      <p>${escapeHtml(`${(state.match.participants || []).length} total seats in this room`)}</p>
    `;
  }

  function renderStage() {
    if (!elements.stage || !elements.stageTitle || !elements.stageMeta) {
      return;
    }
    hideAlert();

    if (!state.match) {
      elements.stageTitle.textContent = "Quiz lobby";
      elements.stageMeta.textContent = "Invite up to 3 colleagues, choose the difficulty, and start when at least 2 people are ready.";
      elements.stage.innerHTML = renderCreateStage();
      return;
    }

    if (state.match.status === "invited") {
      elements.stageTitle.textContent = "Invitations open";
      elements.stageMeta.textContent = "Players can accept or decline. The host can start once at least 2 players have accepted.";
      elements.stage.innerHTML = renderInviteStage();
      return;
    }

    if (state.match.status === "active") {
      elements.stageTitle.textContent = `Question ${state.match.current_question?.index || 1} of ${state.match.current_question?.total || 10}`;
      elements.stageMeta.textContent = "Answer within 15 seconds. Highest score after 10 questions wins.";
      elements.stage.innerHTML = renderActiveStage();
      return;
    }

    elements.stageTitle.textContent = "Match complete";
    elements.stageMeta.textContent = "This quiz is over. You can return to the lobby and start another one.";
    elements.stage.innerHTML = renderCompletedStage();
  }

  function renderCreateStage() {
    const selectedCards = state.selectedInvitees.map((person) => `
      <span class="mini-chip success">
        ${escapeHtml(person.name)}
        <button type="button" class="btn-link" data-action="quiz-remove-invitee" data-id="${person.id}">Remove</button>
      </span>
    `).join("");
    const candidateCards = state.candidateResults.map((person) => `
      <button type="button" class="admin-user-card" data-action="quiz-add-invitee" data-id="${person.id}">
        <div>
          <div class="mini-item-title">${escapeHtml(person.name)}</div>
          <div class="mini-item-meta">${escapeHtml([person.title, person.location].filter(Boolean).join(" | ") || person.email)}</div>
        </div>
        <span class="mini-chip">Add</span>
      </button>
    `).join("");
    return `
      <div class="story-form">
        <label class="field">
          <span>Difficulty level</span>
          <select id="quiz-difficulty-select">
            ${Object.entries(DIFFICULTY_LABELS).map(([value, label]) => `<option value="${value}" ${state.difficulty === value ? "selected" : ""}>${escapeHtml(label)}</option>`).join("")}
          </select>
        </label>
        <label class="field">
          <span>Find colleagues</span>
          <input type="text" id="quiz-candidate-search" value="${escapeHtml(state.searchQuery)}" placeholder="Type at least 2 letters of a name or email">
        </label>
        <div class="mini-item-meta">You can invite up to 3 colleagues.</div>
        <div class="bulletin-meta-lines">${selectedCards || '<span class="mini-item-meta">No colleagues selected yet.</span>'}</div>
        <div class="community-feed">${candidateCards || '<div class="empty-state">Search results will appear here.</div>'}</div>
        <div class="form-actions">
          <p>A 10-question match will be created. Each question has 15 seconds and there is no negative marking.</p>
          <button type="button" class="btn-warm" data-action="quiz-create-match" ${state.selectedInvitees.length ? "" : "disabled"}>Send invites</button>
        </div>
      </div>
    `;
  }

  function renderInviteStage() {
    const viewer = state.match.viewer || {};
    const participants = (state.match.participants || []).map((item) => `
      <article class="summary-card foundation-card">
        <strong>${escapeHtml(item.user?.name || "Player")}</strong>
        <span class="mini-item-meta">${escapeHtml(item.status)}</span>
        <p>${escapeHtml([item.user?.title, item.user?.location].filter(Boolean).join(" | ") || item.user?.email || "")}</p>
      </article>
    `).join("");
    const acceptedCount = (state.match.participants || []).filter((item) => item.status === "accepted").length;
    return `
      <div class="community-feed">${participants}</div>
      <div class="form-actions">
        <p>${escapeHtml(`${acceptedCount} accepted player${acceptedCount === 1 ? "" : "s"} ready.`)}</p>
        ${viewer.status === "invited"
          ? `<button type="button" class="btn-warm" data-action="quiz-respond" data-decision="accept">Accept</button>
             <button type="button" class="btn-outline" data-action="quiz-respond" data-decision="decline">Decline</button>`
          : ""}
        ${viewer.is_host
          ? `<button type="button" class="btn-warm" data-action="quiz-start-match" ${acceptedCount >= 2 ? "" : "disabled"}>Start quiz</button>
             <button type="button" class="btn-outline" data-action="quiz-cancel-match">Cancel</button>`
          : ""}
      </div>
    `;
  }

  function renderActiveStage() {
    const question = state.match.current_question || null;
    const viewer = state.match.viewer || {};
    const leaderboard = (state.match.leaderboard || []).map((item) => `
      <div class="mini-item-row">
        <span>${escapeHtml(item.user?.name || "Player")}</span>
        <strong>${escapeHtml(String(item.score))}</strong>
      </div>
    `).join("");
    if (!question) {
      return '<div class="empty-state">Waiting for the next question.</div>';
    }
    return `
      <div class="voice-card bulletin-card">
        <div class="voice-card-top">
          <div class="voice-card-tags">
            <span class="mini-chip">${escapeHtml(question.category_label)}</span>
            <span class="mini-chip success">${escapeHtml(question.difficulty_label)}</span>
          </div>
          <div class="community-time">${escapeHtml(`${question.seconds_remaining}s left`)}</div>
        </div>
        <div class="card-body">
          <div class="card-title">${escapeHtml(question.prompt)}</div>
        </div>
        <div class="quiz-options">
          ${question.options.map((option) => `
            <button
              type="button"
              class="tool-open live quiz-option-button"
              data-action="quiz-answer"
              data-option="${option.key}"
              ${viewer.status !== "accepted" || question.viewer_answered || question.seconds_remaining <= 0 ? "disabled" : ""}
            >
              ${escapeHtml(`${option.key}. ${option.label}`)}
            </button>
          `).join("")}
        </div>
        <div class="form-actions">
          <p>${escapeHtml(`${question.answers_received} answer${question.answers_received === 1 ? "" : "s"} received so far.`)}</p>
          ${question.viewer_answered ? '<span class="mini-chip success">Answer locked</span>' : ""}
        </div>
      </div>
      <div class="widget-card">
        <p class="widget-kicker">Live scores</p>
        <h3>Leaderboard</h3>
        <div class="directory-meta-list">${leaderboard}</div>
      </div>
    `;
  }

  function renderCompletedStage() {
    const leaderboard = (state.match.leaderboard || []).map((item, index) => `
      <article class="summary-card foundation-card">
        <strong>${escapeHtml(`${index + 1}. ${item.user?.name || "Player"}`)}</strong>
        <span class="mini-item-meta">${escapeHtml(`${item.score} points`)}</span>
      </article>
    `).join("");
    return `
      <div class="community-feed">${leaderboard || '<div class="empty-state">No scores available.</div>'}</div>
      <div class="form-actions">
        <p>The match is complete. Return to the lobby to create a new quiz room.</p>
        <button type="button" class="btn-warm" data-action="quiz-return-lobby">Back to lobby</button>
      </div>
    `;
  }

  async function handleClick(event) {
    const action = event.target.closest("[data-action]");
    if (!action) {
      return;
    }
    const actionName = action.dataset.action;
    if (actionName === "quiz-add-invitee") {
      addInvitee(Number(action.dataset.id || 0));
      return;
    }
    if (actionName === "quiz-remove-invitee") {
      removeInvitee(Number(action.dataset.id || 0));
      return;
    }
    if (actionName === "quiz-create-match") {
      await createMatch();
      return;
    }
    if (actionName === "quiz-respond") {
      await respondToInvite(action.dataset.decision);
      return;
    }
    if (actionName === "quiz-start-match") {
      await postMatchAction("start", "Quiz started.");
      return;
    }
    if (actionName === "quiz-cancel-match") {
      await postMatchAction("cancel", "Quiz cancelled.");
      return;
    }
    if (actionName === "quiz-answer") {
      await answerQuestion(action.dataset.option);
      return;
    }
    if (actionName === "quiz-return-lobby") {
      state.match = null;
      await loadLobby();
    }
  }

  function handleInput(event) {
    if (event.target.id === "quiz-candidate-search") {
      state.searchQuery = event.target.value;
      void searchCandidates();
      return;
    }
    if (event.target.id === "quiz-difficulty-select") {
      state.difficulty = event.target.value || "amateur";
      render();
    }
  }

  function addInvitee(userId) {
    if (state.selectedInvitees.some((item) => item.id === userId) || state.selectedInvitees.length >= 3) {
      return;
    }
    const person = state.candidateResults.find((item) => item.id === userId);
    if (!person) {
      return;
    }
    state.selectedInvitees.push(person);
    render();
  }

  function removeInvitee(userId) {
    state.selectedInvitees = state.selectedInvitees.filter((item) => item.id !== userId);
    render();
  }

  async function createMatch() {
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest("/api/quiz/matches/", {
        method: "POST",
        body: {
          difficulty: state.difficulty,
          invitee_user_ids: state.selectedInvitees.map((item) => item.id),
        },
      });
      state.selectedInvitees = [];
      state.candidateResults = [];
      state.searchQuery = "";
      state.match = payload.match || null;
      render();
      syncPolling();
    } catch (error) {
      showAlert(error.message || "Could not send quiz invites.");
    }
  }

  async function respondToInvite(decision) {
    if (!state.match) {
      return;
    }
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest(`/api/quiz/matches/${state.match.id}/respond/`, {
        method: "POST",
        body: { decision },
      });
      state.match = payload.match || null;
      render();
    } catch (error) {
      showAlert(error.message || "Could not update the invitation.");
    }
  }

  async function postMatchAction(action, successMessage) {
    if (!state.match) {
      return;
    }
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest(`/api/quiz/matches/${state.match.id}/${action}/`, {
        method: "POST",
      });
      state.match = payload.match || null;
      render();
      syncPolling();
      if (successMessage) {
        showAlert(successMessage, true);
      }
    } catch (error) {
      showAlert(error.message || "Could not update the quiz match.");
    }
  }

  async function answerQuestion(option) {
    if (!state.match) {
      return;
    }
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest(`/api/quiz/matches/${state.match.id}/answer/`, {
        method: "POST",
        body: { selected_option: option },
      });
      state.match = payload.match || null;
      render();
    } catch (error) {
      showAlert(error.message || "Could not save your answer.");
    }
  }

  function syncPolling() {
    window.clearInterval(state.pollTimer);
    if (!state.match || state.match.status !== "active") {
      state.pollTimer = null;
      return;
    }
    state.pollTimer = window.setInterval(() => {
      void loadMatchState(state.match.id);
    }, 1000);
  }

  function showAlert(message, isSuccess = false) {
    if (!elements.alert) {
      return;
    }
    elements.alert.hidden = false;
    elements.alert.classList.toggle("success", Boolean(isSuccess));
    elements.alert.textContent = message;
  }

  function hideAlert() {
    if (!elements.alert) {
      return;
    }
    elements.alert.hidden = true;
    elements.alert.classList.remove("success");
    elements.alert.textContent = "";
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }
})();
