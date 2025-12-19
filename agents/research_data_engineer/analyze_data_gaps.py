#!/usr/bin/env python3
"""
Analyze what data exists in markdown files but is missing from the database
"""
import sys
import re
from pathlib import Path
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.research_data_engineer import ResearchDataEngineer


def analyze_demographics_file(file_path: Path) -> dict:
    """Analyze a demographics.md file for extractable data"""
    content = file_path.read_text(encoding='utf-8')
    data_points = {
        'population': False,
        'tv_homes': False,
        'gdp': False,
        'retail_partners': False,
        'psbs': False,
        'operators': False,
        'market_forecasts': False,
        'connectivity': False,
        'devices': False,
        'regulatory': False
    }
    
    # Check for various data points
    if re.search(r'Total population|population.*million', content, re.IGNORECASE):
        data_points['population'] = True
    
    if re.search(r'TV.*household|TV.*home', content, re.IGNORECASE):
        data_points['tv_homes'] = True
    
    if re.search(r'GDP|gdp', content, re.IGNORECASE):
        data_points['gdp'] = True
    
    if re.search(r'retail.*partner|where.*TV.*purchased', content, re.IGNORECASE):
        data_points['retail_partners'] = True
    
    if re.search(r'public.*service.*broadcaster|PSB', content, re.IGNORECASE):
        data_points['psbs'] = True
    
    if re.search(r'Major Operators|Competitive Landscape|operator', content, re.IGNORECASE):
        data_points['operators'] = True
    
    if re.search(r'forecast|forecast.*year', content, re.IGNORECASE):
        data_points['market_forecasts'] = True
    
    if re.search(r'Broadband|connectivity|internet', content, re.IGNORECASE):
        data_points['connectivity'] = True
    
    if re.search(r'Smart TV|device.*penetration|Smartphone', content, re.IGNORECASE):
        data_points['devices'] = True
    
    if re.search(r'Regulatory|licensing|spectrum', content, re.IGNORECASE):
        data_points['regulatory'] = True
    
    return data_points


def analyze_specification_file(file_path: Path) -> dict:
    """Analyze a specifications.md file for extractable data"""
    content = file_path.read_text(encoding='utf-8')
    data_points = {
        'hbbtv': False,
        'ci_plus': False,
        'ca_systems': False,
        'developer_portal': False,
        'website': False,
        'parent_company': False,
        'access_methods': False,
        'test_material': False,
        'gated_process': False,
        'whitelist': False,
        'branding': False
    }
    
    if re.search(r'HbbTV|hbbtv', content, re.IGNORECASE):
        data_points['hbbtv'] = True
    
    if re.search(r'CI\+|CI Plus', content, re.IGNORECASE):
        data_points['ci_plus'] = True
    
    if re.search(r'Conditional Access|CAS|Nagravision|Irdeto|Conax|Viaccess', content, re.IGNORECASE):
        data_points['ca_systems'] = True
    
    if re.search(r'Developer Portal|developer.*portal', content, re.IGNORECASE):
        data_points['developer_portal'] = True
    
    if re.search(r'Website|website', content, re.IGNORECASE):
        data_points['website'] = True
    
    if re.search(r'Parent Company|parent.*company', content, re.IGNORECASE):
        data_points['parent_company'] = True
    
    if re.search(r'Access Methods|access.*method', content, re.IGNORECASE):
        data_points['access_methods'] = True
    
    if re.search(r'test.*material|Test Material', content, re.IGNORECASE):
        data_points['test_material'] = True
    
    if re.search(r'gated.*process|partnership|NDA', content, re.IGNORECASE):
        data_points['gated_process'] = True
    
    if re.search(r'whitelist|white.*list', content, re.IGNORECASE):
        data_points['whitelist'] = True
    
    if re.search(r'branding|brand.*agreement', content, re.IGNORECASE):
        data_points['branding'] = True
    
    return data_points


def check_database_coverage(agent: ResearchDataEngineer, entity_type: str, entity_id: str, attributes: list) -> dict:
    """Check what attributes exist in database for an entity"""
    facts = agent.db.get_facts(entity_type=entity_type, entity_id=entity_id, current_only=True)
    db_attributes = set(f['attribute'] for f in facts)
    
    coverage = {}
    for attr in attributes:
        coverage[attr] = attr in db_attributes
    
    return coverage


