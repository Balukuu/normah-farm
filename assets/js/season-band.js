// NORMAH AGRO FARM — Season Band with Tooltips & Dynamic Progress.
(function () {
  var YEAR_START = new Date(new Date().getFullYear(), 0, 1).getTime();
  var YEAR_MS = 365 * 24 * 60 * 60 * 1000;

  var CROP_SPECS = {
    "Maize": "Season A & B · 13.5% Moisture · Feed/Food Grade",
    "Soya beans": "Season A & B · 12.0% Moisture · Oilseed/Feed",
    "Millet": "Season A · 12.5% Moisture · Cereal Grain",
    "Sorghum": "Season A & B · 13.0% Moisture · Drought Tolerant",
    "Rice": "Season B · 13.0% Moisture · Borehole Irrigated",
    "Sesame": "Season B · 7.0% Moisture · Premium Export Spec"
  };

  function yearProgressPercent() {
    var now = Date.now();
    var pct = ((now - YEAR_START) / YEAR_MS) * 100;
    return Math.max(0, Math.min(100, pct));
  }

  function applyProgress(band, pct) {
    var progressEl = band.querySelector(".progress");
    if (progressEl) progressEl.style.width = pct + "%";

    var todayLine = band.querySelector(".today-line");
    if (!todayLine) {
      todayLine = document.createElement("div");
      todayLine.className = "today-line";
      todayLine.setAttribute("aria-hidden", "true");
      var chipsRef = band.querySelector(".chips");
      band.insertBefore(todayLine, chipsRef || null);
    }
    todayLine.style.left = pct + "%";

    var chips = band.querySelectorAll(".chip");
    chips.forEach(function (chip) {
      var pos = Number(chip.getAttribute("data-pos") || 0);
      chip.style.left = pos + "%";
      chip.classList.toggle("is-lit", pos <= pct);

      // Add tooltip if missing
      var cropName = chip.textContent.trim();
      if (!chip.querySelector(".season-chip-tooltip") && CROP_SPECS[cropName]) {
        var tooltip = document.createElement("span");
        tooltip.className = "season-chip-tooltip";
        tooltip.textContent = CROP_SPECS[cropName];
        chip.appendChild(tooltip);
      }
    });
  }

  var bands = document.querySelectorAll(".season-band");
  var todayPct = yearProgressPercent();
  bands.forEach(function (band) {
    applyProgress(band, todayPct);
  });
})();
