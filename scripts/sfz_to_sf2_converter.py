#!/usr/bin/env python3
"""
Salamander Grand Piano - Direct SFZ to SF2 Conversion
Phase 1, Step 4: Build SF2 using existing tools or custom implementation

This script provides a practical path to SF2 creation using available tools.
"""

import os
import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
WORKSHOP_ROOT = SCRIPT_DIR.parent
BUILD_DIR = WORKSHOP_ROOT / "build/salamander_wav"
DIST_DIR = WORKSHOP_ROOT / "dist"


def check_polyphone():
    """Check if Polyphone is installed"""
    try:
        result = subprocess.run(
            ["polyphone", "--version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def build_with_polyphone():
    """Build SF2 using Polyphone GUI or CLI"""
    sfz_path = BUILD_DIR / "Salamander Grand Piano V3.wav.sfz"
    output_path = DIST_DIR / "salamander_grand_v1.sf2"

    print("=" * 60)
    print("Building SF2 with Polyphone")
    print("=" * 60)
    print()

    if not sfz_path.exists():
        print(f"✗ ERROR: SFZ file not found: {sfz_path}")
        print("Run conversion steps first")
        return False

    print(f"SFZ:    {sfz_path}")
    print(f"Output: {output_path}")
    print()

    # Check if Polyphone is available
    if not check_polyphone():
        print("Polyphone not found. Installation options:")
        print()
        print("  macOS:")
        print("    brew install polyphone")
        print("    or download from: https://www.polyphone-soundfonts.com/")
        print()
        print("  Linux:")
        print("    sudo apt install polyphone")
        print()
        print("  After installation, run this script again.")
        print()
        print("Alternatively, use Polyphone GUI:")
        print("  1. Open Polyphone")
        print("  2. File → Import → SFZ")
        print(f"  3. Select: {sfz_path}")
        print("  4. File → Export → SoundFont2")
        print(f"  5. Save as: {output_path}")
        print("  6. Settings: 16-bit, 44.1kHz, no dithering")
        return False

    # Try CLI mode
    try:
        print("Attempting Polyphone CLI conversion...")
        cmd = [
            "polyphone",
            "--convert",
            str(sfz_path),
            str(output_path),
            "--format", "sf2"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ SF2 created successfully!")
            print(f"  Output: {output_path}")
            return True
        else:
            print(f"Polyphone CLI failed: {result.stderr}")
            print("Please use Polyphone GUI (see instructions above)")
            return False

    except Exception as e:
        print(f"Error running Polyphone: {e}")
        return False


def build_with_custom():
    """
    Placeholder for custom SF2 writer.

    Full implementation would write proper RIFF/IFF chunks:
    - INFO chunk: version, ROM name, copyright
    - SDTA chunk: sample data (smpl)
    - PDTA chunk:
      - PHDR: preset headers
      - PBAG: preset zones
      - PMOD: preset modulators
      - PGEN: preset generators
      - IHDR: instrument headers
      - IBAG: instrument zones
      - IMOD: instrument modulators
      - IGEN: instrument generators
      - SHDR: sample headers
    """
    print("=" * 60)
    print("Custom SF2 Builder")
    print("=" * 60)
    print()
    print("⚠ Full custom SF2 writer not implemented")
    print()
    print("SF2 format requires complex RIFF/IFF structure with:")
    print("  - Sample data packing (16-bit, 44.1kHz)")
    print("  - Preset/instrument zone generation")
    print("  - Generator parameters (key range, vel range, etc.)")
    print("  - Modulator routing")
    print("  - Sample headers with loop points")
    print()
    print("Recommendations:")
    print("  1. Use Polyphone (recommended)")
    print("  2. Use existing Python library (sf2forge)")
    print("  3. Implement custom writer (significant effort)")
    print()

    # Check for sf2 library
    try:
        import sf2forge
        print("✓ sf2forge library available - could be used")
        print("  See: https://github.com/nwnormand/sf2forge")
    except ImportError:
        print("✗ sf2forge not installed")
        print("  Install with: pip install sf2forge")

    return False


def create_attribution():
    """Create attribution file"""
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    attribution = """Salamander Grand Piano
© Alexander Holm
Licensed under Creative Commons Attribution 3.0 (CC-BY 3.0)
Source: https://github.com/sfzinstruments/SalamanderGrandPiano

Original recordings: 48kHz/24-bit FLAC
Converted for Sam Sampler: 16-bit/44.1kHz WAV (SF2 format)

Conversion details:
- 16 velocity layers per note
- Note range: A0 (21) to C8 (108)
- Includes release samples (string resonance, hammer noise)
- Includes pedal noise samples
- ~500-600 MB total size
"""

    attrib_path = DIST_DIR / "attribution.txt"
    with open(attrib_path, 'w') as f:
        f.write(attribution)

    print(f"✓ Created attribution: {attrib_path}")


def main():
    """Main build workflow"""
    print()
    print("=" * 60)
    print("Salamander Grand Piano - SF2 Build")
    print("=" * 60)
    print()

    # Try Polyphone first
    if build_with_polyphone():
        create_attribution()
        print()
        print("=" * 60)
        print("Build Complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Test SF2 in sampler")
        print("  2. Verify all 16 velocity layers")
        print("  3. Test sustain pedal behavior")
        print("  4. Run QA checklist")
        return 0

    # Fallback to custom builder
    print()
    if build_with_custom():
        create_attribution()
        return 0

    print()
    print("=" * 60)
    print("Build Manual Step Required")
    print("=" * 60)
    print()
    print("Please complete SF2 creation manually:")
    print()
    print("RECOMMENDED: Use Polyphone GUI")
    print("  1. Install Polyphone:")
    print("     - macOS: brew install polyphone")
    print("     - Download: https://www.polyphone-soundfonts.com/")
    print()
    print(f"  2. Open: {BUILD_DIR / 'Salamander Grand Piano V3.wav.sfz'}")
    print("  3. Verify:")
    print("     - 16 velocity layers")
    print("     - Release samples present")
    print("     - Note range A0-C8")
    print()
    print(f"  4. Export to: {DIST_DIR / 'salamander_grand_v1.sf2'}")
    print("  5. Settings:")
    print("     - Format: SF2")
    print("     - Bit depth: 16")
    print("     - Sample rate: 44.1kHz")
    print("     - No dithering")
    print("     - No embedded effects")
    print()
    print("After SF2 is created, run:")
    print(f"  python3 {SCRIPT_DIR / '05_package_piano.py'}")
    print()

    return 1


if __name__ == "__main__":
    sys.exit(main())
