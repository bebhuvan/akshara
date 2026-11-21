#!/usr/bin/env python3
"""Fail the build if any address akshara.ink has ever served stops working.

Reads tests/known-urls.txt and the built site in public/. An address passes if public/ holds a page
for it, or if public/_redirects sends it to an address that has a page. Standard library only.

Usage: python3 scripts/check_urls.py [public-dir]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWN = ROOT / "tests" / "known-urls.txt"


def read_known() -> list[str]:
    lines = KNOWN.read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.startswith("#")]


def read_redirects(public: Path) -> dict[str, str]:
    path = public / "_redirects"
    if not path.is_file():
        return {}
    rules: dict[str, str] = {}
    raw: set[str] = set()
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 3 or parts[2] != "301" or "*" in parts[0] or ":" in parts[0]:
            sys.exit(f"_redirects line {n}: each rule must be 'old-path new-path 301': {line}")
        rules[normalise(parts[0])] = normalise(parts[1])
        raw.add(parts[0])
    missing = sorted(r for r in raw if r.endswith("/") and len(r) > 1 and r.rstrip("/") not in raw)
    if missing:
        sys.exit("_redirects: Cloudflare matches exactly, so each rule also needs a line without the final slash:\n"
                 + "\n".join(f"  {m.rstrip('/')}" for m in missing[:20]))
    return rules


def normalise(url: str) -> str:
    if url.startswith("http"):
        return url
    return url if url.endswith("/") or "." in url.rsplit("/", 1)[-1] else url + "/"


def has_page(public: Path, url: str) -> bool:
    rel = url.lstrip("/")
    if rel == "" or rel.endswith("/"):
        return (public / rel / "index.html").is_file()
    return (public / rel).is_file()


def main() -> None:
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "public"
    if not (public / "index.html").is_file():
        sys.exit(f"No built site at {public}. Run hugo first.")
    redirects = read_redirects(public)
    broken, chained = [], []
    for url in read_known():
        url = normalise(url)
        if has_page(public, url):
            continue
        target = redirects.get(url)
        if target is None:
            broken.append(url)
        elif not target.startswith("http") and not has_page(public, target):
            chained.append(f"{url} -> {target}")
    for target_from, target in redirects.items():
        if not target.startswith("http") and not has_page(public, target):
            chained.append(f"{target_from} -> {target}")
    known = read_known()
    print(f"Checked {len(known)} known addresses and {len(redirects)} redirects.")
    if broken:
        print(f"\n{len(broken)} addresses no longer work and have no redirect:")
        print("\n".join(f"  {u}" for u in broken))
    if chained:
        print(f"\n{len(set(chained))} redirects point at a page that does not exist:")
        print("\n".join(f"  {c}" for c in sorted(set(chained))))
    if broken or chained:
        sys.exit(1)
    print("Every known address works.")


if __name__ == "__main__":
    main()
