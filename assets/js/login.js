document.addEventListener("DOMContentLoaded", () => {
  void initLoginPage();
});

function getPostLoginTarget(user) {
  const params = new URLSearchParams(window.location.search);
  const fallbackPath =
    user && user.access_rights && user.access_rights.can_administer
      ? "/admin-console.html"
      : "/";
  const next = params.get("next") || fallbackPath;

  try {
    const target = new URL(next, window.location.origin);
    if (target.origin !== window.location.origin) {
      return fallbackPath;
    }
    return `${target.pathname}${target.search}${target.hash}`;
  } catch (error) {
    return fallbackPath;
  }
}

async function initLoginPage() {
  const auth = window.AcuiteConnectAuth;
  if (!auth) {
    return;
  }

  const loginButton = document.getElementById("employee-sso-login-button");
  const ssoEnabled = loginButton && loginButton.dataset.ssoEnabled === "true";
  const params = new URLSearchParams(window.location.search);
  const errorMessage = params.get("error");

  if (errorMessage) {
    showStatus(errorMessage, "warning");
  }

  if (loginButton) {
    loginButton.addEventListener("click", () => {
      if (!ssoEnabled) {
        showStatus("Employee SSO is not configured yet for this environment.", "warning");
        return;
      }
      showStatus("Redirecting to Employee SSO...", "info");
      window.location.href = `/api/accounts/auth/employee-sso/start/?next=${encodeURIComponent(
        getPostLoginTarget(null)
      )}`;
    });
  }

  try {
    const session = await auth.fetchCurrentSession({ forceRefresh: true });
    if (session.authenticated && session.user) {
      if (session.user.access_rights && session.user.access_rights.can_employee) {
        window.location.replace(getPostLoginTarget(session.user));
        return;
      }
      window.location.replace("/access-denied.html");
      return;
    }
  } catch (error) {
    showStatus("Could not verify the current session. You can still continue with Employee SSO.", "warning");
    return;
  }

  if (ssoEnabled) {
    showStatus("Use Employee SSO to sign in to Acuité Connect.", "info");
  } else {
    showStatus("Employee SSO is not configured yet for this environment.", "warning");
  }
}

function showStatus(message, tone = "info") {
  const node = document.getElementById("auth-status");
  if (!node) {
    return;
  }
  node.hidden = false;
  node.dataset.tone = tone;
  node.textContent = message;
}
