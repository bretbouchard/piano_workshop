#!/usr/bin/env python3
"""
Vintage & Custom Drum Organizer
Handles: R100 Collection, Home Made Drum Kit
"""

import os
import shutil
from pathlib import Path

VINTAGE_COLLECTIONS = {
    "r100": {
        "source": "/Volumes/Storage/samples/R100",
        "dest": "piano_workshop/build/drum_kits/r100_collection",
        "name": "R100 Collection"
    },
    "home_made": {
        "source": "/Volumes/Storage/samples/odd_sounds/Home Made Drum Kit #1",
        "dest": "piano_workshop/build/drum_kits/home_made_kit",
        "name": "Home Made Drum Kit #1"
    },
}

def copy_samples_recursive(source_dir: Path, dest_dir: Path) -> int:
    """Recursively copy all WAV files"""
    print(f"  Copying from {source_dir.name}")

    if not source_dir.exists():
        print(f"  ❌ Source not found")
        return 0

    dest_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for wav_file in source_dir.glob("**/*.wav"):
        # Create flat structure with unique names
        dest_file = dest_dir / wav_file.name
        counter = 1
        while dest_file.exists():
            name_parts = wav_file.stem
            ext = wav_file.suffix
            dest_file = dest_dir / f"{name_parts}_{counter}{ext}"
            counter += 1

        shutil.copy2(wav_file, dest_file)
        count += 1

    print(f"    ✅ Copied {count} samples")
    return count

def generate_vintage_sfz(machine_id: str, machine_name: str, dest_dir: Path, sample_count: int):
    """Generate SFZ for vintage collections"""
    sfz_file = dest_dir / f"{machine_id}.sfz"

    sfz_content = f"""// {machine_name} GM Standard Mapping
// Auto-generated SFZ

<control> set_cc7=127

<global>
ampeg_attack=0.001
ampeg_decay=0.1
ampeg_sustain=100
ampeg_release=0.3

"""

    samples = sorted(dest_dir.glob("*.wav"))
    if not samples:
        return

    # Map across drum range
    start_note = 35
    samples_per_note = max(1, 30 // len(samples)) if samples else 1

    for idx, sample in enumerate(samples):
        midi_note = start_note + (idx // samples_per_note)
        if midi_note > 87:
            midi_note = 60 + (idx % 20)

        rel_path = sample.name
        sfz_content += f"<region> sample={rel_path} lokey={midi_note} hikey={midi_note} lovel=0 hivel=127 pitch_keycenter={midi_note}\n"

    with open(sfz_file, "w") as f:
        f.write(sfz_content)

    print(f"  ✅ SFZ created: {sfz_file.name} ({sample_count} samples)")

def main():
    print("="*70)
    print("VINTAGE & CUSTOM DRUM ORGANIZER")
    print("="*70)
    print()

    total_samples = 0

    for machine_id, config in VINTAGE_COLLECTIONS.items():
        print(f"\n{'='*70}")
        print(f"Processing {config['name']}")
        print(f"{'='*70}")

        source = Path(config["source"])
        dest = Path(config["dest"])

        # Clean destination if exists
        if dest.exists():
            shutil.rmtree(dest)

        # Copy samples
        count = copy_samples_recursive(source, dest)
        total_samples += count

        # Generate SFZ
        if count > 0:
            generate_vintage_sfz(machine_id, config['name'], dest, count)
            print(f"  ✅ {config['name']} complete!")
        else:
            print(f"  ⚠️  {config['name']} had no samples")

    print("\n" + "="*70)
    print(f"VINTAGE & CUSTOM DRUMS COMPLETE! ({total_samples} total samples)")
    print("="*70)

if __name__ == "__main__":
    main()
