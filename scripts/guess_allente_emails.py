#!/usr/bin/env python3
"""
Script to generate likely email addresses for Allente contacts based on common patterns.
"""
import re

# Allente contacts with their full names
contacts = [
    {
        "name": "Eivind Peersen",
        "title": "Director Product and Digitalization i Allente Nordic",
        "firstname": "Eivind",
        "lastname": "Peersen",
        "location": "Bærum"
    },
    {
        "name": "Magnus Torén",
        "title": "Product owner at Allente Sverige",
        "firstname": "Magnus",
        "lastname": "Torén",
        "location": "Stockholm"
    },
    {
        "name": "Victor Björnarås Liljeroth",
        "title": "Chief B2B Officer @ Allente Nordic (Telenor/Viaplay JV) | Commercial & Operations Executive",
        "firstname": "Victor",
        "lastname": "Björnarås Liljeroth",
        "lastname_simple": "liljeroth",
        "location": "Stockholm"
    },
    {
        "name": "Bart Schoorl",
        "title": "Head of Logistics & Installation hos Allente Nordic",
        "firstname": "Bart",
        "lastname": "Schoorl",
        "location": "Oslo"
    },
    {
        "name": "Ilana Knudsen",
        "title": "Business Management, Go to market, Product Management",
        "firstname": "Ilana",
        "lastname": "Knudsen",
        "location": "Helsingør"
    },
    {
        "name": "Michael Bärlin",
        "title": "Chief Content Officer at Allente",
        "firstname": "Michael",
        "lastname": "Bärlin",
        "location": "Stockholm"
    },
    {
        "name": "Cem Buze",
        "title": "Product Manager for Allente's portfolio of streaming apps (Linear & VOD) for the Nordics",
        "firstname": "Cem",
        "lastname": "Buze",
        "location": "Oslo"
    },
    {
        "name": "Maria Strandler Lindholm",
        "title": "Senior Product and Go-To-Market Manager at Allente Nordic",
        "firstname": "Maria",
        "middle": "Strandler",
        "lastname": "Lindholm",
        "location": "Sweden"
    },
    {
        "name": "Peter Fredsted From",
        "title": "Nordic Head of Sales hos Allente Nordic",
        "firstname": "Peter",
        "middle": "Fredsted",
        "lastname": "From",
        "location": "Copenhagen"
    },
    {
        "name": "Mahmoud Mustapha",
        "title": "Group CEO @ Allente Nordic",
        "firstname": "Mahmoud",
        "lastname": "Mustapha",
        "location": "Stockholm"
    },
    {
        "name": "Jon Espen Nergård",
        "title": "CTO Allente",
        "firstname": "Jon",
        "middle": "Espen",
        "lastname": "Nergård",
        "location": "Nordic"
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
    lastname_simple = normalize_name(contact.get('lastname_simple', ''))
    
    variants = []
    
    # Common patterns for Allente Nordic
    # Pattern 1: firstname.lastname@allente.com (most common for Nordic companies)
    variants.append(f"{firstname}.{lastname}@allente.com")
    
    # Pattern 2: firstname.lastname@allente.no (Norway)
    if contact['location'] in ['Oslo', 'Bærum', 'Norway', 'Nordic']:
        variants.append(f"{firstname}.{lastname}@allente.no")
    
    # Pattern 3: firstname.lastname@allente.se (Sweden)
    if contact['location'] in ['Stockholm', 'Sweden', 'Greater Stockholm Metropolitan Area']:
        variants.append(f"{firstname}.{lastname}@allente.se")
    
    # Pattern 4: firstname.lastname@allente.dk (Denmark)
    if contact['location'] in ['Copenhagen', 'Helsingør', 'Denmark']:
        variants.append(f"{firstname}.{lastname}@allente.dk")
    
    # Pattern 5: firstname.lastname@allente.fi (Finland)
    if contact['location'] in ['Finland', 'Helsinki']:
        variants.append(f"{firstname}.{lastname}@allente.fi")
    
    # Pattern 6: firstname_lastname@allente.com
    variants.append(f"{firstname}_{lastname}@allente.com")
    
    # Pattern 7: f.lastname@allente.com (first initial)
    variants.append(f"{firstname[0]}.{lastname}@allente.com")
    
    # Pattern 8: firstname.middle.lastname@allente.com (for compound names)
    if middle:
        variants.append(f"{firstname}.{middle}.{lastname}@allente.com")
        variants.append(f"{firstname}.{middle[0]}.{lastname}@allente.com")
    
    # Pattern 9: Use simplified lastname for compound names
    if lastname_simple:
        variants.append(f"{firstname}.{lastname_simple}@allente.com")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("Allente Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research:")
print("- Allente Nordic uses @allente.com for corporate contacts")
print("- Country-specific domains: @allente.no (Norway), @allente.se (Sweden), @allente.dk (Denmark), @allente.fi (Finland)")
print("- Common pattern: firstname.lastname@allente.com")
print("- Special characters (ö, ä, å, ø, æ) typically converted to standard ASCII")
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

