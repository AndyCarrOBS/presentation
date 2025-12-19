#!/usr/bin/env python3
"""Check Austria data in dashboard"""
import json

with open('dashboard_data.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("AUSTRIA DASHBOARD DATA SUMMARY")
print("=" * 80)

at = data['countries']['Austria']
print(f"\nCountry Information:")
print(f"  Population: {at.get('population_million')} million")
print(f"  TV Homes: {at.get('tv_homes_million')} million")
print(f"  PSBs: {len(at.get('psb', []))}")
for psb in at.get('psb', []):
    print(f"    - {psb['name']}: {psb['ott_app']}")
print(f"  Retail Partners: {', '.join(at.get('retail_partners', []))}")
print(f"  Free-to-Air Platforms: {', '.join(at.get('free_to_air', {}).get('platforms', {}).keys())}")

print(f"\nOperators ({len(at.get('operators', []))}):")
for op in sorted(at.get('operators', [])):
    print(f"  - {op}")

ops = data['operators'].get('Austria', {})
print(f"\nOperator Technical Details:")
for op_name in sorted(ops.keys()):
    op_data = ops[op_name]
    print(f"\n{op_name}:")
    print(f"  HbbTV Version: {op_data.get('hbbtv_version', 'N/A')}")
    print(f"  CI+ Version: {op_data.get('ci_version', 'N/A')}")
    print(f"  CAS Systems: {', '.join(op_data.get('cas_systems', [])) if op_data.get('cas_systems') else 'N/A'}")
    print(f"  Has Specification: {op_data.get('has_specification', False)}")
    print(f"  Website: {op_data.get('website', 'N/A')}")
    print(f"  Parent Company: {op_data.get('parent_company', 'N/A')}")
    print(f"  Access Methods: {', '.join(op_data.get('access_methods', [])) if op_data.get('access_methods') else 'N/A'}")

contacts = data['contacts'].get('Austria', {})
print(f"\nOperator Contacts:")
for op_name in sorted(contacts.keys()):
    op_contacts = contacts[op_name]
    if isinstance(op_contacts, dict):
        total = sum(len(c) for c in op_contacts.values())
        print(f"  {op_name}: {total} contacts across {len(op_contacts)} role(s)")
        for role, role_contacts in op_contacts.items():
            print(f"    - {role}: {len(role_contacts)} contacts")
    else:
        print(f"  {op_name}: {len(op_contacts) if isinstance(op_contacts, list) else 'N/A'} contacts")

print("\n" + "=" * 80)

