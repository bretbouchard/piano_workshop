#!/usr/bin/env python3
"""
Organize Drum Samples for SF2 Creation

This script organizes raw drum machine samples into the GM Standard
structure required for creating SF2 files.

Usage:
    python3 organize_drum_samples.py
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List

# ==============================================================================
# Configuration
# ==============================================================================

SOURCE_DIR = "/Volumes/Storage/samples"
BUILD_DIR = "piano_workshop/build/drum_kits"

# GM Standard Drum Mapping (MIDI key → drum name)
GM_MAPPING = {
    35: "Kick_2",
    36: "Kick",
    37: "Snare_2_Rimshot",
    38: "Snare",
    39: "Hand_Clap",
    40: "Tom_2",
    41: "Tom_2",
    42: "Closed_Hat",
    43: "Tom_3",
    44: "HiHat_Pedal",
    45: "Tom_1",
    46: "Open_Hat",
    47: "Tom_3",
    48: "Crash_Cymbal",
    49: "Ride_Cymbal",
    50: "Tambourine",
}

# ==============================================================================
# TR-808 Organization
# ==============================================================================

def organize_808() -> bool:
    """Organize TR-808 samples into GM structure"""
    print("🎸 Organizing TR-808 samples...")

    src_base = Path(SOURCE_DIR) / "Roland - JeuneLys_Beatz" / "ROLAND_TR-808_(1980)"
    dest_base = Path(BUILD_DIR) / "tr808_gm"

    if not src_base.exists():
        print(f"❌ Source directory not found: {src_base}")
        return False

    # Create destination directories
    (dest_base / "kick").mkdir(parents=True, exist_ok=True)
    (dest_base / "snare").mkdir(parents=True, exist_ok=True)
    (dest_base / "closed_hat").mkdir(parents=True, exist_ok=True)
    (dest_base / "open_hat").mkdir(parents=True, exist_ok=True)
    (dest_base / "tom_low").mkdir(parents=True, exist_ok=True)
    (dest_base / "tom_mid").mkdir(parents=True, exist_ok=True)
    (dest_base / "tom_high").mkdir(parents=True, exist_ok=True)
    (dest_base / "clap").mkdir(parents=True, exist_ok=True)
    (dest_base / "cowbell").mkdir(parents=True, exist_ok=True)
    (dest_base / "conga").mkdir(parents=True, exist_ok=True)
    (dest_base / "cymbal").mkdir(parents=True, exist_ok=True)
    (dest_base / "rimshot").mkdir(parents=True, exist_ok=True)
    (dest_base / "clave").mkdir(parents=True, exist_ok=True)
    (dest_base / "maracas").mkdir(parents=True, exist_ok=True)

    # Organize samples based on folder structure
    folders = {
        "kick": ["[BD]_Bass_Drum_(808s)", "[BD]_Bass_Drum_(Kick)"],
        "snare": ["[SD]_Snare_Drum"],
        "closed_hat": ["[CH]_Closed_Hat"],
        "open_hat": ["[OH]_Open_Hat"],
        "tom_low": ["[LT]_Low_Tom"],
        "tom_mid": ["[MT]_Mid_Tom"],
        "tom_high": ["[HT]_Hi_Tom"],
        "clap": ["[CP]_Hand_Clap"],
        "cowbell": ["[CB]_Cowbell"],
        "conga": ["[LC]_Low_Conga", "[MC]_Mid_Conga", "[HC]_Hi_Conga"],
        "cymbal": ["[CY]_Cymbal"],
        "rimshot": ["[RS]_Rim_Shot"],
        "clave": ["[CL]_Clave"],
        "maracas": ["[MA]_Maracas"],
    }

    samples_copied = 0

    for dest_name, src_folders in folders.items():
        for src_folder in src_folders:
            src_path = src_base / src_folder
            if not src_path.exists():
                print(f"  ⚠️  Folder not found: {src_folder}")
                continue

            # Copy all WAV files from this folder
            for wav_file in src_path.glob("*.wav"):
                dest_file = dest_base / dest_name / wav_file.name
                shutil.copy2(wav_file, dest_file)
                samples_copied += 1

                # Rename to GM standard naming
                gm_name = convert_to_gm_naming(wav_file.name, dest_name)
                gm_path = dest_base / dest_name / gm_name
                if gm_path != dest_file:
                    if gm_path.exists():
                        os.remove(gm_path)
                    os.rename(dest_file, gm_path)

    print(f"✅ TR-808 organized: {samples_copied} samples copied")
    return True


def convert_to_gm_naming(filename: str, instrument: str) -> str:
    """Convert original filename to GM standard naming"""
    # Keep extension
    ext = Path(filename).suffix

    # Extract base name without variant
    base = filename.replace(ext, "")

    # GM standard naming: [machine]_[instrument]_[key].wav
    gm_names = {
        "kick": "808_kick_c1",
        "snare": "808_snare_d1",
        "closed_hat": "808_ch_fsharp1",
        "open_hat": "808_oh_asharp1",
        "tom_low": "808_tom1_g1",
        "tom_mid": "808_tom2_a1",
        "tom_high": "808_tom3_b1",
        "clap": "808_clap_dsharp1",
        "cowbell": "808_cowbell_gsharp1",
        "conga": "808_conga",
        "cymbal": "808_cymbal",
        "rimshot": "808_rimshot_csharp1",
        "clave": "808_clave",
        "maracas": "808_maracas",
    }

    gm_name = gm_names.get(instrument, base)

    # Add velocity layer if applicable
    if "v1" in base.lower() or "_1" in base:
        return f"{gm_name}_v1{ext}"
    elif "v2" in base.lower() or "_2" in base:
        return f"{gm_name}_v2{ext}"
    elif "v3" in base.lower() or "_3" in base:
        return f"{gm_name}_v3{ext}"
    else:
        return f"{gm_name}{ext}"


# ==============================================================================
# TR-909 Organization
# ==============================================================================

def organize_909() -> bool:
    """Organize TR-909 samples into GM structure"""
    print("🥁 Organizing TR-909 samples...")

    src_base = Path(SOURCE_DIR) / "Roland - JeuneLys_Beatz" / "ROLAND_TR-909_(1983)"
    dest_base = Path(BUILD_DIR) / "tr909_gm"

    if not src_base.exists():
        print(f"❌ Source directory not found: {src_base}")
        return False

    # Create destination directories
    instruments = ["kick", "snare", "closed_hat", "open_hat", "tom",
                   "clap", "cymbal", "ride", "crash"]

    for inst in instruments:
        (dest_base / inst).mkdir(parents=True, exist_ok=True)

    # TODO: Implement TR-909 specific mapping
    print("⚠️  TR-909 organization not yet implemented")
    return True


# ==============================================================================
# Retro Machines Organization
# ==============================================================================

def organize_retro() -> bool:
    """Organize retro drum machines into single collection"""
    print("👾 Organizing retro drum machines...")

    src_base = Path(SOURCE_DIR) / "retro drum-machine"
    dest_base = Path(BUILD_DIR) / "retro_machines"

    if not src_base.exists():
        print(f"❌ Source directory not found: {src_base}")
        return False

    # Create directories for each machine
    machines = {
        "blofeld drumkit": "blofeld",
        "Vermona DRM-1": "vermona_drm1",
        "xl7 drumkit": "xl7",
        "synthdrums": "synth",
        "techno drum samples": "techno",
    }

    for src_folder, dest_name in machines.items():
        src_path = src_base / src_folder
        dest_path = dest_base / dest_name

        if not src_path.exists():
            print(f"  ⚠️  Folder not found: {src_folder}")
            continue

        dest_path.mkdir(parents=True, exist_ok=True)

        # Copy all samples
        samples_copied = 0
        for wav_file in src_path.glob("*.wav"):
            shutil.copy2(wav_file, dest_path / wav_file.name)
            samples_copied += 1

        print(f"  ✅ {dest_name}: {samples_copied} samples")

    print("✅ Retro machines organized")
    return True


# ==============================================================================
# Generate SFZ Templates
# ==============================================================================

def generate_808_sfz() -> bool:
    """Generate SFZ file for TR-808"""
    print("📝 Generating TR-808 SFZ...")

    dest_base = Path(BUILD_DIR) / "tr808_gm"
    sfz_file = dest_base / "roland_tr808.sfz"

    sfz_content = """// Roland TR-808 GM Standard Mapping
