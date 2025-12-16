#!/usr/bin/env python3
"""
Script to generate likely email addresses for Telnet contacts based on common patterns.
"""
import re

# Telnet contacts with their full names
contacts = [
    {
        "name": "Anis YOUSSEF",
        "title": "CHIEF INNOVATION OFFICER",
        "firstname": "Anis",
        "lastname": "YOUSSEF",
        "location": "Tunisia"
    },
    {
        "name": "Bilel Drira",
        "title": "Agile Manager/Embedded systems enthusiast, PSM I",
        "firstname": "Bilel",
        "lastname": "Drira",
        "location": "Tunisia"
    },
    {
        "name": "Mehdi MESLMENI",
        "title": "Senior Consultant Technical Lead",
        "firstname": "Mehdi",
        "lastname": "MESLMENI",
        "location": "Tunisia"
    },
    {
        "name": "Ali Mounés",
        "title": "Hardware Engineer",
        "firstname": "Ali",
        "lastname": "Mounés",
        "location": "Tunisia"
    },
    {
        "name": "Ons MESSAOUD",
        "title": "Software Engineer",
        "firstname": "Ons",
        "lastname": "MESSAOUD",
        "location": "Tunisia"
    },
    {
        "name": "Mohamed Ali JEBRI",
        "title": "Ingénieur développement C/C++",
        "firstname": "Mohamed",
        "middle": "Ali",
        "lastname": "JEBRI",
        "location": "Tunisia"
    },
    {
        "name": "Oumaima Said",
        "title": "Étudiante en ingénierie informatique | Spécialisation IoT & Robotique",
        "firstname": "Oumaima",
        "lastname": "Said",
        "location": "Tunisia",
        "note": "Student - may not have company email"
    },
    {
        "name": "Emna BEN AMMAR",
        "title": "Ingénieur électronique",
        "firstname": "Emna",
        "lastname": "BEN AMMAR",
        "lastname_simple": "ammar",
        "location": "Tunisia"
    },
    {
        "name": "Tarek ELGHALI GRASSA",
        "title": "Director of Projects",
        "firstname": "Tarek",
        "lastname": "ELGHALI GRASSA",
        "lastname_simple": "grassa",
        "location": "Tunisia"
    },
    {
        "name": "Mohamed Frikha",
        "title": "CEO",
        "firstname": "Mohamed",
        "lastname": "Frikha",
        "location": "Tunisia"
    },
    {
        "name": "Ahmed Kechaou",
        "title": "Senior IT Manager chez TELNET HOLDING",
        "firstname": "Ahmed",
        "lastname": "Kechaou",
        "location": "Tunisia"
    },
]

def normalize_name(name):
    """Normalize name for email address."""
    if not name:
        return ""
    # Remove special characters, convert to lowercase
    name = name.lower()
    # Handle special characters (é, è, etc.)
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
    
    # Common patterns for Telnet (Tunisia-based company)
    # Pattern 1: firstname.lastname@telnet.tn (Tunisia domain - most likely)
    variants.append(f"{firstname}.{lastname}@telnet.tn")
    
    # Pattern 2: firstname.lastname@telnet.com
    variants.append(f"{firstname}.{lastname}@telnet.com")
    
    # Pattern 3: firstname.lastname@telnet-holding.com
    variants.append(f"{firstname}.{lastname}@telnet-holding.com")
    
    # Pattern 4: firstname.lastname@telnet-holding.tn
    variants.append(f"{firstname}.{lastname}@telnet-holding.tn")
    
    # Pattern 5: firstname_lastname@telnet.tn
    variants.append(f"{firstname}_{lastname}@telnet.tn")
    
    # Pattern 6: f.lastname@telnet.tn (first initial)
    variants.append(f"{firstname[0]}.{lastname}@telnet.tn")
    
    # Pattern 7: firstname.middle.lastname@telnet.tn (for compound names)
    if middle:
        variants.append(f"{firstname}.{middle}.{lastname}@telnet.tn")
        variants.append(f"{firstname}.{middle[0]}.{lastname}@telnet.tn")
    
    # Pattern 8: Use simplified lastname for compound names (BEN AMMAR -> ammar)
    if lastname_simple:
        variants.append(f"{firstname}.{lastname_simple}@telnet.tn")
    
    # Pattern 9: Handle "BEN" prefix specially (common in Arabic names)
    if "ben" in lastname or "bena" in lastname:
        lastname_no_ben = lastname.replace("ben", "").replace("bena", "").strip()
        if lastname_no_ben:
            variants.append(f"{firstname}.{lastname_no_ben}@telnet.tn")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("Telnet Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research:")
print("- Telnet (Tunisia) likely uses @telnet.tn (Tunisia domain)")
print("- Alternative: @telnet.com or @telnet-holding.com")
print("- Common pattern: firstname.lastname@telnet.tn")
print("- Special characters (é, è, ç) typically converted to standard ASCII")
print("- Arabic name prefixes (BEN) may be included or simplified")
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

