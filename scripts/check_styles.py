#!/usr/bin/env python3
"""Fail the build if a built page has a <style> block the content security policy would refuse.

The global policy (static/_headers) allows style elements only from this site's own files, plus any
inline blocks explicitly allowed by sha256 fingerprint. Self-contained one-page HTML downloads under
/downloads/* detach that global CSP and enforce a zero-script policy (`default-src 'none';
style-src 'unsafe-inline'; font-src data:`) so each book's embedded subsetted font renders safely.
Standard library only.

Usage: python3 scripts/check_styles.py [public-dir]
"""
import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
SCRIPT = re.compile(r"<script\b", re.I)


def style_hashes(html: str) -> set[str]:
    """The CSP fingerprint ('sha256-…', base64) of every inline style block in a page."""
    return {"sha256-" + base64.b64encode(hashlib.sha256(m.group(1).encode("utf-8")).digest()).decode()
            for m in STYLE.finditer(html)}


def allowed_hashes(headers: str) -> set[str]:
    """The fingerprints the site-wide policy (/*) allows in style-src-elem."""
    m = re.search(r"Content-Security-Policy:.*?style-src-elem([^;]*)", headers)
    return set(re.findall(r"'(sha256-[A-Za-z0-9+/=]+)'", m.group(1))) if m else set()


def downloads_policy_valid(headers: str) -> bool:
    """True when /downloads/* detaches global CSP and enforces zero-script inline styles + data fonts."""
    section_lines: list[str] = []
    in_downloads = False
    for raw in headers.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("/"):
            in_downloads = line == "/downloads/*"
            continue
        if in_downloads:
            section_lines.append(line)
    if "! Content-Security-Policy" not in section_lines:
        return False
    csp = next((ln.split(":", 1)[1].strip() for ln in section_lines if ln.startswith("Content-Security-Policy:")), "")
    directives = {p.split()[0]: set(p.split()[1:]) for p in csp.split(";") if p.split()}
    return (
        directives.get("default-src") == {"'none'"}
        and "script-src" not in directives
        and "'unsafe-inline'" in directives.get("style-src", set())
        and "data:" in directives.get("font-src", set())
    )


def main() -> None:
    public = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "public")
    headers = (ROOT / "static/_headers").read_text(encoding="utf-8")
    allowed = allowed_hashes(headers)
    downloads_ok = downloads_policy_valid(headers)
    problems, styled = [], 0
    for page in sorted(public.rglob("*.html")):
        rel = page.relative_to(public)
        text = page.read_text(encoding="utf-8", errors="replace")
        found = style_hashes(text)
        styled += bool(found)
        if rel.parts[:1] == ("downloads",):
            if not downloads_ok:
                problems.append(f"{rel}: /downloads/* lacks '! Content-Security-Policy' zero-script style rule")
            elif SCRIPT.search(text):
                problems.append(f"{rel}: one-page download contains a <script> tag")
            continue
        for h in sorted(found - allowed):
            problems.append(f"{rel}: a <style> block the policy would refuse ('{h}')")
    if problems:
        print("\n".join(problems[:20]))
        print(f"{len(problems)} style block(s) would be blocked. Keep inline <style> out of site pages"
              " or configure /downloads/* CSP cleanly in static/_headers.")
        sys.exit(1)
    print(f"Every inline style block ({styled} pages) is allowed by the policy.")


if __name__ == "__main__":
    main()
