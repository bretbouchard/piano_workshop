#!/usr/bin/env python3
import shutil
from pathlib import Path

source_dir = Path("/Volumes/Storage/samples/the_breaks")
target_dir = Path("/Users/bretbouchard/apps/schill/piano_workshop/dist/sf2_sources/drum_breaks")

target_dir.mkdir(parents=True, exist_ok=True)

# Get all WAV files
wav_files = sorted(source_dir.glob("*.wav"))

# Copy first 30 files (skip the 10 we already have)
already_copied = len(list(target_dir.glob("*.wav")))
needed = 30 - already_copied

if needed > 0:
    print(f"Copying {needed} more breaks...")
    for i, wav_file in enumerate(wav_files[already_copied:already_copied+needed]):
        try:
            shutil.copy2(wav_file, target_dir / wav_file.name)
            print(f"✅ {i+1}/{needed}: {wav_file.name}")
        except Exception as e:
            print(f"❌ Error copying {wav_file.name}: {e}")

    print(f"\n✅ Total breaks: {len(list(target_dir.glob('*.wav')))}")
else:
    print(f"✅ Already have {already_copied} breaks!")
