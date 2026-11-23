#!/usr/bin/env python3
"""Thin publisher sync: copies compiled Akshara v6 editions & covers into akshara_site_v2 and akshara_library."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import re
import shutil
import sys
from typing import Any

LEGACY_REDIRECT_MAP: dict[str, str] = {
    "economic-history-india-early-british-dutt": "/books/economic-history-of-india/",
    "economic-history-india-victorian-age-dutt": "/books/economic-history-india-victorian-age/",
    "englands-debt-to-india-lajpat-rai-1917": "/books/englands-debt-to-india/",
}
LEGACY_SUPERSEDED_DIRS = {
    "economic-history-of-india",
    "economic-history-india-victorian-age",
    "englands-debt-to-india",
    "imperial-gazetteer-india-v1",
}

AUTHOR_SLUG_ALIASES: dict[str, str] = {
    "w-h-moreland": "william-harrison-moreland",
    "rammohun-roy": "raja-rammohun-roy",
    "f-max-m-ller": "f-max-muller",
    "friedrich-max-muller": "f-max-muller",
    "john-nicol-farquhar": "j-n-farquhar",
}

LEGACY_PROOFING_APP_URL = "https://akshara-proofing.r-bhuvanesh2007.workers.dev"
CANONICAL_PROOFING_APP_URL = "https://proof.akshara.ink"

COLLECTION_DEFINITIONS: list[dict[str, Any]] = [
    {
        "slug": "indian-economic-history",
        "title": "Indian Economic History & Political Economy",
        "period": "1600–1925",
        "description": (
            "Foundational critiques of the Drain Theory, deindustrialization, land settlements, "
            "tariffs, currency, and colonial public finance."
        ),
        "match_archetypes": {"political_economy_ledger", "currency_and_finance"},
        "extra_books": [
            "india-at-the-death-of-akbar",
            "from-akbar-to-aurangzeb",
            "economics-in-india-inaugural-lecture-jevons-1915",
            "economic-life-bengal-district-faridpur-1916",
            "recent-economic-developments-punjab-wilson-1910",
            "early-history-tea-industry",
        ],
    },
    {
        "slug": "east-india-company-and-trade",
        "title": "East India Company & Maritime Trade",
        "period": "1st Century CE – 1667",
        "description": (
            "Calendars of 17th-century factory correspondence, early European travelogues, "
            "Indian Ocean commerce, and maritime shipping."
        ),
        "match_archetypes": {"maritime_company_records"},
        "extra_books": ["guide-to-india-office-records-1919"],
    },
    {
        "slug": "famines-and-agrarian-surveys",
        "title": "Famines, Surveys & District Handbooks",
        "period": "1807–1920",
        "description": (
            "Empirical field surveys, famine commission histories, village household accounts, "
            "and provincial agricultural monographs."
        ),
        "match_archetypes": {"survey_and_gazetteer"},
        "extra_books": [
            "famines-and-land-assessments",
            "indian-famines-causes-prevention-dutt-1901",
            "economic-causes-of-famines-in-india-ray-1909",
            "history-and-economics-indian-famines-loveday-1914",
            "report-past-famines-bombay-etheridge-1868",
            "musalmans-and-money-lenders",
            "life-in-an-indian-village",
        ],
    },
    {
        "slug": "historical-studies",
        "title": "Chronicles, Statecraft & Regional History",
        "period": "Ancient to Early Modern India",
        "description": (
            "Syntheses of ancient kingdoms, Mughal revenue and administration, "
            "the Maratha confederacy, and sweeping Indian histories."
        ),
        "match_archetypes": {"court_and_chronicle"},
        "extra_books": ["brief-history-indian-peoples"],
    },
    {
        "slug": "reformers-and-visionaries",
        "title": "Speeches, Letters & Reformers",
        "period": "1800–1940",
        "description": (
            "Parliamentary evidence, speeches, correspondence, and reform movements "
            "that shaped modern Indian public life."
        ),
        "match_archetypes": {"epistolary_and_speeches"},
        "extra_books": [
            "judicial-revenue-systems-india-rammohun-1832",
            "poverty-and-un-british-rule",
            "englands-debt-to-india-lajpat-rai-1917",
            "while-sewing-sandals",
            "modern-religious-movements-india",
        ],
    },
    {
        "slug": "vedic-sanskrit-studies",
        "title": "Classical, Vedic & Philological Studies",
        "period": "Vedic & Classical Traditions",
        "description": (
            "Classical translations, Vedic philology, comparative religion, and literary heritage "
            "from India's ancient canons."
        ),
        "match_archetypes": {"classical_and_philological"},
        "extra_books": [],
    },
]

_RELEASE_HELPER_TEMPLATE = """#!/usr/bin/env python3
\"\"\"Upload heavy Print PDF and .originals.pdf camera scan assets to GitHub Releases.\"\"\"

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess


