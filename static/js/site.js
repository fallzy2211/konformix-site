(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // -------------------------------------------------------------------------
  // Menu mobile
  // -------------------------------------------------------------------------
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (toggle && nav) {
    var mq = window.matchMedia("(max-width: 900px)");

    function applyNav() {
      if (mq.matches) {
        nav.hidden = toggle.getAttribute("aria-expanded") !== "true";
      } else {
        nav.hidden = false;
        toggle.setAttribute("aria-expanded", "false");
      }
    }

    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      applyNav();
    });

    mq.addEventListener("change", applyNav);
    applyNav();

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        toggle.setAttribute("aria-expanded", "false");
        applyNav();
        toggle.focus();
      }
    });
  }

  // -------------------------------------------------------------------------
  // Pré-remplissage du formulaire depuis ?interet=
  // -------------------------------------------------------------------------
  var interest = new URLSearchParams(window.location.search).get("interet");
  var select = document.getElementById("id_interest");
  if (interest && select && ["kontrol", "vigil", "both", "other"].indexOf(interest) !== -1) {
    select.value = interest;
  }

  // -------------------------------------------------------------------------
  // Animations — n'activer que si le navigateur suit et que l'utilisateur
  // n'a pas demandé de réduire les animations. Sans cette classe, tout le
  // contenu reste visible et les valeurs finales sont déjà dans le HTML.
  // -------------------------------------------------------------------------
  if (reduce || !("IntersectionObserver" in window)) return;
  document.documentElement.classList.add("js-anim");

  // Compteurs -----------------------------------------------------------------
  function formatNumber(n, sep) {
    var s = String(n);
    if (!sep) return s;
    return s.replace(/\B(?=(\d{3})+(?!\d))/g, " "); // espace insécable
  }

  function countUp(el) {
    // Un compteur peut etre atteint deux fois : par son parent .reveal et par
    // sa propre observation. Ce drapeau garantit une seule animation.
    if (el.dataset.counted === "1") return;
    el.dataset.counted = "1";

    var target = parseFloat(el.dataset.count);
    if (isNaN(target)) return;
    var suffix = el.dataset.suffix || "";
    var sep = el.dataset.sep === "1";
    var duration = 1100;
    var start = null;

    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      // easing outCubic : rapide au début, s'arrête net sur la valeur exacte
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = formatNumber(Math.round(target * eased), sep) + suffix;
      if (p < 1) requestAnimationFrame(frame);
    }

    el.textContent = formatNumber(0, sep) + suffix;
    requestAnimationFrame(frame);
  }

  // Observateur commun --------------------------------------------------------
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      el.classList.add("is-in");
      el.querySelectorAll("[data-count]").forEach(countUp);
      if (el.hasAttribute("data-count")) countUp(el);
      observer.unobserve(el);
    });
  }, { threshold: 0.2, rootMargin: "0px 0px -40px 0px" });

  document.querySelectorAll(".reveal, .chart, [data-count]").forEach(function (el) {
    observer.observe(el);
  });

  // -------------------------------------------------------------------------
  // Infobulle du graphique
  // -------------------------------------------------------------------------
  document.querySelectorAll(".chart-wrap").forEach(function (wrap) {
    var svg = wrap.querySelector(".chart");
    var tip = wrap.querySelector(".tip");
    if (!svg || !tip) return;

    function show(hit) {
      var pt = svg.createSVGPoint();
      pt.x = parseFloat(hit.dataset.cx);
      pt.y = parseFloat(hit.dataset.cy);
      var screen = pt.matrixTransform(svg.getScreenCTM());
      var box = wrap.getBoundingClientRect();
      tip.innerHTML =
        "<b>" + hit.dataset.year + "</b>" +
        hit.dataset.cat + " : " + hit.dataset.val;
      var top = screen.y - box.top;
      tip.style.left = (screen.x - box.left + wrap.scrollLeft) + "px";
      tip.style.top = top + "px";
      // Une barre qui touche le haut du cadre n'a pas la place au-dessus.
      tip.classList.toggle("tip--below", top < 46);
      tip.classList.add("on");
    }

    function hide() { tip.classList.remove("on"); }

    svg.querySelectorAll(".bar-hit").forEach(function (hit) {
      hit.addEventListener("mouseenter", function () { show(hit); });
      hit.addEventListener("focus", function () { show(hit); });
      hit.addEventListener("mouseleave", hide);
      hit.addEventListener("blur", hide);
    });
    wrap.addEventListener("mouseleave", hide);
  });
})();
