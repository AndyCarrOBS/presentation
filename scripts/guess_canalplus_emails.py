#!/usr/bin/env python3
"""
Script to generate likely email addresses for Canal+ Group contacts based on common patterns.
"""
import re

# Canal+ Group contacts with their full names
contacts = [
    {
        "name": "Jerome Trift",
        "title": "Experienced media industry manager, with 20 years at CANAL+",
        "firstname": "Jerome",
        "lastname": "Trift",
        "location": "France"
    },
    {
        "name": "Timothee Vidal",
        "title": "Intrapreneur building new ventures at Canal+ | Streaming | Content Monetization",
        "firstname": "Timothee",
        "lastname": "Vidal",
        "location": "France"
    },
    {
        "name": "Stéphane BAUMIER",
        "title": "CANAL+ Group Chief Technology Officer * CANAL+ Group COMEX Member *",
        "firstname": "Stéphane",
        "lastname": "BAUMIER",
        "location": "France"
    },
    {
        "name": "Alexandre Bac",
        "title": "Managing Director Asia Pacific at CANAL+ DISTRIBUTION, Canal+ Group",
        "firstname": "Alexandre",
        "lastname": "Bac",
        "location": "Singapore"
    },
    {
        "name": "Martijn Van Hout",
        "title": "Country Manager DACH at CANAL+ Luxembourg",
        "firstname": "Martijn",
        "middle": "Van",
        "lastname": "Hout",
        "location": "Luxembourg"
    },
    {
        "name": "Laurent Cardona",
        "title": "Technical Project Manager at CANAL+ Group",
        "firstname": "Laurent",
        "lastname": "Cardona",
        "location": "France"
    },
    {
        "name": "Séverine Garusso",
        "title": "Head of New Activities - Canal+ group",
        "firstname": "Séverine",
        "lastname": "Garusso",
        "location": "France"
    },
    {
        "name": "Jean-Marc Audry",
        "title": "Director of Product Management & Product Design at CANAL+",
        "firstname": "Jean-Marc",
        "middle": "Marc",
        "lastname": "Audry",
        "location": "France"
    },
    {
        "name": "Olivier Germain",
        "title": "OPS CANAL+ TECH DOMAIN DIRECTOR",
        "firstname": "Olivier",
        "lastname": "Germain",
        "location": "France"
    },
    {
        "name": "Aurélien Venet",
        "title": "Head of Media, IT and Digital Procurement chez CANAL+ Group",
        "firstname": "Aurélien",
        "lastname": "Venet",
        "location": "France"
    },
    {
        "name": "Olivier Mesmeur",
        "title": "Product & Engineering Leader - Building Scalable Products & High-Performing Teams",
        "firstname": "Olivier",
        "lastname": "Mesmeur",
        "location": "France"
    },
    {
        "name": "Fabrice Torres",
        "title": "Senior Project Director at CANAL+ Group",
        "firstname": "Fabrice",
        "lastname": "Torres",
        "location": "France"
    },
    {
        "name": "Jacques du PUY",
        "title": "Member of the Management Board of CANAL+ in charge of Global Pay TV",
        "firstname": "Jacques",
        "middle": "du",
        "lastname": "PUY",
        "location": "France"
    },
    {
        "name": "Thomas Follin",
        "title": "Chief Global Transformation Officer",
        "firstname": "Thomas",
        "lastname": "Follin",
        "location": "France"
    },
    {
        "name": "Marianne Bédé",
        "title": "CEO CANAL+ Distribution Canada - SVP Global Marketing - Head of Market studies",
        "firstname": "Marianne",
        "lastname": "Bédé",
        "location": "France"
    },
    {
        "name": "ROVER Cécile",
        "title": "Product Architect at CANAL+ Group",
        "firstname": "Cécile",
        "lastname": "ROVER",
        "location": "France",
        "note": "Name order reversed - Cécile is first name"
    },
    {
        "name": "Szilvia Kiss",
        "title": "Managing Director | TV, OTT, Streaming, Media & Entertainment",
        "firstname": "Szilvia",
        "lastname": "Kiss",
        "location": "Hungary"
    },
    {
        "name": "Benoît Audouard",
        "title": "Head of product delivery myCANAL chez CANAL+ Group",
        "firstname": "Benoît",
        "lastname": "Audouard",
        "location": "France"
    },
    {
        "name": "Abdelkrim Nimour",
        "title": "Head of US Studios Acquisitions at CANAL+",
        "firstname": "Abdelkrim",
        "lastname": "Nimour",
        "location": "France"
    },
    {
        "name": "PATRICE LETOURNEUR",
        "title": "Operations manager of OTT/IPTV/DTH/DTT platforms",
        "firstname": "PATRICE",
        "lastname": "LETOURNEUR",
        "location": "France"
    },
    {
        "name": "Michal Wojciechowski",
        "title": "Digital Products, Services and Partnerships at CANAL+",
        "firstname": "Michal",
        "lastname": "Wojciechowski",
        "location": "Poland"
    },
    {
        "name": "Jean-Christophe DEKEYSER",
        "title": "ULTRA HD - 4K - HDR - ADDRESSABLE TV - OTT - STRATEGY",
        "firstname": "Jean-Christophe",
        "middle": "Christophe",
        "lastname": "DEKEYSER",
        "location": "France"
    },
    {
        "name": "Laurent Miton",
        "title": "RESPONSABLE QUALITE & PROCESS EXPLOITATION chez CANAL+",
        "firstname": "Laurent",
        "lastname": "Miton",
        "location": "France"
    },
    {
        "name": "Julien Winocq",
        "title": "Project Manager chez CANAL+",
        "firstname": "Julien",
        "lastname": "Winocq",
        "location": "France"
    },
    {
        "name": "Philippe SCHWERER",
        "title": "Directeur Partenariats industriels et New Business",
        "firstname": "Philippe",
        "lastname": "SCHWERER",
        "location": "France"
    },
    {
        "name": "Stéphanie JEANDOT",
        "title": "Directrice Stratégie Technique Distribution | Canal plus Group",
        "firstname": "Stéphanie",
        "lastname": "JEANDOT",
        "location": "France"
    },
    {
        "name": "Marc Heller",
        "title": "General Management (growth, turn-around, transformation), Strategy and M&A in Media/Entertainment & Consumer Businesses",
        "firstname": "Marc",
        "lastname": "Heller",
        "location": "France"
    },
    {
        "name": "Jean-Robert LLEDO",
        "title": "Project Director",
        "firstname": "Jean-Robert",
        "middle": "Robert",
        "lastname": "LLEDO",
        "location": "France"
    },
    {
        "name": "Christophe PINARD-LEGRY",
        "title": "Directeur Général de CANAL+ France en charge du business CEO of CANAL+ France",
        "firstname": "Christophe",
        "lastname": "PINARD-LEGRY",
        "lastname_simple": "legry",
        "location": "France"
    },
    {
        "name": "Alco De Jong",
        "title": "Country Manager Benelux CANAL+ Group I Co-founder ridemeister",
        "firstname": "Alco",
        "middle": "De",
        "lastname": "Jong",
        "location": "Netherlands"
    },
    {
        "name": "David Mignot",
        "title": "CEO of CANAL+ AFRICA",
        "firstname": "David",
        "lastname": "Mignot",
        "location": "France"
    },
    {
        "name": "Emmanuel ALDEGUER",
        "title": "C+TECH Resources Manager, CANAL+ Group",
        "firstname": "Emmanuel",
        "lastname": "ALDEGUER",
        "location": "France"
    },
    {
        "name": "Laurent Faureytier",
        "title": "Security Architect for Content Protection, CA/DRM expert at CANAL+ Group",
        "firstname": "Laurent",
        "lastname": "Faureytier",
        "location": "France"
    },
    {
        "name": "Clémentine Egasse Tugendhat",
        "title": "Senior Vice President, Content - Production / Directrice Chaines Thématiques et Sociétés de Production CANAL + Group",
        "firstname": "Clémentine",
        "middle": "Egasse",
        "lastname": "Tugendhat",
        "location": "France"
    },
    {
        "name": "Philippe Rivas",
        "title": "Directeur Technique Distribution - Canal+",
        "firstname": "Philippe",
        "lastname": "Rivas",
        "location": "France"
    },
    {
        "name": "Manuel Rougeron",
        "title": "Executive Vice President Asia Pacific at CANAL+ Group",
        "firstname": "Manuel",
        "lastname": "Rougeron",
        "location": "Singapore"
    },
    {
        "name": "Jean-Marc JURAMIE",
        "title": "Directeur général adjoint de CANAL+ France en charge des programmes et des antennes",
        "firstname": "Jean-Marc",
        "middle": "Marc",
        "lastname": "JURAMIE",
        "location": "France"
    },
    {
        "name": "Alison D.",
        "title": "CANAL+ | Media & Entertainment",
        "firstname": "Alison",
        "lastname": "D",
        "location": "France",
        "note": "Incomplete last name"
    },
    {
        "name": "Cédric VIALLE",
        "title": "Digital transformation, Technologies",
        "firstname": "Cédric",
        "lastname": "VIALLE",
        "location": "France"
    },
    {
        "name": "Gildas Girondin",
        "title": "Directeur Produit / Technique",
        "firstname": "Gildas",
        "lastname": "Girondin",
        "location": "France"
    },
    {
        "name": "Peybernes Pierre",
        "title": "Head of digital products and projects at CANAL+ INTERNATIONAL",
        "firstname": "Pierre",
        "lastname": "Peybernes",
        "location": "France",
        "note": "Name order reversed - Pierre is first name"
    },
    {
        "name": "Arnaud Stelian",
        "title": "Project Manager",
        "firstname": "Arnaud",
        "lastname": "Stelian",
        "location": "France"
    },
    {
        "name": "Benjamin Belle",
        "title": "CEO CANAL+ Antilles/Guyane",
        "firstname": "Benjamin",
        "lastname": "Belle",
        "location": "France"
    },
    {
        "name": "Bruno ROUSSEL",
        "title": "Media & Tech | PMO & Product Management | OTT - Streaming - Broadcast - Transversal projects",
        "firstname": "Bruno",
        "lastname": "ROUSSEL",
        "location": "France"
    },
    {
        "name": "Amir Mureškić",
        "title": "Content Strategy Director at Canal+ Benelux and Central Europe",
        "firstname": "Amir",
        "lastname": "Mureškić",
        "location": "Luxembourg"
    },
    {
        "name": "Jerome Herault",
        "title": "Architecture and services platforms Department Manager chez Canal+",
        "firstname": "Jerome",
        "lastname": "Herault",
        "location": "France"
    },
    {
        "name": "Pierre-Paul VANDER SANDE",
        "title": "Senior VP Advertising Strategy at CANAL+ INTERNATIONAL",
        "firstname": "Pierre-Paul",
        "middle": "Paul",
        "lastname": "VANDER SANDE",
        "lastname_simple": "sande",
        "location": "Belgium"
    },
    {
        "name": "Doriana K.",
        "title": "Strategic Projects / Programs @ Canal + Group",
        "firstname": "Doriana",
        "lastname": "K",
        "location": "France",
        "note": "Incomplete last name"
    },
    {
        "name": "Muriël Goor",
        "title": "Content Director at CANAL+ Group | Founder, The Holistic Way",
        "firstname": "Muriël",
        "lastname": "Goor",
        "location": "Netherlands"
    },
    {
        "name": "Cedric Coutadeur",
        "title": "Project Management Officer at CANAL+ INTERNATIONAL",
        "firstname": "Cedric",
        "lastname": "Coutadeur",
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
        'š': 's',
        'ć': 'c',
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
    
    # Common patterns for Canal+ Group
    # Pattern 1: firstname.lastname@canal-plus.com (Canal+ Group - most common based on known contacts)
    variants.append(f"{firstname}.{lastname}@canal-plus.com")
    
    # Pattern 2: firstname.lastname@canalplus.fr (Canal+ France)
    if location == "France":
        variants.append(f"{firstname}.{lastname}@canalplus.fr")
    
    # Pattern 3: firstname.lastname@canalplus.com
    variants.append(f"{firstname}.{lastname}@canalplus.com")
    
    # Pattern 4: firstname_lastname@canal-plus.com
    variants.append(f"{firstname}_{lastname}@canal-plus.com")
    
    # Pattern 5: f.lastname@canal-plus.com (first initial)
    variants.append(f"{firstname[0]}.{lastname}@canal-plus.com")
    
    # Pattern 6: firstname.middle.lastname@canal-plus.com (for compound names)
    if middle:
        variants.append(f"{firstname}.{middle}.{lastname}@canal-plus.com")
        variants.append(f"{firstname}.{middle[0]}.{lastname}@canal-plus.com")
    
    # Pattern 7: Use simplified lastname for compound names (PINARD-LEGRY -> legry, VANDER SANDE -> sande)
    if lastname_simple:
        variants.append(f"{firstname}.{lastname_simple}@canal-plus.com")
        if location == "France":
            variants.append(f"{firstname}.{lastname_simple}@canalplus.fr")
    
    # Pattern 8: Handle "De" prefix specially (De Jong -> jong)
    if "de" in lastname:
        lastname_no_de = lastname.replace("de", "").strip()
        if lastname_no_de:
            variants.append(f"{firstname}.{lastname_no_de}@canal-plus.com")
    
    # Pattern 9: Handle "Van" prefix specially (Van Hout -> hout)
    if "van" in lastname:
        lastname_no_van = lastname.replace("van", "").strip()
        if lastname_no_van:
            variants.append(f"{firstname}.{lastname_no_van}@canal-plus.com")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

print("Canal+ Group Contact Email Address Predictions")
print("=" * 60)
print("\nBased on research and known contacts:")
print("- Canal+ Group uses @canal-plus.com (confirmed from previous contacts)")
print("- Canal+ France uses @canalplus.fr")
print("- Alternative: @canalplus.com")
print("- Common pattern: firstname.lastname@canal-plus.com")
print("- Special characters (é, è, ç, ï, ô, š, ć) typically converted to standard ASCII")
print("- Compound names (PINARD-LEGRY, VANDER SANDE, du PUY) may be simplified")
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

