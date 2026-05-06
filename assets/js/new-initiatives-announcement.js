(function keepAnnouncementsReadOnly() {
  const LEADERSHIP_FILTER = "leadership";
  const NEW_INITIATIVES_FILTER = "new_initiatives";
  const STYLE_ID = "announcements-readonly-cleanup-style";
  const SNAPSHOT_KEY = "acuite-connect-announcement-snapshot-v1";
  const SNAPSHOT_MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000;
  const LEADERSHIP_BLUE_THEME = {
    "--announcement-bg": "linear-gradient(140deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.02) 34%, transparent 58%), radial-gradient(circle at top right, rgba(125, 211, 252, 0.28), transparent 30%), radial-gradient(circle at bottom left, rgba(59, 130, 246, 0.24), transparent 34%), linear-gradient(135deg, #0f3b68, #174f82 54%, #0b2f55), var(--bg2)",
    "--announcement-text": "#f4f8ff",
    "--announcement-muted": "rgba(244, 248, 255, 0.82)",
    "--announcement-soft": "rgba(244, 248, 255, 0.58)",
    "--announcement-border": "rgba(191, 219, 254, 0.24)",
    "--announcement-surface-bg": "linear-gradient(180deg, rgba(255, 255, 255, 0.13), rgba(255, 255, 255, 0.06))",
    "--announcement-surface-border": "rgba(191, 219, 254, 0.22)",
    "--announcement-badge-bg": "rgba(255, 255, 255, 0.08)",
    "--announcement-badge-border": "rgba(191, 219, 254, 0.2)",
    "--announcement-badge-text": "rgba(244, 248, 255, 0.84)",
    "--announcement-badge-strong-bg": "rgba(125, 211, 252, 0.22)",
    "--announcement-badge-strong-border": "rgba(125, 211, 252, 0.42)",
    "--announcement-badge-strong-text": "#f0f9ff",
    "--announcement-input-bg": "rgba(8, 47, 83, 0.38)",
    "--announcement-input-border": "rgba(191, 219, 254, 0.22)",
    "--announcement-input-placeholder": "rgba(244, 248, 255, 0.68)",
    "--announcement-reaction-bg": "rgba(255, 255, 255, 0.06)",
    "--announcement-reaction-border": "rgba(191, 219, 254, 0.22)",
    "--announcement-reaction-pill-bg": "rgba(255, 255, 255, 0.1)",
    "--announcement-reaction-pill-text": "#f4f8ff",
    "--announcement-reaction-active-bg": "rgba(125, 211, 252, 0.16)",
    "--announcement-reaction-active-border": "rgba(125, 211, 252, 0.42)",
    "--announcement-like-btn-bg": "rgba(255, 255, 255, 0.1)",
    "--announcement-like-count": "rgba(244, 248, 255, 0.84)",
    "--announcement-accent": "#7dd3fc",
  };
  let captureTimer = 0;
  let freshAnnouncementsLoaded = false;

  function getActiveAnnouncementFilter() {
    const activeFilter = document.querySelector("[data-action='set-home-announcement-filter'].active");
    if (activeFilter?.dataset.filter) {
      return activeFilter.dataset.filter;
    }
    try {
      const savedState = JSON.parse(window.localStorage.getItem("acuite-connect-state-v2-live") || "{}");
      return typeof savedState.homeAnnouncementFilter === "string"
        ? savedState.homeAnnouncementFilter
        : "";
    } catch (error) {
      return "";
    }
  }

  function activeFilterIsNewInitiatives() {
    return getActiveAnnouncementFilter() === NEW_INITIATIVES_FILTER;
  }

  function activeFilterIsLeadership() {
    return getActiveAnnouncementFilter() === LEADERSHIP_FILTER;
  }

  function applyLeadershipBlueTheme(container) {
    if (!container || !activeFilterIsLeadership()) {
      return;
    }
    Object.entries(LEADERSHIP_BLUE_THEME).forEach(([key, value]) => {
      container.style.setProperty(key, value);
    });
  }

  function injectStyle() {
    if (document.getElementById(STYLE_ID)) {
      return;
    }
    const style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = `
      .announcement-banner-no-actions {
        grid-template-columns: minmax(0, 1fr) !important;
      }
    `;
    document.head.appendChild(style);
  }

  function readSnapshots() {
    try {
      const parsed = JSON.parse(window.localStorage.getItem(SNAPSHOT_KEY) || "{}");
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch (error) {
      return {};
    }
  }

  function writeSnapshots(payload) {
    try {
      window.localStorage.setItem(SNAPSHOT_KEY, JSON.stringify(payload));
    } catch (error) {
      return;
    }
  }

  function watchAnnouncementFetches() {
    if (!window.fetch || window.fetch.announcementSnapshotWrapped) {
      return;
    }
    const originalFetch = window.fetch.bind(window);
    const wrappedFetch = (input, init) => {
      const requestUrl = typeof input === "string" ? input : (input?.url || "");
      const isHomeAnnouncementRequest =
        requestUrl.includes("/api/feed/posts/")
        && requestUrl.includes("home_announcements=1");
      return originalFetch(input, init).then((response) => {
        if (isHomeAnnouncementRequest) {
          freshAnnouncementsLoaded = true;
          window.setTimeout(scheduleSnapshotCapture, 0);
          window.setTimeout(scheduleSnapshotCapture, 600);
        }
        return response;
      });
    };
    wrappedFetch.announcementSnapshotWrapped = true;
    window.fetch = wrappedFetch;
  }

  function getSnapshotForActiveFilter() {
    const filter = getActiveAnnouncementFilter() || "leadership";
    const snapshots = readSnapshots();
    const snapshot = snapshots.filters?.[filter];
    if (!snapshot || typeof snapshot.html !== "string") {
      return null;
    }
    const savedAt = Number(snapshot.savedAt || 0);
    if (!savedAt || Date.now() - savedAt > SNAPSHOT_MAX_AGE_MS) {
      return null;
    }
    return snapshot;
  }

  function announcementHasContent(container) {
    return Boolean(
      container
      && container.innerHTML.trim()
      && !container.querySelector(".announcement-empty-state")
      && container.querySelector(".announcement-title, .announcement-poll-list, .announcement-meta-grid")
    );
  }

  function captureAnnouncementSnapshot() {
    const container = document.getElementById("home-announcement");
    if (!announcementHasContent(container)) {
      return;
    }
    const filter = getActiveAnnouncementFilter() || "leadership";
    const snapshots = readSnapshots();
    writeSnapshots({
      version: 1,
      filters: {
        ...(snapshots.filters && typeof snapshots.filters === "object" ? snapshots.filters : {}),
        [filter]: {
          html: container.innerHTML,
          className: container.className,
          style: container.getAttribute("style") || "",
          savedAt: Date.now(),
        },
      },
    });
  }

  function restoreAnnouncementSnapshot() {
    const container = document.getElementById("home-announcement");
    const snapshot = container ? getSnapshotForActiveFilter() : null;
    if (!container || !snapshot) {
      return;
    }
    container.innerHTML = snapshot.html;
    if (snapshot.className) {
      container.className = snapshot.className;
    }
    if (snapshot.style) {
      container.setAttribute("style", snapshot.style);
    } else {
      container.removeAttribute("style");
    }
    syncAnnouncementsReadOnly();
  }

  function restoreSnapshotOverPrefetchEmptyState() {
    const container = document.getElementById("home-announcement");
    if (
      !freshAnnouncementsLoaded
      && container?.querySelector(".announcement-empty-state")
      && getSnapshotForActiveFilter()
    ) {
      restoreAnnouncementSnapshot();
    }
  }

  function syncAnnouncementsReadOnly() {
    const isNewInitiatives = activeFilterIsNewInitiatives();
    const announcement = document.getElementById("home-announcement");
    if (announcement) {
      announcement.classList.toggle("announcement-banner-no-actions", isNewInitiatives);
      applyLeadershipBlueTheme(announcement);
    }

    document
      .querySelectorAll("#home-announcement-feedback-form")
      .forEach((element) => {
        element.remove();
      });

    document
      .querySelectorAll("#home-announcement .announcement-like-row")
      .forEach((element) => {
        if (isNewInitiatives) {
          element.remove();
        }
      });

    const adminForm = document.getElementById("home-announcement-admin-form");
    if (adminForm) {
      adminForm.hidden = true;
    }
  }

  function syncAnnouncementReminderCopy() {
    const copy = document.querySelector(".announcement-reminder-copy");
    if (copy?.textContent.includes("importance information")) {
      copy.textContent = "Do not miss out on important information.";
    }
  }

  function preventAnnouncementFormSubmissions(event) {
    if (
      event.target?.id === "home-announcement-feedback-form"
      || event.target?.id === "home-announcement-admin-form"
    ) {
      event.preventDefault();
      event.stopImmediatePropagation();
    }
  }

  function scheduleSnapshotCapture() {
    if (captureTimer) {
      return;
    }
    captureTimer = window.setTimeout(() => {
      captureTimer = 0;
      syncAnnouncementsReadOnly();
      captureAnnouncementSnapshot();
    }, 120);
  }

  function scheduleSync() {
    window.requestAnimationFrame(() => {
      syncAnnouncementsReadOnly();
      syncAnnouncementReminderCopy();
      restoreSnapshotOverPrefetchEmptyState();
      scheduleSnapshotCapture();
    });
  }

  function scheduleSnapshotRestore() {
    window.requestAnimationFrame(() => {
      if (!freshAnnouncementsLoaded) {
        restoreAnnouncementSnapshot();
      }
      scheduleSnapshotCapture();
    });
  }

  function startCleanup() {
    injectStyle();
    watchAnnouncementFetches();
    syncAnnouncementsReadOnly();
    syncAnnouncementReminderCopy();
    restoreAnnouncementSnapshot();

    const observer = new MutationObserver(scheduleSync);
    observer.observe(document.body, {
      attributes: true,
      childList: true,
      subtree: true,
    });

    document.addEventListener("click", (event) => {
      scheduleSync();
      if (event.target?.closest?.("[data-action='set-home-announcement-filter']")) {
        window.setTimeout(scheduleSnapshotRestore, 0);
      }
    }, true);
    document.addEventListener("submit", preventAnnouncementFormSubmissions, true);
    scheduleSnapshotCapture();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startCleanup);
  } else {
    startCleanup();
  }
})();

(function loadDirectoryContactDetails() {
  if (window.directoryContactDetailsRequested) {
    return;
  }
  window.directoryContactDetailsRequested = true;
  const scriptUrl = document.currentScript?.src || "";
  const versionQuery = scriptUrl.includes("?") ? `?${scriptUrl.split("?").slice(1).join("?")}` : "";
  const detailsScript = document.createElement("script");
  detailsScript.src = `/static/js/directory-contact-details.js${versionQuery}`;
  detailsScript.defer = true;
  document.head.appendChild(detailsScript);
})();
