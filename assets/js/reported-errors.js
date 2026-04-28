(function attachReportedErrorsInbox() {
  const ENDPOINT = "/api/ops/reported-errors/admin/";
  let reports = [];
  let loading = false;
  let canViewInbox = false;

  let elements = {};

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initReportedErrorsInbox);
  } else {
    initReportedErrorsInbox();
  }

  function initReportedErrorsInbox() {
    const adminCard = ensureAdminCard();
    elements = {
      adminCard,
      list: document.getElementById("reported-error-list"),
      meta: document.getElementById("reported-error-results-meta"),
      form: document.getElementById("report-error-form"),
      toast: document.getElementById("toast"),
    };

    if (!elements.adminCard || !elements.list || !elements.meta) {
      return;
    }

    document.addEventListener("click", handleDocumentClick);
    if (elements.form) {
      elements.form.addEventListener("submit", () => {
        if (!canViewInbox) {
          return;
        }
        window.setTimeout(() => {
          void loadReportedErrors({ force: true });
        }, 1800);
      });
    }

    void initInbox();
  }

  function ensureAdminCard() {
    const existingCard = document.getElementById("reported-error-admin-card");
    if (existingCard) {
      return existingCard;
    }

    const form = document.getElementById("report-error-form");
    const formCard = form?.closest(".section-card");
    if (!formCard) {
      return null;
    }

    const adminCard = document.createElement("section");
    adminCard.className = "section-card report-error-admin-card";
    adminCard.id = "reported-error-admin-card";
    adminCard.hidden = true;
    adminCard.innerHTML = `
      <div class="section-card-head">
        <div>
          <p class="widget-kicker">Admin Inbox</p>
          <h2>Reported errors</h2>
          <div class="mini-item-meta" id="reported-error-results-meta">Loading reports...</div>
        </div>
      </div>
      <div class="reported-error-list" id="reported-error-list"></div>
    `;
    formCard.insertAdjacentElement("afterend", adminCard);
    return adminCard;
  }

  async function initInbox() {
    const user = await getCurrentUser();
    if (!user?.access_rights?.can_administer) {
      elements.adminCard.hidden = true;
      return;
    }

    canViewInbox = true;
    elements.adminCard.hidden = false;
    await loadReportedErrors({ force: true });
  }

  async function getCurrentUser() {
    if (!window.AcuiteConnectAuth) {
      return null;
    }
    const cachedUser = window.AcuiteConnectAuth.getAuthenticatedUser?.();
    if (cachedUser) {
      return cachedUser;
    }
    try {
      const session = await window.AcuiteConnectAuth.fetchCurrentSession?.();
      return session?.authenticated ? session.user : null;
    } catch (error) {
      return null;
    }
  }

  async function loadReportedErrors({ force = false } = {}) {
    if (!canViewInbox) {
      return;
    }
    if (loading && !force) {
      return;
    }
    if (!window.AcuiteConnectAuth?.apiRequest) {
      renderError("Reported errors are unavailable right now.");
      return;
    }

    loading = true;
    renderLoading();
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest(ENDPOINT);
      reports = Array.isArray(payload.results) ? payload.results : [];
      renderReports();
    } catch (error) {
      if (Number(error.status) === 403) {
        elements.adminCard.hidden = true;
        return;
      }
      renderError(error.message || "Could not load reported errors.");
    } finally {
      loading = false;
    }
  }

  function renderLoading() {
    if (reports.length) {
      return;
    }
    elements.meta.textContent = "Loading reported errors...";
    elements.list.innerHTML = '<div class="empty-state">Loading reported errors...</div>';
  }

  function renderError(message) {
    elements.meta.textContent = "Reported error load issue";
    elements.list.innerHTML = `<div class="empty-state">${escapeHtml(message)}</div>`;
  }

  function renderReports() {
    const openCount = reports.filter((item) => !item.is_resolved).length;
    const resolvedCount = reports.length - openCount;
    elements.meta.textContent = reports.length
      ? `${openCount} open | ${resolvedCount} resolved | ${reports.length} total`
      : "No reported errors yet.";
    elements.list.innerHTML = reports.length
      ? reports.map(renderReportItem).join("")
      : '<div class="empty-state">No one has submitted an error report yet.</div>';
  }

  function renderReportItem(item) {
    const reporter = item.reporter || item.reporter_email || "Unknown reporter";
    const sourceLabel = item.metadata?.source_label || item.source_tab || "Unknown page";
    const submittedAt = formatRelativeTime(item.created_at);
    const resolvedAt = item.resolved_at ? formatRelativeTime(item.resolved_at) : "";
    const actionMarkup = item.is_resolved
      ? `<span class="reported-error-status resolved">${escapeHtml(resolvedAt ? `Resolved ${resolvedAt}` : "Resolved")}</span>`
      : `<button type="button" class="btn-ghost" data-reported-error-id="${escapeHtml(item.id)}">Resolved</button>`;

    return `
      <article class="reported-error-item">
        <div class="reported-error-item-head">
          <div>
            <h3>${escapeHtml(item.title || "Untitled report")}</h3>
            <div class="reported-error-meta">
              <span>${escapeHtml(reporter)}</span>
              <span>${escapeHtml(sourceLabel)}</span>
              ${item.page_path ? `<span>${escapeHtml(item.page_path)}</span>` : ""}
              ${submittedAt ? `<span>${escapeHtml(submittedAt)}</span>` : ""}
            </div>
          </div>
          ${actionMarkup}
        </div>
        <p class="reported-error-details">${escapeHtml(item.details || "")}</p>
        ${item.is_resolved && item.resolved_by ? `<div class="reported-error-meta"><span>Resolved by ${escapeHtml(item.resolved_by)}</span></div>` : ""}
      </article>
    `;
  }

  async function handleDocumentClick(event) {
    const button = event.target.closest("[data-reported-error-id]");
    if (!button) {
      return;
    }
    const reportId = Number(button.dataset.reportedErrorId || 0);
    if (!reportId) {
      return;
    }

    button.disabled = true;
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest(`${ENDPOINT}${reportId}/resolve/`, {
        method: "PATCH",
        body: { is_resolved: true },
      });
      const updatedReport = payload.reported_error;
      if (updatedReport) {
        reports = reports.map((item) => (
          Number(item.id) === Number(updatedReport.id) ? updatedReport : item
        ));
        renderReports();
      } else {
        await loadReportedErrors({ force: true });
      }
      showToast("Reported error marked as resolved.");
    } catch (error) {
      button.disabled = false;
      showToast(error.message || "Could not resolve the reported error.");
    }
  }

  function formatRelativeTime(value) {
    if (!value) {
      return "";
    }
    const parsed = new Date(value);
    if (Number.isNaN(parsed.getTime())) {
      return String(value);
    }

    const diffMs = Date.now() - parsed.getTime();
    const diffMinutes = Math.max(1, Math.round(diffMs / 60000));
    if (diffMinutes < 60) {
      return `${diffMinutes} min ago`;
    }

    const diffHours = Math.round(diffMinutes / 60);
    if (diffHours < 24) {
      return `${diffHours} hr ago`;
    }

    return parsed.toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  }

  function showToast(message) {
    if (!elements.toast) {
      return;
    }
    elements.toast.textContent = message;
    elements.toast.classList.add("show");
    window.clearTimeout(showToast.timer);
    showToast.timer = window.setTimeout(() => {
      elements.toast.classList.remove("show");
    }, 2600);
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }
})();
