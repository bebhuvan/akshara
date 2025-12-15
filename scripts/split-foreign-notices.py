#!/usr/bin/env python3
"""
Script to split 'Foreign Notices of South India' into chapters
"""

import re
import os
from pathlib import Path

# Configuration
SOURCE_FILE = "/home/bhuvanesh.r/Desktop/FOREIGN NOTICES OF SOUTH INDIA.md"
OUTPUT_DIR = "/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/foreign-notices-south-india/chapters"
WORDS_PER_MINUTE = 200

def count_words(text):
    """Count words in text"""
    return len(text.split())

def estimate_reading_time(word_count):
    """Estimate reading time in minutes"""
    return max(1, round(word_count / WORDS_PER_MINUTE))

def clean_title(title):
    """Clean title for filename"""
    # Remove section numbers and clean up
    title = re.sub(r'^[IVX]+\.\s*', '', title)  # Remove Roman numerals
    title = re.sub(r'^\d+\.\s*', '', title)  # Remove numbers
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s-]', '', title)  # Remove special chars
    title = re.sub(r'\s+', '-', title)  # Replace spaces with hyphens
    title = re.sub(r'-+', '-', title)  # Collapse multiple hyphens
    return title.strip('-')[:50]  # Limit length

def parse_book():
    """Parse the book into chapter segments"""
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    chapters = []
    current_chapter = None
    chapter_number = 0

    # Pattern to match main section headers:
    # Both ### I. TITLE and # I. TITLE (single # used in later sections)
    main_section_pattern = re.compile(r'^(#{1,3})\s+([IVX]+)\.\s+(.+)$')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this is a main section header
        match = main_section_pattern.match(line)

        if match:
            hash_marks = match.group(1)
            roman_num = match.group(2)
            title = match.group(3).strip()

            # Only treat as main chapter if it's # or ### (not ####)
            # This filters out subsections like #### A. or #### B.
            if len(hash_marks) <= 3 and not re.match(r'^[A-Z]\.\s+', title):
                # Save previous chapter if exists
                if current_chapter:
                    chapters.append(current_chapter)

                # Start new chapter
                chapter_number += 1

                current_chapter = {
                    'number': chapter_number,
                    'title': title,
                    'roman': roman_num,
                    'content': [line],
                    'start_line': i
                }
            elif current_chapter:
                # This is a subsection, add to current chapter
                current_chapter['content'].append(line)
        elif current_chapter:
            # Add line to current chapter
            current_chapter['content'].append(line)

        i += 1

    # Don't forget last chapter
    if current_chapter:
        chapters.append(current_chapter)

    # Handle front matter (everything before first section)
    front_matter_end = chapters[0]['start_line'] if chapters else len(lines)
    front_matter_content = '\n'.join(lines[:front_matter_end])

    # Split front matter into logical sections
    # 1. Preface & Bibliography (up to Introduction)
    # 2. Introduction

    intro_match = re.search(r'^## INTRODUCTION$', front_matter_content, re.MULTILINE)
    if intro_match:
        intro_start = intro_match.start()

        # Preface & Bibliography chapter
        preface_content = front_matter_content[:intro_start].strip()
        intro_content = front_matter_content[intro_start:].strip()

        front_chapters = [
            {
                'number': 0,
                'title': 'Preface and Bibliography',
                'content': preface_content.split('\n'),
                'roman': ''
            },
            {
                'number': 0.5,
                'title': 'Introduction',
                'content': intro_content.split('\n'),
                'roman': ''
            }
        ]

        # Prepend front chapters
        chapters = front_chapters + chapters

    return chapters

def generate_chapter_files():
    """Generate individual chapter markdown files"""

    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Parse book
    chapters = parse_book()

    print(f"Found {len(chapters)} chapters\n")

    for idx, chapter in enumerate(chapters):
        # Prepare chapter content
        content_text = '\n'.join(chapter['content'])
        word_count = count_words(content_text)
        reading_time = estimate_reading_time(word_count)

        # Determine chapter number for filename
        if chapter['number'] == 0:
            file_num = "00"
        elif chapter['number'] == 0.5:
            file_num = "01"
        else:
            file_num = f"{int(chapter['number']):02d}"

        # Actual display number (for navigation)
        display_num = idx

        # Clean title for filename
        clean_title_str = clean_title(chapter['title'])
        filename = f"{file_num}-{clean_title_str}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Determine next/prev chapters
        next_chapter = ""
        prev_chapter = ""

        if idx > 0:
            prev_ch = chapters[idx - 1]
            prev_num = "00" if prev_ch['number'] == 0 else "01" if prev_ch['number'] == 0.5 else f"{int(prev_ch['number']):02d}"
            prev_title_clean = clean_title(prev_ch['title'])
            prev_chapter = f"/books/foreign-notices-south-india/chapters/{prev_num}-{prev_title_clean}"

        if idx < len(chapters) - 1:
            next_ch = chapters[idx + 1]
            next_num = "00" if next_ch['number'] == 0 else "01" if next_ch['number'] == 0.5 else f"{int(next_ch['number']):02d}"
            next_title_clean = clean_title(next_ch['title'])
            next_chapter = f"/books/foreign-notices-south-india/chapters/{next_num}-{next_title_clean}"

        # Generate front matter
        front_matter = f"""---
title: "{chapter['title']}"
chapter_number: {display_num}
chapter_title: "{chapter.get('roman', '')}"
reading_time: {reading_time}
word_count: {word_count}
weight: {idx}

# Navigation
"""

        if next_chapter:
            front_matter += f'next: "{next_chapter}"\n'
        if prev_chapter:
            front_matter += f'prev: "{prev_chapter}"\n'

        front_matter += "---\n\n"

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(front_matter)
            f.write(content_text)

        print(f"✓ Created: {filename} ({word_count} words, ~{reading_time} min)")

    print(f"\n✓ Successfully created {len(chapters)} chapter files in {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_chapter_files()
