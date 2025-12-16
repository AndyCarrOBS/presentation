#!/usr/bin/env python3
"""
Script to add Orange contacts to the specification file.
"""
import re

# Orange contacts organized by category
orange_contacts = {
    "executive_leadership": [
        ("Bruno Zerbib", "Chief Technology and Innovation Officer @Orange", "bruno.zerbib@orange.com", "France"),
        ("Noureddine HAMDANE", "EVP Corporate Strategy, M&A, Technology Innovation International Business Development", "noureddine.hamdane@orange.com", "France"),
        ("Philippe Lucas", "EVP Devices & Partnerships @Orange", "philippe.lucas@orange.com", "France"),
        ("Arnaud Alvarez", "Chief Commercial Officer (CCO), Viaccess-Orca, Orange Group", "arnaud.alvarez@orange.com", "France"),
    ],
    "tv_product_services": [
        ("Guillaume Lacroix", "Directeur, Produits & Services - Orange France", "guillaume.lacroix@orange.com", "France"),
        ("Benjamin Sobiecki", "TV Product Manager @Orange Belgium", "benjamin.sobiecki@orange.com", "Belgium"),
        ("Dominique THOME", "Product Manager Innovation Data TV", "dominique.thome@orange.com", "France"),
        ("Guillaume Ducellier", "Head of TV Factory", "guillaume.ducellier@orange.com", "Belgium"),
    ],
    "content_media": [
        ("Dorothee Horps", "VP, Strategic Partnerships Director, Entertainment, EMEA", "dorothee.horps@orange.com", "France"),
        ("Pascal Perrot", "Head of video coding and distribution solutions at Orange Innovation", "pascal.perrot@orange.com", "France"),
    ],
    "technology_engineering": [
        ("Jean-Christophe Oriot", "Vice President Of Software Development at Orange", "jeanchristophe.oriot@orange.com", "France"),
        ("Serge Francois", "Head of Broadband CPE Engineering", "serge.francois@orange.com", "Belgium"),
        ("Wojtek Makowski", "Vice President CPE Ecosystem at Orange", "wojtek.makowski@orange.com", "France"),
        ("Jorge Febra", "Technical Leader for Orange Home Connectivity Innovation portfolio", "jorge.febra@orange.com", "France"),
        ("Vincent Pirson", "Cable Core Access engineering chez Orange Belgique", "vincent.pirson@orange.com", "Belgium"),
    ],
    "partnerships_business_development": [
        ("Christophe Francois", "Vice President Strategic Partnerships Orange", "christophe.francois@orange.com", "France"),
        ("Jean-Pierre Combe", "API & Apps Distribution Director at Orange", "jeanpierre.combe@orange.com", "France"),
        ("Laurent Talibart", "CDN Business Development Director, at Orange", "laurent.talibart@orange.com", "France"),
    ],
    "innovation_digital": [
        ("Jean-Marc Barraqué", "Digital Transformation Director at Orange", "jeanmarc.barraque@orange.com", "France"),
        ("Yannick DAGUILLON", "Innovation Strategy @Orange", "yannick.daguillon@orange.com", "France"),
        ("Yvonnick Boursier", "Director of operations and transformation for Orange digital services", "yvonnick.boursier@orange.com", "France"),
        ("Atika Boulgaz", "Events & Experience Director at Orange Innovation", "atika.boulgaz@orange.com", "France"),
        ("Nicolas Bry", "Designing places for Innovation | Paris, Marseille, Africa", "nicolas.bry@orange.com", "France"),
    ],
    "security_risk": [
        ("Frédéric DUBLANCHET", "Chief Security Privacy & Risk Officer - Head of Media Content Protection", "frederic.dublanchet@orange.com", "France"),
    ],
    "country_ceos": [
        ("Julien Ducarroz", "CEO @ Orange Romania", "julien.ducarroz@orange.com", "Romania"),
        ("Mariusz Gatza", "CEO @ Orange Slovensko", "mariusz.gatza@orange.com", "Slovakia"),
        ("Thierry Millet", "CEO Orange Money Group Abidjan", "thierry.millet@orange.com", "Côte d'Ivoire"),
    ],
    "other_roles": [
        ("Sonia Missul", "IP Transit Product Manager at Orange", "sonia.missul@orange.com", "France"),
        ("lionel lacombe", "VP Enterprise IoT chez Orange", "lionel.lacombe@orange.com", "France"),
        ("Steve Blythe", "Vice President at Orange", "steve.blythe@orange.com", "United Kingdom"),
        ("Donna Soane", "Director of Global Sponsorship at Orange", "donna.soane@orange.com", "United Kingdom"),
        ("Arnaud Vilain", "Affaires Publiques @ Orange / Auditeur IHEDN", "arnaud.vilain@orange.com", "France"),
        ("David Baillergeau", "SVP cloud platforms at Orange France", "david.baillergeau@orange.com", "France"),
        ("Jérémie Cousseau", "Roadmap stratégique RSE", "jeremie.cousseau@orange.com", "France"),
        ("Pierre-François Dubois", "Senior Vice President of Innovation for Customer Engagement and Trust chez Orange", "pierrefrancois.dubois@orange.com", "France"),
        ("Alain Tales", "Energie program director at Orange", "alain.tales@orange.com", "France"),
        ("Claude LE GOFF", "Responsable département Business Communication & Collaboration at Orange", "claude.goff@orange.com", "France"),
        ("Yann Ruello", "Marketing Director @Orange | AI Author & Big Bang AI Co-founder", "yann.ruello@orange.com", "France"),
        ("Christophe FLAUX", "Orange International new sales channels director", "christophe.flaux@orange.com", "France"),
        ("Jean-Bernard Leduby", "Orange", "jeanbernard.leduby@orange.com", "France"),
        ("Frédéric Campodonico", "Head of digital at Orange Belgium", "frederic.campodonico@orange.com", "Belgium"),
        ("David VIRET-LANGE", "Directeur Entreprises France at Orange", "david.lange@orange.com", "France"),
        ("Chem Assayag", "C-level executive - Digital, TV, Telco - Orange", "chem.assayag@orange.com", "France"),
        ("Amman Abid", "AI-Telco Panel Host & Moderator (Orange Open Tech) | Strategic Comms | Story Architect @ Orange", "amman.abid@orange.com", "United Kingdom"),
        ("Bruno Martinou", "Head of Submarine Operations & Maintenance chez Orange", "bruno.martinou@orange.com", "France"),
        ("Yves Christol", "Directeur Roadmap & Programmes", "yves.christol@orange.com", "France"),
        ("Otilia Anton", "Director of Orange LiveNet | Network APIs", "otilia.anton@orange.com", "France"),
        ("Raluca - Andreea ATANASIU", "Head of Purchasing and Supply Chain | Bachelor of Economics", "raluca.atanasiu@orange.com", "Moldova"),
        ("Nicole Clarke", "Director of Corporate Communications, Orange Group", "nicole.clarke@orange.com", "United Kingdom"),
        ("Frédéric Bouity", "Global Expert SRM for Orange Group", "frederic.bouity@orange.com", "France"),
    ],
}

def generate_contacts_markdown():
    """Generate markdown for all Orange contacts."""
    markdown = "\n### Additional Orange Contacts\n\n"
    
    for category, contacts_list in orange_contacts.items():
        category_name = category.replace("_", " ").title()
        markdown += f"#### {category_name}\n\n"
        
        for name, title, email, location in contacts_list:
            markdown += f"**{name}**\n"
            markdown += f"- **Title**: {title}\n"
            markdown += f"- **Email**: {email} (predicted)\n"
            markdown += f"- **Location**: {location}\n"
            markdown += f"- **Platform**: LinkedIn\n"
            markdown += f"- **Note**: {title}\n\n"
    
    return markdown

if __name__ == "__main__":
    print(generate_contacts_markdown())

