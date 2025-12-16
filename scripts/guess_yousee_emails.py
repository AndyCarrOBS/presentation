#!/usr/bin/env python3
"""
Script to generate likely email addresses for YouSee contacts based on common patterns.
"""
import re

# YouSee contacts with their full names
contacts = [
    {
        "name": "Leif Björklund",
        "title": "Chief Product Officer @ YouSee",
        "firstname": "Leif",
        "lastname": "Björklund",
        "location": "Copenhagen"
    },
    {
        "name": "Henrik Harder",
        "title": "Senior Director, Digital Product at the LEGO Group",
        "firstname": "Henrik",
        "lastname": "Harder",
        "location": "Aarhus",
        "note": "Currently at LEGO Group, may have been at YouSee/TDC"
    },
    {
        "name": "Torben Rasmussen",
        "title": "Vice President - Head of Transformation",
        "firstname": "Torben",
        "lastname": "Rasmussen",
        "location": "Copenhagen"
    },
    {
        "name": "Jens Jakob Dahlgaard",
        "title": "Head of Product Management",
        "firstname": "Jens",
        "middle": "Jakob",
        "lastname": "Dahlgaard",
        "location": "Aarhus"
    },
    {
        "name": "Sigge Lundqvist",
        "title": "Leading streaming for commercial spaces",
        "firstname": "Sigge",
        "lastname": "Lundqvist",
        "location": "Stockholm",
        "note": "May be at YouSee or related company"
    },
    {
        "name": "Casper Hald",
        "title": "Head of Strategic Distribution & Partnerships",
        "firstname": "Casper",
        "lastname": "Hald",
        "location": "Copenhagen"
    },
    {
        "name": "Henrik Loop",
        "title": "IT-Architect | Digital Transformation Leader | Video Streaming & OTT Solutions Architect",
        "firstname": "Henrik",
        "lastname": "Loop",
        "location": "Høje-Taastrup Municipality"
    },
    {
        "name": "Martin Jürgensen",
        "title": "Senior Product Development Manager hos Waoo/Fibia",
        "firstname": "Martin",
        "lastname": "Jürgensen",
        "location": "Aarhus",
        "note": "Currently at Waoo/Fibia, may have been at YouSee/TDC"
    },
    {
        "name": "Troels Hauch Tornmark",
        "title": "Produktchef YouSee TV | Senior Product Management professional",
        "firstname": "Troels",
        "middle": "Hauch",
        "lastname": "Tornmark",
        "location": "Copenhagen"
    },
    {
        "name": "Zahid Rasheed",
        "title": "Head of Development @ YouSee",
        "firstname": "Zahid",
        "lastname": "Rasheed",
        "location": "Ringsted"
    },
]

def normalize_name(name):
    """Normalize name for email address."""
    if not name:
        return ""
    # Remove special characters, convert to lowercase
    name = name.lower()
    # Handle special characters (ö, ä, å, etc.)
    replacements = {
        'ö': 'o',
        'ä': 'a',
        'å': 'a',
        'ü': 'u',
        'é': 'e',
        'è': 'e',
        'á': 'a',
        'à': 'a',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'ø': 'o',
        'æ': 'ae',
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
    
    # Common patterns for YouSee/TDC Group
    # Pattern 1: firstname.lastname@yousee.dk (most common)
    variants.append(f"{firstname}.{lastname}@yousee.dk")
    
    # Pattern 2: firstname.lastname@tdc.dk (TDC Group domain)
    variants.append(f"{firstname}.{lastname}@tdc.dk")
    
    # Pattern 3: firstname.lastname@nuuday.dk (Nuuday brand)
    variants.append(f"{firstname}.{lastname}@nuuday.dk")
    
    # Pattern 4: firstname_lastname@yousee.dk
    variants.append(f"{firstname}_{lastname}@yousee.dk")
    
    # Pattern 5: f.lastname@yousee.dk (first initial)
    variants.append(f"{firstname[0]}.{lastname}@yousee.dk")
    
    # Pattern 6: firstname.middle.lastname@yousee.dk (for compound names)
    if middle:
        variants.append(f"{firstname}.{middle}.{lastname}@yousee.dk")
        variants.append(f"{firstname}.{middle[0]}.{lastname}@yousee.dk")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("YouSee Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research:")
print("- YouSee uses @yousee.dk for employee contacts")
print("- TDC Group uses @tdc.dk (parent company)")
print("- Nuuday brand uses @nuuday.dk")
print("- Common pattern: firstname.lastname@yousee.dk")
print("- Special characters (ö, ä, å, ø, æ) typically converted to standard ASCII")
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

