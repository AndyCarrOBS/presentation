#!/usr/bin/env python3
"""
Command-line interface for the Research Data Engineer Agent
"""
import argparse
import json
import sys
from pathlib import Path
from typing import List

from .agent import ResearchDataEngineer


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Research Data Engineer Agent - Extract, clean, and store research facts'
    )
    
    parser.add_argument(
        '--db',
        default='research_data.db',
        help='Path to database file (default: research_data.db)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract facts from files')
    extract_parser.add_argument('files', nargs='+', help='Files to extract from (markdown or JSON)')
    extract_parser.add_argument('--source-name', help='Custom source name')
    
    # Enrich command
    enrich_parser = subparsers.add_parser('enrich', help='Enrich facts with external data')
    enrich_parser.add_argument('--entity-type', required=True, help='Entity type (country, operator, etc.)')
    enrich_parser.add_argument('--entity-id', required=True, help='Entity ID')
    enrich_parser.add_argument('--attribute', required=True, help='Attribute name')
    enrich_parser.add_argument('--queries', nargs='+', help='Search queries')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate and clean facts')
    validate_parser.add_argument('--fact-id', type=int, help='Specific fact ID to validate')
    validate_parser.add_argument('--entity-type', help='Entity type filter')
    validate_parser.add_argument('--entity-id', help='Entity ID filter')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query facts from database')
    query_parser.add_argument('--entity-type', help='Filter by entity type')
    query_parser.add_argument('--entity-id', help='Filter by entity ID')
    query_parser.add_argument('--attribute', help='Filter by attribute')
    query_parser.add_argument('--format', choices=['json', 'table'], default='table', help='Output format')
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Generate dashboard data')
    dashboard_parser.add_argument('--output', help='Output file (default: stdout)')
    dashboard_parser.add_argument('--format', choices=['json', 'html'], default='json', help='Output format')
    
    # Trend command
    trend_parser = subparsers.add_parser('trend', help='Analyze trends for a data point')
    trend_parser.add_argument('--entity-type', required=True, help='Entity type')
    trend_parser.add_argument('--entity-id', required=True, help='Entity ID')
    trend_parser.add_argument('--attribute', required=True, help='Attribute name')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize agent
    agent = ResearchDataEngineer(db_path=args.db)
    
    # Execute command
    if args.command == 'extract':
        extract_facts(agent, args.files, args.source_name)
    elif args.command == 'enrich':
        enrich_facts(agent, args.entity_type, args.entity_id, args.attribute, args.queries)
    elif args.command == 'validate':
        validate_facts(agent, args.fact_id, args.entity_type, args.entity_id)
    elif args.command == 'query':
        query_facts(agent, args.entity_type, args.entity_id, args.attribute, args.format)
    elif args.command == 'dashboard':
        generate_dashboard(agent, args.output, args.format)
    elif args.command == 'trend':
        analyze_trend(agent, args.entity_type, args.entity_id, args.attribute)
    elif args.command == 'stats':
        show_stats(agent)


def extract_facts(agent: ResearchDataEngineer, files: List[str], source_name: str = None):
    """Extract facts from files"""
    total_facts = 0
    
    for file_path in files:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"⚠️  File not found: {file_path}", file=sys.stderr)
            continue
        
        try:
            if file_path.suffix == '.json':
                facts = agent.extract_facts_from_json(str(file_path), source_name)
            elif file_path.suffix == '.md':
                facts = agent.extract_facts_from_markdown(str(file_path), source_name)
            else:
                print(f"⚠️  Unsupported file type: {file_path.suffix}", file=sys.stderr)
                continue
            
            total_facts += len(facts)
            print(f"✅ Extracted {len(facts)} facts from {file_path.name}")
        
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}", file=sys.stderr)
    
    print(f"\n📊 Total facts extracted: {total_facts}")


