(function attachEventsSection() {
  const EVENTS_TOPIC = "connect_events";
  const FEED_MODULE_BULLETIN = "bulletin";
  const EVENTS_API_ENDPOINT = "/api/feed/events/";
  const EVENT_FORM_ID = "events-admin-form";
  const EVENT_LIST_ID = "events-list";
  const EVENT_PANEL_ID = "panel-events";
  const EVENT_BUTTON_SELECTOR = '[data-action="open-events-section"]';

  const currentScript = document.currentScript;
  const state = {
    canAdminister: false,
    currentUser: null,
    events: [],
    eventsActive: false,
    hasLoaded: false,
    isLoading: false,
    loadError: "",
    syncInProgress: false,
    toastTimer: null,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initEventsSection, { once: true });
  } else {
    initEventsSection();
  }

  function initEventsSection() {
    ensureEventsMarkup();
    correctReminderCopy();
    loadEventsStyles();
    document.addEventListener("click", handleEventsClick, true);
    document.addEventListener("change", handleEventsChange, true);
    document.addEventListener("submit", handleEventsSubmit, true);
    observePanelMutations();
    void loadSessionAndEvents();
  }

  function ensureEventsMarkup() {
    ensureEventsButton();
    ensureEventsPanel();
  }

  function ensureEventsButton() {
    if (document.querySelector(EVENT_BUTTON_SELECTOR)) {
      return;
    }
    const topnavRight = document.querySelector(".topnav-right");
    if (!topnavRight) {
      return;
    }
    const button = document.createElement("button");
    button.type = "button";
    button.className = "icon-btn";
    button.dataset.action = "open-events-section";
    button.title = "Events";
    button.setAttribute("aria-label", "Events");
    button.innerHTML = `
      <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" d="M8 2v4m8-4v4M3 10h18M5 6h14a2 2 0 012 2v11a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2z"></path>
        <path stroke-linecap="round" stroke-linejoin="round" d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01"></path>
      </svg>
    `;
    const resourcesButton = topnavRight.querySelector('[data-switch-tab="resources"]');
    if (resourcesButton) {
      topnavRight.insertBefore(button, resourcesButton);
    } else {
      topnavRight.appendChild(button);
    }
  }

  function ensureEventsPanel() {
    if (document.getElementById(EVENT_PANEL_ID)) {
      return;
    }
    const resourcesPanel = document.getElementById("panel-resources");
    if (!resourcesPanel || !resourcesPanel.parentElement) {
      return;
    }
    resourcesPanel.insertAdjacentHTML("beforebegin", `
      <section class="panel" id="panel-events">
        <div class="section-head">
          <div>
            <h2>Events</h2>
            <p>Event highlights and links to photo or video albums shared by Admin.</p>
          </div>
        </div>

        <form class="section-card story-form events-admin-form" id="events-admin-form" hidden>
          <div class="section-card-head">
            <div>
              <p class="widget-kicker">Admin Update</p>
              <h2 id="events-admin-form-title">Add Event</h2>
              <div class="mini-item-meta">Add external photo/video links only. Connect will not store media files here.</div>
            </div>
            <button type="button" class="btn-ghost" data-action="cancel-event-edit" id="events-cancel-edit-btn" hidden>Cancel Edit</button>
          </div>
          <input type="hidden" name="event_id" id="events-edit-id">
          <div class="events-form-grid">
            <label class="field">
              <span>Event title</span>
              <input type="text" name="title" maxlength="180" placeholder="Annual Townhall celebration" required>
            </label>
            <label class="field">
              <span>Event date</span>
              <input type="date" name="event_date" required>
            </label>
          </div>
          <label class="field">
            <span>Short description</span>
            <textarea name="description" rows="4" placeholder="Share what took place at the event." required></textarea>
          </label>
          <label class="field">
            <span>Cover image link</span>
            <input type="url" name="cover_image_url" placeholder="https://...">
          </label>
          <label class="field">
            <span>Photo / video links</span>
            <textarea name="media_links" rows="5" placeholder="One link per line, or Label | https://..."></textarea>
          </label>
          <label class="events-publish-toggle">
            <input type="checkbox" name="is_published" checked>
            <span>Publish for employees</span>
          </label>
          <div class="form-actions">
            <p>Employees can view events and open links. Only Connect admins can add, edit, publish, unpublish, or delete events.</p>
            <button type="submit" class="btn-warm" id="events-submit-btn">Publish Event</button>
          </div>
        </form>

        <section class="events-grid" id="events-list"></section>
      </section>
    `);
  }

  function correctReminderCopy() {
    const reminderCopy = document.querySelector(".announcement-reminder-copy");
    if (reminderCopy && reminderCopy.textContent.includes("importance information")) {
      reminderCopy.textContent = reminderCopy.textContent.replace("importance information", "important information");
    }
  }

  function loadEventsStyles() {
    if (document.querySelector('link[data-events-assets="true"]')) {
      return;
    }
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.dataset.eventsAssets = "true";
    try {
      const stylesheetUrl = new URL(currentScript ? currentScript.src : "/static/js/events.js", window.location.href);
      stylesheetUrl.pathname = stylesheetUrl.pathname.replace(/\/js\/events\.js$/, "/css/events.css");
      link.href = stylesheetUrl.href;
    } catch (error) {
      link.href = "/static/css/events.css";
    }
    document.head.appendChild(link);
  }

  async function loadSessionAndEvents() {
    await hydrateCurrentUser();
    await loadEventPosts();
    renderEventsSection();
  }

  async function hydrateCurrentUser() {
    const auth = window.AcuiteConnectAuth;
    if (!auth) {
      state.canAdminister = false;
      return;
    }
    try {
      const session = auth.fetchCurrentSession ? await auth.fetchCurrentSession() : null;
      state.currentUser = (session && session.user) || (auth.getAuthenticatedUser && auth.getAuthenticatedUser()) || null;
      state.canAdminister = Boolean(state.currentUser && state.currentUser.access_rights && state.currentUser.access_rights.can_administer);
    } catch (error) {
      state.currentUser = null;
      state.canAdminister = false;
    }
  }

  async function loadEventPosts() {
    const auth = window.AcuiteConnectAuth;
    state.isLoading = true;
    state.loadError = "";
    renderEventsSection();

    if (!auth || !auth.apiRequest) {
      state.events = [];
      state.loadError = "Events are unavailable in this build.";
      state.isLoading = false;
      state.hasLoaded = true;
      return;
    }

    try {
      const payload = await auth.apiRequest(`${EVENTS_API_ENDPOINT}?limit=100`);
      state.events = Array.isArray(payload.results)
        ? sortEventsNewestFirst(payload.results.map(mapEventPost))
        : [];
    } catch (error) {
      state.events = [];
      state.loadError = error.message || "Could not load Events.";
    } finally {
      state.isLoading = false;
      state.hasLoaded = true;
    }
  }

  function handleEventsClick(event) {
    const action = event.target.closest("[data-action]");
    const actionName = action ? action.dataset.action : "";

    if (actionName === "open-events-section") {
      event.preventDefault();
      event.stopPropagation();
      openEventsPanel();
      return;
    }

    if (actionName === "edit-event") {
      event.preventDefault();
      event.stopPropagation();
      startEventEdit(action.dataset.id);
      return;
    }

    if (actionName === "cancel-event-edit") {
      event.preventDefault();
      event.stopPropagation();
      resetEventForm();
      return;
    }

    if (actionName === "toggle-event-publication") {
      event.preventDefault();
      event.stopPropagation();
      void toggleEventPublication(action.dataset.id);
      return;
    }

    if (actionName === "delete-event") {
      event.preventDefault();
      event.stopPropagation();
      void deleteEventPost(action.dataset.id);
      return;
    }

    if (event.target.closest("[data-switch-tab]") && state.eventsActive) {
      state.eventsActive = false;
      syncEventsPanel(false);
    }
  }

  function handleEventsSubmit(event) {
    if (event.target && event.target.id === EVENT_FORM_ID) {
      event.preventDefault();
      event.stopPropagation();
      void submitEventPost(event.target);
    }
  }

  function handleEventsChange(event) {
    const form = document.getElementById(EVENT_FORM_ID);
    if (form && event.target && event.target.name === "is_published" && form.contains(event.target)) {
      syncEventFormControls(form);
    }
  }

  function openEventsPanel() {
    state.eventsActive = true;
    syncEventsPanel(true);
    if (!state.hasLoaded) {
      void loadSessionAndEvents();
    }
    window.requestAnimationFrame(() => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  function syncEventsPanel(shouldActivate) {
    const panel = document.getElementById(EVENT_PANEL_ID);
    const eventButton = document.querySelector(EVENT_BUTTON_SELECTOR);
    if (!panel) {
      return;
    }

    state.syncInProgress = true;
    if (shouldActivate) {
      document.querySelectorAll(".panel").forEach((candidate) => {
        candidate.classList.toggle("active", candidate === panel);
      });
      document.querySelectorAll(".sidebar-left .tab").forEach((tab) => {
        tab.classList.remove("active");
      });
      document.querySelectorAll(".topnav-right [data-switch-tab]").forEach((button) => {
        button.classList.remove("active");
      });
    }
    if (eventButton) {
      eventButton.classList.toggle("active", shouldActivate);
    }
    state.syncInProgress = false;
  }

  function observePanelMutations() {
    const observer = new MutationObserver(() => {
      if (state.syncInProgress || !state.eventsActive) {
        return;
      }
      window.requestAnimationFrame(() => syncEventsPanel(true));
    });
    observer.observe(document.body, {
      attributes: true,
      subtree: true,
      attributeFilter: ["class"],
    });
  }

  function renderEventsSection() {
    const form = document.getElementById(EVENT_FORM_ID);
    const list = document.getElementById(EVENT_LIST_ID);

    if (form) {
      form.hidden = !state.canAdminister;
      syncEventFormControls(form);
    }
    if (!list) {
      return;
    }

    if (state.isLoading && !state.hasLoaded) {
      list.innerHTML = '<div class="empty-state">Loading Events...</div>';
      return;
    }

    if (state.loadError) {
      list.innerHTML = `<div class="empty-state">${escapeHtml(state.loadError)}</div>`;
      return;
    }

    const visibleEvents = state.canAdminister
      ? state.events
      : state.events.filter((eventPost) => eventPost.moderationStatus === "published");

    if (!visibleEvents.length) {
      list.innerHTML = '<div class="empty-state">Event updates will appear here once Admin publishes the first event.</div>';
      return;
    }

    list.innerHTML = visibleEvents.map(renderEventCard).join("");
  }

  function renderEventCard(eventPost) {
    const isPublished = eventPost.moderationStatus === "published";
    const coverDate = eventCoverDateParts(eventPost);
    const statusChip = state.canAdminister
      ? `<span class="mini-chip ${isPublished ? "success" : ""}">${isPublished ? "Published" : "Unpublished"}</span>`
      : "";
    const mediaLinks = eventPost.mediaLinks.length
      ? eventPost.mediaLinks.map((link) => `
          <a class="btn-outline" href="${escapeHtml(link.url)}" target="_blank" rel="noopener noreferrer">
            ${escapeHtml(link.label)}
          </a>
        `).join("")
      : '<div class="mini-item-meta">Media links will be added here.</div>';
    const adminActions = state.canAdminister
      ? `<div class="event-admin-actions">
          <button type="button" class="btn-link" data-action="edit-event" data-id="${escapeHtml(eventPost.sourceId)}">Edit</button>
          <button type="button" class="btn-link" data-action="toggle-event-publication" data-id="${escapeHtml(eventPost.sourceId)}">
            ${isPublished ? "Unpublish" : "Publish"}
          </button>
          <button type="button" class="btn-link post-delete-btn" data-action="delete-event" data-id="${escapeHtml(eventPost.sourceId)}">Delete</button>
        </div>`
      : "";

    return `
      <article class="section-card event-card" id="event-${escapeHtml(eventPost.sourceId)}">
        <div class="event-cover ${eventPost.coverImageUrl ? "has-image" : "event-cover-designed"}">
          ${eventPost.coverImageUrl ? `<img src="${escapeHtml(eventPost.coverImageUrl)}" alt="${escapeHtml(eventPost.title)} cover" loading="lazy">` : ""}
          <div class="event-cover-content">
            <span class="event-cover-kicker">Acuité Events</span>
            <span class="event-cover-rule" aria-hidden="true"></span>
            <span class="event-cover-date">
              <strong>${escapeHtml(coverDate.day)}</strong>
              <span>${escapeHtml(coverDate.monthYear)}</span>
            </span>
          </div>
        </div>
        <div class="event-card-body">
          <div class="resource-card-head">
            <div>
              <p class="widget-kicker">${escapeHtml(eventPost.eventDateLabel || "Event")}</p>
              <h3>${escapeHtml(eventPost.title)}</h3>
            </div>
            ${statusChip}
          </div>
          <p>${escapeHtml(eventPost.description)}</p>
          <div class="event-link-list">${mediaLinks}</div>
          ${adminActions}
        </div>
      </article>
    `;
  }

  function mapEventPost(post) {
    const metadata = post && typeof post.metadata === "object" && post.metadata ? post.metadata : {};
    return {
      sourceId: String(post.id),
      title: String(post.title || "Event"),
      description: String(post.body || ""),
      eventDate: String(metadata.event_date || ""),
      eventDateLabel: String(metadata.event_date_label || formatEventDate(metadata.event_date) || "Event"),
      coverImageUrl: String(metadata.event_cover_image_url || ""),
      mediaLinks: normalizeMediaLinks(metadata.event_media_links),
      moderationStatus: String(post.moderation_status || "draft"),
      createdAt: String(post.created_at || ""),
      publishedAt: String(post.published_at || ""),
    };
  }

  function eventCoverDateParts(eventPost) {
    const timestamp = parseEventDate(eventPost.eventDate);
    if (!timestamp) {
      return { day: "EV", monthYear: "Event" };
    }
    const date = new Date(timestamp);
    return {
      day: new Intl.DateTimeFormat("en-IN", {
        day: "2-digit",
        timeZone: "UTC",
      }).format(date),
      monthYear: new Intl.DateTimeFormat("en-IN", {
        month: "short",
        year: "numeric",
        timeZone: "UTC",
      }).format(date).toUpperCase(),
    };
  }

  function sortEventsNewestFirst(events) {
    return events.slice().sort((left, right) => {
      const leftDate = eventSortTime(left);
      const rightDate = eventSortTime(right);
      return rightDate - leftDate;
    });
  }

  function eventSortTime(eventPost) {
    return (
      parseEventDate(eventPost.eventDate)
      || Date.parse(eventPost.publishedAt || "")
      || Date.parse(eventPost.createdAt || "")
      || 0
    );
  }

  function startEventEdit(eventId) {
    if (!state.canAdminister) {
      return;
    }
    const eventPost = state.events.find((item) => item.sourceId === String(eventId));
    const form = document.getElementById(EVENT_FORM_ID);
    if (!eventPost || !form) {
      showEventsToast("Could not find that event.", true);
      return;
    }
    form.elements.event_id.value = eventPost.sourceId;
    form.elements.title.value = eventPost.title;
    form.elements.event_date.value = eventPost.eventDate;
    form.elements.description.value = eventPost.description;
    form.elements.cover_image_url.value = eventPost.coverImageUrl;
    form.elements.media_links.value = eventPost.mediaLinks
      .map((link) => `${link.label} | ${link.url}`)
      .join("\n");
    form.elements.is_published.checked = eventPost.moderationStatus === "published";
    syncEventFormControls(form);
    form.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function submitEventPost(form) {
    if (!state.canAdminister) {
      showEventsToast("Admin access is required.", true);
      return;
    }

    const submitButton = document.getElementById("events-submit-btn");
    const originalLabel = submitButton ? submitButton.textContent : "";
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Saving...";
    }

    try {
      const eventId = String(form.elements.event_id.value || "").trim();
      const payload = buildEventPayload(form);
      if (eventId) {
        await apiRequest(`${EVENTS_API_ENDPOINT}${eventId}/`, {
          method: "PATCH",
          body: payload,
        });
        showEventsToast("Event updated.");
      } else {
        await apiRequest(EVENTS_API_ENDPOINT, {
          method: "POST",
          body: payload,
        });
        showEventsToast(payload.moderation_status === "published" ? "Event published." : "Event saved as unpublished.");
      }
      resetEventForm();
      await loadEventPosts();
      renderEventsSection();
      syncEventsPanel(state.eventsActive);
    } catch (error) {
      showEventsToast(error.message || "Could not save the event.", true);
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = originalLabel || "Publish Event";
      }
      syncEventFormControls(form);
    }
  }

  function buildEventPayload(form) {
    const title = readRequiredText(form.elements.title.value, "Event title");
    const description = readRequiredText(form.elements.description.value, "Short description");
    const eventDate = readRequiredText(form.elements.event_date.value, "Event date");
    const coverImageUrl = readOptionalUrl(form.elements.cover_image_url.value, "Cover image link");
    const mediaLinks = parseMediaLinks(form.elements.media_links.value);
    const moderationStatus = form.elements.is_published.checked ? "published" : "draft";

    return {
      title,
      body: description,
      kind: "announcement",
      module: FEED_MODULE_BULLETIN,
      topic: EVENTS_TOPIC,
      visibility: "company",
      post_as_company: true,
      allow_comments: false,
      pinned: false,
      moderation_status: moderationStatus,
      metadata: {
        post_as_company: true,
        bulletin_category: "events",
        event_post: true,
        event_date: eventDate,
        event_date_label: formatEventDate(eventDate),
        event_cover_image_url: coverImageUrl,
        event_media_links: mediaLinks,
      },
    };
  }

  async function toggleEventPublication(eventId) {
    const eventPost = state.events.find((item) => item.sourceId === String(eventId));
    if (!eventPost) {
      showEventsToast("Could not find that event.", true);
      return;
    }
    const nextStatus = eventPost.moderationStatus === "published" ? "draft" : "published";
    try {
      await apiRequest(`${EVENTS_API_ENDPOINT}${eventPost.sourceId}/`, {
        method: "PATCH",
        body: { moderation_status: nextStatus },
      });
      showEventsToast(nextStatus === "published" ? "Event published." : "Event unpublished.");
      await loadEventPosts();
      renderEventsSection();
      syncEventsPanel(state.eventsActive);
    } catch (error) {
      showEventsToast(error.message || "Could not update the event.", true);
    }
  }

  async function deleteEventPost(eventId) {
    const eventPost = state.events.find((item) => item.sourceId === String(eventId));
    if (!eventPost || !window.confirm(`Delete "${eventPost.title}" from Events?`)) {
      return;
    }
    try {
      await apiRequest(`${EVENTS_API_ENDPOINT}${eventPost.sourceId}/`, {
        method: "DELETE",
      });
      showEventsToast("Event deleted.");
      resetEventForm();
      await loadEventPosts();
      renderEventsSection();
      syncEventsPanel(state.eventsActive);
    } catch (error) {
      showEventsToast(error.message || "Could not delete the event.", true);
    }
  }

  function resetEventForm() {
    const form = document.getElementById(EVENT_FORM_ID);
    if (!form) {
      return;
    }
    form.reset();
    form.elements.event_id.value = "";
    form.elements.is_published.checked = true;
    syncEventFormControls(form);
  }

  function syncEventFormControls(form) {
    const targetForm = form || document.getElementById(EVENT_FORM_ID);
    if (!targetForm) {
      return;
    }
    const isEditing = Boolean(targetForm.elements.event_id.value);
    const formTitle = document.getElementById("events-admin-form-title");
    const cancelButton = document.getElementById("events-cancel-edit-btn");
    const submitButton = document.getElementById("events-submit-btn");
    const willPublish = targetForm.elements.is_published.checked;

    if (formTitle) {
      formTitle.textContent = isEditing ? "Edit Event" : "Add Event";
    }
    if (cancelButton) {
      cancelButton.hidden = !isEditing;
    }
    if (submitButton && !submitButton.disabled) {
      submitButton.textContent = isEditing
        ? (willPublish ? "Save and Publish" : "Save as Unpublished")
        : (willPublish ? "Publish Event" : "Save as Unpublished");
    }
  }

  function parseMediaLinks(rawValue) {
    return String(rawValue || "")
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line, index) => {
        const separatorIndex = line.indexOf("|");
        const hasLabel = separatorIndex >= 0;
        const label = hasLabel ? line.slice(0, separatorIndex).trim() : "";
        const urlText = hasLabel ? line.slice(separatorIndex + 1).trim() : line;
        const url = readRequiredUrl(urlText, `Media link ${index + 1}`);
        return {
          label: (label || inferMediaLabel(url, index)).slice(0, 80),
          url,
          type: "link",
        };
      });
  }

  function normalizeMediaLinks(value) {
    if (!Array.isArray(value)) {
      return [];
    }
    return value
      .map((link, index) => {
        if (!link || typeof link !== "object") {
          return null;
        }
        const url = String(link.url || "").trim();
        if (!isHttpUrl(url)) {
          return null;
        }
        const label = String(link.label || inferMediaLabel(url, index)).trim();
        return {
          label: label || inferMediaLabel(url, index),
          url,
          type: String(link.type || "link"),
        };
      })
      .filter(Boolean);
  }

  function inferMediaLabel(url, index) {
    const normalizedUrl = String(url || "").toLowerCase();
    if (/(youtube\.com|youtu\.be|vimeo\.com|\.mp4($|\?)|\.mov($|\?)|\.webm($|\?))/.test(normalizedUrl)) {
      return "Watch Video";
    }
    if (/(photos\.app\.goo\.gl|drive\.google\.com|onedrive\.live\.com|sharepoint\.com|album|photos)/.test(normalizedUrl)) {
      return "Open Album";
    }
    return `Open Link ${index + 1}`;
  }

  function readRequiredText(value, label) {
    const text = String(value || "").trim();
    if (!text) {
      throw new Error(`${label} is required.`);
    }
    return text;
  }

  function readOptionalUrl(value, label) {
    const text = String(value || "").trim();
    if (!text) {
      return "";
    }
    return readRequiredUrl(text, label);
  }

  function readRequiredUrl(value, label) {
    const text = String(value || "").trim();
    if (!isHttpUrl(text)) {
      throw new Error(`${label} must start with http:// or https://.`);
    }
    return new URL(text).href;
  }

  function isHttpUrl(value) {
    if (!/^https?:\/\//i.test(String(value || "").trim())) {
      return false;
    }
    try {
      const parsed = new URL(value);
      return ["http:", "https:"].includes(parsed.protocol);
    } catch (error) {
      return false;
    }
  }

  async function apiRequest(path, options) {
    const auth = window.AcuiteConnectAuth;
    if (!auth || !auth.apiRequest) {
      throw new Error("Events are unavailable in this build.");
    }
    return auth.apiRequest(path, options);
  }

  function formatEventDate(value) {
    const timestamp = parseEventDate(value);
    if (!timestamp) {
      return "";
    }
    return new Intl.DateTimeFormat("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      timeZone: "UTC",
    }).format(new Date(timestamp));
  }

  function parseEventDate(value) {
    const match = String(value || "").match(/^(\d{4})-(\d{2})-(\d{2})$/);
    if (!match) {
      return 0;
    }
    return Date.UTC(Number(match[1]), Number(match[2]) - 1, Number(match[3]));
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function showEventsToast(message, isError) {
    let toast = document.querySelector(".events-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "events-toast";
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.toggle("is-error", Boolean(isError));
    window.clearTimeout(state.toastTimer);
    state.toastTimer = window.setTimeout(() => {
      toast.remove();
    }, isError ? 5200 : 3200);
  }
})();
