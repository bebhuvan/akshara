#!/usr/bin/env python3
"""
Split 'Indian Shipping' by Radhakumud Mookerji into Hugo-compatible chapter files.

Structure:
- Front matter: Preface + Introductory Note
- List of Authorities
- Introduction
- Book I, Part I: 3 chapters (evidences)
- Book I, Part II: 10 chapters (history)
- Book II: 4 chapters (Mahomedan period)
- Conclusion
- Indexes (skipped)
"""

import re
from pathlib import Path

SOURCE = Path("/home/bhuvanesh.r/Akshara Pandoc/History of Indian Shipping/history-of-indian-shipping.md")
OUTPUT = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/indian-shipping")

# Define all sections in order with their output file details.
# Format: (file_num, slug, display_title, section_type)
# section_type is used to find boundaries in the source.
SECTIONS = [
    # Front matter
    (0, "front-matter", "Front Matter", "preface"),
    (1, "list-of-authorities", "List of Authorities Consulted", "authorities"),
    (2, "introduction", "Introduction", "introduction"),
    # Book I, Part I
    (3, "direct-evidences-literature", "Direct Evidences from Sanskrit and Pali Literature", "b1p1_ch1"),
    (4, "direct-evidences-sculpture", "Direct Evidences from Indian Sculpture, Painting, and Coins", "b1p1_ch2"),
    (5, "indirect-evidences", "Indirect Evidences from Sanskrit and Pali Literature", "b1p1_ch3"),
    # Book I, Part II
    (6, "pre-mauryan-period", "The Pre-Mauryan Period", "b1p2_ch1"),
    (7, "maurya-period", "The Maurya Period", "b1p2_ch2"),
    (8, "andhra-kushan-period", "The Andhra-Kushan Period", "b1p2_ch3"),
    (9, "guptas-and-harshavardhana", "The Guptas and Harshavardhana", "b1p2_ch4"),
    (10, "colonization-of-java", "The Colonization of Java", "b1p2_ch5"),
    (11, "maritime-activity-bengalis", "The Maritime Activity of the Bengalis", "b1p2_ch6"),
    (12, "intercourse-with-china", "The Intercourse with China", "b1p2_ch7"),
    (13, "maritime-activity-west-coast", "Maritime Activity on the West Coast", "b1p2_ch8"),
    (14, "chalukyas-and-cholas", "The Chalukyas and the Cholas", "b1p2_ch9"),
    (15, "retrospect", "Retrospect", "b1p2_ch10"),
    # Book II
    (16, "pre-mogul-period", "The Pre-Mogul Period", "b2_ch1"),
    (17, "mogul-period-akbar", "The Mogul Period: The Reign of Akbar", "b2_ch2"),
    (18, "mogul-period-akbar-to-aurangzeb", "The Mogul Period: Akbar to Aurangzeb", "b2_ch3"),
    (19, "later-times", "Later Times", "b2_ch4"),
    # Conclusion
    (20, "conclusion", "Conclusion", "conclusion"),
]


def find_line(lines, pattern, start=0):
    """Find the first line matching pattern starting from start."""
    for i in range(start, len(lines)):
        if re.match(pattern, lines[i].strip()):
            return i
    return None


def find_all_chapter_starts(lines):
    """Find all ## CHAPTER lines and return their indices."""
    starts = []
    for i, line in enumerate(lines):
        if re.match(r'^##\s+CHAPTER\s+[IVXLC]+\.', line.strip()):
            starts.append(i)
    return starts


def strip_heading(text, patterns_to_strip):
    """Remove specified heading patterns from start of content."""
    lines = text.split("\n")
    cleaned = []
    stripped_count = 0

    for line in lines:
        stripped = line.strip()
        should_skip = False
        if stripped_count < len(patterns_to_strip):
            for pat in patterns_to_strip:
                if re.match(pat, stripped):
                    should_skip = True
                    stripped_count += 1
                    break
        if not should_skip:
            cleaned.append(line)

    # Remove leading blank lines and ---
    while cleaned and cleaned[0].strip() in ("", "---"):
        cleaned.pop(0)
    # Remove trailing blank lines
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
        lines = [l.rstrip("\n") for l in f.readlines()]

    # Find key section boundaries
    preface_line = find_line(lines, r'^##\s+PREFACE\.')
    intro_note_line = find_line(lines, r'^##\s+AN INTRODUCTORY NOTE')
    contents_line = find_line(lines, r'^###\s+CONTENTS\.')
    authorities_line = find_line(lines, r'^##\s+LIST OF AUTHORITIES')
    introduction_line = find_line(lines, r'^##\s+INTRODUCTION\.')
    conclusion_line = find_line(lines, r'^##\s+CONCLUSION\.')
    index1_line = find_line(lines, r'^##\s+INDEX I')
    index2_line = find_line(lines, r'^##\s+INDEX II')

    # Find all chapter starts
    chapter_starts = find_all_chapter_starts(lines)

    print(f"Preface: line {preface_line}")
    print(f"Introductory Note: line {intro_note_line}")
    print(f"Contents: line {contents_line}")
    print(f"Authorities: line {authorities_line}")
    print(f"Introduction: line {introduction_line}")
    print(f"Chapter starts: {chapter_starts}")
    print(f"Conclusion: line {conclusion_line}")
    print(f"Index I: line {index1_line}")
    print(f"Found {len(chapter_starts)} chapters total")

    # Map section types to (start_line, end_line)
    # Front matter = preface + introductory note (up to contents)
    section_bounds = {}
    section_bounds["preface"] = (preface_line, contents_line)
    section_bounds["authorities"] = (authorities_line, introduction_line)
    section_bounds["introduction"] = (introduction_line, chapter_starts[0])

    # Chapters: sequential by order found
    for i, ch_start in enumerate(chapter_starts):
        end = chapter_starts[i + 1] if i + 1 < len(chapter_starts) else conclusion_line
        # Determine which section this chapter belongs to
        if i < 3:
            key = f"b1p1_ch{i + 1}"
        elif i < 13:
            key = f"b1p2_ch{i - 3 + 1}"
        else:
            key = f"b2_ch{i - 13 + 1}"
        section_bounds[key] = (ch_start, end)

    section_bounds["conclusion"] = (conclusion_line, index1_line or len(lines))

    total_words = 0

    for file_num, slug, display_title, stype in SECTIONS:
        if stype not in section_bounds:
            print(f"  WARNING: {stype} not found!")
            continue

        start, end = section_bounds[stype]
        raw = "\n".join(lines[start:end])

        # Strip headings based on section type
        if stype == "preface":
            # Strip ## PREFACE. and ## AN INTRODUCTORY NOTE headings
            content = strip_heading(raw, [
                r'^##\s+PREFACE\.',
            ])
        elif stype == "authorities":
            content = strip_heading(raw, [r'^##\s+LIST OF AUTHORITIES'])
        elif stype == "introduction":
            content = strip_heading(raw, [r'^##\s+INTRODUCTION\.'])
        elif stype == "conclusion":
            content = strip_heading(raw, [r'^##\s+CONCLUSION\.'])
        elif stype.startswith("b"):
            # Chapter: strip ## CHAPTER N. and ### TITLE headings
            content = strip_heading(raw, [
                r'^##\s+CHAPTER\s+[IVXLC]+\.',
                r'^###\s+',
            ])
        else:
            content = raw

        rt = reading_time_minutes(content)
        wc = word_count(content)
        total_words += wc

        filename = f"{file_num:02d}-{slug}.md"

        with open(OUTPUT / filename, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{display_title}"
chapter_number: {file_num}
weight: {file_num}
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
