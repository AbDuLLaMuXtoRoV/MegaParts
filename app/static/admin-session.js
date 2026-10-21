// Shared by admin pages: send an expired session back to the login page and wire "Log out".
(() => {
  const toLogin = () => location.replace(`/admin/login?next=${encodeURIComponent(location.pathname)}`);
  const nativeFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const response = await nativeFetch(...args);
    if (response.status === 401) toLogin();
    return response;
  };
  document.addEventListener("click", async (event) => {
    if (!event.target.closest("[data-logout]")) return;
    await nativeFetch("/api/admin/logout", { method: "POST" });
    location.replace("/admin/login");
  });
})();
