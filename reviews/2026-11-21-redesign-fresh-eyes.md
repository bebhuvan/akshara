# Review: redesign to mock 14 (859d148..d798348)

Reviewed up to: d798348
Reviewer model: Claude Opus 5.5 (claude-opus-5-5), fresh session, not the author
Gates: `./verify` passed (Hugo 0.170.0 build with `--panicOnWarning`, 1334 pages; Pagefind indexed 1178
pages; "Checked 1426 known addresses and 169 redirects. Every known address works."; Python compile OK;
`npm audit`: 0 vulnerabilities). `verify` has no lint, format check or tests (finding 9).
Extra checks run: a link walk over every built HTML page (0 broken internal links); search loaded in
headless Chromium behind the exact CSP from `static/_headers` (works); a scan of all pipeline HTML in
`content/books` for script, event handlers, iframes, forms and off-site images (none today).

## In plain words

The rebuild is in good shape where it matters most for safety: no inline scripts, a strict CSP that
search works under, search results built as text, every old address still resolving, and no broken
internal links. The problems are mostly about **what the pages say**. Several sentences promise
things the data does not back: the home page and Reading Room say every book sits page by page beside its
scan, but 16 of 63 do not; the Tables page says "every table, 530 in all" when the books record about 1,004;
search says "344 pages answer" and shows 30 with no way to see the rest. "How it begins" and "Begin reading"
are picked by a rule that sometimes picks a bibliography or a title page. Fix those before launch; the rest
can follow.

## Findings

