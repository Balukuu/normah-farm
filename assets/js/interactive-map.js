// NORMAH AGRO FARM — Interactive Corridor Map Network.
(function () {
  var mapContainer = document.querySelector(".corridor-figure");
  if (!mapContainer) return;

  var dests = mapContainer.querySelectorAll(".destinations .dest");
  dests.forEach(function (dest) {
    dest.addEventListener("mouseenter", function () {
      dest.style.borderColor = "var(--seed)";
      dest.style.color = "var(--seed)";
    });
    dest.addEventListener("mouseleave", function () {
      dest.style.borderColor = "";
      dest.style.color = "";
    });
  });
})();
