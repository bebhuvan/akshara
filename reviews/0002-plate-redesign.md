# Review 0002: the Plate redesign (`origin/main...design/plate`, b3819c8..3269ece)

Reviewed up to: 3269ece
Reviewer model: Claude Opus 5.5 (claude-opus-5-5), fresh subagent, not the author
Gates: `./verify` passed in 21 s with Hugo 0.170.0: "All 63 covers checked: 37 with a picture from their own
book, 26 type only"; build with `--panicOnWarning`; Pagefind indexed 1178 pages; "Checked 1427 known addresses
and 189 redirects. Every known address works."; "Checked 1250 pages … No unsafe or broken markup"; 7151 files
and 378 redirects (within limits); 16 unit tests OK; Python compiles; `npm audit` 0 vulnerabilities.
`verify` still has no lint or format check (carried over from the previous review, finding 9).

Extra checks run: search on the built site (http://127.0.0.1:1415) through Pagefind's own API and on the
search page; a contrast audit of every visible text element on the home, book and chapter pages in light and
dark mode; a tap-target audit at 375px; keyboard use of the reading panel; a script that compares each entry
in `data/plate_sources.toml` with the book its source file or archive.org scan belongs to (all 28 match);
the social cards for the longest titles and for a title with an accent (they look right); Pillow 13.0.0 on
PyPI (released 2026-10-16, old enough).

## In plain words

The redesign is careful where it counts most: the security policy is strict, search results are built as
text, every old address still works, every cover's picture really does come from its own book (I checked all
28 new plates against their sources), and the cover rule is enforced by a tested check. Two things should be
fixed before this goes live. **Search results now show a stray ", shelf:vi" after every book's title**, on
the search page and in the library's search, because of how the shelf was added to the search index. And the
new footer tells readers on every page that "every text is read against the scan", which is not true of the
16 Stage One books and is the same kind of claim the last review asked to remove. Below those: the home
page's "New on the shelves" row will shrink to a single book the next time one book is added; the page-number
buttons in the reading room are about 10 pixels across on a phone; the turning plate cannot be paused; and a
few small things in the docs and code.

## Findings

### 1. [high] Every search result shows ", shelf:xx" after the book's title, and results never get their shelf's colour
- Where: `layouts/chapters/page.html:118` and `layouts/books/book.html:47`
  (`data-pagefind-meta="book:{{ $b.cover_title }}, shelf:{{ $b.code }}"`); read by `assets/js/akshara.js:33`
  and `:49`
- Failure: Pagefind 1.6.0 stores the whole string as the `book` value. Checked on the built site:
  `/search/?q=Sepoy` lists "A Brief History of the Indian Peoples, shelf:vi", "A Comprehensive History of
  India, shelf:co", and so on for every result. `meta.shelf` is never set, so on the search page no result
  gets its shelf class (`li class="hit"`). The same titles appear in the library's "In the text of the books"
  list. On `origin/main` the attribute was `book:` alone, so this is new in the branch. No check catches it
  because nothing tests what the search index holds.
