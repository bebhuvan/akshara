"""Automated SEO and GEO (Generative Engine Optimization) regression tests on public/.
Run via ./verify or: python3 -m unittest tests/test_seo_geo.py"""
from collections import Counter
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"


def iter_real_pages():
    for p in sorted(PUBLIC.rglob("*.html")):
        if any(x in p.parts for x in ("pagefind", "downloads")):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "http-equiv=refresh" in text or 'http-equiv="refresh"' in text:
            continue
        rel = "/" + str(p.relative_to(PUBLIC)).replace("index.html", "")
        is_noindex = bool(re.search(r'<meta\s+name="?robots"?\s+content="[^"]*noindex', text))
        yield rel, text, is_noindex


@unittest.skipUnless((PUBLIC / "index.html").exists(), "the site is not built")
class TechnicalSeoAndStructuredData(unittest.TestCase):
    def test_every_indexable_page_has_unique_title_and_clean_description(self):
        titles = Counter()
        descs = Counter()
        for rel, html, is_noindex in iter_real_pages():
            if is_noindex:
                continue
            tm = re.search(r"<title>(.*?)</title>", html, re.S)
            self.assertIsNotNone(tm, f"missing <title> on {rel}")
            title = tm.group(1).strip()
            self.assertTrue(title, f"empty <title> on {rel}")
            titles[title] += 1

            dm = re.search(r'<meta name="?description"? content=(".*?"|\'.*?\'|[^\s>]+)', html, re.S)
            self.assertIsNotNone(dm, f"missing description on {rel}")
            desc = dm.group(1).strip("\"'")
            self.assertGreaterEqual(len(desc), 40, f"short description on {rel}: {desc!r}")
            self.assertNotIn("Archival scope:", desc, f"raw pipeline boilerplate in description on {rel}")
            self.assertNotIn("[p.", desc, f"raw folio artifact in description on {rel}")
            descs[desc] += 1

        dup_titles = {k: v for k, v in titles.items() if v > 1}
        dup_descs = {k: v for k, v in descs.items() if v > 1}
        self.assertEqual(dup_titles, {}, f"duplicate <title> values found: {dup_titles}")
        self.assertEqual(dup_descs, {}, f"duplicate <meta description> values found: {dup_descs}")

    def test_every_page_has_exactly_one_h1(self):
        for rel, html, _ in iter_real_pages():
            h1s = re.findall(r"<h1\b", html)
            self.assertEqual(len(h1s), 1, f"{rel} has {len(h1s)} <h1> tags")

    def test_every_indexable_page_has_valid_jsonld(self):
        for rel, html, is_noindex in iter_real_pages():
            blocks = re.findall(r'<script type="?application/ld\+json"?>(.*?)</script>', html, re.S)
            if is_noindex:
                continue
            self.assertTrue(blocks, f"missing JSON-LD on {rel}")
            for raw in blocks:
                data = json.loads(raw)
                self.assertEqual(data.get("@context"), "https://schema.org", rel)
                self.assertIsInstance(data.get("@graph"), list, rel)

    def test_books_emit_book_schema_citations_and_datasets(self):
        book_pages = [
            (rel, html) for rel, html, is_noindex in iter_real_pages()
            if not is_noindex and rel.startswith("/books/") and rel.count("/") == 3
        ]
        self.assertGreaterEqual(len(book_pages), 60)
        dataset_books = 0
        for rel, html in book_pages:
            self.assertIn("citation_title", html, rel)
            self.assertIn("DC.title", html, rel)
            block = re.search(r'<script type="?application/ld\+json"?>(.*?)</script>', html, re.S)
            self.assertIsNotNone(block, rel)
            graph = json.loads(block.group(1))["@graph"]
            types = {node.get("@type") for node in graph if isinstance(node.get("@type"), str)}
            self.assertIn("Book", types, rel)
            self.assertIn("BreadcrumbList", types, rel)
            if "Dataset" in types:
                dataset_books += 1
        self.assertGreaterEqual(dataset_books, 40)

    def test_datasets_hub_emits_master_dataset_schema(self):
        html = (PUBLIC / "datasets/index.html").read_text(encoding="utf-8")
        block = re.search(r'<script type="?application/ld\+json"?>(.*?)</script>', html, re.S)
        self.assertIsNotNone(block)
        graph = json.loads(block.group(1))["@graph"]
        ds = [n for n in graph if n.get("@type") == "Dataset"]
        self.assertEqual(len(ds), 1)
        self.assertGreaterEqual(len(ds[0].get("hasPart", [])), 40)

    def test_sitemap_has_lastmod_and_excludes_utility_pages(self):
        tree = ET.parse(PUBLIC / "sitemap.xml")
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = tree.findall("sm:url", ns)
        self.assertGreater(len(urls), 1000)
        for u in urls:
            loc = u.findtext("sm:loc", default="", namespaces=ns)
            lm = u.findtext("sm:lastmod", default="", namespaces=ns)
            self.assertNotIn("/search/", loc)
            self.assertNotIn("/withdrawn/", loc)
            self.assertTrue(lm and not lm.startswith("0001"), f"invalid lastmod on {loc}: {lm!r}")
            self.assertIsNone(u.find("sm:priority", ns), f"unexpected priority on {loc}")

    def test_rss_feed_has_real_dates_and_items(self):
        tree = ET.parse(PUBLIC / "index.xml")
        ch = tree.find("channel")
        self.assertIsNotNone(ch)
        last_build = ch.findtext("lastBuildDate", "")
        self.assertNotIn("0001", last_build)
        items = ch.findall("item")
        self.assertGreaterEqual(len(items), 10)
        for it in items:
            self.assertNotIn("0001", it.findtext("pubDate", ""))

    def test_headers_prevent_downloads_cannibalization(self):
        headers = (PUBLIC / "_headers").read_text(encoding="utf-8")
        self.assertIn("X-Robots-Tag: noindex, follow", headers)
        self.assertIn("</llms.txt>; rel=\"describedby\"", headers)

    def test_github_page_is_not_empty(self):
        html = (PUBLIC / "github/index.html").read_text(encoding="utf-8")
        self.assertIn("akshara-library", html)
        self.assertIn("/llms.txt", html)


