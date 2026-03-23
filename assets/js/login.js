const DEMO_PASSWORD = "acuite@123";

let pendingCode = "";
let validatedEmail = "";

document.addEventListener("DOMContentLoaded", initLoginPage);

function initLoginPage() {
  const auth = window.AcuiteConnectAuth;
  if (auth) {
    auth.redirectIfAuthenticated({ homePath: "/" });
  }

  const accessForm = document.getElementById("connect-access-form");
  const passwordForm = document.getElementById("connect-password-form");
  const passwordToggle = document.getElementById("password-toggle");

  accessForm.addEventListener("submit", handleAccessForm);
  passwordForm.addEventListener("submit", handlePasswordForm);
  passwordToggle.addEventListener("click", togglePasswordVisibility);
}

function handleAccessForm(event) {
  event.preventDefault();

  const submitter = event.submitter;
  const action = submitter ? submitter.value : "";
  const emailInput = document.getElementById("login-email");
  const codeInput = document.getElementById("login-code");
  const email = emailInput.value.trim().toLowerCase();

  clearErrors();

  if (action === "send_code") {
    if (!window.AcuiteConnectAuth.isCompanyEmail(email)) {
      showFieldError("email-error", "Use your Acuité company email ending with @acuite.in.");
      return;
    }

    pendingCode = String(Math.floor(100000 + Math.random() * 900000));
    validatedEmail = "";
    codeInput.disabled = false;
    document.getElementById("validate-code-button").disabled = false;
    disablePasswordStep();
    showStatus(`Code generated for ${email}. Preview code: ${pendingCode}`);
    return;
  }

  if (action === "validate_code") {
    if (!pendingCode) {
      showFieldError("code-error", "Send a code first.");
      return;
    }

    const enteredCode = codeInput.value.trim();
    if (enteredCode !== pendingCode) {
      showFieldError("code-error", "That code does not match the current preview code.");
      return;
    }

    validatedEmail = email;
    enablePasswordStep();
    showStatus(`Code validated for ${validatedEmail}. Enter your password to continue.`);
  }
}

function handlePasswordForm(event) {
  event.preventDefault();

  const passwordInput = document.getElementById("login-password");
  clearErrors();

  if (!validatedEmail) {
    showFieldError("password-error", "Validate your code before logging in.");
    return;
  }

  if (passwordInput.value !== DEMO_PASSWORD) {
    showFieldError("password-error", "Incorrect password for this preview environment.");
    return;
  }

  const user = window.AcuiteConnectAuth.buildUser(validatedEmail);
  window.AcuiteConnectAuth.writeSession(user);
  showStatus(`Login successful for ${validatedEmail}. Redirecting...`);
  window.setTimeout(() => {
    window.location.href = "/";
  }, 350);
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

function togglePasswordVisibility() {
  const passwordInput = document.getElementById("login-password");
  const passwordToggle = document.getElementById("password-toggle");
  const showingPassword = passwordInput.type === "text";
  passwordInput.type = showingPassword ? "password" : "text";
  passwordToggle.textContent = showingPassword ? "Show" : "Hide";
  passwordToggle.setAttribute("aria-pressed", String(!showingPassword));
}

function showFieldError(id, message) {
  const node = document.getElementById(id);
  node.hidden = false;
  node.textContent = message;
}

function clearErrors() {
  ["email-error", "code-error", "password-error"].forEach((id) => {
    const node = document.getElementById(id);
    node.hidden = true;
    node.textContent = "";
  });
}

function showStatus(message) {
  const node = document.getElementById("auth-status");
  node.hidden = false;
  node.textContent = message;
}
