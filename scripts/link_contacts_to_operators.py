#!/usr/bin/env python3
"""
Link contacts to operators by normalizing operator names
This creates a mapping between contact operator names and specification operator names
"""
import json
import re
from pathlib import Path

def normalize_operator_name(name):
    """Normalize operator name for matching"""
    if not name:
        return ""
    # Remove extra text in parentheses
    name = re.sub(r'\s*\([^)]+\)', '', name)
    # Remove special characters, convert to lowercase
    normalized = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
    return normalized

def find_operator_match(contact_op_name, operator_names):
    """Find matching operator name from list"""
    contact_normalized = normalize_operator_name(contact_op_name)
    
    # Try exact match first
    for op_name in operator_names:
        if normalize_operator_name(op_name) == contact_normalized:
            return op_name
    
    # Try partial match
    for op_name in operator_names:
        op_normalized = normalize_operator_name(op_name)
        if contact_normalized in op_normalized or op_normalized in contact_normalized:
            return op_name
    
    # Try fuzzy match (check if key parts match)
    contact_parts = contact_normalized.split()
    for op_name in operator_names:
        op_normalized = normalize_operator_name(op_name)
        op_parts = op_normalized.split()
        # Check if significant parts match
        if len(contact_parts) > 0 and len(op_parts) > 0:
            if contact_parts[0] == op_parts[0] or (len(contact_parts) > 1 and contact_parts[0] in op_parts):
                return op_name
    
    return None

def link_contacts_to_operators(dashboard_data):
    """Link contacts to operators by normalizing names"""
    operators = dashboard_data.get('operators', {})
    contacts = dashboard_data.get('contacts', {})
    
    # Create a linked contacts structure
    linked_contacts = {}
    
    for country in contacts.keys():
        if country not in linked_contacts:
            linked_contacts[country] = {}
        
        country_contacts = contacts[country]
        country_operators = operators.get(country, {})
        operator_names = list(country_operators.keys())
        
        # Iterate through contact data keys (these are the operator names from contacts file)
        for contact_op_name, contact_data in country_contacts.items():
            # Find matching operator from the operators list
            matched_op = find_operator_match(contact_op_name, operator_names)
            
            if matched_op:
                # Flatten contacts if they're organized by role
                if isinstance(contact_data, dict):
                    # Extract all contacts from all roles
                    all_contacts = []
                    for role, role_contacts in contact_data.items():
                        if isinstance(role_contacts, list):
                            all_contacts.extend(role_contacts)
                        elif isinstance(role_contacts, dict):
                            # Handle nested structure
                            all_contacts.extend(role_contacts.values())
                    linked_contacts[country][matched_op] = all_contacts
                elif isinstance(contact_data, list):
                    linked_contacts[country][matched_op] = contact_data
            else:
                # No match found - try to add with original name for debugging
                print(f"⚠️  No match found for '{contact_op_name}' in {country}")
    
    return linked_contacts

def main():
    """Main function to link contacts and update dashboard data"""
    print("Linking contacts to operators...")
    
    # Load dashboard data
    with open('dashboard_data.json', 'r') as f:
        dashboard_data = json.load(f)
    
    # Link contacts
    linked_contacts = link_contacts_to_operators(dashboard_data)
    
    # Update dashboard data
    dashboard_data['contacts'] = linked_contacts
    
    # Save updated data
    with open('dashboard_data.json', 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Contacts linked to operators")
    
    # Show sample
    if 'Austria' in linked_contacts:
        print("\nAustria linked contacts:")
        for op, contacts in linked_contacts['Austria'].items():
            print(f"  {op}: {len(contacts)} contacts")

if __name__ == '__main__':
    main()

