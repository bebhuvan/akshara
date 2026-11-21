"""Tests of the built site in public/ (./verify builds it before running the tests). Skipped if it is not built.
Run: python3 -m unittest discover -s tests"""
import re
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"


@unittest.skipUnless((PUBLIC / "index.html").exists(), "the site is not built")
class OpeningPage(unittest.TestCase):
    def setUp(self):
        self.html = (PUBLIC / "index.html").read_text(encoding="utf-8")

    def test_new_on_the_shelves_shows_four_books_from_four_shelves(self):
        # It once took only the books added on the latest date, so one book added alone would stand by itself.
        section = re.search(r'id="?h-new"?.*?</section>', self.html, re.S).group(0)
        shelves = re.findall(r'class="?book ([a-z]{2})"?', section)
        wanted = min(4, len(tomllib.loads((ROOT / "data/shelves.toml").read_text(encoding="utf-8"))["shelf"]))
        self.assertEqual(len(shelves), wanted)
        self.assertEqual(len(set(shelves)), len(shelves))

    def test_the_turning_plate_can_be_paused(self):
        self.assertIn("data-turn-pause", self.html)


@unittest.skipUnless((PUBLIC / "books/index.html").exists(), "the site is not built")
class SearchMetadata(unittest.TestCase):
    def test_book_and_shelf_are_separate_fields(self):
        # Pagefind splits a meta value at commas: "book:X, shelf:y" once put the shelf into every title.
        page = next((PUBLIC / "books").glob("*/index.html")).read_text(encoding="utf-8")
        self.assertRegex(page, r'data-pagefind-meta="?book"?')
        self.assertNotRegex(page, r'data-pagefind-meta="?book:')


@unittest.skipUnless((PUBLIC / "books/index.html").exists(), "the site is not built")
class HowTheTextWasRead(unittest.TestCase):
    def book_pages(self):
        # a book's old addresses are tiny redirect pages; only real book pages count
        return [p for p in (PUBLIC / "books").glob("*/index.html") if "http-equiv=refresh" not in p.read_text(encoding="utf-8")]

    def test_every_book_page_says_how_its_text_was_read(self):
        for page in self.book_pages():
            html = page.read_text(encoding="utf-8")
            self.assertRegex(html, r'id="?h-reading"?', page)
            self.assertIn("What a machine reading can get wrong", html, page)

    def test_every_score_in_the_records_is_shown(self):
        for record in (ROOT / "content/books").glob("*/_index.md"):
            m = re.search(r"^rubric_score:\s*([0-9.]+)", record.read_text(encoding="utf-8"), re.M)
            if not m or 'edition_tier: "v1_archive"' in record.read_text(encoding="utf-8"):
                continue
            html = (PUBLIC / "books" / record.parent.name / "index.html").read_text(encoding="utf-8")
            self.assertRegex(html, r'class="?rd-n"?><b>%d</b>' % round(float(m.group(1))), record)

    def test_checker_findings_are_put_in_plain_words(self):
        # The checker writes "-3.0: 1 unresolved footnote callout/body mismatch(es)"; a reader should never see that.
        for page in self.book_pages():
            for found in re.findall(r'class="?pl-found"?>([^<]*)', page.read_text(encoding="utf-8")):
                self.assertNotRegex(found, r"\(s\)|\(es\)|\(ies\)|^-?\d+\.\d+:|unclear", page)

    def test_chapters_point_to_the_account(self):
        chapter = next((PUBLIC / "books").glob("*/chapters/*/index.html")).read_text(encoding="utf-8")
        self.assertIn("#h-reading", chapter)
