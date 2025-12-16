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

def extract_senior_contacts(file_path):
    """Extract senior contacts from specification file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    contacts = []
    country = extract_country_from_path(file_path)
    operator = extract_operator_from_file(file_path)
    
    # Look for "### Detailed Contacts by Role" section
    if "### Detailed Contacts by Role" not in content:
        return contacts
    
    # Extract Market-Facing / Executive section
    exec_pattern = r'#### Market-Facing / Executive\s*\n\n(.*?)(?=\n####|\n###|$)'
    exec_match = re.search(exec_pattern, content, re.DOTALL)
    
    if exec_match:
        exec_section = exec_match.group(1)
        # Extract individual contacts
        contact_pattern = r'\*\*(.*?)\*\*\s*\n- \*\*Name\*\*: (.*?)\s*\n- \*\*Title\*\*: (.*?)\s*\n'
        matches = re.finditer(contact_pattern, exec_section, re.DOTALL)
        for match in matches:
            role = match.group(1).strip()
            name = match.group(2).strip()
            title = match.group(3).strip()
            if name and name != "OPEN":
                contacts.append({
                    'name': name,
                    'title': title,
                    'position': role,
                    'company': operator,
                    'country': country
                })
    
    # Also check for Market-Facing / Content section (senior level)
    content_pattern = r'#### Market-Facing / Content\s*\n\n(.*?)(?=\n####|\n###|$)'
    content_match = re.search(content_pattern, content, re.DOTALL)
    
    if content_match:
        content_section = content_match.group(1)
        contact_pattern = r'\*\*(.*?)\*\*\s*\n- \*\*Name\*\*: (.*?)\s*\n- \*\*Title\*\*: (.*?)\s*\n'
        matches = re.finditer(contact_pattern, content_section, re.DOTALL)
        for match in matches:
            role = match.group(1).strip()
            name = match.group(2).strip()
            title = match.group(3).strip()
            if name and name != "OPEN":
                contacts.append({
                    'name': name,
                    'title': title,
                    'position': role,
                    'company': operator,
                    'country': country
                })
    
    # Also check Key Contacts section (from earlier format)
    key_contacts_pattern = r'### Key Contacts\s*\n\n(.*?)(?=\n###|\n##|$)'
    key_match = re.search(key_contacts_pattern, content, re.DOTALL)
    
    if key_match:
        key_section = key_match.group(1)
        # Look for CEO, Director, Head of, etc.
        senior_patterns = [
            r'\*\*(.*?)\*\*\s*\n- \*\*Name\*\*: (.*?)\s*\n- \*\*Title\*\*: (.*?)\s*\n',
            r'\*\*(.*?)\*\*\s*\n- (.*?) - (.*?)\s*\n',
        ]
        for pattern in senior_patterns:
            matches = re.finditer(pattern, key_section, re.DOTALL)
            for match in matches:
                role = match.group(1).strip()
                name = match.group(2).strip()
                title = match.group(3).strip() if len(match.groups()) >= 3 else ""
                # Only include if title contains senior keywords
                if name and name != "OPEN" and any(keyword in title.lower() for keyword in ['ceo', 'director', 'head', 'cto', 'president', 'managing']):
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
    key = (contact['name'], contact['title'], contact['company'])
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

