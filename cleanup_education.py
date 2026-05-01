#!/usr/bin/env python3
"""
Cleanup and fix education folder:
1. Remove duplicate notebooks from root
2. Fix input() calls (comment out)
3. Fix !python commands
4. Enhance incomplete solutions
"""

import json
import os
import glob
import re
from pathlib import Path

def fix_notebook(filepath):
    """Fix issues in a notebook file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    modified = False
    
    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        
        source = cell.get('source', [])
        if isinstance(source, list):
            source = ''.join(source)
        
        # Fix 1: Comment out input() calls
        if 'input(' in source:
            new_source = re.sub(
                r'^(\s*)(.*)input\(',
                r'\1# (Fixed: interactive input removed) \2input(',
                source,
                flags=re.MULTILINE
            )
            if new_source != source:
                cell['source'] = new_source.split('\n')
                modified = True
        
        # Fix 2: Comment out !python commands
        if '!python' in source:
            new_source = source.replace('!python', '# !python')
            if new_source != source:
                cell['source'] = new_source.split('\n')
                modified = True
        
        # Fix 3: Add solution templates for empty "# Решение" cells
        if source.strip() == '# Решение' or source.strip() == '# Решение\n':
            new_source = '# Решение\n# TODO: Добавить решение задачи'
            cell['source'] = new_source.split('\n')
            modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        return True
    return False

def reorganize_education():
    """Remove duplicates and organize education folder"""
    root = 'education'
    
    # List all notebooks in root
    root_notebooks = glob.glob(os.path.join(root, '*.ipynb'))
    
    # List all notebooks in subdirectories
    subdir_notebooks = glob.glob(os.path.join(root, '*', '*.ipynb'))
    
    print(f"Found {len(root_notebooks)} notebooks in root")
    print(f"Found {len(subdir_notebooks)} notebooks in subdirectories")
    
    # Check for duplicates (same filename in root and subdir)
    duplicates_removed = 0
    for root_nb in root_notebooks:
        basename = os.path.basename(root_nb)
        # Check if same file exists in subdirs
        for subdir_nb in subdir_notebooks:
            if os.path.basename(subdir_nb) == basename:
                print(f"Removing duplicate: {root_nb}")
                os.remove(root_nb)
                duplicates_removed += 1
                break
    
    print(f"Removed {duplicates_removed} duplicate notebooks")
    return duplicates_removed

def fix_all_notebooks():
    """Fix all notebooks in education folder"""
    root = 'education'
    all_notebooks = glob.glob(os.path.join(root, '**', '*.ipynb'), recursive=True)
    
    print(f"Processing {len(all_notebooks)} notebooks...")
    
    fixed_count = 0
    for nb_path in all_notebooks:
        try:
            if fix_notebook(nb_path):
                fixed_count += 1
                print(f"✓ Fixed: {nb_path}")
        except Exception as e:
            print(f"✗ Error in {nb_path}: {e}")
    
    print(f"Fixed {fixed_count} notebooks")
    return fixed_count

if __name__ == '__main__':
    print("=== Education Folder Cleanup ===\n")
    
    print("Step 1: Reorganize (remove duplicates)")
    reorganize_education()
    
    print("\nStep 2: Fix all notebooks")
    fix_all_notebooks()
    
    print("\n=== Cleanup Complete ===")
    print("Ready for git commit!")
