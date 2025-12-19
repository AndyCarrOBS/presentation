#!/usr/bin/env python3
"""
Analyze what data we have vs what we're extracting
"""
import json
from pathlib import Path

def analyze_current_extraction():
    """Analyze what we're currently extracting"""
    data_file = Path('dashboard_data.json')
    if not data_file.exists():
        print("❌ dashboard_data.json not found. Run extract_dashboard_data.py first.")
        return
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    print("=" * 80)
    print("CURRENT DATA EXTRACTION ANALYSIS")
    print("=" * 80)
    
    # Analyze countries
    countries = data.get('countries', {})
    print(f"\n📊 Countries: {len(countries)}")
    
    # Sample country
    sample_country = list(countries.keys())[0] if countries else None
    if sample_country:
        print(f"\n📋 Sample Country ({sample_country}):")
        sample = countries[sample_country]
        print(f"   - PSBs: {len(sample.get('psb', []))}")
        print(f"   - Operators: {len(sample.get('operators', []))}")
        print(f"   - Free-to-Air data: {bool(sample.get('free_to_air', {}))}")
    
    # Analyze operators
    operators = data.get('operators', {})
    total_operators = sum(len(ops) for ops in operators.values())
    print(f"\n📊 Operators: {total_operators}")
    
    # Sample operator
    sample_country_ops = list(operators.keys())[0] if operators else None
    if sample_country_ops:
        sample_ops = operators[sample_country_ops]
        sample_op_name = list(sample_ops.keys())[0] if sample_ops else None
        if sample_op_name:
            sample_op = sample_ops[sample_op_name]
            print(f"\n📋 Sample Operator ({sample_op_name}):")
            print(f"   - HbbTV Version: {sample_op.get('hbbtv_version', 'N/A')}")
            print(f"   - CI+ Version: {sample_op.get('ci_version', 'N/A')}")
            print(f"   - Has Specification: {sample_op.get('has_specification', False)}")
            print(f"   - Has Test Material: {sample_op.get('has_test_material', False)}")
            print(f"   - Has Gated Process: {sample_op.get('has_gated_process', False)}")
            print(f"   - Has Whitelist: {sample_op.get('has_whitelist', False)}")
            print(f"   - Has Branding: {sample_op.get('has_branding_agreement', False)}")
    
    # Analyze contacts
    contacts = data.get('contacts', {})
    total_contacts = sum(len(contact_list) for country_contacts in contacts.values() for contact_list in country_contacts.values())
    print(f"\n📊 Contacts: {total_contacts}")
    
    # Sample contact
    sample_country_contacts = list(contacts.keys())[0] if contacts else None
    if sample_country_contacts:
        sample_contacts = contacts[sample_country_contacts]
        sample_op_contacts = list(sample_contacts.keys())[0] if sample_contacts else None
        if sample_op_contacts:
            sample_contact_list = sample_contacts[sample_op_contacts]
            if sample_contact_list:
                sample_contact = sample_contact_list[0]
                print(f"\n📋 Sample Contact:")
                print(f"   - Name: {sample_contact.get('name', 'N/A')}")
                print(f"   - Title: {sample_contact.get('title', 'N/A')}")
                print(f"   - Email: {sample_contact.get('email', 'N/A')}")
                print(f"   - Phone: {sample_contact.get('phone', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("MISSING DATA ANALYSIS")
    print("=" * 80)
    
    print("\n❌ Missing from Country-Strategy-Summary.md:")
    print("   - Population per country")
    print("   - TV homes per country")
    print("   - Subscriber numbers per operator")
    print("   - Market share percentages")
    print("   - Roku engagement likelihood (likely/unlikely)")
    print("   - Amazon Fire TV activity status")
    print("   - Retail partners per country")
    print("   - Technical keywords per operator")
    
    print("\n❌ Missing from specifications.md files:")
    print("   - Conditional Access Systems (CAS) details")
    print("   - Developer portal URLs")
    print("   - Operator website URLs")
    print("   - Parent company information")
    print("   - Access methods (public, NDA, partnership)")
    print("   - Technical keywords")
    print("   - STB specifications")
    print("   - IPTV/OTT details")
    
    print("\n❌ Missing from Operator-Key-Contacts.md:")
    print("   - Contact categories/roles")
    print("   - Source information")
    print("   - Location")
    print("   - Platform (LinkedIn, Corporate, etc.)")
    print("   - Detailed notes")
    
    print("\n❌ Missing from free-to-air-market.md files:")
    print("   - Platform breakdown (DTT, cable, satellite)")
    print("   - Coverage information")
    print("   - Household numbers")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    analyze_current_extraction()

