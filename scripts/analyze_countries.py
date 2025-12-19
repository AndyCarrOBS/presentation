#!/usr/bin/env python3
"""Analyze which countries have actual free-to-air data"""
import json
from pathlib import Path

# Load dashboard data
with open('dashboard_data.json', 'r') as f:
    data = json.load(f)

countries = data['countries']

# Categorize countries
countries_with_psb = []
countries_with_fta_data = []
countries_with_operators = []
countries_with_nothing = []

for country, info in countries.items():
    has_psb = bool(info.get('psb'))
    has_fta = bool(info.get('free_to_air', {}).get('platforms'))
    has_ops = bool(info.get('operators'))
    
    if has_psb:
        countries_with_psb.append(country)
    if has_fta:
        countries_with_fta_data.append(country)
    if has_ops:
        countries_with_operators.append(country)
    
    if not has_psb and not has_fta and not has_ops:
        countries_with_nothing.append(country)

print("=" * 80)
print("COUNTRY ANALYSIS")
print("=" * 80)
print(f"\nTotal countries in dashboard: {len(countries)}")
print(f"Countries with PSB data: {len(countries_with_psb)}")
print(f"Countries with free-to-air market data: {len(countries_with_fta_data)}")
print(f"Countries with operators: {len(countries_with_operators)}")
print(f"Countries with NO relevant data: {len(countries_with_nothing)}")

print("\n" + "=" * 80)
print("COUNTRIES WITH PSB DATA (should show in Free-to-Air view):")
print("=" * 80)
for c in sorted(countries_with_psb):
    psbs = countries[c].get('psb', [])
    print(f"  {c}: {len(psbs)} PSB(s)")

print("\n" + "=" * 80)
print("COUNTRIES WITH FREE-TO-AIR MARKET DATA:")
print("=" * 80)
for c in sorted(countries_with_fta_data):
    fta = countries[c].get('free_to_air', {})
    platforms = fta.get('platforms', {})
    print(f"  {c}: {', '.join(platforms.keys())}")

print("\n" + "=" * 80)
print("COUNTRIES WITH NO RELEVANT DATA (should be filtered out):")
print("=" * 80)
for c in sorted(countries_with_nothing):
    print(f"  {c}")

print("\n" + "=" * 80)
print("RECOMMENDATION:")
print("=" * 80)
relevant_countries = set(countries_with_psb) | set(countries_with_fta_data) | set(countries_with_operators)
print(f"Free-to-Air view should show: {len(relevant_countries)} countries")
print(f"  - Countries with PSBs: {len(countries_with_psb)}")
print(f"  - Countries with free-to-air data: {len(countries_with_fta_data)}")
print(f"  - Countries with operators (for operator view): {len(countries_with_operators)}")