def enrich_facts(agent: ResearchDataEngineer, entity_type: str, entity_id: str,
                attribute: str, queries: List[str] = None):
    """Enrich facts with external data"""
    print(f"🔍 Enriching {entity_type}/{entity_id}/{attribute}...")
    
    try:
        results = agent.enrich_with_external_data(
            entity_type, entity_id, attribute, queries
        )
        
        print(f"✅ Found {len(results)} external data points")
        for i, result in enumerate(results[:5], 1):  # Show first 5
            print(f"  {i}. {result.get('title', result.get('url', 'Unknown'))}")
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)


def validate_facts(agent: ResearchDataEngineer, fact_id: int = None,
                  entity_type: str = None, entity_id: str = None):
    """Validate facts"""
    if fact_id:
        result = agent.validate_and_clean_fact(fact_id)
        if result:
            print(f"✅ Fact {fact_id} validated")
            print(f"   Completeness: {result['completeness']:.2f}")
            print(f"   Accuracy: {result['accuracy']:.2f}")
            print(f"   Freshness: {result['freshness']:.2f}")
        else:
            print(f"❌ Fact {fact_id} not found")
    else:
        facts = agent.db.get_facts(entity_type=entity_type, entity_id=entity_id)
        print(f"Validating {len(facts)} facts...")
        
        validated = 0
        for fact in facts:
            try:
                result = agent.validate_and_clean_fact(fact['id'])
                if result:
                    validated += 1
            except Exception as e:
                print(f"⚠️  Error validating fact {fact['id']}: {e}", file=sys.stderr)
        
        print(f"✅ Validated {validated}/{len(facts)} facts")


def query_facts(agent: ResearchDataEngineer, entity_type: str = None,
               entity_id: str = None, attribute: str = None, format: str = 'table'):
    """Query facts"""
    facts = agent.db.get_facts(
        entity_type=entity_type,
        entity_id=entity_id,
        attribute=attribute
    )
    
    if format == 'json':
        print(json.dumps(facts, indent=2, default=str))
    else:
        if not facts:
            print("No facts found")
            return
        
        print(f"\nFound {len(facts)} facts:\n")
        for fact in facts:
            print(f"  [{fact['entity_type']}] {fact['entity_id']}.{fact['attribute']} = {fact['value']}")
            print(f"    Type: {fact['value_type']}, Created: {fact['created_at']}")


def generate_dashboard(agent: ResearchDataEngineer, output: str = None, format: str = 'json'):
    """Generate dashboard data"""
    dashboard = agent.generate_dashboard_data()
    
    if format == 'json':
        output_data = json.dumps(dashboard, indent=2, default=str)
    else:
        # HTML dashboard generation would go here
        output_data = json.dumps(dashboard, indent=2, default=str)
    
    if output:
        Path(output).write_text(output_data, encoding='utf-8')
        print(f"✅ Dashboard saved to {output}")
    else:
        print(output_data)


def analyze_trend(agent: ResearchDataEngineer, entity_type: str, entity_id: str, attribute: str):
    """Analyze trends"""
    analysis = agent.get_trend_analysis(entity_type, entity_id, attribute)
    
    if not analysis:
        print(f"❌ No trend data found for {entity_type}/{entity_id}/{attribute}")
        return
    
    print(f"\n📈 Trend Analysis: {entity_type}/{entity_id}/{attribute}")
    print(f"   Data points: {analysis['data_points']}")
    print(f"   First recorded: {analysis['first_recorded']}")
    print(f"   Last recorded: {analysis['last_recorded']}")
    print(f"   Current value: {analysis['current_value']}")
    print(f"   Trend: {analysis['trend']}")


def show_stats(agent: ResearchDataEngineer):
    """Show database statistics"""
    # Get counts
    countries = agent.db.get_facts(entity_type='country')
    operators = agent.db.get_facts(entity_type='operator')
    all_facts = agent.db.get_facts()
    
    print("\n📊 Database Statistics")
    print(f"   Total facts: {len(all_facts)}")
    print(f"   Countries: {len(countries)}")
    print(f"   Operators: {len(operators)}")
    print(f"   Unique attributes: {len(set(f['attribute'] for f in all_facts))}")


if __name__ == '__main__':
    main()
