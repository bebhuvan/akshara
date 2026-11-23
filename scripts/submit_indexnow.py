#!/usr/bin/env python3
"""Submit updated Akshara URLs to IndexNow (Bing, Yahoo, DuckDuckGo, Yandex, Seznam, ChatGPT Search).

Standard library only. Reads the verified IndexNow key file from static/ and submits URLs
from public/sitemap.xml (either all URLs, or only URLs matching recently modified books/blog posts,
or explicit URLs passed on the command line).

Usage:
  python3 scripts/submit_indexnow.py --dry-run --all
  python3 scripts/submit_indexnow.py --all
  python3 scripts/submit_indexnow.py --since-days 7
  python3 scripts/submit_indexnow.py https://akshara.ink/ https://akshara.ink/books/india-at-the-death-of-akbar/
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = "akshara.ink"
INDEXNOW_KEY = "a7c4e91f2b8d4036e5a1f8c3d9b2074e"
KEY_LOCATION = f"https://{HOST}/{INDEXNOW_KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
MAX_BATCH = 10_000


def load_sitemap_urls(sitemap: Path, since_days: int | None = None) -> list[str]:
    if not sitemap.is_file():
        sys.exit(f"Sitemap not found at {sitemap}. Run ./verify or hugo first.")
    tree = ET.parse(sitemap)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    cutoff = None
    if since_days is not None:
        cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=since_days)
    urls: list[str] = []
    for node in tree.findall("sm:url", ns):
        loc = node.find("sm:loc", ns)
        if loc is None or not loc.text:
            continue
        if cutoff is not None:
            lm = node.find("sm:lastmod", ns)
            if lm is None or not lm.text:
                continue
            try:
                ts = dt.datetime.fromisoformat(lm.text.replace("Z", "+00:00"))
            except ValueError:
                continue
            if ts < cutoff:
                continue
        urls.append(loc.text.strip())
    return urls


def submit(urls: list[str], dry_run: bool = False) -> None:
    if not urls:
        print("No URLs matched for IndexNow submission.")
        return
    # Verify local key file exists before submitting
    key_file = ROOT / "static" / f"{INDEXNOW_KEY}.txt"
    if not key_file.is_file() or key_file.read_text(encoding="utf-8").strip() != INDEXNOW_KEY:
        sys.exit(f"IndexNow verification file missing or mismatched: {key_file}")

    for i in range(0, len(urls), MAX_BATCH):
        batch = urls[i : i + MAX_BATCH]
        payload = {
            "host": HOST,
            "key": INDEXNOW_KEY,
            "keyLocation": KEY_LOCATION,
            "urlList": batch,
        }
        if dry_run:
            print(f"[dry-run] Would submit {len(batch)} URLs to {ENDPOINT} (keyLocation={KEY_LOCATION})")
            for u in batch[:10]:
                print(f"  - {u}")
            if len(batch) > 10:
                print(f"  ... and {len(batch) - 10} more")
            continue

        req = urllib.request.Request(
            ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"IndexNow HTTP {resp.status}: submitted {len(batch)} URLs.")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            sys.exit(f"IndexNow submission failed (HTTP {e.code}): {body}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit Akshara URLs to IndexNow.")
    parser.add_argument("urls", nargs="*", help="Explicit URLs to submit.")
    parser.add_argument("--all", action="store_true", help="Submit every URL in public/sitemap.xml.")
    parser.add_argument("--since-days", type=int, default=None, help="Submit sitemap URLs modified within N days.")
    parser.add_argument("--sitemap", type=Path, default=ROOT / "public" / "sitemap.xml")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be submitted without sending HTTP.")
    args = parser.parse_args()

    if args.urls:
        urls = args.urls
    elif args.all:
        urls = load_sitemap_urls(args.sitemap)
    elif args.since_days is not None:
        urls = load_sitemap_urls(args.sitemap, since_days=args.since_days)
    else:
        parser.error("Specify explicit URLs, --all, or --since-days N.")
    submit(urls, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
