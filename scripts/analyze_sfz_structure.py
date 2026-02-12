#!/usr/bin/env python3
"""
Analyze SFZ structure to understand sample mappings
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
WORKSHOP_ROOT = SCRIPT_DIR.parent
SFZ_FILE = WORKSHOP_ROOT / "src/SalamanderGrandPiano/Salamander Grand Piano V3.sfz"
DATA_DIR = WORKSHOP_ROOT / "src/SalamanderGrandPiano/Data"

print("Analyzing Salamander Grand Piano SFZ structure...")
print()

# Read main SFZ
with open(SFZ_FILE, 'r') as f:
    sfz_content = f.read()

# Find all include directives
includes = re.findall(r'#include\s+"([^"]+)"', sfz_content)

print(f"Main SFZ includes {len(includes)} files:")
for inc in includes:
    print(f"  - {inc}")
    inc_path = DATA_DIR / inc
    if inc_path.exists():
        with open(inc_path, 'r') as f:
            lines = len(f.readlines())
        print(f"    ({lines} lines)")
print()

# Check notes.txt
notes_file = DATA_DIR / "notes.txt"
if notes_file.exists():
    with open(notes_file, 'r') as f:
        notes_content = f.read()

    # Count regions
    regions = notes_content.count('<region>')
    print(f"notes.txt contains {regions} regions")
    print()

    # Show sample region
    sample_regions = notes_content.split('<region>')[1:6]  # First 5 regions
    for i, region in enumerate(sample_regions, 1):
        lines = [line.strip() for line in region.split('\n') if line.strip() and '=' in line]
        print(f"Example region {i}:")
        for line in lines[:5]:  # First 5 parameters
            print(f"  {line}")
        print()
