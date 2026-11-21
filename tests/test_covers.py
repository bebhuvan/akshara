"""Tests for the cover check. Run: python3 -m unittest discover -s tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_covers  # noqa: E402

BOOKS = {"vol-1", "vol-2", "plain"}
PROVENANCE = {"v1-map": "vol-1", "v2-arms": "vol-2"}
FILES = {"v1-map", "v2-arms"}


def good():
    return {
        "vol-1": {"kind": "map", "plate": "v1-map"},
        "vol-2": {"kind": "device", "plate": "v2-arms"},
        "plain": {"kind": "type", "why": "nothing pictorial in the book"},
    }


class Covers(unittest.TestCase):
    def test_good_covers_pass(self):
        self.assertEqual(check_covers.problems(good(), BOOKS, PROVENANCE, FILES), [])

    def test_picture_from_another_volume_is_refused(self):
        covers = good()
        covers["vol-2"] = {"kind": "map", "plate": "v1-map"}
        found = check_covers.problems(covers, BOOKS, PROVENANCE, FILES)
        self.assertEqual(found, ["vol-2: plate v1-map comes from vol-1, not from this book"])

    def test_plate_without_a_recorded_book_is_refused(self):
        covers = good()
        covers["vol-1"]["plate"] = "stray"
        found = check_covers.problems(covers, BOOKS, PROVENANCE, FILES | {"stray"})
        self.assertIn("vol-1: nothing records which book plate stray came from", found)

    def test_missing_file_and_missing_cover(self):
        covers = good()
        del covers["plain"]
        found = check_covers.problems(covers, BOOKS, PROVENANCE, {"v2-arms"})
        self.assertIn("plain has no cover in data/covers.toml", found)
        self.assertIn("vol-1: plate v1-map is not in static/plates/", found)

    def test_kinds_and_type_rules(self):
        covers = good()
        covers["vol-1"]["kind"] = "woodcut"
        covers["plain"] = {"kind": "type", "plate": "v1-map"}
        found = check_covers.problems(covers, BOOKS, PROVENANCE, FILES)
        self.assertTrue(any("kind 'woodcut'" in f for f in found))
        self.assertIn("plain: a type-only cover takes no plate", found)
        self.assertIn("plain: a type-only cover says why there is no picture (why = ...)", found)

    def test_cover_for_a_book_that_does_not_exist(self):
        covers = good()
        covers["gone"] = {"kind": "type", "why": "x"}
        self.assertIn("data/covers.toml has a cover for gone, which is not a book",
                      check_covers.problems(covers, BOOKS, PROVENANCE, FILES))

    def test_provenance_merges_both_records(self):
        plates = {"group": [{"plate": [{"key": "a", "book": "b1"}]}]}
        sources = {"plate": [{"key": "c", "book": "b2"}]}
        self.assertEqual(check_covers.plate_books(plates, sources), {"a": "b1", "c": "b2"})
