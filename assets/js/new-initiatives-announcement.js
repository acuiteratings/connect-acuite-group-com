(function hideNewInitiativesAnnouncementActions() {
  const NEW_INITIATIVES_FILTER = "new_initiatives";
  const STYLE_ID = "new-initiatives-announcement-cleanup-style";

  function activeFilterIsNewInitiatives() {
    const activeFilter = document.querySelector("[data-action='set-home-announcement-filter'].active");
    return activeFilter?.dataset.filter === NEW_INITIATIVES_FILTER;
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

  function syncNewInitiativesCleanup() {
    const shouldHide = activeFilterIsNewInitiatives();
    const announcement = document.getElementById("home-announcement");
    if (announcement) {
      announcement.classList.toggle("announcement-banner-no-actions", shouldHide);
    }

    document
      .querySelectorAll("#home-announcement-feedback-form, #home-announcement .announcement-like-row")
      .forEach((element) => {
        if (shouldHide) {
          element.remove();
        } else {
          element.hidden = false;
        }
      });

    const adminForm = document.getElementById("home-announcement-admin-form");
    if (adminForm && shouldHide) {
      adminForm.hidden = true;
    }
  }

  function preventHiddenFormSubmissions(event) {
    if (!activeFilterIsNewInitiatives()) {
      return;
    }
    if (
      event.target?.id === "home-announcement-feedback-form"
      || event.target?.id === "home-announcement-admin-form"
    ) {
      event.preventDefault();
      event.stopImmediatePropagation();
    }
  }

  function scheduleSync() {
    window.requestAnimationFrame(syncNewInitiativesCleanup);
  }

  function startCleanup() {
    injectStyle();
    syncNewInitiativesCleanup();

    const observer = new MutationObserver(scheduleSync);
    observer.observe(document.body, {
      attributes: true,
      childList: true,
      subtree: true,
    });

    document.addEventListener("click", scheduleSync, true);
    document.addEventListener("submit", preventHiddenFormSubmissions, true);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startCleanup);
  } else {
    startCleanup();
  }
})();
