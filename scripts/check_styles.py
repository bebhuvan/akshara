#!/usr/bin/env python3
"""Fail the build if a built page has a <style> block the content security policy would refuse.

The policy (static/_headers) allows style elements only from this site's own files, plus inline blocks named by
their sha256 fingerprint. The pipeline's "one page" editions carry one such block; if the pipeline changes it,
the downloads would quietly lose their styles on the live site (review 0003, finding 1). Standard library only.

Usage: python3 scripts/check_styles.py [public-dir]
"""
import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)


def style_hashes(html: str) -> set[str]:
    """The CSP fingerprint ('sha256-…', base64) of every inline style block in a page."""
    return {"sha256-" + base64.b64encode(hashlib.sha256(m.group(1).encode("utf-8")).digest()).decode()
            for m in STYLE.finditer(html)}


def allowed_hashes(headers: str) -> set[str]:
    """The fingerprints the site-wide policy allows in style-src-elem."""
    m = re.search(r"Content-Security-Policy:.*?style-src-elem([^;]*)", headers)
    return set(re.findall(r"'(sha256-[A-Za-z0-9+/=]+)'", m.group(1))) if m else set()


def main() -> None:
    public = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "public")
    allowed = allowed_hashes((ROOT / "static/_headers").read_text(encoding="utf-8"))
    problems, styled = [], 0
    for page in public.rglob("*.html"):
        found = style_hashes(page.read_text(encoding="utf-8", errors="replace"))
        styled += bool(found)
        for h in sorted(found - allowed):
            problems.append(f"{page.relative_to(public)}: a <style> block the policy would refuse ('{h}')")
    if problems:
        print("\n".join(problems[:20]))
        print(f"{len(problems)} style block(s) would be blocked. Add the fingerprint to style-src-elem in static/_headers"
              " only if the block is the pipeline's own; otherwise move the styles into a file.")
        sys.exit(1)
    print(f"Every inline style block ({styled} pages) is allowed by the policy.")


if __name__ == "__main__":
    main()
