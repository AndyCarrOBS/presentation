#!/usr/bin/env python3
"""
Script to update operator specification files with contact information.
"""
import os
import re
from pathlib import Path

# Operator contact information (compiled from web searches and known sources)
OPERATOR_CONTACTS = {
    # Netherlands
    "Ziggo": {
        "website": "https://www.ziggo.nl/",
        "parent_company": "Liberty Global",
        "contact_note": "Contact via Liberty Global partner program or Ziggo business development",
        "developer_portal": "Check Liberty Global developer resources",
    },
    "KPN": {
        "website": "https://www.kpn.com/",
        "contact_note": "Contact KPN business development or technical department",
        "developer_portal": "Check KPN partner/developer portal",
    },
    "M7 Canal Digitaal": {
        "website": "https://www.canaldigitaal.nl/",
        "parent_company": "M7 Group (Canal+)",
        "contact_note": "Contact M7 Group or Canal+ Luxembourg for technical specifications",
        "m7_group_contact": "info@m7group.eu",
        "m7_group_website": "https://www.m7group.eu/",
    },
    
    # Denmark
    "YouSee": {
        "website": "https://www.yousee.dk/",
        "parent_company": "TDC Group",
        "contact_note": "Contact TDC Group business development",
    },
    "Stofa": {
        "website": "https://www.stofa.dk/",
        "contact_note": "Contact Stofa business development or technical department",
    },
    "Allente": {
        "website": "https://www.allente.com/",
        "contact_note": "Contact Allente business development (Nordic-wide platform)",
        "developer_portal": "Check Allente partner program",
    },
    "Boxer HD": {
        "website": "https://www.boxer.dk/",
        "contact_note": "Contact Boxer HD business development",
    },
    
    # Belgium
    "Telenet": {
        "website": "https://www.telenet.be/",
        "contact_note": "Contact Telenet business development or partner program",
        "developer_portal": "Check Telenet partner portal",
    },
    "Proximus Pickx": {
        "website": "https://www.proximus.be/",
        "contact_note": "Contact Proximus business development or technical department",
        "developer_portal": "Check Proximus developer/partner portal",
    },
    "Voo": {
        "website": "https://www.voo.be/",
        "contact_note": "Contact Voo business development",
    },
    "M7 Telesat": {
        "website": "https://www.telesat.be/",
        "parent_company": "M7 Group (Canal+)",
        "contact_note": "Contact M7 Group or Canal+ Luxembourg for technical specifications",
        "m7_group_contact": "info@m7group.eu",
        "m7_group_website": "https://www.m7group.eu/",
    },
    
    # France
    "Orange France": {
        "website": "https://www.orange.fr/",
        "contact_note": "Contact Orange business development or Orange Partner program",
        "developer_portal": "Orange Partner portal available",
    },
    "Free France": {
        "website": "https://www.free.fr/",
        "parent_company": "Iliad",
        "contact_note": "Contact Free/Iliad business development",
    },
    "Canal+ France": {
        "website": "https://www.canalplus.com/",
        "contact_note": "Contact Canal+ business development or partner program",
        "developer_portal": "Check Canal+ partner portal",
    },
    "Fransat": {
        "website": "https://www.fransat.fr/",
        "contact_note": "Contact Fransat business development",
    },
    
    # Austria
    "Magenta TV": {
        "website": "https://www.magenta.at/",
        "parent_company": "Deutsche Telekom",
        "contact_note": "Contact Deutsche Telekom partner program or Magenta business development",
        "developer_portal": "Check Deutsche Telekom developer resources",
    },
    "M7 HD Austria": {
        "website": "https://www.hdaustria.at/",
        "parent_company": "M7 Group (Canal+)",
        "contact_note": "Contact M7 Group or Canal+ Luxembourg for technical specifications",
        "m7_group_contact": "info@m7group.eu",
        "m7_group_website": "https://www.m7group.eu/",
    },
    "SimpliTV": {
        "website": "https://www.simpli.tv/",
        "contact_note": "Contact SimpliTV business development",
    },
    "ORF": {
        "website": "https://www.orf.at/",
        "contact_note": "Contact ORF technical department or business development",
        "email": "dagmar.huebner-alber@orf.at",
        "phone": "+43 1 87878 14174",
    },
    
    # Switzerland
    "Swisscom TV": {
        "website": "https://www.swisscom.ch/",
        "contact_note": "Contact Swisscom business development or partner program",
        "developer_portal": "Check Swisscom partner portal",
    },
    "UPC Switzerland": {
        "website": "https://www.upc.ch/",
        "parent_company": "Liberty Global",
        "contact_note": "Contact via Liberty Global partner program",
    },
    "Sunrise": {
        "website": "https://www.sunrise.ch/",
        "contact_note": "Contact Sunrise business development",
    },
    "Zattoo": {
        "website": "https://www.zattoo.com/",
        "contact_note": "Contact Zattoo business development or partner program",
        "developer_portal": "Check Zattoo partner/developer portal",
    },
    
    # Luxembourg
    "M7 Telesat": {
        "website": "https://www.telesat.lu/",
        "parent_company": "M7 Group (Canal+)",
        "contact_note": "Contact M7 Group or Canal+ Luxembourg for technical specifications",
        "m7_group_contact": "info@m7group.eu",
        "m7_group_website": "https://www.m7group.eu/",
    },
    
    # Italy
    "Sky Italia": {
        "website": "https://www.sky.it/",
        "parent_company": "Sky Group (Comcast)",
        "contact_note": "Contact Sky Italia business development or Sky Partner program",
        "developer_portal": "Check Sky Partner portal",
    },
    "Mediaset": {
        "website": "https://www.mediaset.it/",
        "contact_note": "Contact Mediaset business development",
    },
    "TIM": {
        "website": "https://www.tim.it/",
        "contact_note": "Contact TIM business development or TIM Partner program",
        "developer_portal": "Check TIM partner portal",
    },
    "Tivusat - LaTivu": {
        "website": "https://www.tivusat.it/",
        "contact_note": "Contact Tivusat business development",
    },
    
    # Czech Republic
    "T-Mobile Czech Republic": {
        "website": "https://www.t-mobile.cz/",
        "parent_company": "Deutsche Telekom",
        "contact_note": "Contact Deutsche Telekom partner program or T-Mobile Czech business development",
    },
    "Vodafone Czech Republic": {
        "website": "https://www.vodafone.cz/",
        "parent_company": "Vodafone Group",
        "contact_note": "Contact Vodafone Group partner program or Vodafone Czech business development",
    },
    "O2 Czech Republic": {
        "website": "https://www.o2.cz/",
        "contact_note": "Contact O2 Czech business development or partner program",
    },
    "M7 Skylink CZ": {
        "website": "https://www.skylink.cz/",
        "parent_company": "M7 Group (Canal+)",
        "contact_note": "Contact M7 Group or Canal+ Luxembourg for technical specifications",
        "m7_group_contact": "info@m7group.eu",
        "m7_group_website": "https://www.m7group.eu/",
        "customer_service": "+420 595 694 310",
        "email": "info@skylink.cz",
    },
    
    # Poland
    "Cyfrowy Polsat": {
        "website": "https://www.polsatbox.pl/",
        "contact_note": "Contact Cyfrowy Polsat business development or partner program",
    },
    "CANAL+ Polska": {
        "website": "https://www.canalplus.pl/",
        "parent_company": "Canal+ Group",
        "contact_note": "Contact Canal+ Group partner program or CANAL+ Polska business development",
    },
    "Orange Polska": {
        "website": "https://www.orange.pl/",
        "parent_company": "Orange Group",
        "contact_note": "Contact Orange Group partner program or Orange Polska business development",
    },
    "Vectra": {
        "website": "https://www.vectra.pl/",
        "contact_note": "Contact Vectra business development",
    },
    
    # Hungary
    "UPC": {
        "website": "https://www.upc.hu/",
        "parent_company": "Vodafone",
        "contact_note": "Contact Vodafone Group partner program or UPC Hungary business development",
    },
    "M7 UPC Direct": {
        "website": "https://www.directone.hu/",
        "parent_company": "M7 Group (Canal+)",
        "contact_note": "Contact M7 Group or Canal+ Luxembourg for technical specifications",
        "m7_group_contact": "info@m7group.eu",
        "m7_group_website": "https://www.m7group.eu/",
        "customer_service": "+36 1 336 6000",
        "email": "info@directone.hu",
    },
    
    # Romania
    "DigiTV": {
        "website": "https://www.digi.ro/",
        "parent_company": "4iG (acquired from RCS&RDS)",
        "contact_note": "Contact 4iG or DigiTV business development (specifications may have changed after acquisition)",
        "customer_service": "+40 31 400 4000",
        "email": "relatii.clienti@rcs-rds.ro",
    },
    
    # Slovakia
    "M7 Skylink SK": {
        "website": "https://www.skylink.sk/",
        "parent_company": "M7 Group (Canal+)",
        "contact_note": "Contact M7 Group or Canal+ Luxembourg for technical specifications",
        "m7_group_contact": "info@m7group.eu",
        "m7_group_website": "https://www.m7group.eu/",
        "customer_service": "+421 2 20 250 241",
        "email": "info@skylink.sk",
    },
    
    # Finland
    "Elisa": {
        "website": "https://www.elisa.fi/",
        "contact_note": "Contact Elisa business development or partner program",
    },
    "Telia Finland": {
        "website": "https://www.telia.fi/",
        "parent_company": "Telia Company",
        "contact_note": "Contact Telia Company partner program or Telia Finland business development",
    },
    "Allente": {
        "website": "https://www.allente.com/",
        "contact_note": "Contact Allente business development (Nordic-wide platform)",
    },
    
    # Sweden
    "Tele2": {
        "website": "https://www.tele2.se/",
        "contact_note": "Contact Tele2 business development or partner program",
    },
    "Telenor": {
        "website": "https://www.telenor.se/",
        "parent_company": "Telenor Group",
        "contact_note": "Contact Telenor Group partner program or Telenor Sweden business development",
    },
    "Boxer HD": {
        "website": "https://www.boxer.se/",
        "contact_note": "Contact Boxer HD business development",
    },
    
    # Norway
    "Telenor Norway": {
        "website": "https://www.telenor.no/",
        "parent_company": "Telenor Group",
        "contact_note": "Contact Telenor Group partner program or Telenor Norway business development",
    },
    "Telia Norway": {
        "website": "https://www.telia.no/",
        "parent_company": "Telia Company",
        "contact_note": "Contact Telia Company partner program or Telia Norway business development",
    },
    "Altibox": {
        "website": "https://www.altibox.no/",
        "contact_note": "Contact Altibox business development",
    },
    
    # Ireland
    "Sky Ireland": {
        "website": "https://www.sky.ie/",
        "parent_company": "Sky Group (Comcast)",
        "contact_note": "Contact Sky Ireland business development or Sky Partner program",
        "developer_portal": "Check Sky Partner portal",
    },
    "Virgin Media Ireland": {
        "website": "https://www.virginmedia.ie/",
        "parent_company": "Liberty Global",
        "contact_note": "Contact via Liberty Global partner program or Virgin Media Ireland business development",
    },
    "Eir": {
        "website": "https://www.eir.ie/",
        "contact_note": "Contact Eir business development",
    },
    "Saorview": {
        "website": "https://www.saorview.ie/",
        "contact_note": "Contact Saorview technical department (public service broadcaster)",
    },
}

