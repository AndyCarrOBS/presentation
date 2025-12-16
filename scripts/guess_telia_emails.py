#!/usr/bin/env python3
"""
Script to generate likely email addresses for Telia contacts based on common patterns.
"""
import re

# Telia contacts with their full names
contacts = [
    {
        "name": "Vygintas Kazanavicius",
        "title": "Head of Technology, Content Quality @ Telia",
        "firstname": "Vygintas",
        "lastname": "Kazanavicius",
        "location": "Lithuania"
    },
    {
        "name": "Mikael Malmborg",
        "title": "Head of Video Streaming @ Telia",
        "firstname": "Mikael",
        "lastname": "Malmborg",
        "location": "Stockholm"
    },
    {
        "name": "Mikko Hellsten",
        "title": "Head of Home Connectivity at Telia",
        "firstname": "Mikko",
        "lastname": "Hellsten",
        "location": "Helsinki"
    },
    {
        "name": "Pejman Hafezi",
        "title": "Strategic Tech Investments | New Tech Sourcing | Open Innovation",
        "firstname": "Pejman",
        "lastname": "Hafezi",
        "location": "United Kingdom"
    },
    {
        "name": "Birjo Kiik",
        "title": "Strategic Partner Relationship Management & Innovation",
        "firstname": "Birjo",
        "lastname": "Kiik",
        "location": "Estonia"
    },
    {
        "name": "Stefan Johansson",
        "title": "Product Development at Telia Company Internet Access & Connected Home",
        "firstname": "Stefan",
        "lastname": "Johansson",
        "location": "Stockholm"
    },
    {
        "name": "Timi Lammela",
        "title": "Senior Product Development Manager at Telia Company Internet Access & Connected Home",
        "firstname": "Timi",
        "lastname": "Lammela",
        "location": "Helsinki"
    },
    {
        "name": "Caroline Cardozo",
        "title": "Product Leader | Product Mentor",
        "firstname": "Caroline",
        "lastname": "Cardozo",
        "location": "London"
    },
    {
        "name": "Patrik Höljö",
        "title": "Head of Devices / Consumer Electronics Strategic Sourcing",
        "firstname": "Patrik",
        "lastname": "Höljö",
        "location": "Stockholm"
    },
    {
        "name": "Anders Olsson",
        "title": "CEO at Telia Sverige",
        "firstname": "Anders",
        "lastname": "Olsson",
        "location": "Stockholm"
    },
    {
        "name": "Riku Kreula",
        "title": "Technical Product Manager, Telia TV services",
        "firstname": "Riku",
        "lastname": "Kreula",
        "location": "Finland"
    },
]

def normalize_name(name):
    """Normalize name for email address."""
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
    
    variants = []
    
    # Common patterns for Telia (based on @telia.com domain - most common for corporate)
    # Pattern 1: firstname.lastname@telia.com (most common)
    variants.append(f"{firstname}.{lastname}@telia.com")
    
    # Pattern 2: firstname.lastname@telia.se (Sweden)
    if contact['location'] in ['Stockholm', 'Sweden']:
        variants.append(f"{firstname}.{lastname}@telia.se")
    
    # Pattern 3: firstname.lastname@telia.fi (Finland)
    if contact['location'] in ['Helsinki', 'Finland']:
        variants.append(f"{firstname}.{lastname}@telia.fi")
    
    # Pattern 4: firstname.lastname@telia.no (Norway)
    if contact['location'] in ['Norway']:
        variants.append(f"{firstname}.{lastname}@telia.no")
    
    # Pattern 5: firstname_lastname@telia.com
    variants.append(f"{firstname}_{lastname}@telia.com")
    
    # Pattern 6: f.lastname@telia.com (first initial)
    variants.append(f"{firstname[0]}.{lastname}@telia.com")
    
    # Pattern 7: firstname.lastname@teliacompany.com (alternative domain)
    variants.append(f"{firstname}.{lastname}@teliacompany.com")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("Telia Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research:")
print("- Telia uses @telia.com for corporate/company-level contacts")
print("- Country-specific domains: @telia.se (Sweden), @telia.fi (Finland), @telia.no (Norway)")
print("- Common pattern: firstname.lastname@domain")
print("- Special characters (ö, ä, å) typically converted to standard ASCII")
print("\n" + "=" * 60 + "\n")

for contact in contacts:
    print(f"Name: {contact['name']}")
    print(f"Title: {contact['title']}")
    print(f"Location: {contact['location']}")
    print("Predicted Email Addresses (most likely first):")
    variants = generate_email_variants(contact)
    for i, email in enumerate(variants[:3], 1):  # Show top 3 most likely
        print(f"  {i}. {email}")
    print()

