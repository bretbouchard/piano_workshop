#!/usr/bin/env python3
"""
Validate SFZ file and verify all referenced samples exist
Phase 1, Step 3: Validation
"""

import re
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
WORKSHOP_ROOT = SCRIPT_DIR.parent
BUILD_DIR = WORKSHOP_ROOT / "build/salamander_wav"
SFZ_FILE = BUILD_DIR / "Salamander Grand Piano V3.wav.sfz"


def extract_sample_references(sfz_content: str) -> list[str]:
    """
    Extract all sample file references from SFZ content.
    """
    samples = []

    # Match sample= directives
    pattern = r'sample\s*=\s*"?([^"\s]+)"?'

    for match in re.finditer(pattern, sfz_content):
        sample_ref = match.group(1)

        # Skip wildcards and control files
        if '*' in sample_ref or '.txt' in sample_ref:
            continue

        samples.append(sample_ref)

    return samples


def main():
    print("=" * 60)
    print("SFZ Validation")
    print("=" * 60)
    print()

    if not SFZ_FILE.exists():
        print(f"✗ ERROR: SFZ file not found: {SFZ_FILE}")
        print("Run 02_create_modified_sfz.py first")
        return 1

    print(f"Validating: {SFZ_FILE}")
    print()

    # Read SFZ file
    with open(SFZ_FILE, 'r', encoding='utf-8') as f:
        sfz_content = f.read()

    # Extract sample references
    sample_refs = extract_sample_references(sfz_content)

    print(f"Checking {len(sample_refs)} sample references...")
    print()

    # Validate each sample
    missing = []
    found = 0

    for sample_ref in sample_refs:
        sample_path = BUILD_DIR / "Samples" / sample_ref

        if sample_path.exists():
            found += 1
        else:
            missing.append(sample_ref)

    # Report results
    print("=" * 60)
    print("Validation Results")
    print("=" * 60)
    print(f"Total samples referenced: {len(sample_refs)}")
    print(f"Found:                    {found}")
    print(f"Missing:                  {len(missing)}")
    print()

    if missing:
        print("Missing samples:")
        for sample in missing[:10]:  # Show first 10
            print(f"  ✗ {sample}")

        if len(missing) > 10:
            print(f"  ... and {len(missing) - 10} more")

        print()
        print("✗ Validation failed - missing samples")
        return 1
    else:
        print("✓ All samples present!")
        print()
        print("Next step: Build SF2 (see PHASE1_COMPLETE.md)")
        return 0


if __name__ == "__main__":
    exit(main())
