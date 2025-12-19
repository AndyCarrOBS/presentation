#!/usr/bin/env python3
"""
Analyze what country data is missing
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.research_data_engineer import ResearchDataEngineer
from collections import defaultdict


def analyze_missing_data():
    """Analyze what country data is missing"""
    agent = ResearchDataEngineer(db_path='research_data.db')
    
    print("=" * 70)
    print("MISSING COUNTRY DATA ANALYSIS")
    print("=" * 70)
    
    # Get all countries in database
    country_facts = agent.db.get_facts(entity_type='country', current_only=True)
    db_countries = set(fact['entity_id'] for fact in country_facts)
    
    # Get all countries in Europe directory
    europe_dir = Path('Europe')
    europe_countries = set()
    if europe_dir.exists():
        for item in europe_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                europe_countries.add(item.name)
    
    # Group facts by country
    by_country = defaultdict(set)
    for fact in country_facts:
        by_country[fact['entity_id']].add(fact['attribute'])
    
    # Expected attributes
    expected_attrs = {'population_million', 'tv_homes_million', 'gdp_billion_eur'}
    
    # 1. Countries completely missing
    missing_countries = europe_countries - db_countries
    
    print(f"\n1. COUNTRIES COMPLETELY MISSING FROM DATABASE")
    print("-" * 70)
    print(f"Total: {len(missing_countries)} countries")
    if missing_countries:
        for country in sorted(missing_countries):
            # Check if they have demographics file
            demo_file = europe_dir / country / 'demographics.md'
            has_demo = demo_file.exists()
            status = "📄 has demographics.md" if has_demo else "❌ no demographics.md"
            print(f"  • {country} - {status}")
    
    # 2. Countries missing key attributes
    print(f"\n2. COUNTRIES WITH INCOMPLETE DATA")
    print("-" * 70)
    
    missing_pop = []
    missing_tv = []
    incomplete = []
    
    for country in sorted(db_countries):
        attrs = by_country.get(country, set())
        missing = expected_attrs - attrs
        
        if 'population_million' not in attrs:
            missing_pop.append(country)
        if 'tv_homes_million' not in attrs:
            missing_tv.append(country)
        if missing:
            incomplete.append((country, missing))
    
    print(f"\nMissing population_million: {len(missing_pop)} countries")
    if missing_pop:
        for country in sorted(missing_pop):
            attrs = by_country.get(country, set())
            print(f"  • {country} (has: {', '.join(sorted(attrs)) or 'none'})")
    
    print(f"\nMissing tv_homes_million: {len(missing_tv)} countries")
    if missing_tv:
        for country in sorted(missing_tv):
            attrs = by_country.get(country, set())
            print(f"  • {country} (has: {', '.join(sorted(attrs)) or 'none'})")
    
    # 3. Countries with demographics files but no data extracted
    print(f"\n3. COUNTRIES WITH DEMOGRAPHICS FILES BUT NO DATA EXTRACTED")
    print("-" * 70)
    
    countries_with_demo_no_data = []
    for country in europe_countries:
        demo_file = europe_dir / country / 'demographics.md'
        if demo_file.exists() and country not in db_countries:
            countries_with_demo_no_data.append(country)
    
    print(f"Total: {len(countries_with_demo_no_data)} countries")
    if countries_with_demo_no_data:
        for country in sorted(countries_with_demo_no_data):
            print(f"  • {country}")
    
    # 4. Summary
    print(f"\n4. SUMMARY")
    print("-" * 70)
    print(f"Total countries in Europe directory: {len(europe_countries)}")
    print(f"Countries with data in database: {len(db_countries)}")
    print(f"Countries completely missing: {len(missing_countries)}")
    print(f"Countries missing population data: {len(missing_pop)}")
    print(f"Countries missing TV homes data: {len(missing_tv)}")
    print(f"Countries with demographics files but no data: {len(countries_with_demo_no_data)}")
    
    # 5. Recommendations
    print(f"\n5. RECOMMENDATIONS")
    print("-" * 70)
    
    if countries_with_demo_no_data:
        print(f"✅ Re-extract from demographics files for {len(countries_with_demo_no_data)} countries")
        print(f"   These countries have demographics.md but no data was extracted")
    
    if missing_countries:
        print(f"⚠️  {len(missing_countries)} countries have no data at all")
        print(f"   Check if demographics.md files exist or need to be created")
    
    if missing_pop or missing_tv:
        print(f"⚠️  {len(set(missing_pop + missing_tv))} countries have incomplete data")
        print(f"   Consider enriching with external data sources")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    analyze_missing_data()
