(function attachDirectoryContactDetails() {
  const DIRECTORY_GRID_ID = "directory-grid";
  const DETAIL_CLASS = "directory-contact-details";
  const DETAIL_ROW_SELECTOR = `.${DETAIL_CLASS}`;
  const DATE_FORMATTER = new Intl.DateTimeFormat("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

  let profileMap = new Map();
  let loadPromise = null;
  let retryTimer = 0;
  let syncTimer = 0;

  function formatJoiningDate(value) {
    if (!value) {
      return "";
    }
    const parsed = new Date(`${value}T00:00:00`);
    if (Number.isNaN(parsed.getTime())) {
      return String(value);
    }
    return DATE_FORMATTER.format(parsed);
  }

  function normalizeProfile(profile) {
    return {
      email: profile.email || "",
      mobileNumber: profile.mobile_number || "",
      joiningDate: formatJoiningDate(profile.joined_on),
    };
  }

  async function loadDirectoryContacts() {
    if (loadPromise) {
      return loadPromise;
    }
    if (!window.AcuiteConnectAuth?.apiRequest) {
      return Promise.resolve(false);
    }
    loadPromise = window.AcuiteConnectAuth.apiRequest("/api/directory/?page=1&page_size=500")
      .then((payload) => {
        const nextMap = new Map();
        (Array.isArray(payload.results) ? payload.results : []).forEach((profile) => {
          nextMap.set(`person-${profile.id}`, normalizeProfile(profile));
        });
        profileMap = nextMap;
        return true;
      })
      .catch(() => false)
      .finally(() => {
        loadPromise = null;
      });
    return loadPromise;
  }

  function renderDetailsForCard(card, profile) {
    card.querySelectorAll(DETAIL_ROW_SELECTOR).forEach((element) => element.remove());

    const footerText = [
      profile.email,
      profile.mobileNumber,
      profile.joiningDate ? `Date of Joining: ${profile.joiningDate}` : "",
    ].filter(Boolean).join(" | ");
    if (!footerText) {
      return;
    }

    let footer = card.querySelector(".person-footer");
    if (!footer) {
      footer = document.createElement("div");
      footer.className = "person-footer";
      card.appendChild(footer);
    }
    footer.hidden = false;

    let contactLine = footer.querySelector(".availability");
    if (!contactLine) {
      contactLine = document.createElement("span");
      contactLine.className = "availability";
      footer.prepend(contactLine);
    }
    contactLine.textContent = footerText;
  }

  function syncDirectoryCards() {
    const grid = document.getElementById(DIRECTORY_GRID_ID);
    if (!grid || !profileMap.size) {
      return;
    }
    grid.querySelectorAll(".person-card[id]").forEach((card) => {
      const profile = profileMap.get(card.id);
      if (profile) {
        renderDetailsForCard(card, profile);
      }
    });
  }

  function scheduleSync() {
    window.clearTimeout(syncTimer);
    syncTimer = window.setTimeout(() => {
      void loadDirectoryContacts().then(syncDirectoryCards);
    }, 80);
  }

  function start() {
    const grid = document.getElementById(DIRECTORY_GRID_ID);
    if (!grid) {
      retryTimer = window.setTimeout(start, 400);
      return;
    }
    window.clearTimeout(retryTimer);
    new MutationObserver(scheduleSync).observe(grid, { childList: true });
    scheduleSync();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();
