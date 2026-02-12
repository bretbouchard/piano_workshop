#!/usr/bin/env python3
"""
Flatten all drum kit directories for Polyphone
Creates flat structure: all samples + SFZ in one directory per kit
"""

import os
import shutil
from pathlib import Path

def flatten_drum_kit(source_dir, output_dir, kit_name):
    """Flatten one drum kit directory"""
    source = Path(source_dir)
    output = Path(output_dir)
    flat_dir = output / kit_name

    print(f"\n{'='*70}")
    print(f"Processing: {kit_name}")
    print(f"{'='*70}")

    # Clean and create output directory
    if flat_dir.exists():
        shutil.rmtree(flat_dir)
    flat_dir.mkdir(parents=True, exist_ok=True)

    # Find all WAV files in source directory (both cases)
    wav_files = list(source.rglob("*.wav")) + list(source.rglob("*.WAV"))
    print(f"  Found {len(wav_files)} samples")

    if len(wav_files) == 0:
        print(f"  ⚠️  No samples found!")
        return None

    # Copy all samples to flat directory
    samples_copied = 0
    for wav_file in wav_files:
        dest_file = flat_dir / wav_file.name
        if not dest_file.exists():
            shutil.copy2(wav_file, dest_file)
            samples_copied += 1

    print(f"  ✅ Copied {samples_copied} samples to flat directory")

    # Count duplicates (same filename)
    unique_names = len(set([w.name for w in wav_files]))
    if unique_names != samples_copied:
        print(f"  ⚠️  Warning: {samples_copied - unique_names} duplicates skipped")

    return flat_dir

def generate_simple_sfz(flat_dir, kit_name):
    """Generate a simple SFZ that references all samples - Polyphone compatible"""
    wav_files = sorted(list(flat_dir.glob("*.wav")))

    if len(wav_files) == 0:
        return None

    # SFZ header with default_path for Polyphone
    sfz_content = f"// {kit_name} - GM Standard Mapping\n"
    sfz_content += "// Polyphone-compatible format\n\n"
    sfz_content += "<control>\n"
    sfz_content += "default_path=.\n\n"

    sfz_content += "<global>\n"
    sfz_content += "ampeg_attack=0.001\n"
    sfz_content += "ampeg_decay=0.1\n"
    sfz_content += "ampeg_sustain=100\n"
    sfz_content += "ampeg_release=0.3\n\n"

    sfz_content += "<group>\n"  # Group all regions

    # Simple mapping - distribute samples across keys 35-60
    # This is basic - production version would use proper GM mapping
    key_start = 35
    for i, wav_file in enumerate(wav_files):
        key = key_start + (i % 26)  # Distribute across 2 octaves
        sfz_content += f'<region> sample={wav_file.name} lokey={key} hikey={key} pitch_keycenter={key}\n'

    # Write SFZ
    sfz_path = flat_dir / f"{kit_name}.sfz"
    with open(sfz_path, 'w') as f:
        f.write(sfz_content)

    print(f"  ✅ Created SFZ: {sfz_path.name} ({len(wav_files)} samples mapped)")
    return sfz_path

def main():
    workshop = Path("/Users/bretbouchard/apps/schill/juce_backend/Sam_sampler/piano_workshop")
    source_base = workshop / "piano_workshop/build/drum_kits"
    output_base = workshop / "build/drum_kits_flat"

    # Drum kits to process (exclude test directories)
    kits = [
        ("tr808_gm", "roland_tr808"),
        ("tr909_gm", "roland_tr909"),
        ("tr606_gm", "roland_tr606"),
        ("tr707_gm", "roland_tr707"),
        ("tr505_gm", "roland_tr505"),
        ("tr626_gm", "roland_tr626"),
        ("blofeld_adaptive", "waldorf_blofeld"),
        ("vermona_drm1", "vermona_drm1"),
        ("alesis_sr16", "alesis_sr16"),
        ("101_drums_mars", "101_drums_mars"),
        ("mpc60_mars", "mpc60_mars"),
        ("vinyl_mars", "vinyl_mars"),
        ("808_mars", "808_mars"),
        ("drums_mars", "drums_mars"),
        ("909_tube", "909_tube"),
        ("ampeg_808", "ampeg_808"),
        ("drum_hits", "drum_hits"),
        ("synth_drums", "synth_drums"),
        ("techno_drums", "techno_drums"),
        ("r100_collection", "r100_collection"),
        ("home_made_kit", "home_made_kit"),
    ]

    print("="*70)
    print("FLATTEN ALL DRUM KITS FOR POLYPHONE")
    print("="*70)
    print(f"\nSource: {source_base}")
    print(f"Output: {output_base}")

    output_base.mkdir(parents=True, exist_ok=True)

    successful = []
    failed = []

    for source_name, kit_name in kits:
        source_dir = source_base / source_name

        if not source_dir.exists():
            print(f"\n⚠️  Skipping {kit_name} - source not found")
            failed.append(kit_name)
            continue

        try:
            # Flatten directory
            flat_dir = flatten_drum_kit(source_dir, output_base, kit_name)

            if flat_dir:
                # Generate SFZ
                sfz_path = generate_simple_sfz(flat_dir, kit_name)

                if sfz_path:
                    successful.append(kit_name)
                else:
                    failed.append(kit_name)
            else:
                failed.append(kit_name)

        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed.append(kit_name)

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✅ Successful: {len(successful)} kits")
    print(f"❌ Failed: {len(failed)} kits")
    print(f"\nOutput directory: {output_base}")
    print("\nNext steps:")
    print("1. Open Polyphone")
    print("2. For each kit:")
    print("   - Import samples from flat directory")
    print("   - Open the SFZ file")
    print("   - Export as SF2")
    print("="*70)

if __name__ == "__main__":
    main()
