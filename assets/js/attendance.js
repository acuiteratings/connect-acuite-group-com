(function attachAttendanceExperience() {
  const PANEL_ID = "panel-attendance";
  const TAB_ID = "attendance-sidebar-tab";
  const STYLE_ID = "attendance-experience-style";
  let attendanceStatus = null;
  let adminOverview = null;
  let loading = false;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAttendanceExperience, { once: true });
  } else {
    initAttendanceExperience();
  }

  function initAttendanceExperience() {
    injectStyle();
    injectSidebarTab();
    injectPanel();
    document.addEventListener("click", handleAttendanceClick, true);
    void loadAttendanceData();
  }

  function injectStyle() {
    if (document.getElementById(STYLE_ID)) {
      return;
    }
    const style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = `
      .attendance-grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: 18px; }
      .attendance-status-card { display: grid; gap: 16px; }
      .attendance-status-card.has-admin { grid-template-columns: minmax(220px, 0.8fr) repeat(2, minmax(160px, 1fr)) minmax(220px, 1.2fr); align-items: center; }
      .attendance-status-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 14px; }
      .attendance-status-pill { border: 1px solid var(--border); border-radius: 999px; padding: 8px 12px; font-size: 12px; font-weight: 800; color: var(--orange); background: var(--bg2); white-space: nowrap; }
      .attendance-status-pill.present { color: #15803d; background: #dcfce7; border-color: #bbf7d0; }
      .attendance-status-pill.not_applicable, .attendance-status-pill.holiday, .attendance-status-pill.weekend { color: #334155; background: #e2e8f0; border-color: #cbd5e1; }
      .attendance-time-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
      .attendance-time-box { border: 1px solid var(--border); border-radius: 8px; padding: 14px; background: var(--bg); }
      .attendance-time-box span { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text3); font-weight: 800; margin-bottom: 6px; }
      .attendance-time-box strong { font-size: 18px; }
      .attendance-note { color: var(--text2); line-height: 1.55; }
      .attendance-status-card.has-admin .attendance-note { margin: 0; }
      .attendance-actions { display: flex; flex-wrap: wrap; gap: 10px; }
      .attendance-admin-summary { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }
      .attendance-admin-summary .mini-chip { background: var(--bg2); }
      .attendance-table-wrap { overflow: auto; border: 1px solid var(--border); border-radius: 8px; max-height: min(58vh, 620px); }
      .attendance-table { width: 100%; border-collapse: collapse; min-width: 980px; }
      .attendance-table th, .attendance-table td { padding: 10px 12px; border-bottom: 1px solid var(--border); text-align: left; font-size: 13px; vertical-align: top; }
      .attendance-table th { position: sticky; top: 0; z-index: 1; background: var(--bg2); color: var(--text2); font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; }
      .attendance-table tbody tr:nth-child(even) { background: rgba(0, 0, 0, 0.015); }
      .attendance-admin-card { min-width: 0; }
      .attendance-admin-card .section-card-head { align-items: flex-start; }
      .attendance-employee-cell strong { display: block; line-height: 1.25; }
      .attendance-detail-cell { max-width: 360px; color: var(--text2); }
      @media (max-width: 1100px) { .attendance-status-card.has-admin { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
      @media (max-width: 700px) {
        .attendance-status-card.has-admin { grid-template-columns: 1fr; }
        .attendance-table { min-width: 760px; }
      }
    `;
    document.head.append(style);
  }

  function injectSidebarTab() {
    if (document.getElementById(TAB_ID)) {
      return;
    }
    const storeTab = document.querySelector('[data-switch-tab="store"]');
    const button = document.createElement("button");
    button.type = "button";
    button.className = "tab";
    button.id = TAB_ID;
    button.dataset.action = "open-attendance";
    button.innerHTML = `
      <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3M5 11h14M7 21h10a2 2 0 002-2V7H5v12a2 2 0 002 2zm5-7v4m-2-2h4"></path>
      </svg>
      Attendance
    `;
    if (storeTab) {
      storeTab.insertAdjacentElement("afterend", button);
    }
  }

  function injectPanel() {
    if (document.getElementById(PANEL_ID)) {
      return;
    }
    const storePanel = document.getElementById("panel-store");
    const panel = document.createElement("section");
    panel.className = "panel";
    panel.id = PANEL_ID;
    panel.innerHTML = `
      <div class="section-head">
        <div>
          <h2>Attendance</h2>
          <p>Connect captures attendance only from trusted office networks.</p>
        </div>
      </div>
      <div class="attendance-grid">
        <section class="section-card attendance-status-card" id="attendance-status-card"></section>
        <section class="section-card attendance-admin-card" id="attendance-admin-card" hidden></section>
      </div>
    `;
    if (storePanel) {
      storePanel.insertAdjacentElement("afterend", panel);
    }
    renderAttendancePanel();
  }

  async function loadAttendanceData() {
    if (loading || !window.AcuiteConnectAuth?.apiRequest) {
      return;
    }
    loading = true;
    try {
      attendanceStatus = await window.AcuiteConnectAuth.apiRequest("/api/attendance/status/");
      const user = window.AcuiteConnectAuth.getAuthenticatedUser?.();
      const canAdmin = Boolean(user?.access_rights?.can_administer);
      if (canAdmin) {
        adminOverview = await window.AcuiteConnectAuth.apiRequest("/api/attendance/admin/overview/");
      }
    } catch (error) {
      attendanceStatus = { status_label: "Unavailable", detail: error.message || "Could not load attendance." };
    } finally {
      loading = false;
      renderAttendancePanel();
    }
  }

  function handleAttendanceClick(event) {
    const attendanceAction = event.target.closest("[data-action='open-attendance']");
    if (!attendanceAction) {
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    openAttendancePanel();
  }

  function openAttendancePanel() {
    document.querySelectorAll(".panel").forEach((panel) => {
      panel.classList.toggle("active", panel.id === PANEL_ID);
    });
    document.querySelectorAll(".tab").forEach((tab) => {
      tab.classList.toggle("active", tab.id === TAB_ID);
    });
    void loadAttendanceData();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function renderAttendancePanel() {
    const statusCard = document.getElementById("attendance-status-card");
    if (!statusCard) {
      return;
    }
    if (loading && !attendanceStatus) {
      statusCard.innerHTML = '<div class="empty-state">Loading attendance status...</div>';
      return;
    }
    const status = attendanceStatus || {};
    const record = status.record || {};
    const isAdmin = Boolean(window.AcuiteConnectAuth?.getAuthenticatedUser?.()?.access_rights?.can_administer);
    statusCard.classList.toggle("has-admin", isAdmin);
    statusCard.innerHTML = `
      <div class="attendance-status-head">
        <div>
          <p class="widget-kicker">Today</p>
          <h3>${escapeValue(status.status_label || "Not Marked")}</h3>
        </div>
        <span class="attendance-status-pill ${escapeValue(status.status || "not_marked")}">${escapeValue(status.status_label || "Not Marked")}</span>
      </div>
      <div class="attendance-time-grid">
        <div class="attendance-time-box">
          <span>Punch In</span>
          <strong>${formatTime(record.punch_in_at)}</strong>
        </div>
        <div class="attendance-time-box">
          <span>Punch Out</span>
          <strong>${formatTime(record.punch_out_at)}</strong>
        </div>
      </div>
      <p class="attendance-note">${escapeValue(status.detail || "Attendance status will appear here.")}</p>
      ${
        isAdmin
          ? ""
          : `<div class="attendance-actions">
              <button type="button" class="btn-secondary" disabled>Leave Balance</button>
              <button type="button" class="btn-secondary" disabled>Apply Leave</button>
              ${status.status === "no_punchout" ? '<button type="button" class="btn-secondary" disabled>Regularize Attendance</button>' : ""}
            </div>`
      }
    `;
    renderAdminAttendance();
  }

  function renderAdminAttendance() {
    const adminCard = document.getElementById("attendance-admin-card");
    if (!adminCard) {
      return;
    }
    const results = Array.isArray(adminOverview?.results) ? adminOverview.results : [];
    const user = window.AcuiteConnectAuth?.getAuthenticatedUser?.();
    const canAdmin = Boolean(user?.access_rights?.can_administer);
    adminCard.hidden = !canAdmin;
    if (!canAdmin) {
      return;
    }
    adminCard.innerHTML = `
      <div class="section-card-head">
        <div>
          <p class="widget-kicker">Admin</p>
          <h2>Attendance records</h2>
          <div class="mini-item-meta">${results.length} employees for ${escapeValue(adminOverview?.date || "today")}</div>
          ${renderAdminSummary()}
        </div>
      </div>
      <div class="attendance-table-wrap">
        <table class="attendance-table">
          <thead>
            <tr><th>Employee</th><th>Status</th><th>Punch In</th><th>Punch Out</th><th>Office</th><th>Detail</th></tr>
          </thead>
          <tbody>
            ${results.length ? results.map(renderAdminRow).join("") : '<tr><td colspan="6">No attendance records available.</td></tr>'}
          </tbody>
        </table>
      </div>
    `;
  }

  function renderAdminRow(row) {
    const record = row.record || {};
    return `
      <tr>
        <td class="attendance-employee-cell"><strong>${escapeValue(row.user?.name || "Employee")}</strong><span class="mini-item-meta">${escapeValue(row.user?.email || "")}</span></td>
        <td>${escapeValue(row.status_label || "")}</td>
        <td>${formatTime(record.punch_in_at)}</td>
        <td>${formatTime(record.punch_out_at)}</td>
        <td>${escapeValue(record.office_label || row.calendar_label || "-")}</td>
        <td class="attendance-detail-cell">${escapeValue(row.detail || "")}</td>
      </tr>
    `;
  }

  function renderAdminSummary() {
    const counts = adminOverview?.counts && typeof adminOverview.counts === "object" ? adminOverview.counts : {};
    const labels = [
      ["present", "Present"],
      ["no_punchout", "No Punchout"],
      ["not_marked", "Not Marked"],
      ["not_applicable", "Not Applicable"],
      ["holiday", "Holiday"],
      ["weekend", "Weekend"],
    ];
    const chips = labels
      .filter(([key]) => Number(counts[key] || 0) > 0)
      .map(([key, label]) => `<span class="mini-chip">${escapeValue(label)}: ${escapeValue(String(counts[key]))}</span>`);
    return chips.length ? `<div class="attendance-admin-summary">${chips.join("")}</div>` : "";
  }

  function formatTime(value) {
    if (!value) {
      return "-";
    }
    const date = new Date(value);
    if (!Number.isFinite(date.getTime())) {
      return "-";
    }
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function escapeValue(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }
})();