@unittest.skipUnless((PUBLIC / "index.html").exists(), "the site is not built")
class GenerativeEngineOptimization(unittest.TestCase):
    def test_llms_txt_and_full_and_catalog_json_exist_and_cover_all_books(self):
        llms = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
        llms_full = (PUBLIC / "llms-full.txt").read_text(encoding="utf-8")
        catalog = json.loads((PUBLIC / "catalog.json").read_text(encoding="utf-8"))

        self.assertIn("# Akshara", llms)
        self.assertIn("#p-<folio>", llms)
        self.assertIn("https://akshara.ink/llms-full.txt", llms)
        self.assertIn("https://akshara.ink/catalog.json", llms)
        self.assertGreater(len(llms_full), 100_000)

        book_count = len(list((ROOT / "content/books").glob("*/_index.md")))
        self.assertEqual(len(catalog["books"]), book_count)
        self.assertEqual(catalog["stats"]["books"], book_count)
        self.assertGreaterEqual(catalog["stats"]["tables"], 1300)

    def test_robots_txt_allows_ai_search_bots_and_blocks_pagefind(self):
        robots = (PUBLIC / "robots.txt").read_text(encoding="utf-8")
        for bot in ("OAI-SearchBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended"):
            self.assertIn(bot, robots)
        self.assertIn("Disallow: /pagefind/", robots)
        self.assertIn("Sitemap: https://akshara.ink/sitemap.xml", robots)

    def test_indexnow_key_file_is_served(self):
        key_file = PUBLIC / "a7c4e91f2b8d4036e5a1f8c3d9b2074e.txt"
        self.assertTrue(key_file.is_file())
        self.assertEqual(key_file.read_text(encoding="utf-8").strip(), "a7c4e91f2b8d4036e5a1f8c3d9b2074e")

    def test_content_signal_api_catalog_opensearch_and_webmcp(self):
        robots = (PUBLIC / "robots.txt").read_text(encoding="utf-8")
        headers = (PUBLIC / "_headers").read_text(encoding="utf-8")
        self.assertIn("Content-Signal: search=yes, ai-input=yes, ai-train=yes", robots)
        self.assertIn("Content-Signal: search=yes, ai-input=yes, ai-train=yes", headers)
        self.assertIn('</.well-known/api-catalog>; rel="api-catalog"', headers)

        api_cat = json.loads((PUBLIC / ".well-known/api-catalog").read_text(encoding="utf-8"))
        self.assertIn("linkset", api_cat)
        self.assertGreaterEqual(len(api_cat["linkset"]), 3)

        os_xml = ET.parse(PUBLIC / "opensearch.xml")
        self.assertIn("searchTerms", ET.tostring(os_xml.getroot(), encoding="unicode"))

        lib_html = (PUBLIC / "books/index.html").read_text(encoding="utf-8")
        self.assertIn("toolname=search_akshara_library", lib_html)

    def test_image_sitemap_and_plates_imageobject_and_lcp_preload(self):
        sm = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("http://www.google.com/schemas/sitemap-image/1.1", sm)
        self.assertGreaterEqual(sm.count("<image:image>"), 100)

        plates_html = (PUBLIC / "plates/index.html").read_text(encoding="utf-8")
        block = re.search(r'<script type="?application/ld\+json"?>(.*?)</script>', plates_html, re.S)
        graph = json.loads(block.group(1))["@graph"]
        gallery = [n for n in graph if n.get("@type") == "ImageGallery"][0]
        self.assertGreaterEqual(len(gallery.get("associatedMedia", [])), 20)

        home_html = (PUBLIC / "index.html").read_text(encoding="utf-8")
        self.assertRegex(home_html, r'<link rel=preload as=image href=/plates/[^>]+fetchpriority=high')

    def test_author_wikidata_sameas_coins_and_sibling_crosslinks(self):
        author_pages = list((PUBLIC / "authors").glob("*/index.html"))
        with_wikidata = 0
        for p in author_pages:
            txt = p.read_text(encoding="utf-8")
            if "https://www.wikidata.org/entity/Q" in txt:
                with_wikidata += 1
        self.assertGreaterEqual(with_wikidata, 30)

        vol1 = (PUBLIC / "books/english-factories-india-1618-1621-vol-01/index.html").read_text(encoding="utf-8")
        self.assertIn("Z3988", vol1)
        self.assertIn("/books/english-factories-india-1622-1623-vol-02/", vol1)
