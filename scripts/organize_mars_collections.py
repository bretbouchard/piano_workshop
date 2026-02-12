#!/usr/bin/env python3
"""
Mars Drum Collections Organizer
All 7 Mars collections in one script
"""

import os
import shutil
from pathlib import Path

MARS_COLLECTIONS = {
    "101_drums_mars": {
        "source": "/Volumes/Storage/samples/mars/101 Drums From Mars",
        "dest": "piano_workshop/build/drum_kits/101_drums_mars",
        "name": "101 Drums From Mars"
    },
    "mpc60_mars": {
        "source": "/Volumes/Storage/samples/mars/Free MPC60 From Mars",
        "dest": "piano_workshop/build/drum_kits/mpc60_mars",
        "name": "Free MPC60 From Mars"
    },
    "vinyl_mars": {
        "source": "/Volumes/Storage/samples/mars/Free Vinyl Drums From Mars",
        "dest": "piano_workshop/build/drum_kits/vinyl_mars",
        "name": "Free Vinyl Drums From Mars"
    },
    "808_mars": {
        "source": "/Volumes/Storage/samples/mars/Free 808 From Mars",
        "dest": "piano_workshop/build/drum_kits/808_mars",
        "name": "Free 808 From Mars"
    },
    "drums_mars": {
        "source": "/Volumes/Storage/samples/mars/Free Drums From Mars",
        "dest": "piano_workshop/build/drum_kits/drums_mars",
        "name": "Free Drums From Mars"
    },
    "909_tube": {
        "source": "/Volumes/Storage/samples/mars/909 Tube Kit",
        "dest": "piano_workshop/build/drum_kits/909_tube",
        "name": "909 Tube Kit"
    },
    "ampeg_808": {
        "source": "/Volumes/Storage/samples/mars/Ampeg 808 Kit",
        "dest": "piano_workshop/build/drum_kits/ampeg_808",
        "name": "Ampeg 808 Kit"
    },
}

def copy_all_files(source_dir: Path, dest_dir: Path) -> int:
    """Copy all WAV files from source to destination"""
    print(f"  Copying from {source_dir.name}")

    if not source_dir.exists():
        print(f"  ❌ Source not found")
        return 0

    dest_dir.mkdir(parents=True, exist_ok=True)

    count = 0

    # Check for WAV subdirectory first
    wav_subdir = source_dir / "WAV"
    if wav_subdir.exists() and wav_subdir.is_dir():
        search_dir = wav_subdir
        print(f"    Found WAV subdirectory")
    else:
        search_dir = source_dir

    # Copy all WAV files (recursive)
    for wav_file in search_dir.glob("**/*.wav"):
        dest_file = dest_dir / wav_file.name

        # Handle duplicates
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

def generate_mars_sfz(machine_id: str, machine_name: str, dest_dir: Path, sample_count: int):
    """Generate SFZ for Mars collections (map to GM standard)"""
    sfz_file = dest_dir / f"{machine_id}.sfz"

    sfz_content = f"""// {machine_name} GM Standard Mapping
// Auto-generated SFZ from Mars collection

<control> set_cc7=127

<global>
ampeg_attack=0.001
ampeg_decay=0.1
ampeg_sustain=100
ampeg_release=0.3

"""

    # For Mars collections, we'll do a simple mapping
    # Since these are often mixed kits, we'll map them to a reasonable GM layout

    samples = sorted(dest_dir.glob("*.wav"))
    if not samples:
        return

    # Map samples across GM drum keys
    gm_mapping = [
        (36, "kick"),
        (37, "rimshot"),
        (38, "snare"),
        (39, "clap"),
        (40, "tom"),
        (41, "tom"),
        (42, "hihat"),
        (43, "tom"),
        (44, "hihat"),
        (45, "tom"),
        (46, "hihat_open"),
        (47, "tom"),
        (48, "crash"),
        (49, "crash"),
        (50, "tom"),
        (51, "ride"),
    ]

    # Distribute samples across GM keys
    samples_per_key = max(1, len(samples) // len(gm_mapping))

    for idx, sample in enumerate(samples):
        gm_idx = min(idx // samples_per_key, len(gm_mapping) - 1)
        midi_note, _ = gm_mapping[gm_idx]

        vel_start = 0
        vel_end = 127

        rel_path = sample.name
        sfz_content += f"<region> sample={rel_path} lokey={midi_note} hikey={midi_note} lovel={vel_start} hivel={vel_end} pitch_keycenter={midi_note}\n"

    with open(sfz_file, "w") as f:
        f.write(sfz_content)

    print(f"  ✅ SFZ created: {sfz_file.name} ({sample_count} samples mapped to GM)")

def main():
    print("="*70)
    print("MARS DRUM COLLECTIONS ORGANIZER")
    print("="*70)
    print()

    total_samples = 0

    for machine_id, config in MARS_COLLECTIONS.items():
        print(f"\n{'='*70}")
        print(f"Processing {config['name']}")
        print(f"{'='*70}")

        source = Path(config["source"])
        dest = Path(config["dest"])

        # Clean destination if exists
        if dest.exists():
            shutil.rmtree(dest)

        # Copy samples
        count = copy_all_files(source, dest)
        total_samples += count

        # Generate SFZ
        if count > 0:
            generate_mars_sfz(machine_id, config['name'], dest, count)
            print(f"  ✅ {config['name']} complete!")
        else:
            print(f"  ⚠️  {config['name']} had no samples")

    print("\n" + "="*70)
    print(f"MARS COLLECTIONS COMPLETE! ({total_samples} total samples)")
    print("="*70)

if __name__ == "__main__":
    main()
