# Decisions

Numbered and append-only. Each says what was decided, why, and what was rejected. Read before
changing anything these touch. Decisions about the book pipeline are in `../akshara_new/DECISIONS.md`.

## D1: Keep Hugo; rebuild the templates for design mock 14 (2026-11-21)

**Decided.** The site stays on Hugo, moved from 0.139.3 to 0.170.0, with every template rewritten from
scratch to the approved design mock 14. Same repository, same Cloudflare Worker, same domain.

**Why.** The pipeline already writes Hugo pages for every edition (`render_hugo.py`, pipeline D45), so a
different site builder would mean rebuilding the pipeline's output too. Hugo is a single program with no
package tree, and builds the 1,300 pages in seconds where the old templates took over eight minutes on the
new Hugo. The mock is plain HTML and CSS, which Hugo templates express directly.

**Rejected.** Astro (the usual default for new sites): a rewrite of the pipeline's output for no gain to
readers. A new Worker on a new address: it would split the site's history and search standing.

## D2: Every address the site has served keeps working (2026-11-21)

**Decided.** `tests/known-urls.txt` lists every address akshara.ink has served (the live sitemap of
2026-11-21 and the March 2026 site). `scripts/check_urls.py`, run by `./verify`, fails the build if any of
them neither opens a page nor redirects to one through `static/_redirects`. Lines are never removed.

**Why.** The 2026-11-20 sync moved four books' chapters under `/chapters/` and dropped three books,
breaking 169 addresses that other sites and readers linked to. Links to a public library must last.

**Rejected.** Hugo `aliases` in each chapter's front matter: the pipeline rewrites those files on every
sync, so the aliases would be lost. They also make meta-refresh pages rather than real redirects.

## D3: Static assets only on Cloudflare; no Worker script (2026-11-21)

**Decided.** `wrangler.toml` has no `main`. Cloudflare serves `public/` directly, applies `_headers` and
`_redirects`, and answers unknown addresses with `404.html` and a real 404 status.

**Why.** The old Worker script (`src/index.js`) passed on the 404 page with a 200 status, so search
engines saw every broken link as a real page. Its headers were also only applied to pages that missed the
static files. Less code, fewer places to be wrong.

**Rejected.** Fixing the script: nothing it did needs code.

## D4: Strict content security policy, no third-party scripts (2026-11-21)

**Decided.** Scripts run only from akshara.ink (`script-src 'self' 'wasm-unsafe-eval'`, the latter for the
search index's WebAssembly). Inline styles are allowed, because each book's cloth colour is set in a
`style` attribute. Images may load from archive.org, for the scan beside each page. Cloudflare Web
Analytics was removed from the policy.

**Why.** No inline scripts remain, so `'unsafe-inline'` for scripts is no longer needed. A public library
should not send its readers to third parties.

**Rejected.** Moving every colour into classes to drop inline styles: hundreds of generated classes for a
small gain, since inline styles cannot run code.

## D5: Series numbers are frozen in data (2026-11-21)

**Decided.** Each book's "Akshara No." is stored in `data/series.toml` and never changes or is reused.
Numbers 1 and 18 belonged to books withdrawn for copyright and stay retired. A new book takes the next
number; the build stops if a book has none.

**Why.** The mock worked the numbers out from the catalogue's order, so withdrawing or adding a book
would have renumbered others. A series number printed on a cover must be permanent.

## D6: Book pages are made from each edition's own record (2026-11-21)

**Decided.** A book page shows only what the edition already records: its front matter, its chapters,
its first sentence, its tables, its own edition note. Nothing about a book is written by the site except
the hand-set cover titles in `data/bookdetails.toml` and the curated quotations in `data/home.toml`.
Stage One books say plainly that they have not been checked page by page.

**Why.** At hundreds of books, hand-written pages cannot keep up, and an invented description is worse
than none. Every claim on a book page can be traced to the pipeline's record.

## D7: Search reads the whole text, through Pagefind (2026-11-21)

**Decided.** Pagefind indexes every chapter and book page after the build. Results are built as text
nodes and `<mark>` elements, never inserted as HTML. The library page's own filter (title, author, year,
description) needs no index and works instantly.

