#!/usr/bin/env python3
"""
Split "India: What Can It Teach Us?" into Hugo-compatible lecture files.
Handles both H1 and H2 LECTURE headings.
"""

import re
from pathlib import Path

# Define lecture titles from TOC
LECTURE_TITLES = {
    1: "What Can India Teach Us?",
    2: "On the Truthful Character of the Hindus",
    3: "The Human Interest of Sanskrit Literature",
    4: "Objections",
    5: "The Lessons of the Veda",
    6: "Vedic Deities",
    7: "Veda and Vedanta"
}

# Read the source file
source_file = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/Akshara books/India- What Can It Teach Us?.md")
output_dir = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/india-what-can-it-teach-us")

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Find lecture boundaries - match both H1 and H2 LECTURE headings
# Skip TOC entries which are in table format (| LECTURE ...)
lecture_info = []  # List of (line_number, lecture_number)

# Map roman numerals to integers
ROMAN_TO_INT = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7
}

for i, line in enumerate(lines):
    # Match only actual headings (# or ##), not TOC table entries
    match = re.match(r'^#{1,2}\s+LECTURE\s+([IVX]+)[.:]?\s*', line)
    if match:
        roman = match.group(1)
        lecture_num = ROMAN_TO_INT.get(roman)
        if lecture_num and lecture_num not in [lec[1] for lec in lecture_info]:
            lecture_info.append((i, lecture_num))

# Sort by line number to ensure correct order
lecture_info.sort(key=lambda x: x[0])

print(f"Found {len(lecture_info)} lectures at lines: {[(lec[0]+1, f'Lecture {lec[1]}') for lec in lecture_info]}")

# Extract front matter (everything before first lecture)
front_matter_end = lecture_info[0][0]
front_matter = '\n'.join(lines[10:front_matter_end])  # Skip YAML front matter from original

# Create front matter file
front_matter_content = f"""---
title: "Front Matter"
chapter_number: 0
weight: 0
reading_time: 20
---

{front_matter.strip()}
"""

with open(output_dir / "00-front-matter.md", 'w', encoding='utf-8') as f:
    f.write(front_matter_content)

print("✓ Created front matter")

# Extract each lecture
for idx in range(len(lecture_info)):
    start_line, lecture_num = lecture_info[idx]
    
    # Determine end line
    if idx + 1 < len(lecture_info):
        end_line = lecture_info[idx + 1][0]
    else:
        end_line = len(lines)
    
    lecture_lines = lines[start_line:end_line]
    lecture_text = '\n'.join(lecture_lines)
    
    # Get title from our predefined mapping
    title = LECTURE_TITLES.get(lecture_num, f"Lecture {lecture_num}")
    
    # Estimate reading time (200 words per minute)
    word_count = len(lecture_text.split())
    reading_time = max(5, round(word_count / 200))
    
    # Create lecture file
    lecture_content = f"""---
title: "Lecture {lecture_num}: {title}"
chapter_number: {lecture_num}
weight: {lecture_num}
reading_time: {reading_time}
---

{lecture_text.strip()}
"""
    
    filename = f"{lecture_num:02d}-lecture-{lecture_num}.md"
    with open(output_dir / filename, 'w', encoding='utf-8') as f:
        f.write(lecture_content)
    
    print(f"✓ Created {filename}: {title} ({word_count} words)")

print(f"\n✅ Successfully split book into {len(lecture_info) + 1} files (front matter + {len(lecture_info)} lectures)")
