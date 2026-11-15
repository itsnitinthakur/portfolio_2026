// portfolio/static/portfolio/js/site.js
// Mobile menu: toggles the panel, keeps aria-expanded in sync, closes on
// Escape, on link click, and when the window grows to desktop width.
(function () {
  "use strict";

  var toggle = document.querySelector("[data-menu-toggle]");
  var menu = document.querySelector("[data-menu]");
  if (!toggle || !menu) return;

  var label = toggle.querySelector("[data-menu-label]");
  var iconOpen = toggle.querySelector("[data-icon-open]");
  var iconClose = toggle.querySelector("[data-icon-close]");

  function setOpen(open) {
    menu.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
    if (label) label.textContent = open ? "Close menu" : "Open menu";
    if (iconOpen) iconOpen.classList.toggle("hidden", open);
    if (iconClose) iconClose.classList.toggle("hidden", !open);
  }

  toggle.addEventListener("click", function () {
    setOpen(menu.hidden);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !menu.hidden) {
      setOpen(false);
      toggle.focus();
    }
  });

  menu.addEventListener("click", function (event) {
    if (event.target.closest("a")) setOpen(false);
  });

  var desktop = window.matchMedia("(min-width: 768px)");
  var onChange = function (e) { if (e.matches) setOpen(false); };
  if (desktop.addEventListener) desktop.addEventListener("change", onChange);
  else if (desktop.addListener) desktop.addListener(onChange);
})();
