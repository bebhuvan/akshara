/* Akshara. Plain script, no dependencies. Every page works without it; it only adds conveniences.
   Deciding (folding text, matching) is kept apart from doing (reading and changing the page). */
(function () {
  "use strict";

  /* ---------------- deciding ---------------- */

  /* lower case, accents removed, so "Palas" finds "Pālas" and "Muller" finds "Müller" */
  function fold(s) {
    return String(s).normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/æ/g, "ae").replace(/œ/g, "oe").toLowerCase();
  }
  function tokens(q) { return fold(q).split(/[^a-z0-9]+/).filter(Boolean); }
  function matchesAll(hay, toks) { return toks.every(function (t) { return hay.indexOf(t) !== -1; }); }

  var NUM = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
    "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"];
  var TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];
  function words(n) {
    if (n < 20) return NUM[n];
    if (n < 100) return TENS[Math.floor(n / 10)] + (n % 10 ? "-" + NUM[n % 10] : "");
    return String(n);
  }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  /* ---------------- doing ---------------- */
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* the library: three arrangements rendered by the build; the script chooses one and filters it */
  function library() {
    var box = $("[data-lib-search]");
    if (!box) return;
    box.hidden = false;
    var input = $("#q", box), tally = $("#tally"), empty = $("[data-empty]");
    var order = "shelf";
    var HOW = { shelf: "by shelf", year: "by date of printing", author: "by author" };
    $$("li[data-hay]").forEach(function (li) { li.dataset.fold = fold(li.dataset.hay); });
    var total = $$('[data-order-block="year"] li[data-hay]').length;

    function render() {
      var toks = tokens(input.value), searching = toks.length > 0;
      $$("[data-order-block]").forEach(function (b) { b.hidden = b.dataset.orderBlock !== order; });
      $$("[data-when]").forEach(function (el) { el.hidden = searching || el.dataset.when !== order; });
      var block = $('[data-order-block="' + order + '"]'), n = 0;
      $$(".cat-group", block).forEach(function (g) {
        var shown = 0;
        $$("li[data-hay]", g).forEach(function (li) {
          var ok = !searching || matchesAll(li.dataset.fold, toks);
          li.hidden = !ok;
          li.classList.toggle("open", searching);
          if (ok) shown++;
        });
        var more = $(".more-on", g);
        if (more) more.hidden = searching;
        g.hidden = shown === 0;
        n += shown;
      });
      empty.hidden = n > 0;
      if (!searching) tally.textContent = "All " + words(total) + " editions, " + HOW[order] + ".";
      else if (!n) tally.textContent = "";
      else tally.textContent = cap(words(n)) + (n === 1 ? " book answers" : " books answer") + " to “" + input.value.trim() + "”, " + HOW[order] + ".";
    }
    input.addEventListener("input", render);
    $$("[data-order]", box).forEach(function (btn) {
      btn.addEventListener("click", function () {
        order = btn.dataset.order;
        $$("[data-order]", box).forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
        render();
      });
    });
    var q = new URLSearchParams(location.search).get("q");
    if (q) { input.value = q; render(); }
  }

  library();
})();
