#!/usr/bin/env python3
"""
Blofeld Adaptive Velocity Layer Calculator

Handles the Blofeld drumkit's variable sample counts:
- Kick: 37 samples → 6 velocity layers
- Snare: 16 samples → 4 velocity layers
- Hi-Hat: 16 samples → 4 velocity layers
- Percussion: 31 samples → Key mapping (not velocity)
- Clap: 4 samples → 2 velocity layers
- Tom: 4 samples → 2 velocity layers

Usage:
    python3 blofeld_velocity_calc.py
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple

# ==============================================================================
# Configuration
# ==============================================================================

SOURCE_DIR = "/Volumes/Storage/samples/retro drum-machine/blofeld drumkit"
BUILD_DIR = "piano_workshop/build/drum_kits/blofeld_adaptive"

# Blofeld instrument mapping
BLOFELD_INSTRUMENTS = {
    "bd": "kick",      # 37 samples
    "sd": "snare",     # 16 samples
    "hat": "hihat",    # 16 samples
    "perc": "percussion",  # 31 samples (special: key mapping)
    "clap": "clap",    # 4 samples
    "tom": "tom",      # 4 samples
}

# GM Standard MIDI mapping
GM_MAPPING = {
    "kick": 36,          # C1
    "snare": 38,         # D1
    "clap": 39,          # D#1
    "hihat": 42,         # F#1 (closed), 46 (open) - we'll use closed
    "tom": 45,           # A1
    "percussion": None,  # Special: map to multiple keys
}

# ==============================================================================
# Velocity Layer Calculation
# ==============================================================================

def calculate_velocity_mapping(num_samples: int, instrument_name: str) -> Dict:
    """
    Calculate optimal velocity mapping for variable sample counts

    Args:
        num_samples: Number of samples available
        instrument_name: Name of the instrument

    Returns:
        Dict with mapping strategy and velocity ranges
    """

    # Special case: Percussion maps to keys, not velocity layers
    if instrument_name == "percussion":
        return {
            "strategy": "key_mapping",
            "num_layers": 1,
            "mapping": "keys",
            "ranges": [],
            "note": "Map each sample to different MIDI key (60-90)"
        }

    # Calculate optimal number of velocity layers
    if num_samples >= 30:
        num_layers = 6
        samples_per_layer = num_samples // num_layers
    elif num_samples >= 20:
        num_layers = 5
        samples_per_layer = num_samples // num_layers
    elif num_samples >= 15:
        num_layers = 4
        samples_per_layer = num_samples // num_layers
    elif num_samples >= 8:
        num_layers = 3
        samples_per_layer = num_samples // num_layers
    elif num_samples >= 4:
        num_layers = 2
        samples_per_layer = num_samples // num_layers
    else:
        num_layers = 1
        samples_per_layer = num_samples

    # Calculate velocity ranges for each layer
    ranges = []
    for i in range(num_layers):
        start_vel = (i * 128) // num_layers
        end_vel = ((i + 1) * 128) // num_layers - 1

        # Last layer always extends to 127
        if i == num_layers - 1:
            end_vel = 127

        # Calculate which samples to use for this layer
        sample_start = i * samples_per_layer
        sample_end = min((i + 1) * samples_per_layer, num_samples)

        # For first layer, start at sample 0
        if i == 0:
            sample_start = 0

        ranges.append({
            "layer": i + 1,
            "lovel": start_vel,
            "hivel": end_vel,
            "sample_start": sample_start,
            "sample_end": sample_end,
            "num_samples": sample_end - sample_start
        })

    return {
        "strategy": "velocity_layers",
        "num_layers": num_layers,
        "num_samples_total": num_samples,
        "ranges": ranges,
        "mapping": "velocity"
    }


# ==============================================================================
# Sample Analysis
# ==============================================================================

def analyze_blofeld_samples() -> Dict[str, int]:
    """Analyze Blofeld sample counts per instrument"""
    print("📊 Analyzing Blofeld samples...")

    source_path = Path(SOURCE_DIR)
    if not source_path.exists():
        print(f"❌ Source directory not found: {SOURCE_DIR}")
        return {}

    # Count samples per instrument
    sample_counts = {}

    # Sample naming: cw_blofeld_{instrument}{number}.wav
    for wav_file in source_path.glob("cw_blofeld_*.wav"):
        # Extract instrument name
        # e.g., "cw_blofeld_bd01.wav" → "bd"
        filename = wav_file.stem  # Remove .wav
        parts = filename.split("_")  # ["cw", "blofeld", "bd01"]

        if len(parts) >= 3:
            inst_part = parts[2]  # "bd01", "sd05", etc.

            # Extract instrument prefix (letters before numbers)
            inst_name = ""
            for char in inst_part:
                if char.isalpha():
                    inst_name += char
                else:
                    break

            if inst_name:
                sample_counts[inst_name] = sample_counts.get(inst_name, 0) + 1

    print("\n📈 Sample Counts:")
    for inst, count in sorted(sample_counts.items()):
        inst_full = BLOFELD_INSTRUMENTS.get(inst, inst)
        mapping = calculate_velocity_mapping(count, inst_full)
        print(f"  {inst_full:12} ({inst:4}): {count:3} samples → {mapping['num_layers']} velocity layers")

    return sample_counts


# ==============================================================================
# SFZ Generation
# ==============================================================================

def generate_blofeld_sfz(sample_counts: Dict[str, int]) -> str:
    """Generate SFZ file with adaptive velocity mapping"""
    print("\n📝 Generating Blofeld SFZ file...")

    sfz_lines = [
        "// Waldorf Blofeld Drum Kit - Adaptive Velocity Mapping",
        "// Generated automatically by blofeld_velocity_calc.py",
        "//",
        "// Instruments:",
    ]

    # Add instrument info
    for inst, count in sorted(sample_counts.items()):
        inst_full = BLOFELD_INSTRUMENTS.get(inst, inst)
        mapping = calculate_velocity_mapping(count, inst_full)
        sfz_lines.append(f"//   {inst_full}: {count} samples → {mapping['num_layers']} layers")

    sfz_lines.extend([
        "",
        "// Control defaults",
        "<control>",
        "  set_cc7=127  // Volume",
        "",
        "// Global settings",
        "<global>",
        "  ampeg_attack=0.001",
        "  ampeg_decay=0.1",
        "  ampeg_sustain=100",
        "  ampeg_release=0.3",
        "  ampeg_vel2attack=0",
        "  ampeg_vel2decay=0",
        "  ampeg_vel2release=0",
        ""
    ])

    # Generate regions for each instrument
    for inst, count in sorted(sample_counts.items()):
        inst_full = BLOFELD_INSTRUMENTS.get(inst, inst)
        mapping = calculate_velocity_mapping(count, inst_full)

        sfz_lines.append(f"// {inst_full.upper()} ({inst}) - {count} samples")

        if inst_full == "percussion":
            # Special: Map percussion to different keys
            generate_percussion_regions(sfz_lines, count)
        else:
            # Standard velocity layering
            generate_velocity_regions(sfz_lines, inst, inst_full, mapping)

        sfz_lines.append("")

    return "\n".join(sfz_lines)


def generate_velocity_regions(sfz_lines: List[str], inst: str, inst_full: str, mapping: Dict):
    """Generate SFZ regions with velocity layers"""

    midi_key = GM_MAPPING.get(inst_full, 60)  # Default to C3 if not in GM map

    for layer in mapping["ranges"]:
        # Use samples from this layer
        # We'll use the middle sample from each velocity range
        sample_idx = (layer["sample_start"] + layer["sample_end"]) // 2

        # Sample naming: cw_blofeld_{inst}{number:02d}.wav
        sample_num = sample_idx + 1  # 1-indexed
        sample_name = f"cw_blofeld_{inst}{sample_num:02d}.wav"

        lovel = layer["lovel"]
        hivel = layer["hivel"]

        sfz_lines.extend([
            f"<region>",
            f"  sample={sample_name}",
            f"  lokey={midi_key} hikey={midi_key}",
            f"  lovel={lovel} hivel={hivel}",
            f"  pitch_keycenter={midi_key}",
            ""
        ])


def generate_percussion_regions(sfz_lines: List[str], count: int):
    """Generate SFZ regions for percussion (key mapping)"""

    # Map percussion samples to keys starting at C3 (60)
    start_key = 60
    for i in range(count):
        midi_key = start_key + i
        sample_num = i + 1  # 1-indexed
        sample_name = f"cw_blofeld_perc{sample_num:02d}.wav"

        sfz_lines.extend([
            f"<region>",
            f"  sample={sample_name}",
            f"  lokey={midi_key} hikey={midi_key}",
            f"  pitch_keycenter={midi_key}",
            ""
        ])


# ==============================================================================
# Sample Organization
# ==============================================================================

def organize_blofeld_samples():
    """Organize Blofeld samples for SF2 creation"""
    print("🎼 Organizing Blofeld samples...")

    source_path = Path(SOURCE_DIR)
    dest_path = Path(BUILD_DIR)

    # Create destination directory
    dest_path.mkdir(parents=True, exist_ok=True)

    # Copy all samples to destination (flat structure)
    samples_copied = 0
    for wav_file in source_path.glob("*.wav"):
        dest_file = dest_path / wav_file.name
        if not dest_file.exists():
            import shutil
            shutil.copy2(wav_file, dest_file)
            samples_copied += 1

    print(f"✅ Copied {samples_copied} samples to {BUILD_DIR}")

    return samples_copied


# ==============================================================================
# Main
# ==============================================================================

def main():
    """Main execution"""
    print("=" * 70)
    print("Blofeld Adaptive Velocity Layer Calculator")
    print("=" * 70)
    print()

    # Step 1: Analyze samples
    sample_counts = analyze_blofeld_samples()
    if not sample_counts:
        print("❌ No samples found!")
        return

    print()

    # Step 2: Organize samples
    organize_blofeld_samples()
    print()

    # Step 3: Generate SFZ
    sfz_content = generate_blofeld_sfz(sample_counts)

    # Write SFZ file
    dest_path = Path(BUILD_DIR)
    sfz_file = dest_path / "blofeld_adaptive.sfz"

    with open(sfz_file, "w") as f:
        f.write(sfz_content)

    print(f"✅ SFZ file created: {sfz_file}")
    print()

    # Step 4: Print summary
    print("=" * 70)
    print("📊 Summary:")
    print("=" * 70)

    for inst, count in sorted(sample_counts.items()):
        inst_full = BLOFELD_INSTRUMENTS.get(inst, inst)
        mapping = calculate_velocity_mapping(count, inst_full)

        print(f"\n{inst_full.upper()} ({inst}):")
        print(f"  Total samples: {count}")
        print(f"  Strategy: {mapping['strategy']}")
        print(f"  Layers: {mapping['num_layers']}")

        if mapping['strategy'] == 'velocity_layers':
            print(f"  Velocity ranges:")
            for layer in mapping["ranges"]:
                print(f"    Layer {layer['layer']}: vel {layer['lovel']:3}-{layer['hivel']:3} "
                      f"(samples {layer['sample_start']}-{layer['sample_end']-1})")
        else:
            print(f"  Mapping: Keys 60-{60 + count - 1}")

    print()
    print("=" * 70)
    print("✅ Blofeld organization complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Review organized samples in: piano_workshop/build/drum_kits/blofeld_adaptive/")
    print("2. Open Polyphone")
    print("3. File → Import → SFZ → Select blofeld_adaptive.sfz")
    print("4. Verify velocity layers")
    print("5. File → Export → SoundFont2")
    print("6. Save as: piano_workshop/dist/drum_kits/blofeld_drums.sf2")


if __name__ == "__main__":
    main()
