#!/usr/bin/env python3
"""
Package the completed piano for distribution
Phase 1, Step 5: Create distribution package
"""

import json
import tarfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
WORKSHOP_ROOT = SCRIPT_DIR.parent
DIST_DIR = WORKSHOP_ROOT / "dist"

SF2_FILE = DIST_DIR / "salamander_grand_v1.sf2"
ATTRIB_FILE = DIST_DIR / "attribution.txt"

PKG_DIR = DIST_DIR / "sam_sampler_piano"
PIANO_DIR = PKG_DIR / "piano"


def create_manifest(sf2_size_mb: float) -> dict:
    """Create piano manifest JSON"""
    return {
        "name": "Salamander Grand Piano",
        "version": "1.0.0",
        "format": "SF2",
        "sample_rate": 44100,
        "bit_depth": 16,
        "channels": 1,
        "velocity_layers": 16,
        "note_range": {
            "min": 21,
            "max": 108,
            "min_name": "A0",
            "max_name": "C8"
        },
        "release_samples": True,
        "file_size_mb": round(sf2_size_mb, 2),
        "license": "CC-BY 3.0",
        "attribution": "Alexander Holm",
        "source_url": "https://github.com/sfzinstruments/SalamanderGrandPiano",
        "converted_date": "2024-12-24T00:00:00Z",
        "converter": "Sam Sampler Piano Build Pipeline",
        "features": {
            "sustain_pedal": True,
            "release_samples": True,
            "hammer_noise": True,
            "string_resonance": True,
            "pedal_noise": True,
            "velocity_response": "dynamic",
            "polyphony": "optimized"
        }
    }


def main():
    print("=" * 60)
    print("Packaging Salamander Grand Piano")
    print("=" * 60)
    print()

    if not SF2_FILE.exists():
        print(f"✗ ERROR: SF2 file not found: {SF2_FILE}")
        return 1

    # Get file size
    size_bytes = SF2_FILE.stat().st_size
    size_mb = size_bytes / 1024 / 1024

    print(f"SF2 file: {SF2_FILE}")
    print(f"Size: {size_mb:.1f} MB")
    print()

    # Create package structure
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    PIANO_DIR.mkdir(parents=True, exist_ok=True)

    # Copy files
    print("Copying files...")
    import shutil
    shutil.copy2(SF2_FILE, PIANO_DIR / "salamander_grand_v1.sf2")
    shutil.copy2(ATTRIB_FILE, PIANO_DIR / "attribution.txt")
    print("  ✓ SF2 file")
    print("  ✓ Attribution")
    print()

    # Create manifest
    manifest = create_manifest(size_mb)
    manifest_path = PKG_DIR / "piano_manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"✓ Created manifest: piano_manifest.json")
    print()

    print("Package structure:")
    print("  sam_sampler_piano/")
    print("    ├── piano/")
    print("    │   ├── salamander_grand_v1.sf2")
    print("    │   └── attribution.txt")
    print("    └── piano_manifest.json")
    print()

    # Create archive
    archive_path = DIST_DIR / "sam_sampler_piano.tar.gz"
    print(f"Creating archive: {archive_path}")

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(PKG_DIR, arcname="sam_sampler_piano")

    archive_size = archive_path.stat().st_size / 1024 / 1024
    print(f"✓ Archive created: {archive_size:.1f} MB")
    print()

    print("=" * 60)
    print("Packaging Complete!")
    print("=" * 60)
    print()
    print(f"Distribution: {PKG_DIR}")
    print(f"Archive:      {archive_path}")
    print()
    print("Installation:")
    print("  1. Extract archive to Sam Sampler assets directory")
    print("  2. Load SF2 via Sam Sampler instrument loader")
    print("  3. Enable sustain pedal (CC64) for proper behavior")
    print()
    print("Next: Phase 2 - SF2 Loader Implementation")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
