#!/usr/bin/env python3
"""
Split The Rig-Veda and Vedic Religion into Hugo chapter files
"""

import re
from pathlib import Path

# Source and destination
source_file = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/Akshara books/the-rig-veda-and-vedic-religion.md")
dest_dir = Path("/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/rig-veda-vedic-religion")

# Read the source file
with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by the main section markers
lines = content.split('\n')

# Define chapter boundaries based on the grep results
chapters = [
    {
        'number': 0,
        'filename': '00-front-matter.md',
        'title': 'Front Matter',
        'start_line': 0,
        'end_line': 114  # Before "## I. THE ARYANS"
    },
    {
        'number': 1,
        'filename': '01-the-aryans.md',
        'title': 'The Aryans',
        'start_line': 115,
        'end_line': 307  # Before "## II. THE VEDAS"
    },
    {
        'number': 2,
        'filename': '02-the-vedas-of-the-aryans.md',
        'title': 'The Vedas of the Aryans',
        'start_line': 308,
        'end_line': 548  # Before "## III. THE NATURE"
    },
    {
        'number': 3,
        'filename': '03-nature-of-vedic-gods.md',
        'title': 'The Nature of Vedic Gods',
        'start_line': 549,
        'end_line': 694  # Before "## IV. A CLASSIFIED ACCOUNT"
    },
    {
        'number': 4,
        'filename': '04-classified-account-vedic-gods.md',
        'title': 'A Classified Account of the Vedic Gods',
        'start_line': 695,
        'end_line': 1179  # Before "## V. THE SACRIFICES"
    },
    {
        'number': 5,
        'filename': '05-sacrifices-of-the-aryans.md',
        'title': 'The Sacrifices of the Aryans',
        'start_line': 1180,
        'end_line': 1468  # Before "## VI. THE PRAYERS"
    },
    {
        'number': 6,
        'filename': '06-prayers-of-the-aryans.md',
        'title': 'The Prayers of the Aryans',
        'start_line': 1469,
        'end_line': 1854  # Before "## VII. THE MESSAGE"
    },
    {
        'number': 7,
        'filename': '07-message-of-rig-veda.md',
        'title': 'The Message of the Rig-Veda',
        'start_line': 1855,
        'end_line': 2100  # Approximate - need to find "READINGS FROM THE VEDA"
    },
]

# Function to estimate reading time
def estimate_reading_time(text):
    words = len(text.split())
    minutes = max(1, words // 200)
    return f"{minutes} min"

# Create each chapter file
for chapter in chapters:
    chapter_lines = lines[chapter['start_line']:chapter['end_line']]
    chapter_content = '\n'.join(chapter_lines)
    
    # Remove the Project Akshara header if present
    chapter_content = re.sub(r'^---\ntitle:.*?---\n\n---\n\n\*\*About This Edition\*\*.*?---\n\n', '', chapter_content, flags=re.DOTALL)
    
    # Clean up the content
    chapter_content = chapter_content.strip()
    
    # Create frontmatter
    frontmatter = f"""---
title: "{chapter['title']}"
chapter_number: {chapter['number']}
weight: {chapter['number']}
reading_time: "{estimate_reading_time(chapter_content)}"
---

"""
    
    # Write the file
    output_file = dest_dir / chapter['filename']
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter + chapter_content)
    
    print(f"Created: {chapter['filename']} ({len(chapter_lines)} lines)")

print("\nChapter files created successfully!")
