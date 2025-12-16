#!/usr/bin/env python3
import re
import os

# Read the summary file
with open('Europe/Country-Strategy-Summary.md', 'r') as f:
    content = f.read()

# Extract countries and operators
countries_operators = {}
current_country = None

lines = content.split('\n')
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check for country header
    if line.startswith('## ') and not line.startswith('## Summary'):
        current_country = line.replace('## ', '').strip()
        if current_country not in countries_operators:
            countries_operators[current_country] = []
    
    # Check for operator (starts with ** and contains operator name)
    elif line.startswith('**') and current_country:
        operator = line.replace('**', '').strip()
        # Skip if it's a section header or summary
        if operator and not operator.startswith('For ') and not operator.startswith('In '):
            # Clean up operator name (remove parenthetical info)
            operator_clean = re.sub(r'\s*\([^)]*\)', '', operator).strip()
            if operator_clean and operator_clean not in countries_operators[current_country]:
                countries_operators[current_country].append(operator_clean)
    
    i += 1

# Print and create structure
for country, operators in countries_operators.items():
    if not operators:
        continue
    print(f'\n{country}:')
    for op in operators:
        print(f'  - {op}')

# Create folder structure
base_path = 'Europe'
for country, operators in countries_operators.items():
    if not operators:
        continue
    
    # Clean country name for folder
    country_folder = country.replace(' ', '-')
    country_path = os.path.join(base_path, country_folder)
    
    for operator in operators:
        # Clean operator name for folder
        operator_folder = operator.replace('/', '-').replace(' ', '-').replace('(', '').replace(')', '')
        operator_path = os.path.join(country_path, operator_folder)
        
        # Create directory
        os.makedirs(operator_path, exist_ok=True)
        print(f'Created: {operator_path}')

print(f'\nTotal countries: {len([c for c in countries_operators.values() if c])}')
print(f'Total operators: {sum(len(ops) for ops in countries_operators.values())}')