// Generated by organize_drum_samples.py

// Control defaults
<control> set_cc7=127 // Volume
<control> default_path=Samples

// Global settings
<global>
ampeg_attack=0.001
ampeg_decay=0.1
ampeg_sustain=100
ampeg_release=0.3
ampeg_vel2attack=0
ampeg_vel2decay=0
ampeg_vel2release=0

// Kick (C1, MIDI 36) - Bass Drum 1
<region> sample=kick/808_kick_c1_v1.wav lokey=36 hikey=36 lovel=0 hivel=42 pitch_keycenter=36 ampeg_release=0.6
<region> sample=kick/808_kick_c1_v2.wav lokey=36 hikey=36 lovel=43 hivel=84 pitch_keycenter=36 ampeg_release=0.5
<region> sample=kick/808_kick_c1_v3.wav lokey=36 hikey=36 lovel=85 hivel=127 pitch_keycenter=36 ampeg_release=0.4

// Snare (D1, MIDI 38) - Snare Drum 1
<region> sample=snare/808_snare_d1_v1.wav lokey=38 hikey=38 lovel=0 hivel=42 pitch_keycenter=38 ampeg_release=0.3
<region> sample=snare/808_snare_d1_v2.wav lokey=38 hikey=38 lovel=43 hivel=127 pitch_keycenter=38 ampeg_release=0.25

