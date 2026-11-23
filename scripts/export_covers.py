#!/usr/bin/env python3
"""Export every book's cover as a 1600 × 2400 PNG for its EPUB and PDF (DECISIONS.md, D39).

The covers are drawn by the site's own cover partial (layouts/cover-sheet/page.html, built only in Hugo's
"covers" environment), photographed by headless Chromium from a local server this script starts and stops.
Writes covers-export/<book_id>.png; with --pipeline <akshara_new>, also copies each into
<akshara_new>/books/<book_id>/cover.png where that book folder exists.

    python3 scripts/export_covers.py [--pipeline ../akshara_new] [--only book-id ...]
"""

from __future__ import annotations

import argparse
import functools
import http.server
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1600, 2400


def build_cover_sheets(out_dir: Path) -> list[str]:
    subprocess.run(
        ["hugo", "--environment", "covers", "--quiet", "--destination", str(out_dir)], cwd=SITE, check=True
    )
    return sorted(p.parent.parent.name for p in (out_dir / "books").glob("*/cover-sheet/index.html"))


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # noqa: A002 - the stdlib's name
        pass


def serve(root: Path) -> tuple[http.server.ThreadingHTTPServer, int]:
    handler = functools.partial(_QuietHandler, directory=str(root))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1]


def shoot(url: str, out_png: Path) -> None:
    chromium = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if not chromium:
        sys.exit("export_covers: Chromium is needed to photograph the covers")
    subprocess.run(
        [
            chromium, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            f"--window-size={WIDTH},{HEIGHT}", "--virtual-time-budget=4000", f"--screenshot={out_png}", url,
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if not out_png.is_file() or out_png.stat().st_size < 10_000:
        sys.exit(f"export_covers: no usable picture for {url}")
    # A cover is two inks on pale paper: a 96-colour palette keeps it exact to the eye at a fraction of the size.
    magick = shutil.which("magick")
    if magick:
        subprocess.run([magick, str(out_png), "-strip", "-colors", "96", f"PNG8:{out_png}"], check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pipeline", type=Path, help="akshara_new checkout: copy each cover into books/<id>/cover.png")
    ap.add_argument("--only", nargs="*", help="only these book ids")
    args = ap.parse_args()

    out = SITE / "covers-export"
    out.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="akshara-covers-") as tmp:
        ids = build_cover_sheets(Path(tmp))
        if args.only:
            ids = [i for i in ids if i in set(args.only)]
        server, port = serve(Path(tmp))
        try:
            for book_id in ids:
                png = out / f"{book_id}.png"
                shoot(f"http://127.0.0.1:{port}/books/{book_id}/cover-sheet/", png)
                copied = ""
                if args.pipeline and (args.pipeline / "books" / book_id).is_dir():
                    shutil.copy2(png, args.pipeline / "books" / book_id / "cover.png")
                    copied = " (copied to the pipeline)"
                print(f"{book_id}: {png.stat().st_size // 1024} KB{copied}")
        finally:
            server.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
