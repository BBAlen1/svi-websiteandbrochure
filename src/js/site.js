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

  // ---- Review switcher: on phones the current number toggles the full set ----
  var vs = document.querySelector(".variant-switch");
  if (vs) {
    var cur = vs.querySelector('[aria-current="page"]');
    cur.addEventListener("click", function (e) {
      if (!window.matchMedia("(max-width: 640px)").matches) return;
      e.preventDefault();
      vs.classList.toggle("is-open");
    });
    document.addEventListener("click", function (e) { if (!vs.contains(e.target)) vs.classList.remove("is-open"); });
  }

  // ---- Header shadow once scrolled ----
  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // ---- Project map (Direction B): pins and region list highlight each other ----
  var pins = document.querySelectorAll(".vn-map .pin");
  if (pins.length) {
    var regionEls = document.querySelectorAll(".pin[data-region], .b-region[data-region]");
    var activate = function (id) {
      regionEls.forEach(function (el) { el.classList.toggle("is-active", el.getAttribute("data-region") === id); });
    };
    regionEls.forEach(function (el) {
      var id = el.getAttribute("data-region");
      el.addEventListener("mouseenter", function () { activate(id); });
      el.addEventListener("focusin", function () { activate(id); });
    });
    pins.forEach(function (pin) {
      var go = function () {
        var id = pin.getAttribute("data-region");
        activate(id);
        var target = document.querySelector('.b-region[data-region="' + id + '"]');
        if (target && window.matchMedia("(max-width: 900px)").matches) target.scrollIntoView({ behavior: "smooth", block: "center" });
      };
      pin.addEventListener("click", go);
      pin.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
    });
    document.querySelectorAll(".b-region a[href^='#p-']").forEach(function (a) {
      a.addEventListener("click", function () {
        var card = document.querySelector(a.getAttribute("href"));
        if (!card) return;
        card.classList.add("is-target");
        setTimeout(function () { card.classList.remove("is-target"); }, 2200);
      });
    });
  }

  // ---- Live figures hero: rotate facts and count each one up ----
  var figs = document.querySelectorAll(".fig__i");
  if (figs.length) {
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var fmt = function (v, dec) {
      var s = v.toFixed(dec).split(".");
      s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
      return s.join(",");
    };
    var show = function (i) {
      figs.forEach(function (f, j) { f.classList.toggle("is-on", i === j); });
      var el = figs[i], out = el.querySelector(".fig__v");
      var target = parseFloat(el.getAttribute("data-value")), dec = +el.getAttribute("data-dec");
      if (reduce) { out.textContent = fmt(target, dec); return; }
      var t0 = null;
      var step = function (ts) {
        if (!t0) t0 = ts;
        var p = Math.min(1, (ts - t0) / 1600), e = 1 - Math.pow(1 - p, 3);
        out.textContent = fmt(target * e, dec);
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    var cur = 0;
    show(0);
    if (!reduce) setInterval(function () { cur = (cur + 1) % figs.length; show(cur); }, 5200);
  }

  // ---- Direction C: scroll-linked effects (motto lights up, hero image expands) ----
  var motto = document.querySelector(".c-motto__q");
  var expand = document.querySelector("[data-expand]");
  if ((motto || expand) && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var ticking = false;
    var update = function () {
      ticking = false;
      var vh = window.innerHeight;
      if (motto) {
        var r = motto.getBoundingClientRect();
        var p = (vh * 0.85 - r.top) / (r.height + vh * 0.35);
        motto.style.setProperty("--p", Math.max(0, Math.min(1, p)).toFixed(3));
      }
      if (expand) {
        var e = expand.getBoundingClientRect();
        var s = (vh - e.top) / (vh * 0.9);
        expand.style.setProperty("--s", Math.max(0, Math.min(1, s - 0.35)).toFixed(3));
      }
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  // ---- Filter chips (Direction A projects) ----
  document.querySelectorAll("[data-filter-for]").forEach(function (group) {
    var list = document.getElementById(group.getAttribute("data-filter-for"));
    if (!list) return;
    group.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-filter]");
      if (!btn) return;
      var f = btn.getAttribute("data-filter");
      group.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
      list.querySelectorAll("[data-region]").forEach(function (li) {
        li.classList.toggle("is-out", f !== "all" && li.getAttribute("data-region") !== f);
      });
    });
  });

  // ---- Scroll reveal (skipped entirely for reduced motion) ----
  if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var groups = [
    ".split-head", ".figures__head", ".figure", ".partner-grid li", ".line-item",
    ".projects__sub", ".feature", ".card-grid > li", ".lc", ".vals li", ".vision__q", ".mc li", ".chips", ".members__intro", ".members__list li",
    ".page-head .wrap > *", ".model__center", ".model__branches > li", ".line-section__head",
    ".co-card", ".table-wrap", ".footer-grid > div", ".rv"
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
