#!/usr/bin/env python3
"""
Create complete SFZ package with all include files updated
Phase 1, Step 2b: Ensure all SFZ components reference WAV
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
WORKSHOP_ROOT = SCRIPT_DIR.parent
BUILD_DIR = WORKSHOP_ROOT / "build/salamander_wav"
DATA_SRC = WORKSHOP_ROOT / "src/SalamanderGrandPiano/Data"
DATA_DST = BUILD_DIR / "Data"


def update_file_references(content: str) -> str:
    """Update file extensions from FLAC to WAV"""
    return content.replace('.flac', '.wav')


def process_sfz_file(file_path: Path, output_path: Path):
    """Process a single SFZ file and update references"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = update_file_references(content)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(modified)


def main():
    print("=" * 60)
    print("Updating SFZ Data Files for WAV")
    print("=" * 60)
    print()

    if not DATA_SRC.exists():
        print(f"✗ ERROR: Source data not found: {DATA_SRC}")
        return 1

    # Process all .txt files in Data directory
    txt_files = list(DATA_SRC.rglob("*.txt"))

    print(f"Found {len(txt_files)} files to update")
    print()

    for src_file in txt_files:
        rel_path = src_file.relative_to(DATA_SRC)
        dst_file = DATA_DST / rel_path

        process_sfz_file(src_file, dst_file)
        print(f"  ✓ Updated: {rel_path}")

    print()
    print("=" * 60)
    print("Update Complete!")
    print("=" * 60)
    print()
    print(f"Source: {DATA_SRC}")
    print(f"Output: {DATA_DST}")
    print()
    print("All FLAC references replaced with WAV references")
    print()
    print("Next: Run validation or proceed to SF2 build")


if __name__ == "__main__":
    main()
