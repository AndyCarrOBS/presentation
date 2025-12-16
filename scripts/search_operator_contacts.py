#!/usr/bin/env python3
"""
Script to search for operator contact information and update specification files.
"""
import os
import re
from pathlib import Path

# Operator contact information mapping
# This will be populated with web search results
OPERATOR_CONTACTS = {}

def extract_operator_info(file_path):
    """Extract operator name and country from specification file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    operator = None
    country = None
    
    for line in content.split('\n'):
        if '**Operator**:' in line:
            operator = line.split('**Operator**:')[1].strip()
        if '**Country**:' in line:
            country = line.split('**Country**:')[1].strip()
    
    return operator, country

def update_spec_file_with_contacts(file_path, contacts_info):
    """Update specification file with contact information."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert contact information
    # Look for "## Next Steps" or "## Notes" section
    contact_section = "\n## Contact Information\n\n"
    contact_section += "### Technical Specifications Access\n\n"
    
    if contacts_info:
        for key, value in contacts_info.items():
            if value:
                contact_section += f"- **{key}**: {value}\n"
    else:
        contact_section += "- **Status**: ⚠️ Contact information to be verified\n"
        contact_section += "- **Recommended Approach**: Contact operator's business development or technical department\n"
        contact_section += "- **Alternative**: Check operator website for developer/partner portal\n"
    
    contact_section += "\n### Recommended Contact Points\n"
    contact_section += "- Business Development Department\n"
    contact_section += "- Technical/Engineering Department\n"
    contact_section += "- Partner/Developer Relations\n"
    contact_section += "- API/Integration Support Team\n\n"
    
    # Insert before "## Next Steps" or at the end
    if "## Next Steps" in content:
        content = content.replace("## Next Steps", contact_section + "## Next Steps")
    elif "## Notes" in content:
        content = content.replace("## Notes", contact_section + "## Notes")
    else:
        content += "\n" + contact_section
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Get all specification files
base_path = Path('Europe')
spec_files = list(base_path.rglob('specifications.md'))

print(f"Found {len(spec_files)} specification files")
print("Updating with contact information template...\n")

for spec_file in spec_files:
    operator, country = extract_operator_info(spec_file)
    if operator and country:
        # For now, add template - will be populated with actual search results
        contacts = {
            "Developer Portal": "To be verified",
            "Technical Contact": "To be verified",
            "Business Development": "To be verified",
            "Email": "To be verified",
            "Website": "To be verified"
        }
        update_spec_file_with_contacts(spec_file, contacts)
        print(f"Updated: {country} - {operator}")

print(f"\nUpdated {len(spec_files)} files with contact information template.")

