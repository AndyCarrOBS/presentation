#!/usr/bin/env python3
"""
Systematic Operator Research Workflow
Uses existing data as reference, validates and enriches with web research,
and stores all data with precise source tracking.
"""
import sys
import re
import json
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.research_data_engineer import ResearchDataEngineer


class OperatorResearchWorkflow:
    """Systematic workflow for researching operator data"""
    
    def __init__(self, agent: ResearchDataEngineer, openai_api_key: str = None):
        self.agent = agent
        self.base_path = Path('.')
        self.research_results = []
        self.stats = defaultdict(int)
        
        # Set OpenAI API key if provided
        if openai_api_key:
            self.agent.researcher.openai_api_key = openai_api_key
            self.agent.researcher.openai_base_url = 'https://api.openai.com/v1'
            # Update session headers
            self.agent.researcher.session.headers.update({
                'Authorization': f'Bearer {openai_api_key}'
            })
    
    def get_operator_data_gaps(self, operator: str) -> dict:
        """Identify what data is missing for an operator"""
        try:
            facts = self.agent.db.get_facts(entity_type='operator', entity_id=operator, current_only=True)
            existing_attrs = set(f['attribute'] for f in facts) if facts else set()
        except Exception as e:
            existing_attrs = set()
        
        # Required attributes
        required_attrs = {
            'subscribers': 'Subscriber numbers',
            'hbbtv_version': 'HbbTV version',
            'ci_version': 'CI+ version',
            'ca_systems': 'Conditional Access systems',
            'platform_type': 'Platform type',
            'market_share_percent': 'Market share',
            'website': 'Website URL',
            'developer_portal': 'Developer portal',
            'parent_company': 'Parent company',
            'has_specification': 'Specification availability',
            'has_test_material': 'Test material availability',
            'has_gated_process': 'Gated process flag',
            'has_whitelist': 'Whitelist flag',
            'has_branding_agreement': 'Branding agreement flag'
        }
        
        gaps = {}
        for attr, description in required_attrs.items():
            if attr not in existing_attrs:
                gaps[attr] = description
        
        return gaps
    
    def generate_search_queries(self, operator: str, gaps: dict) -> list:
        """Generate web search queries for missing data"""
        queries = []
        
        # Base query for operator
        base_query = f"{operator} TV operator"
        
        # Specific queries for gaps
        if 'subscribers' in gaps:
            queries.append(f"{operator} subscribers 2024")
            queries.append(f"{operator} TV subscribers number")
        
        if 'hbbtv_version' in gaps:
            queries.append(f"{operator} HbbTV version specifications")
            queries.append(f"{operator} HbbTV technical specifications")
        
        if 'ci_version' in gaps:
            queries.append(f"{operator} CI+ version")
            queries.append(f"{operator} CI Plus specifications")
        
        if 'ca_systems' in gaps:
            queries.append(f"{operator} conditional access system")
            queries.append(f"{operator} CAS Nagravision Irdeto")
        
        if 'website' in gaps:
            queries.append(f"{operator} official website")
        
        if 'developer_portal' in gaps:
            queries.append(f"{operator} developer portal")
            queries.append(f"{operator} API documentation")
        
        if 'parent_company' in gaps:
            queries.append(f"{operator} parent company owner")
        
        if 'market_share_percent' in gaps:
            queries.append(f"{operator} market share pay-TV")
        
        # Always add a general query for validation
        queries.append(base_query)
        
        return queries
    
    def extract_data_from_web_result(self, result: dict, operator: str, gaps: dict) -> dict:
        """Extract structured data from web search results"""
        extracted = {}
        
        if not result or 'content' not in result:
            return extracted
        
        content = result.get('content', '') or result.get('snippet', '') or ''
        url = result.get('url', '')
        title = result.get('title', '')
        
        # Extract subscriber numbers
        if 'subscribers' in gaps:
            # Patterns: "X million subscribers", "X,XXX,XXX subscribers", "X.XM subscribers"
            sub_patterns = [
                r'([\d.,]+)\s*(?:million|M)\s*subscribers',
                r'([\d.,]+)\s*subscribers',
                r'~?([\d.,]+)\s*(?:million|M)\s*customers',
            ]
            for pattern in sub_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    try:
                        sub_str = match.group(1).replace(',', '').replace('.', '')
                        if 'million' in match.group(0).lower() or 'M' in match.group(0).upper():
                            subscribers = int(float(sub_str) * 1000000)
                        else:
                            subscribers = int(float(sub_str))
                        extracted['subscribers'] = {
                            'value': subscribers,
                            'source_url': url,
                            'source_title': title,
                            'extraction_method': 'web_search',
                            'confidence': 0.7
                        }
                        break
                    except:
                        pass
        
        # Extract HbbTV version
        if 'hbbtv_version' in gaps:
            hbbtv_match = re.search(r'HbbTV\s+([\d.]+)', content, re.IGNORECASE)
            if hbbtv_match:
                extracted['hbbtv_version'] = {
                    'value': hbbtv_match.group(1),
                    'source_url': url,
                    'source_title': title,
                    'extraction_method': 'web_search',
                    'confidence': 0.8
                }
        
        # Extract CI+ version
        if 'ci_version' in gaps:
            ci_match = re.search(r'CI\+?\s+([\d.]+)', content, re.IGNORECASE)
            if ci_match:
                extracted['ci_version'] = {
                    'value': ci_match.group(1),
                    'source_url': url,
                    'source_title': title,
                    'extraction_method': 'web_search',
                    'confidence': 0.8
                }
        
        # Extract CA systems
        if 'ca_systems' in gaps:
            ca_systems = []
            ca_patterns = [
                (r'Nagravision', 'Nagravision'),
                (r'Irdeto', 'Irdeto'),
                (r'Conax', 'Conax'),
                (r'Viaccess', 'Viaccess'),
                (r'Videoguard|NDS', 'Videoguard/NDS'),
            ]
            for pattern, name in ca_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    ca_systems.append(name)
            if ca_systems:
                extracted['ca_systems'] = {
                    'value': ca_systems,
                    'source_url': url,
                    'source_title': title,
                    'extraction_method': 'web_search',
                    'confidence': 0.7
                }
        
        # Extract website
        if 'website' in gaps:
            website_match = re.search(r'(https?://(?:www\.)?[^\s\)]+)', content)
            if website_match:
                website = website_match.group(1)
                # Filter out common non-operator sites
                if not any(skip in website.lower() for skip in ['wikipedia', 'linkedin', 'facebook', 'twitter']):
                    extracted['website'] = {
                        'value': website,
                        'source_url': url,
                        'source_title': title,
                        'extraction_method': 'web_search',
                        'confidence': 0.6
                    }
        
        # Extract parent company
        if 'parent_company' in gaps:
            parent_patterns = [
                r'parent company[:\s]+([A-Z][A-Za-z\s&]+)',
                r'owned by[:\s]+([A-Z][A-Za-z\s&]+)',
                r'([A-Z][A-Za-z\s&]+)\s+owns\s+' + re.escape(operator),
            ]
            for pattern in parent_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    parent = match.group(1).strip()
                    if len(parent) < 100:  # Reasonable length
                        extracted['parent_company'] = {
                            'value': parent,
                            'source_url': url,
                            'source_title': title,
                            'extraction_method': 'web_search',
                            'confidence': 0.6
                        }
                        break
        
        # Extract market share
        if 'market_share_percent' in gaps:
            ms_match = re.search(r'([\d.]+)%\s*(?:market share|of.*market)', content, re.IGNORECASE)
            if ms_match:
                try:
                    market_share = float(ms_match.group(1))
                    extracted['market_share_percent'] = {
                        'value': market_share,
                        'source_url': url,
                        'source_title': title,
                        'extraction_method': 'web_search',
                        'confidence': 0.7
                    }
                except:
                    pass
        
        return extracted
    
    def research_operator(self, operator: str, country: str = None) -> dict:
        """Research a single operator systematically"""
        print(f"\n🔍 Researching: {operator}")
        if country:
            print(f"   Country: {country}")
        
        result = {
            'operator': operator,
            'country': country,
            'existing_data': {},
            'gaps_identified': {},
            'research_performed': {},
            'new_data_added': {},
            'validation_results': {}
        }
        
        try:
            # 1. Get existing data
            facts = self.agent.db.get_facts(entity_type='operator', entity_id=operator, current_only=True)
            for fact in facts:
                result['existing_data'][fact['attribute']] = fact['value']
            
            # 2. Identify gaps
            gaps = self.get_operator_data_gaps(operator)
            result['gaps_identified'] = gaps
        except Exception as e:
            print(f"   ⚠️  Error in data assessment: {e}")
            gaps = {}
        
        if not gaps:
            print(f"   ✅ All data present")
            return result
        
        print(f"   ⚠️  Missing: {', '.join(list(gaps.keys())[:5])}{'...' if len(gaps) > 5 else ''}")
        
        # 3. Generate search queries
        try:
            queries = self.generate_search_queries(operator, gaps)
        except Exception as e:
            print(f"   ⚠️  Error generating queries: {e}")
            queries = []
        
        # 4. Perform web research (simulated - would use actual search API)
        print(f"   🔎 Performing {len(queries)} web searches...")
        
        # Note: In production, this would call actual web search API
        # For now, we'll use the web_researcher but note it needs API integration
        research_data = {}
        
        for query in queries[:3]:  # Limit to 3 queries per operator for now
            try:
                print(f"      Query: {query}")
                
                # First, try to extract from existing files
                spec_paths = []
                if country:
                    spec_paths.append(self.base_path / 'Europe' / country / operator / 'specifications.md')
                    spec_paths.append(self.base_path / 'Europe' / country / operator / f'{operator}.md')
                spec_paths.append(self.base_path / 'Operators' / operator / f'{operator}.md')
                spec_paths.append(self.base_path / 'Operators' / operator / 'specifications.md')
                
                file_extracted = False
                for spec_path in spec_paths:
                    if spec_path and spec_path.exists():
                        content = spec_path.read_text(encoding='utf-8')
                        # Extract missing data from file
                        extracted = self.extract_data_from_web_result(
                            {'content': content, 'url': str(spec_path), 'title': spec_path.name},
                            operator,
                            gaps
                        )
                        if extracted:
                            research_data.update(extracted)
                            file_extracted = True
                            print(f"         ✅ Found data in file")
                        break
                
                # If file extraction didn't find everything, try web search with OpenAI
                if not file_extracted or len(research_data) < len(gaps):
                    try:
                        web_results = self.agent.researcher.search(query, max_results=3)
                        
                        # Use OpenAI to extract data from web results
                        if self.agent.researcher.openai_api_key:
                            from agents.research_data_engineer.extract_with_openai import OpenAIExtractor
                            openai_extractor = OpenAIExtractor(api_key=self.agent.researcher.openai_api_key)
                            
                            for web_result in web_results:
                                if web_result.get('source') != 'none' and web_result.get('content'):
                                    # Use OpenAI to extract structured data
                                    openai_data = openai_extractor.extract_operator_data(
                                        content=web_result.get('content', ''),
                                        operator=operator,
                                        query=query,
                                        data_points=list(gaps.keys())
                                    )
                                    
                                    # Convert OpenAI format to our format
                                    for attr, value in openai_data.items():
                                        if attr in gaps and attr not in research_data:
                                            research_data[attr] = {
                                                'value': value,
                                                'source_url': web_result.get('url', ''),
                                                'source_title': web_result.get('title', ''),
                                                'extraction_method': 'openai_extraction',
                                                'confidence': 0.8
                                            }
                                    
                                    if openai_data:
                                        print(f"         ✅ Extracted data with OpenAI from: {web_result.get('source', 'unknown')}")
                                        break
                        else:
                            # Fallback to regex extraction if no OpenAI
                            for web_result in web_results:
                                if web_result.get('source') != 'none':
                                    extracted = self.extract_data_from_web_result(web_result, operator, gaps)
                                    if extracted:
                                        research_data.update(extracted)
                                        print(f"         ✅ Found data from web: {web_result.get('source', 'unknown')}")
                                        break
                    except Exception as e:
                        print(f"         ⚠️  Web search error: {e}")
                
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"      ⚠️  Error: {e}")
        
        result['research_performed'] = research_data
        
        # 5. Store new data with sources
        if research_data:
            source_id = self.agent.db.add_source(
                source_type='web_search',
                source_path='operator_research_workflow',
                source_name=f'Operator research: {operator}',
                source_date=datetime.now().date().isoformat()
            )
            
            new_facts = 0
            existing_attrs = set(result['existing_data'].keys())
            
            for attr, data in research_data.items():
                if attr not in existing_attrs:
                    value = data['value']
                    value_type = 'number' if isinstance(value, (int, float)) else 'string'
                    
                    if attr == 'ca_systems' and isinstance(value, list):
                        value = json.dumps(value)
                        value_type = 'json'
                    
                    fact_id = self.agent.db.add_fact(
                        entity_type='operator',
                        entity_id=operator,
                        attribute=attr,
                        value=value,
                        value_type=value_type,
                        source_id=source_id,
                        confidence=data.get('confidence', 0.7),
                        extraction_method=data.get('extraction_method', 'web_search')
                    )
                    
                    # Add reference
                    if data.get('source_url'):
                        self.agent.db.add_reference(
                            fact_id=fact_id,
                            reference_type='url',
                            reference_url=data['source_url'],
                            reference_title=data.get('source_title')
                        )
                    
                    result['new_data_added'][attr] = value
                    new_facts += 1
            
            if new_facts > 0:
                print(f"   ✅ Added {new_facts} new facts")
                self.stats['facts_added'] += new_facts
            else:
                print(f"   ℹ️  No new data found")
        else:
            print(f"   ℹ️  No research data extracted")
        
        # 6. Validate existing data (optional - compare with web results)
        # This would compare existing data with web results and flag discrepancies
        # For now, just return the result
        
        try:
            # Ensure all keys exist
            if 'new_data_added' not in result:
                result['new_data_added'] = {}
            if 'validation_results' not in result:
                result['validation_results'] = {}
        except:
            pass
        
        return result
    
    def research_all_operators(self, limit: int = None):
        """Research all operators systematically"""
        print("=" * 70)
        print("OPERATOR RESEARCH WORKFLOW")
        print("=" * 70)
        
        # Get all operators from database
        all_facts = self.agent.db.get_facts(entity_type='operator', current_only=True)
        operators = set(f['entity_id'] for f in all_facts)
        
        print(f"\n📊 Found {len(operators)} operators in database")
        
        if limit:
            operators = list(operators)[:limit]
            print(f"   Limiting to first {limit} operators")
        
        # Research each operator
        for i, operator in enumerate(sorted(operators), 1):
            print(f"\n[{i}/{len(operators)}] Processing: {operator}")
            
            # Try to determine country from existing data or file structure
            country = None
            # Check if we can find country from file paths
            spec_files = list(self.base_path.glob(f'Europe/**/{operator}/specifications.md'))
            if spec_files:
                country = spec_files[0].parent.parent.name
            
            try:
                result = self.research_operator(operator, country)
                if result:  # Only append if result is valid
                    self.research_results.append(result)
                    self.stats['operators_researched'] += 1
            except Exception as e:
                import traceback
                print(f"   ❌ Error: {e}")
                print(f"   Traceback: {traceback.format_exc()[:200]}")
                self.stats['errors'] += 1
        
        # Summary
        print("\n" + "=" * 70)
        print("RESEARCH SUMMARY")
        print("=" * 70)
        print(f"Operators researched: {self.stats['operators_researched']}")
        print(f"New facts added: {self.stats['facts_added']}")
        print(f"Errors: {self.stats['errors']}")
        
        # Save results
        results_file = Path('operator_research_results.json')
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.research_results, f, indent=2, default=str, ensure_ascii=False)
        
        print(f"\n✅ Results saved to: {results_file}")
        
        return self.research_results


def main():
    """Main workflow execution"""
    import os
    
    agent = ResearchDataEngineer(db_path='research_data.db')
    
    # Get OpenAI API key from environment or command line
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key and len(sys.argv) > 2:
        openai_key = sys.argv[2]
    
    workflow = OperatorResearchWorkflow(agent, openai_api_key=openai_key)
    
    # Research all operators (or limit for testing)
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    workflow.research_all_operators(limit=limit)


if __name__ == '__main__':
    main()
