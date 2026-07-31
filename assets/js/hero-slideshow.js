// NORMAH AGRO FARM — hero photo slideshow, crossfades every 10s.
(function () {
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) return;

  var slides = document.querySelectorAll(".hero-photo > img.hero-slide");
  if (slides.length < 2) return;

  var current = 0;
  setInterval(function () {
    var next = (current + 1) % slides.length;
    slides[current].classList.remove("is-active");
    slides[next].classList.add("is-active");
    current = next;
  }, 10000);
})();
