# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow==13.0.0"]
# ///
"""Make the one-ink cover plates listed in data/plate_sources.toml.

A plate is a picture from a book's own pages, cleaned so it prints in one ink: black on
transparent, saved as WebP with alpha, and used by the site as a CSS mask. Each entry names its
source (a figure under static/figures, or an Internet Archive page image), a crop, and a mode:
"line" keeps the engraved line as soft alpha; "halftone" turns a photograph into an ordered
(Bayer) dither so it reads as a fine screen of dots at cover size. Entries that carry `made`
instead of `crop` were made by hand earlier and are skipped.

Usage: uv run scripts/make_plates.py [--cache DIR] [--only KEY ...]
Archive.org pages are downloaded once into the cache (default: $PLATE_CACHE, else a folder in the
system temp directory), never into the repository.
"""
import argparse
import io
import os
import sys
import tempfile
import tomllib
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "data" / "plate_sources.toml"
OUT = ROOT / "static" / "plates"
LONG_SIDE = {"line": 1400, "halftone": 800}
BAYER_8 = [
    [0, 32, 8, 40, 2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21],
]


# Deciding: pure functions on numbers and plate entries.

def check_entry(p: dict) -> None:
    """Stop on an entry that is missing something or names an impossible crop."""
    for field in ("key", "book", "source", "what"):
        if not p.get(field):
            raise ValueError(f"plate {p.get('key', '?')}: missing {field}")
    if "made" in p:
        return
    if p.get("mode") not in LONG_SIDE:
        raise ValueError(f"{p['key']}: mode must be 'line' or 'halftone'")
    l, t, r, b = p["crop"]
    if not (0 <= l < r <= 1 and 0 <= t < b <= 1):
        raise ValueError(f"{p['key']}: crop {p['crop']} must be fractions with left<right, top<bottom")
    if "levels" in p and not (0 <= p["levels"][0] < p["levels"][1] <= 255):
        raise ValueError(f"{p['key']}: levels must be [black, white] with 0 <= black < white <= 255")


def crop_box(size: tuple[int, int], frac: list[float]) -> tuple[int, int, int, int]:
    w, h = size
    l, t, r, b = frac
    return round(l * w), round(t * h), round(r * w), round(b * h)


def fit_long_side(size: tuple[int, int], long_side: int) -> tuple[int, int]:
    """Shrink to the long side; never enlarge, since that only invents detail."""
    w, h = size
    scale = min(1.0, long_side / max(w, h))
    return max(1, round(w * scale)), max(1, round(h * scale))


def percentile(hist: list[int], p: float) -> int:
    total, acc = sum(hist), 0
    for value, count in enumerate(hist):
        acc += count
        if acc >= total * p:
            return value
    return 255


def auto_levels(hist: list[int], mode: str) -> tuple[int, int]:
    """Black and white points from the grey histogram. In a line plate most of the area is paper,
    so the paper tone sits near the median and the line is the darkest percent. A photograph has
    no such paper, so only its extreme tones are clipped."""
    if mode == "halftone":
        black, white = percentile(hist, 0.03), percentile(hist, 0.97)
        return black, max(white, black + 30)
    paper = percentile(hist, 0.55)
    dark = percentile(hist, 0.01)
    white = max(paper - 14, dark + 40)
    black = min(dark + 6, white - 30)
    return max(0, black), min(255, white)


def level_table(black: int, white: int) -> list[int]:
    span = white - black
    return [min(255, max(0, round((v - black) * 255 / span))) for v in range(256)]


# Doing: reading sources, image operations, writing files.

def fetch(url: str, cache: Path) -> Path:
    parts = urllib.parse.urlparse(url)
    if parts.scheme != "https" or parts.hostname != "archive.org":
        raise ValueError(f"only https://archive.org page images are allowed as sources: {url}")
    target = cache / parts.path.strip("/").replace("/", "_")
    if target.is_file():
        return target
    cache.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "akshara-make-plates/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read(50_000_000)
    Image.open(io.BytesIO(data)).verify()  # refuse an error page saved as an image
    partial = target.with_suffix(".part")
    partial.write_bytes(data)
    partial.replace(target)
    return target


def load_source(source: str, cache: Path) -> Image.Image:
    path = fetch(source, cache) if source.startswith("https://") else ROOT / source
    if not path.is_file():
        raise FileNotFoundError(f"source not found: {source}")
    return Image.open(path)


def bayer_tile(size: tuple[int, int]) -> Image.Image:
    cell = Image.new("L", (8, 8))
    cell.putdata([round((v + 0.5) * 255 / 64) for row in BAYER_8 for v in row])
    tile = Image.new("L", size)
    for y in range(0, size[1], 8):
        for x in range(0, size[0], 8):
            tile.paste(cell, (x, y))
    return tile


def make_plate(p: dict, cache: Path) -> Image.Image:
    im = load_source(p["source"], cache)
    if p.get("rotate"):
        im = im.rotate(p["rotate"], expand=True)
    im = im.crop(crop_box(im.size, p["crop"]))
    grey = im.getchannel(p["channel"][0].upper()) if p.get("channel") else im.convert("L")
    for rect in p.get("blank", []):
        grey.paste(255, crop_box(grey.size, rect))
    grey = grey.resize(fit_long_side(grey.size, p.get("long_side", LONG_SIDE[p["mode"]])), Image.LANCZOS)
    grey = ImageOps.autocontrast(grey, cutoff=0.5)
    black, white = p.get("levels") or auto_levels(grey.histogram(), p["mode"])
    grey = grey.point(level_table(black, white))
    if p["mode"] == "halftone":
        # paper (255) stays clear only where it is brighter than the threshold cell
        grey = ImageChops.subtract(grey, bayer_tile(grey.size)).point(lambda v: 255 if v > 0 else 0)
    plate = Image.new("RGBA", grey.size, (0, 0, 0, 0))
    plate.putalpha(ImageOps.invert(grey))
    return plate


def save(plate: Image.Image, out: Path, mode: str) -> None:
    if mode == "halftone":  # two-level alpha compresses best losslessly
        plate.save(out, "WEBP", lossless=True, quality=100, method=6, exact=False)
    else:
        plate.save(out, "WEBP", quality=70, alpha_quality=60, method=6)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cache", type=Path, default=Path(os.environ.get("PLATE_CACHE") or Path(tempfile.gettempdir()) / "akshara-plate-cache"))
    ap.add_argument("--only", nargs="*", help="make only these keys")
    args = ap.parse_args()
    plates = tomllib.loads(SOURCES.read_text(encoding="utf-8"))["plate"]
    keys = [p.get("key") for p in plates]
    if len(keys) != len(set(keys)):
        sys.exit("duplicate keys in data/plate_sources.toml")
    for p in plates:
        check_entry(p)
    unknown = set(args.only or []) - set(keys)
    if unknown:
        sys.exit(f"unknown keys: {', '.join(sorted(unknown))}")
    for p in plates:
        if "made" in p or (args.only and p["key"] not in args.only):
            continue
        out = OUT / f"{p['key']}.webp"
        plate = make_plate(p, args.cache)
        save(plate, out, p["mode"])
        print(f"{p['key']:22} {plate.width}x{plate.height}  {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
