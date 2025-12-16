#!/usr/bin/env python3
"""
Script to add detailed contact information to operator specification files.
"""
import os
from pathlib import Path

# Detailed contacts organized by operator and role type
DETAILED_CONTACTS = {
    "Ziggo": {
        "market_facing_exec": [
            ("Stephen van Rooyen", "CEO VodafoneZiggo (effective September 2024)", "Vodafone", "Market-facing / exec sponsor")
        ],
        "market_facing_content": [
            ("Raymond van der Vliet", "Content & Programming Director, VodafoneZiggo", "VodafoneZiggo", "Market-facing (TV proposition/content)")
        ],
        "market_facing_marketing": [
            ("Koen Cluistra", "Consumer Marketing Director, VodafoneZiggo", "VodafoneZiggo", "Market-facing (consumer marketing / Ziggo TV launch messaging)")
        ],
        "technology": [
            ("OPEN", "Needs dedicated Ziggo TV platform/engineering owner", "", "Technology / Specs owner")
        ],
        "onboarding": [
            ("OPEN", "Needs 'Connected TV onboarding / device certification / TV platform lead'", "", "Onboarding owner")
        ]
    },
    "KPN": {
        "market_facing_partnerships": [
            ("Cornelis Kalma", "Director Product & Marketing, TV & Entertainment (explicitly responsible for partnerships)", "LinkedIn", "Market-facing + partnerships")
        ],
        "technology": [
            ("Alejandro Casal Gomez", "Senior TV Technical Product Manager, KPN", "adwantedevents.com", "Technology / Specs owner (speaker listing)")
        ],
        "onboarding": [
            ("OPEN", "Likely inside TV Platforms / TV Tech Product; needs KPN-specific 'TV Platforms Lead' / 'Device onboarding'", "", "Onboarding owner")
        ]
    },
    "M7 Canal Digitaal": {
        "market_facing_exec": [
            ("Ruud Arts", "Managing Director, CANAL+ Netherlands", "thetvplatform.zattoo.com", "Exec sponsor (market-facing)")
        ],
        "onboarding": [
            ("OPEN", "M7 platform engineering / device onboarding lead for NL", "", "Onboarding / Specs owner")
        ]
    },
    "Norlys": {
        "tv_product_leadership": [
            ("Jacob Vestergaard", "Leads TV dept at Norlys; responsible for commercial + product mgmt incl. Stofa TV products", "LinkedIn", "TV product leadership (strong onboarding entry)")
        ],
        "product_stakeholder": [
            ("Lasse Birch Eilenberg", "Senior Product Manager/Owner TV & Streaming (B2C), Norlys", "LinkedIn", "Additional product stakeholder (useful operational contact)")
        ],
        "technology": [
            ("OPEN", "Need 'TV platform engineering/architecture' lead at Norlys/Stofa", "", "Technology / Specs owner")
        ]
    },
    "YouSee": {
        "technology_product": [
            ("Lars Bjerg", "Senior Director, Technical Product (TV & OTT) responsible for product management & development across TDC/YouSee/Wholesale", "LinkedIn", "Technology + product/spec direction")
        ],
        "product_leadership": [
            ("Bozena Haslund", "Product Management Lead (OTT brand / TV & streaming context)", "LinkedIn", "Product leadership (new OTT brand context)")
        ],
        "onboarding": [
            ("OPEN", "Often a 'TV Platforms / Device' function inside YouSee TV product org", "", "Onboarding owner")
        ]
    },
    "Allente": {
        "technology": [
            ("Jon Espen Nergård", "CTO Allente", "Reddit", "Technology / Specs owner")
        ],
        "onboarding": [
            ("OPEN", "Local DK onboarding owner", "", "Onboarding owner (local DK)")
        ]
    },
    "Boxer HD": {
        "market_facing": [
            ("Jeff Vulevic Brødbæk", "CCO (commercial/partner-facing)", "ContactOut", "Market-facing commercial")
        ],
        "technology": [
            ("OPEN", "Technology / onboarding owner", "", "Technology / onboarding owner")
        ]
    },
    "Telenet": {
        "market_facing_entertainment": [
            ("Ivor Micallef", "Director of Entertainment / Head of Entertainment Products (industry interviews + profile)", "LinkedIn, Telco Magazine", "Market-facing / entertainment strategy + partnerships")
        ],
        "technology": [
            ("OPEN", "Need Telenet TV platform tech/spec owner", "", "Technology / Specs owner")
        ],
        "onboarding": [
            ("OPEN", "Onboarding owner", "", "Onboarding owner")
        ]
    },
    "Proximus Pickx": {
        "onboarding_platform": [
            ("Pradeep Thekkedath", "TV Platforms Lead (Pickx), Proximus (also referenced in platform expansion press)", "LinkedIn", "Onboarding + platform lead (excellent entry point)")
        ],
        "technology_program": [
            ("Accenture", "Next-gen digital TV platform engagement (confirms major platform workstream; helps route to internal owners)", "Accenture Newsroom", "Technology program context (platform re-architecture)")
        ],
        "market_facing": [
            ("OPEN", "Need Pickx product/entertainment commercial lead name", "", "Market-facing")
        ]
    },
    "Voo": {
        "technology": [
            ("Xavier Lüthi", "Director Technology Operations & Quality, VOO", "Vodafone", "Technology / Specs owner")
        ],
        "market_facing_content": [
            ("Christian Loiseau", "Directeur général Be tv & Director Content & Media @VOO", "Telia Company", "Market-facing (content)")
        ],
        "onboarding": [
            ("OPEN", "Onboarding owner", "", "Onboarding owner")
        ]
    },
    "Orange France": {
        "market_facing_tv": [
            ("Guillaume Lacroix", "Director Product & Services, Orange France (quoted on STB6 launch)", "SoftAtHome", "Market-facing + TV device/platform sponsor")
        ],
        "technology": [
            ("Nathalie Vandermeersch", "TV & Entertainment platforms technical director, Orange France", "LinkedIn", "Technology / Specs owner (strong)")
        ],
        "onboarding": [
            ("OPEN", "Usually 'TV device certification / Smart TV partnerships' under TV platforms", "", "Onboarding owner")
        ]
    },
    "Free France": {
        "program_context": [
            ("Iliad", "Press release for Free TV app (explicit smart TV availability; use to locate internal owner)", "Iliad", "Program context (smart TV app launch)")
        ],
        "market_facing_content": [
            ("Frédéric Goyon", "Responsable des contenus, Free", "LinkedIn", "Market-facing (content stakeholder)")
        ],
        "technology": [
            ("OPEN", "Need Freebox/TV platform technical director or device onboarding lead", "", "Technology / Specs owner")
        ]
    },
    "SFR": {
        "market_facing_product": [
            ("Nicolas Leroy", "Head of B2C Product Management (history includes TV content product mgmt)", "LinkedIn", "Market-facing / product owner line")
        ],
        "technology": [
            ("OPEN", "Need 'TV platforms / OTT platform' technical director", "", "Technology / Specs owner")
        ]
    },
    "Bouygues Telecom": {
        "market_facing": [
            ("Régis Rembado", "Head of TV & broadband product marketing", "LinkedIn", "Market-facing (TV & broadband proposition)")
        ],
        "technology_stb": [
            ("Herminio de Faria", "IPTV STB Director (quoted in Android TV STB partnership coverage)", "Advanced Television", "Technology / STB program leadership")
        ],
        "onboarding": [
            ("OPEN", "Onboarding owner", "", "Onboarding owner")
        ]
    },
    "Canal+ France": {
        "market_facing_exec": [
            ("Maxime Saada", "CEO CANAL+ Group (governance listing)", "3SS", "Market-facing exec sponsor")
        ],
        "technology": [
            ("Philippe Rivas", "Distribution CTO, CANAL+ Group (referenced in partner coverage)", "LinkedIn", "Technology / specs owner")
        ],
        "onboarding": [
            ("OPEN", "Onboarding owner", "", "Onboarding owner")
        ]
    },
    "Fransat": {
        "technology": [
            ("Alexandre Joffre", "Direction technique (Digital), FRANSAT", "LinkedIn", "Technology / Specs owner")
        ],
        "market_facing": [
            ("Lydia Gaillard", "Commercial & Marketing Director, FRANSAT", "LinkedIn", "Market-facing")
        ],
        "onboarding": [
            ("OPEN", "Onboarding owner", "", "Onboarding owner")
        ]
    },
    "Magenta TV": {
        "market_facing": [
            ("Christoph Ewerth", "Head of Product & Content B2C (Magenta TV area)", "LinkedIn", "Market-facing (product/content)")
        ],
        "technology": [
            ("OPEN", "Technology / onboarding owner", "", "Technology / onboarding owner")
        ]
    },
    "SimpliTV": {
        "exec_sponsor": [
            ("Patrick Preissl", "CEO, simpliTV", "Insight TV Newsroom", "Exec sponsor")
        ],
        "product_delivery": [
            ("Helmut Riemer", "Product Manager / Circle Lead, simpliTV", "LinkedIn", "Product delivery stakeholder")
        ],
        "technology": [
            ("OPEN", "Technology/spec owner", "", "Technology/spec owner")
        ]
    },
    "M7 HD Austria": {
        "market_facing": [
            ("Peter Kail", "Marketing role tied to HD Austria/AustriaSat (useful routing contact)", "LinkedIn", "Market-facing (brand/marketing)")
        ],
        "technology": [
            ("OPEN", "Technology/spec owner", "", "Technology/spec owner")
        ]
    },
    "Swisscom TV": {
        "technology": [
            ("Peter Fregelius", "Head of TV & Entertainment Technology (vendor case study + historical press)", "3SS, Advanced Television", "Technology / Specs owner (excellent)")
        ],
        "onboarding": [
            ("OPEN", "Often sits with TV platform engineering or device partnerships under TV & Entertainment Technology", "", "Onboarding owner")
        ]
    },
    "Sunrise": {
        "technology_platform": [
            ("Fabrizio Campanale", "VP / Senior Director, Entertainment & In-Home Connectivity (responsible for video platforms/services)", "LinkedIn, Telco Magazine", "Technology + platform ownership")
        ],
        "onboarding": [
            ("OPEN", "Onboarding owner", "", "Onboarding owner")
        ]
    },
    "Salt TV": {
        "product_stakeholder": [
            ("Alexandre Perret", "TV & Content Product Manager (Salt)", "THE ORG", "Product stakeholder")
        ],
        "technology": [
            ("OPEN", "Technology/spec owner", "", "Technology/spec owner")
        ]
    },
    "Zattoo": {
        "technology_product": [
            ("Bert Schulzki", "Chief Product & Technology Officer (official Zattoo press)", "zattoo.com", "Technology + product/spec owner")
        ],
        "market_facing_exec": [
            ("Roger Elsener", "CEO (Zattoo management page)", "thetvplatform.zattoo.com", "Market-facing exec")
        ]
    },
    "Sky Italia": {
        "market_facing_exec": [
            ("Andrea Duilio", "CEO Sky Italia (Sky leadership page)", "Sky Group", "Exec sponsor (market-facing)")
        ],
        "technology": [
            ("OPEN", "Need Sky Italia platform/technology leader tied to device onboarding/specs", "", "Technology/spec owner")
        ]
    },
    "TIM": {
        "product_experience": [
            ("Antonio Imbimbo", "Head of Product & Experience Design, TIM (profile)", "LinkedIn", "Product + experience (onboarding-adjacent)")
        ],
        "onboarding": [
            ("OPEN", "Onboarding/spec owner", "", "Onboarding/spec owner")
        ]
    },
    "Vodafone Italy": {
        "onboarding_partnerships": [
            ("Claudia Sarnelli", "Head of Vodafone TV product & Content Partnership", "LinkedIn", "Onboarding + partnerships (strong)")
        ],
        "technology": [
            ("OPEN", "Technology/spec owner", "", "Technology/spec owner")
        ]
    },
    "O2 Czech Republic": {
        "market_facing": [
            ("Dana Tomaskova", "Digital Services Director (O2 / Oneplay)", "", "Market-facing / digital services leadership")
        ],
        "technology": [
            ("OPEN", "Technology/spec owner", "", "Technology/spec owner")
        ]
    },
    "M7 Skylink CZ": {
        "market_facing": [
            ("Robert Beranek", "Sales Director Skylink CZ/SK", "", "Market-facing (commercial)")
        ],
        "technology": [
            ("OPEN", "Technology/onboarding owner", "", "Technology/onboarding owner")
        ]
    },
    "Cyfrowy Polsat": {
        "exec_sponsor": [
            ("Andrzej Abramczuk", "President of the Management Board (leadership listing / Reuters)", "Reuters", "Exec sponsor")
        ],
        "technology": [
            ("Jacek Felczykowski", "Management Board member responsible for network & technology", "Grupa Polsat Plus", "Technology/spec owner")
        ],
        "onboarding": [
            ("OPEN", "Onboarding owner", "", "Onboarding owner")
        ]
    },
    "CANAL+ Polska": {
        "technology": [
            ("Nicolas Cazamayou", "CTO Canal+ Poland", "Telco Magazine", "Technology/spec owner")
        ],
        "onboarding": [
            ("OPEN", "Onboarding owner", "", "Onboarding owner")
        ]
    },
    "Orange Polska": {
        "technology": [
            ("Paweł Zietek", "TV Lead Architect (referenced in vendor content)", "LinkedIn", "Technology/spec owner")
        ],
        "onboarding": [
            ("OPEN", "Onboarding owner", "", "Onboarding owner")
        ]
    },
    "Vectra": {
        "tv_service_owner": [
            ("Aleksandra Kozłowska", "VOD & TV Manager (Vectra)", "", "TV service owner (product)")
        ],
        "market_facing": [
            ("Paweł Gruszecki", "Head of Product Offerings", "", "Market-facing product (offer)")
        ],
        "technology": [
            ("OPEN", "Technology/spec owner", "", "Technology/spec owner")
        ]
    },
    "DNA": {
        "technology": [
            ("Tom Sederlöf", "Head of TV Development, DNA", "LinkedIn", "Technology/spec owner")
        ],
        "market_facing": [
            ("Mervi Rouvinen", "Business Team Lead, DNA TV", "LinkedIn", "Market-facing / business lead")
        ]
    },
    "Telia Finland": {
        "technology": [
            ("Riku Kreula", "Technical Product Manager, Telia TV services", "Sky Group", "Technology/spec owner")
        ],
        "onboarding": [
            ("OPEN", "Onboarding owner", "", "Onboarding owner")
        ]
    },
    "Elisa": {
        "market_facing": [
            ("Ani Korpela", "Chief Content Officer, Elisa Entertaining Services", "INNOVATION Magazine", "Market-facing content leader")
        ],
        "technology": [
            ("OPEN", "Technology/spec owner", "", "Technology/spec owner")
        ]
    },
    "Tele2": {
        "technology_exec": [
            ("Jacob Segerheim", "Group CTO, Tele2", "4GameChangers", "Technology exec sponsor")
        ],
        "product_design": [
            ("Mall Allpere", "Head of Product Design (TV & Streaming), Tele2", "THE ORG", "Product/design stakeholder (TV & streaming)")
        ],
        "onboarding": [
            ("OPEN", "Onboarding/spec owner", "", "Onboarding/spec owner")
        ]
    },
    "Telia Sweden": {
        "b2c_tv_business": [
            ("Linna Hafström", "Head of Telia TV & Telia Play (B2C)", "LinkedIn", "B2C TV business owner (Sweden context)")
        ]
    },
    "Telenor Norway": {
        "tv_product_platform": [
            ("Jette Overgaard", "Product Director Nordic TV (Norway)", "LinkedIn", "TV product/platform leadership")
        ],
        "product_tv_everywhere": [
            ("Sara Marazuela Reca", "Product Manager, TV Everywhere", "LinkedIn", "Product (TV everywhere)")
        ],
        "technology": [
            ("OPEN", "Needs Telenor TV platform tech director / device onboarding", "", "Technology/spec owner")
        ]
    },
    "Altibox": {
        "product_strategy": [
            ("Hans Bjarne Solheim", "Head of Content Acquisition & Product Strategy / Head of Products", "4ig.hu", "Product strategy owner")
        ],
        "technology": [
            ("OPEN", "Technology/spec owner", "", "Technology/spec owner")
        ]
    },
    "Telia Norway": {
        "country_exec": [
            ("Morten Karlsen Sørby", "Acting Head of Telia Norway (March 2025)", "Telia Company", "Country exec sponsor")
        ],
        "tv_platform_product": [
            ("Ulrika Frid", "Global Product Manager IPTV (Telia org listing)", "THE ORG", "TV platform product (IPTV) breadcrumb")
        ],
        "onboarding": [
            ("OPEN", "Needs Norway-specific TV platform owner", "", "Norway TV onboarding/spec owner")
        ]
    },
    "Eir": {
        "technology": [
            ("Declan Malone", "Head of TV & Entertainment Technology", "Reuters", "Technology/spec owner (excellent)")
        ],
        "market_facing": [
            ("Lily O'Donoghue", "Director of Broadband and TV", "Yahoo Finance", "Market-facing (broadband & TV)")
        ],
        "product_owner": [
            ("Paul Mulqueen", "Head of Product (broadband & TV proposition scope)", "Bloomberg", "Product owner (broad proposition)")
        ]
    },
    "Virgin Media Ireland": {
        "tech_product_leadership": [
            ("Eoin Hegarty", "Head of Product Management, Technology Solutions", "LinkedIn", "Tech/product leadership")
        ],
        "product_entertainment": [
            ("Frankie Liston", "Product Manager (Connectivity & Entertainment roadmap)", "Broadband TV News", "Product (entertainment roadmap)")
        ]
    },
    "Sky Ireland": {
        "commercial": [
            ("Alix Vavasseur", "Commercial Director, TV", "LinkedIn", "Commercial / partner-facing")
        ]
    }
}

