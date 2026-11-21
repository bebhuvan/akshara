"""Check every book's cover (data/covers.toml) before the site is built.

The rule that is never broken: a cover's picture comes from that same book. Each plate's book is
recorded where the plate was made (data/plates.toml for the earlier ones, data/plate_sources.toml for
the rest); a cover may only use a plate recorded for its own book. Also: every book has a cover, every
cover belongs to a book, the kind is known, a picture's file exists, and a type-only cover says why.

Usage: python3 scripts/check_covers.py [repo root]
"""
import sys
import tomllib
from pathlib import Path

KINDS = {"plate", "map", "device", "portrait", "photo", "type"}


def plate_books(plates: dict, sources: dict) -> dict[str, str]:
    """Each plate key and the book it was taken from, from both records."""
    out = {}
    for group in plates.get("group", []):
        for p in group.get("plate", []):
            out[p["key"]] = p["book"]
    for p in sources.get("plate", []):
        out[p["key"]] = p["book"]
    return out


def problems(covers: dict, books: set[str], provenance: dict[str, str], files: set[str]) -> list[str]:
    """Everything wrong with the covers, as sentences. Empty when all is well."""
    out = []
    for book in sorted(books - covers.keys()):
        out.append(f"{book} has no cover in data/covers.toml")
    for book in sorted(covers.keys() - books):
        out.append(f"data/covers.toml has a cover for {book}, which is not a book")
    for book, c in sorted(covers.items()):
        kind, plate = c.get("kind"), c.get("plate")
        if kind not in KINDS:
            out.append(f"{book}: kind {kind!r} is not one of {sorted(KINDS)}")
            continue
        if kind == "type":
            if plate:
                out.append(f"{book}: a type-only cover takes no plate")
            if not c.get("why"):
                out.append(f"{book}: a type-only cover says why there is no picture (why = ...)")
            continue
        if not plate:
            out.append(f"{book}: a {kind} cover needs a plate")
            continue
        if plate not in files:
            out.append(f"{book}: plate {plate} is not in static/plates/")
        source_book = provenance.get(plate)
        if source_book is None:
            out.append(f"{book}: nothing records which book plate {plate} came from")
        elif source_book != book:
            out.append(f"{book}: plate {plate} comes from {source_book}, not from this book")
    return out


def main(root: Path) -> int:
    def toml(rel):
        path = root / rel
        return tomllib.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

    covers = toml("data/covers.toml")
    books = {p.name for p in (root / "content" / "books").iterdir() if p.is_dir()}
    provenance = plate_books(toml("data/plates.toml"), toml("data/plate_sources.toml"))
    files = {p.stem for p in (root / "static" / "plates").glob("*.webp")}
    found = problems(covers, books, provenance, files)
    for line in found:
        print(line)
    pictured = sum(1 for c in covers.values() if c.get("kind") != "type")
    if found:
        print(f"{len(found)} cover problem(s).")
        return 1
    print(f"All {len(covers)} covers checked: {pictured} with a picture from their own book, {len(covers) - pictured} type only.")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent))
