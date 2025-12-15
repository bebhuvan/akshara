#!/usr/bin/env python3
"""
Split A Brief History of Indian Peoples into Hugo-compatible chapter files.
Uses proper chapter titles from the Table of Contents.
Handles special cases for chapters 15-16 which don't have "CHAPTER" prefix.
"""

import re
from pathlib import Path

# Define chapter titles from TOC (matching the book's table of contents)
CHAPTER_TITLES = {
    1: "The Country",
    2: "The People",
    3: "The Non-Aryans",
    4: "The Aryans in India",
    5: "Buddhism—543 B.C. to 1000 A.D.",
    6: "The Greeks in India, 327 to 161 B.C.",
    7: "The Scythic Inroads, from about 100 B.C. to 500 A.D.",
    8: "Growth of Hinduism, 700 to 1500 A.D.",
    9: "Early Muhammadan Conquerors, 714-1526 A.D.",
    10: "The Mughal Dynasty, 1526-1761",
    11: "The Marathas",
    12: "Early European Settlements",
    13: "The Foundation of British Rule in India",
    14: "The Consolidation of British India",
    15: "The Sepoy Mutiny of 1857",
    16: "India Under the British Crown, 1858-1892"
}

# Filename overrides for cleaner names
FILENAME_OVERRIDES = {
    15: "sepoy-mutiny",
    16: "india-under-british-crown"
}

# Roman numeral conversion
ROMAN_TO_INT = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
    'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
    'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15, 'XVI': 16
}

# Read the source file
source_file = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/Akshara books/A Brief History Of The Indian Peoples.md")
output_dir = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/brief-history-indian-peoples")

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by chapter markers
lines = content.split('\n')

# Find chapter boundaries (both standard and special cases)
chapter_info = []  # List of (line_number, chapter_number)

for i, line in enumerate(lines):
    # Match standard chapter headings: ## CHAPTER or # CHAPTER
    match = re.match(r'^#{1,2} CHAPTER ([IVXLCDM]+)', line)
    if match:
        roman_num = match.group(1)
        chapter_num = ROMAN_TO_INT.get(roman_num)
        if chapter_num:
            chapter_info.append((i, chapter_num))
    # Special case for Chapter 15
    elif re.match(r'^## THE SEPOY MUTINY', line):
        chapter_info.append((i, 15))
    # Special case for Chapter 16
    elif re.match(r'^## INDIA UNDER THE BRITISH CROWN', line):
        chapter_info.append((i, 16))

print(f"Found {len(chapter_info)} chapters: {[ch[1] for ch in chapter_info]}")

# Extract front matter (everything before first chapter)
front_matter_end = chapter_info[0][0]
front_matter = '\n'.join(lines[10:front_matter_end])  # Skip YAML front matter from original

# Create front matter file
front_matter_content = f"""---
title: "Front Matter"
chapter_number: 0
weight: 0
reading_time: 10
---

{front_matter.strip()}
"""

with open(output_dir / "00-front-matter.md", 'w', encoding='utf-8') as f:
    f.write(front_matter_content)

print("✓ Created front matter")

# Extract each chapter
for idx in range(len(chapter_info)):
    start_line, chapter_num = chapter_info[idx]
    
    # Determine end line (next chapter start or end of file)
    if idx + 1 < len(chapter_info):
        end_line = chapter_info[idx + 1][0]
    else:
        end_line = len(lines)
    
    chapter_lines = lines[start_line:end_line]
    chapter_text = '\n'.join(chapter_lines)
    
    # Get title from our predefined mapping
    title = CHAPTER_TITLES.get(chapter_num, f"Chapter {chapter_num}")
    
    # Create filename - use override if available, otherwise generate
    if chapter_num in FILENAME_OVERRIDES:
        filename_base = FILENAME_OVERRIDES[chapter_num]
    else:
        filename_base = title.lower()
        # Remove dates, special chars
        filename_base = re.sub(r'\d{2,4}', '', filename_base)  # Remove years
        filename_base = re.sub(r'[—,():.;]', '', filename_base)  # Remove punctuation
        filename_base = re.sub(r'\s+', '-', filename_base).strip('-')
        filename_base = re.sub(r'-+', '-', filename_base)
        filename_base = re.sub(r'^the-', '', filename_base)  # Remove leading "the-"
    
    # Estimate reading time (200 words per minute)
    word_count = len(chapter_text.split())
    reading_time = max(5, round(word_count / 200))
    
    # Create chapter file
    chapter_content = f"""---
title: "{title}"
chapter_number: {chapter_num}
weight: {chapter_num}
reading_time: {reading_time}
---

{chapter_text.strip()}
"""
    
    filename = f"{chapter_num:02d}-{filename_base}.md"
    with open(output_dir / filename, 'w', encoding='utf-8') as f:
        f.write(chapter_content)
    
    print(f"✓ Created {filename}")

print(f"\n✅ Successfully split book into {len(chapter_info) + 1} files (front matter + {len(chapter_info)} chapters)")
