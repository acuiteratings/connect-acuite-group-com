(function attachAuthHelpers() {
  const AUTH_STORAGE_KEY = "acuite-connect-auth-v1";
  const COMPANY_DOMAIN = "@acuite.in";

  function readSession() {
    try {
      const raw = window.localStorage.getItem(AUTH_STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  }

  function writeSession(session) {
    try {
      window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
    } catch (error) {
      return;
    }
  }

  function clearSession() {
    try {
      window.localStorage.removeItem(AUTH_STORAGE_KEY);
    } catch (error) {
      return;
    }
  }

  function buildUser(email) {
    const normalizedEmail = String(email || "").trim().toLowerCase();
    const localPart = normalizedEmail.split("@")[0] || "employee";
    const segments = localPart.split(/[._-]+/).filter(Boolean);
    const name = segments.length
      ? segments.map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join(" ")
      : "Acuité Employee";
    const initials = segments.length >= 2
      ? `${segments[0][0]}${segments[1][0]}`.toUpperCase()
      : name.slice(0, 2).toUpperCase();

    return {
      email: normalizedEmail,
      name,
      initials,
      role: "Employee - Acuité Connect",
      city: "Mumbai",
      signedInAt: new Date().toISOString(),
    };
  }

  function isCompanyEmail(email) {
    return String(email || "").trim().toLowerCase().endsWith(COMPANY_DOMAIN);
  }

  function requireAuth(options) {
    const loginPath = (options && options.loginPath) || "/login.html";
    const session = readSession();
    if (session && session.email) {
      return session;
    }
    window.location.href = loginPath;
    return null;
  }

  function redirectIfAuthenticated(options) {
    const homePath = (options && options.homePath) || "/";
    const session = readSession();
    if (session && session.email) {
      window.location.href = homePath;
      return session;
    }
    return null;
  }

  window.AcuiteConnectAuth = {
    AUTH_STORAGE_KEY,
    COMPANY_DOMAIN,
    readSession,
    writeSession,
    clearSession,
    buildUser,
    isCompanyEmail,
    requireAuth,
    redirectIfAuthenticated,
    getAuthenticatedUser: readSession,
  };
})();
