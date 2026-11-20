// Akshara Reading Room Interactions: Scan Drawer, Footnote Popovers, Progress, Search, Shortcuts
(function () {
  var fontSize = 20.5;
  var focusMode = false;
  var pagefind = null;
  var searchTimeout = null;
  var currentScanLeaf = 1;

  var canvas = document.querySelector('.reader-canvas');
  var bookSlug = canvas ? canvas.dataset.bookSlug : '';
  var chapterId = canvas ? canvas.dataset.chapterId : '';
  var archiveId = canvas ? canvas.dataset.archiveId : '';
  var proofingBase = canvas ? (canvas.dataset.proofingBase || '') : '';
  var storageKey = bookSlug && chapterId ? (bookSlug + '-' + chapterId) : '';

  function updateProgress() {
    var docH = document.documentElement.scrollHeight - window.innerHeight;
    var pct = docH > 0 ? Math.min(100, Math.max(0, (window.scrollY / docH) * 100)) : 0;
    var bar = document.getElementById('progress');
    if (bar) bar.style.width = pct.toFixed(1) + '%';
  }

  window.toggleMenu = function () {
    var menu = document.getElementById('menuPanel');
    var overlay = document.getElementById('overlay');
    if (!menu || !overlay) return;
    var open = !menu.classList.contains('open');
    menu.classList.toggle('open', open);
    overlay.classList.toggle('show', open);
  };

  window.closeMenu = function () {
    var menu = document.getElementById('menuPanel');
    var overlay = document.getElementById('overlay');
    if (menu) menu.classList.remove('open');
    if (overlay) overlay.classList.remove('show');
  };

  window.toggleFocusMode = function () {
    focusMode = !focusMode;
    document.body.classList.toggle('focus-mode', focusMode);
    window.closeMenu();
    showShortcutHint(focusMode ? 'Focus Mode On — Press F or Esc to exit' : 'Focus Mode Off');
  };

  window.adjustSize = function (delta) {
    fontSize = delta === 0 ? 20.5 : Math.max(16, Math.min(27, fontSize + delta));
    var el = document.querySelector('.reading-prose');
    if (el) {
      el.style.fontSize = fontSize + 'px';
      try { localStorage.setItem('fontSize-' + bookSlug, String(fontSize)); } catch (e) {}
    }
    showShortcutHint('Font size ' + fontSize + 'px');
  };

  function showShortcutHint(msg) {
    var hint = document.getElementById('shortcutHint');
    if (!hint) return;
    hint.textContent = msg;
    hint.classList.add('show');
    clearTimeout(hint._timer);
    hint._timer = setTimeout(function () { hint.classList.remove('show'); }, 1800);
  }

  // Facsimile Scan Drawer (<dialog>)
  var scanDrawer = document.getElementById('scanDrawer');
  var scanImg = document.getElementById('scanDrawerImg');
  var scanTitle = document.getElementById('scanDrawerTitle');
  var scanLeafEl = document.getElementById('scanDrawerLeaf');
  var scanIaLink = document.getElementById('scanIaLink');
  var scanProofLink = document.getElementById('scanProofLink');
  var scanStage = document.getElementById('scanDrawerStage');

  function openScanLeaf(leafNum, folioLabel, explicitUrl) {
    if (!scanDrawer || !scanImg) return;
    currentScanLeaf = Math.max(1, parseInt(leafNum, 10) || 1);
    var url = explicitUrl || (archiveId ? ('https://archive.org/download/' + archiveId + '/page/n' + Math.max(0, currentScanLeaf - 1) + '_w1400.jpg') : '');
    if (!url) return;
    scanImg.src = url;
    if (scanTitle) scanTitle.textContent = folioLabel ? ('Printed Folio ' + folioLabel) : ('Scan Leaf ' + currentScanLeaf);
    if (scanLeafEl) scanLeafEl.textContent = 'IA Leaf ' + currentScanLeaf;
    if (scanProofLink && proofingBase && bookSlug) {
      scanProofLink.href = proofingBase.replace(/\/+$/, '') + '/#desk/' + encodeURIComponent(bookSlug) + '/' + currentScanLeaf;
      scanProofLink.style.display = '';
    }
    if (scanIaLink && archiveId) {
      scanIaLink.href = 'https://archive.org/details/' + archiveId + '/page/n' + Math.max(0, currentScanLeaf - 1) + '/mode/1up';
      scanIaLink.style.display = '';
    }
    if (scanStage) scanStage.classList.remove('is-zoomed');
    if (!scanDrawer.open) scanDrawer.showModal();
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.folio-trigger, #openChapterScanBtn');
    if (btn) {
      e.preventDefault();
      openScanLeaf(btn.dataset.page, btn.dataset.folio, btn.dataset.scan);
      return;
    }

    // Inline Footnote Popover
    var fnLink = e.target.closest('.fn-ref a');
    var pop = document.getElementById('fnPopover');
    if (fnLink && pop) {
      var targetId = fnLink.dataset.fnTarget || (fnLink.getAttribute('href') || '').replace(/^#/, '');
      var noteEl = targetId ? document.getElementById(targetId) : null;
      if (noteEl) {
        e.preventDefault();
        var bodyClone = noteEl.querySelector('.fn-body');
        document.getElementById('fnPopoverLabel').textContent = 'Note ' + fnLink.textContent;
        document.getElementById('fnPopoverBody').innerHTML = bodyClone ? bodyClone.innerHTML : noteEl.innerHTML;
        document.getElementById('fnPopoverJump').href = '#' + targetId;
        pop.hidden = false;
        var rect = fnLink.getBoundingClientRect();
        var topPos = Math.min(window.innerHeight - 220, Math.max(70, rect.bottom + 10));
        var leftPos = Math.min(window.innerWidth - 400, Math.max(16, rect.left - 40));
        pop.style.top = topPos + 'px';
        pop.style.left = leftPos + 'px';
        return;
      }
    }

    if (pop && !pop.hidden && !e.target.closest('#fnPopover')) {
      pop.hidden = true;
    }
  });

  var popClose = document.getElementById('fnPopoverClose');
  if (popClose) popClose.addEventListener('click', function () {
    document.getElementById('fnPopover').hidden = true;
  });
  var popJump = document.getElementById('fnPopoverJump');
  if (popJump) popJump.addEventListener('click', function () {
    document.getElementById('fnPopover').hidden = true;
  });

  if (scanDrawer) {
    document.getElementById('scanCloseBtn')?.addEventListener('click', function () { scanDrawer.close(); });
    document.getElementById('scanPrevBtn')?.addEventListener('click', function () {
      openScanLeaf(Math.max(1, currentScanLeaf - 1), '', '');
    });
    document.getElementById('scanNextBtn')?.addEventListener('click', function () {
      openScanLeaf(currentScanLeaf + 1, '', '');
    });
    document.getElementById('scanZoomBtn')?.addEventListener('click', function () {
      scanStage?.classList.toggle('is-zoomed');
    });
    scanDrawer.addEventListener('click', function (e) {
      if (e.target === scanDrawer) scanDrawer.close();
    });
  }

  // Book Search (Pagefind)
  async function initBookSearch() {
    if (pagefind) return;
    pagefind = await import('/pagefind/pagefind.js');
    await pagefind.options({ excerptLength: 22 });
  }

  async function handleBookSearch(query) {
    var box = document.getElementById('bookSearchResults');
    if (!box) return;
    if (!query || query.length < 2) { box.innerHTML = ''; return; }
    try {
      await initBookSearch();
      var search = await pagefind.search(query, { filters: { book: bookSlug } });
      var results = await Promise.all(search.results.slice(0, 10).map(function (r) { return r.data(); }));
      if (!results.length) {
        box.innerHTML = '<div class="no-results">No matches inside this book</div>';
        return;
      }
      box.innerHTML = results.map(function (r) {
        return '<a href="' + r.url + '" class="book-search-result">' +
          '<span class="result-title">' + (r.meta.title || 'Section') + '</span>' +
          '<span class="result-excerpt">' + r.excerpt + '</span></a>';
      }).join('');
    } catch (err) {
      box.innerHTML = '<div class="no-results">Search index builds after production/pagefind step.</div>';
    }
  }

  window.openMenuAndFocusSearch = function () {
    var menu = document.getElementById('menuPanel');
    var overlay = document.getElementById('overlay');
    var input = document.getElementById('bookSearchInput');
    menu?.classList.add('open');
    overlay?.classList.add('show');
    if (input) setTimeout(function () { input.focus(); }, 100);
  };

  document.addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (scanDrawer && scanDrawer.open) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); openScanLeaf(Math.max(1, currentScanLeaf - 1), '', ''); }
      if (e.key === 'ArrowRight') { e.preventDefault(); openScanLeaf(currentScanLeaf + 1, '', ''); }
      return;
    }
    switch (e.key.toLowerCase()) {
      case 's': e.preventDefault(); window.openMenuAndFocusSearch(); break;
      case 'm': e.preventDefault(); window.toggleMenu(); break;
      case 'f': e.preventDefault(); window.toggleFocusMode(); break;
      case 'arrowleft':
        var prev = document.querySelector('.pag-card.is-prev');
        if (prev) { e.preventDefault(); window.location.href = prev.href; }
        break;
      case 'arrowright':
        var next = document.querySelector('.pag-card.is-next');
        if (next) { e.preventDefault(); window.location.href = next.href; }
        break;
      case 'escape':
        window.closeMenu();
        if (focusMode) window.toggleFocusMode();
        var pop = document.getElementById('fnPopover');
        if (pop) pop.hidden = true;
        break;
    }
  });

  window.addEventListener('scroll', updateProgress, { passive: true });
  window.addEventListener('beforeunload', function () {
    if (storageKey) {
      try { localStorage.setItem('scroll-' + storageKey, String(window.scrollY)); } catch (e) {}
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('bookSearchInput');
    if (input) {
      input.addEventListener('input', function (e) {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(function () { handleBookSearch(e.target.value); }, 200);
      });
    }
    try {
      var savedSz = localStorage.getItem('fontSize-' + bookSlug);
      if (savedSz) {
        fontSize = parseFloat(savedSz);
        var prose = document.querySelector('.reading-prose');
        if (prose) prose.style.fontSize = fontSize + 'px';
      }
      if (!window.location.hash && storageKey) {
        var savedY = localStorage.getItem('scroll-' + storageKey);
        if (savedY) window.scrollTo(0, parseInt(savedY, 10));
      }
    } catch (e) {}
    updateProgress();
  });
})();
