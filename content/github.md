---
title: "The Code & Open Data"
description: "Source repositories, open editions (EPUB, Markdown, TEI XML, CSV tables), CC BY 4.0 licensing, and machine-readable endpoints for Project Akshara."
type: "page"
---

Everything that makes Akshara — the website, the digitization pipeline, and the finished editions — is published openly on GitHub. The underlying books are in the public domain, and every Akshara edition is released under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## Repositories

- **[akshara](https://github.com/bebhuvan/akshara)** — The website (`akshara.ink`), built with Hugo and Pagefind, including every layout, cover specification, plate record, and build check.
- **[akshara-library](https://github.com/bebhuvan/akshara-library)** — The open archive of published editions: Markdown, TEI XML archival masters, EPUBs, Print PDFs, original page-scan PDFs (in GitHub Releases), and every extracted statistical table as diplomatic and tidy CSV with Frictionless Data Packages.
- **[akshara-new](https://github.com/bebhuvan/akshara-new)** — The page-by-page digitization, verification, table-arithmetic, and compilation pipeline.

## Bulk Access & Machine-Readable Endpoints

Researchers, librarians, software developers, and AI agents can read the entire catalogue programmatically without scraping HTML:

- **[`/llms.txt`](/llms.txt)** — Curated Markdown index of the library, shelves, books, direct Markdown editions, and page-level citation conventions (`#p-<folio>`).
- **[`/llms-full.txt`](/llms-full.txt)** — Expanded compendium with bibliographic metadata, chapter URLs, author biographies, and dataset pointers for all editions.
- **[`/catalog.json`](/catalog.json)** — Complete JSON catalogue (CORS-enabled) covering every book, author, shelf, collection, download URL, and Internet Archive provenance identifier.
- **[`/data/tables_atlas.json`](/data/tables_atlas.json)** — Structured index of all extracted historical statistical tables with links to diplomatic CSV, tidy CSV, chapter context, and original scan pages.
- **[`/index.xml`](/index.xml)** — RSS 2.0 feed of new editions and Journal essays.

## Proofreading & Corrections

If you spot a misreading, dropped footnote, or broken figure in any edition, you can check the text beside the original scan at [proof.akshara.ink](https://proof.akshara.ink) or [write to me](/contact/).
