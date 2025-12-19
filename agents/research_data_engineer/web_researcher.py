#!/usr/bin/env python3
"""
Web research capabilities for the Research Data Engineer Agent
Fetches external data points and validates information from the internet
Uses OpenAI API for intelligent data extraction and analysis
"""
import requests
from typing import List, Dict, Optional
from urllib.parse import urlparse
import time
import os
import json


class WebResearcher:
    """Handles web research and external data fetching using OpenAI API"""
    
    def __init__(self, timeout: int = 10, openai_api_key: str = None):
        """Initialize web researcher"""
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; ResearchDataEngineer/1.0)'
        })
        
        # OpenAI API setup
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.openai_base_url = 'https://api.openai.com/v1'
        
        if self.openai_api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.openai_api_key}'
            })
    
    def _extract_with_openai(self, content: str, query: str, operator: str, data_points: List[str]) -> Dict:
        """Use OpenAI to extract structured data from content"""
        if not self.openai_api_key:
            return {}
        
        try:
            # Create a prompt for OpenAI to extract specific data points
            prompt = f"""Extract the following information about the TV operator "{operator}" from the provided content.

Query: {query}
Data points to extract: {', '.join(data_points)}

Content:
{content[:4000]}  # Limit content to avoid token limits

Extract the requested information and return as JSON with the following structure:
{{
  "subscribers": number or null,
  "hbbtv_version": string or null,
  "ci_version": string or null,
  "ca_systems": array of strings or null,
  "website": string or null,
  "developer_portal": string or null,
  "parent_company": string or null,
  "market_share_percent": number or null
}}

Only include fields that are found in the content. Return null for fields not found.
Return only valid JSON, no additional text."""

            response = self.session.post(
                f'{self.openai_base_url}/chat/completions',
                json={
                    'model': 'gpt-4o-mini',  # Using mini for cost efficiency
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a data extraction assistant. Extract structured data from text and return only valid JSON.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': 0.1,
                    'response_format': {'type': 'json_object'}
                },
                timeout=self.timeout * 2
            )
            response.raise_for_status()
            data = response.json()
            
            content_text = data['choices'][0]['message']['content']
            extracted = json.loads(content_text)
            
            # Filter out null values
            return {k: v for k, v in extracted.items() if v is not None}
            
        except Exception as e:
            # If OpenAI fails, return empty dict
            return {}
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search the web for information using DuckDuckGo (free)
        Then use OpenAI to extract structured data from results
        """
        results = []
        
        # Try using duckduckgo-search library if available
        try:
            from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                search_results = list(ddgs.text(query, max_results=max_results))
                
                for item in search_results:
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('href', ''),
                        'snippet': item.get('body', ''),
                        'content': item.get('body', ''),
                        'source': 'duckduckgo'
                    })
                
                if results:
                    # Fetch full content for OpenAI extraction
                    if self.openai_api_key:
                        for result in results[:max_results]:
                            if result.get('url') and result['url'].startswith('http'):
                                try:
                                    page_response = self.session.get(
                                        result['url'],
                                        timeout=self.timeout,
                                        allow_redirects=True,
                                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                                    )
                                    page_response.raise_for_status()
                                    
                                    # Extract text content
                                    import re
                                    from html import unescape
                                    
                                    # Remove script and style tags
                                    text = re.sub(r'<script[^>]*>.*?</script>', '', page_response.text, flags=re.DOTALL | re.IGNORECASE)
                                    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
                                    
                                    # Remove HTML tags
                                    text_content = re.sub(r'<[^>]+>', ' ', text)
                                    text_content = unescape(text_content)
                                    
                                    # Clean up whitespace and limit
                                    text_content = ' '.join(text_content.split()[:2000])
                                    
                                    result['content'] = text_content
                                    result['snippet'] = text_content[:500] if text_content else result.get('snippet', '')
                                except Exception as e:
                                    pass  # Keep snippet if fetch fails
                    
                    return results
        except ImportError:
            # Library not installed, fall back to manual search
            pass
        except Exception as e:
            # If library search fails, fall back
            pass
        
        # Fallback: Use DuckDuckGo API
        try:
            # Use DuckDuckGo instant answer API
            ddg_response = self.session.get(
                'https://api.duckduckgo.com/',
                params={
                    'q': query,
                    'format': 'json',
                    'no_html': '1',
                    'skip_disambig': '1'
                },
                timeout=self.timeout
            )
            ddg_response.raise_for_status()
            ddg_data = ddg_response.json()
            
            # Get related topics for more URLs
            if ddg_data.get('RelatedTopics'):
                for topic in ddg_data['RelatedTopics'][:max_results]:
                    if isinstance(topic, dict) and 'FirstURL' in topic:
                        results.append({
                            'title': topic.get('Text', '').split(' - ')[0] if ' - ' in topic.get('Text', '') else topic.get('Text', ''),
                            'url': topic.get('FirstURL', ''),
                            'snippet': topic.get('Text', ''),
                            'content': topic.get('Text', ''),
                            'source': 'duckduckgo'
                        })
        except Exception as e:
            pass
        
        # If we have OpenAI, also try Wikipedia for reliable information
        if self.openai_api_key:
            # Try Wikipedia for operator information
            wiki_query = query.split()[0]  # Use first word (operator name) for Wikipedia
            wiki_result = self.get_wikipedia_summary(wiki_query)
            if wiki_result:
                results.insert(0, {
                    'title': wiki_result.get('title', ''),
                    'url': wiki_result.get('url', ''),
                    'snippet': wiki_result.get('extract', '')[:500],
                    'content': wiki_result.get('extract', ''),
                    'source': 'wikipedia'
                })
        
        # If we have OpenAI, fetch and extract from URLs
        if self.openai_api_key and results:
            for result in results[:max_results]:
                if result.get('url') and result['url'].startswith('http') and not result.get('content'):
                    try:
                        # Fetch full content
                        page_response = self.session.get(
                            result['url'],
                            timeout=self.timeout,
                            allow_redirects=True,
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                        )
                        page_response.raise_for_status()
                        
                        # Extract text content (simple - remove HTML tags)
                        import re
                        from html import unescape
                        
                        # Remove script and style tags
                        text = re.sub(r'<script[^>]*>.*?</script>', '', page_response.text, flags=re.DOTALL | re.IGNORECASE)
                        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
                        
                        # Remove HTML tags
                        text_content = re.sub(r'<[^>]+>', ' ', text)
                        text_content = unescape(text_content)
                        
                        # Clean up whitespace and limit
                        text_content = ' '.join(text_content.split()[:2000])  # Limit to 2000 words
                        
                        result['content'] = text_content
                        result['snippet'] = text_content[:500] if text_content else result.get('snippet', '')
                    except Exception as e:
                        # If fetch fails, keep snippet if available
                        pass
        
        # If no results, return placeholder
        if not results:
            results.append({
                'title': f'Search results for: {query}',
                'url': f'https://duckduckgo.com/?q={query}',
                'snippet': 'Use OpenAI to extract data from search results',
                'content': '',
                'source': 'duckduckgo'
            })
        
        return results
    
    def fetch_url(self, url: str) -> Optional[Dict]:
        """Fetch content from a URL"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            return {
                'url': url,
                'status_code': response.status_code,
                'content_type': response.headers.get('Content-Type'),
                'content_length': len(response.content),
                'title': self._extract_title(response.text),
                'fetched_at': time.time()
            }
        except requests.RequestException as e:
            return {
                'url': url,
                'error': str(e),
                'fetched_at': time.time()
            }
    
    def _extract_title(self, html: str) -> Optional[str]:
        """Extract title from HTML"""
        import re
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def validate_url(self, url: str) -> bool:
        """Validate that a URL is accessible"""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            response = self.session.head(url, timeout=5, allow_redirects=True)
            return response.status_code == 200
        except:
            return False
    
    def extract_data_from_url(self, url: str, patterns: Dict[str, str] = None) -> Dict:
        """
        Extract structured data from a URL using regex patterns
        patterns: dict mapping attribute names to regex patterns
        """
        result = self.fetch_url(url)
        if 'error' in result:
            return result
        
        extracted = {'url': url}
        
        if patterns:
            # This would parse the HTML/text and extract data
            # For now, just return the basic fetch result
            pass
        
        return extracted
    
    def get_wikipedia_summary(self, topic: str) -> Optional[Dict]:
        """Get Wikipedia summary for a topic"""
        # Wikipedia API endpoint
        api_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(' ', '_')
        
        try:
            response = self.session.get(api_url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            return {
                'title': data.get('title'),
                'extract': data.get('extract'),
                'url': data.get('content_urls', {}).get('desktop', {}).get('page'),
                'source': 'wikipedia'
            }
        except requests.RequestException:
            return None
    
    def check_data_freshness(self, url: str) -> Optional[Dict]:
        """Check when data at a URL was last updated"""
        try:
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            
            last_modified = response.headers.get('Last-Modified')
            etag = response.headers.get('ETag')
            
            return {
                'url': url,
                'last_modified': last_modified,
                'etag': etag,
                'status_code': response.status_code
            }
        except requests.RequestException:
            return None
