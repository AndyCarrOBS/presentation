#!/usr/bin/env python3
"""
Script to generate likely email addresses for Ziggo contacts based on common patterns.
"""
import re

# Ziggo contacts with their full names
contacts = [
    {
        "name": "Stephen van Rooyen",
        "title": "CEO VodafoneZiggo",
        "firstname": "Stephen",
        "lastname": "van Rooyen",
        "lastname_simple": "rooyen"
    },
    {
        "name": "Raymond van der Vliet",
        "title": "Content & Programming Director",
        "firstname": "Raymond",
        "lastname": "van der Vliet",
        "lastname_simple": "vliet"
    },
    {
        "name": "Koen Cluistra",
        "title": "Consumer Marketing Director",
        "firstname": "Koen",
        "lastname": "Cluistra",
        "lastname_simple": "cluistra"
    },
    {
        "name": "Stephen O'Boyle",
        "title": "Head of Product, TV Onboarding & Help",
        "firstname": "Stephen",
        "lastname": "O'Boyle",
        "lastname_simple": "oboyle"
    },
    {
        "name": "Alex Smith",
        "title": "Senior Product Manager – Video",
        "firstname": "Alex",
        "lastname": "Smith",
        "lastname_simple": "smith"
    },
    {
        "name": "Robin Kroes",
        "title": "CCO Consumer - Executive Committee",
        "firstname": "Robin",
        "lastname": "Kroes",
        "lastname_simple": "kroes"
    },
    {
        "name": "Joke Van Griensven",
        "title": "Head of Ziggo Brand, Marcomms & In-house Studio",
        "firstname": "Joke",
        "lastname": "Van Griensven",
        "lastname_simple": "griensven"
    },
    {
        "name": "Ivar Slavenburg",
        "title": "Product Management",
        "firstname": "Ivar",
        "lastname": "Slavenburg",
        "lastname_simple": "slavenburg"
    },
    {
        "name": "Thomas Helbo",
        "title": "Business Transformation | Innovation",
        "firstname": "Thomas",
        "lastname": "Helbo",
        "lastname_simple": "helbo"
    },
    {
        "name": "Steven Offerein",
        "title": "Product & Business Development",
        "firstname": "Steven",
        "lastname": "Offerein",
        "lastname_simple": "offerein"
    },
    {
        "name": "Nathalie Toeset",
        "title": "Product Leadership",
        "firstname": "Nathalie",
        "lastname": "Toeset",
        "lastname_simple": "toeset"
    },
]

def normalize_name(name):
    """Normalize name for email address."""
    # Remove special characters, convert to lowercase
    name = name.lower()
    # Handle common Dutch prefixes (van, van der, de, etc.)
    name = re.sub(r'\s+', '', name)  # Remove spaces
    # Handle apostrophes
    name = name.replace("'", "")
    # Handle hyphens
    name = name.replace("-", "")
    return name

def generate_email_variants(contact):
    """Generate likely email address variants."""
    firstname = contact['firstname'].lower()
    lastname = contact['lastname'].lower()
    lastname_simple = contact['lastname_simple'].lower()
    
    # Remove spaces and special characters from lastname
    lastname_clean = re.sub(r'[^a-z]', '', lastname)
    
    variants = []
    
    # Common patterns for VodafoneZiggo (based on @vodafoneziggo.com domain)
    # Pattern 1: firstname.lastname@vodafoneziggo.com
    variants.append(f"{firstname}.{lastname_clean}@vodafoneziggo.com")
    
    # Pattern 2: firstname.lastname@ziggo.nl (legacy)
    variants.append(f"{firstname}.{lastname_clean}@ziggo.nl")
    
    # Pattern 3: firstname_lastname@vodafoneziggo.com
    variants.append(f"{firstname}_{lastname_clean}@vodafoneziggo.com")
    
    # Pattern 4: f.lastname@vodafoneziggo.com (first initial)
    variants.append(f"{firstname[0]}.{lastname_clean}@vodafoneziggo.com")
    
    # Pattern 5: firstname.lastname_simple (for compound names)
    if lastname_simple != lastname_clean:
        variants.append(f"{firstname}.{lastname_simple}@vodafoneziggo.com")
    
    # Pattern 6: Handle "van" prefix specially
    if "van" in lastname:
        lastname_no_van = lastname.replace("van", "").replace("der", "").strip()
        lastname_no_van = re.sub(r'\s+', '', lastname_no_van)
        variants.append(f"{firstname}.{lastname_no_van}@vodafoneziggo.com")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("Ziggo Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research:")
print("- Ziggo uses @ziggo.nl for general support")
print("- VodafoneZiggo uses @vodafoneziggo.com for business/technical contacts")
print("- Common pattern: firstname.lastname@domain")
print("\n" + "=" * 60 + "\n")

for contact in contacts:
    print(f"Name: {contact['name']}")
    print(f"Title: {contact['title']}")
    print("Predicted Email Addresses (most likely first):")
    variants = generate_email_variants(contact)
    for i, email in enumerate(variants[:3], 1):  # Show top 3 most likely
        print(f"  {i}. {email}")
    print()

