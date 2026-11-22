# Akshara

The website of [Akshara](https://akshara.ink), a free public-domain library of rare books about India:
travellers' journals, East India Company records, famine reports, economic histories, speeches,
letters and verse, each read afresh from photographs of its pages and kept page by page beside its scan.

This repository is the site only. The books are made by the pipeline in `../akshara_new`, which writes
each edition's Hugo pages; `scripts/sync_from_pipeline.py` copies them in here.

## How it is built

- **Hugo 0.170.0** turns `content/` into a static site in `public/`. The version is in `.hugo-version`.
- **Pagefind** builds the full-text search index from the finished pages.
- **Cloudflare** serves `public/` as static files (no server code). `static/_headers` sets the security
  and cache headers; `static/_redirects` keeps old addresses working.

The design is "The Plate" (`../design_directions/2026-11-redesign/plate.html`, see `DECISIONS.md` D10–):
white paper, and for each shelf a pale paper and a deep ink. Every cover is drawn from the book's data and
carries a picture from that same book, printed in its shelf's ink, or its title alone. The rules for how
everything looks, and for extending it, are in `docs/VISUAL_GRAMMAR.md`: read it before changing the design.

## Where things are

| Path | What it holds |
|---|---|
| `content/books/<id>/` | One folder per book: `_index.md` (its record) and its chapters, from the pipeline |
| `content/shelves/_content.gotmpl` | Makes the eight shelf pages from `data/shelves.toml` |
| `data/shelves.toml` | The eight shelves, their colours and epigraphs |
| `data/series.toml` | Each book's permanent series number (Akshara No.). Never renumber |
| `data/bookdetails.toml` | Hand-set cover titles and author spellings |
| `data/covers.toml` | Each book's cover: its kind and which of its own pictures it carries |
| `data/plates.toml` | The cleaned engravings in `static/plates/`, each tied to its book and page |
| `data/plate_sources.toml` | Where each newer plate came from (its book, page and crop), for `scripts/make_plates.py` |
| `data/home.toml` | What is hand-chosen on the opening page: the turning plates, the featured edition, the small things |
| `layouts/` | The templates. `_partials/book/record.html` is the one place a book's details are worked out |
| `assets/css/plate.css` | All the styles; every colour and size is a custom property named in `docs/VISUAL_GRAMMAR.md` |
| `assets/js/akshara.js`, `assets/js/paper.js` | The one small script, and the few lines that choose light or dark paper before a page is drawn |
| `layouts/_partials/book/social.html` | Each book's 1200×630 social preview, drawn by Hugo at build time |
| `assets/fonts/og-*.ttf` | Newsreader cut for drawing those previews; never sent to readers |
| `tests/known-urls.txt` | Every address the site has ever served. Never delete a line |

## Run it

You need Hugo 0.170.0 (extended) and Node 22.

```bash
npm ci --ignore-scripts
```

```bash
hugo server
```

Then open http://localhost:1313.

## Check it

```bash
./verify
```

This builds the whole site with warnings treated as errors, makes the search index, checks that every
address in `tests/known-urls.txt` still opens a page or redirects to one, checks every page for unsafe
or broken markup (`scripts/check_content.py`), warns before Cloudflare's size limits
(`scripts/check_limits.py`), runs the tests in `tests/`, and audits dependencies. CI runs it on every push.

To refuse commits containing secrets, turn on the hook once per clone (needs gitleaks):

```bash
git config core.hooksPath .githooks
```

## Add a book

1. Make the edition in the pipeline, then copy it in with `scripts/sync_from_pipeline.py`.
2. Give it the next number in `data/series.toml`. The build stops until you do.
3. Make sure its `archetype` is one of the eight shelves in `data/shelves.toml`. The build stops if not.
4. Give it a cover in `data/covers.toml` (see `docs/VISUAL_GRAMMAR.md`, Covers). If it has a picture of its
   own, add the picture's source and crop to `data/plate_sources.toml` and make it with
   `uv run scripts/make_plates.py --only <key>`. The check stops the build if the cover is missing or its
   picture comes from another book.
5. Run `./verify`.

## Deploy

Pushing to `main` deploys to akshara.ink through GitHub Actions (`.github/workflows/deploy.yml`), after
`./verify` passes. To check a change first, deploy the preview (the default; only `--env production` touches the live site):

```bash
npx wrangler deploy
```

To roll back the live site, either revert the merge on `main` (CI deploys the reverted site), or return the
Worker to an earlier version at once: `npx wrangler deployments list --env production` shows the versions, and
`npx wrangler rollback <version-id> --env production` serves one again.

### The living book's path

The living-book imprint is a separate Worker on a path of akshara.ink (DECISIONS.md, D31). This repository
does not build or deploy it; its only part is the one redirect line for the path without its final slash.

## If a page moves

Add a line `old-path new-path 301` to `static/_redirects`. `./verify` fails if any known address breaks.

## Decisions

Why things are the way they are: `DECISIONS.md`.
