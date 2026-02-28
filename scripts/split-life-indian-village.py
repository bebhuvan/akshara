#!/usr/bin/env python3
"""
Split 'Life in an Indian Village' into Hugo-compatible chapter files.
Handles: Introduction + 15 Chapters. Skips printer's colophon.
"""

import re
from pathlib import Path

SOURCE = Path("/home/bhuvanesh.r/Akshara Pandoc/Life in an Indian Village/life-in-an-indian-village.md")
OUTPUT = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/life-in-an-indian-village")

# Short titles for each chapter (extracted from the verbose headings)
CHAPTER_TITLES = {
    1: ("The Headman, Accountant, and Watchman", "headman-accountant-watchman"),
    2: ("Caste, Astrologer, Priests, and Schoolmaster", "caste-astrologer-priests-schoolmaster"),
    3: ("Poetry, Physician, Carpenter, Blacksmith, and Shepherd", "poetry-physician-carpenter-blacksmith-shepherd"),
    4: ("Washerman, Potter, Barber, and the Village Goddess", "washerman-potter-barber-village-goddess"),
    5: ("The Panisiva, the Moneylender, and the Dancing Girls", "panisiva-moneylender-dancing-girls"),
    6: ("Slavery, Pariahs, and the Outcaste Communities", "slavery-pariahs-outcaste-communities"),
    7: ("Village Constitution and Hindu Women", "village-constitution-hindu-women"),
    8: ("The Village Bards", "village-bards"),
    9: ("Jugglers and Acrobats", "jugglers-and-acrobats"),
    10: ("Snake-Charmers and Animal-Tamers", "snake-charmers-animal-tamers"),
    11: ("The Village Preacher", "village-preacher"),
    12: ("The Village Drama", "village-drama"),
    13: ("Feasts and Festivals", "feasts-and-festivals"),
    14: ("The Religious Brotherhood", "religious-brotherhood"),
    15: ("Concluding Remarks", "concluding-remarks"),
}

ROMAN = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V",
    6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
    11: "XI", 12: "XII", 13: "XIII", 14: "XIV", 15: "XV",
}

INT_FROM_ROMAN = {v: k for k, v in ROMAN.items()}


def find_sections(lines):
    """Find line indices for all major sections."""
    sections = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Introduction
        if stripped == "## INTRODUCTION.":
            sections.append((i, "introduction", None))
        # Contents (to skip)
        elif stripped == "## CONTENTS.":
            sections.append((i, "contents", None))
        # Chapters: pattern is "## I." or "## II." or "## XV." etc.
        elif re.match(r'^##\s+([IVXLC]+)\.\s', stripped):
            m = re.match(r'^##\s+([IVXLC]+)\.', stripped)
            roman = m.group(1)
            if roman in INT_FROM_ROMAN:
                sections.append((i, "chapter", INT_FROM_ROMAN[roman]))
    return sections


def strip_heading(text):
    """Remove the first ## heading line from content."""
    lines = text.split("\n")
    cleaned = []
    found = False
    for line in lines:
        if not found and line.strip().startswith("## "):
            found = True
            continue
        cleaned.append(line)
    # Remove leading blank lines and --- separators
    while cleaned and cleaned[0].strip() in ("", "---"):
        cleaned.pop(0)
    # Remove trailing blank lines and printer colophon
    while cleaned and (cleaned[-1].strip() == "" or
                       cleaned[-1].strip().startswith("UNWIN BROTHERS")):
        cleaned.pop()
    return "\n".join(cleaned)


def word_count(text):
    return len(text.split())


def reading_time_minutes(text):
    return max(5, round(word_count(text) / 200))


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)

    with open(SOURCE, "r", encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f.readlines()]

    sections = find_sections(lines)

    print(f"Found {len(sections)} sections:")
    for line_num, stype, sval in sections:
        print(f"  Line {line_num + 1}: {stype} {sval or ''}")

    # Build ranges
    section_list = []
    for idx, (line_num, stype, sval) in enumerate(sections):
        end = sections[idx + 1][0] if idx + 1 < len(sections) else len(lines)
        section_list.append((line_num, end, stype, sval))

    total_words = 0

    for start, end, stype, sval in section_list:
        if stype == "contents":
            continue  # Skip table of contents

        raw = "\n".join(lines[start:end])
        content = strip_heading(raw)
        rt = reading_time_minutes(content)
        wc = word_count(content)
        total_words += wc

        if stype == "introduction":
            filename = "00-introduction.md"
            title = "Introduction"
            ch_num = 0
        elif stype == "chapter":
            ch_num = sval
            title_text, slug = CHAPTER_TITLES[ch_num]
            roman = ROMAN[ch_num]
            title = f"Chapter {roman}: {title_text}"
            filename = f"{ch_num:02d}-{slug}.md"
        else:
            continue

        with open(OUTPUT / filename, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{title}"
chapter_number: {ch_num}
weight: {ch_num}
reading_time: {rt}
---

{content}
""")
        print(f"  Created {filename} ({rt} min, {wc} words)")

    total_hours = round(total_words / 200 / 60, 1)
    print(f"\nTotal: {total_words} words, ~{total_hours} hours reading time")
    print(f"Files created in: {OUTPUT}")


if __name__ == "__main__":
    main()
