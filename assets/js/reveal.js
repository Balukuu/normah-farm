// NORMAH AGRO FARM — scroll-triggered reveal, stat counter, and header scroll effects.
(function () {
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Header scroll shadow detector
  var header = document.querySelector(".site-header");
  if (header) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 20) {
        header.classList.add("is-scrolled");
      } else {
        header.classList.remove("is-scrolled");
      }
    }, { passive: true });
  }

  // Stat Counter Count-up Animation
  function animateCounter(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var suffix = el.getAttribute("data-suffix") || "";
    var prefix = el.getAttribute("data-prefix") || "";
    if (isNaN(target)) return;

    var start = 0;
    var duration = 1200;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var current = Math.floor(progress * (target - start) + start);
      el.textContent = prefix + current.toLocaleString() + suffix;
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        el.textContent = prefix + target.toLocaleString() + suffix;
      }
    }
    window.requestAnimationFrame(step);
  }

  var targets = document.querySelectorAll(".reveal, [data-count]");
  if (!targets.length) return;

  if (reduceMotion || !("IntersectionObserver" in window)) {
    targets.forEach(function (el) {
      el.classList.add("is-visible");
      if (el.hasAttribute("data-count")) {
        var target = el.getAttribute("data-count");
        var suffix = el.getAttribute("data-suffix") || "";
        var prefix = el.getAttribute("data-prefix") || "";
        el.textContent = prefix + target + suffix;
      }
    });
    return;
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var delay = el.hasAttribute("data-reveal-delay") ? Number(el.getAttribute("data-reveal-delay")) : 0;
          setTimeout(function () {
            el.classList.add("is-visible");
            if (el.hasAttribute("data-count") && !el.dataset.animated) {
              el.dataset.animated = "true";
              animateCounter(el);
            }
          }, delay);
          observer.unobserve(el);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -5% 0px" }
  );

  targets.forEach(function (el) { observer.observe(el); });
})();
