#!/usr/bin/env python3
"""
Research Data Engineer Agent
A senior research data engineer that extracts, cleans, validates, and stores facts
with source tracking, external data enrichment, and citation management.
"""
import re
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import requests
from urllib.parse import urlparse

from .database import ResearchDatabase
from .data_cleaner import DataCleaner
from .web_researcher import WebResearcher


class ResearchDataEngineer:
    """Senior Research Data Engineer Agent"""
    
    def __init__(self, db_path: str = "research_data.db"):
        """Initialize the agent with database and tools"""
        self.db = ResearchDatabase(db_path)
        self.cleaner = DataCleaner()
        self.researcher = WebResearcher()
        
    def extract_facts_from_markdown(self, file_path: str, 
                                    source_name: str = None) -> List[Dict]:
        """Extract structured facts from markdown files"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Register source
        source_id = self.db.add_source(
            source_type='file',
            source_path=str(file_path),
            source_name=source_name or file_path.name,
            source_date=datetime.fromtimestamp(file_path.stat().st_mtime).date().isoformat()
        )
        
        content = file_path.read_text(encoding='utf-8')
        facts = []
        
        # Extract based on file type/location
        if 'specifications.md' in str(file_path):
            facts.extend(self._extract_specification_facts(content, file_path, source_id))
        elif 'demographics.md' in str(file_path):
            facts.extend(self._extract_demographic_facts(content, file_path, source_id))
        elif 'contacts' in str(file_path).lower():
            facts.extend(self._extract_contact_facts(content, file_path, source_id))
        else:
            # Generic extraction
            facts.extend(self._extract_generic_facts(content, file_path, source_id))
        
        return facts
    
    def _extract_specification_facts(self, content: str, file_path: Path, source_id: int) -> List[Dict]:
        """Extract facts from specification markdown files"""
        facts = []
        
        # Extract country and operator
        country_match = re.search(r'\*\*Country\*\*:\s*(.+)', content)
        operator_match = re.search(r'\*\*Operator\*\*:\s*(.+)', content)
        
        country = country_match.group(1).strip() if country_match else None
        operator = operator_match.group(1).strip() if operator_match else None
        
        if not country or not operator:
            # Try to infer from path
            path_parts = file_path.parts
            if 'Europe' in path_parts:
                idx = path_parts.index('Europe')
                if idx + 1 < len(path_parts):
                    country = path_parts[idx + 1]
                if idx + 2 < len(path_parts):
                    operator = path_parts[idx + 2]
        
        # Extract HbbTV version
        hbbtv_match = re.search(r'HbbTV[:\s]+([\d.]+)', content, re.IGNORECASE)
        if hbbtv_match:
            version = hbbtv_match.group(1)
            fact_id = self.db.add_fact(
                entity_type='operator',
                entity_id=operator,
                attribute='hbbtv_version',
                value=version,
                value_type='string',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts.append({'fact_id': fact_id, 'type': 'hbbtv_version'})
        
        # Extract CI+ version
        ci_match = re.search(r'CI\+[:\s]+([\d.]+)', content, re.IGNORECASE)
        if ci_match:
            version = ci_match.group(1)
            fact_id = self.db.add_fact(
                entity_type='operator',
                entity_id=operator,
                attribute='ci_version',
                value=version,
                value_type='string',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts.append({'fact_id': fact_id, 'type': 'ci_version'})
        
        # Extract specification status
        spec_status_match = re.search(r'\*\*Status\*\*:\s*(.+)', content)
        if spec_status_match:
            status = spec_status_match.group(1).strip()
            has_spec = 'available' in status.lower() or 'verified' in status.lower()
            fact_id = self.db.add_fact(
                entity_type='operator',
                entity_id=operator,
                attribute='has_specification',
                value=has_spec,
                value_type='boolean',
                source_id=source_id,
                extraction_method='regex_pattern'
            )
            facts.append({'fact_id': fact_id, 'type': 'has_specification'})
        
        # Extract URLs
        url_pattern = r'https?://[^\s\)]+'
        urls = re.findall(url_pattern, content)
        for url in urls:
            if any(domain in url for domain in ['hbbtv.org', 'ci-plus.com', 'developer']):
                fact_id = self.db.add_fact(
                    entity_type='operator',
                    entity_id=operator,
                    attribute='specification_url',
                    value=url,
                    value_type='string',
                    source_id=source_id,
                    extraction_method='url_extraction'
                )
                self.db.add_reference(
                    fact_id=fact_id,
                    reference_type='url',
                    reference_url=url
                )
                facts.append({'fact_id': fact_id, 'type': 'url'})
        
        return facts
    
    def _extract_demographic_facts(self, content: str, file_path: Path, source_id: int) -> List[Dict]:
        """Extract demographic facts from markdown files"""
        facts = []
        
        # Extract country from path
        path_parts = file_path.parts
        if 'Europe' in path_parts:
            idx = path_parts.index('Europe')
            if idx + 1 < len(path_parts):
                country = path_parts[idx + 1]
            else:
                return facts
        else:
            return facts
        
        # Extract population - try multiple patterns
        # Pattern 1: Population in millions
        pop_match = re.search(r'Total population[:\s]+~?([\d.]+)\s*million', content, re.IGNORECASE)
        if not pop_match:
            pop_match = re.search(r'\*\*Total population\*\*[:\s]+~?([\d.]+)\s*million', content, re.IGNORECASE)
        
        # Pattern 2: Population in thousands (convert to millions)
        if not pop_match:
            pop_match_thousands = re.search(r'\*\*Total population\*\*[:\s]+~?([\d,]+)', content, re.IGNORECASE)
            if not pop_match_thousands:
                pop_match_thousands = re.search(r'Total population[:\s]+~?([\d,]+)', content, re.IGNORECASE)
            
            if pop_match_thousands:
                # Remove commas and convert to millions
                pop_str = pop_match_thousands.group(1).replace(',', '')
                pop_value = float(pop_str) / 1000000.0
                # Only use if it's less than 10 (likely thousands, not already millions)
                if pop_value < 10:
                    fact_id = self.db.add_fact(
                        entity_type='country',
                        entity_id=country,
                        attribute='population_million',
                        value=round(pop_value, 3),
                        value_type='number',
                        unit='million',
                        source_id=source_id,
                        extraction_method='regex_pattern_thousands'
                    )
                    facts.append({'fact_id': fact_id, 'type': 'population'})
                    pop_match = None  # Mark as processed
                else:
                    pop_match = pop_match_thousands  # Use as-is if already in millions
        
        if pop_match:
            try:
                population = float(pop_match.group(1))
                fact_id = self.db.add_fact(
                    entity_type='country',
                    entity_id=country,
                    attribute='population_million',
                    value=population,
                    value_type='number',
                    unit='million',
                    source_id=source_id,
                    extraction_method='regex_pattern'
                )
                facts.append({'fact_id': fact_id, 'type': 'population'})
            except (ValueError, Exception) as e:
                pass  # Skip if extraction fails
        
        # Extract TV homes - try multiple patterns
        # Pattern 1: TV homes in millions
        tv_match = re.search(r'\*\*Total TV households\*\*[:\s]+~?([\d.]+)\s*million', content, re.IGNORECASE)
        if not tv_match:
            tv_match = re.search(r'Total TV households[:\s]+~?([\d.]+)\s*million', content, re.IGNORECASE)
        if not tv_match:
            tv_match = re.search(r'TV\s+households[:\s]+~?([\d.]+)\s*million', content, re.IGNORECASE)
        
        # Pattern 2: TV homes in thousands (convert to millions)
        if not tv_match:
            tv_match_thousands = re.search(r'\*\*Total TV households\*\*[:\s]+~?([\d,]+)', content, re.IGNORECASE)
            if not tv_match_thousands:
                tv_match_thousands = re.search(r'Total TV households[:\s]+~?([\d,]+)', content, re.IGNORECASE)
            
            if tv_match_thousands:
                # Remove commas and convert to millions
                tv_str = tv_match_thousands.group(1).replace(',', '')
                tv_value = float(tv_str) / 1000000.0
                # Only use if it's less than 100 (likely thousands, not already millions)
                if tv_value < 100:
                    fact_id = self.db.add_fact(
                        entity_type='country',
                        entity_id=country,
                        attribute='tv_homes_million',
                        value=round(tv_value, 3),
                        value_type='number',
                        unit='million',
                        source_id=source_id,
                        extraction_method='regex_pattern_thousands'
                    )
                    facts.append({'fact_id': fact_id, 'type': 'tv_homes'})
                    tv_match = None  # Mark as processed
        
        if tv_match:
            try:
                tv_homes = float(tv_match.group(1))
                fact_id = self.db.add_fact(
                    entity_type='country',
                    entity_id=country,
                    attribute='tv_homes_million',
                    value=tv_homes,
                    value_type='number',
                    unit='million',
                    source_id=source_id,
                    extraction_method='regex_pattern'
                )
                facts.append({'fact_id': fact_id, 'type': 'tv_homes'})
            except (ValueError, Exception) as e:
                pass  # Skip if extraction fails
        
        # Extract GDP - try multiple patterns
        gdp_match = re.search(r'\*\*GDP\s*\(total\)\*\*[:\s]+~?€?([\d.]+)\s*billion', content, re.IGNORECASE)
        if not gdp_match:
            gdp_match = re.search(r'GDP\s*\(total\)[:\s]+~?€?([\d.]+)\s*billion', content, re.IGNORECASE)
        if not gdp_match:
            gdp_match = re.search(r'GDP[:\s]+~?€?([\d.]+)\s*billion', content, re.IGNORECASE)
        
        if gdp_match:
            try:
                gdp = float(gdp_match.group(1))
                fact_id = self.db.add_fact(
                    entity_type='country',
                    entity_id=country,
                    attribute='gdp_billion_eur',
                    value=gdp,
                    value_type='number',
                    unit='billion_eur',
                    source_id=source_id,
                    extraction_method='regex_pattern'
                )
                facts.append({'fact_id': fact_id, 'type': 'gdp'})
            except (ValueError, Exception) as e:
                pass  # Skip if extraction fails
        
        return facts
    
    def _extract_contact_facts(self, content: str, file_path: Path, source_id: int) -> List[Dict]:
        """Extract contact information facts"""
        facts = []
        # Implementation for contact extraction
        # This would parse contact markdown files
        return facts
    
    def _extract_generic_facts(self, content: str, file_path: Path, source_id: int) -> List[Dict]:
        """Generic fact extraction for unknown markdown formats"""
        facts = []
        # Extract key-value pairs, lists, etc.
        return facts
    
    def extract_facts_from_json(self, file_path: str, source_name: str = None) -> List[Dict]:
        """Extract facts from JSON files"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        source_id = self.db.add_source(
            source_type='file',
            source_path=str(file_path),
            source_name=source_name or file_path.name,
            source_date=datetime.fromtimestamp(file_path.stat().st_mtime).date().isoformat()
        )
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        facts = []
        
        # Extract from dashboard_data.json structure
        if 'countries' in data:
            for country, country_data in data['countries'].items():
                # Population
                if 'population_million' in country_data and country_data['population_million']:
                    fact_id = self.db.add_fact(
                        entity_type='country',
                        entity_id=country,
                        attribute='population_million',
                        value=float(country_data['population_million']),
                        value_type='number',
                        unit='million',
                        source_id=source_id,
                        extraction_method='json_extraction'
                    )
                    facts.append({'fact_id': fact_id})
                
                # TV homes
                if 'tv_homes_million' in country_data and country_data['tv_homes_million']:
                    fact_id = self.db.add_fact(
                        entity_type='country',
                        entity_id=country,
                        attribute='tv_homes_million',
                        value=float(country_data['tv_homes_million']),
                        value_type='number',
                        unit='million',
                        source_id=source_id,
                        extraction_method='json_extraction'
                    )
                    facts.append({'fact_id': fact_id})
        
        if 'operators' in data:
            for country, operators in data['operators'].items():
                for operator, op_data in operators.items():
                    # HbbTV version
                    if 'hbbtv_version' in op_data and op_data['hbbtv_version']:
                        fact_id = self.db.add_fact(
                            entity_type='operator',
                            entity_id=operator,
                            attribute='hbbtv_version',
                            value=op_data['hbbtv_version'],
                            value_type='string',
                            source_id=source_id,
                            extraction_method='json_extraction'
                        )
                        facts.append({'fact_id': fact_id})
                    
                    # CI version
                    if 'ci_version' in op_data and op_data['ci_version']:
                        fact_id = self.db.add_fact(
                            entity_type='operator',
                            entity_id=operator,
                            attribute='ci_version',
                            value=op_data['ci_version'],
                            value_type='string',
                            source_id=source_id,
                            extraction_method='json_extraction'
                        )
                        facts.append({'fact_id': fact_id})
        
        return facts
    
    def enrich_with_external_data(self, entity_type: str, entity_id: str, 
                                  attribute: str, search_queries: List[str] = None):
        """Enrich facts with external data from web research"""
        facts = self.db.get_facts(
            entity_type=entity_type,
            entity_id=entity_id,
            attribute=attribute
        )
        
        if not facts:
            return []
        
        fact = facts[0]  # Get most recent
        
        # Generate search queries if not provided
        if not search_queries:
            search_queries = [
                f"{entity_id} {attribute}",
                f"{entity_type} {entity_id} {attribute} statistics"
            ]
        
        enriched_data = []
        for query in search_queries:
            results = self.researcher.search(query)
            for result in results:
                # Store external data point
                self.db.add_external_data(
                    fact_id=fact['id'],
                    external_source='web_search',
                    external_url=result.get('url'),
                    data_snapshot=result
                )
                
                # Add as reference
                self.db.add_reference(
                    fact_id=fact['id'],
                    reference_type='url',
                    reference_url=result.get('url'),
                    reference_title=result.get('title')
                )
                
                enriched_data.append(result)
        
        return enriched_data
    
    def validate_and_clean_fact(self, fact_id: int) -> Dict:
        """Validate and clean a fact, updating quality scores"""
        fact = self.db.get_fact_with_sources(fact_id)
        if not fact:
            return None
        
        # Clean the value
        cleaned_value = self.cleaner.clean_value(
            fact['value'],
            fact['value_type']
        )
        
        # Calculate quality scores
        completeness = self._calculate_completeness(fact)
        accuracy = self._calculate_accuracy(fact)
        freshness = self._calculate_freshness(fact)
        
        # Update fact if value changed
        if cleaned_value != fact['value']:
            # Create new fact version with cleaned value
            new_fact_id = self.db.add_fact(
                entity_type=fact['entity_type'],
                entity_id=fact['entity_id'],
                attribute=fact['attribute'],
                value=cleaned_value,
                value_type=fact['value_type'],
                unit=fact['unit'],
                source_id=fact['sources'][0]['id'] if fact['sources'] else None
            )
            fact['id'] = new_fact_id
        
        return {
            'fact_id': fact['id'],
            'completeness': completeness,
            'accuracy': accuracy,
            'freshness': freshness,
            'cleaned_value': cleaned_value
        }
    
    def _calculate_completeness(self, fact: Dict) -> float:
        """Calculate completeness score (0.0 to 1.0)"""
        score = 0.5  # Base score
        
        # More sources = higher completeness
        if fact.get('sources'):
            score += min(len(fact['sources']) * 0.1, 0.3)
        
        # Has external data = higher completeness
        if fact.get('external_data'):
            score += 0.1
        
        # Has references = higher completeness
        if fact.get('references'):
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_accuracy(self, fact: Dict) -> float:
        """Calculate accuracy score based on source quality"""
        if not fact.get('sources'):
            return 0.5
        
        # Average confidence scores
        confidences = [s.get('confidence_score', 0.5) for s in fact['sources']]
        return sum(confidences) / len(confidences) if confidences else 0.5
    
    def _calculate_freshness(self, fact: Dict) -> float:
        """Calculate freshness score based on data age"""
        if not fact.get('sources'):
            return 0.5
        
        # Check most recent source date
        dates = []
        for source in fact['sources']:
            if source.get('source_date'):
                dates.append(datetime.fromisoformat(source['source_date']).date())
        
        if dates:
            most_recent = max(dates)
            days_old = (datetime.now().date() - most_recent).days
            
            # Score decreases with age
            if days_old < 30:
                return 1.0
            elif days_old < 90:
                return 0.8
            elif days_old < 180:
                return 0.6
            elif days_old < 365:
                return 0.4
            else:
                return 0.2
        
        return 0.5
    
    def generate_dashboard_data(self, filters: Dict = None) -> Dict:
        """Generate dashboard data from the database"""
        filters = filters or {}
        
        # Get all countries
        countries = self.db.get_facts(entity_type='country', current_only=True)
        
        dashboard = {
            'countries': {},
            'operators': {},
            'statistics': {
                'total_countries': 0,
                'total_operators': 0,
                'total_facts': 0,
                'data_quality_avg': 0.0
            }
        }
        
        # Group facts by entity
        country_data = {}
        operator_data = {}
        
        for fact in countries:
            country = fact['entity_id']
            if country not in country_data:
                country_data[country] = {}
            country_data[country][fact['attribute']] = fact['value']
        
        operators = self.db.get_facts(entity_type='operator', current_only=True)
        for fact in operators:
            operator = fact['entity_id']
            country = self._get_operator_country(operator)
            if country not in operator_data:
                operator_data[country] = {}
            if operator not in operator_data[country]:
                operator_data[country][operator] = {}
            operator_data[country][operator][fact['attribute']] = fact['value']
        
        dashboard['countries'] = country_data
        dashboard['operators'] = operator_data
        dashboard['statistics']['total_countries'] = len(country_data)
        dashboard['statistics']['total_operators'] = sum(len(ops) for ops in operator_data.values())
        dashboard['statistics']['total_facts'] = len(countries) + len(operators)
        
        return dashboard
    
    def _get_operator_country(self, operator: str) -> str:
        """Try to determine country from operator name or database"""
        # This could be enhanced with a lookup table
        # For now, return None and let it be handled elsewhere
        return None
    
    def get_trend_analysis(self, entity_type: str, entity_id: str, 
                           attribute: str) -> Dict:
        """Get trend analysis for a specific data point"""
        trend_data = self.db.get_trend_data(entity_type, entity_id, attribute)
        
        if not trend_data:
            return None
        
        # Calculate trends
        values = []
        dates = []
        
        for point in trend_data:
            try:
                if point['value_type'] == 'number':
                    values.append(float(point['value']))
                else:
                    values.append(point['value'])
                dates.append(point['created_at'])
            except (ValueError, TypeError):
                continue
        
        analysis = {
            'entity_type': entity_type,
            'entity_id': entity_id,
            'attribute': attribute,
            'data_points': len(trend_data),
            'first_recorded': dates[0] if dates else None,
            'last_recorded': dates[-1] if dates else None,
            'current_value': values[-1] if values else None,
            'trend': 'stable'  # Could calculate actual trend
        }
        
        # Calculate trend direction if numeric
        if len(values) >= 2 and all(isinstance(v, (int, float)) for v in values):
            if values[-1] > values[0]:
                analysis['trend'] = 'increasing'
            elif values[-1] < values[0]:
                analysis['trend'] = 'decreasing'
        
        return analysis
