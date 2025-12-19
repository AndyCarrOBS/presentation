#!/usr/bin/env python3
"""
Extract data for the European TV Markets Dashboard
"""
import os
import re
import json
from pathlib import Path

def extract_country_psb_info():
    """Extract PSB information from Country-Strategy-Summary.md"""
    psb_data = {}
    summary_file = Path('Europe/Country-Strategy-Summary.md')
    
    if not summary_file.exists():
        return psb_data
    
    with open(summary_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract country sections - split by "---" separator
    country_sections = re.split(r'\n---\n\n## ', content)[1:]
    
    for section in country_sections:
        # Extract country name - look for "## CountryName" at the start
        # The section starts with the country name after the split
        lines = section.split('\n')
        country = lines[0].strip() if lines else None
        
        # Clean up country name - remove any trailing text
        if country and '\n' in country:
            country = country.split('\n')[0].strip()
        
        if not country or len(country) > 50:  # Skip invalid country names
            continue
        
        # Extract PSB information - format: **PSB1 (OTT1)**, **PSB2 (OTT2)**
        psb_match = re.search(r'The public service broadcasters, and their OTT apps are\s+(.+?)\.', section)
        if psb_match:
            psb_text = psb_match.group(1)
            # Parse PSB entries - handle format like "**NPO (NPO Start)**, **BVN (Best of Vlaanderen en Nederland)**"
            psbs = []
            # Match **PSB Name (OTT App)**
            psb_entries = re.findall(r'\*\*([^*]+?)\s*\(([^)]+)\)\*\*', psb_text)
            for psb_name, ott_app in psb_entries:
                psbs.append({
                    'name': psb_name.strip(),
                    'ott_app': ott_app.strip()
                })
            if psbs:
                psb_data[country] = psbs
    
    return psb_data

def extract_specification_info():
    """Extract specification information from all specifications.md files"""
    spec_data = {}
    base_dir = Path('Europe')
    
    for spec_file in base_dir.rglob('specifications.md'):
        # Extract country and operator from path
        parts = spec_file.parts
        if 'Europe' not in parts:
            continue
        
        europe_idx = parts.index('Europe')
        if europe_idx + 1 >= len(parts):
            continue
        
        country = parts[europe_idx + 1]
        operator = parts[-2] if len(parts) > europe_idx + 2 else None
        
        if not operator:
            continue
        
        # Clean up names
        country = country.replace('-', ' ').title()
        operator = operator.replace('-', ' ').replace('_', ' ')
        
        with open(spec_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract HbbTV version
        hbbtv_match = re.search(r'HbbTV.*?Version[:\s]+([0-9.]+)', content, re.IGNORECASE)
        hbbtv_version = hbbtv_match.group(1) if hbbtv_match else None
        
        # Extract CI+ version
        ci_match = re.search(r'CI\+.*?Version[:\s]+([0-9.]+)', content, re.IGNORECASE)
        ci_version = ci_match.group(1) if ci_match else None
        
        # Check if specifications are available
        has_spec = '✅' in content or 'PARTIALLY VERIFIED' in content or 'VERIFIED' in content
        
        # Check for test material, gated process, whitelist, branding
        has_test_material = 'test material' in content.lower() or 'test' in content.lower()
        has_gated_process = 'gated' in content.lower() or 'partnership' in content.lower() or 'nda' in content.lower()
        has_whitelist = 'whitelist' in content.lower() or 'white list' in content.lower()
        has_branding = 'branding' in content.lower() or 'brand' in content.lower()
        
        if country not in spec_data:
            spec_data[country] = {}
        
        spec_data[country][operator] = {
            'hbbtv_version': hbbtv_version,
            'ci_version': ci_version,
            'has_specification': has_spec,
            'has_test_material': has_test_material,
            'has_gated_process': has_gated_process,
            'has_whitelist': has_whitelist,
            'has_branding_agreement': has_branding,
            'spec_file_path': str(spec_file)
        }
    
    return spec_data

def extract_operator_contacts():
    """Extract key contacts from Operator-Key-Contacts.md"""
    contacts_data = {}
    contacts_file = Path('Europe/Operator-Key-Contacts.md')
    
    if not contacts_file.exists():
        return contacts_data
    
    with open(contacts_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract by country sections
    country_sections = re.split(r'\n## ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\n', content)[1:]
    
    for i in range(0, len(country_sections), 2):
        if i + 1 >= len(country_sections):
            break
        
        country = country_sections[i].strip()
        section_content = country_sections[i + 1]
        
        # Extract operator sections
        operator_sections = re.split(r'\n### ([^\n]+)\n', section_content)[1:]
        
        for j in range(0, len(operator_sections), 2):
            if j + 1 >= len(operator_sections):
                break
            
            operator = operator_sections[j].strip()
            operator_content = operator_sections[j + 1]
            
            # Extract contacts
            contacts = []
            name_matches = re.finditer(r'\*\*Name\*\*:\s*([^\n]+)', operator_content)
            
            for match in name_matches:
                name = match.group(1).strip()
                if name == 'OPEN' or not name:
                    continue
                
                # Extract title
                title_match = re.search(r'\*\*Title\*\*:\s*([^\n]+)', operator_content[match.end():])
                title = title_match.group(1).strip() if title_match else ''
                
                # Extract email
                email_match = re.search(r'\*\*Email\*\*:\s*([^\n]+)', operator_content[match.end():])
                email = email_match.group(1).strip() if email_match else ''
                email = re.sub(r'\s*\(predicted\)', '', email, flags=re.IGNORECASE)
                
                # Extract phone
                phone_match = re.search(r'\*\*Phone\*\*:\s*([^\n]+)', operator_content[match.end():])
                phone = phone_match.group(1).strip() if phone_match else ''
                
                contacts.append({
                    'name': name,
                    'title': title,
                    'email': email,
                    'phone': phone
                })
            
            if country not in contacts_data:
                contacts_data[country] = {}
            
            contacts_data[country][operator] = contacts
    
    return contacts_data

def extract_free_to_air_info():
    """Extract free-to-air market information"""
    fta_data = {}
    base_dir = Path('Europe')
    
    for fta_file in base_dir.rglob('free-to-air-market.md'):
        parts = fta_file.parts
        if 'Europe' not in parts:
            continue
        
        europe_idx = parts.index('Europe')
        if europe_idx + 1 >= len(parts):
            continue
        
        country = parts[europe_idx + 1].replace('-', ' ').title()
        
        with open(fta_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract HbbTV info
        hbbtv_info = {}
        hbbtv_match = re.search(r'HbbTV[:\s]+([0-9.]+)', content, re.IGNORECASE)
        if hbbtv_match:
            hbbtv_info['version'] = hbbtv_match.group(1)
        
        # Extract CI+ info
        ci_info = {}
        ci_match = re.search(r'CI\+[:\s]+([0-9.]+)', content, re.IGNORECASE)
        if ci_match:
            ci_info['version'] = ci_match.group(1)
        
        fta_data[country] = {
            'hbbtv': hbbtv_info,
            'ci_plus': ci_info,
            'has_specification': '✅' in content or 'specification' in content.lower()
        }
    
    return fta_data

def main():
    """Main function to extract all dashboard data"""
    print("Extracting dashboard data...")
    
    # Extract all data
    psb_data = extract_country_psb_info()
    spec_data = extract_specification_info()
    contacts_data = extract_operator_contacts()
    fta_data = extract_free_to_air_info()
    
    # Combine into dashboard data structure
    dashboard_data = {
        'countries': {},
        'operators': spec_data,
        'contacts': contacts_data,
        'free_to_air': fta_data,
        'psb': psb_data
    }
    
    # Get all countries
    all_countries = set()
    all_countries.update(psb_data.keys())
    all_countries.update(spec_data.keys())
    all_countries.update(contacts_data.keys())
    all_countries.update(fta_data.keys())
    
    # Build country data
    for country in sorted(all_countries):
        dashboard_data['countries'][country] = {
            'psb': psb_data.get(country, []),
            'operators': list(spec_data.get(country, {}).keys()),
            'free_to_air': fta_data.get(country, {})
        }
    
    # Write to JSON file
    output_file = Path('dashboard_data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Dashboard data extracted to {output_file}")
    print(f"   Countries: {len(dashboard_data['countries'])}")
    print(f"   Operators: {sum(len(ops) for ops in spec_data.values())}")
    print(f"   Contacts: {sum(len(contacts) for ops in contacts_data.values() for contacts in ops.values())}")
    
    return dashboard_data

if __name__ == '__main__':
    main()