def resolve_pipeline_root(cli_root: str | None = None) -> Path:
    lib_root = Path(__file__).resolve().parents[1]
    if cli_root:
        return Path(cli_root).expanduser().resolve()
    env_root = os.environ.get("AKSHARA_PIPELINE_ROOT") or os.environ.get("AKSHARA_NEW_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return (lib_root.parent / "akshara_new").resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload Print & Originals PDFs to GitHub Releases")
    parser.add_argument("--book", help="Single book_id to upload")
    parser.add_argument("--pipeline-root", help="Path to akshara_new repository")
    parser.add_argument("--repo", default="bebhuvan/akshara-library", help="Target GitHub repo")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    args = parser.parse_args()

    lib_root = Path(__file__).resolve().parents[1]
    pipeline_root = resolve_pipeline_root(args.pipeline_root)
    catalog = json.loads((lib_root / "catalog.json").read_text(encoding="utf-8"))
    books = [b for b in catalog["books"] if not args.book or b["book_id"] == args.book]

    for b in books:
        bid = b["book_id"]
        col = b["collection"]
        ed_dir = pipeline_root / "library" / col / bid
        print_pdf = ed_dir / "print" / f"{bid}.pdf"
        orig_pdf = pipeline_root / "sources" / f"{bid}.originals.pdf"
        assets = [str(p) for p in (print_pdf, orig_pdf) if p.is_file()]
        if not assets:
            print(f"SKIP {bid}: no heavy PDF assets found under {pipeline_root}")
            continue
        tag = f"edition-{bid}"
        title = f"{b['title']} ({b.get('publication_year') or 'PD'})"
        notes = (
            f"Compiled PDF and de-blotted Archive.org camera scan backup for `{bid}`.\\n\\n"
            f"- Tier: `{b['edition_tier']}` ({b['rubric_score']:.1f}/100)\\n"
            f"- Online Reader: https://akshara.ink/books/{bid}/"
        )
        exists = subprocess.run(
            ["gh", "release", "view", tag, "--repo", args.repo],
            capture_output=True,
        ).returncode == 0
        cmd = (
            ["gh", "release", "upload", tag, "--repo", args.repo, "--clobber", *assets]
            if exists
            else ["gh", "release", "create", tag, "--repo", args.repo, "--title", title, "--notes", notes, *assets]
        )
        print(f"[{'UPLOAD' if exists else 'CREATE'}] {tag}: {len(assets)} file(s)")
        if not args.dry_run:
            subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
