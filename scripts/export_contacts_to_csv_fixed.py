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
        exec_pattern = r'#### Market-Facing / Executive\s*\n\n(.*?)(?=\n####|\n###|$)'
        exec_match = re.search(exec_pattern, content, re.DOTALL)
        
        if exec_match:
            exec_section = exec_match.group(1)
            # Extract individual contacts - improved pattern
            contact_blocks = re.split(r'\*\*([^*]+)\*\*', exec_section)
            for i in range(1, len(contact_blocks), 2):
                if i + 1 < len(contact_blocks):
                    role = clean_text(contact_blocks[i])
                    contact_text = contact_blocks[i + 1]
                    
                    # Extract name
                    name_match = re.search(r'- \*\*Name\*\*:\s*(.+?)(?:\n|$)', contact_text)
                    if not name_match:
                        continue
                    name = clean_text(name_match.group(1))
                    
                    if name and name.upper() != "OPEN":
                        # Extract title
                        title_match = re.search(r'- \*\*Title\*\*:\s*(.+?)(?:\n|$)', contact_text)
                        title = clean_text(title_match.group(1)) if title_match else ""
                        
                        contacts.append({
                            'name': name,
                            'title': title,
                            'position': role,
                            'company': operator,
                            'country': country
                        })
        
        # Also check Market-Facing / Content section
        content_pattern = r'#### Market-Facing / Content\s*\n\n(.*?)(?=\n####|\n###|$)'
        content_match = re.search(content_pattern, content, re.DOTALL)
        
        if content_match:
            content_section = content_match.group(1)
            contact_blocks = re.split(r'\*\*([^*]+)\*\*', content_section)
            for i in range(1, len(contact_blocks), 2):
                if i + 1 < len(contact_blocks):
                    role = clean_text(contact_blocks[i])
                    contact_text = contact_blocks[i + 1]
                    
                    name_match = re.search(r'- \*\*Name\*\*:\s*(.+?)(?:\n|$)', contact_text)
                    if not name_match:
                        continue
                    name = clean_text(name_match.group(1))
                    
                    if name and name.upper() != "OPEN":
                        title_match = re.search(r'- \*\*Title\*\*:\s*(.+?)(?:\n|$)', contact_text)
                        title = clean_text(title_match.group(1)) if title_match else ""
                        
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

