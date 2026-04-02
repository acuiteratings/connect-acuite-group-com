(function attachAdminConsole() {
  const state = {
    currentUser: null,
    users: [],
    exitProcesses: [],
    celebrations: {
      birthdays: [],
      anniversaries: [],
    },
    previews: {
      birthday: null,
      anniversary: null,
    },
    selectedExitEmployeeId: 0,
    toastTimer: null,
  };

  let elements = {};

  document.addEventListener("DOMContentLoaded", () => {
    void initAdminConsole();
  });

  async function initAdminConsole() {
    const authenticatedUser = window.AcuiteConnectAuth && window.AcuiteConnectAuth.requireAuth
      ? await window.AcuiteConnectAuth.requireAuth({ loginPath: "/login.html?next=/admin-console.html" })
      : null;
    if (!authenticatedUser) {
      return;
    }
    if (!authenticatedUser.access_rights || !authenticatedUser.access_rights.can_administer) {
      window.location.href = "/";
      return;
    }

    state.currentUser = authenticatedUser;
    cacheElements();
    bindEvents();
    renderCurrentUser();
    await Promise.all([loadUsers(), loadExitProcesses(), loadCelebrations()]);
    renderAll();
  }

  function cacheElements() {
    elements = {
      userName: document.getElementById("admin-console-user-name"),
      toast: document.getElementById("admin-toast"),
      onboardForm: document.getElementById("admin-onboard-form"),
      exitSearchInput: document.getElementById("admin-exit-search"),
      exitSearchHelp: document.getElementById("admin-exit-search-help"),
      exitSearchResults: document.getElementById("admin-exit-search-results"),
      exitForm: document.getElementById("admin-exit-form"),
      exitEmployeeId: document.getElementById("admin-exit-employee-id"),
      exitSelectedUser: document.getElementById("admin-exit-selected-user"),
      exitProcessList: document.getElementById("admin-exit-process-list"),
      exitResultsMeta: document.getElementById("admin-exit-results-meta"),
      birthdayList: document.getElementById("admin-birthday-list"),
      birthdayResultsMeta: document.getElementById("admin-birthday-results-meta"),
      birthdayPreviewShell: document.getElementById("admin-birthday-preview-shell"),
      birthdayPreviewMeta: document.getElementById("admin-birthday-preview-meta"),
      anniversaryList: document.getElementById("admin-anniversary-list"),
      anniversaryResultsMeta: document.getElementById("admin-anniversary-results-meta"),
      anniversaryPreviewShell: document.getElementById("admin-anniversary-preview-shell"),
      anniversaryPreviewMeta: document.getElementById("admin-anniversary-preview-meta"),
      internalJobForm: document.getElementById("admin-internal-job-form"),
      vacancyForm: document.getElementById("admin-vacancy-form"),
      awardForm: document.getElementById("admin-award-form"),
      contestForm: document.getElementById("admin-contest-form"),
      sportsForm: document.getElementById("admin-sports-form"),
      quizForm: document.getElementById("admin-quiz-form"),
      debateForm: document.getElementById("admin-debate-form"),
    };
  }

  function bindEvents() {
    document.addEventListener("click", handleDocumentClick);
    document.addEventListener("submit", handleSubmit);
    if (elements.exitSearchInput) {
      elements.exitSearchInput.addEventListener("input", renderExitSearchResults);
    }
  }

  async function loadUsers() {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/accounts/access/users/");
    state.users = Array.isArray(payload.results) ? payload.results : [];
  }

  async function loadExitProcesses() {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/accounts/access/exit-processes/?status=open");
    state.exitProcesses = Array.isArray(payload.results) ? payload.results : [];
  }

  async function loadCelebrations() {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/ops/celebrations/today/");
    state.celebrations.birthdays = Array.isArray(payload.birthdays) ? payload.birthdays : [];
    state.celebrations.anniversaries = Array.isArray(payload.anniversaries) ? payload.anniversaries : [];
  }

  function renderAll() {
    renderExitSearchResults();
    renderExitProcessList();
    syncExitForm();
    renderCelebrationSections();
  }

  function renderCurrentUser() {
    if (!elements.userName || !state.currentUser) {
      return;
    }
    elements.userName.textContent = state.currentUser.name || state.currentUser.email;
  }

  function handleDocumentClick(event) {
    const action = event.target.closest("[data-action]");
    if (!action) {
      return;
    }

    if (action.dataset.action === "logout-admin-console") {
      void logout();
      return;
    }

    if (action.dataset.action === "open-connect-app") {
      window.location.href = "/";
      return;
    }

    if (action.dataset.action === "select-exit-employee") {
      state.selectedExitEmployeeId = Number(action.dataset.id || 0);
      const selectedUser = state.users.find((user) => user.id === state.selectedExitEmployeeId);
      if (selectedUser && elements.exitSearchInput) {
        elements.exitSearchInput.value = selectedUser.name || selectedUser.email || "";
      }
      syncExitForm();
      renderExitSearchResults();
      return;
    }

    if (action.dataset.action === "select-exit-process") {
      state.selectedExitEmployeeId = Number(action.dataset.id || 0);
      syncExitForm();
      renderExitProcessList();
      return;
    }

    if (action.dataset.action === "finalize-exit-process") {
      void submitExitProcess({ finalize: true });
      return;
    }

    if (action.dataset.action === "generate-celebration-card") {
      void generateCelebrationPreview(action.dataset.kind, Number(action.dataset.userId || 0));
      return;
    }

    if (action.dataset.action === "post-celebration-card") {
      void publishCelebrationPreview(action.dataset.kind);
      return;
    }
  }

  function handleSubmit(event) {
    if (event.target === elements.onboardForm) {
      event.preventDefault();
      void submitOnboarding();
      return;
    }

    if (event.target === elements.exitForm) {
      event.preventDefault();
      void submitExitProcess({ finalize: false });
      return;
    }

    if (event.target === elements.internalJobForm) {
      event.preventDefault();
      void submitInternalJob();
      return;
    }

    if (event.target === elements.vacancyForm) {
      event.preventDefault();
      void submitVacancy();
      return;
    }

    if (event.target === elements.awardForm) {
      event.preventDefault();
      void submitAwardAnnouncement();
      return;
    }

    if (event.target === elements.contestForm) {
      event.preventDefault();
      void submitContestAnnouncement();
      return;
    }

    if (event.target === elements.sportsForm) {
      event.preventDefault();
      void submitSportsAnnouncement();
      return;
    }

    if (event.target === elements.quizForm) {
      event.preventDefault();
      void submitQuizAnnouncement();
      return;
    }

    if (event.target === elements.debateForm) {
      event.preventDefault();
      void submitDebateAnnouncement();
    }
  }

  function renderExitSearchResults() {
    if (!elements.exitSearchResults) {
      return;
    }
    const query = String(elements.exitSearchInput?.value || "").trim().toLowerCase();
    if (elements.exitSearchHelp) {
      elements.exitSearchHelp.textContent = query.length >= 2
        ? "Select the right employee from the search results below."
        : "Type at least 2 characters to search and select an employee.";
    }
    if (query.length < 2) {
      elements.exitSearchResults.hidden = true;
      elements.exitSearchResults.innerHTML = "";
      return;
    }

    const results = state.users
      .filter((user) => user.employment_status !== "alumni")
      .filter((user) => {
        return [
          user.name,
          user.email,
          user.title,
          user.department,
          user.location,
          user.employee_code,
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase()
          .includes(query);
      })
      .slice(0, 8);

    if (!results.length) {
      elements.exitSearchResults.hidden = false;
      elements.exitSearchResults.innerHTML = '<div class="admin-search-empty">No matching employee found.</div>';
      return;
    }

    elements.exitSearchResults.hidden = false;
    elements.exitSearchResults.innerHTML = results.map((user) => `
      <button
        type="button"
        class="admin-search-result ${state.selectedExitEmployeeId === user.id ? "active" : ""}"
        data-action="select-exit-employee"
        data-id="${user.id}"
      >
        <div class="admin-search-result-head">
          <strong>${escapeHtml(user.name || user.email)}</strong>
          <span class="admin-process-stage">${escapeHtml(capitalize(user.access_level || "employee"))}</span>
        </div>
        <div class="admin-search-result-meta">${escapeHtml([user.title, user.location, user.email].filter(Boolean).join(" | "))}</div>
      </button>
    `).join("");
  }

  function renderExitProcessList() {
    if (!elements.exitProcessList || !elements.exitResultsMeta) {
      return;
    }
    elements.exitResultsMeta.textContent = state.exitProcesses.length
      ? `${state.exitProcesses.length} open workflow${state.exitProcesses.length === 1 ? "" : "s"}`
      : "No open workflows";

    if (!state.exitProcesses.length) {
      elements.exitProcessList.innerHTML = '<div class="admin-selected-user">No exit workflows are open right now.</div>';
      return;
    }

    elements.exitProcessList.innerHTML = state.exitProcesses.map((process) => `
      <button
        type="button"
        class="admin-process-card ${state.selectedExitEmployeeId === process.employee.id ? "active" : ""}"
        data-action="select-exit-process"
        data-id="${process.employee.id}"
      >
        <div class="admin-process-card-head">
          <strong>${escapeHtml(process.employee.name || process.employee.email)}</strong>
          <span class="admin-process-stage">${escapeHtml(formatStageLabel(process.stage))}</span>
        </div>
        <div class="admin-process-card-meta">
          ${escapeHtml([process.employee.title, process.employee.location].filter(Boolean).join(" | ") || process.employee.email)}
        </div>
        <div class="admin-process-card-meta">Last working day: ${escapeHtml(formatDateLabel(process.last_working_day))}</div>
        <div class="admin-process-flags">
          ${process.resignation_acknowledged ? '<span class="admin-flag">Notice</span>' : ""}
          ${process.knowledge_transfer_completed ? '<span class="admin-flag">KT done</span>' : ""}
          ${process.assets_returned ? '<span class="admin-flag">Assets back</span>' : ""}
          ${process.access_review_completed ? '<span class="admin-flag">Access reviewed</span>' : ""}
        </div>
      </button>
    `).join("");
  }

  function renderCelebrationSections() {
    renderCelebrationList("birthday");
    renderCelebrationList("anniversary");
    renderCelebrationPreview("birthday");
    renderCelebrationPreview("anniversary");
  }

  function renderCelebrationList(kind) {
    const list = kind === "birthday" ? elements.birthdayList : elements.anniversaryList;
    const meta = kind === "birthday" ? elements.birthdayResultsMeta : elements.anniversaryResultsMeta;
    if (!list || !meta) {
      return;
    }
    const items = kind === "birthday" ? state.celebrations.birthdays : state.celebrations.anniversaries;
    meta.textContent = items.length
      ? `${items.length} employee${items.length === 1 ? "" : "s"} today`
      : "No employees for today";
    if (!items.length) {
      list.innerHTML = `<div class="celebration-empty">No ${kind === "birthday" ? "birthdays" : "anniversaries"} fall today.</div>`;
      return;
    }
    list.innerHTML = items.map((item) => `
      <article class="celebration-row">
        <div class="celebration-row-head">
          <div>
            <h4>${escapeHtml(item.name)}</h4>
            <p>${escapeHtml([item.title, item.department || item.team_label, item.email].filter(Boolean).join(" | "))}</p>
          </div>
          <span class="admin-process-stage">${escapeHtml(kind === "birthday" ? "Birthday" : "Anniversary")}</span>
        </div>
        <div class="celebration-row-meta">
          <span class="admin-flag">${escapeHtml(item.date_label)}</span>
          ${item.years_completed ? `<span class="admin-flag">${escapeHtml(`${item.years_completed} years`)}</span>` : ""}
        </div>
        <div class="celebration-preview-actions">
          <button type="button" class="admin-btn admin-btn-secondary" data-action="generate-celebration-card" data-kind="${kind}" data-user-id="${item.user_id}">Generate card</button>
        </div>
      </article>
    `).join("");
  }

  function renderCelebrationPreview(kind) {
    const preview = state.previews[kind];
    const shell = kind === "birthday" ? elements.birthdayPreviewShell : elements.anniversaryPreviewShell;
    const meta = kind === "birthday" ? elements.birthdayPreviewMeta : elements.anniversaryPreviewMeta;
    if (!shell || !meta) {
      return;
    }
    if (!preview) {
      meta.textContent = "Choose a person to generate a card.";
      shell.innerHTML = `<div class="admin-selected-user">Choose ${kind === "birthday" ? "a birthday" : "an anniversary"} entry and click Generate card.</div>`;
      return;
    }
    meta.textContent = `${preview.name} | ${preview.template_label || preview.template_file}`;
    shell.innerHTML = `
      <div class="celebration-preview-card">
        ${renderCelebrationCard(preview.card)}
        <div class="celebration-preview-details">
          <h4>${escapeHtml(preview.title)}</h4>
          <p>${escapeHtml(preview.body)}</p>
          <div class="celebration-row-meta">
            ${preview.meta_lines.map((line) => `<span class="admin-flag">${escapeHtml(line)}</span>`).join("")}
          </div>
        </div>
        <div class="celebration-preview-actions">
          <button type="button" class="admin-btn admin-btn-secondary" data-action="generate-celebration-card" data-kind="${kind}" data-user-id="${preview.user_id}">Regenerate</button>
          <button type="button" class="admin-btn admin-btn-primary" data-action="post-celebration-card" data-kind="${kind}">Post</button>
        </div>
      </div>
    `;
  }

  function renderCelebrationCard(card) {
    if (!card) {
      return "";
    }
    const photo = String(card.photo_url || "").trim();
    return `
      <div class="celebration-native-card celebration-style-${escapeHtml(card.style_key || "sunrise")}">
        <div class="celebration-native-card-top">
          <span class="celebration-native-kicker">${escapeHtml(card.occasion_label || "Celebration")}</span>
          <span class="celebration-native-date">${escapeHtml(card.date_label || "")}</span>
        </div>
        <div class="celebration-native-person">
          ${
            photo
              ? `<img src="${escapeHtml(photo)}" alt="${escapeHtml(card.person_name || "Employee")}" class="celebration-native-photo">`
              : `<div class="celebration-native-photo celebration-native-photo-fallback">${escapeHtml(card.initials || "AC")}</div>`
          }
          <div>
            <h3>${escapeHtml(card.person_name || "")}</h3>
            <p>${escapeHtml(card.person_role || "")}</p>
          </div>
        </div>
        <div class="celebration-native-message">${escapeHtml(card.message || "")}</div>
      </div>
    `;
  }

  async function generateCelebrationPreview(kind, userId) {
    if (!userId) {
      return;
    }
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest("/api/ops/celebrations/preview/", {
        method: "POST",
        body: { kind, user_id: userId },
      });
      state.previews[kind] = payload.preview || null;
      renderCelebrationPreview(kind);
      showToast("Card generated. Review it before posting.");
    } catch (error) {
      showToast(error.message || "Could not generate the celebration card.");
    }
  }

  async function publishCelebrationPreview(kind) {
    const preview = state.previews[kind];
    if (!preview) {
      showToast("Generate a card first.");
      return;
    }
    try {
      await window.AcuiteConnectAuth.apiRequest("/api/ops/celebrations/publish/", {
        method: "POST",
        body: {
          kind,
          user_id: preview.user_id,
          template_file: preview.template_file,
        },
      });
      state.previews[kind] = null;
      await loadCelebrations();
      renderCelebrationSections();
      showToast(`${kind === "birthday" ? "Birthday" : "Anniversary"} post published to the bulletin board.`);
    } catch (error) {
      showToast(error.message || "Could not publish the celebration post.");
    }
  }

  function syncExitForm() {
    if (!elements.exitForm || !elements.exitEmployeeId || !elements.exitSelectedUser) {
      return;
    }

    const selectedUser = state.users.find((user) => user.id === state.selectedExitEmployeeId) || null;
    const selectedProcess = state.exitProcesses.find((item) => item.employee.id === state.selectedExitEmployeeId) || null;

    if (!selectedUser) {
      elements.exitForm.reset();
      elements.exitEmployeeId.value = "";
      elements.exitSelectedUser.textContent = "Select an employee to start or continue an exit workflow.";
      return;
    }

    elements.exitEmployeeId.value = String(selectedUser.id);
    elements.exitSelectedUser.textContent = [
      selectedUser.name || selectedUser.email,
      selectedUser.title,
      selectedUser.location,
      selectedUser.email,
    ].filter(Boolean).join(" | ");

    elements.exitForm.elements.resignation_date.value = selectedProcess?.resignation_date || "";
    elements.exitForm.elements.last_working_day.value = selectedProcess?.last_working_day || "";
    elements.exitForm.elements.stage.value = selectedProcess?.stage || "notice_received";
    elements.exitForm.elements.resignation_acknowledged.checked = Boolean(selectedProcess?.resignation_acknowledged);
    elements.exitForm.elements.knowledge_transfer_completed.checked = Boolean(selectedProcess?.knowledge_transfer_completed);
    elements.exitForm.elements.assets_returned.checked = Boolean(selectedProcess?.assets_returned);
    elements.exitForm.elements.access_review_completed.checked = Boolean(selectedProcess?.access_review_completed);
    elements.exitForm.elements.notes.value = selectedProcess?.notes || "";
  }

  async function submitOnboarding() {
    const formData = new FormData(elements.onboardForm);
    const payload = {
      display_name: String(formData.get("display_name") || "").trim(),
      email: String(formData.get("email") || "").trim(),
      company_name: String(formData.get("company_name") || "").trim(),
      employee_code: String(formData.get("employee_code") || "").trim(),
      title: String(formData.get("title") || "").trim(),
      department: String(formData.get("department") || "").trim(),
      function_name: String(formData.get("function_name") || "").trim(),
      location: String(formData.get("location") || "").trim(),
      office_location: String(formData.get("location") || "").trim(),
      city: String(formData.get("location") || "").trim(),
      mobile_number: String(formData.get("mobile_number") || "").trim(),
      phone_number: String(formData.get("mobile_number") || "").trim(),
      access_level: String(formData.get("access_level") || "employee").trim(),
      can_post_in_connect: formData.get("can_post_in_connect") === "on",
      employment_status: "active",
    };

    try {
      await window.AcuiteConnectAuth.apiRequest("/api/accounts/access/users/", {
        method: "POST",
        body: payload,
      });
      elements.onboardForm.reset();
      await loadUsers();
      renderExitSearchResults();
      showToast(`Employee account created for ${payload.email}.`);
    } catch (error) {
      showToast(error.message || "Could not create the employee account.");
    }
  }

  async function submitExitProcess({ finalize }) {
    const formData = new FormData(elements.exitForm);
    const employeeId = Number(formData.get("employee_id") || 0);
    if (!employeeId) {
      showToast("Select an employee before saving the exit workflow.");
      return;
    }

    const payload = {
      employee_id: employeeId,
      resignation_date: String(formData.get("resignation_date") || "").trim(),
      last_working_day: String(formData.get("last_working_day") || "").trim(),
      stage: String(formData.get("stage") || "notice_received").trim(),
      resignation_acknowledged: formData.get("resignation_acknowledged") === "on",
      knowledge_transfer_completed: formData.get("knowledge_transfer_completed") === "on",
      assets_returned: formData.get("assets_returned") === "on",
      access_review_completed: formData.get("access_review_completed") === "on",
      notes: String(formData.get("notes") || "").trim(),
      finalize,
    };

    if (finalize && !window.confirm("Convert this employee into alumni state now?")) {
      return;
    }

    try {
      await window.AcuiteConnectAuth.apiRequest("/api/accounts/access/exit-processes/", {
        method: "POST",
        body: payload,
      });
      await Promise.all([loadUsers(), loadExitProcesses()]);
      renderAll();
      showToast(finalize ? "Employee converted to alumni state." : "Exit workflow saved.");
    } catch (error) {
      showToast(error.message || "Could not save the exit workflow.");
    }
  }

  async function submitBirthdayWish() {
    const formData = new FormData(elements.birthdayForm);
    const employeeName = String(formData.get("employee_name") || "").trim();
    const teamLabel = String(formData.get("team_label") || "").trim();
    const occasionDate = String(formData.get("occasion_date") || "").trim();
    const note = String(formData.get("note") || "").trim();
    if (!employeeName || !note) {
      showToast("Add the employee name and the message before publishing.");
      return;
    }

    await publishBulletinPost({
      form: elements.birthdayForm,
      title: `Birthday wishes | ${employeeName}`,
      body: `Please join us in wishing ${employeeName} a very happy birthday.\n\n${note}`,
      category: "hr",
      templateKey: "birthday_wish",
      metadata: {
        bulletin_meta_lines: [teamLabel, occasionDate ? `Birthday: ${formatDateLabel(occasionDate)}` : ""].filter(Boolean),
      },
      successMessage: "Birthday wish published to the bulletin board.",
    });
  }

  async function submitWorkAnniversaryWish() {
    const formData = new FormData(elements.anniversaryForm);
    const employeeName = String(formData.get("employee_name") || "").trim();
    const yearsCompleted = String(formData.get("years_completed") || "").trim();
    const occasionDate = String(formData.get("occasion_date") || "").trim();
    const note = String(formData.get("note") || "").trim();
    if (!employeeName || !note) {
      showToast("Add the employee name and the message before publishing.");
      return;
    }

    await publishBulletinPost({
      form: elements.anniversaryForm,
      title: `Work anniversary | ${employeeName}`,
      body: `Please join us in celebrating ${employeeName}${yearsCompleted ? ` on completing ${yearsCompleted} year${yearsCompleted === "1" ? "" : "s"} with Acuité.` : " on this work anniversary."}\n\n${note}`,
      category: "hr",
      templateKey: "work_anniversary",
      metadata: {
        bulletin_meta_lines: [yearsCompleted ? `${yearsCompleted} years completed` : "", occasionDate ? `Date: ${formatDateLabel(occasionDate)}` : ""].filter(Boolean),
      },
      successMessage: "Work anniversary wish published to the bulletin board.",
    });
  }

  async function submitInternalJob() {
    const formData = new FormData(elements.internalJobForm);
    const roleTitle = String(formData.get("role_title") || "").trim();
    const teamName = String(formData.get("team_name") || "").trim();
    const location = String(formData.get("location") || "").trim();
    const closingDate = String(formData.get("closing_date") || "").trim();
    const ctaTarget = String(formData.get("cta_target") || "").trim();
    const note = String(formData.get("note") || "").trim();
    if (!roleTitle || !ctaTarget || !note) {
      showToast("Role title, apply target and role summary are required.");
      return;
    }

    await publishBulletinPost({
      form: elements.internalJobForm,
      title: `Internal job | ${roleTitle}`,
      body: note,
      category: "hr",
      templateKey: "internal_job",
      metadata: {
        bulletin_meta_lines: [teamName, location, closingDate ? `Apply by ${formatDateLabel(closingDate)}` : ""].filter(Boolean),
        bulletin_cta_label: "Apply now",
        bulletin_cta_target: normalizeActionTarget(ctaTarget),
      },
      successMessage: "Internal job post published to the bulletin board.",
    });
  }

  async function submitVacancy() {
    const formData = new FormData(elements.vacancyForm);
    const roleTitle = String(formData.get("role_title") || "").trim();
    const teamName = String(formData.get("team_name") || "").trim();
    const location = String(formData.get("location") || "").trim();
    const closingDate = String(formData.get("closing_date") || "").trim();
    const ctaTarget = String(formData.get("cta_target") || "").trim();
    const note = String(formData.get("note") || "").trim();
    if (!roleTitle || !ctaTarget || !note) {
      showToast("Role title, referral target and role summary are required.");
      return;
    }

    await publishBulletinPost({
      form: elements.vacancyForm,
      title: `Vacancy | ${roleTitle}`,
      body: note,
      category: "hr",
      templateKey: "vacancy",
      metadata: {
        bulletin_meta_lines: [teamName, location, closingDate ? `Refer by ${formatDateLabel(closingDate)}` : ""].filter(Boolean),
        bulletin_cta_label: "Refer CV",
        bulletin_cta_target: normalizeActionTarget(ctaTarget),
      },
      successMessage: "Vacancy post published to the bulletin board.",
    });
  }

  async function submitAwardAnnouncement() {
    const formData = new FormData(elements.awardForm);
    const headline = String(formData.get("headline") || "").trim();
    const subjectName = String(formData.get("subject_name") || "").trim();
    const eventDate = String(formData.get("event_date") || "").trim();
    const note = String(formData.get("note") || "").trim();
    if (!headline || !subjectName || !note) {
      showToast("Award title, awardee, and message are required.");
      return;
    }

    await publishBulletinPost({
      form: elements.awardForm,
      title: `Award | ${headline}`,
      body: `${subjectName} has been announced for ${headline}.\n\n${note}`,
      category: "celebration",
      templateKey: "award",
      metadata: {
        bulletin_meta_lines: [subjectName, eventDate ? `Award date: ${formatDateLabel(eventDate)}` : ""].filter(Boolean),
      },
      successMessage: "Award announcement published to the bulletin board.",
    });
  }

  async function submitContestAnnouncement() {
    await submitActionAnnouncement({
      form: elements.contestForm,
      prefix: "Contest",
      category: "engagement",
      templateKey: "contest",
      defaultActionLabel: "Join contest",
      successMessage: "Contest announcement published to the bulletin board.",
    });
  }

  async function submitSportsAnnouncement() {
    await submitActionAnnouncement({
      form: elements.sportsForm,
      prefix: "Sports event",
      category: "engagement",
      templateKey: "sports_event",
      defaultActionLabel: "Book a slot",
      successMessage: "Sports event published to the bulletin board.",
    });
  }

  async function submitQuizAnnouncement() {
    await submitActionAnnouncement({
      form: elements.quizForm,
      prefix: "Quiz",
      category: "engagement",
      templateKey: "quiz",
      defaultActionLabel: "Register now",
      successMessage: "Quiz announcement published to the bulletin board.",
    });
  }

  async function submitDebateAnnouncement() {
    await submitActionAnnouncement({
      form: elements.debateForm,
      prefix: "Debate",
      category: "engagement",
      templateKey: "debate",
      defaultActionLabel: "Join debate",
      successMessage: "Debate announcement published to the bulletin board.",
    });
  }

  async function submitActionAnnouncement({
    form,
    prefix,
    category,
    templateKey,
    defaultActionLabel,
    successMessage,
  }) {
    const formData = new FormData(form);
    const headline = String(formData.get("headline") || "").trim();
    const hostLabel = String(formData.get("host_label") || formData.get("location") || "").trim();
    const eventDate = String(formData.get("event_date") || "").trim();
    const ctaTarget = String(formData.get("cta_target") || "").trim();
    const ctaLabel = String(formData.get("cta_label") || defaultActionLabel).trim() || defaultActionLabel;
    const note = String(formData.get("note") || "").trim();
    if (!headline || !ctaTarget || !note) {
      showToast("Headline, action target, and message are required.");
      return;
    }

    await publishBulletinPost({
      form,
      title: `${prefix} | ${headline}`,
      body: note,
      category,
      templateKey,
      metadata: {
        bulletin_meta_lines: [hostLabel, eventDate ? `Date: ${formatDateLabel(eventDate)}` : ""].filter(Boolean),
        bulletin_cta_label: ctaLabel,
        bulletin_cta_target: normalizeActionTarget(ctaTarget),
      },
      successMessage,
    });
  }

  async function publishBulletinPost({ form, title, body, category, templateKey, metadata, successMessage }) {
    try {
      await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
        method: "POST",
        body: {
          title,
          body,
          kind: "announcement",
          module: "general",
          topic: category,
          post_as_company: true,
          allow_comments: true,
          metadata: {
            bulletin_category: category,
            bulletin_template: templateKey,
            ...metadata,
          },
        },
      });
      form.reset();
      showToast(successMessage);
    } catch (error) {
      showToast(error.message || "Could not publish the bulletin post.");
    }
  }

  function normalizeActionTarget(value) {
    if (!value) {
      return "";
    }
    if (value.includes("://") || value.startsWith("mailto:")) {
      return value;
    }
    if (value.includes("@")) {
      return `mailto:${value}`;
    }
    return `https://${value}`;
  }

  function logout() {
    return (window.AcuiteConnectAuth && window.AcuiteConnectAuth.logout
      ? window.AcuiteConnectAuth.logout()
      : Promise.resolve()
    ).finally(() => {
      window.location.href = "/login.html";
    });
  }

  function formatStageLabel(stage) {
    return String(stage || "")
      .split("_")
      .filter(Boolean)
      .map((part) => part[0].toUpperCase() + part.slice(1))
      .join(" ");
  }

  function formatDateLabel(value) {
    if (!value) {
      return "";
    }
    const dateValue = new Date(`${value}T00:00:00`);
    if (Number.isNaN(dateValue.getTime())) {
      return value;
    }
    return dateValue.toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  }

  function escapeHtml(value) {
    return String(value || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function capitalize(value) {
    const text = String(value || "");
    return text ? text[0].toUpperCase() + text.slice(1) : "";
  }

  function showToast(message) {
    if (!elements.toast) {
      return;
    }
    elements.toast.textContent = message;
    elements.toast.classList.add("show");
    window.clearTimeout(state.toastTimer);
    state.toastTimer = window.setTimeout(() => {
      elements.toast.classList.remove("show");
    }, 2400);
  }
})();
