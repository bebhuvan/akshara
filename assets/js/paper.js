/* Akshara: which paper to print on, decided before the page is drawn so it never flashes white.
   The reader's choice (Day, Cotton, Night) is kept on this device; with none, or with Auto, the page follows
   the device's light or dark setting, and changes with it. Sets <html data-paper> and <html data-theme>. */
(function () {
  "use strict";
  var root = document.documentElement;
  var dark = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  function chosen() { try { return window.localStorage.getItem("ak-paper"); } catch (e) { return null; } }
  function apply() {
    var paper = chosen() || "auto";
    if (["day", "cotton", "night", "auto"].indexOf(paper) < 0) paper = "auto";
    root.dataset.paper = paper;
    root.dataset.theme = paper === "night" || (paper === "auto" && dark && dark.matches) ? "dark" : "light";
  }
  apply();
  if (dark && dark.addEventListener) dark.addEventListener("change", apply);
  window.akPaper = apply;
})();
