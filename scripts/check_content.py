#!/usr/bin/env python3
"""Fail the build if a built page carries markup that could run code or load from elsewhere.

Chapter text comes from the book pipeline, where a model reads each page, and is placed on the site as
HTML. The content security policy blocks most harm, but this check stops it before publication: no
script or style elements, no event-handler attributes, no javascript: links, no frames or objects, and
no images from anywhere but this site and archive.org. Standard library only.

Also fails on an image that points to a file the site does not have.

Usage: python3 scripts/check_content.py [public-dir]
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANNED_TAGS = {"iframe", "object", "embed", "frame", "frameset", "applet", "base", "form", "meta", "link", "style"}
IMG_REMOTE_OK = re.compile(r"^(data:image/|https://(?:[a-z0-9-]+\.)*archive\.org/)")


class Checker(HTMLParser):
    def __init__(self, page: Path, public: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.page, self.public = page, public
        self.depth = 0
        self.text_depth = 0
        self.problems: list[str] = []
        self.scripts_outside = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        void = tag in ("img", "br", "hr", "input", "source", "wbr", "col", "area", "meta", "link")
        if not void:
            self.depth += 1
        if "data-pagefind-body" in dict(attrs) and not self.text_depth:
            self.text_depth = self.depth
        for name, value in attrs:
            v = (value or "").strip().lower()
            if name.startswith("on"):
                self.problems.append(f"<{tag} {name}=...> event handler")
            if name in ("href", "src", "action", "formaction", "xlink:href") and v.startswith(("javascript:", "vbscript:", "data:text")):
                self.problems.append(f"<{tag} {name}={value!r}>")
            if tag == "img" and name == "src":
                self.check_img(value or "")
        if self.text_depth and (tag in BANNED_TAGS or tag == "script"):
            self.problems.append(f"<{tag}> inside the book text")

    def check_img(self, src: str) -> None:
        if IMG_REMOTE_OK.match(src):
            return
        if "://" in src or src.startswith("//"):
            self.problems.append(f"<img src={src!r}> loads from elsewhere")
            return
        target = self.public / src.lstrip("/") if src.startswith("/") else self.page.parent / src
        if not Path(str(target).split("?")[0]).is_file():
            self.problems.append(f"<img src={src!r}> is missing")

    def handle_endtag(self, tag: str) -> None:
        if self.text_depth and self.depth == self.text_depth:
            self.text_depth = 0
        self.depth -= 1


def check_file(path: Path, public: Path) -> list[str]:
    c = Checker(path, public)
    c.feed(path.read_text(encoding="utf-8"))
    return c.problems


def main() -> None:
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "public"
    pages = [p for p in public.rglob("*.html") if "pagefind" not in p.parts and "downloads" not in p.parts]
    if not pages:
        sys.exit(f"No built pages in {public}. Run hugo first.")
    bad = {}
    for p in pages:
        problems = check_file(p, public)
        if problems:
            bad[p.relative_to(public)] = problems
    print(f"Checked {len(pages)} pages for unsafe or broken markup.")
    if bad:
        for p, problems in sorted(bad.items())[:40]:
            print(f"  {p}: " + "; ".join(sorted(set(problems))[:4]))
        sys.exit(f"{len(bad)} pages carry unsafe or broken markup.")
    print("No unsafe or broken markup.")


if __name__ == "__main__":
    main()
