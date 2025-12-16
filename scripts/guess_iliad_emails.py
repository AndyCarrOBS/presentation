#!/usr/bin/env python3
"""
Script to generate likely email addresses for Iliad Group/Free France contacts based on common patterns.
"""
import re

# Iliad Group contacts with their full names
contacts = [
    {
        "name": "Ersilia Manzo",
        "title": "CTO at Iliad Italy",
        "firstname": "Ersilia",
        "lastname": "Manzo",
        "location": "Italy"
    },
    {
        "name": "Jérémie Sitruk",
        "title": "COO at Iliad Italia S.p.A.",
        "firstname": "Jérémie",
        "lastname": "Sitruk",
        "location": "Italy"
    },
    {
        "name": "Bertrand Fievet",
        "title": "Wireless Mobile Network at Iliad Group",
        "firstname": "Bertrand",
        "lastname": "Fievet",
        "location": "France"
    },
    {
        "name": "Marcello Borzi",
        "title": "Software Factory Director @ Iliad",
        "firstname": "Marcello",
        "lastname": "Borzi",
        "location": "Italy"
    },
    {
        "name": "Francesca Reich",
        "title": "CEO @Barzanò&Zanardo / Non Executive Director / Digital & Innovation Expert",
        "firstname": "Francesca",
        "lastname": "Reich",
        "location": "Italy",
        "note": "External - Barzanò&Zanardo, not Iliad employee"
    },
    {
        "name": "Francesco Tollini",
        "title": "Corporate Development at iliad",
        "firstname": "Francesco",
        "lastname": "Tollini",
        "location": "Italy"
    },
    {
        "name": "Tiziana Talevi",
        "title": "Regulatory Affairs & Competition Iliad Italia Policy | Lobbying | Economic Analysis",
        "firstname": "Tiziana",
        "lastname": "Talevi",
        "location": "Italy"
    },
    {
        "name": "Giuseppe Nisticò",
        "title": "Street Smart Mindset at iliad",
        "firstname": "Giuseppe",
        "lastname": "Nisticò",
        "location": "Italy"
    },
    {
        "name": "PAMELA MUNOZ",
        "title": "Cheffe de projet Learning and Talent chez Iliad / Free / JURY FPA",
        "firstname": "PAMELA",
        "lastname": "MUNOZ",
        "location": "France"
    },
    {
        "name": "Lydia ATMANI-ATTHALIN",
        "title": "Group Energy Purchasing Manager",
        "firstname": "Lydia",
        "lastname": "ATMANI-ATTHALIN",
        "lastname_simple": "atthalin",
        "location": "France"
    },
    {
        "name": "Francesca Piro",
        "title": "Head of Sales Key Account Management @iliad | Sales Management | Channel Strategy",
        "firstname": "Francesca",
        "lastname": "Piro",
        "location": "Italy"
    },
    {
        "name": "Drera Emanuele",
        "title": "Head of Radio Network Engineering Iliad Italia",
        "firstname": "Emanuele",
        "lastname": "Drera",
        "location": "Italy",
        "note": "Name order reversed - Emanuele is first name"
    },
    {
        "name": "Riccardo Lorenzon",
        "title": "Iliad | Head of Data",
        "firstname": "Riccardo",
        "lastname": "Lorenzon",
        "location": "Italy"
    },
    {
        "name": "Giovanni Leone",
        "title": "Head SO.HO & SME Sales Development Lead",
        "firstname": "Giovanni",
        "lastname": "Leone",
        "location": "Italy"
    },
    {
        "name": "Odé GABRIEL",
        "title": "Chargée de Mission RH",
        "firstname": "Odé",
        "lastname": "GABRIEL",
        "location": "France"
    },
    {
        "name": "Michele Moizi",
        "title": "Head of Procurement | iliad",
        "firstname": "Michele",
        "lastname": "Moizi",
        "location": "Italy"
    },
    {
        "name": "Alberto Rescigno",
        "title": "Finance I Strategy I Commercial Operations I EY Alumni",
        "firstname": "Alberto",
        "lastname": "Rescigno",
        "location": "Italy"
    },
    {
        "name": "Celine Lazorthes",
        "title": "Entrepreneur, Investor & Activist",
        "firstname": "Celine",
        "lastname": "Lazorthes",
        "location": "France",
        "note": "May not be Iliad employee - Entrepreneur/Investor"
    },
    {
        "name": "Federica Vitale",
        "title": "Product marketing & Go to Market | B2C| Marketing strategy & planning | telco market mobile & broadband",
        "firstname": "Federica",
        "lastname": "Vitale",
        "location": "Italy"
    },
    {
        "name": "Denis Laforgue",
        "title": "Marketing Director",
        "firstname": "Denis",
        "lastname": "Laforgue",
        "location": "France"
    },
    {
        "name": "Francesco Como",
        "title": "Director of Software Engineering at Iliad Italia S.p.A.",
        "firstname": "Francesco",
        "lastname": "Como",
        "location": "Italy"
    },
    {
        "name": "Luca Piedimonte",
        "title": "Digital & Performance Marketing Lead presso Iliad",
        "firstname": "Luca",
        "lastname": "Piedimonte",
        "location": "Italy"
    },
    {
        "name": "Dario Radaelli",
        "title": "Senior Manager @iliad | Strategy | Finance | Data Analytics",
        "firstname": "Dario",
        "lastname": "Radaelli",
        "location": "Italy"
    },
    {
        "name": "Giovanni Castelli",
        "title": "User Value & Loyalty Specialist - Marketing and Communication - Iliad",
        "firstname": "Giovanni",
        "lastname": "Castelli",
        "location": "Italy"
    },
    {
        "name": "Michela Nelli",
        "title": "Revenues Insights Analyst (iliad)",
        "firstname": "Michela",
        "lastname": "Nelli",
        "location": "Italy"
    },
    {
        "name": "Giorgio Carafa Cohen",
        "title": "Bringing about a Revolution at iliad",
        "firstname": "Giorgio",
        "middle": "Carafa",
        "lastname": "Cohen",
        "location": "Italy"
    },
    {
        "name": "Giulia De Dominicis",
        "title": "Trade Marketing Lead at iliad",
        "firstname": "Giulia",
        "middle": "De",
        "lastname": "Dominicis",
        "location": "Italy"
    },
    {
        "name": "Cucciol Silvia",
        "title": "Head of Service Creation - PMO | Telco & Digital Transformation | Project Delivery & Governance Expert",
        "firstname": "Silvia",
        "lastname": "Cucciol",
        "location": "Italy",
        "note": "Name order reversed - Silvia is first name"
    },
    {
        "name": "Benedetto Levi",
        "title": "CEO at Iliad Italia S.p.A.",
        "firstname": "Benedetto",
        "lastname": "Levi",
        "location": "Italy"
    },
    {
        "name": "Alberto Caldarera",
        "title": "HR Learning, Development & Engagement Specialist @iliad",
        "firstname": "Alberto",
        "lastname": "Caldarera",
        "location": "Italy"
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
        'ò': 'o',
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
    location = contact.get('location', 'France')
    
    variants = []
    
    # Common patterns for Iliad Group/Free France
    # Pattern 1: firstname.lastname@iliad.fr (Iliad Group France - most likely)
    if location == "France":
        variants.append(f"{firstname}.{lastname}@iliad.fr")
        variants.append(f"{firstname}.{lastname}@free.fr")
    
    # Pattern 2: firstname.lastname@iliad.it (Iliad Italia)
    if location == "Italy":
        variants.append(f"{firstname}.{lastname}@iliad.it")
        variants.append(f"{firstname}.{lastname}@iliaditalia.it")
    
    # Pattern 3: firstname.lastname@iliad.com (Iliad Group corporate)
    variants.append(f"{firstname}.{lastname}@iliad.com")
    
    # Pattern 4: firstname_lastname@iliad.fr
    if location == "France":
        variants.append(f"{firstname}_{lastname}@iliad.fr")
    
    # Pattern 5: f.lastname@iliad.fr (first initial)
    if location == "France":
        variants.append(f"{firstname[0]}.{lastname}@iliad.fr")
    
    # Pattern 6: firstname.middle.lastname@iliad.it (for compound names)
    if middle:
        if location == "Italy":
            variants.append(f"{firstname}.{middle}.{lastname}@iliad.it")
            variants.append(f"{firstname}.{middle[0]}.{lastname}@iliad.it")
        variants.append(f"{firstname}.{middle}.{lastname}@iliad.com")
    
    # Pattern 7: Use simplified lastname for compound names (ATMANI-ATTHALIN -> atthalin)
    if lastname_simple:
        if location == "France":
            variants.append(f"{firstname}.{lastname_simple}@iliad.fr")
        variants.append(f"{firstname}.{lastname_simple}@iliad.com")
    
    # Pattern 8: Handle "De" prefix specially (De Dominicis -> dominicis)
    if "de" in lastname:
        lastname_no_de = lastname.replace("de", "").strip()
        if lastname_no_de:
            if location == "Italy":
                variants.append(f"{firstname}.{lastname_no_de}@iliad.it")
            variants.append(f"{firstname}.{lastname_no_de}@iliad.com")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("Iliad Group/Free France Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research:")
print("- Iliad Group uses @iliad.fr for France-based contacts")
print("- Free France uses @free.fr")
print("- Iliad Italia uses @iliad.it or @iliaditalia.it")
print("- Iliad Group corporate may use @iliad.com")
print("- Common pattern: firstname.lastname@iliad.fr (France) or @iliad.it (Italy)")
print("- Special characters (é, è, ç, ï, ô, ò) typically converted to standard ASCII")
print("- Compound names (ATMANI-ATTHALIN, De Dominicis) may be simplified")
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

