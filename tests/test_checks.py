"""Tests for the build checks. Run: python3 -m unittest discover -s tests"""
import base64
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_content  # noqa: E402
import check_styles  # noqa: E402
import check_urls  # noqa: E402


def site(files: dict[str, str]) -> Path:
    root = Path(tempfile.mkdtemp())
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root


class Urls(unittest.TestCase):
    def test_normalise_adds_trailing_slash_to_pages_only(self):
        self.assertEqual(check_urls.normalise("/books/x"), "/books/x/")
        self.assertEqual(check_urls.normalise("/books/x/"), "/books/x/")
        self.assertEqual(check_urls.normalise("/index.xml"), "/index.xml")

    def test_redirect_rules_are_read(self):
        root = site({"_redirects": "# note\n/old/ /new/ 301\n/old /new/ 301\n"})
        self.assertEqual(check_urls.read_redirects(root), {"/old/": "/new/"})

    def test_malformed_redirect_stops_the_build(self):
        for bad in ("/old/ /new/", "/old/* /new/ 301", "/old/ /new/ 302", "/a/ /b/ 301 extra"):
            root = site({"_redirects": bad + "\n"})
            with self.assertRaises(SystemExit, msg=bad):
                check_urls.read_redirects(root)

    def test_rule_without_slashless_twin_stops_the_build(self):
        root = site({"_redirects": "/old/ /new/ 301\n"})
        with self.assertRaises(SystemExit):
            check_urls.read_redirects(root)

    def test_has_page(self):
        root = site({"index.html": "", "books/x/index.html": ""})
        self.assertTrue(check_urls.has_page(root, "/"))
        self.assertTrue(check_urls.has_page(root, "/books/x/"))
        self.assertFalse(check_urls.has_page(root, "/books/y/"))


class Content(unittest.TestCase):
    def problems(self, body: str, extra: dict[str, str] | None = None) -> list[str]:
        files = {"page/index.html": f'<html><body><main><div data-pagefind-body>{body}</div></main></body></html>'}
        files.update(extra or {})
        root = site(files)
        return check_content.check_file(root / "page/index.html", root)

    def test_clean_text_passes(self):
        self.assertEqual(self.problems('<p>Plain <em>text</em> and <a href="/books/">a link</a>.</p>'), [])

    def test_search_metadata_with_a_comma_is_caught(self):
        found = self.problems('<span data-pagefind-meta="book:Essays, Speeches, shelf:le"></span>')
        self.assertTrue(any("data-pagefind-meta" in f for f in found))
        self.assertEqual(self.problems('<span data-pagefind-meta="shelf:le"></span>'), [])

    def test_scripts_and_handlers_are_caught(self):
        self.assertTrue(self.problems("<script>alert(1)</script>"))
        self.assertTrue(self.problems('<p onclick="x()">hi</p>'))
        self.assertTrue(self.problems('<a href="javascript:alert(1)">x</a>'))
        self.assertTrue(self.problems('<iframe src="/x"></iframe>'))

    def test_images(self):
        self.assertEqual(self.problems('<img src="https://archive.org/download/x/page/n1.jpg">'), [])
        self.assertEqual(self.problems('<img src="/fig.webp">', {"fig.webp": "x"}), [])
        self.assertTrue(self.problems('<img src="/missing.webp">'))
        self.assertTrue(self.problems('<img src="https://example.com/x.png">'))

    def test_site_form_outside_book_text_is_allowed(self):
        root = site({"s/index.html": '<main><form action="/search/"></form></main>'})
        self.assertEqual(check_content.check_file(root / "s/index.html", root), [])


class Headers(unittest.TestCase):
    """static/_headers: the search index's entry files must be checked on every visit, or a deploy that
    renames the index chunks breaks search for readers with an old entry cached."""
    def rules(self):
        text = (Path(__file__).resolve().parent.parent / "static" / "_headers").read_text(encoding="utf-8")
        rules, path = {}, None
        for line in text.splitlines():
            if line.startswith("/"):
                path = line.strip()
                rules[path] = ""
            elif path and line.strip().lower().startswith("cache-control:"):
                rules[path] = line.split(":", 1)[1].strip()
        return rules

    def test_search_entry_files_are_never_cached_stale(self):
        rules = self.rules()
        for f in ("/pagefind/pagefind-entry.json", "/pagefind/pagefind.js"):
            self.assertIn("max-age=0", rules.get(f, ""), f)
        self.assertNotIn("/pagefind/*", rules, "a rule for all of /pagefind/ would also cache the entry files")


class InlineStyles(unittest.TestCase):
    """The policy allows inline <style> only by fingerprint; the one-page editions once lost their styles
    on the live site because nothing compared the two (review 0003, finding 1)."""
    def test_a_block_is_fingerprinted_as_the_browser_does(self):
        # sha256 of "p{color:red}", base64, as browsers compute it for a CSP hash source
        self.assertEqual(check_styles.style_hashes("<style>p{color:red}</style>"),
                         {"sha256-" + base64.b64encode(hashlib.sha256(b"p{color:red}").digest()).decode()})

    def test_only_the_policy_line_counts_not_a_comment(self):
        headers = ("# style-src-elem 'sha256-AAAA'\n/*\n  Content-Security-Policy: default-src 'self'; "
                   "style-src-elem 'self' 'sha256-BBBB='; img-src 'self'\n")
        self.assertEqual(check_styles.allowed_hashes(headers), {"sha256-BBBB="})

    def test_the_sites_own_downloads_are_allowed(self):
        headers = (Path(__file__).resolve().parent.parent / "static" / "_headers").read_text(encoding="utf-8")
        allowed = check_styles.allowed_hashes(headers)
        for page in (Path(__file__).resolve().parent.parent / "public" / "downloads").glob("*/*.html"):
            self.assertLessEqual(check_styles.style_hashes(page.read_text(encoding="utf-8")), allowed, page)


if __name__ == "__main__":
    unittest.main()
