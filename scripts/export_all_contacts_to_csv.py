#!/usr/bin/env python3
"""
Script to export ALL operator contacts to CSV file.
Extracts all contacts from specification files across all role categories.
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

def extract_all_contacts(file_path):
    """Extract all contacts from specification file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    contacts = []
    country = extract_country_from_path(file_path)
    operator = extract_operator_from_file(file_path)
    
    # Look for "### Detailed Contacts by Role" section
    if "### Detailed Contacts by Role" in content:
        # Extract all role sections
        role_sections = [
            ('Market-Facing / Executive', r'#### Market-Facing / Executive\s*\n\n(.*?)(?=\n####|\n###|$)'),
            ('Market-Facing / Content', r'#### Market-Facing / Content\s*\n\n(.*?)(?=\n####|\n###|$)'),
            ('Technology / Specifications', r'#### Technology / Specifications\s*\n\n(.*?)(?=\n####|\n###|$)'),
            ('Onboarding / Device Certification', r'#### Onboarding / Device Certification\s*\n\n(.*?)(?=\n####|\n###|$)'),
            ('Product Leadership', r'#### Product Leadership\s*\n\n(.*?)(?=\n####|\n###|$)'),
            ('TV Product / Platform', r'#### TV Product / Platform\s*\n\n(.*?)(?=\n####|\n###|$)'),
            ('Other', r'#### Other\s*\n\n(.*?)(?=\n####|\n###|$)'),
        ]
        
        for category, pattern in role_sections:
            section_match = re.search(pattern, content, re.DOTALL)
            if section_match:
                section = section_match.group(1)
                # Find all contact blocks (each starts with **role**)
                contact_pattern = r'\*\*([^*]+)\*\*\s*\n- \*\*Name\*\*:\s*(.+?)\s*\n- \*\*Title\*\*:\s*(.+?)(?:\n|$)'
                matches = re.finditer(contact_pattern, section, re.DOTALL)
                for match in matches:
                    role = clean_text(match.group(1))
                    name = clean_text(match.group(2))
                    title = clean_text(match.group(3))
                    
                    if name and name.upper() != "OPEN":
                        # Extract source if available
                        source_match = re.search(r'- \*\*Source\*\*:\s*(.+?)(?:\n|$)', section[match.end():match.end()+200], re.DOTALL)
                        source = clean_text(source_match.group(1)) if source_match else ""
                        
                        contacts.append({
                            'name': name,
                            'title': title,
                            'position': role,
                            'category': category,
                            'company': operator,
                            'country': country,
                            'source': source
                        })
    
    # Also check Key Contacts section (from earlier format)
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
            
            if name and name.upper() != "OPEN":
                # Extract source if available
                source_match = re.search(r'- \*\*Source\*\*:\s*(.+?)(?:\n|$)', key_section[match.end():match.end()+200], re.DOTALL)
                source = clean_text(source_match.group(1)) if source_match else ""
                
                # Determine category based on role/title
                category = "Other"
                if any(keyword in role.lower() or keyword in title.lower() for keyword in ['ceo', 'president', 'exec', 'managing']):
                    category = "Market-Facing / Executive"
                elif any(keyword in role.lower() or keyword in title.lower() for keyword in ['content', 'marketing', 'programming']):
                    category = "Market-Facing / Content"
                elif any(keyword in role.lower() or keyword in title.lower() for keyword in ['technology', 'technical', 'cto', 'spec', 'platform']):
                    category = "Technology / Specifications"
                elif any(keyword in role.lower() or keyword in title.lower() for keyword in ['onboarding', 'device', 'certification']):
                    category = "Onboarding / Device Certification"
                elif any(keyword in role.lower() or keyword in title.lower() for keyword in ['product']):
                    category = "Product Leadership"
                
                contacts.append({
                    'name': name,
                    'title': title,
                    'position': role,
                    'category': category,
                    'company': operator,
                    'country': country,
                    'source': source
                })
    
    return contacts

# Process all specification files
base_path = Path('Europe')
spec_files = list(base_path.rglob('specifications.md'))

all_contacts = []

print(f"Processing {len(spec_files)} specification files...\n")

for spec_file in spec_files:
    contacts = extract_all_contacts(spec_file)
    all_contacts.extend(contacts)
    if contacts:
        print(f"Found {len(contacts)} contact(s) in {spec_file.parent.name}")

# Remove duplicates (same name, title, company)
seen = set()
unique_contacts = []
for contact in all_contacts:
    key = (contact['name'].lower(), contact['title'].lower(), contact['company'].lower())
    if key not in seen:
        seen.add(key)
        unique_contacts.append(contact)

# Sort by country, then company, then category, then name
unique_contacts.sort(key=lambda x: (x['country'], x['company'], x['category'], x['name']))

# Write to CSV
csv_file = 'Europe/Operator-All-Contacts.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['name', 'title', 'position', 'category', 'company', 'country', 'source']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    for contact in unique_contacts:
        writer.writerow(contact)

print(f"\n✅ Exported {len(unique_contacts)} contacts to {csv_file}")
print(f"\nColumns: name, title, position, category, company, country, source")
print(f"\nFile location: {csv_file}")

# Print summary by category
print(f"\nContacts by category:")
categories = {}
for contact in unique_contacts:
    cat = contact['category']
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {count}")

