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

The design follows design mock 14 (`../design_mocks/directions/14-akshara-next`, see its `GRAMMAR.md`):
paper and ink, one cloth colour per shelf, covers and spines drawn from each book's data.

## Where things are

| Path | What it holds |
|---|---|
| `content/books/<id>/` | One folder per book: `_index.md` (its record) and its chapters, from the pipeline |
| `content/shelves/_content.gotmpl` | Makes the eight shelf pages from `data/shelves.toml` |
| `data/shelves.toml` | The eight shelves, their colours and epigraphs |
| `data/series.toml` | Each book's permanent series number (Akshara No.). Never renumber |
| `data/bookdetails.toml` | Hand-set cover titles, author spellings and cover engravings |
| `data/plates.toml` | The cleaned engravings in `static/plates/`, each tied to its book and page |
| `data/home.toml` | The quotations and plates chosen for the opening page |
| `layouts/` | The templates. `_partials/book/record.html` is the one place a book's details are worked out |
| `assets/css/akshara.css`, `assets/js/akshara.js` | All the styles and the one small script |
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
address in `tests/known-urls.txt` still opens a page or redirects to one, and audits dependencies.
CI runs it on every push.

## Add a book

1. Make the edition in the pipeline, then copy it in with `scripts/sync_from_pipeline.py`.
2. Give it the next number in `data/series.toml`. The build stops until you do.
3. Make sure its `archetype` is one of the eight shelves in `data/shelves.toml`. The build stops if not.
4. Run `./verify`.

## Deploy

Pushing to `main` deploys to akshara.ink through GitHub Actions (`.github/workflows/deploy.yml`), after
`./verify` passes. To check a change privately first, deploy the preview:

```bash
npx wrangler deploy --env preview
```

## If a page moves

Add a line `old-path new-path 301` to `static/_redirects`. `./verify` fails if any known address breaks.

## Decisions

Why things are the way they are: `DECISIONS.md`.
