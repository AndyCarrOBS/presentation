#!/usr/bin/env python3
"""
OpenAI-powered data extraction for operator research
Uses OpenAI API to intelligently extract structured data from web content
"""
import os
import json
import requests
from typing import Dict, List, Optional


class OpenAIExtractor:
    """Extract structured data using OpenAI API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = 'https://api.openai.com/v1'
        
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
    
    def extract_operator_data(self, content: str, operator: str, query: str, 
                              data_points: List[str]) -> Dict:
        """
        Extract structured operator data from content using OpenAI
        
        Args:
            content: Text content to extract from
            operator: Operator name
            query: Original search query
            data_points: List of data points to extract (e.g., ['subscribers', 'hbbtv_version'])
        
        Returns:
            Dictionary with extracted data
        """
        # Limit content to avoid token limits
        content_preview = content[:6000] if len(content) > 6000 else content
        
        prompt = f"""Extract the following information about the TV operator "{operator}" from the provided content.

Original query: {query}
Data points to extract: {', '.join(data_points)}

Content:
{content_preview}

Extract the requested information and return as JSON with the following structure:
{{
  "subscribers": number or null,
  "hbbtv_version": string or null,
  "ci_version": string or null,
  "ca_systems": array of strings or null,
  "website": string or null,
  "developer_portal": string or null,
  "parent_company": string or null,
  "market_share_percent": number or null,
  "platform_type": string or null
}}

Instructions:
- Only include fields that are explicitly found in the content
- Return null for fields not found
- For subscribers: convert to number (e.g., "2.1 million" -> 2100000)
- For versions: extract version numbers (e.g., "HbbTV 2.0.1" -> "2.0.1")
- For CA systems: extract system names (e.g., ["Nagravision", "Irdeto"])
- For URLs: extract full URLs only
- Return only valid JSON, no additional text or explanation"""

        try:
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-4o-mini',  # Cost-efficient model
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a data extraction assistant. Extract structured data from text and return only valid JSON. Be precise and only extract information that is explicitly stated in the content.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': 0.1,
                    'response_format': {'type': 'json_object'}
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            content_text = data['choices'][0]['message']['content']
            extracted = json.loads(content_text)
            
            # Filter out null values and validate
            result = {}
            for k, v in extracted.items():
                if v is not None:
                    result[k] = v
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON decode error: {e}")
            return {}
        except Exception as e:
            print(f"⚠️  OpenAI extraction error: {e}")
            return {}
    
    def validate_and_enrich(self, existing_data: Dict, new_data: Dict) -> Dict:
        """
        Use OpenAI to validate and enrich data by comparing existing and new data
        
        Returns:
            Dictionary with validated/enriched data and confidence scores
        """
        if not existing_data and not new_data:
            return {}
        
        prompt = f"""Compare and validate operator data:

Existing data:
{json.dumps(existing_data, indent=2)}

New data found:
{json.dumps(new_data, indent=2)}

Provide a validated dataset with:
1. Most accurate values (prefer official sources)
2. Confidence scores (0.0-1.0) for each field
3. Source quality assessment

Return JSON:
{{
  "validated_data": {{...}},
  "confidence_scores": {{...}},
  "source_quality": "high|medium|low",
  "notes": "string"
}}"""

        try:
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-4o-mini',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a data validation assistant. Compare data sources and provide validated results with confidence scores.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': 0.1,
                    'response_format': {'type': 'json_object'}
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            content_text = data['choices'][0]['message']['content']
            return json.loads(content_text)
            
        except Exception as e:
            print(f"⚠️  Validation error: {e}")
            return {'validated_data': new_data, 'confidence_scores': {}}


if __name__ == '__main__':
    # Test extraction
    test_content = """
    KPN is a major telecommunications operator in the Netherlands.
    KPN has approximately 2.1 million TV subscribers.
    KPN supports HbbTV version 2.0.1.
    KPN uses Nagravision and Irdeto for conditional access.
    Visit KPN at https://www.kpn.com
    """
    
    extractor = OpenAIExtractor()
    result = extractor.extract_operator_data(
        content=test_content,
        operator='KPN',
        query='KPN subscribers HbbTV',
        data_points=['subscribers', 'hbbtv_version', 'ca_systems', 'website']
    )
    
    print("Extracted data:")
    print(json.dumps(result, indent=2))
