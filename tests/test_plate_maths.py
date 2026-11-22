"""Tests for the deciding half of scripts/make_plates.py. Run: python3 -m unittest discover -s tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import plate_maths as pm  # noqa: E402


def entry(**over):
    p = {"key": "x-a", "book": "b", "source": "static/figures/b/f.webp", "what": "a map", "mode": "line",
         "crop": [0.1, 0.1, 0.9, 0.9]}
    p.update(over)
    return p


class Entries(unittest.TestCase):
    def test_a_good_entry_passes(self):
        pm.check_entry(entry())

    def test_missing_fields_impossible_crops_and_levels_are_refused(self):
        for bad in (entry(what=""), entry(mode="sepia"), entry(crop=[0.5, 0, 0.4, 1]),
                    entry(crop=[0, 0, 1, 1.2]), entry(levels=[200, 100])):
            with self.assertRaises(ValueError):
                pm.check_entry(bad)

    def test_a_plate_made_by_hand_needs_no_crop(self):
        pm.check_entry({"key": "x", "book": "b", "source": "s", "what": "w", "made": "by hand"})


class Geometry(unittest.TestCase):
    def test_crop_box_turns_fractions_into_pixels(self):
        self.assertEqual(pm.crop_box((1000, 500), [0.1, 0.2, 0.9, 1.0]), (100, 100, 900, 500))

    def test_fit_long_side_shrinks_but_never_enlarges(self):
        self.assertEqual(pm.fit_long_side((2800, 1400), 1400), (1400, 700))
        self.assertEqual(pm.fit_long_side((600, 300), 1400), (600, 300))


class Levels(unittest.TestCase):
    def test_line_plates_put_white_below_the_paper_and_black_near_the_line(self):
        hist = [0] * 256
        hist[20] = 5       # the darkest line
        hist[230] = 95     # paper
        black, white = pm.auto_levels(hist, "line")
        self.assertLess(black, white)
        self.assertLessEqual(white, 230)
        self.assertGreaterEqual(white - black, 30)

    def test_level_table_maps_black_and_white_to_the_ends(self):
        t = pm.level_table(50, 200)
        self.assertEqual((t[0], t[50], t[200], t[255]), (0, 0, 255, 255))


class Hosts(unittest.TestCase):
    def test_only_archive_org_and_its_own_servers(self):
        self.assertTrue(pm.archive_host_ok("https://archive.org/download/x/page/n1.jpg"))
        self.assertTrue(pm.archive_host_ok("https://ia800300.us.archive.org/1/items/x/n1.jpg"))
        self.assertFalse(pm.archive_host_ok("http://archive.org/download/x/page/n1.jpg"))
        self.assertFalse(pm.archive_host_ok("https://archive.org.example.com/x.jpg"))
        self.assertFalse(pm.archive_host_ok("https://example.com/archive.org/x.jpg"))
