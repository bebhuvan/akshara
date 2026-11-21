"""The deciding half of make_plates.py: pure functions on numbers and plate entries, with no image library,
so they can be tested anywhere (tests/test_plate_maths.py). Standard library only."""
from urllib.parse import urlparse

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


def archive_host_ok(url: str) -> bool:
    """Plates are made only from archive.org page images; a redirect may move the file to one of
    archive.org's own servers (ia800300.us.archive.org), never anywhere else."""
    parts = urlparse(url)
    host = parts.hostname or ""
    return parts.scheme == "https" and (host == "archive.org" or host.endswith(".archive.org"))
