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
repository's variable file). Both are served from akshara.ink; the policy allows no font host (D4).
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
