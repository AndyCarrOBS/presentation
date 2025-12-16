#!/usr/bin/env python3
"""
Script to add key contacts to operator specification files.
"""
import os
from pathlib import Path

# Key contacts by operator
KEY_CONTACTS = {
    "Ziggo": {
        "contacts": [
            ("Platform / Spec Ownership (Group-Level)", "Enrique Rodriguez", "Liberty Global EVP & CTO", "libertyglobal.com", "Group-level technical specifications and platform ownership"),
            ("Operator Leadership (Top-Level Escalation)", "Stephen van Rooyen", "CEO VodafoneZiggo (effective September 2024)", "", "Top-level escalation path for formal engagement"),
            ("TV Product / Onboarding Lead", "Stephen O'Boyle", "Head of Product, TV Onboarding & Help", "LinkedIn", "Direct ownership of onboarding flows and TV product specifications"),
            ("Video Product Management", "Alex Smith", "Senior Product Manager – Video, VodafoneZiggo", "LinkedIn", "Video product specifications and technical requirements"),
        ]
    },
    "KPN": {
        "contacts": [
            ("TV & Entertainment Product Leadership / Partnerships", "Cornelis Kalma", "Director Product & Marketing, TV & Entertainment, KPN", "LinkedIn", "Involved in KPN TV+ strategy and streaming partnerships. Industry Presence: Dataxis conferences"),
            ("Corporate Exec Chain (Formal Engagement)", "Joost Farwerck", "CEO (KPN Board of Management)", "ir.kpn.com", "Formal corporate engagement route"),
        ]
    },
    "YouSee": {
        "contacts": [
            ("TV Technical Product Ownership", "Lars Bjerg", "Senior Director, Technical Product… TV & OTT", "LinkedIn", "Explicitly references TV product/development across TDC/YouSee/Wholesale"),
            ("Frontend/Platform Delivery Leadership", "Omar Esli Jimenez Villarreal", "Head of Frontend for YouSee TV", "LinkedIn", "Frontend/platform delivery and technical specifications"),
        ]
    },
    "Norlys": {
        "contacts": [
            ("TV Leadership / Product Strategy", "Jacob Vestergaard", "Director of TV at Norlys", "Broadband TV News", "TV product strategy and technical direction (quoted in industry press)"),
        ]
    },
    "Telenet": {
        "contacts": [
            ("Entertainment Product Leadership (Market-Facing Touchpoint)", "Ivor Micallef", "Director of Entertainment / Product Entertainment at Telenet", "Technology Magazine", "Market-facing touchpoint for entertainment product specifications (widely cited in interviews/partner announcements)"),
            ("Partner & VOD Relationships", "Dimme Pleysier", "Product Manager TV – Partner Relationship Management", "LinkedIn", "Partner relationship management for Telenet Digital TV, VOD focus. Useful for broadcaster/app onboarding"),
        ]
    },
    "Proximus Pickx": {
        "contacts": [
            ("Platform Transformation Reference", "Program", "Proximus Pickx 'next-gen digital TV platform' program (Accenture Video Solution)", "Accenture Newsroom", "Use as hook to identify internal platform owner/sponsor"),
            ("Partner Integration Example", "Integration", "Netflix integration on Pickx", "Proximus Group Website", "Helps route to the owning organization (operator announcement)"),
            ("Cross-Platform Expansion Context", "Program", "Pickx web app rollout with 3SS/3Ready", "3SS, Broadband TV News", "Helps triangulate internal product/engineering owners"),
        ]
    },
    "Orange France": {
        "contacts": [
            ("TV Product & Services Owner", "Guillaume Lacroix", "Director Product & Services, Orange France", "SoftAtHome", "Device/onboarding/spec direction for TV products (quoted on STB launch)"),
            ("Connected Device Program Context", "Program", "Orange STB 6 launch", "SoftAtHome", "Points to the owning TV device/platform organization"),
        ]
    },
    "Canal+ France": {
        "contacts": [
            ("Corporate Leadership (Market-Facing)", "Maxime Saada", "CEO", "Canal Plus Group", "Market-facing corporate leadership (appears on governance listing)"),
            ("Distribution Technology Leadership (Spec-Heavy Touchpoint)", "Philippe Rivas", "Distribution CTO at Canal+ Group", "Broadband TV News", "Technical specifications and distribution technology (quoted in NAGRA partnership coverage)"),
        ]
    },
    "SFR": {
        "contacts": [
            ("B2C Product Leadership", "Nicolas Leroy", "Head of B2C Product Management, SFR", "LinkedIn", "Good entry point for TV app/device onboarding routing"),
        ]
    },
    "Swisscom TV": {
        "contacts": [
            ("TV & Entertainment Technology/Spec Owner", "Peter Fregelius", "Head of TV & Entertainment Technology / Head of TV & Entertainment", "3SS, Synaptics", "TV & entertainment technology and specifications ownership (named in press materials)"),
            ("TV Development Leadership (Historic but Relevant Lineage)", "Volker Dietzel", "Head of TV Development", "Swisscom/EIDR note", "TV development and technical specifications"),
            ("Partnerships Touchpoint", "Role", "Swisscom blue Entertainment partnerships role", "Dataxis speaker bio", "Useful for streaming/app onboarding and partner relationships"),
        ]
    },
    "Sunrise": {
        "contacts": [
            ("Entertainment Leadership (Connected TV / In-Home)", "Fabrizio Campanale", "Senior Director of Entertainment and In-Home Connectivity, Sunrise", "Telco Magazine", "Connected TV and in-home entertainment specifications"),
            ("Strategy & Innovation with TV Background", "Smaranda Radoi", "Senior Director Strategy & Innovation at Sunrise", "LinkedIn", "Profile highlights TV product background, candidate for technical specifications"),
        ]
    },
    "Cyfrowy Polsat": {
        "contacts": [
            ("Top Leadership / Formal Route", "Andrzej Abramczuk", "President/CEO of Cyfrowy Polsat S.A.", "Grupa Polsat Plus", "Top-level formal engagement route (listed by the group, from July 2025)"),
            ("Technology & Network Leadership", "Jacek Felczykowski", "Management Board: Technology & Network", "Bloomberg", "Good spec ownership route, industry-profile reference"),
        ]
    },
    "CANAL+ Polska": {
        "contacts": [
            ("Technology Leadership", "Nicolas Cazamayou", "CTO Canal+ Poland", "LinkedIn", "Profile states exec committee + technology functions"),
        ]
    },
    "TIM": {
        "contacts": [
            ("OTT/Entertainment Product Ownership", "Antonio Imbimbo", "Head of Product & Experience Design", "LinkedIn", "Explicitly mentions TIMVISION + OTT partners. Onboarding + partner integration"),
            ("Service Leadership", "Giovanni Brunelli", "Head of TIMVISION", "LinkedIn", "Profile header indicates service leadership role"),
        ]
    },
}