### 1. [high] Home page, Reading Room and closing quote promise a scan beside every page; 16 books have none
- Where: `layouts/home.html:17` ("Each is read afresh from photographs of its pages … kept page by page
  beside its scan"), `layouts/home.html:173` ("every page is kept beside its photograph"),
  `layouts/page/reading-room.html:5` ("the photograph of each page a tap away")
- Failure: the 16 `edition_tier: "v1_archive"` books have no `data-scan` folio buttons at all (checked:
  `letters-from-malabar`, `life-in-an-indian-village`, `indian-shipping` have 0; Journey vol. I has 450). The
  Reading Room picks the lowest series number on each shelf, so **5 of its 8 featured books are Stage One
  books without scans**, directly under the sentence promising scans. The book page for these books says
  the truth ("has not been checked against the scans page by page"), so the site contradicts itself.
- Rule: DECISIONS D6 (every claim traceable to the record); CLAUDE.md "numbers or claims … the data does
  not support"
- Fix: word the home and Reading Room copy for "the new editions" only, or compute it ("47 of the 63 …").
  Have the Reading Room pick the first non-Stage-One book on each shelf.
- Resolution:

### 2. [medium] Search says how many pages matched but shows only the first 30, with no way to see more
- Where: `assets/js/akshara.js` `search()` (`res.results.slice(0, 30)`, tally uses `res.results.length`)
- Failure: `/search/?q=famine` shows "344 pages answer to 'famine'." and lists 30. At 500 books almost every
  word will exceed 30. Readers can't reach result 31 or later, and nothing tells them the list is cut.
- Fix: a "Show more" button that loads the next 30 `r.data()` calls, or say "the first 30 are shown".
- Resolution:

### 3. [medium] The Tables page undercounts and says "every table"
- Where: `layouts/page/datasets.html:3-7`
- Failure: the total is summed from `tables_list`, which the pipeline caps at 30 per book. Nine books have
  more (Poverty and Un-British Rule: `tables_count` 169, 333 CSVs on disk). The page says "Every table set
  from the books so far, 530 in all", but the books' own `tables_count` add up to 1,004, and the lists
  are silently cut at 30. Each book page says "169, each given as CSV", which disagrees with this page.
- Fix: use `tables_count` for the total, and for capped books say "the first 30 of 169" and link the
  book's data package. Or have the pipeline write the full list.
- Resolution:

### 4. [medium] "How it begins" and "Begin reading" sometimes show a bibliography, title page or heading
- Where: `layouts/_partials/book/first-chapter.html`, `layouts/_partials/book/first-sentence.html`
- Failure (built pages): Early Travels begins reading at "List of Chief Authorities Quoted" and quotes
  "Manucci, Niccolao. Storia do Mogor…" as its opening. Indian Shipping begins at "List of Authorities".
  Dutt's Indian Famines quotes "Late of the Indian Civil Service, and of the Middle Temple,
  Barrister-at-Law." England's Debt and Periplus quote their own headings in capitals ("CHAPTER I A
  Historical Retrospect…"). English Factories vol. 2 quotes a date fragment. The Pālas skips Chapter I
  (tagged `introduction`) and "Begin reading" opens Chapter II. Five books show no opening at all. At 500
  books nobody will catch these by eye.
- Fix: let the record name the opening (`featured_quote` already exists; add `begin_at`). Have the build
  list, or fail on, books whose chosen first chapter title matches /authorities|contents|list of/i. Remove
  `sec-h1` text before picking the sentence.
- Resolution:

### 5. [medium] Old /themes/, /periods/ and /languages/ pages pass the address check but are empty or misleading
- Where: `hugo.toml` taxonomies, `layouts/taxonomy.html`, `layouts/term.html`
- Failure: `/themes/` and `/periods/` render a heading and an empty list, because no content sets those
  taxonomies. `/languages/english/` lists 13 *author* pages and no books, because books use `language:`
  (singular), not `languages:`. `check_urls.py` counts any `index.html` as "works", so the gate is green.
- Fix: redirect them to `/books/` (or the library filtered), or populate them from the book records.
  Consider making `check_urls.py` flag pages with an empty main list.
- Resolution:

### 6. [medium] Every shared link has a broken preview image
- Where: `layouts/_partials/page/head.html:12` (`og-image.png`)
- Failure: only `static/og-image.svg` exists, and `http://127.0.0.1:8791/og-image.png` returns 404. Every
  share on WhatsApp, X, Mastodon and the like shows no image. Social sites also don't accept SVG.
- Fix: add a 1200×630 `og-image.png` to `static/`, and add the file to `tests/known-urls.txt`.
- Resolution:

### 7. [medium] Keyboard users land on links that screen readers are told to ignore (shelf pages)
- Where: `layouts/shelves/page.html:12` (`<div class="so-case" aria-hidden="true">` holding spine `<a>` links)
- Failure: on all eight `/shelves/*/` pages, Tab moves through every spine link, but assistive technology
  announces nothing, because they sit inside `aria-hidden`. The home page already fixes this by turning
  spines into `<span>` (`home.html:126`); the shelf page doesn't.
- Rule: WCAG 4.1.2 / ARIA "no focusable content inside aria-hidden"
- Fix: render spines as spans here too (the covers below already link to each book), or drop `aria-hidden`.
- Resolution:

### 8. [medium] Chapter HTML from the pipeline (model output) is inserted raw with no check at the site boundary
- Where: `hugo.toml` (`unsafe = true`), `layouts/chapters/page.html:92` (`$text | safeHTML`),
  `layouts/books/book.html` (`editorial_note_markdown | markdownify`)
- Failure: the text is read by a vision model, and the site trusts the pipeline's HTML completely. Today it
  is clean (scanned: no script, `on*=`, iframe, form, meta or off-site src). But one bad sync could ship
  markup that the CSP doesn't stop: `<meta http-equiv=refresh>`, fake links, CSS overlays. Nothing in
  `verify` would notice. It also passes through non-HTML tags such as `<unclear>` (32 uses).
- Rule: CLAUDE.md "model output is untrusted data … check outside data once where it enters"
- Fix: add an allow-list tag/attribute check of `content/books/**` to `verify` (standard library
  `html.parser`), failing on anything outside the compiler's known set.
- Resolution:

### 9. [medium] `verify` has no lint, format check or tests; the only code with logic is untested
- Where: `verify`
- Failure: `assets/js/akshara.js` (excerpt escaping, filter, `words()`), `scripts/check_urls.py`, and the
  template rules (`record.html` title/author/sort-name munging, first-sentence picking) have no tests. A
  regression in `excerptNodes` would reintroduce HTML injection with every gate green. The repo also has
  no gitleaks pre-commit hook, though its code is linked publicly from `/github/`.
- Rule: CLAUDE.md Quality gates
- Fix: add `node --test` for the pure functions in `akshara.js` (export them), a `unittest` for
  `check_urls.py`, and a built-page assertion script for the record rules. Add gitleaks.
- Resolution:

### 10. [medium] At a few hundred books the site will hit Cloudflare's static-asset limits, and no check warns first
- Where: `wrangler.toml` (assets-only Worker), `static/_redirects`, `scripts/check_urls.py`
- Failure: `public/` holds 6,644 files for 63 books (~105 per book, mostly `downloads/` and `pagefind/`).
  Workers static assets allow 20,000 files per version on the Free plan (100,000 on Paid), so around 190
  books on Free. `_redirects` allows 2,000 static rules. This sync alone needed 169 for four books, lines
  are never removed, and `check_urls.py` forbids wildcards. The deploy will fail on main with no
  warning beforehand.
- Fix: have `check_urls.py` fail above 1,800 redirects and `verify` fail above 90% of the plan's file
  limit. Plan to move `downloads/` to R2 or GitHub Releases. Record the plan limit in DECISIONS.md.
- Resolution:

### 11. [medium] Stage One books show invented-looking page counts as fact
- Where: `layouts/books/book.html` ("Pages … printed pages"), `record.html` (`pages | default 300`)
- Failure: Lays of Ancient India, Religion of the Veda and Rig-Veda all say "300 printed pages", and both
  volumes of Comprehensive History say "900". These are round placeholders from the v1 records. The spine
  widths use them too, and `record.html` quietly defaults to 300 when the field is missing.
- Rule: D6
- Fix: hide "Pages" for `v1_archive` unless verified. Make a missing `pages` a build error, not 300.
- Resolution:

### 12. [low] Smaller things
- Fonts are cached `immutable` for a year but not fingerprinted (`static/_headers` `/fonts/*`). A changed
  Kannada subset would stay stale for returning readers. 19 of the 24 font files are unused by the CSS and
  still deployed.
- `layouts/_partials/words.html` errors at 1,000 (`index $ones 10`). JS `words()` prints digits from 100
  while the template spells them out, so the library tally changes wording when JS loads.
- `book/all.html` says "Cached" but is called with plain `partial` at 7 call sites. Build cost grows with books × pages.
- `chapters/page.html` strips only the first `sec-h1`. 110 of 1,115 chapters still open with a printed
  heading in capitals under the new title (e.g. Journey vol. I ch. I keeps "CHAPTER I." plus a shouting h3).
  The `$book.Title "Chapters"` branch is dead: no `chapters/_index.md` exists.
- 3 Hugo `aliases` (meta-refresh pages) still come from pipeline front matter, which D2 rejected.
- Six `content/books/*/_index.md` were hand-edited (`_target` → `target`). The next sync of those books
  will undo the edit without warning.
- The 10 new addresses (`/plates/`, `/reading-room/`, `/shelves/*`) are not in `tests/known-urls.txt`, so a
  future move of them would not be caught.
- The home page quote "It begins: In the afternoon of the 23d April 1800…" is really the second sentence.
  The book opens "MY inquiries could not commence…", which is what the book page shows.
- "New books, by RSS" (`/index.xml`) is a feed of the 20 latest chapters, mostly shouting-caps titles, not books.
- The reading panel has no focus trap, and the single-key shortcuts (M, F, +, −) can't be turned off (WCAG 2.1.4).
  Night paper is applied after the deferred script runs, so night readers get a flash of white on every chapter.
- `npx wrangler deploy` with no `--env` deploys to the worker named `akshara`, the production worker.
  README shows only `--env preview`, but one missing flag deploys a local build live. Consider renaming
  the top-level worker.
- Cloudflare's matching of `_redirects` sources with or without a trailing slash is untested. Check one
  old address without its slash on the preview deploy before going live.
