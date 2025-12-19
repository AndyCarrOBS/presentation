#!/usr/bin/env python3
"""
Demo script showing how data is extracted, stored, and presented
"""
import json
from pathlib import Path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.research_data_engineer import ResearchDataEngineer


def show_extraction_process():
    """Demonstrate the extraction process"""
    print("=" * 70)
    print("RESEARCH DATA ENGINEER AGENT - DATA EXTRACTION DEMO")
    print("=" * 70)
    
    # Initialize agent
    agent = ResearchDataEngineer(db_path='demo_research_data.db')
    
    # Step 1: Extract from demographics
    print("\n📊 STEP 1: Extracting from demographics.md")
    print("-" * 70)
    demo_file = Path('Europe/Austria/demographics.md')
    
    if demo_file.exists():
        print(f"Reading: {demo_file}")
        content_preview = demo_file.read_text(encoding='utf-8')[:500]
        print(f"\nFile preview (first 500 chars):")
        print(content_preview + "...\n")
        
        facts = agent.extract_facts_from_markdown(str(demo_file))
        print(f"✅ Extracted {len(facts)} facts")
        
        # Show what was extracted
        for i, fact in enumerate(facts[:5], 1):
            fact_detail = agent.db.get_fact_with_sources(fact['fact_id'])
            if fact_detail:
                print(f"\n  Fact {i}:")
                print(f"    Entity: {fact_detail['entity_type']}/{fact_detail['entity_id']}")
                print(f"    Attribute: {fact_detail['attribute']}")
                print(f"    Value: {fact_detail['value']} ({fact_detail['value_type']})")
                print(f"    Source: {fact_detail['sources'][0]['source_name'] if fact_detail['sources'] else 'None'}")
                print(f"    Source Date: {fact_detail['sources'][0].get('source_date', 'N/A') if fact_detail['sources'] else 'N/A'}")
    else:
        print(f"⚠️  File not found: {demo_file}")
    
    # Step 2: Extract from specifications
    print("\n\n📋 STEP 2: Extracting from specifications.md")
    print("-" * 70)
    spec_file = Path('Europe/Austria/ORF/specifications.md')
    
    if spec_file.exists():
        print(f"Reading: {spec_file}")
        content_preview = spec_file.read_text(encoding='utf-8')[:500]
        print(f"\nFile preview (first 500 chars):")
        print(content_preview + "...\n")
        
        facts = agent.extract_facts_from_markdown(str(spec_file))
        print(f"✅ Extracted {len(facts)} facts")
        
        for i, fact in enumerate(facts[:5], 1):
            fact_detail = agent.db.get_fact_with_sources(fact['fact_id'])
            if fact_detail:
                print(f"\n  Fact {i}:")
                print(f"    Entity: {fact_detail['entity_type']}/{fact_detail['entity_id']}")
                print(f"    Attribute: {fact_detail['attribute']}")
                print(f"    Value: {fact_detail['value']}")
                if fact_detail.get('references'):
                    print(f"    References: {len(fact_detail['references'])}")
                    for ref in fact_detail['references'][:2]:
                        print(f"      - {ref.get('reference_url', 'N/A')}")
    else:
        print(f"⚠️  File not found: {spec_file}")
    
    # Step 3: Show database storage
    print("\n\n💾 STEP 3: Database Storage Structure")
    print("-" * 70)
    
    all_facts = agent.db.get_facts()
    print(f"Total facts in database: {len(all_facts)}")
    
    # Group by entity type
    by_type = {}
    for fact in all_facts:
        etype = fact['entity_type']
        by_type[etype] = by_type.get(etype, 0) + 1
    
    print("\nFacts by entity type:")
    for etype, count in by_type.items():
        print(f"  - {etype}: {count} facts")
    
    # Show database schema info
    print("\nDatabase tables:")
    print("  - facts: Core data points (entity_type, entity_id, attribute, value)")
    print("  - sources: Where data came from (files, URLs, etc.)")
    print("  - fact_sources: Links facts to sources with confidence scores")
    print("  - references: External citations and URLs")
    print("  - external_data: Data from web research")
    print("  - data_quality: Quality metrics (completeness, accuracy, freshness)")
    
    # Step 4: Generate dashboard data
    print("\n\n📈 STEP 4: Dashboard Data Generation")
    print("-" * 70)
    
    dashboard = agent.generate_dashboard_data()
    
    print(f"Dashboard Statistics:")
    print(f"  - Total Countries: {dashboard['statistics']['total_countries']}")
    print(f"  - Total Operators: {dashboard['statistics']['total_operators']}")
    print(f"  - Total Facts: {dashboard['statistics']['total_facts']}")
    
    # Show sample country data
    if dashboard['countries']:
        print(f"\nSample Country Data (first country):")
        first_country = list(dashboard['countries'].keys())[0]
        country_data = dashboard['countries'][first_country]
        print(f"  Country: {first_country}")
        for attr, value in list(country_data.items())[:5]:
            print(f"    {attr}: {value}")
    
    # Step 5: Show presentation format
    print("\n\n🎨 STEP 5: Presentation Format")
    print("-" * 70)
    
    print("The agent can generate data in multiple formats:")
    print("\n1. JSON (for API/dashboard consumption):")
    print("   python -m agents.research_data_engineer.cli dashboard --output dashboard.json --format json")
    
    print("\n2. Database queries (for custom visualizations):")
    print("   python -m agents.research_data_engineer.cli query --entity-type country")
    
    print("\n3. Trend analysis (for time-series visualization):")
    print("   python -m agents.research_data_engineer.cli trend --entity-type country --entity-id Austria --attribute population_million")
    
    # Save sample dashboard
    output_file = Path('demo_dashboard_output.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard, f, indent=2, default=str)
    print(f"\n✅ Sample dashboard saved to: {output_file}")
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    show_extraction_process()
