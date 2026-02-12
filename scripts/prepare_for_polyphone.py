#!/usr/bin/env python3
"""
Reorganize drum kits for Polyphone import
Creates flat directory structure with all samples + SFZ
"""

import os
import shutil
from pathlib import Path

# GM Standard Drum Mapping
GM_MAPPING = {
    35: ("clave", 35),
    36: ("kick", 36),
    37: ("rimshot", 37),
    38: ("snare", 38),
    39: ("clap", 39),
    40: ("tom", 40),  # usually not used
    41: ("tom", 41),  # usually not used
    42: ("closed_hat", 42),
    43: ("tom", 43),  # low tom
    44: ("hihat", 44),  # usually not used
    45: ("tom", 45),  # mid tom
    46: ("open_hat", 46),
    47: ("tom", 47),  # high tom
    48: ("cymbal", 48),  # usually not used
    49: ("crash", 49),  # cymbal
    50: ("tom", 50),  # usually not used
    51: ("cymbal", 51),  # ride
    52: ("cymbal", 52),  # chinese cymbal or similar
    53: ("cymbal", 53),  # ride bell
    54: ("cymbal", 54),  # usually not used
    55: ("cymbal", 55),  # usually not used
    56: ("cowbell", 56),
    57: ("cymbal", 57),  # usually not used
    58: ("cymbal", 58),  # usually not used
}

def create_flat_kit(source_dir, output_dir, kit_name):
    """Create flat directory structure for Polyphone"""
    source = Path(source_dir)
    output = Path(output_dir)
    flat_dir = output / kit_name

    # Clean and create
    if flat_dir.exists():
        shutil.rmtree(flat_dir)
    flat_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Preparing: {kit_name}")
    print(f"{'='*60}")

    # Find all WAV files
    wav_files = list(source.rglob("*.wav"))
    print(f"Found {len(wav_files)} samples")

    # Copy all samples to flat directory
    samples_added = []
    for wav in wav_files:
        dest = flat_dir / wav.name
        if not dest.exists():
            shutil.copy2(wav, dest)
            samples_added.append(wav.name)

    print(f"Copied {len(samples_added)} samples to flat directory")

    # Generate SFZ
    sfz_content = generate_simple_sfz(kit_name, samples_added)
    sfz_path = flat_dir / f"{kit_name}.sfz"

    with open(sfz_path, 'w') as f:
        f.write(sfz_content)

    print(f"Created SFZ: {sfz_path.name}")
    print(f"✅ Ready for Polyphone!")

    return flat_dir

def generate_simple_sfz(kit_name, sample_list):
    """Generate simple SFZ that references all samples"""
    # This is a placeholder - would need smarter mapping
    sfz = f"// {kit_name} - Polyphone Ready\n\n<global>\nampeg_release=0.3\n\n"

    # Add all samples with basic mapping
    # In production, would map to GM keys properly
    for i, sample in enumerate(sorted(sample_list)):
        key = 36 + (i % 20)  # Simple distribution
        sfz += f'<region> sample={sample} lokey={key} hikey={key} pitch_keycenter={key}\n'

    return sfz

def main():
    workshop = Path("/Users/bretbouchard/apps/schill/juce_backend/Sam_sampler/piano_workshop/piano_workshop")
    source_base = workshop / "build/drum_kits"
    output_base = workshop / "build/drum_kits_flat"

    # Test with TR-808
    tr808_source = source_base / "tr808_gm"

    if tr808_source.exists():
        create_flat_kit(tr808_source, output_base, "roland_tr808")
    else:
        print(f"Source not found: {tr808_source}")

if __name__ == "__main__":
    main()
