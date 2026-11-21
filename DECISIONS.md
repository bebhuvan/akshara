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
