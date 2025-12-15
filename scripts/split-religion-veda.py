#!/usr/bin/env python3
"""
Split The Religion of the Veda into Hugo-compatible lecture files.
Splits by '## LECTURE THE' markers (H2), ignoring '### LECTURE THE' in TOC.
"""

import re
from pathlib import Path

# Define lecture titles from TOC
LECTURE_TITLES = {
    1: "India the Land of Religions—The Veda",
    2: "The Hieratic Religion—The Pantheon of the Veda",
    3: "The Prehistoric Gods",
    4: "The Transparent, Translucent, and Opaque Gods—Religious Conceptions and Religious Feeling in the Veda",
    5: "The Beginnings of Hindu Theosophy",
    6: "The Final Philosophy of the Veda"
}

# Read the source file
source_file = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/Akshara books/the-religion-of-the-veda.md")
output_dir = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/religion-of-the-veda")

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Find lecture boundaries (only H2 headings, not H3 in TOC)
lecture_info = []  # List of (line_number, lecture_number)

for i, line in enumerate(lines):
    # Match only ## LECTURE THE (H2), not ### (H3 in TOC)
    if re.match(r'^## LECTURE THE (FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH)', line):
        # Map ordinal to number
        ordinal_map = {
            'FIRST': 1, 'SECOND': 2, 'THIRD': 3,
            'FOURTH': 4, 'FIFTH': 5, 'SIXTH': 6
        }
        match = re.search(r'(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH)', line)
        if match:
            ordinal = match.group(1)
            lecture_num = ordinal_map.get(ordinal)
            if lecture_num:
                lecture_info.append((i, lecture_num))

print(f"Found {len(lecture_info)} lectures: {[lec[1] for lec in lecture_info]}")

# Extract front matter (everything before first lecture)
front_matter_end = lecture_info[0][0]
front_matter = '\n'.join(lines[10:front_matter_end])  # Skip YAML front matter from original

# Create front matter file
front_matter_content = f"""---
title: "Front Matter"
lecture_number: 0
weight: 0
reading_time: 15
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
    
    # Create filename
    filename_base = title.lower()
    filename_base = re.sub(r'[—,():.;]', '', filename_base)
    filename_base = re.sub(r'\s+', '-', filename_base).strip('-')
    filename_base = re.sub(r'-+', '-', filename_base)
    filename_base = filename_base[:50]  # Truncate long names
    
    # Estimate reading time (200 words per minute)
    word_count = len(lecture_text.split())
    reading_time = max(5, round(word_count / 200))
    
    # Create lecture file
    lecture_content = f"""---
title: "{title}"
lecture_number: {lecture_num}
weight: {lecture_num}
reading_time: {reading_time}
---

{lecture_text.strip()}
"""
    
    filename = f"{lecture_num:02d}-lecture-{lecture_num}.md"
    with open(output_dir / filename, 'w', encoding='utf-8') as f:
        f.write(lecture_content)
    
    print(f"✓ Created {filename} ({word_count} words)")

print(f"\n✅ Successfully split book into {len(lecture_info) + 1} files (front matter + {len(lecture_info)} lectures)")
