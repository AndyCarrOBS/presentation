#!/usr/bin/env python3
"""
Data cleaning and validation utilities for the Research Data Engineer Agent
"""
import re
from typing import Any, Optional
from datetime import datetime


class DataCleaner:
    """Cleans and validates data values"""
    
    def clean_value(self, value: Any, value_type: str) -> Any:
        """Clean a value based on its type"""
        if value is None:
            return None
        
        if value_type == 'string':
            return self._clean_string(value)
        elif value_type == 'number':
            return self._clean_number(value)
        elif value_type == 'boolean':
            return self._clean_boolean(value)
        elif value_type == 'date':
            return self._clean_date(value)
        else:
            return str(value).strip()
    
    def _clean_string(self, value: Any) -> str:
        """Clean string values"""
        if isinstance(value, str):
            # Remove extra whitespace
            cleaned = ' '.join(value.split())
            # Remove common markdown artifacts
            cleaned = cleaned.replace('**', '').replace('*', '').replace('`', '')
            # Remove leading/trailing punctuation artifacts
            cleaned = cleaned.strip('.,;:')
            return cleaned
        return str(value).strip()
    
    def _clean_number(self, value: Any) -> float:
        """Clean numeric values"""
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            # Remove common formatting
            cleaned = value.replace(',', '').replace(' ', '')
            # Remove currency symbols
            cleaned = re.sub(r'[€$£¥]', '', cleaned)
            # Remove units (million, billion, etc.)
            cleaned = re.sub(r'\s*(million|billion|thousand|k|m|b)\s*', '', cleaned, flags=re.IGNORECASE)
            # Extract number
            match = re.search(r'([\d.]+)', cleaned)
            if match:
                return float(match.group(1))
        
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def _clean_boolean(self, value: Any) -> bool:
        """Clean boolean values"""
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            value_lower = value.lower().strip()
            if value_lower in ('true', 'yes', '1', 'available', 'verified', '✅'):
                return True
            elif value_lower in ('false', 'no', '0', 'unavailable', 'unverified', '❌'):
                return False
        
        return bool(value)
    
    def _clean_date(self, value: Any) -> Optional[str]:
        """Clean date values"""
        if isinstance(value, datetime):
            return value.isoformat()
        
        if isinstance(value, str):
            # Try common date formats
            date_formats = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%m/%d/%Y',
                '%Y-%m-%d %H:%M:%S',
                '%d %B %Y',
                '%B %d, %Y'
            ]
            
            for fmt in date_formats:
                try:
                    dt = datetime.strptime(value.strip(), fmt)
                    return dt.date().isoformat()
                except ValueError:
                    continue
        
        return None
    
    def validate_value(self, value: Any, value_type: str, constraints: dict = None) -> tuple:
        """Validate a value against type and constraints"""
        constraints = constraints or {}
        
        # Type validation
        if value_type == 'number':
            if not isinstance(value, (int, float)):
                try:
                    float(value)
                except (ValueError, TypeError):
                    return False, f"Value '{value}' is not a valid number"
            
            # Range constraints
            if 'min' in constraints and value < constraints['min']:
                return False, f"Value {value} is below minimum {constraints['min']}"
            if 'max' in constraints and value > constraints['max']:
                return False, f"Value {value} is above maximum {constraints['max']}"
        
        elif value_type == 'string':
            if not isinstance(value, str):
                return False, f"Value '{value}' is not a string"
            
            # Length constraints
            if 'min_length' in constraints and len(value) < constraints['min_length']:
                return False, f"String length {len(value)} is below minimum {constraints['min_length']}"
            if 'max_length' in constraints and len(value) > constraints['max_length']:
                return False, f"String length {len(value)} is above maximum {constraints['max_length']}"
        
        elif value_type == 'boolean':
            if not isinstance(value, bool):
                return False, f"Value '{value}' is not a boolean"
        
        return True, None
    
    def normalize_entity_id(self, entity_id: str) -> str:
        """Normalize entity IDs for consistency"""
        if not entity_id:
            return ""
        
        # Remove extra whitespace
        normalized = ' '.join(entity_id.split())
        
        # Standardize common variations
        replacements = {
            'CI+': 'CI Plus',
            'HbbTV': 'HbbTV',
            'TV': 'TV',
        }
        
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        return normalized.strip()
