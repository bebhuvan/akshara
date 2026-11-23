# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools==4.60.1", "brotli==1.1.0"]
# ///
"""Cut the three faces a reader can choose for a book's text into small WOFF2 files (DECISIONS.md, D35, D36).

EB Garamond (Book), Noto Serif (Clear) and Source Sans 3 (Plain) are each instanced to weights 400-700 (Noto
Serif also to its normal width) and cut into three files per style, by the same three ranges as Newsreader in
assets/css/plate.css: Latin; the accented letters the books use, with the combining accents (a dot below typed
as its own mark must come from the same face as its letter); and the rest of Latin Extended with the modifier
letters, super- and subscripts, letterlike symbols and fractions the books' notes and tables use. Each range is
a unicode-range in plate.css, so a browser fetches a file only for a page that has one of its letters.

Source Sans 3's licence reserves the name "Source" for the original, and a cut is a modified version, so its
cuts are renamed "Akshara Plain" inside the files (the other two licences reserve no name).

Every OpenType feature is kept: small capitals, old-style figures, ligatures, kerning, mark positioning.
This is a one-off tool, run only when a face is updated; the site never runs it.

Usage: uv run scripts/cut_reading_fonts.py SOURCE_DIR
SOURCE_DIR holds EBGaramond.ttf and EBGaramond-Italic.ttf (from the EB Garamond project), and NotoSerif[wdth,wght].ttf,
NotoSerif-Italic[wdth,wght].ttf, SourceSans3[wght].ttf and SourceSans3-Italic[wght].ttf (from github.com/google/fonts,
ofl/). The files go to static/fonts/; the ranges are printed for the @font-face rules.
"""
import io
import re
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static" / "fonts"
FACES = [  # source file, name of the cut, axis limits
    ("EBGaramond.ttf", "ebgaramond-normal", {"wght": (400, 700)}),
    ("EBGaramond-Italic.ttf", "ebgaramond-italic", {"wght": (400, 700)}),
    ("NotoSerif[wdth,wght].ttf", "notoserif-normal", {"wght": (400, 700), "wdth": 100}),
    ("NotoSerif-Italic[wdth,wght].ttf", "notoserif-italic", {"wght": (400, 700), "wdth": 100}),
    ("SourceSans3[wght].ttf", "sourcesans3-normal", {"wght": (400, 700)}),
    ("SourceSans3-Italic[wght].ttf", "sourcesans3-italic", {"wght": (400, 700)}),
]
FILE = {"latin": "{}-400-700-latin.woff2", "ext-common": "{}-ext-common.woff2", "latin-ext": "{}-400-700-latin-ext.woff2"}


def newsreader_ranges() -> dict[str, list[int]]:
    """The three ranges of Newsreader's upright @font-face rules, as code points."""
    css = (ROOT / "assets" / "css" / "plate.css").read_text(encoding="utf-8")
    rules = re.findall(r'font-family: "Newsreader"; font-style: normal;.*?url\("/fonts/newsreader-normal-([a-z0-9-]+)\.woff2"\)'
                       r'.*?unicode-range: ([^;]+);', css, re.S)
    names = {"400-700-latin": "latin", "ext-common": "ext-common", "400-700-latin-ext": "latin-ext"}
    ranges = {}
    for name, spec in rules:
        cps = []
        for part in spec.split(","):
            a, _, b = part.strip()[2:].partition("-")
            cps.extend(range(int(a, 16), int(b or a, 16) + 1))
        ranges[names[name]] = cps
    if set(ranges) != set(names.values()):
        sys.exit("plate.css: Newsreader's three upright @font-face rules were not found")
    return ranges


def reading_ranges() -> dict[str, list[int]]:
    ranges = newsreader_ranges()
    taken = {c for cps in ranges.values() for c in cps}

    def span(a: int, b: int) -> list[int]:
        return [c for c in range(a, b + 1) if c not in taken]

    ranges["ext-common"] += span(0x0300, 0x036F)
    taken |= set(ranges["ext-common"])
    for a, b in [(0x02B0, 0x02FF), (0x1D00, 0x1DBF), (0x1EA0, 0x1EF1), (0x2070, 0x209F), (0x2100, 0x218F)]:
        ranges["latin-ext"] += span(a, b)
    return ranges


def rename(font: TTFont, family: str, style: str) -> None:
    """Keep only the copyright, licence and the new name: the original's names may not travel with a cut."""
    table = font["name"]
    table.names = [n for n in table.names if n.nameID in (0, 13, 14)]
    for nid, value in {1: family, 2: style, 3: f"{family} {style}; cut for akshara.ink", 4: f"{family} {style}",
                       6: f"{family.replace(' ', '')}-{style}"}.items():
        table.setName(value, nid, 3, 1, 0x409)


def unicode_range(cps: list[int]) -> str:
    cps, out, i = sorted(set(cps)), [], 0
    while i < len(cps):
        j = i
        while j + 1 < len(cps) and cps[j + 1] == cps[j] + 1:
            j += 1
        out.append(f"U+{cps[i]:04X}" if i == j else f"U+{cps[i]:04X}-{cps[j]:04X}")
        i = j + 1
    return ", ".join(out)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    ranges = reading_ranges()
    for fn, name, limits in FACES:
        # instanced once, then written out and read back whole, so the subsetter sees a plain font
        buf = io.BytesIO()
        instancer.instantiateVariableFont(TTFont(src / fn), limits).save(buf)
        for key, cps in ranges.items():
            buf.seek(0)
            font = TTFont(buf, lazy=False)
            opts = subset.Options()
            opts.layout_features = ["*"]
            opts.name_IDs = ["*"]
            opts.name_languages = ["*"]
            opts.notdef_outline = True
            opts.hinting = False
            sub = subset.Subsetter(opts)
            sub.populate(unicodes=cps)
            sub.subset(font)
            if name.startswith("sourcesans3"):
                rename(font, "Akshara Plain", "Italic" if "italic" in name else "Regular")
            font.flavor = "woff2"
            path = OUT / FILE[key].format(name)
            font.save(path)
            print(f"{path.name}: {path.stat().st_size // 1024} KB")
    for key, cps in ranges.items():
        print(f"\n{key}: {unicode_range(cps)}")


if __name__ == "__main__":
    main()
