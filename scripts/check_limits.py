#!/usr/bin/env python3
"""Warn well before the built site outgrows what Cloudflare will deploy.

Cloudflare's static assets allow 20,000 files on the Free plan (100,000 on paid) and 2,000 static
redirects. This fails at 90% of the Free limits, so there is time to move downloads elsewhere or
change plan before a deploy is refused. Standard library only.

Usage: python3 scripts/check_limits.py [public-dir]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE_LIMIT, REDIRECT_LIMIT, MARGIN = 20_000, 2_000, 0.9


def main() -> None:
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "public"
    files = sum(1 for p in public.rglob("*") if p.is_file())
    red = public / "_redirects"
    rules = sum(1 for ln in red.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")) if red.is_file() else 0
    print(f"{files} files (limit {FILE_LIMIT}), {rules} redirects (limit {REDIRECT_LIMIT}).")
    over = []
    if files > FILE_LIMIT * MARGIN:
        over.append(f"files: {files} is over 90% of {FILE_LIMIT}. Move static/downloads to GitHub Releases or R2, or change plan.")
    if rules > REDIRECT_LIMIT * MARGIN:
        over.append(f"redirects: {rules} is over 90% of {REDIRECT_LIMIT}. Group them by pattern.")
    if over:
        sys.exit("\n".join(over))


if __name__ == "__main__":
    main()
