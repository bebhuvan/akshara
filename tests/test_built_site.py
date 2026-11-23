"""Tests of the built site in public/ (./verify builds it before running the tests). Skipped if it is not built.
Run: python3 -m unittest discover -s tests"""
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
import html
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
            # the vision-language model's quirks are told only for books it read; Stage One books were made
            # by OCR or an earlier reading and get their own account (review 0003, finding 4)
            stage_one = "An earlier edition, read by machine" in html
            self.assertEqual("The quirks of a machine reading" in html, not stage_one, page)

    def test_every_score_in_the_records_is_shown(self):
        for record in (ROOT / "content/books").glob("*/_index.md"):
            m = re.search(r"^rubric_score:\s*([0-9.]+)", record.read_text(encoding="utf-8"), re.M)
            if not m or 'edition_tier: "v1_archive"' in record.read_text(encoding="utf-8"):
                continue
            html = (PUBLIC / "books" / record.parent.name / "index.html").read_text(encoding="utf-8")
            # Hugo's math.Round rounds half away from zero, unlike Python's round-half-to-even.
            shown = int(Decimal(m.group(1)).to_integral_value(rounding=ROUND_HALF_UP))
            self.assertRegex(html, r'class="?rd-n"?><b>%d</b>' % shown, record)

    def test_checker_findings_are_put_in_plain_words(self):
        # The checker writes "-3.0: 1 unresolved footnote callout/body mismatch(es)"; a reader should never see that.
        for page in self.book_pages():
            for found in re.findall(r'class="?pl-found"?>([^<]*)', page.read_text(encoding="utf-8")):
                self.assertNotRegex(found, r"\(s\)|\(es\)|\(ies\)|^-?\d+\.\d+:|unclear", page)

    def test_chapters_point_to_the_account(self):
        chapter = next((PUBLIC / "books").glob("*/chapters/*/index.html")).read_text(encoding="utf-8")
        self.assertIn("#h-reading", chapter)

    def lede(self, html):
        m = re.search(r'class="?rd-lede"?>(.*?)</p>', html, re.S)
        return m.group(1) if m else ""

    def test_the_account_claims_no_more_than_the_record(self):
        # It once told every book its text was "checked against the scans" and its errors "few and small",
        # beside records saying no page was re-read and 38 items were open (review 0003, finding 2).
        for record in (ROOT / "content/books").glob("*/_index.md"):
            text = record.read_text(encoding="utf-8")
            page = PUBLIC / "books" / record.parent.name / "index.html"
            if not page.exists():
                continue
            lede = self.lede(page.read_text(encoding="utf-8"))
            self.assertNotIn("checked against the scans", lede, record)
            m = re.search(r"^rubric_score:\s*([0-9.]+)", text, re.M)
            if m and float(m.group(1)) < 95:
                self.assertNotIn("few and small", lede, record)

    def test_a_score_among_the_facts_cannot_be_read_as_proofread(self):
        for page in self.book_pages():
            for label in re.findall(r'class="?fact-score"?.*?<span>([^<]*)</span>', page.read_text(encoding="utf-8")):
                self.assertIn("automatic checks", label, page)


@unittest.skipUnless((PUBLIC / "books/index.html").exists(), "the site is not built")
class SearchAndPages(unittest.TestCase):
    def test_title_and_author_are_not_indexed_as_words_of_every_chapter(self):
        # Searching "Foster" once returned 411 pages, every chapter of his own volumes (review 0003, finding 3).
        chapter = next((PUBLIC / "books").glob("*/chapters/*/index.html")).read_text(encoding="utf-8")
        for field in ("book", "author"):
            tag = re.search(r'<span[^>]*data-pagefind-meta="?%s"?[^>]*>' % field, chapter).group(0)
            self.assertIn("data-pagefind-ignore", tag)

    def test_each_printed_page_can_be_linked_to(self):
        # A living book's note opens an edition at the page it quotes: #p-<folio>.
        chapter = next(iter(sorted((PUBLIC / "books/journey-from-madras-vol-i/chapters").glob("04-*/index.html"))))
        html = chapter.read_text(encoding="utf-8")
        self.assertRegex(html, r'id="?p-1"?')
        ids = re.findall(r'id="?(p-[0-9ivxlcdm]+)"?', html)
        self.assertEqual(len(ids), len(set(ids)), "a page target appears twice")



@unittest.skipUnless((PUBLIC / "blog/index.html").exists(), "the site is not built")
class JournalEssay(unittest.TestCase):
    def setUp(self):
        self.html = (PUBLIC / "blog/akshara-take-two/index.html").read_text(encoding="utf-8")
        self.journal = tomllib.loads((ROOT / "data/journal.toml").read_text(encoding="utf-8"))

    def test_the_older_essay_is_labelled_earlier(self):
        # The labels were swapped: the 2025 essay was offered as "Later" under the 2026 one.
        foot = self.html[self.html.index('aria-label=Journal'):]
        self.assertRegex(foot, r"<small>Earlier</small><b>Introducing Akshara</b>")
        self.assertNotIn("<small>Later</small>", foot)

    def test_byline_names_the_writer_and_reading_time(self):
        self.assertRegex(self.html, r"By Bhuvan .*?\d+ minutes")

    def test_pull_quotes_are_the_essays_own_words_and_hidden_from_screen_readers(self):
        pulls = re.findall(r'<figure class=pull aria-hidden=true><blockquote><p>(.*?)</p>', self.html)
        expected = self.journal["akshara-take-two"]["pull"]
        self.assertEqual(len(pulls), len(expected))
        body = html.unescape(re.sub(r'<figure class=pull.*?</figure>', "", self.html))
        for s in expected:
            self.assertIn(s, body, "a pull quote must be a sentence the essay itself contains")

    def test_books_the_essay_names_are_shown(self):
        for book in self.journal["akshara-take-two"]["books"]:
            self.assertIn(f'href=/books/{book}/', self.html)

    def test_a_pull_quote_never_sits_against_a_section_break(self):
        self.assertNotRegex(self.html, r"</figure>\s*<hr")