def add_detailed_contacts_to_file(file_path, operator_name, contacts_dict):
    """Add detailed contacts section to specification file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build detailed contacts section
    contacts_section = "\n### Detailed Contacts by Role\n\n"
    
    # Organize by role category
    role_categories = {
        "Market-Facing / Executive": ["market_facing_exec", "exec_sponsor", "market_facing"],
        "Market-Facing / Content": ["market_facing_content", "market_facing_marketing", "market_facing_partnerships", "market_facing_entertainment", "market_facing_tv", "market_facing_product"],
        "Technology / Specifications": ["technology", "technology_product", "technology_platform", "technology_exec", "technology_stb"],
        "Onboarding / Device Certification": ["onboarding", "onboarding_platform", "onboarding_partnerships"],
        "Product Leadership": ["product_leadership", "product_stakeholder", "product_delivery", "product_experience", "product_design", "product_owner", "product_strategy", "product_tv_everywhere", "product_entertainment"],
        "TV Product / Platform": ["tv_product_leadership", "tv_product_platform", "tv_service_owner", "tv_platform_product"],
        "Other": ["program_context", "technology_program", "b2c_tv_business", "country_exec", "commercial", "tech_product_leadership"]
    }
    
    for category, keys in role_categories.items():
        category_contacts = []
        for key in keys:
            if key in contacts_dict:
                category_contacts.extend(contacts_dict[key])
        
        if category_contacts:
            contacts_section += f"#### {category}\n\n"
            for contact_tuple in category_contacts:
                if len(contact_tuple) == 4:
                    name, title, source, note = contact_tuple
                    role = note  # Use note as role description
                elif len(contact_tuple) == 5:
                    role, name, title, source, note = contact_tuple
                else:
                    continue
                
                contacts_section += f"**{role}**\n"
                if name != "OPEN" and name not in ["Accenture", "Iliad"]:
                    contacts_section += f"- **Name**: {name}\n"
                contacts_section += f"- **Title**: {title}\n"
                if source:
                    contacts_section += f"- **Source**: {source}\n"
                contacts_section += f"- **Note**: {note}\n\n"
    
    # Insert before "### Recommended Contact Points" or at end of Contact Information
    if "### Recommended Contact Points" in content:
        content = content.replace("### Recommended Contact Points", contacts_section + "### Recommended Contact Points")
    elif "### Access Process" in content:
        content = content.replace("### Access Process", contacts_section + "### Access Process")
    elif "## Next Steps" in content:
        content = content.replace("## Next Steps", contacts_section + "## Next Steps")
    else:
        # Append at end of Contact Information section
        if "## Contact Information" in content:
            start_idx = content.find("## Contact Information")
            next_section = content.find("##", start_idx + 1)
            if next_section == -1:
                content += "\n" + contacts_section
            else:
                content = content[:next_section] + contacts_section + content[next_section:]
        else:
            content += "\n" + contacts_section
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Process all specification files
base_path = Path('Europe')
spec_files = list(base_path.rglob('specifications.md'))

print(f"Found {len(spec_files)} specification files")
print("Adding detailed contacts...\n")

updated = 0

for spec_file in spec_files:
    # Extract operator name from file
    with open(spec_file, 'r', encoding='utf-8') as f:
        content = f.read()
        for line in content.split('\n'):
            if '**Operator**:' in line:
                operator = line.split('**Operator**:')[1].strip()
                # Clean operator name for matching
                operator_clean = operator.replace(' (', ' ').replace(')', '').split()[0] if operator else ""
                
                # Try to find matching contacts
                for key, value in DETAILED_CONTACTS.items():
                    if key.lower() in operator.lower() or operator_clean.lower() in key.lower():
                        add_detailed_contacts_to_file(spec_file, operator, value)
                        print(f"✅ Updated: {operator} ({key})")
                        updated += 1
                        break
                break

print(f"\n✅ Updated {updated} files with detailed contacts")

