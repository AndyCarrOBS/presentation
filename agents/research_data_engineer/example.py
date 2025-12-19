#!/usr/bin/env python3
"""
Example usage of the Research Data Engineer Agent
"""
from pathlib import Path
from agent import ResearchDataEngineer


def main():
    """Example workflow"""
    # Initialize agent
    print("🔧 Initializing Research Data Engineer Agent...")
    agent = ResearchDataEngineer(db_path='example_research_data.db')
    
    # Example 1: Extract facts from markdown files
    print("\n📄 Example 1: Extracting facts from markdown files...")
    demo_files = [
        'Europe/Austria/demographics.md',
        'Europe/Austria/ORF/specifications.md'
    ]
    
    for file_path in demo_files:
        full_path = Path(file_path)
        if full_path.exists():
            try:
                facts = agent.extract_facts_from_markdown(str(full_path))
                print(f"✅ Extracted {len(facts)} facts from {full_path.name}")
            except Exception as e:
                print(f"⚠️  Error extracting from {full_path.name}: {e}")
        else:
            print(f"⚠️  File not found: {full_path}")
    
    # Example 2: Extract facts from JSON
    print("\n📊 Example 2: Extracting facts from JSON...")
    json_file = Path('dashboard_data.json')
    if json_file.exists():
        try:
            facts = agent.extract_facts_from_json(str(json_file))
            print(f"✅ Extracted {len(facts)} facts from {json_file.name}")
        except Exception as e:
            print(f"⚠️  Error extracting from {json_file.name}: {e}")
    else:
        print(f"⚠️  File not found: {json_file}")
    
    # Example 3: Query facts
    print("\n🔍 Example 3: Querying facts...")
    facts = agent.db.get_facts(entity_type='country', entity_id='Austria')
    print(f"Found {len(facts)} facts about Austria:")
    for fact in facts[:5]:  # Show first 5
        print(f"  - {fact['attribute']}: {fact['value']}")
    
    # Example 4: Generate dashboard
    print("\n📈 Example 4: Generating dashboard data...")
    dashboard = agent.generate_dashboard_data()
    print(f"Dashboard contains:")
    print(f"  - {dashboard['statistics']['total_countries']} countries")
    print(f"  - {dashboard['statistics']['total_operators']} operators")
    print(f"  - {dashboard['statistics']['total_facts']} total facts")
    
    # Example 5: Trend analysis (if we have historical data)
    print("\n📊 Example 5: Trend analysis...")
    trend = agent.get_trend_analysis(
        entity_type='country',
        entity_id='Austria',
        attribute='population_million'
    )
    if trend:
        print(f"Trend for Austria population:")
        print(f"  - Data points: {trend['data_points']}")
        print(f"  - Current value: {trend['current_value']}")
        print(f"  - Trend: {trend['trend']}")
    else:
        print("  No trend data available yet")
    
    print("\n✅ Examples completed!")


if __name__ == '__main__':
    main()
