#!/usr/bin/env python3
"""
Script to export senior operator contacts to CSV file.
Extracts market-facing/executive level contacts from specification files.
"""
import csv
import re
from pathlib import Path

def extract_country_from_path(file_path):
    """Extract country name from file path."""
    parts = file_path.parts
    if 'Europe' in parts:
        idx = parts.index('Europe')
        if idx + 1 < len(parts):
            country = parts[idx + 1]
            return country.replace('-', ' ')
    return ""

def extract_operator_from_file(file_path):
    """Extract operator name from specification file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        for line in content.split('\n'):
            if '**Operator**:' in line:
                operator = line.split('**Operator**:')[1].strip()
                return operator
    return ""

def clean_text(text):
    """Clean text by removing markdown, extra whitespace, and newlines."""
    if not text:
        return ""
    # Remove markdown formatting
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\*', '', text)
    # Remove newlines and extra whitespace
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_senior_contacts(file_path):
    """Extract senior contacts from specification file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    contacts = []
    country = extract_country_from_path(file_path)
    operator = extract_operator_from_file(file_path)
    
    # Look for "### Detailed Contacts by Role" section
    if "### Detailed Contacts by Role" in content:
        # Extract Market-Facing / Executive section
        exec_section_match = re.search(
            r'#### Market-Facing / Executive\s*\n\n(.*?)(?=\n####|\n###|$)',
            content,
            re.DOTALL
        )
        
        if exec_section_match:
            exec_section = exec_section_match.group(1)
            # Find all contact blocks (each starts with **role**)
            contact_pattern = r'\*\*([^*]+)\*\*\s*\n- \*\*Name\*\*:\s*(.+?)\s*\n- \*\*Title\*\*:\s*(.+?)(?:\n|$)'
            matches = re.finditer(contact_pattern, exec_section, re.DOTALL)
            for match in matches:
                role = clean_text(match.group(1))
                name = clean_text(match.group(2))
                title = clean_text(match.group(3))
                
                if name and name.upper() != "OPEN":
                    contacts.append({
                        'name': name,
                        'title': title,
                        'position': role,
                        'company': operator,
                        'country': country
                    })
        
        # Also check Market-Facing / Content section
        content_section_match = re.search(
            r'#### Market-Facing / Content\s*\n\n(.*?)(?=\n####|\n###|$)',
            content,
            re.DOTALL
        )
        
        if content_section_match:
            content_section = content_section_match.group(1)
            contact_pattern = r'\*\*([^*]+)\*\*\s*\n- \*\*Name\*\*:\s*(.+?)\s*\n- \*\*Title\*\*:\s*(.+?)(?:\n|$)'
            matches = re.finditer(contact_pattern, content_section, re.DOTALL)
            for match in matches:
                role = clean_text(match.group(1))
                name = clean_text(match.group(2))
                title = clean_text(match.group(3))
                
                if name and name.upper() != "OPEN":
                    contacts.append({
                        'name': name,
                        'title': title,
                        'position': role,
                        'company': operator,
                        'country': country
                    })
    
    # Also check Key Contacts section (from earlier format) - look for CEO, Director, Head, etc.
    key_contacts_pattern = r'### Key Contacts\s*\n\n(.*?)(?=\n### Recommended|\n### Access|\n##|$)'
    key_match = re.search(key_contacts_pattern, content, re.DOTALL)
    
    if key_match:
        key_section = key_match.group(1)
        # Pattern for contacts with Name and Title
        pattern = r'\*\*([^*]+)\*\*\s*\n- \*\*Name\*\*:\s*(.+?)\s*\n- \*\*Title\*\*:\s*(.+?)(?:\n|$)'
        matches = re.finditer(pattern, key_section, re.DOTALL)
        for match in matches:
            role = clean_text(match.group(1))
            name = clean_text(match.group(2))
            title = clean_text(match.group(3))
            
            # Only include if title contains senior keywords
            if name and name.upper() != "OPEN" and any(keyword in title.lower() for keyword in ['ceo', 'director', 'head', 'cto', 'president', 'managing', 'chief']):
                contacts.append({
                    'name': name,
                    'title': title,
                    'position': role,
                    'company': operator,
                    'country': country
                })
    
    return contacts

# Process all specification files
base_path = Path('Europe')
spec_files = list(base_path.rglob('specifications.md'))

all_contacts = []

print(f"Processing {len(spec_files)} specification files...\n")

for spec_file in spec_files:
    contacts = extract_senior_contacts(spec_file)
    all_contacts.extend(contacts)
    if contacts:
        print(f"Found {len(contacts)} senior contact(s) in {spec_file.parent.name}")

# Remove duplicates (same name, title, company)
seen = set()
unique_contacts = []
for contact in all_contacts:
    key = (contact['name'].lower(), contact['title'].lower(), contact['company'].lower())
    if key not in seen:
        seen.add(key)
        unique_contacts.append(contact)

# Sort by country, then company, then name
unique_contacts.sort(key=lambda x: (x['country'], x['company'], x['name']))

# Write to CSV
csv_file = 'Europe/Operator-Senior-Contacts.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['name', 'title', 'position', 'company', 'country']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    for contact in unique_contacts:
        writer.writerow(contact)

print(f"\n✅ Exported {len(unique_contacts)} senior contacts to {csv_file}")
print(f"\nColumns: name, title, position, company, country")
print(f"\nFile location: {csv_file}")

