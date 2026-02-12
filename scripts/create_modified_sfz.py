#!/usr/bin/env python3
"""
Create modified SFZ file pointing to WAV files instead of FLAC
Phase 1, Step 2: Update SFZ mappings
"""

import re
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
WORKSHOP_ROOT = SCRIPT_DIR.parent
SOURCE_SFZ = WORKSHOP_ROOT / "src/SalamanderGrandPiano/Salamander Grand Piano V3.sfz"
OUTPUT_SFZ = WORKSHOP_ROOT / "build/salamander_wav/Salamander Grand Piano V3.wav.sfz"


def modify_sfz(sfz_content: str) -> str:
    """
    Modify SFZ content to reference WAV files instead of FLAC.
    """
    # Replace .flac with .wav
    modified = sfz_content.replace('.flac', '.wav')

    # Replace file extension definition
    modified = modified.replace('#define $EXT flac', '#define $EXT wav')

    return modified


def main():
    print("=" * 60)
    print("Creating WAV-compatible SFZ file")
    print("=" * 60)
    print()

    if not SOURCE_SFZ.exists():
        print(f"✗ ERROR: SFZ file not found: {SOURCE_SFZ}")
        sys.exit(1)

    print(f"Source: {SOURCE_SFZ}")
    print(f"Output: {OUTPUT_SFZ}")
    print()

    # Read source SFZ
    with open(SOURCE_SFZ, 'r', encoding='utf-8') as f:
        sfz_content = f.read()

    # Modify content
    modified_sfz = modify_sfz(sfz_content)

    # Count references
    wav_refs = modified_sfz.count('.wav')
    flac_refs = modified_sfz.count('.flac')

    # Create output directory
    OUTPUT_SFZ.parent.mkdir(parents=True, exist_ok=True)

    # Write modified SFZ
    with open(OUTPUT_SFZ, 'w', encoding='utf-8') as f:
        f.write(modified_sfz)

    print("✓ Modified SFZ created successfully")
    print(f"  - WAV references:  {wav_refs}")
    print(f"  - FLAC references: {flac_refs} (in comments/headers)")
    print()
    print("Next step: python3 ../scripts/03_validate_sfz.py")


if __name__ == "__main__":
    main()
