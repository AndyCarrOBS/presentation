#!/usr/bin/env python3
"""
Comprehensive data extraction for the European TV Markets Dashboard
Extracts data from all available sources in the Europe directory structure
"""
import os
import re
import json
from pathlib import Path

def normalize_operator_name(name):
    """Normalize operator name for matching"""
    if not name:
        return ""
    # Remove extra text in parentheses
    name = re.sub(r'\s*\([^)]+\)', '', name)
    # Remove special characters, convert to lowercase
    normalized = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
    return normalized

def find_operator_match(contact_op_name, operator_names):
    """Find matching operator name from list"""
    contact_normalized = normalize_operator_name(contact_op_name)
    
    # Try exact match first
    for op_name in operator_names:
        if normalize_operator_name(op_name) == contact_normalized:
            return op_name
    
    # Try partial match
    for op_name in operator_names:
        op_normalized = normalize_operator_name(op_name)
        if contact_normalized in op_normalized or op_normalized in contact_normalized:
            return op_name
    
    # Try fuzzy match (check if key parts match)
    contact_parts = contact_normalized.split()
    for op_name in operator_names:
        op_normalized = normalize_operator_name(op_name)
        op_parts = op_normalized.split()
        # Check if significant parts match
        if len(contact_parts) > 0 and len(op_parts) > 0:
            if contact_parts[0] == op_parts[0] or (len(contact_parts) > 1 and contact_parts[0] in op_parts):
                return op_name
    
    return None

def link_contacts_to_operators(operators_data, contacts_data):
    """Link contacts to operators by normalizing names"""
    linked_contacts = {}
    
    for country in contacts_data.keys():
        if country not in linked_contacts:
            linked_contacts[country] = {}
        
        country_contacts = contacts_data[country]
        country_operators = operators_data.get(country, {})
        operator_names = list(country_operators.keys())
        
        # Iterate through contact data keys (these are the operator names from contacts file)
        for contact_op_name, contact_data in country_contacts.items():
            # Find matching operator from the operators list
            matched_op = find_operator_match(contact_op_name, operator_names)
            
            if matched_op:
                # Flatten contacts if they're organized by role
                if isinstance(contact_data, dict):
                    # Extract all contacts from all roles
                    all_contacts = []
                    for role, role_contacts in contact_data.items():
                        if isinstance(role_contacts, list):
                            all_contacts.extend(role_contacts)
                        elif isinstance(role_contacts, dict):
                            # Handle nested structure
                            all_contacts.extend(role_contacts.values())
                    linked_contacts[country][matched_op] = all_contacts
                elif isinstance(contact_data, list):
                    linked_contacts[country][matched_op] = contact_data
    
    return linked_contacts