"""


def _slugify(text: str) -> str:
    cleaned = re.sub(r"\b(?:sir|dr|prof|rev)\.?\s+", "", text.strip(), flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", cleaned.lower()).strip("-") or "public-domain"


def _parse_frontmatter(md_text: str, yaml_mod: Any) -> tuple[dict[str, Any], str]:
    if not md_text.startswith("---"):
        return {}, md_text
    parts = md_text.split("---", 2)
    if len(parts) < 3:
        return {}, md_text
    fm = yaml_mod.safe_load(parts[1]) or {}
    return dict(fm), parts[2].lstrip("\r\n")


def _copy_clean_text(src: Path, dst: Path, scrub_fn: Any) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    raw = src.read_text(encoding="utf-8", errors="replace")
    dst.write_text(scrub_fn(raw), encoding="utf-8")


def _rewrite_atlas_reader_url(raw_url: str, chap_slug_map: dict[str, dict[str, str]]) -> str:
    m = re.match(r"^([^/]+)/web/chapters/([^/#]+)\.html(#.*)?$", raw_url.strip())
    if not m:
        return raw_url
    bid, stem, frag = m.group(1), m.group(2), m.group(3) or ""
    hugo_stem = chap_slug_map.get(bid, {}).get(stem) or stem
    return f"/books/{bid}/chapters/{hugo_stem}/{frag}"


def _write_library_book_readme(
    dst: Path,
    *,
    bid: str,
    title: str,
    author: str,
    year: Any,
    imprint: str,
    col: str,
    tier: str,
    score: float,
    archive_url: str,
    has_datasets: bool,
    fig_count: int,
) -> None:
    lines = [
        f"# {title}",
        "",
        f"- **Author(s)**: {author}",
        f"- **Publication Year**: {year or 'Public Domain'}",
        f"- **Imprint**: {imprint or 'Public Domain'}",
        f"- **Collection**: `{col}`",
        f"- **Edition Tier**: `{tier}` (**{score:.1f} / 100**)",
        f"- **Internet Archive Source**: {archive_url or 'N/A'}",
        "",
        "## Files in This Folder",
        "",
        "- `EDITORIAL_NOTE.md` — Source scan provenance, what was normalized vs. preserved verbatim",
        "- `EDITION_REPORT.md` — Machine audit, spend telemetry, and validator summary",
        "- `PROOFING_BRIEFING.md` — Open verification notes and hotspots for proofreaders",
        f"- `epub/{bid}.epub` — Typeset EPUB 3 edition",
        f"- `html/{bid}.html` — Single-page Gutenberg-style HTML edition",
        f"- `markdown/{bid}.md` — Complete Scholarly Markdown",
        f"- `tei/{bid}.tei.xml` — TEI P5 XML archival master",
    ]
    if has_datasets:
        lines.append("- `datasets/` — Diplomatic 2D & Tidy unpivoted statistical CSV/JSON datasets (`datapackage.json`)")
    if fig_count:
        lines.append(f"- `figures/` — {fig_count} cropped archival plates/maps")
    lines.extend([
        "",
        "## Binary Release Assets",
        "",
        f"Typeset Print PDF (`{bid}.pdf`) and the de-blotted original camera scan (`{bid}.originals.pdf`) are attached to GitHub Release `edition-{bid}`.",
    ])
    dst.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    site_root = Path(__file__).resolve().parents[1]
    portable_root = (
        Path(os.environ["AKSHARA_PORTABLE_ROOT"]).expanduser().resolve()
        if os.environ.get("AKSHARA_PORTABLE_ROOT")
        else site_root.parent
    )

    parser = argparse.ArgumentParser(description="Copy compiled Hugo/asset bundles into akshara_site_v2 and akshara_library")
    parser.add_argument("--pipeline-root", default=str(portable_root / "akshara_new"))
    parser.add_argument("--library-root", default=str(portable_root / "akshara_library"))
    args = parser.parse_args()

    pipeline_root = Path(args.pipeline_root).expanduser().resolve()
    library_root = Path(args.library_root).expanduser().resolve()
    pipeline_src = pipeline_root / "src"
    if str(pipeline_src) not in sys.path:
        sys.path.insert(0, str(pipeline_src))

    import yaml  # type: ignore[import-untyped]
    from akshara.compiler.covers import generate_cover_assets
    from akshara.compiler.render_hugo import dump_hugo_frontmatter_md, scrub_local_paths

    library_root.mkdir(parents=True, exist_ok=True)
    (library_root / "collections").mkdir(parents=True, exist_ok=True)
    (site_root / "static" / "covers").mkdir(parents=True, exist_ok=True)
    (site_root / "static" / "downloads").mkdir(parents=True, exist_ok=True)
    (site_root / "static" / "figures").mkdir(parents=True, exist_ok=True)
    hugo_books_dir = site_root / "content" / "books"
    hugo_books_dir.mkdir(parents=True, exist_ok=True)

    ed_manifests = sorted(
        (pipeline_root / "library").glob("*/*/edition_manifest.json"),
        key=lambda p: (p.parent.parent.name, p.parent.name),
    )

    author_counts: dict[str, int] = defaultdict(int)
    author_first_pub: dict[str, int] = {}
    author_names: dict[str, str] = {}
    catalog_books: list[dict[str, Any]] = []
    all_site_books: list[dict[str, Any]] = []
    chap_slug_map: dict[str, dict[str, str]] = {}
    total_v6_pages = 0
    total_tables = 0
    total_tidy_obs = 0

    for mpath in ed_manifests:
        ed_dir = mpath.parent
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
        bid = str(manifest.get("book_id") or ed_dir.name)
        col = str(manifest.get("collection") or ed_dir.parent.name)
        hugo_src = ed_dir / "web" / "hugo"
        hm_path = hugo_src / "hugo_manifest.json"

        if manifest.get("blocked") or manifest.get("is_preview") or manifest.get("is_partial_pages"):
            continue
        if not (hm_path.is_file() and (hugo_src / "_index.md").is_file()):
            continue

        hm = json.loads(hm_path.read_text(encoding="utf-8"))
        lib_book_dir = library_root / "collections" / col / bid
        lib_book_dir.mkdir(parents=True, exist_ok=True)

        # 1. Covers (SVG + WebP) generated by akshara_new
        for cov_name in ("cover.svg", "cover.webp"):
            src_cov = ed_dir / cov_name
            if not src_cov.is_file():
                raise FileNotFoundError(f"Missing compiled {cov_name} in {ed_dir}")
            shutil.copy2(src_cov, site_root / "static" / "covers" / f"{bid}{Path(cov_name).suffix}")
            shutil.copy2(src_cov, lib_book_dir / cov_name)

        # 2. Proofing/rubric reports, Markdown, TEI XML, Gutenberg HTML, EPUB 3
        for doc_name in ("EDITORIAL_NOTE.md", "EDITION_REPORT.md", "PROOFING_BRIEFING.md", "edition_manifest.json", "rubric_score.json"):
            src_doc = ed_dir / doc_name
            if src_doc.is_file():
                _copy_clean_text(src_doc, lib_book_dir / doc_name, scrub_local_paths)

        site_dl_dir = site_root / "static" / "downloads" / bid
        site_dl_dir.mkdir(parents=True, exist_ok=True)
        for src_p, lib_rel, dl_name in (
            (ed_dir / "markdown" / f"{bid}.md", Path("markdown") / f"{bid}.md", f"{bid}.md"),
            (ed_dir / "tei" / f"{bid}.tei.xml", Path("tei") / f"{bid}.tei.xml", f"{bid}.tei.xml"),
        ):
            if src_p.is_file():
                _copy_clean_text(src_p, lib_book_dir / lib_rel, scrub_local_paths)
                _copy_clean_text(src_p, site_dl_dir / dl_name, scrub_local_paths)

        src_html = ed_dir / "html" / f"{bid}.html"
        if not src_html.is_file():
            src_html = ed_dir / "print" / f"{bid}.print.html"
        if src_html.is_file():
            raw_html = scrub_local_paths(src_html.read_text(encoding="utf-8", errors="replace"))
            (lib_book_dir / "html").mkdir(parents=True, exist_ok=True)
            (lib_book_dir / "html" / f"{bid}.html").write_text(raw_html, encoding="utf-8")
            site_html = raw_html.replace("src='../figures/", f"src='/figures/{bid}/").replace('src="../figures/', f'src="/figures/{bid}/')
            (site_dl_dir / f"{bid}.html").write_text(site_html, encoding="utf-8")

        src_epub = ed_dir / "epub" / f"{bid}.epub"
        if src_epub.is_file():
            (lib_book_dir / "epub").mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_epub, lib_book_dir / "epub" / f"{bid}.epub")
            shutil.copy2(src_epub, site_dl_dir / f"{bid}.epub")

        # 3. Figures & CSV/JSON Datasets
        fig_count = 0
        if (ed_dir / "figures").is_dir():
            figs = sorted(p for p in (ed_dir / "figures").iterdir() if p.is_file())
            if figs:
                (lib_book_dir / "figures").mkdir(parents=True, exist_ok=True)
                site_fig_dir = site_root / "static" / "figures" / bid
                site_fig_dir.mkdir(parents=True, exist_ok=True)
                for ff in figs:
                    shutil.copy2(ff, lib_book_dir / "figures" / ff.name)
                    shutil.copy2(ff, site_fig_dir / ff.name)
                fig_count = len(figs)

        src_ds = ed_dir / "datasets"
        has_datasets = False
        if src_ds.is_dir() and (src_ds / "datapackage.json").is_file():
            has_datasets = True
            for dst_ds in (lib_book_dir / "datasets", site_dl_dir / "datasets"):
                if dst_ds.exists():
                    shutil.rmtree(dst_ds)
                shutil.copytree(src_ds, dst_ds)
            tm_path = src_ds / "tables_manifest.json"
            if tm_path.is_file():
                tm = json.loads(tm_path.read_text(encoding="utf-8"))
                total_tidy_obs += sum(int(t.get("tidy_observation_count") or 0) for t in (tm.get("tables") or []))

        # 4. Copy compiled Hugo Markdown bundle & apply site author/redirect aliases
        dst_book = hugo_books_dir / bid
        if dst_book.exists():
            shutil.rmtree(dst_book)
        (dst_book / "chapters").mkdir(parents=True, exist_ok=True)

        raw_idx = (hugo_src / "_index.md").read_text(encoding="utf-8").replace(
            LEGACY_PROOFING_APP_URL, CANONICAL_PROOFING_APP_URL
        )
        idx_fm, idx_body = _parse_frontmatter(raw_idx, yaml)
        aslug = str(hm.get("author_slug") or idx_fm.get("author_slug") or _slugify(str(hm.get("primary_author") or "")))
        aslug = AUTHOR_SLUG_ALIASES.get(aslug, aslug)
        idx_fm["author_slug"] = aslug
        if bid in LEGACY_REDIRECT_MAP:
            idx_fm["aliases"] = [LEGACY_REDIRECT_MAP[bid]]
        (dst_book / "_index.md").write_text(dump_hugo_frontmatter_md(idx_fm, idx_body), encoding="utf-8")

        chap_slug_map[bid] = {}
        for ch_path in sorted((hugo_src / "chapters").glob("*.md")):
            ch_text = ch_path.read_text(encoding="utf-8").replace(
                LEGACY_PROOFING_APP_URL, CANONICAL_PROOFING_APP_URL
            )
            (dst_book / "chapters" / ch_path.name).write_text(ch_text, encoding="utf-8")
            stem = ch_path.stem
            chap_slug_map[bid][stem] = stem
            chap_slug_map[bid][re.sub(r"^\d{2,}-", "", stem)] = stem

        yr = hm.get("publication_year")
        primary_author = str(hm.get("primary_author") or "Public Domain")
        author_counts[aslug] += 1
        author_names.setdefault(aslug, primary_author)
        if isinstance(yr, int) and (aslug not in author_first_pub or yr < author_first_pub[aslug]):
            author_first_pub[aslug] = yr

        _write_library_book_readme(
            lib_book_dir / "README.md",
            bid=bid,
            title=str(hm["title"]),
            author=primary_author,
            year=yr,
            imprint=str(idx_fm.get("imprint") or ""),
            col=col,
            tier=str(hm["edition_tier"]),
            score=float(hm["rubric_score"]),
            archive_url=str(hm.get("archive_url") or ""),
            has_datasets=has_datasets,
            fig_count=fig_count,
        )

        pages = int(hm.get("pages") or 0)
        tables_cnt = int(hm.get("tables_count") or 0)
        total_v6_pages += pages
        total_tables += tables_cnt
        catalog_books.append({
            "book_id": bid,
            "title": hm["title"],
            "subtitle": hm.get("subtitle") or "",
            "authors": hm.get("authors") or [primary_author],
            "publication_year": yr,
            "collection": col,
            "edition_tier": hm["edition_tier"],
            "rubric_score": hm["rubric_score"],
            "pages": pages,
            "tables_count": tables_cnt,
            "footnotes_count": int(hm.get("footnotes_count") or 0),
            "archive_id": hm.get("archive_id") or "",
            "path": f"collections/{col}/{bid}",
        })
        all_site_books.append({
            "book_id": bid,
            "title": hm["title"],
            "author": primary_author,
            "author_slug": aslug,
            "year": yr,
            "archetype": hm["archetype"],
            "collection": col,
            "tier": hm["edition_tier"],
        })

    # 5. Remove superseded v1 stubs and refresh remaining PD v1 covers/frontmatter
    for old_dir in LEGACY_SUPERSEDED_DIRS:
        p = hugo_books_dir / old_dir
        if p.exists():
            shutil.rmtree(p)

    v6_ids = {b["book_id"] for b in all_site_books}
    v1_count = 0
    for bdir in sorted(hugo_books_dir.iterdir()):
        if not bdir.is_dir() or bdir.name in v6_ids or not (bdir / "_index.md").is_file():
            continue
        v1_count += 1
        bid = bdir.name
        fm, body = _parse_frontmatter((bdir / "_index.md").read_text(encoding="utf-8"), yaml)
        author = str(fm.get("editor") or fm.get("author") or "Public Domain")
        yr = fm.get("year")
        aslug = AUTHOR_SLUG_ALIASES.get(str(fm.get("author_slug") or _slugify(author)), str(fm.get("author_slug") or _slugify(author)))
        author_counts[aslug] += 1
        author_names.setdefault(aslug, author)
        if isinstance(yr, int) and (aslug not in author_first_pub or yr < author_first_pub[aslug]):
            author_first_pub[aslug] = yr

        cov = generate_cover_assets(
            book_id=bid,
            title=str(fm.get("title") or bid),
            author=author,
            year=yr,
            edition_tier="v1_archive",
            collection_title="Akshara Heritage Library",
            subtitle=str(fm.get("subtitle") or ""),
            metadata=fm,
            out_svg=site_root / "static" / "covers" / f"{bid}.svg",
            out_webp=site_root / "static" / "covers" / f"{bid}.webp",
        )
        fm.update({
            "edition_generation": "v1",
            "edition_tier": "v1_archive",
            "cover": f"/covers/{bid}.webp",
            "cover_svg": f"/covers/{bid}.svg",
            "archetype": cov["archetype"],
            "palette": cov["palette"],
        })
        if not fm.get("chapters"):
            fm["chapters"] = max(1, len(list(bdir.glob("*.md"))) - 1)
        (bdir / "_index.md").write_text(dump_hugo_frontmatter_md(fm, body), encoding="utf-8")
        all_site_books.append({
            "book_id": bid,
            "title": str(fm.get("title") or bid),
            "author": author,
            "author_slug": aslug,
            "year": yr,
            "archetype": cov["archetype"],
            "collection": "general-heritage",
            "tier": "v1_archive",
        })

    # 6. Merge compiled tables_atlas files into site static/data & data/
    merged_atlas: list[dict[str, Any]] = []
    for atlas_path in sorted((pipeline_root / "library").glob("*/tables_atlas.json")):
        for entry in json.loads(atlas_path.read_text(encoding="utf-8")).get("tables") or []:
            e_bid = str(entry.get("book_id") or "")
            if e_bid not in v6_ids:
                continue
            item = dict(entry)
            item["reader_url"] = _rewrite_atlas_reader_url(str(item.get("reader_url") or ""), chap_slug_map)
            for k in ("diplomatic_csv_url", "tidy_csv_url"):
                val = str(item.get(k) or "")
                if val.startswith(f"{e_bid}/"):
                    item[k] = f"/downloads/{val}"
            merged_atlas.append(item)

    atlas_out = {"version": "tables-atlas-site-v1", "total_tables": len(merged_atlas), "tables": merged_atlas}
    for atlas_dst in (site_root / "static" / "data" / "tables_atlas.json", site_root / "data" / "tables_atlas.json"):
        atlas_dst.parent.mkdir(parents=True, exist_ok=True)
        atlas_dst.write_text(json.dumps(atlas_out, indent=2), encoding="utf-8")

    # 7. Sync curated collections
    col_dir = site_root / "content" / "collections"
    col_dir.mkdir(parents=True, exist_ok=True)
    defined_slugs = {c["slug"] for c in COLLECTION_DEFINITIONS}
    for existing in col_dir.glob("*.md"):
        if existing.stem != "_index" and existing.stem not in defined_slugs:
            existing.unlink()

    all_ids = {b["book_id"] for b in all_site_books}
    for cdef in COLLECTION_DEFINITIONS:
        matched = sorted({
            b["book_id"]
            for b in all_site_books
            if (b["archetype"] in cdef["match_archetypes"] or b["book_id"] in cdef["extra_books"]) and b["book_id"] in all_ids
        })
        mset = set(matched)
        years = [int(b["year"]) for b in all_site_books if b["book_id"] in mset and isinstance(b.get("year"), int)]
        authors_in_col = {b["author_slug"] for b in all_site_books if b["book_id"] in mset}
        cfm = {
            "title": cdef["title"],
            "type": "collections",
            "book_count": len(matched),
            "author_count": len(authors_in_col),
            "earliest_year": min(years) if years else 1800,
            "latest_year": max(years) if years else 1939,
            "description": cdef["description"],
            "period": cdef["period"],
            "books": matched,
        }
        cbody = f"{cdef['description']}\n\nThis curated shelf brings together {len(matched)} public-domain editions across Akshara."
        (col_dir / f"{cdef['slug']}.md").write_text(dump_hugo_frontmatter_md(cfm, cbody), encoding="utf-8")

    # 8. Update author works_count while preserving existing bios
    authors_dir = site_root / "content" / "authors"
    authors_dir.mkdir(parents=True, exist_ok=True)
    for aslug, cnt in sorted(author_counts.items()):
        apath = authors_dir / f"{aslug}.md"
        if apath.is_file():
            afm, abody = _parse_frontmatter(apath.read_text(encoding="utf-8"), yaml)
            afm["works_count"] = cnt
            afm.setdefault("slug", aslug)
            if not afm.get("first_publication") and aslug in author_first_pub:
                afm["first_publication"] = author_first_pub[aslug]
            apath.write_text(dump_hugo_frontmatter_md(afm, abody), encoding="utf-8")
        else:
            disp = author_names.get(aslug) or aslug.replace("-", " ").title()
            afm = {
                "title": disp,
                "slug": aslug,
                "short_bio": f"Author of {cnt} historical work(s) preserved in the Akshara Public Domain Archive.",
                "works_count": cnt,
                "first_publication": author_first_pub.get(aslug, ""),
            }
            apath.write_text(dump_hugo_frontmatter_md(afm, f"{disp} authored works preserved in Project Akshara's public-domain digital library."), encoding="utf-8")

    # 9. Write akshara_library root files & dynamic GitHub release helper
    (library_root / "LICENSE").write_text(
        "Creative Commons Attribution 4.0 International (CC BY 4.0)\n\n"
        "The original source books digitized in Akshara are in the public domain. What Akshara adds — "
        "transcriptions, corrections, structure, XML/Markdown/HTML/EPUB formatting, and extracted statistical "
        "CSV datasets — is licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), "
        "crediting Akshara (akshara.ink).\n",
        encoding="utf-8",
    )
    (library_root / "catalog.json").write_text(
        json.dumps({"version": "akshara-library-v1", "book_count": len(catalog_books), "total_tables": total_tables, "books": catalog_books}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    readme_lines = [
        "# Akshara Public-Domain Digital Library (`akshara-library`)",
        "",
        f"**{len(catalog_books)} full scholarly editions · {total_tables} structured CSV/JSON statistical tables · CC BY 4.0**",
        "",
        "Every edition in this repository is compiled from camera-original Archive.org JP2 scans with 100% diplomatic orthographic fidelity.",
        "",
        "## Per-Book Folder Structure",
        "",
        "```text",
        "collections/<collection>/<book_id>/",
        "  README.md              # Overview & direct release links",
        "  EDITORIAL_NOTE.md      # Source scan SHA-256 & normalization policy",
        "  EDITION_REPORT.md      # 100-point rubric breakdown & validator telemetry",
        "  PROOFING_BRIEFING.md   # Open items for community proofreaders",
        "  edition_manifest.json  # Machine metadata & provenance tags",
        "  cover.svg / cover.webp # Contextual series cover",
        "  epub/<book_id>.epub    # Typeset EPUB 3",
        "  html/<book_id>.html    # Single-page Gutenberg-style HTML",
        "  markdown/<book_id>.md  # Scholarly Markdown",
        "  tei/<book_id>.tei.xml  # TEI P5 XML archival master",
        "  figures/*.webp         # Cropped plates & maps",
        "  datasets/              # Diplomatic 2D + Tidy CSV/JSON tables",
        "```",
        "",
        "Heavy Print PDFs and de-blotted `.originals.pdf` camera scan backups live under GitHub Releases (`edition-<book_id>`).",
        "",
        "## Complete Catalog",
        "",
        "| Title | Author(s) | Year | Tier | Rubric | Tables |",
        "| :--- | :--- | :---: | :--- | ---: | ---: |",
    ]
    for b in sorted(catalog_books, key=lambda x: str(x["title"]).lower()):
        readme_lines.append(
            f"| [{b['title']}]({b['path']}/README.md) | {', '.join(b['authors'])} | {b['publication_year'] or 'PD'} | "
            f"`{b['edition_tier']}` | {b['rubric_score']:.1f} | {b['tables_count']} |"
        )
    (library_root / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

    helper_path = library_root / "scripts" / "publish_github_releases.py"
    helper_path.parent.mkdir(parents=True, exist_ok=True)
    helper_path.write_text(_RELEASE_HELPER_TEMPLATE, encoding="utf-8")
    os.chmod(helper_path, 0o755)

    print(
        json.dumps(
            {
                "v6_books": len(catalog_books),
                "v1_books": v1_count,
                "total_site_books": len(all_site_books),
                "total_v6_pages": total_v6_pages,
                "total_tables": total_tables,
                "total_tidy_observations": total_tidy_obs,
                "authors_updated": len(author_counts),
                "collections": len(COLLECTION_DEFINITIONS),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
