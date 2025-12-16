#!/usr/bin/env python3
"""
Script to generate likely email addresses for Proximus contacts based on common patterns.
"""
import re

# Proximus contacts with their full names
contacts = [
    {
        "name": "Antoine Noël",
        "title": "Senior Engineer at Belgacom",
        "firstname": "Antoine",
        "lastname": "Noël",
        "location": "Belgium",
        "note": "Belgacom (now Proximus)"
    },
    {
        "name": "Raymond WULLEMAN",
        "title": "Retired at Proximus",
        "firstname": "Raymond",
        "lastname": "WULLEMAN",
        "location": "Belgium",
        "note": "Retired - may not have active email"
    },
    {
        "name": "Gary McCullough",
        "title": "Senior Global Programs Manager - Channel Partners at Equinix",
        "firstname": "Gary",
        "lastname": "McCullough",
        "location": "Belgium",
        "note": "Currently at Equinix, may have been at Proximus"
    },
    {
        "name": "Jacques Ruckert",
        "title": "Chief Solutions & Innovation Officer at Proximus Luxembourg",
        "firstname": "Jacques",
        "lastname": "Ruckert",
        "location": "Luxembourg"
    },
    {
        "name": "Gilles Roelants",
        "title": "Customer Experience & Sales Efficiency Product Owner Lead",
        "firstname": "Gilles",
        "lastname": "Roelants",
        "location": "Belgium"
    },
    {
        "name": "João Sousa Guerreiro",
        "title": "Product & Brand Marketing Director",
        "firstname": "João",
        "middle": "Sousa",
        "lastname": "Guerreiro",
        "location": "Belgium"
    },
    {
        "name": "Clément Toukal",
        "title": "Product manager | Design Thinking & Agile Coach | Professional Trainer",
        "firstname": "Clément",
        "lastname": "Toukal",
        "location": "Belgium"
    },
    {
        "name": "Robin Belliere",
        "title": "Product Expert In-Home Solutions at Proximus",
        "firstname": "Robin",
        "lastname": "Belliere",
        "location": "Belgium"
    },
    {
        "name": "Véronique Dardenne",
        "title": "buyer at Proximus",
        "firstname": "Véronique",
        "lastname": "Dardenne",
        "location": "Belgium"
    },
    {
        "name": "Gert Marien",
        "title": "Corporate Innovation Manager at Proximus",
        "firstname": "Gert",
        "lastname": "Marien",
        "location": "Belgium"
    },
    {
        "name": "Benoît Gilot",
        "title": "Corporate Strategy Manager at Proximus Group",
        "firstname": "Benoît",
        "lastname": "Gilot",
        "location": "Belgium"
    },
    {
        "name": "Stefanie G.",
        "title": "Product Owner Technical Journey bij Proximus",
        "firstname": "Stefanie",
        "lastname": "G",
        "location": "Belgium",
        "note": "Incomplete last name - may need full name for email"
    },
    {
        "name": "Pradeep Thekkedath",
        "title": "TV Platforms Lead (Pickx), Proximus",
        "firstname": "Pradeep",
        "lastname": "Thekkedath",
        "location": "Belgium"
    },
]

def normalize_name(name):
    """Normalize name for email address."""
    if not name:
        return ""
    # Remove special characters, convert to lowercase
    name = name.lower()
    # Handle special characters (é, è, ç, etc.)
    replacements = {
        'é': 'e',
        'è': 'e',
        'ê': 'e',
        'ë': 'e',
        'à': 'a',
        'â': 'a',
        'ä': 'a',
        'î': 'i',
        'ï': 'i',
        'ô': 'o',
        'ö': 'o',
        'ù': 'u',
        'û': 'u',
        'ü': 'u',
        'ç': 'c',
        'ñ': 'n',
        'ó': 'o',
        'á': 'a',
        'í': 'i',
        'ú': 'u',
    }
    for char, replacement in replacements.items():
        name = name.replace(char, replacement)
    # Remove spaces and special characters
    name = re.sub(r'[^a-z]', '', name)
    return name

def generate_email_variants(contact):
    """Generate likely email address variants."""
    firstname = normalize_name(contact['firstname'])
    lastname = normalize_name(contact['lastname'])
    middle = normalize_name(contact.get('middle', ''))
    
    variants = []
    
    # Common patterns for Proximus
    # Pattern 1: firstname.lastname@proximus.com (most common)
    variants.append(f"{firstname}.{lastname}@proximus.com")
    
    # Pattern 2: firstname.lastname@proximus.be (Belgium domain)
    variants.append(f"{firstname}.{lastname}@proximus.be")
    
    # Pattern 3: firstname.lastname@belgacom.be (legacy Belgacom domain)
    if contact.get('note', '').find('Belgacom') != -1:
        variants.append(f"{firstname}.{lastname}@belgacom.be")
    
    # Pattern 4: firstname_lastname@proximus.com
    variants.append(f"{firstname}_{lastname}@proximus.com")
    
    # Pattern 5: f.lastname@proximus.com (first initial)
    variants.append(f"{firstname[0]}.{lastname}@proximus.com")
    
    # Pattern 6: firstname.middle.lastname@proximus.com (for compound names)
    if middle:
        variants.append(f"{firstname}.{middle}.{lastname}@proximus.com")
        variants.append(f"{firstname}.{middle[0]}.{lastname}@proximus.com")
    
    # Pattern 7: For Luxembourg (Proximus Luxembourg)
    if contact['location'] == 'Luxembourg':
        variants.append(f"{firstname}.{lastname}@proximus.lu")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("Proximus Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research:")
print("- Proximus uses @proximus.com for corporate contacts")
print("- Also uses @proximus.be (Belgium domain)")
print("- Legacy: @belgacom.be (Belgacom - now Proximus)")
print("- Luxembourg: @proximus.lu")
print("- Common pattern: firstname.lastname@proximus.com")
print("- Special characters (é, è, ç, ï, ô) typically converted to standard ASCII")
print("\n" + "=" * 60 + "\n")

for contact in contacts:
    print(f"Name: {contact['name']}")
    print(f"Title: {contact['title']}")
    print(f"Location: {contact['location']}")
    if 'note' in contact:
        print(f"Note: {contact['note']}")
    print("Predicted Email Addresses (most likely first):")
    variants = generate_email_variants(contact)
    for i, email in enumerate(variants[:3], 1):  # Show top 3 most likely
        print(f"  {i}. {email}")
    print()