// Closed Hi-Hat (F#1, MIDI 42)
<region> sample=closed_hat/808_ch_fsharp1.wav lokey=42 hikey=42 pitch_keycenter=42 ampeg_release=0.15

// Open Hi-Hat (A#1, MIDI 46)
<region> sample=open_hat/808_oh_asharp1.wav lokey=46 hikey=46 pitch_keycenter=46 ampeg_release=0.5

// Low Tom (G1, MIDI 43)
<region> sample=tom_low/808_tom1_g1.wav lokey=43 hikey=43 pitch_keycenter=43 ampeg_release=0.4

// Mid Tom (A1, MIDI 45)
<region> sample=tom_mid/808_tom2_a1.wav lokey=45 hikey=45 pitch_keycenter=45 ampeg_release=0.35

// High Tom (B1, MIDI 47)
<region> sample=tom_high/808_tom3_b1.wav lokey=47 hikey=47 pitch_keycenter=47 ampeg_release=0.3

// Hand Clap (D#1, MIDI 39)
<region> sample=clap/808_clap_dsharp1.wav lokey=39 hikey=39 pitch_keycenter=39 ampeg_release=0.2

// Cowbell (G#1, MIDI 56)
<region> sample=cowbell/808_cowbell_gsharp1.wav lokey=56 hikey=56 pitch_keycenter=56 ampeg_release=0.3

// Rim Shot (C#1, MIDI 37)
<region> sample=rimshot/808_rimshot_csharp1.wav lokey=37 hikey=37 pitch_keycenter=37 ampeg_release=0.15

// Clave (B0, MIDI 35)
<region> sample=clave/808_clave.wav lokey=35 hikey=35 pitch_keycenter=35 ampeg_release=0.2

// Maracas (C#2, MIDI 49)
<region> sample=maracas/808_maracas.wav lokey=49 hikey=49 pitch_keycenter=49 ampeg_release=0.15
"""

    with open(sfz_file, "w") as f:
        f.write(sfz_content)

    print(f"✅ SFZ file created: {sfz_file}")
    return True


# ==============================================================================
# Main
# ==============================================================================

def main():
    """Main execution"""
    print("=" * 60)
    print("Drum Sample Organization for SF2 Creation")
    print("=" * 60)
    print()

    # Create build directory
    Path(BUILD_DIR).mkdir(parents=True, exist_ok=True)

    # Organize samples
    organize_808()
    print()
    organize_909()
    print()
    organize_retro()
    print()

    # Generate SFZ files
    generate_808_sfz()
    print()

    print("=" * 60)
    print("✅ Organization complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review organized samples in: piano_workshop/build/drum_kits/")
    print("2. Install Polyphone: brew install --cask polyphone")
    print("3. Open Polyphone and import SFZ files")
    print("4. Export as SF2 to: piano_workshop/dist/drum_kits/")


if __name__ == "__main__":
    main()
