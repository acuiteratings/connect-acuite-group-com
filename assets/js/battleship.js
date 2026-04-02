(function attachBattleshipModule() {
  const BOARD_SIZE = 10;
  const ROW_LABELS = "ABCDEFGHIJ";
  const DEFAULT_POLL_SECONDS = 4;
  const DRAFT_STORAGE_PREFIX = "acuite-connect-battleship-draft-";
  const FLEET_ORDER = ["carrier", "battleship", "cruiser", "submarine", "destroyer"];

  const state = {
    currentUser: null,
    lobby: null,
    match: null,
    alert: null,
    busy: false,
    inviteQuery: "",
    selectedShipType: "carrier",
    orientation: "horizontal",
    draft: [],
    pollTimer: 0,
    searchTimer: 0,
  };

  const elements = {};

  document.addEventListener("DOMContentLoaded", () => {
    void initBattleship();
  });

  async function initBattleship() {
    elements.panel = document.getElementById("panel-battleship");
    if (!elements.panel) {
      return;
    }

    elements.stage = document.getElementById("battleship-stage");
    elements.alert = document.getElementById("battleship-alert");
    elements.stageTitle = document.getElementById("battleship-stage-title");
    elements.stageMeta = document.getElementById("battleship-stage-meta");
    elements.headStatus = document.getElementById("battleship-head-status");
    elements.officeSummary = document.getElementById("battleship-office-summary");
    elements.slotSummary = document.getElementById("battleship-slot-summary");
    elements.rulesCard = document.getElementById("battleship-rules-card");

    bindEvents();
    renderRulesCard();
    render();

    if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.fetchCurrentSession) {
      setAlert("Battleship needs the Connect auth layer to be available.", "error");
      render();
      return;
    }

    try {
      const session = await window.AcuiteConnectAuth.fetchCurrentSession();
      if (!session || !session.authenticated || !session.user) {
        return;
      }
      state.currentUser = session.user;
      await refreshLobby({ silent: true });
      schedulePoll();
    } catch (error) {
      setAlert(error.message || "Could not load Battleship right now.", "error");
      render();
    }
  }

  function bindEvents() {
    document.addEventListener("visibilitychange", () => {
      schedulePoll();
    });

    if (elements.stage) {
      elements.stage.addEventListener("click", (event) => {
        void handleStageClick(event);
      });
      elements.stage.addEventListener("submit", (event) => {
        void handleStageSubmit(event);
      });
      elements.stage.addEventListener("input", (event) => {
        handleStageInput(event);
      });
    }
  }

  function getPollIntervalMs() {
    const seconds = Number(state.lobby?.office_policy?.poll_interval_seconds || DEFAULT_POLL_SECONDS);
    return Math.max(2, seconds) * 1000;
  }

  function schedulePoll() {
    if (state.pollTimer) {
      window.clearTimeout(state.pollTimer);
      state.pollTimer = 0;
    }
    if (document.hidden || !state.currentUser) {
      return;
    }
    state.pollTimer = window.setTimeout(async () => {
      await refreshLobby({ silent: true });
      schedulePoll();
    }, getPollIntervalMs());
  }

  async function refreshLobby({ silent = false } = {}) {
    if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
      return;
    }
    try {
      const query = state.inviteQuery ? `?q=${encodeURIComponent(state.inviteQuery)}` : "";
      const payload = await window.AcuiteConnectAuth.apiRequest(`/api/battleship/lobby/${query}`);
      state.lobby = payload;
      state.match = payload.viewer_match || payload.viewer_open_match || null;
      if (isPlacementPhase(state.match)) {
        hydrateDraftFromMatch();
      } else if (!state.match) {
        state.draft = [];
      }
      if (!silent) {
        clearAlert();
      }
      render();
      schedulePoll();
    } catch (error) {
      if (!silent) {
        setAlert(error.message || "Could not refresh Battleship.", "error");
      }
      render();
    }
  }

  async function handleStageClick(event) {
    const actionButton = event.target.closest("[data-bs-action]");
    if (!actionButton || state.busy) {
      return;
    }

    const action = actionButton.dataset.bsAction;
    if (action === "refresh-lobby") {
      await refreshLobby();
      return;
    }
    if (action === "invite-user") {
      await inviteUser(actionButton.dataset.userId);
      return;
    }
    if (action === "accept-invite") {
      await respondToInvite("accept");
      return;
    }
    if (action === "decline-invite") {
      if (!window.confirm("Decline this Battleship invitation?")) {
        return;
      }
      await respondToInvite("decline");
      return;
    }
    if (action === "cancel-invite") {
      if (!window.confirm("Cancel this invitation?")) {
        return;
      }
      await cancelInvite();
      return;
    }
    if (action === "rotate-placement") {
      state.orientation = state.orientation === "horizontal" ? "vertical" : "horizontal";
      render();
      return;
    }
    if (action === "select-ship") {
      state.selectedShipType = actionButton.dataset.shipType || state.selectedShipType;
      render();
      return;
    }
    if (action === "reset-layout") {
      if (!window.confirm("Clear your current fleet layout?")) {
        return;
      }
      state.draft = [];
      persistDraft();
      render();
      return;
    }
    if (action === "randomize-layout") {
      state.draft = generateRandomFleet();
      persistDraft();
      ensureSelectedShip();
      render();
      return;
    }
    if (action === "submit-placement") {
      await submitPlacement();
      return;
    }
    if (action === "place-cell") {
      placeSelectedShip(Number(actionButton.dataset.row), Number(actionButton.dataset.col));
      return;
    }
    if (action === "fire-cell") {
      await fireShot(Number(actionButton.dataset.row), Number(actionButton.dataset.col));
      return;
    }
    if (action === "resign-match") {
      if (!window.confirm("Resign from this Battleship match?")) {
        return;
      }
      await resignCurrentMatch();
      return;
    }
    if (action === "request-rematch") {
      if (!window.confirm("Send a rematch invitation?")) {
        return;
      }
      await requestRematch();
    }
  }

  async function handleStageSubmit(event) {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) {
      return;
    }

    if (form.id === "battleship-search-form") {
      event.preventDefault();
      const input = form.querySelector('input[name="invite_query"]');
      state.inviteQuery = (input?.value || "").trim();
      await refreshLobby({ silent: true });
    }
  }

  function handleStageInput(event) {
    const target = event.target;
    if (!(target instanceof HTMLInputElement)) {
      return;
    }
    if (target.name !== "invite_query") {
      return;
    }
    state.inviteQuery = target.value.trim();
    if (state.searchTimer) {
      window.clearTimeout(state.searchTimer);
    }
    state.searchTimer = window.setTimeout(() => {
      void refreshLobby({ silent: true });
    }, 250);
  }

  async function inviteUser(userId) {
    if (!userId) {
      return;
    }
    await runAction(async () => {
      const payload = await window.AcuiteConnectAuth.apiRequest("/api/battleship/invite/", {
        method: "POST",
        body: { invitee_user_id: Number(userId) },
      });
      state.match = payload.match || null;
      setAlert("Invitation sent.", "success");
      await refreshLobby({ silent: true });
    });
  }

  async function respondToInvite(decision) {
    if (!state.match?.id) {
      return;
    }
    await runAction(async () => {
      const payload = await window.AcuiteConnectAuth.apiRequest(
        `/api/battleship/matches/${state.match.id}/respond/`,
        {
          method: "POST",
          body: { decision },
        },
      );
      state.match = payload.match || null;
      setAlert(
        decision === "accept"
          ? "Invitation accepted. Place your fleet to begin."
          : "Invitation declined.",
        decision === "accept" ? "success" : "info",
      );
      await refreshLobby({ silent: true });
    });
  }

  async function cancelInvite() {
    if (!state.match?.id) {
      return;
    }
    await runAction(async () => {
      await window.AcuiteConnectAuth.apiRequest(
        `/api/battleship/matches/${state.match.id}/cancel/`,
        { method: "POST" },
      );
      setAlert("Invitation cancelled.", "info");
      await refreshLobby({ silent: true });
    });
  }

  async function submitPlacement() {
    if (!state.match?.id || !isPlacementPhase(state.match)) {
      return;
    }
    if (state.draft.length !== 5) {
      setAlert("Place all five ships before locking in your fleet.", "error");
      render();
      return;
    }
    await runAction(async () => {
      const payload = await window.AcuiteConnectAuth.apiRequest(
        `/api/battleship/matches/${state.match.id}/placement/`,
        {
          method: "POST",
          body: { fleet_layout: state.draft.map(stripDraftForSubmit) },
        },
      );
      clearPersistedDraft();
      state.match = payload.match || null;
      setAlert("Fleet locked in.", "success");
      await refreshLobby({ silent: true });
    });
  }

  async function fireShot(row, col) {
    if (!state.match?.id) {
      return;
    }
    await runAction(async () => {
      const payload = await window.AcuiteConnectAuth.apiRequest(
        `/api/battleship/matches/${state.match.id}/fire/`,
        {
          method: "POST",
          body: { row, col },
        },
      );
      state.match = payload.match || null;
      clearAlert();
      await refreshLobby({ silent: true });
    });
  }

  async function resignCurrentMatch() {
    if (!state.match?.id) {
      return;
    }
    await runAction(async () => {
      const payload = await window.AcuiteConnectAuth.apiRequest(
        `/api/battleship/matches/${state.match.id}/resign/`,
        { method: "POST" },
      );
      state.match = payload.match || null;
      setAlert("Match resigned.", "info");
      await refreshLobby({ silent: true });
    });
  }

  async function requestRematch() {
    if (!state.match?.id) {
      return;
    }
    await runAction(async () => {
      const payload = await window.AcuiteConnectAuth.apiRequest(
        `/api/battleship/matches/${state.match.id}/rematch/`,
        { method: "POST" },
      );
      state.match = payload.match || null;
      setAlert("Rematch invitation sent.", "success");
      await refreshLobby({ silent: true });
    });
  }

  async function runAction(callback) {
    state.busy = true;
    render();
    try {
      await callback();
    } catch (error) {
      const officePolicy = error.payload?.office_policy;
      if (officePolicy?.message) {
        setAlert(officePolicy.message, "error");
      } else {
        setAlert(error.message || "Action could not be completed.", "error");
      }
      render();
    } finally {
      state.busy = false;
      render();
    }
  }

  function render() {
    renderSummaryCards();
    renderStage();
    renderRulesCard();
    renderAlert();
  }

  function renderSummaryCards() {
    const officePolicy = state.lobby?.office_policy || null;
    const globalMatch = state.lobby?.global_active_match || null;
    const currentMatch = state.match;

    if (elements.headStatus) {
      if (!officePolicy) {
        elements.headStatus.textContent = "Loading...";
      } else if (officePolicy.blocked) {
        elements.headStatus.innerHTML = `<span class="battleship-chip danger">Paused until ${escapeHtml(officePolicy.next_allowed_label)}</span>`;
      } else {
        elements.headStatus.innerHTML = `<span class="battleship-chip success">Available now</span>`;
      }
    }

    if (elements.officeSummary) {
      elements.officeSummary.innerHTML = officePolicy
        ? `
          <p class="widget-kicker">Office hours</p>
          <h3>${officePolicy.blocked ? "Gameplay paused" : "Gameplay open"}</h3>
          <p class="muted-copy">${escapeHtml(officePolicy.blocked ? officePolicy.message : "Invites, placement and turns are currently allowed.")}</p>
          <div class="mini-item-meta">${escapeHtml(officePolicy.windows.map((window) => window.label).join(" | "))}</div>
        `
        : renderLoadingMiniCard();
    }

    if (elements.slotSummary) {
      const occupiedByOthers = globalMatch && !isViewerInMatch(globalMatch);
      elements.slotSummary.innerHTML = `
        <p class="widget-kicker">Intranet slot</p>
        <h3>${globalMatch ? "Occupied" : "Open"}</h3>
        <p class="muted-copy">${
          globalMatch
            ? `${escapeHtml(globalMatch.players.inviter.name)} vs ${escapeHtml(globalMatch.players.invitee.name)}`
            : "No accepted Battleship match is occupying the live slot right now."
        }</p>
        <div class="mini-item-meta">${
          occupiedByOthers
            ? "You may still send invitations, but no second match can enter placement or play until this one finishes."
            : globalMatch
              ? escapeHtml(globalMatch.status_label)
              : "Pending invitations are allowed."
        }</div>
      `;
    }

  }

  function renderStage() {
    if (!elements.stage) {
      return;
    }
    if (!state.lobby) {
      setStageHeader("Lobby", "Loading Battleship...");
      elements.stage.innerHTML = renderLoadingStage();
      return;
    }

    if (!state.match) {
      renderLobbyStage();
      return;
    }

    if (state.match.status === "invited") {
      if (state.match.viewer?.can_accept || state.match.viewer?.can_decline) {
        renderIncomingInviteStage();
      } else {
        renderOutgoingInviteStage();
      }
      return;
    }

    if (isPlacementPhase(state.match)) {
      renderPlacementStage();
      return;
    }

    renderBattleStage();
  }

  function renderLobbyStage() {
    const officePolicy = state.lobby.office_policy;
    const globalMatch = state.lobby.global_active_match;
    setStageHeader(
      "Game lobby",
      officePolicy.blocked
        ? `New invitations are paused until ${officePolicy.next_allowed_label}.`
        : "Invite one colleague. Multiple pending invitations are allowed, but only one accepted Battleship match may occupy the live slot across Connect at a time.",
    );
    elements.stage.innerHTML = `
      <div class="battleship-lobby">
        ${globalMatch ? renderGlobalSlotNotice(globalMatch) : ""}
        <div class="battleship-lobby-grid">
          <article class="battleship-card">
            <p class="widget-kicker">Invite a colleague</p>
            <h3>Start a 2-player match</h3>
            <p class="muted-copy">Use employee search inside the intranet and invite exactly one human opponent.</p>
            <form id="battleship-search-form" class="battleship-search-form">
              <input
                type="text"
                name="invite_query"
                value="${escapeHtml(state.inviteQuery)}"
                placeholder="Search by name, email, location or role"
                autocomplete="off"
              >
              <button type="submit" class="btn-ghost">Search</button>
            </form>
            <div class="battleship-candidate-list">
              ${renderCandidateResults()}
            </div>
          </article>
          <article class="battleship-card">
            <p class="widget-kicker">Invitation overview</p>
            <h3>Incoming and outgoing invites</h3>
            ${renderInviteList("Incoming", state.lobby.incoming_invites)}
            ${renderInviteList("Outgoing", state.lobby.outgoing_invites)}
            <div class="battleship-actions-row">
              <button type="button" class="btn-ghost" data-bs-action="refresh-lobby">Refresh</button>
            </div>
          </article>
        </div>
      </div>
    `;
  }

  function renderIncomingInviteStage() {
    const match = state.match;
    setStageHeader(
      "Invite received",
      `${match.players.inviter.name} invited you to a Battleship match.`,
    );
    elements.stage.innerHTML = `
      <div class="battleship-card invite-card">
        <p class="widget-kicker">Pending invitation</p>
        <h3>${escapeHtml(match.players.inviter.name)} wants to play Battleship</h3>
        <p class="muted-copy">
          This is a 10x10, 2-player, turn-based match. Once accepted, the match will claim the single live slot for Battleship across the intranet.
        </p>
        <div class="battleship-meta-list">
          <div><span>Invited by</span><strong>${escapeHtml(match.players.inviter.name)}</strong></div>
          <div><span>Expires</span><strong>${formatDateTime(match.invitation_expires_at)}</strong></div>
          <div><span>Office policy</span><strong>${escapeHtml(state.lobby.office_policy.blocked ? "Paused now" : "Available now")}</strong></div>
        </div>
        <div class="battleship-actions-row">
          <button type="button" class="btn-warm" data-bs-action="accept-invite" ${state.busy || !match.viewer?.can_accept ? "disabled" : ""}>Accept invite</button>
          <button type="button" class="btn-ghost" data-bs-action="decline-invite" ${state.busy || !match.viewer?.can_decline ? "disabled" : ""}>Decline</button>
        </div>
      </div>
    `;
  }

  function renderOutgoingInviteStage() {
    const match = state.match;
    setStageHeader(
      "Invitation pending",
      `Waiting for ${match.opponent.name} to accept or decline.`,
    );
    elements.stage.innerHTML = `
      <div class="battleship-card invite-card">
        <p class="widget-kicker">Pending invitation</p>
        <h3>${escapeHtml(match.opponent.name)} has not responded yet</h3>
        <p class="muted-copy">
          Once accepted, the match will move to ship placement and claim the single active Battleship slot across Connect.
        </p>
        <div class="battleship-meta-list">
          <div><span>Invited player</span><strong>${escapeHtml(match.opponent.name)}</strong></div>
          <div><span>Sent at</span><strong>${formatDateTime(match.created_at)}</strong></div>
          <div><span>Expires</span><strong>${formatDateTime(match.invitation_expires_at)}</strong></div>
        </div>
        <div class="battleship-actions-row">
          <button type="button" class="btn-ghost" data-bs-action="cancel-invite" ${state.busy || !match.viewer?.can_cancel ? "disabled" : ""}>Cancel invite</button>
          <button type="button" class="btn-ghost" data-bs-action="refresh-lobby">Refresh</button>
        </div>
      </div>
    `;
  }

  function renderPlacementStage() {
    const match = state.match;
    const officeBlocked = match.office_policy?.blocked;
    const viewerReady = Boolean(match.viewer?.placement_ready);
    setStageHeader(
      officeBlocked ? "Ship placement paused" : "Ship placement",
      officeBlocked
        ? "Game paused due to office peak hours. Fleet changes are locked until play resumes."
        : viewerReady
          ? "Your fleet is locked. Waiting for your opponent to finish."
          : "Place all five ships on your 10x10 board, then lock in your fleet.",
    );

    elements.stage.innerHTML = `
      <div class="battleship-placement">
        <div class="battleship-card">
          <div class="battleship-card-head">
            <div>
              <p class="widget-kicker">Your fleet</p>
              <h3>Placement board</h3>
            </div>
            <div class="battleship-actions-row">
              <button type="button" class="btn-ghost" data-bs-action="rotate-placement" ${viewerReady || officeBlocked ? "disabled" : ""}>
                Rotate: ${escapeHtml(titleCase(state.orientation))}
              </button>
              <button type="button" class="btn-ghost" data-bs-action="randomize-layout" ${viewerReady || officeBlocked ? "disabled" : ""}>Auto-place</button>
              <button type="button" class="btn-ghost" data-bs-action="reset-layout" ${viewerReady || officeBlocked ? "disabled" : ""}>Reset</button>
            </div>
          </div>
          <div class="battleship-ship-selector">
            ${renderShipSelector()}
          </div>
          <div class="battleship-board-shell">
            ${renderPlacementGrid()}
          </div>
          <div class="battleship-actions-row">
            <button type="button" class="btn-warm" data-bs-action="submit-placement" ${
              state.busy || viewerReady || officeBlocked || state.draft.length !== 5 ? "disabled" : ""
            }>Lock fleet</button>
            <span class="battleship-inline-note">${
              viewerReady
                ? "Fleet locked. Waiting for opponent."
                : `${state.draft.length}/5 ships placed`
            }</span>
          </div>
        </div>
        <div class="battleship-card">
          <p class="widget-kicker">Match readiness</p>
          <h3>${escapeHtml(match.opponent.name)}</h3>
          <div class="battleship-meta-list">
            <div><span>Your status</span><strong>${viewerReady ? "Ready" : "Placing ships"}</strong></div>
            <div><span>Opponent</span><strong>${match.opponent.placement_ready ? "Ready" : "Still placing"}</strong></div>
            <div><span>Turn rule</span><strong>Server decides first turn after both fleets lock</strong></div>
          </div>
          <div class="muted-copy">
            Refreshing or reconnecting will not lose the match. Only the unsaved local placement draft changes until you lock your fleet.
          </div>
        </div>
      </div>
    `;
  }

  function renderBattleStage() {
    const match = state.match;
    const completed = isFinishedPhase(match);
    const paused = match.status === "paused_office_hours";
    setStageHeader(
      completed
        ? "Match complete"
        : paused
          ? "Match paused"
          : "Live battle",
      completed
        ? `${match.winner?.name || "Winner"} finished the match in ${match.total_turns} turns.`
        : paused
          ? "Game paused due to office peak hours. No moves may be made until allowed hours resume."
          : match.turn_status,
    );

    elements.stage.innerHTML = `
      <div class="battleship-battle">
        <div class="battleship-match-banner ${completed ? "completed" : paused ? "paused" : "active"}">
          <div>
            <p class="widget-kicker">Match status</p>
            <h3>${escapeHtml(match.status_label)}</h3>
            <p>${escapeHtml(match.turn_status)}</p>
          </div>
          <div class="battleship-actions-row">
            ${
              match.viewer?.can_resign
                ? `<button type="button" class="btn-ghost" data-bs-action="resign-match" ${state.busy ? "disabled" : ""}>Resign</button>`
                : ""
            }
            ${
              match.viewer?.can_rematch
                ? `<button type="button" class="btn-warm" data-bs-action="request-rematch" ${state.busy ? "disabled" : ""}>Request rematch</button>`
                : ""
            }
          </div>
        </div>
        <div class="battleship-board-duo">
          <div class="battleship-board-card">
            <div class="battleship-board-head">
              <div>
                <p class="widget-kicker">Your fleet</p>
                <h3>${escapeHtml(state.currentUser.name)}</h3>
              </div>
            </div>
            ${renderOwnBattleGrid()}
          </div>
          <div class="battleship-board-card">
            <div class="battleship-board-head">
              <div>
                <p class="widget-kicker">Target board</p>
                <h3>${escapeHtml(match.opponent.name)}</h3>
              </div>
              <div class="mini-item-meta">${
                match.viewer?.can_fire
                  ? "Click one cell to fire."
                  : completed
                    ? "Match finished."
                    : paused
                      ? "Waiting for allowed hours."
                      : "Waiting for opponent."
              }</div>
            </div>
            ${renderTargetGrid()}
          </div>
        </div>
      </div>
    `;
  }

  function renderRulesCard() {
    if (!elements.rulesCard) {
      return;
    }
    const windows = (state.lobby?.office_policy?.windows || [
      { label: "10:00 AM - 01:00 PM" },
      { label: "02:00 PM - 06:30 PM" },
    ]).map((item) => item.label);
    elements.rulesCard.innerHTML = `
      <p class="widget-kicker">Rules</p>
      <h3>Quick rules</h3>
      <ul class="battleship-rules-list">
        <li>2 players only.</li>
        <li>Only 1 live match can run across Connect at a time.</li>
        <li>No play during office hours: ${escapeHtml(windows.join(" and "))}.</li>
        <li>A paused match resumes automatically after blocked hours.</li>
        <li>One turn means one shot.</li>
        <li>Sink all enemy ships to win.</li>
      </ul>
    `;
  }

  function renderAlert() {
    if (!elements.alert) {
      return;
    }
    if (!state.alert) {
      elements.alert.hidden = true;
      elements.alert.textContent = "";
      elements.alert.className = "battleship-alert";
      return;
    }
    elements.alert.hidden = false;
    elements.alert.className = `battleship-alert ${state.alert.type}`;
    elements.alert.textContent = state.alert.message;
  }

  function renderCandidateResults() {
    const blocked = Boolean(state.lobby?.office_policy?.blocked);
    const query = String(state.inviteQuery || "").trim();
    const candidates = state.lobby?.candidate_people || [];
    if (query.length < 2) {
      return `<div class="muted-copy">Type at least 2 characters to search and select one employee.</div>`;
    }
    if (!candidates.length) {
      return `<div class="muted-copy">No employee matches found for this search yet.</div>`;
    }
    return candidates
      .map(
        (person) => `
          <article class="battleship-candidate">
            <div>
              <h4>${escapeHtml(person.name)}</h4>
              <div class="mini-item-meta">${escapeHtml([person.title, person.location, person.department].filter(Boolean).join(" | "))}</div>
            </div>
            <button type="button" class="btn-ghost" data-bs-action="invite-user" data-user-id="${person.id}" ${
              blocked || state.busy ? "disabled" : ""
            }>Invite</button>
          </article>
        `,
      )
      .join("");
  }

  function renderInviteList(label, matches) {
    return `
      <div class="battleship-invite-list-block">
        <div class="battleship-invite-list-title">${escapeHtml(label)}</div>
        ${
          matches && matches.length
            ? `<div class="battleship-invite-mini-list">${matches
                .map(
                  (match) => `
                    <article class="battleship-mini-match">
                      <strong>${escapeHtml(
                        label === "Incoming" ? match.players.inviter.name : match.players.invitee.name,
                      )}</strong>
                      <span>${escapeHtml(match.status_label)}</span>
                    </article>
                  `,
                )
                .join("")}</div>`
            : `<div class="muted-copy">No ${label.toLowerCase()} invitations.</div>`
        }
      </div>
    `;
  }

  function renderGlobalSlotNotice(match) {
    return `
      <div class="battleship-slot-notice">
        <p class="widget-kicker">Single active-slot rule</p>
        <h3>One intranet match is already in progress</h3>
        <p>${escapeHtml(match.players.inviter.name)} vs ${escapeHtml(match.players.invitee.name)} currently occupies the live Battleship slot.</p>
      </div>
    `;
  }

  function renderShipSelector() {
    const placedTypes = new Set((state.draft || []).map((ship) => ship.ship_type));
    const fleet = state.match?.fleet_spec || [];
    return fleet
      .map((ship) => {
        const isSelected = ship.ship_type === state.selectedShipType;
        const isPlaced = placedTypes.has(ship.ship_type);
        return `
          <button
            type="button"
            class="battleship-ship-pill ${isSelected ? "active" : ""} ${isPlaced ? "placed" : ""}"
            data-bs-action="select-ship"
            data-ship-type="${ship.ship_type}"
          >
            ${escapeHtml(ship.label)} · ${ship.size}
          </button>
        `;
      })
      .join("");
  }

  function renderPlacementGrid() {
    const shipMap = new Map();
    state.draft.forEach((ship) => {
      ship.cells.forEach((cell) => {
        shipMap.set(`${cell.row}:${cell.col}`, ship.ship_type);
      });
    });
    return renderGrid((row, col) => {
      const shipType = shipMap.get(`${row}:${col}`);
      const selected = shipType && shipType === state.selectedShipType;
      return `
        <button
          type="button"
          class="battleship-cell ${shipType ? "ship" : ""} ${selected ? "selected" : ""}"
          data-bs-action="place-cell"
          data-row="${row}"
          data-col="${col}"
          ${state.busy ? "disabled" : ""}
        >${shipType ? escapeHtml(shipType.slice(0, 1).toUpperCase()) : ""}</button>
      `;
    });
  }

  function renderOwnBattleGrid() {
    const shipMap = new Map();
    const shotMap = new Map();
    const ships = state.match?.own_board?.ships || [];
    const shotsReceived = state.match?.own_board?.shots_received || [];
    ships.forEach((ship) => {
      ship.cells.forEach((cell) => {
        shipMap.set(`${cell.row}:${cell.col}`, {
          shipType: ship.ship_type,
          sunk: Boolean(ship.sunk),
        });
      });
    });
    shotsReceived.forEach((shot) => {
      shotMap.set(`${shot.row}:${shot.col}`, shot.result);
    });

    return renderGrid((row, col) => {
      const ship = shipMap.get(`${row}:${col}`);
      const shotResult = shotMap.get(`${row}:${col}`);
      const classes = ["battleship-cell"];
      let content = "";
      if (ship) {
        classes.push("ship");
        if (ship.sunk) {
          classes.push("sunk");
        }
        content = escapeHtml(ship.shipType.slice(0, 1).toUpperCase());
      }
      if (shotResult === "miss") {
        classes.push("miss");
        content = "•";
      }
      if (shotResult === "hit") {
        classes.push("hit");
        content = "×";
      }
      if (shotResult === "sunk") {
        classes.push("sunk");
        content = "×";
      }
      return `<div class="${classes.join(" ")}">${content}</div>`;
    });
  }

  function renderTargetGrid() {
    const shots = state.match?.target_board?.shots || [];
    const revealedSunkCells = state.match?.target_board?.revealed_sunk_cells || [];
    const shotMap = new Map();
    const sunkCellMap = new Set();
    shots.forEach((shot) => {
      shotMap.set(`${shot.row}:${shot.col}`, shot.result);
    });
    revealedSunkCells.forEach((cell) => {
      sunkCellMap.add(`${cell.row}:${cell.col}`);
    });

    const canFire = Boolean(state.match?.viewer?.can_fire) && !state.busy;
    return renderGrid((row, col) => {
      const key = `${row}:${col}`;
      const shotResult = shotMap.get(key);
      const isSunk = sunkCellMap.has(key);
      const classes = ["battleship-cell", "target-board"];
      let content = "";
      if (isSunk) {
        classes.push("sunk");
        content = "×";
      } else if (shotResult === "miss") {
        classes.push("miss");
        content = "•";
      } else if (shotResult === "hit" || shotResult === "sunk") {
        classes.push("hit");
        content = "×";
      } else if (canFire) {
        classes.push("targetable");
      }

      if (!shotResult && canFire) {
        return `
          <button
            type="button"
            class="${classes.join(" ")}"
            data-bs-action="fire-cell"
            data-row="${row}"
            data-col="${col}"
          ></button>
        `;
      }
      return `<div class="${classes.join(" ")}">${content}</div>`;
    });
  }

  function renderGrid(cellRenderer) {
    let html = '<div class="battleship-grid">';
    html += '<div class="battleship-grid-axis corner"></div>';
    for (let col = 0; col < BOARD_SIZE; col += 1) {
      html += `<div class="battleship-grid-axis">${col + 1}</div>`;
    }
    for (let row = 0; row < BOARD_SIZE; row += 1) {
      html += `<div class="battleship-grid-axis">${ROW_LABELS[row]}</div>`;
      for (let col = 0; col < BOARD_SIZE; col += 1) {
        html += cellRenderer(row, col);
      }
    }
    html += "</div>";
    return html;
  }

  function hydrateDraftFromMatch() {
    if (!state.match) {
      state.draft = [];
      return;
    }
    const persisted = loadPersistedDraft();
    const serverShips = normalizeShipsFromServer(state.match.own_board?.ships || []);
    if (state.match.viewer?.placement_ready && serverShips.length) {
      state.draft = serverShips;
      clearPersistedDraft();
    } else if (persisted.length) {
      state.draft = persisted;
    } else {
      state.draft = serverShips;
    }
    ensureSelectedShip();
  }

  function normalizeShipsFromServer(ships) {
    return (ships || []).map((ship) => ({
      ship_type: ship.ship_type,
      label: ship.label,
      size: ship.size,
      row: ship.row,
      col: ship.col,
      orientation: ship.orientation,
      cells: (ship.cells || []).map((cell) => ({
        row: cell.row,
        col: cell.col,
        label: cell.label,
      })),
    }));
  }

  function placeSelectedShip(row, col) {
    if (!state.match || !isPlacementPhase(state.match) || state.match.viewer?.placement_ready) {
      return;
    }
    const spec = getShipSpec(state.selectedShipType);
    if (!spec) {
      return;
    }
    const nextDraft = state.draft.filter((ship) => ship.ship_type !== state.selectedShipType);
    try {
      const ship = buildDraftShip(spec, row, col, state.orientation);
      ensureNoOverlap(nextDraft, ship);
      nextDraft.push(ship);
      state.draft = sortDraft(nextDraft);
      persistDraft();
      ensureSelectedShip();
      clearAlert();
      render();
    } catch (error) {
      setAlert(error.message || "That ship placement is not valid.", "error");
      render();
    }
  }

  function buildDraftShip(spec, row, col, orientation) {
    const cells = [];
    for (let offset = 0; offset < spec.size; offset += 1) {
      const targetRow = orientation === "vertical" ? row + offset : row;
      const targetCol = orientation === "horizontal" ? col + offset : col;
      if (
        targetRow < 0 ||
        targetRow >= BOARD_SIZE ||
        targetCol < 0 ||
        targetCol >= BOARD_SIZE
      ) {
        throw new Error("Ships cannot go outside the 10x10 board.");
      }
      cells.push({
        row: targetRow,
        col: targetCol,
        label: `${ROW_LABELS[targetRow]}${targetCol + 1}`,
      });
    }
    return {
      ship_type: spec.ship_type,
      label: spec.label,
      size: spec.size,
      row,
      col,
      orientation,
      cells,
    };
  }

  function ensureNoOverlap(existingShips, newShip) {
    const occupied = new Set();
    existingShips.forEach((ship) => {
      ship.cells.forEach((cell) => {
        occupied.add(`${cell.row}:${cell.col}`);
      });
    });
    const overlappingCell = newShip.cells.find((cell) => occupied.has(`${cell.row}:${cell.col}`));
    if (overlappingCell) {
      throw new Error(`Ships cannot overlap at ${overlappingCell.label}.`);
    }
  }

  function generateRandomFleet() {
    const specList = getFleetSpec();
    for (let attempt = 0; attempt < 200; attempt += 1) {
      const nextDraft = [];
      let failed = false;
      for (const spec of specList) {
        let placed = false;
        for (let innerAttempt = 0; innerAttempt < 100; innerAttempt += 1) {
          const orientation = Math.random() > 0.5 ? "horizontal" : "vertical";
          const row = Math.floor(Math.random() * BOARD_SIZE);
          const col = Math.floor(Math.random() * BOARD_SIZE);
          try {
            const ship = buildDraftShip(spec, row, col, orientation);
            ensureNoOverlap(nextDraft, ship);
            nextDraft.push(ship);
            placed = true;
            break;
          } catch (error) {
            // Try another coordinate.
          }
        }
        if (!placed) {
          failed = true;
          break;
        }
      }
      if (!failed && nextDraft.length === specList.length) {
        return sortDraft(nextDraft);
      }
    }
    return [];
  }

  function persistDraft() {
    if (!state.match?.id) {
      return;
    }
    try {
      window.localStorage.setItem(
        `${DRAFT_STORAGE_PREFIX}${state.match.id}`,
        JSON.stringify(state.draft.map(stripDraftForSubmit)),
      );
    } catch (error) {
      // Ignore local storage failures.
    }
  }

  function clearPersistedDraft() {
    if (!state.match?.id) {
      return;
    }
    try {
      window.localStorage.removeItem(`${DRAFT_STORAGE_PREFIX}${state.match.id}`);
    } catch (error) {
      // Ignore local storage failures.
    }
  }

  function loadPersistedDraft() {
    if (!state.match?.id) {
      return [];
    }
    try {
      const raw = window.localStorage.getItem(`${DRAFT_STORAGE_PREFIX}${state.match.id}`);
      if (!raw) {
        return [];
      }
      const payload = JSON.parse(raw);
      return payload.map((ship) => {
        const spec = getShipSpec(ship.ship_type);
        return buildDraftShip(spec, Number(ship.row), Number(ship.col), ship.orientation);
      });
    } catch (error) {
      return [];
    }
  }

  function stripDraftForSubmit(ship) {
    return {
      ship_type: ship.ship_type,
      row: ship.row,
      col: ship.col,
      orientation: ship.orientation,
    };
  }

  function ensureSelectedShip() {
    const placed = new Set((state.draft || []).map((ship) => ship.ship_type));
    const nextOpen = getFleetSpec().find((ship) => !placed.has(ship.ship_type));
    if (!state.selectedShipType || !getShipSpec(state.selectedShipType)) {
      state.selectedShipType = nextOpen?.ship_type || getFleetSpec()[0]?.ship_type || "carrier";
      return;
    }
    if (!placed.has(state.selectedShipType)) {
      return;
    }
    state.selectedShipType = nextOpen?.ship_type || state.selectedShipType;
  }

  function getFleetSpec() {
    return state.match?.fleet_spec || [
      { ship_type: "carrier", label: "Carrier", size: 5 },
      { ship_type: "battleship", label: "Battleship", size: 4 },
      { ship_type: "cruiser", label: "Cruiser", size: 3 },
      { ship_type: "submarine", label: "Submarine", size: 3 },
      { ship_type: "destroyer", label: "Destroyer", size: 2 },
    ];
  }

  function getShipSpec(shipType) {
    return getFleetSpec().find((ship) => ship.ship_type === shipType);
  }

  function sortDraft(draft) {
    return [...draft].sort(
      (left, right) => FLEET_ORDER.indexOf(left.ship_type) - FLEET_ORDER.indexOf(right.ship_type),
    );
  }

  function isViewerInMatch(match) {
    if (!state.currentUser || !match?.players) {
      return false;
    }
    return [match.players.inviter?.id, match.players.invitee?.id].includes(state.currentUser.id);
  }

  function isPlacementPhase(match) {
    if (!match) {
      return false;
    }
    return match.status === "ship_placement" || (
      match.status === "paused_office_hours" && match.paused_from_status === "ship_placement"
    );
  }

  function isFinishedPhase(match) {
    return match && ["completed", "resigned", "abandoned"].includes(match.status);
  }

  function setAlert(message, type = "info") {
    state.alert = message ? { message, type } : null;
  }

  function clearAlert() {
    state.alert = null;
  }

  function setStageHeader(title, meta) {
    if (elements.stageTitle) {
      elements.stageTitle.textContent = title;
    }
    if (elements.stageMeta) {
      elements.stageMeta.textContent = meta;
    }
  }

  function renderLoadingStage() {
    return `
      <div class="battleship-card">
        <p class="widget-kicker">Loading</p>
        <h3>Preparing the game lobby</h3>
        <p class="muted-copy">Fetching office-hours policy, current slot status and your latest Battleship state.</p>
      </div>
    `;
  }

  function renderLoadingMiniCard() {
    return `
      <p class="widget-kicker">Loading</p>
      <h3>Just a moment</h3>
      <p class="muted-copy">Fetching the latest Battleship state.</p>
    `;
  }

  function titleCase(value) {
    return String(value || "")
      .replace(/_/g, " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase());
  }

  function formatDateTime(value) {
    if (!value) {
      return "";
    }
    const parsed = new Date(value);
    if (Number.isNaN(parsed.getTime())) {
      return String(value);
    }
    return parsed.toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      hour: "numeric",
      minute: "2-digit",
    });
  }

  function formatDuration(totalSeconds) {
    const seconds = Number(totalSeconds || 0);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    if (hours) {
      return `${hours}h ${minutes % 60}m`;
    }
    return `${minutes}m`;
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }
})();
