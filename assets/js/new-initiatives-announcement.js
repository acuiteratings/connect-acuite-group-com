(function keepAnnouncementsReadOnly() {
  const NEW_INITIATIVES_FILTER = "new_initiatives";
  const STYLE_ID = "announcements-readonly-cleanup-style";

  function getActiveAnnouncementFilter() {
    const activeFilter = document.querySelector("[data-action='set-home-announcement-filter'].active");
    return activeFilter?.dataset.filter || "";
  }

  function activeFilterIsNewInitiatives() {
    return getActiveAnnouncementFilter() === NEW_INITIATIVES_FILTER;
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

  function syncAnnouncementsReadOnly() {
    const isNewInitiatives = activeFilterIsNewInitiatives();
    const announcement = document.getElementById("home-announcement");
    if (announcement) {
      announcement.classList.toggle("announcement-banner-no-actions", isNewInitiatives);
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

  function preventAnnouncementFormSubmissions(event) {
    if (
      event.target?.id === "home-announcement-feedback-form"
      || event.target?.id === "home-announcement-admin-form"
    ) {
      event.preventDefault();
      event.stopImmediatePropagation();
    }
  }

  function scheduleSync() {
    window.requestAnimationFrame(syncAnnouncementsReadOnly);
  }

  function startCleanup() {
    injectStyle();
    syncAnnouncementsReadOnly();

    const observer = new MutationObserver(scheduleSync);
    observer.observe(document.body, {
      attributes: true,
      childList: true,
      subtree: true,
    });

    document.addEventListener("click", scheduleSync, true);
    document.addEventListener("submit", preventAnnouncementFormSubmissions, true);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startCleanup);
  } else {
    startCleanup();
  }
})();
