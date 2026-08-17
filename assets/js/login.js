document.addEventListener("DOMContentLoaded", () => {
  void initLoginPage();
});

function getPostLoginTarget(user) {
  const params = new URLSearchParams(window.location.search);
  const fallbackPath = "/?landing=home";
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
