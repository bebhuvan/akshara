#!/usr/bin/env python3
"""
Split 'India at the Death of Akbar' into Hugo-compatible chapter files.
Handles: Preface, 8 Chapters, 5 Appendices. Skips Index (page-number references).
"""

import re
from pathlib import Path

SOURCE = Path("/home/bhuvanesh.r/Akshara Pandoc/India at the Death of Akbar/india-at-the-death-of-akbar.md")
OUTPUT = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/india-at-the-death-of-akbar")

# Chapter metadata: (number, title, filename_slug)
CHAPTERS = {
    1: ("The Country and People", "the-country-and-people"),
    2: ("The Administration", "the-administration"),
    3: ("The Consuming Classes", "the-consuming-classes"),
    4: ("Agricultural Production", "agricultural-production"),
    5: ("Non-Agricultural Production", "non-agricultural-production"),
    6: ("Commerce", "commerce"),
    7: ("The Standard of Life", "the-standard-of-life"),
    8: ("The Wealth of India", "the-wealth-of-india"),
}

APPENDICES = {
    "A": ("The Crops Grown in India in the Sixteenth Century", "crops-grown-in-india"),
    "B": ("'Indian Corn' in Vijayanagar", "indian-corn-in-vijayanagar"),
    "C": ("The Seaports of Bengal", "seaports-of-bengal"),
    "D": ("The Shipping Ton", "the-shipping-ton"),
    "E": ("List of Authorities", "list-of-authorities"),
}

ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII"}


def find_sections(lines):
    """Find line indices for all major sections."""
    sections = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Preface
        if stripped == "## PREFACE":
            sections.append((i, "preface", None))
        # Contents (to skip)
        elif stripped == "## CONTENTS":
            sections.append((i, "contents", None))
        # Chapters (handle inconsistent casing)
        elif re.match(r'^##\s+CHAPTER\s+([IVXLC]+)', stripped):
            m = re.match(r'^##\s+CHAPTER\s+([IVXLC]+)', stripped)
            sections.append((i, "chapter", roman_to_int(m.group(1))))
        elif re.match(r'^##\s+Chapter\s+([IVXLC]+)', stripped):
            m = re.match(r'^##\s+Chapter\s+([IVXLC]+)', stripped)
            sections.append((i, "chapter", roman_to_int(m.group(1))))
        # Appendices
        elif re.match(r'^##\s+APPENDIX\s+([A-E])', stripped):
            m = re.match(r'^##\s+APPENDIX\s+([A-E])', stripped)
            sections.append((i, "appendix", m.group(1)))
        # Index
        elif stripped == "## INDEX":
            sections.append((i, "index", None))
    return sections


def roman_to_int(s):
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    total = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and vals[c] < vals[s[i + 1]]:
            total -= vals[c]
        else:
            total += vals[c]
    return total


def strip_chapter_headings(text, is_chapter_v=False):
    """Remove the chapter number heading and chapter title heading from content.

    Pattern: lines start with '## CHAPTER N' or '## Chapter N' followed by
    '### TITLE' or '#### TITLE'. We strip both, keeping sub-section headings.
    """
    lines = text.split("\n")
    cleaned = []
    skip_next_heading = False
    found_chapter_heading = False
    found_title_heading = False

    for line in lines:
        stripped = line.strip()

        # Skip the chapter number heading (## CHAPTER N)
        if not found_chapter_heading and re.match(r'^#{2}\s+(CHAPTER|Chapter)\s+[IVXLC]+', stripped):
            found_chapter_heading = True
            skip_next_heading = True  # Next heading is the title
            continue

        # Skip the chapter title heading (### TITLE or #### TITLE)
        if skip_next_heading and not found_title_heading and re.match(r'^#{3,4}\s+', stripped):
            # This is the chapter title heading (not a section heading)
            # Section headings have a number like "### I. ..." or "### 1. ..."
            if not re.match(r'^#{3,4}\s+[IVXLC0-9]+[\.\s]', stripped):
                found_title_heading = True
                skip_next_heading = False
                continue

        # For Chapter V: normalize #### to ### for section headings
        if is_chapter_v and stripped.startswith("####"):
            line = line.replace("####", "###", 1)

        cleaned.append(line)

    # Remove leading blank lines and --- separators
    while cleaned and cleaned[0].strip() in ("", "---"):
        cleaned.pop(0)

    # Remove trailing blank lines
    while cleaned and cleaned[-1].strip() == "":
        cleaned.pop()

    return "\n".join(cleaned)


def strip_preface_heading(text):
    """Remove '## PREFACE' heading from preface content."""
    lines = text.split("\n")
    cleaned = []
    found = False
    for line in lines:
        if not found and line.strip() == "## PREFACE":
            found = True
            continue
        cleaned.append(line)
    while cleaned and cleaned[0].strip() in ("", "---"):
        cleaned.pop(0)
    while cleaned and cleaned[-1].strip() == "":
        cleaned.pop()
    return "\n".join(cleaned)


