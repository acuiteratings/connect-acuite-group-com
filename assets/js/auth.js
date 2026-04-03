(function attachAuthHelpers() {
  const COMPANY_DOMAIN = "@acuite.in";
  const ME_ENDPOINT = "/api/accounts/me/";
  let cachedSession = null;
  let sessionRequest = null;
  let sessionExpiryTimer = null;

  function readCookie(name) {
    const prefix = `${name}=`;
    const cookies = document.cookie ? document.cookie.split(";") : [];
    for (const cookie of cookies) {
      const trimmed = cookie.trim();
      if (trimmed.startsWith(prefix)) {
        return decodeURIComponent(trimmed.slice(prefix.length));
      }
    }
    return "";
  }

  function getCsrfToken() {
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken && metaToken.content) {
      return metaToken.content;
    }
    return readCookie("csrftoken");
  }

  async function parseJson(response) {
    const text = await response.text();
    if (!text) {
      return {};
    }

    try {
      return JSON.parse(text);
    } catch (error) {
      return { detail: text };
    }
  }

  function clearSessionExpiryTimer() {
    if (sessionExpiryTimer) {
      window.clearTimeout(sessionExpiryTimer);
      sessionExpiryTimer = null;
    }
  }

  function scheduleSessionExpiry(session) {
    clearSessionExpiryTimer();
    if (!session || !session.authenticated || !session.session_expires_at) {
      return;
    }

    const deadline = Date.parse(session.session_expires_at);
    if (!Number.isFinite(deadline)) {
      return;
    }

    const delay = deadline - Date.now();
    const triggerLogout = async () => {
      try {
        const payload = await logout();
        if (payload && payload.redirect_url) {
          window.location.href = payload.redirect_url;
          return;
        }
      } finally {
        if (window.location.pathname !== "/login.html") {
          window.location.href = "/login.html";
        }
      }
    };

    if (delay <= 0) {
      void triggerLogout();
      return;
    }

    sessionExpiryTimer = window.setTimeout(() => {
      void triggerLogout();
    }, delay);
  }

  async function apiRequest(path, options = {}) {
    const requestOptions = { ...options };
    const method = (requestOptions.method || "GET").toUpperCase();
    const headers = new Headers(requestOptions.headers || {});
    const isJsonBody =
      requestOptions.body &&
      typeof requestOptions.body === "object" &&
      !(requestOptions.body instanceof FormData);

    if (isJsonBody) {
      headers.set("Content-Type", "application/json");
      requestOptions.body = JSON.stringify(requestOptions.body);
    }

    if (!["GET", "HEAD", "OPTIONS", "TRACE"].includes(method)) {
      const csrfToken = getCsrfToken();
      if (csrfToken) {
        headers.set("X-CSRFToken", csrfToken);
      }
    }

    const response = await fetch(path, {
      credentials: "same-origin",
      ...requestOptions,
      headers,
    });
    const payload = await parseJson(response);

    if (!response.ok) {
      const error = new Error(payload.detail || "Request failed.");
      error.status = response.status;
      error.code = payload.code || "request_failed";
      error.payload = payload;
      throw error;
    }

    return payload;
  }

  function isAuthSessionError(error) {
    return Boolean(error && [401, 403].includes(Number(error.status)));
  }

  function clearSession() {
    cachedSession = null;
    sessionRequest = null;
    clearSessionExpiryTimer();
  }

  function hydrateSession(session) {
    if (!session || !session.authenticated || !session.user) {
      return false;
    }
    cachedSession = session;
    scheduleSessionExpiry(session);
    return true;
  }

  async function fetchCurrentSession({ forceRefresh = false } = {}) {
    if (!forceRefresh && cachedSession) {
      return cachedSession;
    }
    if (!forceRefresh && sessionRequest) {
      return sessionRequest;
    }

    sessionRequest = apiRequest(ME_ENDPOINT)
      .then((payload) => {
        cachedSession = payload;
        scheduleSessionExpiry(payload);
        return payload;
      })
      .catch((error) => {
        if (isAuthSessionError(error)) {
          clearSession();
          return { authenticated: false, user: null };
        }
        throw error;
      })
      .finally(() => {
        sessionRequest = null;
      });

    return sessionRequest;
  }

  function isCompanyEmail(email) {
    return String(email || "").trim().toLowerCase().endsWith(COMPANY_DOMAIN);
  }

  async function requireAuth(options = {}) {
    const loginPath = options.loginPath || "/login.html";
    let session = cachedSession;
    try {
      if (!(session && session.authenticated && session.user)) {
        session = await fetchCurrentSession();
      }
      if (session && session.authenticated && session.user) {
        return session.user;
      }
      session = await fetchCurrentSession({ forceRefresh: true });
      if (session && session.authenticated && session.user) {
        return session.user;
      }
    } catch (error) {
      clearSession();
    }
    window.location.href = loginPath;
    return null;
  }

  async function redirectIfAuthenticated(options = {}) {
    const homePath = options.homePath || "/";
    let session = cachedSession;
    try {
      if (!(session && session.authenticated && session.user)) {
        session = await fetchCurrentSession();
      }
      if (session && session.authenticated && session.user) {
        window.location.href = homePath;
        return session.user;
      }
      session = await fetchCurrentSession({ forceRefresh: true });
      if (session && session.authenticated && session.user) {
        window.location.href = homePath;
        return session.user;
      }
    } catch (error) {
      clearSession();
    }
    return null;
  }

  async function logout() {
    try {
      return await apiRequest("/api/accounts/auth/logout/", { method: "POST" });
    } finally {
      clearSession();
    }
  }

  window.AcuiteConnectAuth = {
    COMPANY_DOMAIN,
    apiRequest,
    clearSession,
    fetchCurrentSession,
    getAuthenticatedUser() {
      return cachedSession && cachedSession.authenticated ? cachedSession.user : null;
    },
    getCsrfToken,
    hydrateSession,
    isCompanyEmail,
    logout,
    redirectIfAuthenticated,
    requireAuth,
  };
})();
