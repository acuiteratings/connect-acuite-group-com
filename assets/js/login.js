const authFlow = {
  challengeToken: "",
  email: "",
  authPolicy: {
    password_max_age_days: 90,
  },
};
const CONNECT_BOOT_USER_KEY = "acuite-connect-boot-user";

document.addEventListener("DOMContentLoaded", () => {
  void initLoginPage();
});

function getDefaultPostLoginTarget(user) {
  const accessRights = user && user.access_rights ? user.access_rights : {};
  return accessRights.can_administer ? "/admin-console.html" : "/";
}

function primeConnectBootSession(session) {
  if (!session || !session.authenticated || !session.user) {
    return;
  }
  if (getDefaultPostLoginTarget(session.user) !== "/") {
    return;
  }
  try {
    window.sessionStorage.setItem(
      CONNECT_BOOT_USER_KEY,
      JSON.stringify({
        created_at: Date.now(),
        session: {
          authenticated: true,
          user: session.user,
          session_expires_at: session.session_expires_at || null,
          auth_policy: session.auth_policy || null,
        },
      })
    );
  } catch (error) {
    // Ignore sessionStorage issues and continue with the normal redirect.
  }
}

function getPostLoginTarget(user) {
  const params = new URLSearchParams(window.location.search);
  const fallbackPath = getDefaultPostLoginTarget(user);
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
  updatePolicyCopy();
  disablePasswordStep();
  hidePasswordResetStep();

  document.getElementById("connect-access-form").addEventListener("submit", (event) => {
    void handleAccessForm(event);
  });
  document.getElementById("connect-password-form").addEventListener("submit", (event) => {
    void handlePasswordForm(event);
  });
  document
    .getElementById("connect-password-change-form")
    .addEventListener("submit", (event) => {
      void handlePasswordChangeForm(event);
    });
  document.getElementById("forgot-password-button").addEventListener("click", (event) => {
    void handleForgotPassword(event);
  });

  bindToggle("password-toggle", "login-password");
  bindToggle("new-password-toggle", "new-password");
  bindToggle("confirm-password-toggle", "confirm-password");

  void resolveExistingSession(auth);
}

async function resolveExistingSession(auth) {
  try {
    const session = await auth.fetchCurrentSession({ forceRefresh: true });
    if (session.authenticated) {
      primeConnectBootSession(session);
      window.location.replace(getPostLoginTarget(session.user));
      return;
    }
    authFlow.authPolicy = session.auth_policy || authFlow.authPolicy;
    updatePolicyCopy();
  } catch (error) {
    // Leave the login form usable even if the session probe fails.
  }
}

function bindToggle(buttonId, inputId) {
  const button = document.getElementById(buttonId);
  const input = document.getElementById(inputId);
  if (!button || !input) {
    return;
  }

  button.addEventListener("click", () => {
    const showingPassword = input.type === "text";
    input.type = showingPassword ? "password" : "text";
    button.textContent = showingPassword ? "Show" : "Hide";
    button.setAttribute("aria-pressed", String(!showingPassword));
  });
}

