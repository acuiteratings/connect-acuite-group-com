(function attachReportedErrorsInbox() {
  const ENDPOINT = "/api/ops/reported-errors/admin/";
  const NOTIFICATIONS_ENDPOINT = "/api/ops/reported-errors/notifications/";
  let reports = [];
  let reporterNotifications = [];
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

    void loadReporterNotifications();
    if (!elements.adminCard || !elements.list || !elements.meta) {
      return;
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
    const submittedAt = formatReportedErrorDate(item.created_at);
    const resolvedAt = item.resolved_at ? formatRelativeTime(item.resolved_at) : "";
    const outcomeLabel = item.resolution_outcome_label || (item.resolution_outcome === "not_an_error" ? "Not an error" : "Resolved");
    const actionMarkup = item.is_resolved
      ? `<span class="reported-error-status resolved">${escapeHtml(resolvedAt ? `${outcomeLabel} ${resolvedAt}` : outcomeLabel)}</span>`
      : `
        <div class="reported-error-resolution-box">
          <label class="field">
            <span>Admin comments, if any</span>
            <textarea data-reported-error-comment="${escapeHtml(item.id)}" rows="2" maxlength="1000" placeholder="Optional comment to show the reporter"></textarea>
          </label>
          <div class="reported-error-actions">
            <button type="button" class="btn-ghost" data-reported-error-action="resolved" data-reported-error-id="${escapeHtml(item.id)}">Resolved</button>
            <button type="button" class="btn-outline" data-reported-error-action="not_an_error" data-reported-error-id="${escapeHtml(item.id)}">Not an error</button>
          </div>
        </div>
      `;

    return `
      <article class="reported-error-item">
        <div class="reported-error-item-head">
          <div>
            <h3>${escapeHtml(item.title || "Untitled report")}</h3>
            <div class="reported-error-meta">
              <span>${escapeHtml(reporter)}</span>
              <span>${escapeHtml(sourceLabel)}</span>
              ${item.page_path ? `<span>${escapeHtml(item.page_path)}</span>` : ""}
              ${submittedAt ? `<span>Reported on ${escapeHtml(submittedAt)}</span>` : ""}
            </div>
          </div>
          ${actionMarkup}
        </div>
        <p class="reported-error-details">${escapeHtml(item.details || "")}</p>
        ${item.attachment ? renderReportAttachment(item.attachment) : ""}
        ${item.is_resolved && item.resolution_comment ? `<p class="reported-error-resolution-comment">${escapeHtml(item.resolution_comment)}</p>` : ""}
        ${item.is_resolved && item.resolved_by ? `<div class="reported-error-meta"><span>${escapeHtml(outcomeLabel)} by ${escapeHtml(item.resolved_by)}</span></div>` : ""}
      </article>
    `;
  }

  function renderReportAttachment(attachment) {
    const dataUrl = String(attachment.data_url || "");
    if (!dataUrl.startsWith("data:image/")) {
      return "";
    }
    const label = attachment.name || "Attached screenshot";
    return `
      <div class="reported-error-attachment">
        <div class="reported-error-meta">
          <span>Attachment: ${escapeHtml(label)}</span>
          <span>${escapeHtml(formatBytes(attachment.size))}</span>
          <span>Auto-deletes when closed</span>
        </div>
        <a href="${escapeHtml(dataUrl)}" target="_blank" rel="noopener" aria-label="Open attached screenshot">
          <img src="${escapeHtml(dataUrl)}" alt="${escapeHtml(label)}">
        </a>
      </div>
    `;
  }

  async function handleDocumentClick(event) {
    const acknowledgeButton = event.target.closest("[data-reported-error-ack]");
    if (acknowledgeButton) {
      await acknowledgeReporterNotification(Number(acknowledgeButton.dataset.reportedErrorAck || 0));
      return;
    }

    const closeButton = event.target.closest("[data-reported-error-close-notice]");
    if (closeButton) {
      closeReporterNotificationModal();
      return;
    }

    const button = event.target.closest("[data-reported-error-action]");
    if (!button) {
      return;
    }
    const reportId = Number(button.dataset.reportedErrorId || 0);
    if (!reportId) {
      return;
    }
    const outcome = button.dataset.reportedErrorAction === "not_an_error" ? "not_an_error" : "resolved";
    const commentInput = document.querySelector(`[data-reported-error-comment="${reportId}"]`);
    const resolutionComment = String(commentInput?.value || "").trim();

    button.disabled = true;
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest(`${ENDPOINT}${reportId}/resolve/`, {
        method: "PATCH",
        body: {
          resolution_outcome: outcome,
          resolution_comment: resolutionComment,
        },
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
      showToast(outcome === "not_an_error" ? "Reported error marked as not an error." : "Reported error marked as resolved.");
    } catch (error) {
      button.disabled = false;
      showToast(error.message || "Could not resolve the reported error.");
    }
  }

  async function loadReporterNotifications() {
    if (!window.AcuiteConnectAuth?.apiRequest) {
      return;
    }
    try {
      const payload = await window.AcuiteConnectAuth.apiRequest(NOTIFICATIONS_ENDPOINT);
      reporterNotifications = Array.isArray(payload.results) ? payload.results : [];
      showNextReporterNotification();
    } catch (error) {
      // Non-admin users still use this quietly; auth/session failures should not interrupt Connect.
    }
  }

  function showNextReporterNotification() {
    const report = reporterNotifications[0];
    if (!report) {
      return;
    }
    closeReporterNotificationModal();
    const outcomeLabel = report.resolution_outcome_label || (report.resolution_outcome === "not_an_error" ? "Not an error" : "Resolved");
    const sourceLabel = report.metadata?.source_label || report.source_tab || "Unknown page";
    const modal = document.createElement("div");
    modal.className = "reported-error-notice-backdrop";
    modal.id = "reported-error-resolution-notice";
    modal.innerHTML = `
      <section class="reported-error-notice" role="dialog" aria-modal="true" aria-labelledby="reported-error-notice-title">
        <button type="button" class="reported-error-notice-close" data-reported-error-ack="${escapeHtml(report.id)}" aria-label="Close">&times;</button>
        <p class="widget-kicker">Reported issue update</p>
        <h2 id="reported-error-notice-title">Your reported issue has been ${escapeHtml(outcomeLabel.toLowerCase())}</h2>
        <div class="reported-error-notice-grid">
          <div>
            <span>Issue</span>
            <strong>${escapeHtml(report.title || "Untitled report")}</strong>
          </div>
          <div>
            <span>Page</span>
            <strong>${escapeHtml(sourceLabel)}</strong>
          </div>
          <div>
            <span>Status</span>
            <strong>${escapeHtml(outcomeLabel)}</strong>
          </div>
          <div>
            <span>Resolved by</span>
            <strong>${escapeHtml(report.resolved_by || "Connect admin")}</strong>
          </div>
        </div>
        <div class="reported-error-notice-detail">
          <span>Your report</span>
          <p>${escapeHtml(report.details || "")}</p>
        </div>
        ${
          report.resolution_comment
            ? `<div class="reported-error-notice-detail">
                <span>Admin comments</span>
                <p>${escapeHtml(report.resolution_comment)}</p>
              </div>`
            : ""
        }
        <div class="form-actions">
          <button type="button" class="btn-warm" data-reported-error-ack="${escapeHtml(report.id)}">Understood</button>
        </div>
      </section>
    `;
    document.body.append(modal);
  }

  function closeReporterNotificationModal() {
    document.getElementById("reported-error-resolution-notice")?.remove();
  }

  async function acknowledgeReporterNotification(reportId) {
    if (!reportId || !window.AcuiteConnectAuth?.apiRequest) {
      closeReporterNotificationModal();
      return;
    }
    try {
      await window.AcuiteConnectAuth.apiRequest(`${NOTIFICATIONS_ENDPOINT}${reportId}/acknowledge/`, {
        method: "PATCH",
      });
      reporterNotifications = reporterNotifications.filter((item) => Number(item.id) !== Number(reportId));
      closeReporterNotificationModal();
      showNextReporterNotification();
    } catch (error) {
      showToast(error.message || "Could not close the reported issue notice.");
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

  function formatReportedErrorDate(value) {
    if (!value) {
      return "";
    }
    const parsed = new Date(value);
    if (Number.isNaN(parsed.getTime())) {
      return String(value);
    }
    return parsed.toLocaleString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
  }

  function formatBytes(value) {
    const bytes = Number(value || 0);
    if (!Number.isFinite(bytes) || bytes <= 0) {
      return "0 KB";
    }
    if (bytes < 1024 * 1024) {
      return `${Math.max(1, Math.round(bytes / 1024))} KB`;
    }
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
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
