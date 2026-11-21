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
