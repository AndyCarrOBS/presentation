#!/usr/bin/env python3
"""
Script to generate likely email addresses for Orange contacts based on common patterns.
"""
import re

# Orange contacts with their full names
contacts = [
    {
        "name": "Arnaud Alvarez",
        "title": "Chief Commercial Officer (CCO), Viaccess-Orca, Orange Group",
        "firstname": "Arnaud",
        "lastname": "Alvarez",
        "location": "France",
        "note": "Viaccess-Orca (Orange Group subsidiary)"
    },
    {
        "name": "Serge Francois",
        "title": "Head of Broadband CPE Engineering",
        "firstname": "Serge",
        "lastname": "Francois",
        "location": "Belgium"
    },
    {
        "name": "Jean-Pierre Combe",
        "title": "API & Apps Distribution Director at Orange",
        "firstname": "Jean-Pierre",
        "middle": "Pierre",
        "lastname": "Combe",
        "location": "France"
    },
    {
        "name": "Jean-Marc Barraqué",
        "title": "Digital Transformation Director at Orange",
        "firstname": "Jean-Marc",
        "middle": "Marc",
        "lastname": "Barraqué",
        "location": "France"
    },
    {
        "name": "lionel lacombe",
        "title": "VP Enterprise IoT chez Orange",
        "firstname": "lionel",
        "lastname": "lacombe",
        "location": "France"
    },
    {
        "name": "Sonia Missul",
        "title": "IP Transit Product Manager at Orange",
        "firstname": "Sonia",
        "lastname": "Missul",
        "location": "France"
    },
    {
        "name": "Jean-Christophe Oriot",
        "title": "Vice President Of Software Development at Orange",
        "firstname": "Jean-Christophe",
        "middle": "Christophe",
        "lastname": "Oriot",
        "location": "France"
    },
    {
        "name": "Benjamin Sobiecki",
        "title": "TV Product Manager @Orange Belgium",
        "firstname": "Benjamin",
        "lastname": "Sobiecki",
        "location": "Belgium"
    },
    {
        "name": "Steve Blythe",
        "title": "Vice President at Orange",
        "firstname": "Steve",
        "lastname": "Blythe",
        "location": "United Kingdom"
    },
    {
        "name": "Dorothee Horps",
        "title": "VP, Strategic Partnerships Director, Entertainment, EMEA",
        "firstname": "Dorothee",
        "lastname": "Horps",
        "location": "France"
    },
    {
        "name": "Yannick DAGUILLON",
        "title": "Innovation Strategy @Orange",
        "firstname": "Yannick",
        "lastname": "DAGUILLON",
        "location": "France"
    },
    {
        "name": "Philippe Lucas",
        "title": "EVP Devices & Partnerships @Orange",
        "firstname": "Philippe",
        "lastname": "Lucas",
        "location": "France"
    },
    {
        "name": "Dominique THOME",
        "title": "Product Manager Innovation Data TV",
        "firstname": "Dominique",
        "lastname": "THOME",
        "location": "France"
    },
    {
        "name": "Guillaume Lacroix",
        "title": "Directeur, Produits & Services - Orange France",
        "firstname": "Guillaume",
        "lastname": "Lacroix",
        "location": "France"
    },
    {
        "name": "Frédéric DUBLANCHET",
        "title": "Chief Security Privacy & Risk Officer - Head of Media Content Protection",
        "firstname": "Frédéric",
        "lastname": "DUBLANCHET",
        "location": "France"
    },
    {
        "name": "Yvonnick Boursier",
        "title": "Director of operations and transformation for Orange digital services",
        "firstname": "Yvonnick",
        "lastname": "Boursier",
        "location": "France"
    },
    {
        "name": "Donna Soane",
        "title": "Director of Global Sponsorship at Orange",
        "firstname": "Donna",
        "lastname": "Soane",
        "location": "United Kingdom"
    },
    {
        "name": "Arnaud Vilain",
        "title": "Affaires Publiques @ Orange / Auditeur IHEDN",
        "firstname": "Arnaud",
        "lastname": "Vilain",
        "location": "France"
    },
    {
        "name": "Atika Boulgaz",
        "title": "Events & Experience Director at Orange Innovation",
        "firstname": "Atika",
        "lastname": "Boulgaz",
        "location": "France"
    },
    {
        "name": "David Baillergeau",
        "title": "SVP cloud platforms at Orange France",
        "firstname": "David",
        "lastname": "Baillergeau",
        "location": "France"
    },
    {
        "name": "Jérémie Cousseau",
        "title": "Roadmap stratégique RSE",
        "firstname": "Jérémie",
        "lastname": "Cousseau",
        "location": "France"
    },
    {
        "name": "Pascal Perrot",
        "title": "Head of video coding and distribution solutions at Orange Innovation",
        "firstname": "Pascal",
        "lastname": "Perrot",
        "location": "France"
    },
    {
        "name": "Guillaume Ducellier",
        "title": "Head of TV Factory",
        "firstname": "Guillaume",
        "lastname": "Ducellier",
        "location": "Belgium"
    },
    {
        "name": "Pierre-François Dubois",
        "title": "Senior Vice President of Innovation for Customer Engagement and Trust chez Orange",
        "firstname": "Pierre-François",
        "middle": "François",
        "lastname": "Dubois",
        "location": "France"
    },
    {
        "name": "Alain Tales",
        "title": "Energie program director at Orange",
        "firstname": "Alain",
        "lastname": "Tales",
        "location": "France"
    },
    {
        "name": "Claude LE GOFF",
        "title": "Responsable département Business Communication & Collaboration at Orange",
        "firstname": "Claude",
        "lastname": "LE GOFF",
        "lastname_simple": "goff",
        "location": "France"
    },
    {
        "name": "Jorge Febra",
        "title": "Technical Leader for Orange Home Connectivity Innovation portfolio",
        "firstname": "Jorge",
        "lastname": "Febra",
        "location": "France"
    },
    {
        "name": "Christophe Francois",
        "title": "Vice President Strategic Partnerships Orange",
        "firstname": "Christophe",
        "lastname": "Francois",
        "location": "France"
    },
    {
        "name": "Yann Ruello",
        "title": "Marketing Director @Orange | AI Author & Big Bang AI Co-founder",
        "firstname": "Yann",
        "lastname": "Ruello",
        "location": "France"
    },
    {
        "name": "Thierry Millet",
        "title": "CEO Orange Money Group Abidjan",
        "firstname": "Thierry",
        "lastname": "Millet",
        "location": "Côte d'Ivoire"
    },
    {
        "name": "Christophe FLAUX",
        "title": "Orange International new sales channels director",
        "firstname": "Christophe",
        "lastname": "FLAUX",
        "location": "France"
    },
    {
        "name": "Laurent Talibart",
        "title": "CDN Business Development Director, at Orange",
        "firstname": "Laurent",
        "lastname": "Talibart",
        "location": "France"
    },
    {
        "name": "Jean-Bernard Leduby",
        "title": "Orange",
        "firstname": "Jean-Bernard",
        "middle": "Bernard",
        "lastname": "Leduby",
        "location": "France"
    },
    {
        "name": "Noureddine HAMDANE",
        "title": "EVP Corporate Strategy, M&A, Technology Innovation International Business Development",
        "firstname": "Noureddine",
        "lastname": "HAMDANE",
        "location": "France"
    },
    {
        "name": "Nicolas Bry",
        "title": "Designing places for Innovation | Paris, Marseille, Africa | Entrepreneurs Mentor",
        "firstname": "Nicolas",
        "lastname": "Bry",
        "location": "France"
    },
    {
        "name": "Mariusz Gatza",
        "title": "CEO @ Orange Slovensko",
        "firstname": "Mariusz",
        "lastname": "Gatza",
        "location": "Slovakia"
    },
    {
        "name": "Vincent Pirson",
        "title": "Cable Core Access engineering chez Orange Belgique",
        "firstname": "Vincent",
        "lastname": "Pirson",
        "location": "Belgium"
    },
    {
        "name": "Julien Ducarroz",
        "title": "CEO @ Orange Romania",
        "firstname": "Julien",
        "lastname": "Ducarroz",
        "location": "Romania"
    },
    {
        "name": "Frédéric Campodonico",
        "title": "Head of digital at Orange Belgium",
        "firstname": "Frédéric",
        "lastname": "Campodonico",
        "location": "Belgium"
    },
    {
        "name": "David VIRET-LANGE",
        "title": "Directeur Entreprises France at Orange",
        "firstname": "David",
        "lastname": "VIRET-LANGE",
        "lastname_simple": "lange",
        "location": "France"
    },
    {
        "name": "Chem Assayag",
        "title": "C-level executive - Digital, TV, Telco - Orange",
        "firstname": "Chem",
        "lastname": "Assayag",
        "location": "France"
    },
    {
        "name": "Amman Abid",
        "title": "AI-Telco Panel Host & Moderator (Orange Open Tech) | Strategic Comms | Story Architect @ Orange",
        "firstname": "Amman",
        "lastname": "Abid",
        "location": "United Kingdom"
    },
    {
        "name": "Bruno Martinou",
        "title": "Head of Submarine Operations & Maintenance chez Orange",
        "firstname": "Bruno",
        "lastname": "Martinou",
        "location": "France"
    },
    {
        "name": "Yves Christol",
        "title": "Directeur Roadmap & Programmes",
        "firstname": "Yves",
        "lastname": "Christol",
        "location": "France"
    },
    {
        "name": "Wojtek Makowski",
        "title": "Vice President CPE Ecosystem at Orange",
        "firstname": "Wojtek",
        "lastname": "Makowski",
        "location": "France"
    },
    {
        "name": "Otilia Anton",
        "title": "Director of Orange LiveNet | Network APIs",
        "firstname": "Otilia",
        "lastname": "Anton",
        "location": "France"
    },
    {
        "name": "Raluca - Andreea ATANASIU",
        "title": "Head of Purchasing and Supply Chain | Bachelor of Economics",
        "firstname": "Raluca",
        "middle": "Andreea",
        "lastname": "ATANASIU",
        "location": "Moldova"
    },
    {
        "name": "Nicole Clarke",
        "title": "Director of Corporate Communications, Orange Group",
        "firstname": "Nicole",
        "lastname": "Clarke",
        "location": "United Kingdom"
    },
    {
        "name": "Frédéric Bouity",
        "title": "Global Expert SRM for Orange Group",
        "firstname": "Frédéric",
        "lastname": "Bouity",
        "location": "France"
    },
    {
        "name": "Bruno Zerbib",
        "title": "Chief Technology and Innovation Officer @Orange",
        "firstname": "Bruno",
        "lastname": "Zerbib",
        "location": "France"
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
    location = contact.get('location', 'France')
    
    variants = []
    
    # Common patterns for Orange
    # Pattern 1: firstname.lastname@orange.com (Orange Group - most common)
    variants.append(f"{firstname}.{lastname}@orange.com")
    
    # Pattern 2: firstname.lastname@orange.fr (Orange France)
    if location == "France":
        variants.append(f"{firstname}.{lastname}@orange.fr")
    
    # Pattern 3: firstname.lastname@orange.be (Orange Belgium)
    if location == "Belgium":
        variants.append(f"{firstname}.{lastname}@orange.be")
    
    # Pattern 4: firstname.lastname@orange-innovation.com (Orange Innovation)
    if "Innovation" in contact.get('title', ''):
        variants.append(f"{firstname}.{lastname}@orange-innovation.com")
    
    # Pattern 5: firstname_lastname@orange.com
    variants.append(f"{firstname}_{lastname}@orange.com")
    
    # Pattern 6: f.lastname@orange.com (first initial)
    variants.append(f"{firstname[0]}.{lastname}@orange.com")
    
    # Pattern 7: firstname.middle.lastname@orange.com (for compound names)
    if middle:
        variants.append(f"{firstname}.{middle}.{lastname}@orange.com")
        variants.append(f"{firstname}.{middle[0]}.{lastname}@orange.com")
    
    # Pattern 8: Use simplified lastname for compound names (LE GOFF -> goff, VIRET-LANGE -> lange)
    if lastname_simple:
        variants.append(f"{firstname}.{lastname_simple}@orange.com")
        if location == "France":
            variants.append(f"{firstname}.{lastname_simple}@orange.fr")
    
    # Pattern 9: Handle hyphenated names (Pierre-François -> pierre.francois or pierre.francois)
    if "-" in contact['firstname']:
        firstname_parts = contact['firstname'].lower().split('-')
        if len(firstname_parts) > 1:
            variants.append(f"{normalize_name(firstname_parts[0])}.{normalize_name(firstname_parts[1])}.{lastname}@orange.com")
            variants.append(f"{normalize_name(firstname_parts[0])}.{normalize_name(firstname_parts[1][0])}.{lastname}@orange.com")
    
    # Pattern 10: For country-specific Orange entities
    if location == "Romania":
        variants.append(f"{firstname}.{lastname}@orange.ro")
    elif location == "Slovakia":
        variants.append(f"{firstname}.{lastname}@orange.sk")
    elif location == "United Kingdom":
        variants.append(f"{firstname}.{lastname}@orange.co.uk")
    elif location == "Côte d'Ivoire":
        variants.append(f"{firstname}.{lastname}@orange.ci")
    elif location == "Moldova":
        variants.append(f"{firstname}.{lastname}@orange.md")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("Orange Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research:")
print("- Orange Group uses @orange.com for corporate contacts")
print("- Orange France uses @orange.fr")
print("- Orange Belgium uses @orange.be")
print("- Orange Innovation may use @orange-innovation.com")
print("- Country-specific domains: @orange.ro, @orange.sk, @orange.co.uk, etc.")
print("- Common pattern: firstname.lastname@orange.com")
print("- Special characters (é, è, ç, ï, ô) typically converted to standard ASCII")
print("- Compound names (Jean-Pierre, Pierre-François) may use middle initial or full middle name")
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

