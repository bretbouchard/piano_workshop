#!/usr/bin/env python3
"""
Universal Roland Drum Organizer - Simple version
Copies all WAV files and generates basic SFZ
"""

import os
import shutil
from pathlib import Path
import re

# Configuration for all remaining Roland machines
MACHINES = {
    "tr505": {
        "source": "/Volumes/Storage/samples/Roland - JeuneLys_Beatz/ROLAND_TR-505_(1986)",
        "dest": "piano_workshop/build/drum_kits/tr505_gm",
        "name": "TR-505"
    },
    "tr626": {
        "source": "/Volumes/Storage/samples/Roland - JeuneLys_Beatz/ROLAND_TR-626_(1987)",
        "dest": "piano_workshop/build/drum_kits/tr626_gm",
        "name": "TR-626"
    },
    "tr707": {
        "source": "/Volumes/Storage/samples/Roland - JeuneLys_Beatz/ROLAND_TR-707_(1985)",
        "dest": "piano_workshop/build/drum_kits/tr707_gm",
        "name": "TR-707"
    },
}

def copy_all_samples(source_dir: Path, dest_dir: Path) -> dict:
    """Copy all samples maintaining folder structure"""
    print(f"  Copying from {source_dir}")
    print(f"  To {dest_dir}")

    if not source_dir.exists():
        print(f"  ❌ Source not found")
        return {}

    dest_dir.mkdir(parents=True, exist_ok=True)
    instrument_counts = {}
    total_copied = 0

    # Copy each instrument folder
    for inst_folder in source_dir.iterdir():
        if not inst_folder.is_dir():
            continue

        # Skip system files
        if inst_folder.name.startswith('.'):
            continue

        # Create destination instrument folder
        inst_dest = dest_dir / inst_folder.name.lower()
        inst_dest.mkdir(exist_ok=True)

        # Copy all WAV files
        count = 0
        for wav_file in inst_folder.glob("*.wav"):
            dest_file = inst_dest / wav_file.name
            if not dest_file.exists():
                shutil.copy2(wav_file, dest_file)
                count += 1
            else:
                count += 1  # Already exists

        instrument_counts[inst_folder.name] = count
        total_copied += count
        if count > 0:
            print(f"    ✅ {inst_folder.name:20}: {count:3} samples")

    print(f"  Total: {total_copied} samples")
    return instrument_counts

def generate_simple_sfz(machine_name: str, dest_dir: Path, inst_counts: dict):
    """Generate a simple SFZ that just maps all samples"""
    sfz_file = dest_dir / f"roland_{machine_name.lower()}.sfz"

    sfz_content = f"""// {machine_name} GM Standard Mapping
// Auto-generated SFZ

<control> set_cc7=127

<global>
ampeg_attack=0.001
ampeg_decay=0.1
ampeg_sustain=100
ampeg_release=0.3

"""

    # Basic GM mappings (will need manual adjustment)
    midi_map = {
        "kick": 36,      # C1
        "snare": 38,     # D1
        "rim_shot": 37,  # C#1
        "rimshot": 37,
        "hi_hat": 42,    # F#1
        "closed_hat": 42,
        "open_hat": 46,  # A#1
        "open_hats": 46,
        "tom": 43,       # G1
        "clap": 39,      # D#1
        "cymbal": 49,    # C#2/D2
        "cymbals": 49,
        "cowbell": 56,
        "tambourine": 54,
        "perc": 60,      # Various
        "percs": 60,
    }

    # Add regions for each instrument
    for inst_name, count in inst_counts.items():
        inst_lower = inst_name.lower()

        # Skip empty instruments
        if count == 0:
            continue

        # Get MIDI note
        midi_note = midi_map.get(inst_lower, 60)

        # Get first sample file to check naming
        inst_dir = dest_dir / inst_lower
        if not inst_dir.exists():
            continue

        samples = sorted(inst_dir.glob("*.wav"))
        if not samples:
            continue

        # Add regions (all samples at full velocity range for now)
        for i, sample in enumerate(samples):
            vel_start = 0
            vel_end = 127

            # If multiple samples, divide velocity range
            if count > 1:
                range_size = 128 // count
                vel_start = i * range_size
                vel_end = ((i + 1) * range_size) - 1
                if i == count - 1:
                    vel_end = 127

            rel_path = f"{inst_lower}/{sample.name}"
            sfz_content += f"<region> sample={rel_path} lokey={midi_note} hikey={midi_note} lovel={vel_start} hivel={vel_end} pitch_keycenter={midi_note}\n"

    with open(sfz_file, "w") as f:
        f.write(sfz_content)

    print(f"  ✅ SFZ created: {sfz_file.name}")

def main():
    print("="*70)
    print("UNIVERSAL ROLAND DRUM ORGANIZER")
    print("="*70)
    print()

    for machine_id, config in MACHINES.items():
        print(f"\n{'='*70}")
        print(f"Processing {config['name']}")
        print(f"{'='*70}")

        source = Path(config["source"])
        dest = Path(config["dest"])

        # Clean destination if exists
        if dest.exists():
            shutil.rmtree(dest)

        # Copy samples
        inst_counts = copy_all_samples(source, dest)

        # Generate SFZ
        if inst_counts:
            generate_simple_sfz(machine_id, dest, inst_counts)
            print(f"  ✅ {config['name']} complete!")
        else:
            print(f"  ⚠️  {config['name']} failed - no samples found")

    print("\n" + "="*70)
    print("ALL MACHINES PROCESSED!")
    print("="*70)
    print("\nNext steps:")
    print("1. Open Polyphone")
    print("2. Import each SFZ file from piano_workshop/build/drum_kits/")
    print("3. Export as SF2")
    print("4. Save to piano_workshop/dist/drum_kits/")

if __name__ == "__main__":
    main()
