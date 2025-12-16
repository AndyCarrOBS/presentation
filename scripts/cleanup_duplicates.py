#!/usr/bin/env python3
"""
Script to remove duplicate Key Contacts sections from specification files.
"""
import re
from pathlib import Path

def remove_duplicate_contacts(file_path):
    """Remove duplicate Key Contacts sections."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all "### Key Contacts" sections
    pattern = r'### Key Contacts\n\n'
    matches = list(re.finditer(pattern, content))
    
    if len(matches) > 1:
        # Keep the first one, remove duplicates
        first_end = matches[0].end()
        second_start = matches[1].start()
        
        # Find the end of the first Key Contacts section (before next ### or ##)
        first_section_end = content.find('###', first_end)
        if first_section_end == -1:
            first_section_end = content.find('##', first_end)
        if first_section_end == -1:
            first_section_end = len(content)
        
        # Find the end of the second Key Contacts section
        second_section_end = content.find('###', second_start + 1)
        if second_section_end == -1:
            second_section_end = content.find('##', second_start + 1)
        if second_section_end == -1:
            second_section_end = len(content)
        
        # Remove the duplicate section
        new_content = content[:first_section_end] + content[second_section_end:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False

# Process all specification files
base_path = Path('Europe')
spec_files = list(base_path.rglob('specifications.md'))

cleaned = 0
for spec_file in spec_files:
    if remove_duplicate_contacts(spec_file):
        cleaned += 1
        print(f"Cleaned: {spec_file}")

print(f"\nCleaned {cleaned} files with duplicate sections")