def strip_appendix_heading(text):
    """Remove the '## APPENDIX X ...' heading and any sub-title heading."""
    lines = text.split("\n")
    cleaned = []
    found_main = False
    found_subtitle = False

    for line in lines:
        stripped = line.strip()
        # Skip the main appendix heading
        if not found_main and re.match(r'^##\s+APPENDIX\s+[A-E]', stripped):
            found_main = True
            # Check if there's a subtitle on the next heading line
            continue
        # Skip subtitle heading (### "TITLE") if present
        if found_main and not found_subtitle and re.match(r'^###\s+', stripped):
            found_subtitle = True
            continue
        # If we found the main heading but no subtitle heading, stop skipping
        if found_main and not found_subtitle and stripped:
            found_subtitle = True  # no subtitle to skip
        cleaned.append(line)

    while cleaned and cleaned[0].strip() in ("", "---"):
        cleaned.pop(0)
    while cleaned and cleaned[-1].strip() == "":
        cleaned.pop()
    return "\n".join(cleaned)


def word_count(text):
    return len(text.split())


def reading_time_minutes(text):
    return max(5, round(word_count(text) / 200))


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)

    with open(SOURCE, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    # Strip newlines for processing
    lines = [l.rstrip("\n") for l in all_lines]
    sections = find_sections(lines)

    print(f"Found {len(sections)} sections:")
    for line_num, stype, sval in sections:
        print(f"  Line {line_num + 1}: {stype} {sval or ''}")

    # Build a map: section -> (start_line, end_line)
    section_ranges = {}
    for idx, (line_num, stype, sval) in enumerate(sections):
        end = sections[idx + 1][0] if idx + 1 < len(sections) else len(lines)
        key = f"{stype}:{sval}" if sval else stype
        section_ranges[key] = (line_num, end)

    file_num = 0
    total_words = 0

    # --- Preface (00-front-matter.md) ---
    if "preface" in section_ranges:
        start, end = section_ranges["preface"]
        # End at contents or first chapter, whichever comes first
        if "contents" in section_ranges:
            end = section_ranges["contents"][0]
        raw = "\n".join(lines[start:end])
        content = strip_preface_heading(raw)
        rt = reading_time_minutes(content)
        total_words += word_count(content)

        with open(OUTPUT / "00-front-matter.md", "w", encoding="utf-8") as f:
            f.write(f"""---
title: "Preface"
chapter_number: 0
weight: 0
reading_time: {rt}
---

{content}
""")
        print(f"  Created 00-front-matter.md ({rt} min)")

    # --- Chapters ---
    for ch_num in range(1, 9):
        key = f"chapter:{ch_num}"
        if key not in section_ranges:
            print(f"  WARNING: Chapter {ch_num} not found!")
            continue

        start, end = section_ranges[key]
        raw = "\n".join(lines[start:end])
        content = strip_chapter_headings(raw, is_chapter_v=(ch_num == 5))
        rt = reading_time_minutes(content)
        total_words += word_count(content)

        title, slug = CHAPTERS[ch_num]
        roman = ROMAN[ch_num]
        file_num = ch_num
        filename = f"{file_num:02d}-{slug}.md"

        with open(OUTPUT / filename, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "Chapter {roman}: {title}"
chapter_number: {ch_num}
weight: {ch_num}
reading_time: {rt}
---

{content}
""")
        print(f"  Created {filename} ({rt} min, {word_count(content)} words)")

    # --- Appendices ---
    app_letters = ["A", "B", "C", "D", "E"]
    for i, letter in enumerate(app_letters):
        key = f"appendix:{letter}"
        if key not in section_ranges:
            print(f"  WARNING: Appendix {letter} not found!")
            continue

        start, end = section_ranges[key]
        raw = "\n".join(lines[start:end])
        content = strip_appendix_heading(raw)
        rt = reading_time_minutes(content)
        total_words += word_count(content)

        title, slug = APPENDICES[letter]
        file_num = 9 + i
        filename = f"{file_num:02d}-appendix-{letter.lower()}-{slug}.md"

        with open(OUTPUT / filename, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "Appendix {letter}: {title}"
chapter_number: {file_num}
weight: {file_num}
reading_time: {rt}
---

{content}
""")
        print(f"  Created {filename} ({rt} min, {word_count(content)} words)")

    total_reading = round(total_words / 200 / 60, 1)
    print(f"\nTotal: {total_words} words, ~{total_reading} hours reading time")
    print(f"Files created in: {OUTPUT}")


if __name__ == "__main__":
    main()
