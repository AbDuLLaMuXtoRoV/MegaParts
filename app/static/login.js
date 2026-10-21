const loginForm = document.querySelector("#login-form");
const loginError = document.querySelector("#login-error");
const loginSubmit = document.querySelector("#login-submit");

// Only return to an admin page on this site; anything else could be an open redirect.
const safeNext = (value) => (value && /^\/admin(\/[\w\-/]*)?$/.test(value) ? value : null);

const showError = (message) => {
  loginError.textContent = message;
  loginError.hidden = false;
};

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const username = loginForm.username.value.trim();
  const password = loginForm.password.value;
  if (!username || !password) { showError("Enter your username and password."); return; }
  loginError.hidden = true;
  loginSubmit.disabled = true;
  loginSubmit.textContent = "Signing in…";
  try {
    const response = await fetch("/api/admin/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      showError(typeof data.detail === "string" ? data.detail : "Sign-in failed. Try again.");
      loginForm.password.select();
      return;
    }
    location.replace(safeNext(new URLSearchParams(location.search).get("next")) || data.next);
  } catch {
    showError("The server could not be reached.");
  } finally {
    loginSubmit.disabled = false;
    loginSubmit.textContent = "Sign in";
  }
});

loginForm.username.focus();
