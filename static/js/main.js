window.addEventListener("load", () => {
  document.getElementById("loader")?.classList.add("hidden");
});

document.addEventListener("DOMContentLoaded", () => {
  const scrollTop = document.getElementById("scrollTop");
  window.addEventListener("scroll", () => {
    scrollTop?.classList.toggle("visible", window.scrollY > 480);
  });
  scrollTop?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  const chartEl = document.getElementById("viewsChart");
  if (chartEl && window.Chart) {
    const labels = chartEl.dataset.labels ? chartEl.dataset.labels.split(",") : [];
    const values = chartEl.dataset.values ? chartEl.dataset.values.split(",").map(Number) : [];
    new Chart(chartEl, {
      type: "line",
      data: {
        labels,
        datasets: [{
          label: "Views",
          data: values,
          borderColor: "#06B6D4",
          backgroundColor: "rgba(6, 182, 212, 0.18)",
          tension: 0.35,
          fill: true
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      }
    });
  }
});