def add_key_contacts_to_file(file_path, operator_name, contacts):
    """Add key contacts section to specification file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build key contacts section
    contacts_section = "\n### Key Contacts\n\n"
    
    for role, name, title, source, note in contacts:
        contacts_section += f"**{role}**\n"
        if name != "Program" and name != "Integration" and name != "Role":
            contacts_section += f"- **Name**: {name}\n"
        contacts_section += f"- **Title**: {title}\n"
        if source:
            contacts_section += f"- **Source**: {source}\n"
        contacts_section += f"- **Note**: {note}\n\n"
    
    # Find where to insert (after "### Technical Specifications Access" section, before "### Recommended Contact Points")
    if "### Recommended Contact Points" in content:
        content = content.replace("### Recommended Contact Points", contacts_section + "### Recommended Contact Points")
    elif "### Access Process" in content:
        content = content.replace("### Access Process", contacts_section + "### Access Process")
    elif "## Next Steps" in content:
        content = content.replace("## Next Steps", contacts_section + "## Next Steps")
    else:
        # Append at end of Contact Information section
        if "## Contact Information" in content:
            # Find end of Contact Information section
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
print("Adding key contacts...\n")

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
                for key, value in KEY_CONTACTS.items():
                    if key.lower() in operator.lower() or operator_clean.lower() in key.lower():
                        add_key_contacts_to_file(spec_file, operator, value['contacts'])
                        print(f"✅ Updated: {operator} ({key})")
                        updated += 1
                        break
                break

print(f"\n✅ Updated {updated} files with key contacts")

