(function attachCelebrationPhotos() {
  const state = {
    birthdays: [],
    anniversaries: [],
    photoByUserId: new Map(),
    loaded: false,
    loading: false,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCelebrationPhotos, { once: true });
  } else {
    initCelebrationPhotos();
  }

  function initCelebrationPhotos() {
    loadCelebrationPhotoStyles();
    observeCelebrationLists();
    void loadCelebrationPhotos();
  }

  async function loadCelebrationPhotos() {
    if (state.loading || state.loaded) {
      return;
    }
    const auth = window.AcuiteConnectAuth;
    if (!auth || !auth.apiRequest) {
      return;
    }
    state.loading = true;
    try {
      const recognitionPayload = await auth.apiRequest("/api/recognition/overview/");
      state.birthdays = Array.isArray(recognitionPayload.birthdays) ? recognitionPayload.birthdays : [];
      state.anniversaries = Array.isArray(recognitionPayload.anniversaries) ? recognitionPayload.anniversaries : [];
      state.photoByUserId = buildPhotoMap(state.birthdays, state.anniversaries);
      state.loaded = true;
      applyCelebrationPhotos();
    } catch (error) {
      state.birthdays = [];
      state.anniversaries = [];
      state.photoByUserId = new Map();
    } finally {
      state.loading = false;
    }
  }

  function observeCelebrationLists() {
    const observer = new MutationObserver(() => {
      if (!state.loaded) {
        void loadCelebrationPhotos();
        return;
      }
      applyCelebrationPhotos();
    });
    ["birthdays-list", "anniversaries-list"].forEach((id) => {
      const list = document.getElementById(id);
      if (list) {
        observer.observe(list, { childList: true, subtree: true });
      }
    });
  }

  function applyCelebrationPhotos() {
    applyListPhotos("birthdays-list", state.birthdays);
    applyListPhotos("anniversaries-list", state.anniversaries);
  }

  function applyListPhotos(listId, people) {
    const list = document.getElementById(listId);
    if (!list || !Array.isArray(people) || !people.length) {
      return;
    }
    list.querySelectorAll(".bday-item").forEach((item, index) => {
      const person = people[index] || null;
      const photoUrl = getPhotoUrl(person);
      const avatar = item.querySelector(".bday-avatar");
      if (!avatar || !photoUrl || avatar.dataset.photoUrl === photoUrl) {
        return;
      }
      avatar.dataset.photoUrl = photoUrl;
      avatar.classList.remove("has-photo");
      avatar.querySelectorAll("img").forEach((image) => image.remove());
      const image = document.createElement("img");
      image.src = photoUrl;
      image.alt = "";
      image.loading = "lazy";
      image.decoding = "async";
      image.addEventListener("load", () => {
        avatar.classList.add("has-photo");
      }, { once: true });
      image.addEventListener("error", () => {
        image.remove();
        avatar.classList.remove("has-photo");
        avatar.dataset.photoUrl = "";
      }, { once: true });
      avatar.appendChild(image);
    });
  }

  function buildPhotoMap(...groups) {
    const photoMap = new Map();
    groups.flat().forEach((profile) => {
      const userId = Number(profile?.id || profile?.user_id || 0);
      const photoUrl = String(profile?.photo_url || "").trim();
      if (userId && photoUrl) {
        photoMap.set(userId, photoUrl);
      }
    });
    return photoMap;
  }

  function getPhotoUrl(person) {
    const directPhotoUrl = String(person?.photo_url || "").trim();
    if (directPhotoUrl) {
      return directPhotoUrl;
    }
    const userId = Number(person?.id || 0);
    if (!userId) {
      return "";
    }
    return String(state.photoByUserId.get(userId) || "").trim();
  }

  function loadCelebrationPhotoStyles() {
    if (document.querySelector('link[data-celebration-photo-assets="true"]')) {
      return;
    }
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.dataset.celebrationPhotoAssets = "true";
    try {
      const currentScript = document.currentScript;
      const stylesheetUrl = new URL(currentScript ? currentScript.src : "/static/js/celebration-photos.js", window.location.href);
      stylesheetUrl.pathname = stylesheetUrl.pathname.replace(/\/js\/celebration-photos\.js$/, "/css/celebration-photos.css");
      link.href = stylesheetUrl.href;
    } catch (error) {
      link.href = "/static/css/celebration-photos.css";
    }
    document.head.appendChild(link);
  }
})();
