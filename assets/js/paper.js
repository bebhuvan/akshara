/* Akshara: which paper to print on and which type to read in, decided before the page is drawn, so the page never
flashes white and a reader who chose Clear or Plain never downloads the Book face first.
   The reader's paper (Day, Cotton, Night) is kept on this device; with none, or with Auto, the page follows
   the device's light or dark setting, and changes with it. Sets <html data-paper>, <html data-theme> and, on every
   page, <html data-type> (book, clear or plain; only the reading pages use it). */
(function () {
  "use strict";
  var root = document.documentElement;
  var dark = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  function kept(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function apply() {
    var paper = kept("ak-paper") || "auto", type = kept("ak-type") || "book";
    if (["day", "cotton", "night", "auto"].indexOf(paper) < 0) paper = "auto";
    root.dataset.paper = paper;
    root.dataset.theme = paper === "night" || (paper === "auto" && dark && dark.matches) ? "dark" : "light";
    root.dataset.type = ["book", "clear", "plain"].indexOf(type) < 0 ? "book" : type;
  }
  apply();
  if (dark && dark.addEventListener) dark.addEventListener("change", apply);
  window.akPaper = apply;
})();
