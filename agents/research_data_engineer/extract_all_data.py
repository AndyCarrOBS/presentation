#!/usr/bin/env python3
"""
Extract all data from the project using the Research Data Engineer Agent
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.research_data_engineer import ResearchDataEngineer
from collections import defaultdict


def extract_all_data():
    """Extract all data from markdown and JSON files"""
    print("=" * 70)
    print("RESEARCH DATA ENGINEER - EXTRACTING ALL DATA")
    print("=" * 70)
    
    # Initialize agent
    agent = ResearchDataEngineer(db_path='research_data.db')
    
    base_path = Path('.')
    stats = defaultdict(int)
    errors = []
    
    # 1. Extract from demographics files
    print("\n📊 Step 1: Extracting from demographics files...")
    print("-" * 70)
    demo_files = list(base_path.glob('Europe/**/demographics.md'))
    print(f"Found {len(demo_files)} demographics files")
    
    for demo_file in demo_files:
        try:
            facts = agent.extract_facts_from_markdown(str(demo_file))
            stats['demographics_files'] += 1
            stats['demographics_facts'] += len(facts)
            print(f"  ✅ {demo_file.parent.name}: {len(facts)} facts")
        except Exception as e:
            errors.append((str(demo_file), str(e)))
            print(f"  ❌ {demo_file.parent.name}: {e}")
    
    # 2. Extract from specification files
    print("\n📋 Step 2: Extracting from specification files...")
    print("-" * 70)
    spec_files = list(base_path.glob('Europe/**/specifications.md'))
    print(f"Found {len(spec_files)} specification files")
    
    for spec_file in spec_files:
        try:
            facts = agent.extract_facts_from_markdown(str(spec_file))
            stats['spec_files'] += 1
            stats['spec_facts'] += len(facts)
            print(f"  ✅ {spec_file.parent.parent.name}/{spec_file.parent.name}: {len(facts)} facts")
        except Exception as e:
            errors.append((str(spec_file), str(e)))
            print(f"  ❌ {spec_file.parent.name}: {e}")
    
    # 3. Extract from JSON files
    print("\n📄 Step 3: Extracting from JSON files...")
    print("-" * 70)
    json_files = [
        'dashboard_data.json',
        'operators-subscribers.json',
        'countries-operators.json'
    ]
    
    for json_file in json_files:
        json_path = base_path / json_file
        if json_path.exists():
            try:
                facts = agent.extract_facts_from_json(str(json_path))
                stats['json_files'] += 1
                stats['json_facts'] += len(facts)
                print(f"  ✅ {json_file}: {len(facts)} facts")
            except Exception as e:
                errors.append((str(json_path), str(e)))
                print(f"  ❌ {json_file}: {e}")
        else:
            print(f"  ⚠️  {json_file}: not found")
    
    # 4. Get total statistics
    print("\n📈 Step 4: Database Statistics...")
    print("-" * 70)
    all_facts = agent.db.get_facts()
    
    # Group by entity type
    by_type = defaultdict(int)
    by_country = defaultdict(int)
    by_operator = defaultdict(int)
    
    for fact in all_facts:
        by_type[fact['entity_type']] += 1
        if fact['entity_type'] == 'country':
            by_country[fact['entity_id']] += 1
        elif fact['entity_type'] == 'operator':
            by_operator[fact['entity_id']] += 1
    
    print(f"Total facts in database: {len(all_facts)}")
    print(f"\nBy entity type:")
    for etype, count in sorted(by_type.items()):
        print(f"  - {etype}: {count} facts")
    
    print(f"\nCountries with data: {len(by_country)}")
    print(f"Operators with data: {len(by_operator)}")
    
    # 5. Generate dashboard
    print("\n🎨 Step 5: Generating dashboard...")
    print("-" * 70)
    dashboard = agent.generate_dashboard_data()
    
    output_file = base_path / 'dashboard_data.json'
    import json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"✅ Dashboard saved to: {output_file}")
    print(f"   Countries: {dashboard['statistics']['total_countries']}")
    print(f"   Operators: {dashboard['statistics']['total_operators']}")
    print(f"   Total facts: {dashboard['statistics']['total_facts']}")
    
    # 6. Summary
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"Demographics files processed: {stats['demographics_files']}")
    print(f"Demographics facts extracted: {stats['demographics_facts']}")
    print(f"Specification files processed: {stats['spec_files']}")
    print(f"Specification facts extracted: {stats['spec_facts']}")
    print(f"JSON files processed: {stats['json_files']}")
    print(f"JSON facts extracted: {stats['json_facts']}")
    print(f"Total facts in database: {len(all_facts)}")
    print(f"Errors encountered: {len(errors)}")
    
    if errors:
        print("\n⚠️  Errors:")
        for file, error in errors[:10]:  # Show first 10 errors
            print(f"  - {Path(file).name}: {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    print("\n✅ Extraction complete!")
    print(f"📊 Database: research_data.db")
    print(f"📈 Dashboard: dashboard_data.json")
    print("=" * 70)


if __name__ == '__main__':
    extract_all_data()
