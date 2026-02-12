#!/usr/bin/env python3
"""
Modern Digital Drum Organizer
Handles: Vermona DRM-1, Alesis SR-16/XL7
"""

import os
import shutil
from pathlib import Path

MACHINES = {
    "vermona_drm1": {
        "source": "/Volumes/Storage/samples/retro drum-machine/Vermona DRM-1",
        "dest": "piano_workshop/build/drum_kits/vermona_drm1",
        "name": "Vermona DRM-1",
        "split": True  # Will need to split this massive collection
    },
    "alesis_sr16": {
        "source": "/Volumes/Storage/samples/retro drum-machine/xl7 drumkit",
        "dest": "piano_workshop/build/drum_kits/alesis_sr16",
        "name": "Alesis SR-16/XL7",
        "split": False
    },
}

def copy_samples_with_subdirs(source_dir: Path, dest_dir: Path) -> dict:
    """Copy all samples maintaining folder structure"""
    print(f"  Copying from {source_dir}")

    if not source_dir.exists():
        print(f"  ❌ Source not found: {source_dir}")
        return {}

    dest_dir.mkdir(parents=True, exist_ok=True)
    instrument_counts = {}
    total_copied = 0

    # Copy each instrument folder
    for inst_folder in source_dir.iterdir():
        if not inst_folder.is_dir() or inst_folder.name.startswith('.'):
            continue

        # Create destination instrument folder
        inst_dest = dest_dir / inst_folder.name.lower().replace(' ', '_')
        inst_dest.mkdir(exist_ok=True)

        # Copy all WAV files (both .wav and .WAV)
        count = 0
        for wav_file in list(inst_folder.glob("*.wav")) + list(inst_folder.glob("*.WAV")):
            dest_file = inst_dest / wav_file.name
            if not dest_file.exists():
                shutil.copy2(wav_file, dest_file)
                count += 1
            else:
                count += 1

        instrument_counts[inst_folder.name] = count
        total_copied += count
        if count > 0:
            print(f"    ✅ {inst_folder.name:30}: {count:4} samples")

    print(f"  Total: {total_copied} samples")
    return instrument_counts

def generate_sfz(machine_name: str, dest_dir: Path, inst_counts: dict):
    """Generate SFZ file"""
    sfz_file = dest_dir / f"{machine_name.lower().replace(' ', '_')}.sfz"

    sfz_content = f"""// {machine_name.replace('_', ' ').title()} GM Standard Mapping
// Auto-generated SFZ

<control> set_cc7=127

<global>
ampeg_attack=0.001
ampeg_decay=0.1
ampeg_sustain=100
ampeg_release=0.3

"""

    # Basic GM mappings
    midi_map = {
        "kick": 36, "kick_drum": 36, "bd": 36, "bass_drum": 36,
        "snare": 38, "snare_drum": 38, "sd": 38,
        "hihat": 42, "hi_hat": 42, "hh": 42, "closed_hat": 42, "ch": 42,
        "open_hat": 46, "open_hihat": 46, "oh": 46,
        "tom": 43, "toms": 43,
        "clap": 39,
        "cymbal": 49, "cymbals": 49,
        "rim": 37, "rimshot": 37,
        "cowbell": 56,
        "perc": 60, "percussion": 60,
    }

    for inst_name, count in inst_counts.items():
        if count == 0:
            continue

        inst_lower = inst_name.lower().replace(' ', '_')
        midi_note = midi_map.get(inst_lower, 60)

        inst_dir = dest_dir / inst_lower
        if not inst_dir.exists():
            continue

        samples = sorted(inst_dir.glob("*.wav"))
        if not samples:
            continue

        # Add regions
        for i, sample in enumerate(samples):
            if count > 1:
                range_size = 128 // count
                vel_start = i * range_size
                vel_end = ((i + 1) * range_size) - 1 if i < count - 1 else 127
            else:
                vel_start, vel_end = 0, 127

            rel_path = f"{inst_lower}/{sample.name}"
            sfz_content += f"<region> sample={rel_path} lokey={midi_note} hikey={midi_note} lovel={vel_start} hivel={vel_end} pitch_keycenter={midi_note}\n"

    with open(sfz_file, "w") as f:
        f.write(sfz_content)

    print(f"  ✅ SFZ created: {sfz_file.name}")

def main():
    print("="*70)
    print("MODERN DIGITAL DRUM ORGANIZER")
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
        inst_counts = copy_samples_with_subdirs(source, dest)

        # Generate SFZ
        if inst_counts:
            generate_sfz(machine_id, dest, inst_counts)
            print(f"  ✅ {config['name']} complete!")
        else:
            print(f"  ⚠️  {config['name']} failed - no samples found")

    print("\n" + "="*70)
    print("MODERN DIGITAL DRUMS COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    main()
