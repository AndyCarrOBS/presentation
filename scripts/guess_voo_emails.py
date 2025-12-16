#!/usr/bin/env python3
"""
Script to generate likely email addresses for Voo/Orange Belgium contacts based on common patterns.
"""
import re

# Voo/Orange Belgium contacts with their full names
contacts = [
    {
        "name": "Stéphane Le Goff",
        "title": "Director Wholesale and Fixed Accesses | Orange Belgium - Chief Wholesale Officer | VOO",
        "firstname": "Stéphane",
        "lastname": "Le Goff",
        "lastname_simple": "goff",
        "location": "Belgium"
    },
    {
        "name": "Martial Foucart",
        "title": "Lead Partnership & IT Infrastructure Service Manager chez VOO",
        "firstname": "Martial",
        "lastname": "Foucart",
        "location": "Belgium"
    },
    {
        "name": "Frederic Chaballe",
        "title": "Head of Quality & Performance",
        "firstname": "Frederic",
        "lastname": "Chaballe",
        "location": "Belgium"
    },
    {
        "name": "Dylan Guetta",
        "title": "Experienced Product, Project and Technical manager with speciality on OTT and IPTV offerings",
        "firstname": "Dylan",
        "lastname": "Guetta",
        "location": "Belgium"
    },
    {
        "name": "Philippe LOGIE",
        "title": "Head of Pay tv/VOD Acquisitions & Coproductions",
        "firstname": "Philippe",
        "lastname": "LOGIE",
        "location": "Belgium"
    },
    {
        "name": "Massimo Pacini",
        "title": "Lead DevOps & Full stack software engineer",
        "firstname": "Massimo",
        "lastname": "Pacini",
        "location": "Belgium"
    },
    {
        "name": "Adriana Izatt",
        "title": "Director at VOO",
        "firstname": "Adriana",
        "lastname": "Izatt",
        "location": "Belgium"
    },
    {
        "name": "Maïté CASSANO",
        "title": "Hunting Manager CoolDeals",
        "firstname": "Maïté",
        "lastname": "CASSANO",
        "location": "Belgium"
    },
    {
        "name": "Philippe Fox",
        "title": "GIGA Network Director at VOO",
        "firstname": "Philippe",
        "lastname": "Fox",
        "location": "Belgium"
    },
    {
        "name": "Gildas Bouchet",
        "title": "Deputy CFO Orange Belgium - CFO VOO",
        "firstname": "Gildas",
        "lastname": "Bouchet",
        "location": "Belgium"
    },
    {
        "name": "Stéphanie Etienne",
        "title": "Enthusiastic and creative digital/social storyteller",
        "firstname": "Stéphanie",
        "lastname": "Etienne",
        "location": "Belgium"
    },
    {
        "name": "Frédéric Despontin",
        "title": "TV Director",
        "firstname": "Frédéric",
        "lastname": "Despontin",
        "location": "Belgium"
    },
    {
        "name": "Matthieu Dekeyser",
        "title": "Head Of Technical and Mobile Inquiries at VOO",
        "firstname": "Matthieu",
        "lastname": "Dekeyser",
        "location": "Belgium"
    },
    {
        "name": "Orban Christophe",
        "title": "Head of Engineering",
        "firstname": "Christophe",
        "lastname": "Orban",
        "location": "Belgium",
        "note": "Name order reversed - Orban is likely last name"
    },
    {
        "name": "Gilles Reunis",
        "title": "Responsable des Acquisitions / Acquisitions Manager PayTV and VOD (BeTV/VOO)",
        "firstname": "Gilles",
        "lastname": "Reunis",
        "location": "Belgium"
    },
    {
        "name": "Fatiha A.",
        "title": "Process, Performance et Quality manager chez VOO",
        "firstname": "Fatiha",
        "lastname": "A",
        "location": "Belgium",
        "note": "Incomplete last name"
    },
    {
        "name": "Philippe Dubus",
        "title": "Technicien station Brutele",
        "firstname": "Philippe",
        "lastname": "Dubus",
        "location": "Belgium"
    },
    {
        "name": "Christian Loiseau",
        "title": "Directeur général @ Be tv & Director Content & Media @VOO",
        "firstname": "Christian",
        "lastname": "Loiseau",
        "location": "Belgium"
    },
    {
        "name": "Alexis De Bartolo",
        "title": "Operations Engineer IP/Docsis - Orange | VOO",
        "firstname": "Alexis",
        "middle": "De",
        "lastname": "Bartolo",
        "location": "Belgium"
    },
    {
        "name": "mohamed hassan",
        "title": "Business Development and project Manager",
        "firstname": "mohamed",
        "lastname": "hassan",
        "location": "Belgium"
    },
    {
        "name": "Nadia Manco",
        "title": "Operational expert BillToCash",
        "firstname": "Nadia",
        "lastname": "Manco",
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
    lastname_simple = normalize_name(contact.get('lastname_simple', ''))
    
    variants = []
    
    # Common patterns for Voo/Orange Belgium
    # Pattern 1: firstname.lastname@voo.be (Voo domain - most likely)
    variants.append(f"{firstname}.{lastname}@voo.be")
    
    # Pattern 2: firstname.lastname@orange.be (Orange Belgium domain)
    variants.append(f"{firstname}.{lastname}@orange.be")
    
    # Pattern 3: firstname.lastname@orange-belgium.be
    variants.append(f"{firstname}.{lastname}@orange-belgium.be")
    
    # Pattern 4: firstname_lastname@voo.be
    variants.append(f"{firstname}_{lastname}@voo.be")
    
    # Pattern 5: f.lastname@voo.be (first initial)
    variants.append(f"{firstname[0]}.{lastname}@voo.be")
    
    # Pattern 6: firstname.middle.lastname@voo.be (for compound names)
    if middle:
        variants.append(f"{firstname}.{middle}.{lastname}@voo.be")
        variants.append(f"{firstname}.{middle[0]}.{lastname}@voo.be")
    
    # Pattern 7: Use simplified lastname for compound names (Le Goff -> goff)
    if lastname_simple:
        variants.append(f"{firstname}.{lastname_simple}@voo.be")
        variants.append(f"{firstname}.{lastname_simple}@orange.be")
    
    # Pattern 8: Handle "De" prefix specially (De Bartolo -> bartolo)
    if "de" in lastname:
        lastname_no_de = lastname.replace("de", "").strip()
        if lastname_no_de:
            variants.append(f"{firstname}.{lastname_no_de}@voo.be")
            variants.append(f"{firstname}.{lastname_no_de}@orange.be")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("Voo/Orange Belgium Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research:")
print("- Voo uses @voo.be for Voo-branded contacts")
print("- Orange Belgium uses @orange.be or @orange-belgium.be")
print("- Common pattern: firstname.lastname@voo.be or @orange.be")
print("- Special characters (é, è, ç, ï, ô) typically converted to standard ASCII")
print("- Compound names (Le Goff, De Bartolo) may be simplified")
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

