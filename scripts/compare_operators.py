#!/usr/bin/env python3
"""
Script to compare operators in Operators/ directory with those in Europe/ directory
and identify any missing operators.
"""
import os
from pathlib import Path

def get_operators_from_directory(base_dir):
    """Extract operator names from directory structure."""
    operators = set()
    base_path = Path(base_dir)
    
    if not base_path.exists():
        return operators
    
    for item in base_path.iterdir():
        if item.is_dir():
            # Get the directory name as operator name
            operator_name = item.name
            operators.add(operator_name)
    
    return operators

def normalize_operator_name(name):
    """Normalize operator names for comparison."""
    # Remove common variations
    name = name.replace(' ', '-').replace('_', '-').lower()
    # Handle special cases
    name = name.replace('canal+', 'canal')
    name = name.replace('m7-', 'm7')
    name = name.replace('---', '-')
    return name

def find_operator_in_europe(operator_name, europe_path):
    """Check if operator exists in Europe directory structure."""
    normalized = normalize_operator_name(operator_name)
    
    # Search through all specifications.md files
    for spec_file in europe_path.rglob('specifications.md'):
        # Get the directory name containing the spec file
        operator_dir = spec_file.parent.name
        normalized_dir = normalize_operator_name(operator_dir)
        
        if normalized in normalized_dir or normalized_dir in normalized:
            return str(spec_file.parent.relative_to(europe_path))
    
    # Also check operator name in file content
    for spec_file in europe_path.rglob('specifications.md'):
        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check if operator name appears in the file
                if operator_name.lower() in content.lower():
                    return str(spec_file.parent.relative_to(europe_path))
        except:
            pass
    
    return None

def main():
    operators_dir = Path('Operators')
    europe_dir = Path('Europe')
    
    # Get operators from Operators directory
    operators_in_dir = get_operators_from_directory(operators_dir)
    
    print(f"Operators found in Operators/ directory: {len(operators_in_dir)}")
    print("\nOperators in Operators/ directory:")
    for op in sorted(operators_in_dir):
        print(f"  - {op}")
    
    print("\n" + "="*80)
    print("Checking which operators have specifications.md files in Europe/...")
    print("="*80 + "\n")
    
    found = []
    missing = []
    partial = []
    
    for operator in sorted(operators_in_dir):
        location = find_operator_in_europe(operator, europe_dir)
        if location:
            found.append((operator, location))
        else:
            # Check if there's a similar name
            normalized_op = normalize_operator_name(operator)
            similar = []
            for spec_file in europe_dir.rglob('specifications.md'):
                dir_name = spec_file.parent.name
                normalized_dir = normalize_operator_name(dir_name)
                if normalized_op in normalized_dir or normalized_dir in normalized_op:
                    similar.append(str(spec_file.parent.relative_to(europe_dir)))
            
            if similar:
                partial.append((operator, similar))
            else:
                missing.append(operator)
    
    print(f"\n✅ Found in Europe/ ({len(found)}):")
    for operator, location in found:
        print(f"  ✓ {operator:30} → {location}")
    
    if partial:
        print(f"\n⚠️  Partial matches ({len(partial)}):")
        for operator, locations in partial:
            print(f"  ~ {operator:30} → {', '.join(locations)}")
    
    if missing:
        print(f"\n❌ Missing from Europe/ ({len(missing)}):")
        for operator in missing:
            print(f"  ✗ {operator}")
    else:
        print("\n✅ All operators from Operators/ directory have corresponding entries in Europe/")
    
    # Also check for operators in Europe that aren't in Operators directory
    print("\n" + "="*80)
    print("Checking for operators in Europe/ that aren't in Operators/ directory...")
    print("="*80 + "\n")
    
    europe_operators = set()
    for spec_file in europe_dir.rglob('specifications.md'):
        operator_dir = spec_file.parent.name
        # Extract operator name from path
        country = spec_file.parent.parent.name
        europe_operators.add((country, operator_dir))
    
    operators_in_operators_dir = {normalize_operator_name(op) for op in operators_in_dir}
    
    extra = []
    for country, operator_dir in sorted(europe_operators):
        normalized = normalize_operator_name(operator_dir)
        # Check if this operator exists in Operators directory
        found_in_ops_dir = False
        for op_dir_name in operators_in_dir:
            if normalize_operator_name(op_dir_name) == normalized:
                found_in_ops_dir = True
                break
        
        if not found_in_ops_dir:
            extra.append((country, operator_dir))
    
    if extra:
        print(f"Operators in Europe/ but not in Operators/ ({len(extra)}):")
        for country, operator in extra:
            print(f"  + {country:20} / {operator}")
    else:
        print("✅ All operators in Europe/ have corresponding entries in Operators/")

if __name__ == '__main__':
    main()

