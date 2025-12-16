#!/usr/bin/env python3
"""
Script to generate likely email addresses for KPN contacts based on common patterns.
"""
import re

# KPN contacts with their full names
contacts = [
    {
        "name": "Cornelis Kalma",
        "title": "Director Product and Marketing TV & Entertainment @ KPN",
        "firstname": "Cornelis",
        "lastname": "Kalma",
        "location": "Amsterdam"
    },
    {
        "name": "Martin Tafft",
        "title": "Client Director IoT for KPN",
        "firstname": "Martin",
        "lastname": "Tafft",
        "location": "St Briavels"
    },
    {
        "name": "Alejandro Casal",
        "title": "Senior TV Product Manager | Innovation | Business Development",
        "firstname": "Alejandro",
        "lastname": "Casal",
        "location": "The Hague"
    },
    {
        "name": "Erol Baran",
        "title": "Productmanager at KPN",
        "firstname": "Erol",
        "lastname": "Baran",
        "location": "Hoofddorp"
    },
    {
        "name": "Johan Trouwborst",
        "title": "VP Fixed Networks at KPN | Leadership | Strategy & Innovation",
        "firstname": "Johan",
        "lastname": "Trouwborst",
        "location": "The Randstad, Netherlands"
    },
    {
        "name": "Karen Rakowska",
        "title": "Client Director IoT at KPN",
        "firstname": "Karen",
        "lastname": "Rakowska",
        "location": "Slough"
    },
    {
        "name": "Sohini Ghosh",
        "title": "Customer growth & change @KPN| Intrapreneurship | Sustainable success",
        "firstname": "Sohini",
        "lastname": "Ghosh",
        "location": "The Randstad, Netherlands"
    },
    {
        "name": "Barna Kutvolgyi",
        "title": "CEO/CCO/COO/CMO",
        "firstname": "Barna",
        "lastname": "Kutvolgyi",
        "location": "United Kingdom",
        "note": "May not be directly at KPN"
    },
    {
        "name": "Tommy Björkberg",
        "title": "VP Network & Cloud @ KPN - Advisor - Technology Strategist",
        "firstname": "Tommy",
        "lastname": "Björkberg",
        "location": "Woking"
    },
    {
        "name": "Hille Ardjosemito",
        "title": "Partnerships Manager at KPN",
        "firstname": "Hille",
        "lastname": "Ardjosemito",
        "location": "Netherlands"
    },
    {
        "name": "Joost Farwerck",
        "title": "CEO (KPN Board of Management)",
        "firstname": "Joost",
        "lastname": "Farwerck",
        "location": "Netherlands"
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
    
    variants = []
    
    # Common patterns for KPN
    # Pattern 1: firstname.lastname@kpn.com (most common for corporate)
    variants.append(f"{firstname}.{lastname}@kpn.com")
    
    # Pattern 2: firstname.lastname@kpn.nl (Netherlands domain)
    variants.append(f"{firstname}.{lastname}@kpn.nl")
    
    # Pattern 3: firstname_lastname@kpn.com
    variants.append(f"{firstname}_{lastname}@kpn.com")
    
    # Pattern 4: f.lastname@kpn.com (first initial)
    variants.append(f"{firstname[0]}.{lastname}@kpn.com")
    
    # Pattern 5: firstname.lastname@kpnbusiness.nl (business domain)
    variants.append(f"{firstname}.{lastname}@kpnbusiness.nl")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("KPN Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research:")
print("- KPN uses @kpn.com for corporate/company-level contacts")
print("- KPN also uses @kpn.nl (Netherlands domain)")
print("- Business domain: @kpnbusiness.nl")
print("- Common pattern: firstname.lastname@kpn.com")
print("- Special characters (ö, ä, å) typically converted to standard ASCII")
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

