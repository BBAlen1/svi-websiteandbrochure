/* Mobile menu, scroll reveal and header state. The only script on the site. */
(function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");

  // ---- Mobile menu ----
  if (header && toggle && nav) {
    var setOpen = function (open) {
      header.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.querySelector(".nav-toggle__label").textContent = open ? "Đóng" : "Menu";
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && header.classList.contains("nav-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    window.matchMedia("(min-width: 1021px)").addEventListener("change", function (mq) {
      if (mq.matches) setOpen(false);
    });
  }

  // ---- Header shadow once scrolled ----
  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // ---- Scroll reveal (skipped entirely for reduced motion) ----
  if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var groups = [
    ".split-head", ".figures__head", ".figure", ".partner-grid li", ".line-item",
    ".projects__sub", ".feature", ".card-grid > li", ".members__intro", ".members__list li",
    ".page-head .wrap > *", ".model__center", ".model__branches > li", ".line-section__head",
    ".co-card", ".table-wrap", ".footer-grid > div"
  ];
  groups.forEach(function (sel) {
    var parents = new Map();
    document.querySelectorAll(sel).forEach(function (el) {
      var i = parents.get(el.parentNode) || 0;
      parents.set(el.parentNode, i + 1);
      el.setAttribute("data-reveal", "");
      el.style.setProperty("--i", Math.min(i, 8));
    });
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add("is-in");
        io.unobserve(en.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });

  document.querySelectorAll("[data-reveal]").forEach(function (el) { io.observe(el); });
  document.documentElement.classList.add("motion");
})();
