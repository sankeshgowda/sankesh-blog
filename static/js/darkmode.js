(function () {
  const root = document.documentElement;
  const saved = localStorage.getItem("sankesh-theme");
  if (saved) root.dataset.theme = saved;

  document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("themeToggle");
    if (!toggle) return;
    toggle.addEventListener("click", () => {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      localStorage.setItem("sankesh-theme", next);
    });
  });
})();
