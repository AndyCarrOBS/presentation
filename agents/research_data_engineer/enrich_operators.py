#!/usr/bin/env python3
"""
Comprehensive operator data enrichment
Iterates through all countries, extracts operators, subscriber numbers,
broadcasters, and technical specifications (HbbTV, CI+, CA)
"""
import sys
import re
import json
from pathlib import Path
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.research_data_engineer import ResearchDataEngineer


class OperatorEnricher:
    """Enriches operator data for all countries"""
    
    def __init__(self, agent: ResearchDataEngineer):
        self.agent = agent
        self.base_path = Path('.')
    
    def extract_operators_from_demographics(self, country: str) -> list:
        """Extract operator information from demographics.md and Country-Strategy-Summary.md"""
        operators = []
        operator_names_seen = set()
        
        # First, try Country-Strategy-Summary.md (has more comprehensive data)
        strategy_file = self.base_path / 'Europe' / 'Country-Strategy-Summary.md'
        if strategy_file.exists():
            content = strategy_file.read_text(encoding='utf-8')
            
            # Find country section
            country_section = re.search(
                rf'## {re.escape(country)}.*?(?=## |$)',
                content,
                re.DOTALL | re.IGNORECASE
            )
            
            if country_section:
                section_text = country_section.group(0)
                
                # Extract operators from "In the market are the following TV platforms"
                # The format is: **Operator Name** (~X million subscribers), **Operator Name** (~X% market share)
                # The text is all on one line, so we need to match the entire sentence
                platforms_line = re.search(
                    r'In the market are the following TV platforms\s+([^\n]+)',
                    section_text,
                    re.IGNORECASE
                )
                
                if platforms_line:
                    platforms_text = platforms_line.group(1)
                    # Split by **, ** to get individual operators
                    # Then extract operator name and subscriber info from each
                    operator_parts = re.split(r'\*\*,\s*\*\*', platforms_text)
                    
                    op_matches = []
                    for part in operator_parts:
                        # Remove leading/trailing ** and whitespace
                        part = part.strip('*').strip()
                        # Extract operator name and info in parentheses
                        match = re.match(r'^([^(]+?)\s*\(~?([^)]+)\)', part)
                        if match:
                            op_name = match.group(1).strip()
                            op_info = match.group(2).strip()
                            # Create a match-like object
                            class Match:
                                def __init__(self, name, info):
                                    self.name = name
                                    self.info = info
                                def group(self, n):
                                    return self.name if n == 1 else self.info
                            op_matches.append(Match(op_name, op_info))
                    
                    for match in op_matches:
                        op_name = match.group(1).strip()
                        op_info = match.group(2).strip()
                        
                        if op_name not in operator_names_seen:
                            operator_names_seen.add(op_name)
                            
                            # Extract subscriber numbers
                            subscribers = None
                            sub_match = re.search(r'~?([\d.,\s]+)\s*(?:million|thousand|M|K)?', op_info, re.IGNORECASE)
                            if sub_match:
                                sub_str = sub_match.group(1).replace(',', '').replace(' ', '')
                                try:
                                    sub_num = float(sub_str)
                                    if 'million' in op_info.lower() or 'M' in op_info.upper():
                                        subscribers = int(sub_num * 1000000)
                                    elif 'thousand' in op_info.lower() or 'K' in op_info.upper():
                                        subscribers = int(sub_num * 1000)
                                    else:
                                        subscribers = int(sub_num)
                                except:
                                    pass
                            
                            # Extract market share
                            market_share = None
                            ms_match = re.search(r'~?([\d.]+)%', op_info)
                            if ms_match:
                                try:
                                    market_share = float(ms_match.group(1))
                                except:
                                    pass
                            
                            # Look for operator details section
                            op_details_section = re.search(
                                rf'\*\*{re.escape(op_name)}\*\*.*?(?=\*\*|## |$)',
                                section_text,
                                re.DOTALL | re.IGNORECASE
                            )
                            
                            platform_type = None
                            if op_details_section:
                                details = op_details_section.group(0)
                                # Extract platform type
                                pt_match = re.search(r'uses\s+\*\*([^*]+)\*\*', details, re.IGNORECASE)
                                if pt_match:
                                    platform_type = pt_match.group(1).strip()
                            
                            operators.append({
                                'name': op_name,
                                'subscribers': subscribers,
                                'platform_type': platform_type,
                                'market_share': market_share,
                                'details': op_details_section.group(0) if op_details_section else ''
                            })
        
        # Also check demographics.md for additional operators
        demo_file = self.base_path / 'Europe' / country / 'demographics.md'
        if demo_file.exists():
            content = demo_file.read_text(encoding='utf-8')
            
            # Look for "Major Operators" section
            operator_section = re.search(r'## \d+\.\s*Competitive Landscape.*?## \d+\.', content, re.DOTALL | re.IGNORECASE)
            if not operator_section:
                operator_section = re.search(r'Major Operators.*?## \d+\.', content, re.DOTALL | re.IGNORECASE)
            
            if operator_section:
                section_content = operator_section.group(0)
                
                # Extract operator blocks
                operator_blocks = re.finditer(
                    r'\*\*([^*]+)\*\*\s*\n(.*?)(?=\n\*\*|$)',
                    section_content,
                    re.MULTILINE
                )
                
                for match in operator_blocks:
                    op_name = match.group(1).strip()
                    op_details = match.group(2)
                    
                    if op_name not in operator_names_seen:
                        operator_names_seen.add(op_name)
                        
                        # Extract subscriber numbers
                        subscriber_match = re.search(
                            r'Subscriber\s+(?:numbers?|count)[:\s]+~?([\d.,\s]+(?:\s*(?:million|thousand|M|K))?)',
                            op_details,
                            re.IGNORECASE
                        )
                        subscribers = None
                        if subscriber_match:
                            sub_str = subscriber_match.group(1).strip().replace(',', '').replace(' ', '')
                            if 'million' in sub_str.lower() or 'M' in sub_str.upper():
                                sub_str = sub_str.lower().replace('million', '').replace('m', '')
                                try:
                                    subscribers = int(float(sub_str) * 1000000)
                                except:
                                    pass
                            elif 'thousand' in sub_str.lower() or 'K' in sub_str.upper():
                                sub_str = sub_str.lower().replace('thousand', '').replace('k', '')
                                try:
                                    subscribers = int(float(sub_str) * 1000)
                                except:
                                    pass
                            else:
                                try:
                                    subscribers = int(float(sub_str))
                                except:
                                    pass
                        
                        # Extract platform type
                        platform_match = re.search(
                            r'Platform\s+type[:\s]+([^\n]+)',
                            op_details,
                            re.IGNORECASE
                        )
                        platform_type = platform_match.group(1).strip() if platform_match else None
                        
                        # Extract market share
                        market_share_match = re.search(
                            r'Market\s+share[:\s]+~?([\d.]+)%',
                            op_details,
                            re.IGNORECASE
                        )
                        market_share = None
                        if market_share_match:
                            try:
                                market_share = float(market_share_match.group(1))
                            except:
                                pass
                        
                        operators.append({
                            'name': op_name,
                            'subscribers': subscribers,
                            'platform_type': platform_type,
                            'market_share': market_share,
                            'details': op_details
                        })
        
        return operators
    
    def extract_psbs_from_demographics(self, country: str) -> list:
        """Extract Public Service Broadcasters from demographics.md"""
        demo_file = self.base_path / 'Europe' / country / 'demographics.md'
        if not demo_file.exists():
            return []
        
        content = demo_file.read_text(encoding='utf-8')
        psbs = []
        
        # Look for PSB section or public service broadcaster mentions
        psb_patterns = [
            r'Public\s+service\s+broadcaster[:\s]+([^\n]+)',
            r'PSB[:\s]+([^\n]+)',
            r'\*\*([^*]+)\*\*.*?public\s+service\s+broadcaster',
        ]
        
        for pattern in psb_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                psb_name = match.group(1).strip()
                if psb_name and len(psb_name) < 100:  # Reasonable length
                    psbs.append(psb_name)
        
        # Also check Country-Strategy-Summary.md
        strategy_file = self.base_path / 'Europe' / 'Country-Strategy-Summary.md'
        if strategy_file.exists():
            strategy_content = strategy_file.read_text(encoding='utf-8')
            # Find country section
            country_section = re.search(
                rf'## {re.escape(country)}.*?(?=## |$)',
                strategy_content,
                re.DOTALL | re.IGNORECASE
            )
            if country_section:
                # Look for PSB mentions
                psb_matches = re.finditer(
                    r'public\s+service\s+broadcasters?[:\s]+([^\n]+)',
                    country_section.group(0),
                    re.IGNORECASE
                )
                for match in psb_matches:
                    psb_text = match.group(1).strip()
                    # Extract PSB names (often in parentheses or after colons)
                    psb_names = re.findall(r'([A-Z][A-Za-z\s]+(?:TV|Broadcasting|Media))', psb_text)
                    for name in psb_names:
                        if name not in psbs:
                            psbs.append(name.strip())
        
        return list(set(psbs))  # Remove duplicates
    
    def extract_operator_specs(self, country: str, operator: str) -> dict:
        """Extract technical specifications for an operator"""
        # Try to find specifications.md file
        spec_paths = [
            self.base_path / 'Europe' / country / operator / 'specifications.md',
            self.base_path / 'Operators' / operator / f'{operator}.md',
        ]
        
        specs = {
            'hbbtv_version': None,
            'ci_version': None,
            'ca_systems': [],
            'has_specification': False
        }
        
        for spec_path in spec_paths:
            if spec_path.exists():
                content = spec_path.read_text(encoding='utf-8')
                
                # Extract HbbTV version
                hbbtv_match = re.search(r'HbbTV[:\s]+([\d.]+)', content, re.IGNORECASE)
                if hbbtv_match:
                    specs['hbbtv_version'] = hbbtv_match.group(1)
                
                # Extract CI+ version
                ci_match = re.search(r'CI\+[:\s]+([\d.]+)', content, re.IGNORECASE)
                if ci_match:
                    specs['ci_version'] = ci_match.group(1)
                
                # Extract CA systems
                ca_patterns = [
                    (r'Nagravision', 'Nagravision'),
                    (r'Irdeto', 'Irdeto'),
                    (r'Conax', 'Conax'),
                    (r'Viaccess', 'Viaccess'),
                    (r'Videoguard|NDS', 'Videoguard/NDS'),
                    (r'Conditional\s+Access[:\s]+([^\n]+)', None)
                ]
                
                for pattern, name in ca_patterns:
                    if name:
                        if re.search(pattern, content, re.IGNORECASE):
                            if name not in specs['ca_systems']:
                                specs['ca_systems'].append(name)
                    else:
                        # Generic CA extraction
                        match = re.search(pattern, content, re.IGNORECASE)
                        if match:
                            ca_text = match.group(1) if match.lastindex else ''
                            # Extract CA system names from text
                            for ca_name in ['Nagravision', 'Irdeto', 'Conax', 'Viaccess', 'Videoguard']:
                                if ca_name.lower() in ca_text.lower() and ca_name not in specs['ca_systems']:
                                    specs['ca_systems'].append(ca_name)
                
                # Check if specification is available
                if '✅' in content or 'VERIFIED' in content or 'available' in content.lower():
                    specs['has_specification'] = True
                
                break  # Use first found file
        
        return specs
    
    def enrich_country(self, country: str) -> dict:
        """Enrich all operator data for a country"""
        print(f"\n📊 Enriching {country}...")
        
        result = {
            'country': country,
            'operators': [],
            'psbs': [],
            'commercial_broadcasters': []
        }
        
        # Extract operators from demographics
        operators = self.extract_operators_from_demographics(country)
        
        # Also check existing database for operators
        existing_ops = self.agent.db.get_facts(
            entity_type='operator',
            current_only=True
        )
        country_ops = [op for op in existing_ops if country.lower() in str(op.get('entity_id', '')).lower()]
        
        # Combine and deduplicate
        operator_names = set()
        for op in operators:
            operator_names.add(op['name'])
        for op in country_ops:
            operator_names.add(op['entity_id'])
        
        # Create source once for the country
        demo_file = self.base_path / 'Europe' / country / 'demographics.md'
        source_id = None
        if demo_file.exists():
            source_id = self.agent.db.add_source(
                source_type='file',
                source_path=str(demo_file),
                source_name=f'{country} demographics'
            )
        
        # Enrich each operator
        for op_name in operator_names:
            # Find operator data
            op_data = next((o for o in operators if o['name'] == op_name), {})
            
            # Get specifications
            specs = self.extract_operator_specs(country, op_name)
            
            # Store operator
            if op_data.get('subscribers'):
                self.agent.db.add_fact(
                    entity_type='operator',
                    entity_id=op_name,
                    attribute='subscribers',
                    value=int(op_data['subscribers']),
                    value_type='number',
                    unit='subscribers',
                    source_id=source_id,
                    extraction_method='demographics_extraction'
                )
            
            if specs['hbbtv_version']:
                self.agent.db.add_fact(
                    entity_type='operator',
                    entity_id=op_name,
                    attribute='hbbtv_version',
                    value=specs['hbbtv_version'],
                    value_type='string',
                    source_id=source_id,
                    extraction_method='specifications_extraction'
                )
            
            if specs['ci_version']:
                self.agent.db.add_fact(
                    entity_type='operator',
                    entity_id=op_name,
                    attribute='ci_version',
                    value=specs['ci_version'],
                    value_type='string',
                    source_id=source_id,
                    extraction_method='specifications_extraction'
                )
            
            if specs['ca_systems']:
                self.agent.db.add_fact(
                    entity_type='operator',
                    entity_id=op_name,
                    attribute='ca_systems',
                    value=json.dumps(specs['ca_systems']),
                    value_type='json',
                    source_id=source_id,
                    extraction_method='specifications_extraction'
                )
            
            if op_data.get('platform_type'):
                self.agent.db.add_fact(
                    entity_type='operator',
                    entity_id=op_name,
                    attribute='platform_type',
                    value=op_data['platform_type'],
                    value_type='string',
                    source_id=source_id,
                    extraction_method='demographics_extraction'
                )
            
            if op_data.get('market_share'):
                self.agent.db.add_fact(
                    entity_type='operator',
                    entity_id=op_name,
                    attribute='market_share_percent',
                    value=op_data['market_share'],
                    value_type='number',
                    unit='percent',
                    source_id=source_id,
                    extraction_method='demographics_extraction'
                )
            
            result['operators'].append({
                'name': op_name,
                'subscribers': op_data.get('subscribers'),
                'platform_type': op_data.get('platform_type'),
                'market_share': op_data.get('market_share'),
                'hbbtv_version': specs['hbbtv_version'],
                'ci_version': specs['ci_version'],
                'ca_systems': specs['ca_systems'],
                'has_specification': specs['has_specification']
            })
        
        # Extract PSBs
        psbs = self.extract_psbs_from_demographics(country)
        for psb in psbs:
            self.agent.db.add_fact(
                entity_type='broadcaster',
                entity_id=psb,
                attribute='type',
                value='PSB',
                value_type='string',
                source_id=source_id,
                extraction_method='demographics_extraction'
            )
            result['psbs'].append(psb)
        
        print(f"  ✅ Found {len(result['operators'])} operators, {len(result['psbs'])} PSBs")
        
        return result
    
    def enrich_all_countries(self):
        """Enrich operator data for all countries"""
        print("=" * 70)
        print("OPERATOR DATA ENRICHMENT")
        print("=" * 70)
        
        # Get all countries
        europe_dir = self.base_path / 'Europe'
        countries = []
        if europe_dir.exists():
            for item in europe_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.') and item.name != 'Multi-Country':
                    countries.append(item.name)
        
        countries.sort()
        
        print(f"\nFound {len(countries)} countries to process")
        
        results = []
        for country in countries:
            try:
                result = self.enrich_country(country)
                results.append(result)
            except Exception as e:
                print(f"  ❌ Error processing {country}: {e}")
        
        # Summary
        print("\n" + "=" * 70)
        print("ENRICHMENT SUMMARY")
        print("=" * 70)
        
        total_operators = sum(len(r['operators']) for r in results)
        total_psbs = sum(len(r['psbs']) for r in results)
        
        print(f"Countries processed: {len(results)}")
        print(f"Total operators: {total_operators}")
        print(f"Total PSBs: {total_psbs}")
        
        # Show countries with most operators
        results_sorted = sorted(results, key=lambda x: len(x['operators']), reverse=True)
        print(f"\nTop 10 countries by operator count:")
        for r in results_sorted[:10]:
            print(f"  • {r['country']}: {len(r['operators'])} operators")
        
        return results


def main():
    """Main function"""
    agent = ResearchDataEngineer(db_path='research_data.db')
    enricher = OperatorEnricher(agent)
    results = enricher.enrich_all_countries()
    
    # Save results to JSON
    output_file = Path('operator_enrichment_results.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"\n✅ Results saved to: {output_file}")
    print("✅ Database updated with operator data")


if __name__ == '__main__':
    main()
