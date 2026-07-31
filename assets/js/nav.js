// NORMAH AGRO FARM — mobile nav toggle. Progressive enhancement only;
// the nav is fully usable (as a static list) with this script absent.
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var mobileNav = document.querySelector(".nav-mobile");
  if (!toggle || !mobileNav) return;

  toggle.addEventListener("click", function () {
    var isOpen = mobileNav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  // Close on Escape, return focus to the toggle.
  mobileNav.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      mobileNav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.focus();
    }
  });
})();
