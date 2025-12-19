#!/usr/bin/env python3
"""
Extract all missing data from markdown files and add to database
"""
import sys
import re
import json
from pathlib import Path
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.research_data_engineer import ResearchDataEngineer


def extract_connectivity_data(content: str, country: str, source_id: int, agent: ResearchDataEngineer):
    """Extract connectivity and device penetration data"""
    facts_added = 0
    
    # Broadband penetration - try multiple patterns
    bb_match = re.search(r'Broadband penetration[:\s]+~?([\d.]+)%', content, re.IGNORECASE)
    if not bb_match:
        bb_match = re.search(r'Broadband penetration[:\s]+~?([\d.]+)\s*of', content, re.IGNORECASE)
    if not bb_match:
        bb_match = re.search(r'internet penetration[:\s]+~?([\d.]+)%', content, re.IGNORECASE)
    
    if bb_match:
        try:
            penetration = float(bb_match.group(1))
            agent.db.add_fact(
                entity_type='country',
                entity_id=country,
                attribute='broadband_penetration_percent',
                value=penetration,
                value_type='number',
                unit='percent',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts_added += 1
        except:
            pass
    
    # Average broadband speed
    speed_match = re.search(r'Average broadband speed[:\s]+~?([\d.]+)\s*Mbps', content, re.IGNORECASE)
    if speed_match:
        try:
            speed = float(speed_match.group(1))
            agent.db.add_fact(
                entity_type='country',
                entity_id=country,
                attribute='broadband_speed_mbps',
                value=speed,
                value_type='number',
                unit='mbps',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts_added += 1
        except:
            pass
    
    # Smart TV penetration
    stv_match = re.search(r'Smart TV penetration[:\s]+~?([\d.]+)%', content, re.IGNORECASE)
    if stv_match:
        try:
            penetration = float(stv_match.group(1))
            agent.db.add_fact(
                entity_type='country',
                entity_id=country,
                attribute='smart_tv_penetration_percent',
                value=penetration,
                value_type='number',
                unit='percent',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts_added += 1
        except:
            pass
    
    # Smartphone penetration
    phone_match = re.search(r'Smartphone penetration[:\s]+~?([\d.]+)%', content, re.IGNORECASE)
    if phone_match:
        try:
            penetration = float(phone_match.group(1))
            agent.db.add_fact(
                entity_type='country',
                entity_id=country,
                attribute='smartphone_penetration_percent',
                value=penetration,
                value_type='number',
                unit='percent',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts_added += 1
        except:
            pass
    
    return facts_added


def extract_retail_partners(content: str, country: str, source_id: int, agent: ResearchDataEngineer):
    """Extract retail partners from demographics or strategy files"""
    facts_added = 0
    
    # Look for retail partners pattern
    retail_match = re.search(
        r'retail partners.*?where.*?TV.*?purchased[:\s]+([^\n]+)',
        content,
        re.IGNORECASE | re.DOTALL
    )
    
    if retail_match:
        partners_text = retail_match.group(1)
        # Extract partner names (usually in bold or listed)
        partners = re.findall(r'\*\*([^*]+)\*\*', partners_text)
        if not partners:
            # Try comma-separated
            partners = [p.strip() for p in partners_text.split(',') if p.strip()]
        
        if partners:
            # Store as JSON array
            agent.db.add_fact(
                entity_type='country',
                entity_id=country,
                attribute='retail_partners',
                value=json.dumps(partners),
                value_type='json',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts_added += 1
    
    return facts_added


def extract_operator_details(content: str, operator: str, source_id: int, agent: ResearchDataEngineer):
    """Extract additional operator details from specifications"""
    facts_added = 0
    
    # Developer portal
    dev_portal_match = re.search(r'Developer Portal[:\s]+([^\n]+)', content, re.IGNORECASE)
    if dev_portal_match:
        portal = dev_portal_match.group(1).strip()
        if portal and portal.lower() not in ['to be verified', 'none', 'n/a']:
            agent.db.add_fact(
                entity_type='operator',
                entity_id=operator,
                attribute='developer_portal',
                value=portal,
                value_type='string',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts_added += 1
    
    # Website - try multiple patterns
    website_match = re.search(r'\*\*Website\*\*[:\s]+(https?://[^\s\n]+|www\.[^\s\n]+)', content, re.IGNORECASE)
    if not website_match:
        website_match = re.search(r'Website[:\s]+(https?://[^\s\n]+|www\.[^\s\n]+)', content, re.IGNORECASE)
    if not website_match:
        # Look for URLs in the content
        url_match = re.search(r'(https?://www\.[^\s\n]+)', content, re.IGNORECASE)
        if url_match and 'developer' not in url_match.group(1).lower() and 'specification' not in url_match.group(1).lower():
            website_match = url_match
    
    if website_match:
        website = website_match.group(1).strip()
        # Check if already exists
        existing = agent.db.get_facts(
            entity_type='operator',
            entity_id=operator,
            attribute='website',
            current_only=True
        )
        if not existing:
            agent.db.add_fact(
                entity_type='operator',
                entity_id=operator,
                attribute='website',
                value=website,
                value_type='string',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts_added += 1
    
    # Parent company
    parent_match = re.search(r'Parent Company[:\s]+([^\n]+?)(?:\n|$)', content, re.IGNORECASE)
    if parent_match:
        parent = parent_match.group(1).strip()
        # Clean up
        parent = re.sub(r'^\*\*|\*\*$', '', parent)
        if parent and len(parent) < 100 and parent.lower() not in ['to be verified', 'none', 'n/a']:
            agent.db.add_fact(
                entity_type='operator',
                entity_id=operator,
                attribute='parent_company',
                value=parent,
                value_type='string',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts_added += 1
    
    # Test material flag
    if re.search(r'test.*material|Test Material', content, re.IGNORECASE):
        agent.db.add_fact(
            entity_type='operator',
            entity_id=operator,
            attribute='has_test_material',
            value=True,
            value_type='boolean',
            source_id=source_id,
            extraction_method='regex_pattern'
        )
        facts_added += 1
    
    # Gated process flag
    if re.search(r'gated.*process|partnership.*required|NDA.*required', content, re.IGNORECASE):
        agent.db.add_fact(
            entity_type='operator',
            entity_id=operator,
            attribute='has_gated_process',
            value=True,
            value_type='boolean',
            source_id=source_id,
            extraction_method='regex_pattern'
        )
        facts_added += 1
    
    # Whitelist flag
    if re.search(r'whitelist|white.*list', content, re.IGNORECASE):
        agent.db.add_fact(
            entity_type='operator',
            entity_id=operator,
            attribute='has_whitelist',
            value=True,
            value_type='boolean',
            source_id=source_id,
            extraction_method='regex_pattern'
        )
        facts_added += 1
    
    # Branding agreement flag
    if re.search(r'branding.*agreement|brand.*agreement', content, re.IGNORECASE):
        agent.db.add_fact(
            entity_type='operator',
            entity_id=operator,
            attribute='has_branding_agreement',
            value=True,
            value_type='boolean',
            source_id=source_id,
            extraction_method='regex_pattern'
        )
        facts_added += 1
    
    return facts_added


def extract_all_missing_data():
    """Extract all missing data from markdown files"""
    print("=" * 70)
    print("EXTRACTING MISSING DATA FROM MARKDOWN FILES")
    print("=" * 70)
    
    agent = ResearchDataEngineer(db_path='research_data.db')
    base_path = Path('.')
    
    stats = defaultdict(int)
    
    # 1. Extract connectivity and device data from demographics
    print("\n📡 Step 1: Extracting connectivity and device data...")
    print("-" * 70)
    
    demo_files = list(base_path.glob('Europe/**/demographics.md'))
    for demo_file in demo_files:
        country = demo_file.parent.name
        content = demo_file.read_text(encoding='utf-8')
        
        source_id = agent.db.add_source(
            source_type='file',
            source_path=str(demo_file),
            source_name=f'{country} demographics'
        )
        
        facts = extract_connectivity_data(content, country, source_id, agent)
        stats['connectivity_facts'] += facts
        
        facts = extract_retail_partners(content, country, source_id, agent)
        stats['retail_partner_facts'] += facts
    
    print(f"  ✅ Extracted {stats['connectivity_facts']} connectivity/device facts")
    print(f"  ✅ Extracted {stats['retail_partner_facts']} retail partner facts")
    
    # 2. Extract retail partners from Country-Strategy-Summary.md
    print("\n🛒 Step 2: Extracting retail partners from strategy file...")
    print("-" * 70)
    
    strategy_file = base_path / 'Europe' / 'Country-Strategy-Summary.md'
    if strategy_file.exists():
        content = strategy_file.read_text(encoding='utf-8')
        
        source_id = agent.db.add_source(
            source_type='file',
            source_path=str(strategy_file),
            source_name='Country Strategy Summary'
        )
        
        # Extract retail partners for each country
        country_sections = re.split(r'\n## ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\n', content)[1:]
        
        for i in range(0, len(country_sections), 2):
            if i + 1 >= len(country_sections):
                break
            
            country = country_sections[i].strip()
            section_content = country_sections[i + 1]
            
            # Extract retail partners
            retail_match = re.search(
                r'retail partners.*?where.*?TV.*?purchased[:\s]+([^\n]+)',
                section_content,
                re.IGNORECASE
            )
            
            if retail_match:
                partners_text = retail_match.group(1)
                partners = re.findall(r'\*\*([^*]+)\*\*', partners_text)
                
                if partners:
                    # Check if already exists
                    existing = agent.db.get_facts(
                        entity_type='country',
                        entity_id=country,
                        attribute='retail_partners',
                        current_only=True
                    )
                    
                    if not existing:
                        agent.db.add_fact(
                            entity_type='country',
                            entity_id=country,
                            attribute='retail_partners',
                            value=json.dumps(partners),
                            value_type='json',
                            source_id=source_id,
                            extraction_method='regex_pattern'
                        )
                        stats['retail_partner_facts'] += 1
    
    print(f"  ✅ Extracted retail partners from strategy file")
    
    # 3. Extract additional operator details from specifications
    print("\n📋 Step 3: Extracting additional operator details...")
    print("-" * 70)
    
    spec_files = list(base_path.glob('Europe/**/specifications.md'))
    for spec_file in spec_files:
        parts = spec_file.parts
        if 'Europe' in parts:
            idx = parts.index('Europe')
            if idx + 2 < len(parts):
                country = parts[idx + 1]
                operator = parts[idx + 2]
                
                content = spec_file.read_text(encoding='utf-8')
                
                source_id = agent.db.add_source(
                    source_type='file',
                    source_path=str(spec_file),
                    source_name=f'{operator} specifications'
                )
                
                facts = extract_operator_details(content, operator, source_id, agent)
                stats['operator_detail_facts'] += facts
    
    print(f"  ✅ Extracted {stats['operator_detail_facts']} operator detail facts")
    
    # 4. Summary
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    
    total_facts = sum(stats.values())
    print(f"\nTotal new facts added: {total_facts}")
    print(f"  • Connectivity/device facts: {stats['connectivity_facts']}")
    print(f"  • Retail partner facts: {stats['retail_partner_facts']}")
    print(f"  • Operator detail facts: {stats['operator_detail_facts']}")
    
    # Final database stats
    all_facts = agent.db.get_facts(current_only=True)
    print(f"\n📊 Final Database Statistics:")
    print(f"   Total facts: {len(all_facts)}")
    
    return stats


if __name__ == '__main__':
    extract_all_missing_data()
