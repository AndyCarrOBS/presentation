#!/usr/bin/env python3
"""
Export all database data to a master JSON file for visualization
"""
import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.research_data_engineer import ResearchDataEngineer


def export_master_json(output_file='master_data.json'):
    """Export all database data to a comprehensive JSON file"""
    print("=" * 70)
    print("EXPORTING MASTER JSON FILE")
    print("=" * 70)
    
    agent = ResearchDataEngineer(db_path='research_data.db')
    
    # Get all facts
    all_facts = agent.db.get_facts(current_only=True)
    
    # Get all sources
    with agent.db._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sources")
        sources = [dict(row) for row in cursor.fetchall()]
        
        # Get fact-source links
        cursor.execute("""
            SELECT fs.*, s.source_type, s.source_path, s.source_name, s.source_date
            FROM fact_sources fs
            JOIN sources s ON fs.source_id = s.id
        """)
        fact_sources = [dict(row) for row in cursor.fetchall()]
        
        # Get references
        cursor.execute("SELECT * FROM fact_references")
        references = [dict(row) for row in cursor.fetchall()]
        
        # Get external data
        cursor.execute("SELECT * FROM external_data")
        external_data = [dict(row) for row in cursor.fetchall()]
    
    # Organize data by entity type
    master_data = {
        'metadata': {
            'export_date': datetime.now().isoformat(),
            'total_facts': len(all_facts),
            'total_sources': len(sources),
            'total_references': len(references),
            'total_external_data': len(external_data)
        },
        'countries': {},
        'operators': {},
        'broadcasters': {},
        'sources': {},
        'statistics': {}
    }
    
    # Group facts by entity type and entity_id
    countries_data = defaultdict(dict)
    operators_data = defaultdict(dict)
    broadcasters_data = defaultdict(dict)
    
    # Create source lookup
    sources_lookup = {s['id']: s for s in sources}
    
    # Create fact-source lookup
    fact_sources_lookup = defaultdict(list)
    for fs in fact_sources:
        fact_sources_lookup[fs['fact_id']].append({
            'source_id': fs['source_id'],
            'source_type': fs['source_type'],
            'source_path': fs['source_path'],
            'source_name': fs['source_name'],
            'source_date': fs['source_date'],
            'confidence_score': fs['confidence_score'],
            'extraction_method': fs['extraction_method']
        })
    
    # Create references lookup
    references_lookup = defaultdict(list)
    for ref in references:
        references_lookup[ref['fact_id']].append({
            'reference_type': ref['reference_type'],
            'reference_url': ref['reference_url'],
            'reference_title': ref['reference_title'],
            'reference_date': ref['reference_date']
        })
    
    # Create external data lookup
    external_data_lookup = defaultdict(list)
    for ext in external_data:
        external_data_lookup[ext['fact_id']].append({
            'external_source': ext['external_source'],
            'external_id': ext['external_id'],
            'external_url': ext['external_url'],
            'fetched_at': ext['fetched_at'],
            'data_snapshot': json.loads(ext['data_snapshot']) if ext['data_snapshot'] else None
        })
    
    # Organize facts
    for fact in all_facts:
        entity_type = fact['entity_type']
        entity_id = fact['entity_id']
        attribute = fact['attribute']
        
        # Parse value based on type
        value = fact['value']
        if fact['value_type'] == 'number':
            try:
                value = float(value) if '.' in str(value) else int(value)
            except:
                pass
        elif fact['value_type'] == 'boolean':
            value = value.lower() in ('true', '1', 'yes')
        elif fact['value_type'] == 'json':
            try:
                value = json.loads(value)
            except:
                pass
        
        fact_data = {
            'value': value,
            'value_type': fact['value_type'],
            'unit': fact['unit'],
            'created_at': fact['created_at'],
            'updated_at': fact['updated_at'],
            'sources': fact_sources_lookup.get(fact['id'], []),
            'references': references_lookup.get(fact['id'], []),
            'external_data': external_data_lookup.get(fact['id'], [])
        }
        
        if entity_type == 'country':
            if entity_id not in countries_data:
                countries_data[entity_id] = {
                    'attributes': {},
                    'facts': []
                }
            countries_data[entity_id]['attributes'][attribute] = fact_data
            countries_data[entity_id]['facts'].append({
                'attribute': attribute,
                **fact_data
            })
        
        elif entity_type == 'operator':
            if entity_id not in operators_data:
                operators_data[entity_id] = {
                    'attributes': {},
                    'facts': []
                }
            operators_data[entity_id]['attributes'][attribute] = fact_data
            operators_data[entity_id]['facts'].append({
                'attribute': attribute,
                **fact_data
            })
        
        elif entity_type == 'broadcaster':
            if entity_id not in broadcasters_data:
                broadcasters_data[entity_id] = {
                    'attributes': {},
                    'facts': []
                }
            broadcasters_data[entity_id]['attributes'][attribute] = fact_data
            broadcasters_data[entity_id]['facts'].append({
                'attribute': attribute,
                **fact_data
            })
    
    # Convert to regular dicts and add to master_data
    master_data['countries'] = dict(countries_data)
    master_data['operators'] = dict(operators_data)
    master_data['broadcasters'] = dict(broadcasters_data)
    
    # Add sources
    for source in sources:
        source_id = str(source['id'])
        master_data['sources'][source_id] = {
            'source_type': source['source_type'],
            'source_path': source['source_path'],
            'source_name': source['source_name'],
            'source_date': source['source_date'],
            'source_metadata': json.loads(source['source_metadata']) if source['source_metadata'] else {}
        }
    
    # Calculate statistics
    master_data['statistics'] = {
        'countries': {
            'total': len(countries_data),
            'with_population': len([c for c in countries_data.values() if 'population_million' in c['attributes']]),
            'with_tv_homes': len([c for c in countries_data.values() if 'tv_homes_million' in c['attributes']]),
            'with_gdp': len([c for c in countries_data.values() if 'gdp_billion_eur' in c['attributes']])
        },
        'operators': {
            'total': len(operators_data),
            'with_subscribers': len([o for o in operators_data.values() if 'subscribers' in o['attributes']]),
            'with_hbbtv': len([o for o in operators_data.values() if 'hbbtv_version' in o['attributes']]),
            'with_ci': len([o for o in operators_data.values() if 'ci_version' in o['attributes']]),
            'with_ca': len([o for o in operators_data.values() if 'ca_systems' in o['attributes']]),
            'with_market_share': len([o for o in operators_data.values() if 'market_share_percent' in o['attributes']])
        },
        'broadcasters': {
            'total': len(broadcasters_data),
            'psbs': len([b for b in broadcasters_data.values() if b['attributes'].get('type', {}).get('value') == 'PSB'])
        },
        'data_quality': {
            'total_facts': len(all_facts),
            'facts_with_sources': len([f for f in all_facts if fact_sources_lookup.get(f['id'])]),
            'facts_with_references': len([f for f in all_facts if references_lookup.get(f['id'])]),
            'facts_with_external_data': len([f for f in all_facts if external_data_lookup.get(f['id'])])
        }
    }
    
    # Add a flattened view for easier visualization
    master_data['flattened'] = {
        'countries': [
            {
                'country': country_id,
                **{attr: data['value'] for attr, data in country_data['attributes'].items()}
            }
            for country_id, country_data in countries_data.items()
        ],
        'operators': [
            {
                'operator': operator_id,
                **{attr: data['value'] for attr, data in operator_data['attributes'].items()}
            }
            for operator_id, operator_data in operators_data.items()
        ],
        'broadcasters': [
            {
                'broadcaster': broadcaster_id,
                **{attr: data['value'] for attr, data in broadcaster_data['attributes'].items()}
            }
            for broadcaster_id, broadcaster_data in broadcasters_data.items()
        ]
    }
    
    # Write to file
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(master_data, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"\n✅ Master JSON exported to: {output_file}")
    print(f"\n📊 Export Statistics:")
    print(f"   Countries: {master_data['statistics']['countries']['total']}")
    print(f"   Operators: {master_data['statistics']['operators']['total']}")
    print(f"   Broadcasters: {master_data['statistics']['broadcasters']['total']}")
    print(f"   Total facts: {master_data['metadata']['total_facts']}")
    print(f"   Total sources: {master_data['metadata']['total_sources']}")
    print(f"   Total references: {master_data['metadata']['total_references']}")
    
    print(f"\n📋 Data Structure:")
    print(f"   • metadata - Export information and statistics")
    print(f"   • countries - Country data with attributes and sources")
    print(f"   • operators - Operator data with attributes and sources")
    print(f"   • broadcasters - Broadcaster data with attributes and sources")
    print(f"   • sources - Source information")
    print(f"   • statistics - Summary statistics")
    print(f"   • flattened - Flattened view for easy visualization")
    
    return master_data


if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else 'master_data.json'
    export_master_json(output_file)