def analyze_data_gaps():
    """Analyze gaps between markdown files and database"""
    print("=" * 70)
    print("DATA GAP ANALYSIS")
    print("=" * 70)
    
    agent = ResearchDataEngineer(db_path='research_data.db')
    base_path = Path('.')
    
    # Analyze demographics files
    print("\n📊 Analyzing Demographics Files...")
    print("-" * 70)
    
    demo_files = list(base_path.glob('Europe/**/demographics.md'))
    demographics_gaps = defaultdict(int)
    missing_data = []
    
    for demo_file in demo_files:
        country = demo_file.parent.name
        data_points = analyze_demographics_file(demo_file)
        
        # Check what's in database
        db_facts = agent.db.get_facts(entity_type='country', entity_id=country, current_only=True)
        db_attrs = set(f['attribute'] for f in db_facts)
        
        # Check gaps
        if data_points['population'] and 'population_million' not in db_attrs:
            demographics_gaps['population'] += 1
            missing_data.append((country, 'population_million', 'demographics.md'))
        
        if data_points['tv_homes'] and 'tv_homes_million' not in db_attrs:
            demographics_gaps['tv_homes'] += 1
            missing_data.append((country, 'tv_homes_million', 'demographics.md'))
        
        if data_points['gdp'] and 'gdp_billion_eur' not in db_attrs:
            demographics_gaps['gdp'] += 1
            missing_data.append((country, 'gdp_billion_eur', 'demographics.md'))
        
        if data_points['retail_partners'] and 'retail_partners' not in db_attrs:
            demographics_gaps['retail_partners'] += 1
            missing_data.append((country, 'retail_partners', 'demographics.md'))
        
        if data_points['connectivity'] and 'broadband_penetration' not in db_attrs:
            demographics_gaps['connectivity'] += 1
        
        if data_points['devices'] and 'smart_tv_penetration' not in db_attrs:
            demographics_gaps['devices'] += 1
    
    print(f"Demographics files analyzed: {len(demo_files)}")
    print(f"Missing data points:")
    for data_point, count in sorted(demographics_gaps.items()):
        print(f"  • {data_point}: {count} countries")
    
    # Analyze specification files
    print("\n📋 Analyzing Specification Files...")
    print("-" * 70)
    
    spec_files = list(base_path.glob('Europe/**/specifications.md'))
    specification_gaps = defaultdict(int)
    
    for spec_file in spec_files:
        parts = spec_file.parts
        if 'Europe' in parts:
            idx = parts.index('Europe')
            if idx + 2 < len(parts):
                country = parts[idx + 1]
                operator = parts[idx + 2]
                
                data_points = analyze_specification_file(spec_file)
                
                # Check what's in database
                db_facts = agent.db.get_facts(entity_type='operator', entity_id=operator, current_only=True)
                db_attrs = set(f['attribute'] for f in db_facts)
                
                # Check gaps
                if data_points['developer_portal'] and 'developer_portal' not in db_attrs:
                    specification_gaps['developer_portal'] += 1
                
                if data_points['website'] and 'website' not in db_attrs:
                    specification_gaps['website'] += 1
                
                if data_points['parent_company'] and 'parent_company' not in db_attrs:
                    specification_gaps['parent_company'] += 1
                
                if data_points['test_material'] and 'has_test_material' not in db_attrs:
                    specification_gaps['test_material'] += 1
                
                if data_points['gated_process'] and 'has_gated_process' not in db_attrs:
                    specification_gaps['gated_process'] += 1
                
                if data_points['whitelist'] and 'has_whitelist' not in db_attrs:
                    specification_gaps['whitelist'] += 1
                
                if data_points['branding'] and 'has_branding_agreement' not in db_attrs:
                    specification_gaps['branding'] += 1
    
    print(f"Specification files analyzed: {len(spec_files)}")
    print(f"Missing data points:")
    for data_point, count in sorted(specification_gaps.items()):
        print(f"  • {data_point}: {count} operators")
    
    # Check for additional data types
    print("\n🔍 Checking for Additional Data Types...")
    print("-" * 70)
    
    # Check for contact files
    contact_files = list(base_path.glob('Europe/**/*contact*.md'))
    contact_files.extend(list(base_path.glob('**/Operator-Key-Contacts.md')))
    
    print(f"Contact files found: {len(contact_files)}")
    
    # Check for free-to-air market files
    fta_files = list(base_path.glob('Europe/**/free-to-air-market.md'))
    print(f"Free-to-air market files: {len(fta_files)}")
    
    # Summary
    print("\n" + "=" * 70)
    print("GAP ANALYSIS SUMMARY")
    print("=" * 70)
    
    total_gaps = sum(demographics_gaps.values()) + sum(specification_gaps.values())
    
    print(f"\nTotal missing data points: {total_gaps}")
    print(f"Countries with missing demographics data: {len(set(m[0] for m in missing_data if m[2] == 'demographics.md'))}")
    print(f"Operators with missing specification data: {sum(specification_gaps.values())}")
    
    print(f"\n📋 Recommendations:")
    print(f"  1. Extract retail partners from demographics files")
    print(f"  2. Extract connectivity/device data from demographics files")
    print(f"  3. Extract developer portals, websites, parent companies from specifications")
    print(f"  4. Extract test material, gated process, whitelist flags from specifications")
    print(f"  5. Extract contact information from contact files")
    print(f"  6. Extract free-to-air market data")
    
    return {
        'demographics_gaps': dict(demographics_gaps),
        'specification_gaps': dict(specification_gaps),
        'missing_data': missing_data[:20]  # First 20 examples
    }


if __name__ == '__main__':
    analyze_data_gaps()