- Rule: D18 (results grouped by book, the title in its shelf's ink); readers will see it at once
- Fix: give the shelf its own element or attribute, e.g. `data-pagefind-meta="book:{{ … }}"` on the article
  and a separate `<span hidden data-pagefind-meta="shelf:{{ $b.code }}"></span>` inside it (or Pagefind's
  `shelf[data-shelf]` attribute form). Add a step to `verify` that loads `public/pagefind` fragments (or greps
  one built page's fragment) and fails if a `book` value contains `shelf:`.
- Resolution: Fixed in 418d301: book and shelf are separate search fields; `check_content.py` refuses a search-metadata value with a comma (test in `test_checks.py`), and `test_built_site.py` checks the fields.

### 2. [high] The new footer says on every page that every text is read against its scan; 16 books are not
- Where: `layouts/_partials/page/foot.html:10` ("Every text is read against the scan of the copy it came from.")
- Failure: 16 of the 63 books are `edition_tier: "v1_archive"`. Their own pages say "It has not been checked
  against the scans page by page" (`layouts/books/book.html:156`), and the same footer sits directly under
  that sentence. The line is new in this branch (not in `origin/main`'s footer). It repeats the problem of
  the previous review's finding 1, which was about the same promise on the home page.
- Rule: D6 ("Stage One books say plainly that they have not been checked page by page"); global standard:
  claims must trace to the data
- Fix: say what is true of all of them ("Each edition says how far it has been checked against its scan"),
  or count it ("47 of the 63 are read against the scan").
- Resolution: Fixed in 418d301: the footer now says "Each new edition is read against the photographs of the copy it came from, and says how far it has been checked."

### 3. [medium] "New on the shelves" will show one book the next time a single book is added
- Where: `layouts/home.html:43-53`
- Failure: the row takes only books whose date equals the single latest date. Today 47 books share
  2026-11-20, so the row has four. Add one book dated, say, 2026-12-05 and `$latest` becomes that date: the
  row shows that one book alone, and stays that way until another book shares its exact date. The README's
  "add a book" steps don't mention it.
- Rule: D15 ("the books added most recently, at most one per shelf")
- Fix: sort all books by date (then series number) descending and take the first four that pass the
  one-per-shelf rule, instead of filtering to one date.
- Resolution: Fixed in 6f662e6: the row takes the most recently added books across all dates (date, then series number); `test_built_site.py` checks four books from four shelves.

### 4. [medium] The page numbers that open the scan are about 10 pixels across on a phone
- Where: `assets/css/plate.css:697` (`#chapter-text .folio-trigger`: 11px type, `padding: 0`, set in the 20px gutter)
- Failure: measured at 375px on Journey vol. I, chapter I: 61 page-number buttons, each 7 to 14 px wide and
  11 px tall. The scan beside the text is the feature the site is built around; on a phone it is very hard to
  hit, and easy to miss for anyone with less steady hands. The reading bar's "Aa" button is 20 px wide.
- Rule: WCAG 2.2 target size (24×24 minimum); D13 sets 44px for links
- Fix: keep the small numeral but enlarge the hit area, e.g. `padding: 12px 8px; margin: -12px -8px` (or a
  `::before` with `inset: -14px`), and give "Aa" `min-width: 44px`.
- Resolution: Fixed in 6f662e6: the numeral stays small; its place to tap is 26×35px, and it does not push past the screen edge.

### 5. [medium] The turning plate on the opening page moves for ever with no way to stop it
- Where: `assets/js/akshara.js:398-425`, `layouts/home.html:24-30`
- Failure: the engraving and its caption change every 6.5 seconds without end. Only readers whose device asks
  for reduced motion get a still plate; anyone else (including someone distracted by movement who has never
  found that setting) has no pause.
- Rule: WCAG 2.2.2 Pause, Stop, Hide (level A): moving content that starts by itself and lasts more than 5
  seconds needs a way to pause it
- Fix: a small "Pause" / "Play" button in the caption line (it already has the "1 of 6" counter), or stop
  after one full round, or stop on hover and focus.
- Resolution: Fixed in 6f662e6: a Pause / Play button beside "1 of 6"; `test_built_site.py` checks it is there.

### 6. [medium] The featured edition's quotation source is below WCAG contrast; D24 says every ink passes
- Where: `assets/css/plate.css:240` (`.feat-body > figure figcaption { color: var(--ink-3) }` on the
  shelf's pale ground)
- Failure: measured on the home page: "The day the survey began · vol. I, p. 1" at 14.5px is 4.29:1. `--ink-3`
  is 4.8:1 on white but only 3.8 to 3.9:1 on any of the eight light shelf grounds, so any future use of
  `--ink-3` inside a band, feature or cover falls short too. D24 states "Every other ink already passed" and
  checked `--ink-3` only on white.
- Rule: D24; WCAG 1.4.3
- Fix: use `--ink-2` (about 6:1 on every ground) for text on a shelf ground, and add that rule to
  `docs/VISUAL_GRAMMAR.md` and D24.
- Resolution: Fixed in 6f662e6: text on a shelf's ground (the featured quotation's source, a shelf's epigraph source) uses `--ink-2`.

### 7. [medium] The cover check trusts a typed `book` field; it never checks the picture's source belongs to that book
- Where: `scripts/check_covers.py:17-26` (`plate_books`), `data/plate_sources.toml`
- Failure: the rule "a cover's picture always comes from its own book" is only as good as the `book =` line
  typed beside each plate. A plate made from `static/figures/journey-from-madras-vol-ii/…` but entered with
  `book = "journey-from-madras-vol-i"` passes the check and the build. (Today all 28 entries are right: I
  compared each source folder or archive.org identifier with the book's own `archive_id`.) Also, a key that
  appears in both `plates.toml` and `plate_sources.toml` with different books is silently resolved to the
  second.
- Rule: D17 ("the rule that is never broken"); global standard: check outside data once where it enters
- Fix: in `check_covers.py`, require that a `static/figures/<id>/…` source has `<id> == book`, and that an
  archive.org source's identifier equals that book's `archive_id` (or appears in its `archive_url`); fail on a
  key recorded twice with different books. Add a test for each.
- Resolution: Fixed in 6f662e6: `provenance_problems` checks a figures source against its book, an archive.org source against the book's `archive_id`, refuses other sources and a key recorded for two books; a test for each in `test_covers.py`.

### 8. [medium] A new shelf would break the social cards and lose dark mode; the grammar only says to add one CSS class
- Where: `layouts/_partials/book/social.html:7-8` (hard-coded paper and ink per shelf), `assets/js/akshara.js:54`
  (hard-coded `su|ma|le|co|cl|vi|ec|cu`), `assets/css/plate.css:848-855` (dark classes),
  `docs/VISUAL_GRAMMAR.md:408`
- Failure: the shelf colours now live in three places (the CSS, the social-card template and the script), and
  `data/shelves.toml` still holds a `cloth` value that nothing uses any more. A ninth shelf added as the
  grammar says gets no social-card colour (`index` returns nothing, so the card build fails or comes out
  wrong), no dark-mode colours, and no colour on library search results. Changing one shelf's ink in the CSS
  leaves the social cards in the old ink. D16 says every value is a token in `plate.css`, but social.html
  repeats them.
- Rule: D16; global standard "one obvious place for each thing"
- Fix: put each shelf's `paper`, `ink`, `paper_dark` and `ink_dark` in `data/shelves.toml`, and have
  social.html read them (and, if wanted, a small template that writes the shelf classes). At least, list
  every place in VISUAL_GRAMMAR §11 "A new shelf", and drop the unused `cloth` from `record.html:72`.
- Resolution: Fixed in 6f662e6: each shelf's paper, ink and dark pair are in `data/shelves.toml`; the build writes the classes (`assets/css/shelves.css`) and the social cards read them; the unused `cloth` was dropped from the record; the build stops if a shelf lacks a colour. Rendering is pixel-identical. VISUAL_GRAMMAR §11 updated.

### 9. [low] HTML built from front matter and data is marked safe instead of escaped
- Where: `layouts/books/book.html:60-64` (download links built with `printf` and `safeHTML`),
  `layouts/_partials/book/cover.html:10` (`inset` from `data/covers.toml` through `safeCSS`, never
  validated), `layouts/page/plates.html:8` (plate group names through `safeHTML`)
- Failure: a `download_epub` value containing `"` (it comes from the pipeline sync) breaks out of the
  attribute. `check_content.py` would catch an event handler or a `javascript:` link, and the CSP blocks
  scripts, so the harm is limited; but the global standard says no raw-HTML insertion of stored text, and
  these three can be written without it.
- Rule: global standard, Security ("no raw-HTML insertion of stored or fetched text")
- Fix: build the download sentence in the template (`<a href="{{ . }}" download>EPUB</a>` in a range with
  the separators as plain text); check `inset` in `check_covers.py` against
  `^-?\d+% -?\d+% -?\d+% -?\d+%$`; set the group name's italic part with a template, not `safeHTML`.
- Resolution: Fixed: the download sentence is built in the template with escaped addresses; the plates heading is escaped before italics are added; a cover's `inset` must be four percentages or the build stops.

### 10. [low] The CSP allows inline `<style>` elements when only style attributes need it
- Where: `static/_headers:11` (`style-src 'self' 'unsafe-inline'`); its comment (line 3) still says inline
  styles "carry each book's cloth colour", which is no longer what they carry
- Failure: the site only needs inline `style="…"` attributes (plate URLs, `inset`, `--rs`). `'unsafe-inline'`
  in `style-src` also lets an injected `<style>` element run, which is the CSS-based leak route if pipeline
  HTML ever carries one.
- Fix: `style-src 'self'; style-src-attr 'unsafe-inline'`, and correct the comment. Confirm search and the
  reading room still work under it (Pagefind's UI is not used, so it should).
- Resolution: Answered (D25): `style-src-elem 'self'` and `style-src-attr 'unsafe-inline'` added, so browsers that know them refuse `<style>` elements from elsewhere; `'unsafe-inline'` stays in `style-src` for older browsers, which would otherwise show blank covers. Comment corrected.

### 11. [low] The open reading panel does not hold keyboard focus
- Where: `assets/js/akshara.js:197-216`
- Failure: press M, then Shift+Tab: focus goes to the Focus button behind the scrim (checked). On a phone the
  panel covers 92% of the screen, so keyboard and switch users move through controls they can't see. The tabs
  also lack arrow-key movement.
- Fix: while open, make the rest of `.read` `inert` (or trap Tab inside the panel), and give the panel
  `role="dialog" aria-modal="true"` with its existing label.
- Resolution: Fixed: while the panel is open, everything else on the page is `inert`, so Tab stays in the panel.

### 12. [low] Smaller things
- `layouts/home.html:71`: "Read chapter I" opens the Introduction (`02-introduction`), because
  `first-chapter.html` allows introductions. Use `$featFirst`'s own name, as the book page's Begin reading does.
- `data/home.toml` featured plates: two of the three "plates beneath" the featured Vol. I are from Vol. II and
  Vol. III, with captions that don't say so ("Seringapatam bull, fig. 38"), under the link "The volume, its
  contents and plates". Add the volume to those captions.
- `layouts/chapters/page.html:21-23`: portraits marked `face = true` (pal-jones, j1-krishna) are used as
  chapter headpieces and print as negatives in dark mode (seen on Pālas of Bengal, Preface), which the
  `face` comment in `plates.toml` says should never happen. Skip `face` plates as headpieces, or apply the
  `.face` treatment.
- `layouts/books/book.html:193`: `<b>{{ $b.title }}</b>{{ with $b.subtitle }}…` has no space or stop between
  title and what follows, so screen readers and the search index read "…Indian PeoplesOxford: Clarendon".
- `assets/js/akshara.js:368-379`: two quick taps on "Show more" both read from the same `shown` and list
  the same 60 results twice. Disable the button while loading.
- Without JavaScript the site is always light, even on a dark device: `data-theme` is set only by `paper.js`.
  A `@media (prefers-color-scheme: dark)` fallback on `html:not([data-theme])` would cover it.
- Docs that disagree with the code: D12 names `noto-serif-kannada-500-subset.woff2` (35 KB); the file is
  `noto-serif-kannada-500-mark.woff2` (3 KB, per D23). D18 says the library lists "six results"; the code shows
  up to five books with two places each. Since DECISIONS is append-only, a one-line note under D12 pointing to
  D23 is enough.
- The library page carries every cover three times (by shelf, date, author): 138 KB of HTML for 63 books,
  so about 1 MB at 500. Not urgent; worth a line in DECISIONS for when it starts to matter.
- Dead files: `static/covers/` (3 MB, about 126 files) is no longer used by any page; `static/plates/j1-oilmill.webp`,
  `pal-rubbing.webp` and `dims.json` are recorded nowhere and used nowhere (these three predate the branch).
  `/og-image.png` and `/logo.svg` were removed; old shared links pointed at `/og-image.png`, so a redirect to
  `/og/akshara.jpg` would keep their previews.
- `scripts/make_plates.py` has pure functions (`check_entry`, `auto_levels`, `crop_box`, `fit_long_side`)
  and no tests; the global standard asks for tests of logic. It also follows archive.org's redirects to
  whatever host they name; harmless for archive.org, but the host check only covers the first URL.
- Resolution: Fixed: "Read chapter I" opens chapter I and names it from the chapter; the featured plates from vols. II and III say so; `face` plates are not used as headpieces; the imprint has a stop after the title; "Show more" waits for one fetch to finish; without the script the page follows the device's dark setting; D12 and D18 corrected; the library's thrice-drawn covers noted in D25; `dims.json` removed and `/og-image.png` redirected to the site card. `static/covers/` is written by the pipeline's sync script, so it stays until the sync stops writing it (a pipeline change). The plate script's pure functions moved to `scripts/plate_maths.py` with tests (`test_plate_maths.py`), and a download redirected away from archive.org's own servers is refused.