ATTR = r'="?([^"\s>]+)'


@unittest.skipUnless((PUBLIC / "index.html").exists(), "the site is not built")
class WholeBook(unittest.TestCase):
    """The whole book on one page (D37), made from the chapter pages."""

    def pages(self):
        return sorted((PUBLIC / "books").glob("*/whole/index.html"))

    def test_every_book_with_chapters_has_one(self):
        books = {d.name for d in (ROOT / "content/books").iterdir()
                 if d.is_dir() and any(f.name != "_index.md" for f in d.rglob("*.md"))}
        self.assertEqual({p.parent.parent.name for p in self.pages()}, books)

    def test_ids_from_different_chapters_never_collide(self):
        for page in self.pages():
            ids = re.findall(r"\sid" + ATTR, page.read_text(encoding="utf-8"))
            dup = sorted(k for k, v in Counter(ids).items() if v > 1)
            self.assertEqual(dup, [], page)

    def test_contents_and_links_between_chapters_stay_on_the_page(self):
        page = (PUBLIC / "books/palas-of-bengal/whole/index.html").read_text(encoding="utf-8")
        ids = set(re.findall(r"\sid" + ATTR, page))
        for n in range(1, 13):
            self.assertIn(f"c{n}", ids)
        self.assertNotRegex(page, r'href="?/books/palas-of-bengal/chapters/[^"\s>]*#')
        notes = re.findall(r'href="?#(c\d+-sec-[^"\s>]+)', page)
        self.assertTrue(notes)
        self.assertEqual([n for n in notes if n not in ids], [])

    def test_it_is_not_indexed_for_search_twice(self):
        for page in self.pages():
            self.assertNotIn("data-pagefind-body", page.read_text(encoding="utf-8"), page)

    def test_the_book_page_offers_it(self):
        book = (PUBLIC / "books/palas-of-bengal/index.html").read_text(encoding="utf-8")
        self.assertRegex(book, r'href="?/books/palas-of-bengal/whole/"?[^>]*><span>Read it whole')


@unittest.skipUnless((PUBLIC / "index.html").exists(), "the site is not built")
class TheOriginal(unittest.TestCase):
    """The Internet Archive's reader on a book's page, loaded only when asked (D38)."""

    def setUp(self):
        self.html = (PUBLIC / "books/palas-of-bengal/index.html").read_text(encoding="utf-8")

    def test_nothing_is_fetched_from_archive_org_until_asked(self):
        self.assertNotIn("<iframe", self.html)
        self.assertRegex(self.html, r'href="?https://archive.org/details/cu31924096224476"?[^>]*data-ia=')

    def test_the_identifiers_are_the_records_own(self):
        self.assertIn("1f1fb550222e61521e2de3820b498d44dbf6d94bc234071682e0e2e36736f225", self.html)
        self.assertIn("126, 105 of them with text", self.html)

    def test_the_one_page_file_says_what_it_is(self):
        self.assertIn("a single web page you can save and read offline", self.html)


class ReadingType(unittest.TestCase):
    """A face a reader has not chosen is never fetched: Clear and Plain are named only under [data-type] (D36)."""

    def test_clear_and_plain_are_used_only_when_chosen(self):
        css = (ROOT / "assets/css/plate.css").read_text(encoding="utf-8")
        for face in ("--clear", "--plain"):
            uses = [ln for ln in css.splitlines() if f"var({face})" in ln]
            self.assertTrue(uses)
            for ln in uses:
                self.assertIn("[data-type=", ln)

    @unittest.skipUnless((PUBLIC / "index.html").exists(), "the site is not built")
    def test_small_capitals_given_in_capitals_are_set_wholly_small(self):
        chapter = next((PUBLIC / "books/palas-of-bengal/chapters").glob("03-*/index.html")).read_text(encoding="utf-8")
        self.assertRegex(chapter, r'class="?sc sc-caps"?>A\. ?D\.')

    @unittest.skipUnless((PUBLIC / "index.html").exists(), "the site is not built")
    def test_heading_footnote_backlinks_resolve_everywhere(self):
        for page in list((PUBLIC / "books").glob("*/chapters/*/index.html")) + list((PUBLIC / "books").glob("*/whole/index.html")):
            html_txt = page.read_text(encoding="utf-8")
            refs = re.findall(r'href="?#((?:c\d+-)?ref-sec-[^"\s>]+)', html_txt)
            if refs:
                ids = set(re.findall(r"\sid" + ATTR, html_txt))
                missing = [r for r in refs if r not in ids]
                self.assertEqual(missing, [], page)

    @unittest.skipUnless((PUBLIC / "index.html").exists(), "the site is not built")
    def test_chapter_titles_never_start_with_stray_comma(self):
        for bid in ("comprehensive-history-india-v1", "comprehensive-history-india-v2"):
            for page in (PUBLIC / "books" / bid / "chapters").glob("*/index.html"):
                html_txt = page.read_text(encoding="utf-8")
                self.assertNotRegex(html_txt, r"<h1\b[^>]*>\s*,")
                self.assertNotRegex(html_txt, r"<title>[^<]*:\s*,")