**Why.** Pagefind was already used by the live site, runs with no server, and keeps the index on
akshara.ink. Inserting result excerpts as HTML would put stored text into the page unescaped.

## D8: Book text is checked before it is published (2026-11-21)

**Decided.** `scripts/check_content.py` reads every built page and fails the build on script, style,
frame or form elements inside book text, event-handler attributes, `javascript:` links, images from
anywhere but this site and archive.org, and images whose files are missing.

**Why.** Chapter text comes from the pipeline, where a model reads each page, and goes onto the site as
HTML. The security policy would block most harm, but nothing should rely on one layer. The first run found
five broken images in three Stage One chapters, left over from the old OCR; each is now a plain note that
a figure is printed there and not yet reproduced.

## D9: Warn at 90% of Cloudflare's limits (2026-11-21)

**Decided.** `scripts/check_limits.py` fails the build above 18,000 files or 1,800 redirects (90% of
the Free plan's 20,000 and 2,000).

**Why.** 63 books already make 6,648 files, most of them downloads. At a few hundred books the deploy
would be refused without warning. When the warning comes, move `static/downloads` to GitHub Releases or
R2 rather than raising the margin.

## D10: The design is "The Plate" (2026-11-21)

**Decided.** The site is rebuilt to direction A, "The Plate", as refined over seventeen rounds into the
mock at `../design_directions/2026-11-redesign/plate.html` (judged against `BRIEF.md` there). Every shelf
has a pale paper and a deeper ink, washed and deepened from its cloth: the classes `.su .ma .le .co .cl
.vi .ec .cu` in `assets/css/plate.css` set `--g` (paper) and `--k` (ink), and `data/shelves.toml` names
each shelf's class as `code`. The engravings print as masks in the shelf's ink, so one cleaned file
prints in any colour. All styles are in one file, `assets/css/plate.css`; the old `akshara.css` and the
unused stylesheets beside it were removed.

**Why.** Bhuvanesh chose A of three directions and rejected a combined version: the engravings are the
most beautiful thing the project owns, and printing them in each shelf's ink makes the whole library
read as one series.

**Rejected.** B, The Title Page (typography alone), and C, The Register (a timeline); a mix of the three.

## D11: White paper (2026-11-21)

**Decided.** The page is pure white, `#FFFFFF`. Colour comes only from the shelves' pale papers and inks.

**Why.** Compared side by side in the mock, white let the shelf colours and the engravings carry the page;
the warm off-white made everything look aged on purpose.

**Rejected.** `#F9F8F5`, the warm white the mock also offered; the cream paper banned by the brief.

## D12: Newsreader for all text, Noto Serif Kannada for the mark, self-hosted (2026-11-21)

**Decided.** One family, Newsreader (variable, weights 200–800, optical sizes 6–72), sets every word.
Noto Serif Kannada sets only ಅಕ್ಷರ; it is instanced at weight 500 and cut to the Kannada block
(`static/fonts/noto-serif-kannada-500-subset.woff2`, 35 KB, made with fonttools from the Google Fonts
repository's variable file; since D23 cut to the five letters of the mark, `noto-serif-kannada-500-mark.woff2`, 3 KB). Both are served from akshara.ink; the policy allows no font host (D4).
The fonts that nothing used any more (Crimson, Inter, JetBrains Mono, Source Serif) were removed.

**Why.** The mock was approved in these faces. Newsreader's optical sizes let one family serve the large
light headlines and the 19px reading text.

**Known limit.** Newsreader has no old-style figures and no true small capitals (checked in both the
site's files and the full family). The reading text asks for old-style figures, so they appear if the
font ever gains them; small capitals at a chapter's opening are drawn by the browser from capitals,
exactly as they were in the approved mock.

## D13: A centred masthead (2026-11-21)

**Decided.** On a wide screen the header is a masthead: Library, Plates and Authors on the left, the mark
in the middle, Journal, About and Search on the right. On a phone it folds to the mark on the left and
Library and Search on the right. One hairline beneath, no colour band; Search is a plain word with a
small glass. Every link is at least 44px tall.

## D14: The footer is a colophon (2026-11-21)

**Decided.** The footer ends the site as a book ends: the printer's device from the First Letter Book (a
ship before the sun), the house name and its gloss, one sentence on what Akshara is, the ways back in on
one line of words, and a last line with Bhuvan's Twitter, LinkedIn and GitHub (from `hugo.toml`).

**Rejected.** The three columns of grouped links: a directory, not an ending.

## D15: The opening page (2026-11-21)

**Decided.** In this order: the headline beside a turning plate (six engravings crossfading every 6.5
seconds, each on its own shelf's paper, still for readers who ask for reduced motion), one sentence on
what the library holds, a compact "Begin reading →" and one sentence beneath it; New on the shelves; the
featured edition; Small things from the books; How a book is made (the photographed table beside the set
one, then the four steps); the eight shelves with their epigraphs. Everything hand-chosen on the page
(the turning plates and their captions, the featured edition's words, the small things, the book
"Begin reading" opens) is in `data/home.toml`. "New on the shelves" is worked out: the books added most
recently, at most one per shelf, those with a picture of their own first.

**Why.** The first screen on a phone says what Akshara is and offers the next step, with an engraving
on it, which is what the project has that nobody else has.

**Rejected.** The open-book comparison and the strip of engravings from the earlier opening: two
signatures where the Plate has one. The commons section and the closing quotation: their facts are on
the book pages and the About page.

## D16: The visual grammar is the source of truth for design (2026-11-21)

**Decided.** `docs/VISUAL_GRAMMAR.md` is the rulebook for how Akshara looks: principles, colour, type,
space, the plate, covers, components, motion, writing, and how to extend it. Every value it relies on is a
CSS custom property in `assets/css/plate.css` (type sizes as `--fs-…` role tokens, section rhythm as
`--sec`, the measure as `--measure`, colours as named tokens and shelf classes); the document names the
tokens and never repeats their values. A design change updates the grammar in the same change.

**Why.** Future sessions and the sister projects (living books, a review) must be able to follow the
design without reverse-engineering the stylesheet, and a document that repeats raw values drifts from
what ships.

**Rejected.** A design-token build step (Style Dictionary or similar): a dependency and a generator for
what custom properties already do.

## D17: Five kinds of cover, each picture from its own book (2026-11-21)

**Decided.** Every book's cover is drawn from `data/covers.toml`: its kind (engraving, map, device,
portrait or photograph, type only), the key of its plate in `static/plates/`, and where needed a crop
(`inset`). A cover's picture always comes from that same book, never another book, volume or edition.
Each plate's book is recorded where it was made (`data/plates.toml`, `data/plate_sources.toml`), and
`scripts/check_covers.py`, run first by `./verify`, fails if a cover uses a plate recorded for another
book, if a book has no cover, or if a type-only cover does not say why. 37 books carry a picture; 26 are
type only, three of them (Toru Dutt, Sarojini Naidu, the Comprehensive History Vol. II) until better scans
are found. New plates are made by `scripts/make_plates.py` from the sources and crops recorded in
`data/plate_sources.toml` (grayscale, level, negate to an alpha mask on black; photographs first get an
ordered-dither halftone). Book titles on covers never break inside a word: a title with a word of eleven
letters or more steps its type down.

**Why.** A series must be recognisable from across a room, so one system holds every cover; and a
library of rare books cannot dress one book in another's picture.

**Dependency.** `make_plates.py` uses Pillow 13.0.0 (pinned in the script's own `uv` header, never a site
dependency): image decoding, cropping and levels, which the standard library cannot do. Pillow is the
standard Python imaging library, maintained since 2010 and among the most-used packages on PyPI. It runs
only when plates are remade, not in the build or CI.

**Rejected.** Covers taking the first figure the pipeline extracted (too often a table or a blot);
borrowing another volume's engraving for a book without one.

## D18: The library: search, three arrangements, shelves face out (2026-11-21)

**Decided.** The library page has a real search field: as the reader types it narrows the covers by
title, author, year, place and shelf at once, and lists where the words occur in the text of the books
(Pagefind; up to five books with two places in each, then a link to the search page). Without JavaScript the field is a plain form that
opens the search page. Three arrangements, switched by plain words on a hairline: by shelf, by date (by
decade) and by author (by surname). On a phone each group is a row of covers to swipe, snapping to the
gutter; on a wide screen a grid of six. The text catalogue with its tier marks is gone: a book's tier is
on its own page. The shelf, author and collection pages show the same covers, and `/books/` is titled
The Library.

## D19: The book page is one band, then the book's own material (2026-11-21)

**Decided.** A book's page opens on one full-width band in its shelf's paper holding the cover and the
text: the series line (Akshara No., volume, shelf), the short title, the rest of the title in italic, the
author, place and year, then Begin reading (naming the first chapter), the downloads as one sentence, and
the book's measure as figures on one hairline (pages, chapters, tables, hours). On a phone Begin reading
comes before the description so it is always on the first screen. Below: how the book begins (its own
first sentence), contents, its plates, one of its tables set as printed, this edition (how far it is
checked, the record, every form), the editor's note, and the imprint. A prose description is shown as
written; the pipeline's catalogue line ("Archival scope: …") is not shown raw: its record's own period,
places and subjects are shown as two plain lines instead (D6: nothing invented).

## D20: The reading page (2026-11-21)

**Decided.** A chapter has a reading bar in place of the masthead: the way back to the book, Contents, Aa
and Focus, with a hairline beneath that fills in the book's ink as the chapter is read. The chapter opens
with a headpiece: one of the book's own engravings (a different one per chapter when it has several), or,
for a book with no engraving, the house mark; a photograph is never used as a headpiece. Text at 19px on a
phone and 20px from 760px, measure about 33em, indented paragraphs, old-style figures asked for (D12),
small capitals only on the chapter's first line. The author's marginal notes sit in the left margin on a
wide screen and above their paragraph on a phone; the printed page numbers sit in the right margin and open
the scan. The chapter ends with a short rule, then next and before. Every earlier feature stays: the panel
(size, paper, spacing, width, paragraphs, edges, notes, page numbers), the scan leaf, focus, find in this
book, the keys and the progress line. Marginal notes are now shown by default (the reader can hide them),
and paragraphs are indented by default, as the books were printed.

## D21: Favicon, social previews and /library/ (2026-11-21)

**Decided.** The favicon is ಅ, traced from Noto Serif Kannada (weight 500) into an outline, in the Surveys
shelf's ink on its pale paper, with a dark version for devices in dark mode (`static/favicon.svg`); a
180px touch icon and a 32/16px `favicon.ico` are made from the same outline. Every book has a social
preview, 1200×630, made by Hugo itself at build time (`layouts/_partials/book/social.html`): the shelf's
paper, the book's own plate printed in its ink (cut from a block of ink with the plate as a mask), the series
line, the title, the author and year. Type-only books set the title larger under a rule. The rest of the site
uses one card for Akshara (`page/social-home.html`). The plates are mounted as assets for this
(`hugo.toml`, `[module]`). The text is drawn with three small static instances of Newsreader in
`assets/fonts/og-*.ttf` (Latin only, made with fonttools; licence beside them), used only at build time and
never sent to readers. `/library/` and `/library` redirect to `/books/`.

**Why.** Hugo's own image filters (Padding, Mask, Overlay, Text) do this with no new dependency and no
step outside the build, so the cards can never fall out of date with the covers.

**Rejected.** Screenshots of a card page with a headless browser (a browser in CI, or 64 committed images
that drift); an image library in a script (a dependency for what the build can do).

## D22: Dark mode follows the device; the reading room's Paper can override it (2026-11-21)

**Decided.** The whole site has a dark version: a deep neutral paper (`#17181A`), light inks, and for each
shelf a dark ground and an ink lifted toward the light so the plates still read (every shelf ink at least
5.5:1 on its ground). It follows the device's light or dark setting and changes with it. The reading room's
Paper setting (Day, Cotton, Night, and Auto, which follows the device) is kept on the device and applies to
every page. A small script in the page's head (`assets/js/paper.js`, self-hosted, so D4 holds) sets
`<html data-theme>` before the page is drawn, so a chosen paper never flashes white. Only tokens change in
dark mode; on dark paper the solid Begin reading block becomes a deep tint of the ink. Photographs of pages
are dimmed a little; the books' own figures in the text are printed light on dark.

**Rejected.** A `prefers-color-scheme` media query alone: it cannot honour a reader's chosen paper on every
page. A toggle in the masthead: one more control for something the device already decides.

## D23: Speed: send only what the reader will see (2026-11-21)

**Decided.**
- **Plates at the size they are shown.** `layouts/_partials/plate/url.html` asks the build for a copy no wider
  than needed (covers 440px, a book's own cover 800px, tiles 600–640px, headpieces 700px, the turning plate
  960px, the footer device 200px), and keeps the hand-made file instead whenever the copy would be heavier.
  Nothing extra is committed; Hugo makes and caches the copies.
- **Nothing below the first screen is laid out or fetched until the reader comes near it** (`content-visibility:
  auto` on shelf rows, bookcases, bands, plate groups, result rows and figures in chapters). The library loads
  one row of covers, not sixty-three.
- **The turning plate fetches only the next engraving,** a little before it turns, instead of all six at once.
- **Fonts cut to what is used.** The Kannada mark is cut to the five letters of ಅಕ್ಷರ (35 KB to 3 KB). The
  accented letters the books actually use (74, chiefly transliteration) are in a small file of their own
  (about 30 KB in each style), so the 90 KB Latin Extended file loads only for a page that needs a rarer
  letter. Both upright and italic Latin are preloaded; the unused Vietnamese files were removed.
- Measured on a first visit with nothing cached, before compression: the opening page went from about 1.36 MB
  to about 0.87 MB (of which 0.4 MB is the two text fonts), the library to about 0.4 MB, a chapter to about
  0.6 MB. HTML and CSS are compressed further by Cloudflare.

**Rejected.** Lossy re-encoding of every plate in a script (the masks' fine lines blur, and the gain was
small beside not loading them at all); a font-loading script (the browser's own `unicode-range` does it).

## D24: The third ink is darkened for legibility (2026-11-21)

**Decided.** `--ink-3`, the faintest text colour (captions, notes on notes, placeholders), is `#76726A`,
4.8:1 on white, instead of the mock's `#8A867E` (3.6:1, below the 4.5:1 that WCAG asks of small text). In
dark mode it is `#8E897F` (5.1:1). Every other ink already passed: `--ink-2` 7.5:1, each shelf's ink at least
7:1 on white and 5.9:1 on its own ground.

## D25: Review 0002 answered (2026-11-21)

**Decided.** Every finding of the fresh-eyes review `reviews/0002-plate-redesign.md` is fixed or answered
there, each bug fix with its test. Shelf colours moved to `data/shelves.toml`, from which the build writes the
shelf classes (`assets/css/shelves.css`) and the social cards read their colours. The cover check now checks
each plate's record against its source. The security policy keeps `'unsafe-inline'` in `style-src` for
browsers that do not know `style-src-elem`/`style-src-attr` (inline style attributes carry plate addresses
and crops; without them older Safari would show blank covers) and narrows `<style>` elements to this site in
the browsers that do.

**Noted for later.** The library page draws every cover three times (by shelf, date and author): about 140 KB
of HTML for 63 books, so about 1 MB at 500. When that matters, render the shelf view and build the other two
in the script from the same cards.

## D26: Every edition is CC BY 4.0, and says so (2026-11-21)

**Decided (by Bhuvanesh).** Every Akshara edition is released under Creative Commons Attribution 4.0
International. The site says so in the footer of every page, in each book page's edition record (with the
note that the book itself is in the public domain), and in a `<link rel="license">` in every page's head. The
licence's name and address are in `hugo.toml` (`license_name`, `license_title`, `license_url`).

**Why.** It had been stated nowhere: a reader or another library could not tell what they may do with an
edition, and a public library's terms should be plain on every page.
