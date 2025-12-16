#!/usr/bin/env python3
"""
Script to merge duplicate operator directories.
Preserves contents from both directories, preferring hyphenated versions.
"""
import os
import shutil
from pathlib import Path

# Find duplicates - directories with same name but different formatting
def find_duplicates():
    """Find duplicate operator directories."""
    base_path = Path('Europe')
    duplicates = []
    
    for country_dir in base_path.iterdir():
        if not country_dir.is_dir():
            continue
        
        operators = {}
        for op_dir in country_dir.iterdir():
            if not op_dir.is_dir():
                continue
            
            op_name = op_dir.name
            # Normalize name (remove hyphens/spaces for comparison)
            normalized = op_name.replace('-', ' ').lower().strip()
            
            if normalized not in operators:
                operators[normalized] = []
            operators[normalized].append(op_dir)
        
        # Find duplicates
        for normalized, dirs in operators.items():
            if len(dirs) > 1:
                duplicates.append((country_dir.name, dirs))
    
    return duplicates

def merge_directories(source_dir, target_dir):
    """Merge source_dir contents into target_dir."""
    if not source_dir.exists():
        return
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all files from source to target
    for item in source_dir.iterdir():
        target_item = target_dir / item.name
        
        if item.is_file():
            # If file exists in target, check if different
            if target_item.exists():
                # Compare file sizes/content
                if item.stat().st_size != target_item.stat().st_size:
                    # Create backup or append
                    backup_name = f"{item.stem}_backup{item.suffix}"
                    backup_path = target_dir / backup_name
                    if not backup_path.exists():
                        shutil.copy2(item, backup_path)
                        print(f"  Created backup: {backup_path}")
                # Use the newer file or keep both
                if item.stat().st_mtime > target_item.stat().st_mtime:
                    shutil.copy2(item, target_item)
                    print(f"  Updated: {target_item}")
            else:
                shutil.copy2(item, target_item)
                print(f"  Copied: {target_item}")
        elif item.is_dir():
            # Recursively merge subdirectories
            merge_directories(item, target_item)

def main():
    duplicates = find_duplicates()
    
    if not duplicates:
        print("No duplicates found.")
        return
    
    print(f"Found {len(duplicates)} sets of duplicate directories:\n")
    
    for country, dirs in duplicates:
        print(f"\n{country}:")
        for d in dirs:
            print(f"  - {d.name}")
        
        # Prefer hyphenated version, or first one if both have same format
        # Sort to prefer hyphenated versions
        dirs_sorted = sorted(dirs, key=lambda x: ('-' in x.name, x.name))
        target_dir = dirs_sorted[0]  # Keep this one
        source_dirs = dirs_sorted[1:]  # Merge these into target
        
        print(f"\n  Keeping: {target_dir.name}")
        print(f"  Merging from: {[d.name for d in source_dirs]}")
        
        for source_dir in source_dirs:
            print(f"\n  Merging {source_dir.name} -> {target_dir.name}")
            merge_directories(source_dir, target_dir)
            
            # Remove source directory after merging
            if source_dir.exists():
                shutil.rmtree(source_dir)
                print(f"  Removed: {source_dir}")

if __name__ == '__main__':
    main()