async function handleAccessForm(event) {
  event.preventDefault();

  const submitter = event.submitter;
  const action = submitter ? submitter.value : "";
  const emailInput = document.getElementById("login-email");
  const codeInput = document.getElementById("login-code");
  const email = emailInput.value.trim().toLowerCase();

  clearErrors();

  if (!email) {
    showFieldError("email-error", "Enter your employee email ID.");
    return;
  }

  if (action === "send_code") {
    showStatus("Sending OTP...", "info");
    await withButtonBusy(submitter, async () => {
      const response = await window.AcuiteConnectAuth.apiRequest(
        "/api/accounts/auth/request-otp/",
        {
          method: "POST",
          body: { email },
        }
      );

      authFlow.challengeToken = response.challenge_token;
      authFlow.email = email;
      codeInput.disabled = false;
      codeInput.value = "";
      document.getElementById("validate-code-button").disabled = false;
      disablePasswordStep();
      hidePasswordResetStep();
      showStatus(response.detail, "success");
      updateStep(
        "Step 2 of 3",
        "Enter the OTP from your email to unlock the password step."
      );
      showOtpPreview(response.preview_code || "");
      codeInput.focus();
    }, "email-error");
    return;
  }

  if (action === "validate_code") {
    if (!authFlow.challengeToken) {
      showFieldError("code-error", "Request an OTP first.");
      return;
    }

    await withButtonBusy(submitter, async () => {
      const response = await window.AcuiteConnectAuth.apiRequest(
        "/api/accounts/auth/verify-otp/",
        {
          method: "POST",
          body: {
            challenge_token: authFlow.challengeToken,
            otp: codeInput.value.trim(),
          },
        }
      );

      showStatus(response.detail, "success");
      enablePasswordStep();
      updateStep(
        "Step 3 of 3",
        "OTP verified. Enter your password to continue."
      );
      document.getElementById("login-password").focus();
    }, "code-error");
  }
}

async function handlePasswordForm(event) {
  event.preventDefault();
  clearErrors();

  if (!authFlow.challengeToken) {
    showFieldError("password-error", "Request and validate an OTP before logging in.");
    return;
  }

  const password = document.getElementById("login-password").value;
  const submitButton = document.getElementById("login-button");

  await withButtonBusy(submitButton, async () => {
    const response = await window.AcuiteConnectAuth.apiRequest("/api/accounts/auth/login/", {
      method: "POST",
      body: {
        challenge_token: authFlow.challengeToken,
        password,
      },
    });

    if (response.requires_password_change) {
      showPasswordResetStep(response.reason);
      showStatus(response.detail, "warning");
      updateStep(
        "Password update required",
        "Set a new password before Acuité Connect can sign you in."
      );
      return;
    }

    showStatus("Login successful. Redirecting to Acuité Connect...", "success");
    primeConnectBootSession(response);
    window.location.replace(getPostLoginTarget(response.user));
  }, "password-error");
}

async function handleForgotPassword(event) {
  event.preventDefault();
  clearErrors();

  const emailInput = document.getElementById("login-email");
  const codeInput = document.getElementById("login-code");
  const email = emailInput.value.trim().toLowerCase();
  const trigger = event.currentTarget;

  if (!email) {
    showFieldError("email-error", "Enter your employee email ID first.");
    emailInput.focus();
    return;
  }

  await withButtonBusy(trigger, async () => {
    const response = await window.AcuiteConnectAuth.apiRequest(
      "/api/accounts/auth/forgot-password/",
      {
        method: "POST",
        body: { email },
      }
    );

    authFlow.challengeToken = "";
    authFlow.email = email;
    codeInput.disabled = true;
    codeInput.value = "";
    document.getElementById("validate-code-button").disabled = true;
    disablePasswordStep();
    hidePasswordResetStep();
    showOtpPreview("");
    showStatus(response.detail, "info");
    updateStep(
      "Step 1 of 3",
      "Request a fresh OTP, then log in with the temporary password from your email."
    );
  }, "email-error");
}

async function handlePasswordChangeForm(event) {
  event.preventDefault();
  clearErrors();

  const submitButton = document.getElementById("change-password-button");
  const newPassword = document.getElementById("new-password").value;
  const confirmPassword = document.getElementById("confirm-password").value;

  await withButtonBusy(submitButton, async () => {
    const response = await window.AcuiteConnectAuth.apiRequest("/api/accounts/auth/change-password/", {
      method: "POST",
      body: {
        challenge_token: authFlow.challengeToken,
        new_password: newPassword,
        confirm_password: confirmPassword,
      },
    });

    showStatus("Password updated. Redirecting to Acuité Connect...", "success");
    updateStep("Access granted", "Your password has been updated and your session is now active.");
    primeConnectBootSession(response);
    window.location.replace(getPostLoginTarget(response.user));
  }, "new-password-error", "confirm-password-error");
}

