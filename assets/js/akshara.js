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

  /* search results grouped by the book they come from, in the order the books first appear; a result
     that is the book's own page is marked, so it can be named as such */
  function bookOf(url) { var m = /^\/books\/([^/]+)\//.exec(url || ""); return m ? m[1] : ""; }
  function groupByBook(items, perBook) {
    var order = [], by = {};
    items.forEach(function (d) {
      var id = bookOf(d.url);
      if (!id) return;
      var m = d.meta || {};
      if (!by[id]) { by[id] = { id: id, title: m.book || "", author: m.author || "", year: m.year || "", kind: m.kind || "", plate: m.plate || "", shelf: m.shelf || "", hits: [] }; order.push(id); }
      if (by[id].hits.length < perBook) by[id].hits.push({ url: d.url, title: ((d.meta && d.meta.title) || "").replace(/^[\s—–-]+/, ""), excerpt: d.excerpt, own: d.url === "/books/" + id + "/" });
    });
    return order.map(function (id) { return by[id]; });
  }

  /* ---------------- doing ---------------- */
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* a small cover for a result, drawn from what the search index records about the book: its shelf's paper,
     its own plate placed by its kind, or the rule of a type-only cover. Only values the build wrote are used. */
  function smallCover(g) {
    if (!/^[a-z]{2}$/.test(g.shelf) || !/^[a-z]+$/.test(g.kind)) return null;
    var c = document.createElement("div");
    c.className = "cover k-" + g.kind + " " + g.shelf;
    c.dataset.shelf = g.shelf;
    if (g.kind !== "type" && /^\/plates\/[a-z0-9_-]+\.webp$/.test(g.plate)) {
      var pic = document.createElement("div"), plate = document.createElement("i");
      pic.className = "pic"; plate.className = "plate";
      plate.style.setProperty("--src", "url(" + g.plate + ")");
      pic.appendChild(plate); c.appendChild(pic);
    }
    return c;
  }

  /* one result group: the book's cover (when the page has it), its title in its shelf's ink, then each
     place in it where the words occur. Built as text nodes and <mark> elements, never HTML (D7). */
  function renderGroups(list, groups) {
    list.replaceChildren.apply(list, groups.map(function (g) {
      var li = document.createElement("li"), head = document.createElement("a"), title = document.createElement("i");
      var cover = $('.book[href="/books/' + g.id + '/"] .cover') || smallCover(g);
      li.className = "hit" + (/^[a-z]{2}$/.test(g.shelf) ? " " + g.shelf : "");
      if (cover) {
        var thumb = document.createElement("a");
        thumb.className = "hit-cover"; thumb.href = "/books/" + g.id + "/"; thumb.tabIndex = -1; thumb.setAttribute("aria-hidden", "true");
        thumb.appendChild(cover.cloneNode(true));
        if (!/^[a-z]{2}$/.test(g.shelf) && /^[a-z]{2}$/.test(cover.dataset.shelf || "")) li.className = "hit " + cover.dataset.shelf;
        li.appendChild(thumb);
      }
      var body = document.createElement("div"); body.className = "hit-body";
      head.className = "hit-book"; head.href = "/books/" + g.id + "/"; title.textContent = g.title || g.id; head.appendChild(title);
      body.appendChild(head);
      if (g.author || g.year) {
        var by = document.createElement("p"); by.className = "hit-by";
        by.textContent = [g.author, g.year].filter(Boolean).join(", ");
        body.appendChild(by);
      }
      g.hits.forEach(function (h) {
        var a = document.createElement("a"), t = document.createElement("span"), x = document.createElement("span");
        a.className = "hit-place"; a.href = h.url;
        t.className = "t"; t.textContent = h.own ? "The book’s own page" : (h.title || "A chapter");
        x.className = "x"; x.append("…", excerptNodes(h.excerpt), "…");
        a.append(t, x); body.appendChild(a);
      });
      li.appendChild(body);
      return li;
    }));
  }

  /* a search field's Clear: shown once something is written; clearing runs the search again, empty */
  function clearButton(form, input, rerun) {
    var btn = $(".clear", form);
    if (!btn) return function () {};
    function sync() { btn.hidden = !input.value; }
    form.addEventListener("reset", function () { setTimeout(function () { rerun(); sync(); input.focus(); }, 0); });
    return sync;
  }

  /* the library: three arrangements rendered by the build (by shelf, date or author); the script shows
     one, narrows it as the reader types (title, author, year, place), and lists where the words occur in
     the text of the books, from the search index. Results are built as text nodes, never HTML (D7). */
  function library() {
    var form = $("[data-lib-find]");
    if (!form) return;
    var input = $("#find", form), views = $("[data-views]"), count = $("[data-count]");
    var hits = $("[data-hits]"), hitList = $("[data-hits-list]"), hitTally = $("[data-hits-tally]"), hitMore = $("[data-hits-more]");
    var empty = $("[data-empty]"), view = "shelf", seq = 0, pf = null;
    views.hidden = false;
    $$("[data-hay]").forEach(function (a) { a.dataset.fold = fold(a.dataset.hay); });
    var shelfWord = count.textContent;

    function narrow() {
      var toks = tokens(input.value), searching = toks.length > 0, shown = 0;
      $$("[data-view-block]").forEach(function (block) {
        var on = block.dataset.viewBlock === view;
        block.hidden = !on;
        if (!on) return;
        $$(".row", block).forEach(function (row) {
          var n = 0;
          $$("[data-hay]", row).forEach(function (a) {
            var ok = !searching || matchesAll(a.dataset.fold, toks);
            a.hidden = !ok;
            if (ok) n++;
          });
          row.hidden = n === 0;
          var tally = $(".row-h span", row);
          if (tally) {
            if (!tally.dataset.all) tally.dataset.all = tally.textContent;
            tally.textContent = searching ? cap(words(n)) + " of " + tally.dataset.all.toLowerCase() : tally.dataset.all;
          }
          shown += n;
        });
      });
      empty.hidden = !searching || shown > 0;
      if (searching) count.textContent = shown ? cap(words(shown)) + (shown === 1 ? " book" : " books") : "";
      else count.textContent = { shelf: shelfWord, date: "By decade", author: "By surname" }[view];
    }
    function load() { return pf || (pf = import("/pagefind/pagefind.js").then(function (m) { m.options({ excerptLength: 24 }); return m; })); }
    function inText() {
      var q = input.value.trim(), mine = ++seq;
      if (q.length < 3) { hits.hidden = true; hitList.replaceChildren(); return; }
      load().then(function (p) { return p.debouncedSearch(q, {}, 300); }).then(function (res) {
        if (!res || mine !== seq) return;
        var n = res.results.length;
        if (!n) { hits.hidden = true; return; }
        return Promise.all(res.results.slice(0, 24).map(function (r) { return r.data(); })).then(function (items) {
          if (mine !== seq) return;
          var groups = groupByBook(items, 2).slice(0, 5);
          hitTally.textContent = (n === 1 ? "One page" : n + " pages") + ", the best below";
          hitMore.href = "/search/?q=" + encodeURIComponent(q);
          renderGroups(hitList, groups);
          hits.hidden = groups.length === 0;
        });
      }).catch(function () { hits.hidden = true; });
    }
    var syncClear = clearButton(form, input, function () { narrow(); inText(); });
    input.addEventListener("input", function () { narrow(); inText(); syncClear(); });
    form.addEventListener("submit", function (e) { e.preventDefault(); input.blur(); });
    $$("[data-view]", views).forEach(function (btn) {
      btn.addEventListener("click", function () {
        view = btn.dataset.view;
        $$("[data-view]", views).forEach(function (o) { o.setAttribute("aria-pressed", String(o === btn)); });
        narrow();
      });
    });
    var q = new URLSearchParams(location.search).get("q");
    if (q) { input.value = q; narrow(); inText(); syncClear(); }
  }

  /* settings kept on this device; storage may be unavailable (private windows), and the page works without it */
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* unavailable: nothing is kept */ } }
  };

  /* the reading room */
  function reading() {
    var read = $("#read");
    if (!read) return;
    var body = document.body, panel = $("#rpanel"), scrim = $("#rp-scrim");
    $$("[data-needs-js]").forEach(function (el) { el.hidden = false; });

    /* "[p. 12]" in the margin reads better as "12" */
    $$(".folio-trigger").forEach(function (b) {
      b.textContent = b.dataset.folio || b.textContent.replace(/^\[p\.\s*|\]$/g, "");
      b.setAttribute("aria-expanded", "false");
    });

    var DEFAULTS = { lh: "normal", width: "medium", notes: "margin", para: "indented", align: "ragged", folios: "shown" };
    function apply() {
      Object.keys(DEFAULTS).forEach(function (k) { read.dataset[k] = store.get("ak-" + k) || DEFAULTS[k]; });
      if (window.akPaper) window.akPaper();
      var sz = Math.max(0, Math.min(5, parseInt(store.get("ak-size") || "2", 10)));
      read.style.setProperty("--rs", String(1 + (sz - 2) * 0.075));
      $$("[data-sz]", panel).forEach(function (b) { b.setAttribute("aria-pressed", String(+b.dataset.sz === sz)); });
      $$("[data-set]", panel).forEach(function (b) {
        var now = b.dataset.set === "paper" ? document.documentElement.dataset.paper : read.dataset[b.dataset.set];
        b.setAttribute("aria-pressed", String(now === b.dataset.val));
      });
    }
    function size(step) {
      var sz = Math.max(0, Math.min(5, parseInt(store.get("ak-size") || "2", 10) + step));
      store.set("ak-size", String(sz)); apply();
    }
    $$("[data-sz]", panel).forEach(function (b) { b.addEventListener("click", function () { store.set("ak-size", b.dataset.sz); apply(); }); });
    $$("[data-set]", panel).forEach(function (b) { b.addEventListener("click", function () { store.set("ak-" + b.dataset.set, b.dataset.val); apply(); }); });
    apply();

    /* the panel */
    var opener = null;
    function tab(id) {
      $$(".rp-tabs [data-tab]", panel).forEach(function (t) { t.setAttribute("aria-selected", String(t.dataset.tab === id)); });
      $$(".rp-sec", panel).forEach(function (s) { s.hidden = s.id !== id; });
    }
    /* everything on the page but the panel, made inert while the panel is open so Tab stays inside it */
    function behindPanel() { return $$("body > *").concat($$("#read > *")).filter(function (el) { return el !== read && el !== panel && !el.contains(panel); }); }
    function openPanel(id, from) {
      opener = from || document.activeElement;
      tab(id);
      panel.classList.add("open"); panel.setAttribute("aria-hidden", "false"); scrim.hidden = false;
      behindPanel().forEach(function (el) { el.inert = true; });
      $$("[data-open]").forEach(function (b) { b.setAttribute("aria-expanded", "true"); });
      panel.focus();
      var cur = $('#rtoc a[aria-current]', panel); if (id === "rp-contents" && cur) cur.scrollIntoView({ block: "center" });
    }
    function closePanel() {
      if (!panel.classList.contains("open")) return;
      panel.classList.remove("open"); panel.setAttribute("aria-hidden", "true"); scrim.hidden = true;
      behindPanel().forEach(function (el) { el.inert = false; });
      $$("[data-open]").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
      if (opener) opener.focus({ preventScroll: true });
    }
    $$("[data-open]").forEach(function (b) {
      b.addEventListener("click", function (e) { e.preventDefault(); openPanel(b.dataset.open, b); });
    });
    $$(".rp-tabs [data-tab]", panel).forEach(function (t) { t.addEventListener("click", function () { tab(t.dataset.tab); }); });
    $("#rp-close").addEventListener("click", closePanel);
    scrim.addEventListener("click", closePanel);

    /* focus: nothing but the text */
    var focusBtn = $("#rb-focus");
    function focusMode(on) { body.classList.toggle("focus", on); focusBtn.setAttribute("aria-pressed", String(on)); }
    focusBtn.addEventListener("click", function () { focusMode(!body.classList.contains("focus")); });

    /* the scan leaf: a printed page number opens the camera's photograph of that page */
    var leaf = $("#leaf"), leafImg = $("#leaf-img"), leafNo = $("#leaf-no"), leafFrom = null;
    function closeLeaf() {
      if (!leaf.classList.contains("open")) return;
      leaf.classList.remove("open"); leaf.setAttribute("aria-hidden", "true"); body.classList.remove("leaf-open");
      $$(".folio-trigger[aria-expanded='true']").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
      if (leafFrom) leafFrom.focus({ preventScroll: true });
    }
    $$(".folio-trigger").forEach(function (b) {
      b.addEventListener("click", function () {
        var src = b.dataset.scan;
        if (!src || !/^https:\/\/archive\.org\//.test(src)) return;
        if (b.getAttribute("aria-expanded") === "true") { closeLeaf(); return; }
        $$(".folio-trigger[aria-expanded='true']").forEach(function (x) { x.setAttribute("aria-expanded", "false"); });
        leafFrom = b;
        var img = document.createElement("img");
        img.src = src; img.alt = "Photograph of printed page " + (b.dataset.folio || "");
        img.decoding = "async";
        leafImg.replaceChildren(img);
        leafNo.textContent = b.dataset.folio || "";
        b.setAttribute("aria-expanded", "true");
        leaf.classList.add("open"); leaf.setAttribute("aria-hidden", "false"); body.classList.add("leaf-open");
        $("#leaf-close").focus({ preventScroll: true });
      });
    });
    $("#leaf-close").addEventListener("click", closeLeaf);

    /* find in this book: the search index, filtered to this book; results are built as text, never HTML */
    var rfind = $("#rfind"), rout = $("#rfind-out"), rtally = $("#rfind-tally"), rtoc = $("#rtoc"), rseq = 0, rpf = null;
    function rload() { return rpf || (rpf = import("/pagefind/pagefind.js").then(function (m) { m.options({ excerptLength: 22 }); return m; })); }
    function findRun() {
      var q = rfind.value.trim(), mine = ++rseq;
      if (!q) { rout.hidden = true; rout.replaceChildren(); rtally.textContent = ""; rtoc.hidden = false; return; }
      rload().then(function (p) { return p.debouncedSearch(q, { filters: { book: read.dataset.book } }, 250); }).then(function (res) {
        if (!res || mine !== rseq) return;
        return Promise.all(res.results.slice(0, 40).map(function (r) { return r.data(); })).then(function (items) {
          if (mine !== rseq) return;
          rtoc.hidden = true; rout.hidden = false;
          rtally.textContent = items.length ? (res.results.length === 1 ? "One chapter" : res.results.length + " chapters") + " answer to “" + q + "”." :
            "Nothing answers to that. Old books spell differently: try another spelling, or part of the word.";
          rout.replaceChildren.apply(rout, items.map(function (d) {
            var li = document.createElement("li"), a = document.createElement("a"), t = document.createElement("span"), x = document.createElement("span");
            a.href = d.url + (d.url.indexOf("?") < 0 ? "?" : "&") + "find=" + encodeURIComponent(q);
            t.className = "rf-t"; t.textContent = (d.meta && d.meta.title) || d.url;
            x.className = "rf-x"; x.appendChild(excerptNodes(d.excerpt));
            a.append(t, x); li.appendChild(a); return li;
          }));
        });
      }).catch(function () { rtally.textContent = "Find could not be loaded; the contents are below."; rtoc.hidden = false; });
    }
    rfind.addEventListener("input", findRun);

    /* arriving from a find: mark the word in the text and bring its first place to the middle of the screen */
    var found = new URLSearchParams(location.search).get("find");
    if (found) { try { markFound(found); } catch (e) { /* never let finding break the reading room */ } }
    function markFound(q) {
      var want = fold(q.trim()), text = $("#chapter-text"), ranges = [];
      if (!want) return;
      var walk = document.createTreeWalker(text, NodeFilter.SHOW_TEXT, null), node;
      while ((node = walk.nextNode()) && ranges.length < 200) {
        if (node.parentElement.closest("button, .apparatus-zone")) continue;
        var hay = fold(node.nodeValue), at = 0, i;
        if (hay.length !== node.nodeValue.length) continue;
        while ((i = hay.indexOf(want, at)) !== -1) { var r = document.createRange(); r.setStart(node, i); r.setEnd(node, i + want.length); ranges.push(r); at = i + want.length; }
      }
      if (!ranges.length) return;
      try {
        if (window.CSS && CSS.highlights && window.Highlight) {
          var hl = new Highlight();
          ranges.forEach(function (r) { hl.add(r); });
          CSS.highlights.set("find", hl);
        }
      } catch (e) { /* marking is a nicety; the passage is still brought into view */ }
      ranges[0].startContainer.parentElement.scrollIntoView({ block: "center" });
    }

    /* keys */
    document.addEventListener("keydown", function (e) {
      if (e.target.closest("input, textarea, select") || e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === "/") { e.preventDefault(); openPanel("rp-contents"); rfind.focus(); return; }
      if (e.key === "Escape") { closePanel(); closeLeaf(); if (body.classList.contains("focus")) focusMode(false); }
      else if (e.key === "m" || e.key === "M") { panel.classList.contains("open") ? closePanel() : openPanel("rp-settings"); }
      else if (e.key === "f" || e.key === "F") focusMode(!body.classList.contains("focus"));
      else if (e.key === "+" || e.key === "=") size(1);
      else if (e.key === "-" || e.key === "−") size(-1);
    });

    /* how far through the chapter: a hairline under the bar */
    var prog = $("#rb-prog"), text = $("#chapter-text"), ticking = false;
    function progress() {
      ticking = false;
      var r = text.getBoundingClientRect(), span = r.height - window.innerHeight * 0.6;
      var f = span > 0 ? Math.max(0, Math.min(1, -r.top / span)) : 1;
      prog.style.setProperty("--p", f.toFixed(4));
    }
    /* the bar slides away while reading down and comes back on the first move up */
    var bar = $("#rbar"), lastY = window.scrollY;
    function barPlace() {
      var y = window.scrollY, dy = y - lastY;
      if (y < 80 || panel.classList.contains("open")) bar.classList.remove("rbar-away");
      else if (dy > 6) bar.classList.add("rbar-away");
      else if (dy < -6) bar.classList.remove("rbar-away");
      if (Math.abs(dy) > 6) lastY = y;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(function () { progress(); barPlace(); }); }
    }, { passive: true });
    progress();
  }


  /* search: the Pagefind index made after the build (static, on this site, nothing third-party).
     Excerpts come back as escaped text with <mark> around the found words; they are rebuilt as text
     nodes and <mark> elements, never inserted as HTML. */
  function excerptNodes(excerpt) {
    var frag = document.createDocumentFragment(), parts = String(excerpt).split(/<\/?mark>/);
    var dec = document.createElement("textarea");
    parts.forEach(function (part, i) {
      dec.innerHTML = part.replace(/</g, "&lt;");
      var text = document.createTextNode(dec.value);
      if (i % 2) { var m = document.createElement("mark"); m.appendChild(text); frag.appendChild(m); } else frag.appendChild(text);
    });
    return frag;
  }
  function search() {
    var form = $("[data-search]");
    if (!form) return;
    var input = $("#sq", form), out = $("#s-results"), tally = $("#s-tally"), ways = $("#s-ways"), pf = null, seq = 0;
    function load() { return pf || (pf = import("/pagefind/pagefind.js").then(function (m) { m.options({ excerptLength: 30 }); return m; })); }
    function run() {
      var q = input.value.trim(), mine = ++seq;
      history.replaceState(null, "", q ? "?q=" + encodeURIComponent(q) : location.pathname);
      if (!q) { out.replaceChildren(); tally.textContent = ""; ways.hidden = false; moreBtn.hidden = true; return; }
      ways.hidden = true;
      load().then(function (p) { return p.debouncedSearch(q, {}, 250); }).then(function (res) {
        if (!res || mine !== seq) return;
        var n = res.results.length;
        tally.textContent = n ? (n === 1 ? "One page" : n + " pages") + " answer to “" + q + "”." : "Nothing answers to “" + q + "”. Try another spelling, or a shorter word.";
        shown = 0; all = res.results;
        return more(mine);
      }).catch(function () {
        tally.textContent = "Search could not be loaded. The catalogue in the library lists every book.";
      });
    }
    var all = [], shown = 0, items = [], moreBtn = $("#s-more");
    var fetching = false;
    function more(mine) {
      if (fetching) return Promise.resolve();
      fetching = true; moreBtn.disabled = true;
      var next = all.slice(shown, shown + 60);
      return Promise.all(next.map(function (r) { return r.data(); })).then(function (got) {
          if (mine !== seq) return;
          if (shown === 0) items = [];
          shown += got.length; items = items.concat(got);
          moreBtn.hidden = shown >= all.length;
          moreBtn.textContent = "Show more, from " + (all.length - shown) + " further pages";
          renderGroups(out, groupByBook(items, 4));
      }).then(function () { fetching = false; moreBtn.disabled = false; }, function () { fetching = false; moreBtn.disabled = false; });
    }
    moreBtn.addEventListener("click", function () { more(seq); });
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
    var syncClear = clearButton(form, input, run);
    input.addEventListener("input", function () { run(); syncClear(); });
    var q = new URLSearchParams(location.search).get("q");
    if (q) { input.value = q; run(); syncClear(); }
  }

  /* the opening: the plate turns slowly, each engraving on its own shelf's paper. Nothing moves for a
     reader who has asked for less motion. Captions are built as text nodes; *words* are set in italic. */
  function captionNodes(line) {
    var frag = document.createDocumentFragment();
    String(line).split("*").forEach(function (part, i) {
      if (!part) return;
      if (i % 2) { var it = document.createElement("i"); it.textContent = part; frag.appendChild(it); }
      else frag.appendChild(document.createTextNode(part));
    });
    return frag;
  }
  function turning() {
    var stage = $("#stage");
    if (!stage || !stage.dataset.turn) return;
    if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var plates;
    try { plates = JSON.parse(stage.dataset.turn); } catch (e) { return; }
    if (!Array.isArray(plates) || plates.length < 2) return;
    var faces = $$(".art .plate", stage), a = faces[0], b = faces[1], i = 0, base = stage.className.split(" ")[0];
    var capT = $('[data-cap="t"]', stage), capS = $('[data-cap="s"]', stage), capN = $('[data-cap="n"]', stage);
    /* only the next plate is fetched, a little before it is needed, so the opening page stays light */
    function fetchNext() { var im = new Image(); im.src = plates[(i + 1) % plates.length].src; }
    setTimeout(fetchNext, 3000);
    /* the reader can stop it (WCAG 2.2.2): Pause holds the plate that is showing */
    var paused = false, pause = $("[data-turn-pause]", stage);
    if (pause) {
      pause.hidden = false;
      pause.addEventListener("click", function () {
        paused = !paused;
        pause.setAttribute("aria-pressed", String(paused));
        pause.textContent = paused ? "Play" : "Pause";
      });
    }
    setInterval(function () {
      if (document.hidden || paused) return;
      i = (i + 1) % plates.length; var p = plates[i];
      if (!/^\/plates\/[a-z0-9_-]+\.webp$/.test(p.src) || !/^[a-z]{2}$/.test(p.code)) return;
      setTimeout(fetchNext, 2500);
      b.style.setProperty("--src", "url(" + p.src + ")");
      b.setAttribute("role", "img"); b.setAttribute("aria-label", p.alt || ""); b.removeAttribute("aria-hidden");
      a.removeAttribute("role"); a.removeAttribute("aria-label"); a.setAttribute("aria-hidden", "true");
      stage.className = base + " " + p.code;
      b.classList.remove("off"); a.classList.add("off");
      var t = a; a = b; b = t;
      capT.textContent = p.title;
      capT.classList.toggle("sp", p.sp === true);
      capS.replaceChildren(captionNodes(p.line));
      capN.textContent = (i + 1) + " of " + plates.length;
    }, 6500);
  }

  turning();
  library();
  reading();
  search();
})();