def extract_operator_name(file_path):
    """Extract operator name from specification file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for line in content.split('\n'):
        if '**Operator**:' in line:
            operator = line.split('**Operator**:')[1].strip()
            return operator
    
    return None

def find_matching_contact(operator_name):
    """Find matching contact information for operator."""
    # Try exact match first
    if operator_name in OPERATOR_CONTACTS:
        return OPERATOR_CONTACTS[operator_name]
    
    # Try partial matches
    for key, value in OPERATOR_CONTACTS.items():
        if key.lower() in operator_name.lower() or operator_name.lower() in key.lower():
            return value
    
    return None

def update_spec_file_with_contacts(file_path, contacts_info):
    """Update specification file with contact information."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build contact section
    contact_section = "\n## Contact Information\n\n"
    contact_section += "### Technical Specifications Access\n\n"
    
    if contacts_info:
        if contacts_info.get("website"):
            contact_section += f"- **Website**: {contacts_info['website']}\n"
        
        if contacts_info.get("email"):
            contact_section += f"- **Email**: {contacts_info['email']}\n"
        
        if contacts_info.get("customer_service"):
            contact_section += f"- **Customer Service**: {contacts_info['customer_service']}\n"
        
        if contacts_info.get("phone"):
            contact_section += f"- **Phone**: {contacts_info['phone']}\n"
        
        if contacts_info.get("parent_company"):
            contact_section += f"- **Parent Company**: {contacts_info['parent_company']}\n"
        
        if contacts_info.get("developer_portal"):
            contact_section += f"- **Developer Portal**: {contacts_info['developer_portal']}\n"
        
        if contacts_info.get("m7_group_contact"):
            contact_section += f"- **M7 Group Contact**: {contacts_info['m7_group_contact']}\n"
            contact_section += f"- **M7 Group Website**: {contacts_info.get('m7_group_website', 'N/A')}\n"
        
        if contacts_info.get("contact_note"):
            contact_section += f"\n**Note**: {contacts_info['contact_note']}\n"
    else:
        contact_section += "- **Status**: ⚠️ Contact information to be verified\n"
        contact_section += "- **Recommended Approach**: Contact operator's business development or technical department\n"
        contact_section += "- **Alternative**: Check operator website for developer/partner portal\n"
    
    contact_section += "\n### Recommended Contact Points\n"
    contact_section += "- **Business Development Department**: For partnership and integration discussions\n"
    contact_section += "- **Technical/Engineering Department**: For technical specifications and API access\n"
    contact_section += "- **Partner/Developer Relations**: For developer portal access and documentation\n"
    contact_section += "- **API/Integration Support Team**: For technical integration support\n\n"
    
    contact_section += "### Access Process\n"
    contact_section += "1. Visit operator website and look for 'Partner', 'Developer', or 'Business' sections\n"
    contact_section += "2. Contact business development department via website contact form or email\n"
    contact_section += "3. Request access to technical specifications and developer documentation\n"
    contact_section += "4. May require partnership agreement or NDA for detailed specifications\n"
    contact_section += "5. For M7 Group operators, contact M7 Group directly for unified platform specifications\n\n"
    
    # Insert before "## Next Steps" or at the end before "## Notes"
    if "## Next Steps" in content:
        content = content.replace("## Next Steps", contact_section + "## Next Steps")
    elif "## Notes" in content:
        content = content.replace("## Notes", contact_section + "## Notes")
    else:
        # Find last section and append
        if "## Findings" in content:
            content = content.replace("## Findings", "## Findings" + contact_section)
        else:
            content += "\n" + contact_section
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Process all specification files
base_path = Path('Europe')
spec_files = list(base_path.rglob('specifications.md'))

print(f"Found {len(spec_files)} specification files")
print("Updating with contact information...\n")

updated = 0
not_found = []

for spec_file in spec_files:
    operator = extract_operator_name(spec_file)
    if operator:
        contacts = find_matching_contact(operator)
        update_spec_file_with_contacts(spec_file, contacts)
        if contacts:
            updated += 1
            print(f"✅ Updated: {operator}")
        else:
            not_found.append(operator)
            print(f"⚠️  No contacts found: {operator}")

print(f"\n✅ Updated {updated} files with contact information")
if not_found:
    print(f"⚠️  {len(not_found)} operators without contact information:")
    for op in not_found:
        print(f"   - {op}")

