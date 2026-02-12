#!/usr/bin/env python3
"""
Synth/Electronic Drum Organizer
Handles: Drum Hits, Synth Drums, Techno Drums
"""

import os
import shutil
from pathlib import Path

SYNTH_COLLECTIONS = {
    "drum_hits": {
        "source": "/Volumes/Storage/samples/retro drum-machine/Drums Hits",
        "dest": "piano_workshop/build/drum_kits/drum_hits",
        "name": "Drum Hits"
    },
    "synth_drums": {
        "source": "/Volumes/Storage/samples/retro drum-machine/synthdrums",
        "dest": "piano_workshop/build/drum_kits/synth_drums",
        "name": "Synth Drums"
    },
    "techno_drums": {
        "source": "/Volumes/Storage/samples/retro drum-machine/techno drum samples",
        "dest": "piano_workshop/build/drum_kits/techno_drums",
        "name": "Techno Drums"
    },
}

def copy_flat_samples(source_dir: Path, dest_dir: Path) -> int:
    """Copy all WAV files to single directory"""
    print(f"  Copying from {source_dir.name}")

    if not source_dir.exists():
        print(f"  ❌ Source not found")
        return 0

    dest_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for wav_file in source_dir.glob("**/*.wav"):
        dest_file = dest_dir / wav_file.name
        if not dest_file.exists():
            shutil.copy2(wav_file, dest_file)
            count += 1
        else:
            count += 1

    print(f"    ✅ Copied {count} samples")
    return count

def generate_simple_sfz(machine_id: str, machine_name: str, dest_dir: Path, sample_count: int):
    """Generate simple SFZ mapped across keyboard"""
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

    # Map across GM drum range (35-60) plus some extras
    start_note = 35
    notes_per_sample = max(1, 26 // len(samples)) if samples else 1

    for idx, sample in enumerate(samples):
        midi_note = start_note + (idx * notes_per_sample)
        if midi_note > 87:  # Don't go too high
            midi_note = 60 + (idx % 12)

        rel_path = sample.name
        sfz_content += f"<region> sample={rel_path} lokey={midi_note} hikey={midi_note} lovel=0 hivel=127 pitch_keycenter={midi_note}\n"

    with open(sfz_file, "w") as f:
        f.write(sfz_content)

    print(f"  ✅ SFZ created: {sfz_file.name} ({sample_count} samples)")

def main():
    print("="*70)
    print("SYNTH/ELECTRONIC DRUM ORGANIZER")
    print("="*70)
    print()

    total_samples = 0

    for machine_id, config in SYNTH_COLLECTIONS.items():
        print(f"\n{'='*70}")
        print(f"Processing {config['name']}")
        print(f"{'='*70}")

        source = Path(config["source"])
        dest = Path(config["dest"])

        # Clean destination if exists
        if dest.exists():
            shutil.rmtree(dest)

        # Copy samples
        count = copy_flat_samples(source, dest)
        total_samples += count

        # Generate SFZ
        if count > 0:
            generate_simple_sfz(machine_id, config['name'], dest, count)
            print(f"  ✅ {config['name']} complete!")
        else:
            print(f"  ⚠️  {config['name']} had no samples")

    print("\n" + "="*70)
    print(f"SYNTH/ELECTRONIC DRUMS COMPLETE! ({total_samples} total samples)")
    print("="*70)

if __name__ == "__main__":
    main()