function enablePasswordStep() {
  document.getElementById("login-password").disabled = false;
  document.getElementById("password-toggle").disabled = false;
  document.getElementById("login-button").disabled = false;
}

function disablePasswordStep() {
  const passwordInput = document.getElementById("login-password");
  const passwordToggle = document.getElementById("password-toggle");
  const loginButton = document.getElementById("login-button");
  passwordInput.disabled = true;
  passwordInput.value = "";
  passwordInput.type = "password";
  passwordToggle.disabled = true;
  passwordToggle.textContent = "Show";
  passwordToggle.setAttribute("aria-pressed", "false");
  loginButton.disabled = true;
}

function showPasswordResetStep(reason) {
  const panel = document.getElementById("connect-password-change-form");
  const copy = document.getElementById("password-reset-copy");
  panel.hidden = false;
  if (copy) {
    copy.textContent =
      reason === "expired"
        ? "Your password has crossed the 90-day rotation window. Set a new one to continue."
        : "This is your first login or an administrator has reset your password. Choose a new password to continue.";
  }
  document.getElementById("new-password").focus();
}

function hidePasswordResetStep() {
  const panel = document.getElementById("connect-password-change-form");
  panel.hidden = true;
  document.getElementById("new-password").value = "";
  document.getElementById("confirm-password").value = "";
  ["new-password", "confirm-password"].forEach((inputId) => {
    const input = document.getElementById(inputId);
    input.type = "password";
  });
  ["new-password-toggle", "confirm-password-toggle"].forEach((buttonId) => {
    const button = document.getElementById(buttonId);
    button.textContent = "Show";
    button.setAttribute("aria-pressed", "false");
  });
}

function showFieldError(id, message) {
  const node = document.getElementById(id);
  node.hidden = false;
  node.textContent = message;
}

function clearErrors() {
  [
    "email-error",
    "code-error",
    "password-error",
    "new-password-error",
    "confirm-password-error",
  ].forEach((id) => {
    const node = document.getElementById(id);
    node.hidden = true;
    node.textContent = "";
  });
}

function showStatus(message, tone = "info") {
  const node = document.getElementById("auth-status");
  node.hidden = false;
  node.dataset.tone = tone;
  node.textContent = message;
}

function updateStep(label, copy) {
  const labelNode = document.getElementById("auth-step-label");
  const copyNode = document.getElementById("auth-step-copy");
  if (!labelNode || !copyNode) {
    return;
  }
  labelNode.textContent = label;
  copyNode.textContent = copy;
}

function showOtpPreview(code) {
  const node = document.getElementById("otp-preview-line");
  if (!node) {
    return;
  }
  if (!code) {
    node.hidden = true;
    node.textContent = "";
    return;
  }

  node.hidden = false;
  node.innerHTML = `Preview OTP for this environment: <code>${escapeHtml(code)}</code>`;
}

function updatePolicyCopy() {
  const maxAgeDays =
    (authFlow.authPolicy && authFlow.authPolicy.password_max_age_days) || 90;
  const daysNode = document.getElementById("password-policy-days");
  const policyNode = document.getElementById("password-policy-copy");
  if (daysNode) {
    daysNode.textContent = String(maxAgeDays);
  }
  if (policyNode) {
    policyNode.textContent = `Passwords must be changed on first login and every ${maxAgeDays} days after that.`;
  }
}

async function withButtonBusy(button, action, ...errorIds) {
  if (button) {
    button.disabled = true;
  }

  try {
    await action();
  } catch (error) {
    const targetId = selectErrorTarget(error, errorIds);
    showFieldError(targetId, error.message || "Something went wrong. Please try again.");
  } finally {
    if (button) {
      button.disabled = false;
    }
  }
}

function selectErrorTarget(error, errorIds) {
  if (error && error.code === "password_confirmation_mismatch") {
    return "confirm-password-error";
  }
  if (
    error &&
    error.code === "password_invalid" &&
    Array.isArray(error.payload && error.payload.validation_messages)
  ) {
    return "new-password-error";
  }
  return errorIds[0] || "password-error";
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