def extract_country_strategy_info():
    """Extract comprehensive country and operator information from Country-Strategy-Summary.md"""
    country_data = {}
    summary_file = Path('Europe/Country-Strategy-Summary.md')
    
    if not summary_file.exists():
        return country_data
    
    with open(summary_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract country sections
    country_sections = re.split(r'\n---\n\n## ', content)[1:]
    
    for section in country_sections:
        lines = section.split('\n')
        country = lines[0].strip() if lines else None
        
        if not country or len(country) > 50:
            continue
        
        # Extract population
        pop_match = re.search(r'population is\s+\*\*([0-9.]+)\s+million\*\*', section)
        population = pop_match.group(1) if pop_match else None
        
        # Extract TV homes
        tvhomes_match = re.search(r'with\s+\*\*([0-9.]+)\s+million\s+TV\s+homes\*\*', section)
        tv_homes = tvhomes_match.group(1) if tvhomes_match else None
        
        # Extract PSB information
        psbs = []
        psb_match = re.search(r'The public service broadcasters, and their OTT apps are\s+(.+?)\.', section)
        if psb_match:
            psb_text = psb_match.group(1)
            psb_entries = re.findall(r'\*\*([^*]+?)\s*\(([^)]+)\)\*\*', psb_text)
            for psb_name, ott_app in psb_entries:
                psbs.append({
                    'name': psb_name.strip(),
                    'ott_app': ott_app.strip()
                })
        
        # Extract retail partners
        retail_match = re.search(r'In\s+\*\*' + re.escape(country) + r'\*\*\s+these retail partners are where TV\'s are purchased\s+(.+?)\.', section)
        retail_partners = []
        if retail_match:
            retail_text = retail_match.group(1)
            # Extract bolded retailer names
            retailers = re.findall(r'\*\*([^*]+)\*\*', retail_text)
            retail_partners = [r.strip() for r in retailers]
        
        # Extract operators with detailed information
        operators = {}
        operator_blocks = re.finditer(r'\*\*([^*]+?)\*\*\nThis operator uses\s+\*\*([^*]+?)\*\*', section)
        
        for match in operator_blocks:
            op_name = match.group(1).strip()
            tech_keywords = match.group(2).strip()
            
            # Extract subscriber numbers or market share
            sub_match = re.search(rf'\*\*{re.escape(op_name)}\*\*.*?\(([^)]+)\)', section)
            subscribers = sub_match.group(1).strip() if sub_match else None
            
            # Extract Roku engagement
            roku_match = re.search(rf'\*\*{re.escape(op_name)}\*\*.*?is\s+\*\*(\w+)\*\*\s+to engage with Roku', section)
            roku_engagement = roku_match.group(1).lower() if roku_match else None
            
            # Extract Amazon Fire TV status
            firetv_match = re.search(rf'\*\*{re.escape(op_name)}\*\*.*?Amazon Fire TV is\s+\*\*(\w+)\*\*', section)
            firetv_active = firetv_match.group(1).lower() == 'active' if firetv_match else None
            
            # Extract specification availability
            spec_match = re.search(rf'\*\*{re.escape(op_name)}\*\*.*?Technical specifications are\s+\*\*(\w+)\*\*', section)
            spec_available = spec_match.group(1).lower() == 'available' if spec_match else None
            
            operators[op_name] = {
                'technical_keywords': tech_keywords,
                'subscribers': subscribers,
                'roku_engagement': roku_engagement,
                'amazon_fire_tv': firetv_active,
                'specification_available': spec_available
            }
        
        country_data[country] = {
            'population_million': population,
            'tv_homes_million': tv_homes,
            'psb': psbs,
            'retail_partners': retail_partners,
            'operators': operators
        }
    
    return country_data

def extract_specification_info_comprehensive():
    """Extract comprehensive specification information from all specifications.md files"""
    spec_data = {}
    base_dir = Path('Europe')
    
    for spec_file in base_dir.rglob('specifications.md'):
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
        
        country = country.replace('-', ' ').title()
        operator = operator.replace('-', ' ').replace('_', ' ')
        
        with open(spec_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract HbbTV version - look for various patterns
        hbbtv_match = re.search(r'HbbTV.*?Version[:\s]+([0-9.]+)', content, re.IGNORECASE)
        if not hbbtv_match:
            hbbtv_match = re.search(r'HbbTV\s+([0-9.]+)', content, re.IGNORECASE)
        if not hbbtv_match:
            hbbtv_match = re.search(r'HbbTV\s+2\.0\.4|HbbTV\s+2\.0\.3|HbbTV\s+1\.5', content, re.IGNORECASE)
            if hbbtv_match:
                version_match = re.search(r'([0-9.]+)', hbbtv_match.group(0))
                hbbtv_version = version_match.group(1) if version_match else None
            else:
                hbbtv_version = None
        else:
            hbbtv_version = hbbtv_match.group(1)
        
        # Extract CI+ version - look for various patterns
        ci_match = re.search(r'CI\+.*?Version[:\s]+([0-9.]+)', content, re.IGNORECASE)
        if not ci_match:
            ci_match = re.search(r'CI\+\s+([0-9.]+)', content, re.IGNORECASE)
        ci_version = ci_match.group(1) if ci_match else None
        
        # Extract CAS systems
        cas_systems = []
        cas_patterns = [
            (r'Nagravision', 'Nagravision'),
            (r'Irdeto', 'Irdeto'),
            (r'Conax', 'Conax'),
            (r'Viaccess', 'Viaccess'),
            (r'Videoguard|NDS', 'Videoguard/NDS')
        ]
        for pattern, name in cas_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                cas_systems.append(name)
        
        # Check specification availability
        has_spec = '✅' in content or 'PARTIALLY VERIFIED' in content or 'VERIFIED' in content
        
        # Check for test material, gated process, whitelist, branding
        has_test_material = 'test material' in content.lower() or 'test' in content.lower()
        has_gated_process = 'gated' in content.lower() or 'partnership' in content.lower() or 'nda' in content.lower()
        has_whitelist = 'whitelist' in content.lower() or 'white list' in content.lower()
        has_branding = 'branding' in content.lower() or 'brand' in content.lower()
        
        # Extract developer portal
        dev_portal_match = re.search(r'Developer Portal[:\s]+([^\n]+)', content, re.IGNORECASE)
        developer_portal = dev_portal_match.group(1).strip() if dev_portal_match else None
        
        # Extract operator website - look for URL patterns or website field
        website_match = re.search(r'Website[:\s]+(https?://[^\s\n]+|www\.[^\s\n]+)', content, re.IGNORECASE)
        if not website_match:
            website_match = re.search(r'\*\*Website\*\*:\s*(https?://[^\s\n]+|www\.[^\s\n]+)', content, re.IGNORECASE)
        website = website_match.group(1).strip() if website_match else None
        
        # Extract parent company - look for Parent Company field
        parent_match = re.search(r'Parent Company[:\s]+([^\n]+?)(?:\n|$)', content, re.IGNORECASE)
        if not parent_match:
            parent_match = re.search(r'\*\*Parent Company\*\*:\s*([^\n]+?)(?:\n|$)', content, re.IGNORECASE)
        parent_company = parent_match.group(1).strip() if parent_match else None
        # Clean up parent company (remove markdown, extra text)
        if parent_company:
            parent_company = re.sub(r'^\*\*|\*\*$', '', parent_company)
            parent_company = re.sub(r'^-\s*\*\*|\*\*$', '', parent_company)
            if len(parent_company) > 100:  # Likely extracted too much
                parent_company = None
        
        # Extract access methods
        access_methods = []
        if 'public' in content.lower() and 'documentation' in content.lower():
            access_methods.append('public')
        if 'nda' in content.lower():
            access_methods.append('nda')
        if 'partnership' in content.lower():
            access_methods.append('partnership')
        
        if country not in spec_data:
            spec_data[country] = {}
        
        spec_data[country][operator] = {
            'hbbtv_version': hbbtv_version,
            'ci_version': ci_version,
            'cas_systems': cas_systems,
            'has_specification': has_spec,
            'has_test_material': has_test_material,
            'has_gated_process': has_gated_process,
            'has_whitelist': has_whitelist,
            'has_branding_agreement': has_branding,
            'developer_portal': developer_portal,
            'website': website,
            'parent_company': parent_company,
            'access_methods': access_methods,
            'spec_file_path': str(spec_file)
        }
    
    return spec_data

def extract_operator_contacts_comprehensive():
    """Extract comprehensive contact information from Operator-Key-Contacts.md"""
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
            
            # Extract contacts by role
            contacts_by_role = {}
            
            # Look for role sections
            role_sections = re.split(r'\n#### ([^\n]+)\n', operator_content)[1:]
            
            for k in range(0, len(role_sections), 2):
                if k + 1 >= len(role_sections):
                    break
                
                role = role_sections[k].strip()
                role_content = role_sections[k + 1]
                
                contacts = []
                # Extract individual contacts in this role
                name_matches = re.finditer(r'\*\*Name\*\*:\s*([^\n]+)', role_content)
                
                for match in name_matches:
                    name = match.group(1).strip()
                    if name == 'OPEN' or not name:
                        continue
                    
                    # Extract title
                    title_match = re.search(r'\*\*Title\*\*:\s*([^\n]+)', role_content[match.end():])
                    title = title_match.group(1).strip() if title_match else ''
                    
                    # Extract email
                    email_match = re.search(r'\*\*Email\*\*:\s*([^\n]+)', role_content[match.end():])
                    email = email_match.group(1).strip() if email_match else ''
                    email = re.sub(r'\s*\(predicted\)', '', email, flags=re.IGNORECASE)
                    
                    # Extract phone
                    phone_match = re.search(r'\*\*Phone\*\*:\s*([^\n]+)', role_content[match.end():])
                    phone = phone_match.group(1).strip() if phone_match else ''
                    
                    # Extract source
                    source_match = re.search(r'\*\*Source\*\*:\s*([^\n]+)', role_content[match.end():])
                    source = source_match.group(1).strip() if source_match else ''
                    
                    # Extract note
                    note_match = re.search(r'\*\*Note\*\*:\s*([^\n]+)', role_content[match.end():])
                    note = note_match.group(1).strip() if note_match else ''
                    
                    contacts.append({
                        'name': name,
                        'title': title,
                        'email': email,
                        'phone': phone,
                        'source': source,
                        'note': note
                    })
                
                if contacts:
                    contacts_by_role[role] = contacts
            
            # Also extract contacts from "Key Contacts" section (legacy format)
            if not contacts_by_role:
                name_matches = re.finditer(r'\*\*Name\*\*:\s*([^\n]+)', operator_content)
                all_contacts = []
                
                for match in name_matches:
                    name = match.group(1).strip()
                    if name == 'OPEN' or not name:
                        continue
                    
                    title_match = re.search(r'\*\*Title\*\*:\s*([^\n]+)', operator_content[match.end():])
                    title = title_match.group(1).strip() if title_match else ''
                    
                    email_match = re.search(r'\*\*Email\*\*:\s*([^\n]+)', operator_content[match.end():])
                    email = email_match.group(1).strip() if email_match else ''
                    email = re.sub(r'\s*\(predicted\)', '', email, flags=re.IGNORECASE)
                    
                    phone_match = re.search(r'\*\*Phone\*\*:\s*([^\n]+)', operator_content[match.end():])
                    phone = phone_match.group(1).strip() if phone_match else ''
                    
                    all_contacts.append({
                        'name': name,
                        'title': title,
                        'email': email,
                        'phone': phone
                    })
                
                if all_contacts:
                    contacts_by_role['Key Contacts'] = all_contacts
            
            if contacts_by_role:
                if country not in contacts_data:
                    contacts_data[country] = {}
                contacts_data[country][operator] = contacts_by_role
    
    return contacts_data

def extract_free_to_air_info_comprehensive():
    """Extract comprehensive free-to-air market information"""
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
        
        # Extract platform breakdown
        platforms = {}
        if 'DTT' in content or 'DVB-T' in content:
            platforms['dtt'] = True
        if 'cable' in content.lower():
            platforms['cable'] = True
        if 'satellite' in content.lower():
            platforms['satellite'] = True
        if 'IPTV' in content or 'OTT' in content:
            platforms['iptv_ott'] = True
        
        # Extract coverage information
        coverage_match = re.search(r'Coverage[:\s]+([^\n]+)', content, re.IGNORECASE)
        coverage = coverage_match.group(1).strip() if coverage_match else None
        
        fta_data[country] = {
            'hbbtv': hbbtv_info,
            'ci_plus': ci_info,
            'platforms': platforms,
            'coverage': coverage,
            'has_specification': '✅' in content or 'specification' in content.lower()
        }
    
    return fta_data

def extract_demographics_info():
    """Extract demographic information from demographics.md files"""
    demographics_data = {}
    base_dir = Path('Europe')
    
    for demo_file in base_dir.rglob('demographics.md'):
        parts = demo_file.parts
        if 'Europe' not in parts:
            continue
        
        europe_idx = parts.index('Europe')
        if europe_idx + 1 >= len(parts):
            continue
        
        country = parts[europe_idx + 1].replace('-', ' ').title()
        
        with open(demo_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract population
        pop_match = re.search(r'Population[:\s]+([0-9.,]+)', content, re.IGNORECASE)
        population = pop_match.group(1) if pop_match else None
        
        # Extract TV households
        tv_match = re.search(r'TV\s+Households[:\s]+([0-9.,]+)', content, re.IGNORECASE)
        tv_households = tv_match.group(1) if tv_match else None
        
        demographics_data[country] = {
            'population': population,
            'tv_households': tv_households
        }
    
    return demographics_data

def main():
    """Main function to extract all dashboard data comprehensively"""
    print("Extracting comprehensive dashboard data...")
    
    # Extract all data
    country_strategy = extract_country_strategy_info()
    spec_data = extract_specification_info_comprehensive()
    contacts_data = extract_operator_contacts_comprehensive()
    
    print("Linking contacts to operators...")
    linked_contacts = link_contacts_to_operators(spec_data, contacts_data)
    
    fta_data = extract_free_to_air_info_comprehensive()
    demographics_data = extract_demographics_info()
    
    # Combine into dashboard data structure
    dashboard_data = {
        'countries': {},
        'operators': spec_data,
        'contacts': linked_contacts,
        'free_to_air': fta_data,
        'demographics': demographics_data
    }
    
    # Get all countries
    all_countries = set()
    all_countries.update(country_strategy.keys())
    all_countries.update(spec_data.keys())
    all_countries.update(contacts_data.keys())
    all_countries.update(fta_data.keys())
    all_countries.update(demographics_data.keys())
    
    # Build comprehensive country data
    for country in sorted(all_countries):
        strategy_info = country_strategy.get(country, {})
        demo_info = demographics_data.get(country, {})
        fta_info = fta_data.get(country, {})
        
        dashboard_data['countries'][country] = {
            'population_million': strategy_info.get('population_million') or demo_info.get('population'),
            'tv_homes_million': strategy_info.get('tv_homes_million') or demo_info.get('tv_households'),
            'psb': strategy_info.get('psb', []),
            'retail_partners': strategy_info.get('retail_partners', []),
            'operators': list(spec_data.get(country, {}).keys()),
            'free_to_air': fta_info,
            'operator_details': strategy_info.get('operators', {})
        }
    
    # Write to JSON file
    output_file = Path('dashboard_data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Comprehensive dashboard data extracted to {output_file}")
    print(f"   Countries: {len(dashboard_data['countries'])}")
    print(f"   Operators: {sum(len(ops) for ops in spec_data.values())}")
    total_contacts = 0
    for ops in contacts_data.values():
        for contacts in ops.values():
            if isinstance(contacts, dict):
                total_contacts += sum(len(role_contacts) for role_contacts in contacts.values())
            elif isinstance(contacts, list):
                total_contacts += len(contacts)
    print(f"   Contacts: {total_contacts}")
    print(f"   Countries with demographics: {len(demographics_data)}")
    print(f"   Countries with free-to-air data: {len(fta_data)}")
    
    return dashboard_data

if __name__ == '__main__':
    main()

