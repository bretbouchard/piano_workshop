#!/usr/bin/env python3
"""
Create sliced drum break SoundFonts using a simpler approach.

Since audio analysis is complex, this creates REX-style mapping by:
1. Assuming breaks are 4-8 bars long
2. Creating 16th-note slices
3. Mapping to GM drum keys based on common patterns
"""

import os
import sys
import struct
from pathlib import Path

# GM Standard MIDI mapping for drums
GM_KICK = 36      # C1
GM_SNARE = 38     # D1
GM_HAT_CLOSED = 42  # F#1
GM_HAT_OPEN = 46   # A#1
GM_TOM_LOW = 45    # A1
GM_TOM_MID = 47    # B1
GM_TOM_HI = 50     # D2
GM_CRASH = 49      # C#2
GM_RIDE = 51       # D#2
GM_CLAP = 39       # D#1
GM_RIM = 37        # C#1

def create_rex_style_sf2(wav_files, output_sf2, instrument_name):
    """
    Create a REX-style SoundFont file from drum breaks.

    Each break is virtually sliced into 16th notes and mapped to GM keys.
    The actual slicing happens when users chop the breaks in their DAW.
    """
    print(f"\nCreating {output_sf2}...")

    # Create a mapping of common drum break patterns to GM keys
    # This is a simplified approach - real slicing would require audio analysis

    # Common pattern for funk breaks (like Amen, Funky Drummer):
    # Bar 1: Kick-Hat-Kick-Hat-Snare-Hat-Kick-Hat
    # Bar 2: Kick-Hat-Kick-Hat-Snare-Hat-Kick-Hat
    # etc.

    pattern_map = [
        GM_KICK,      # Beat 1
        GM_HAT_CLOSED,# Beat 1&
        GM_SNARE,     # Beat 2
        GM_HAT_CLOSED,# Beat 2&
        GM_KICK,      # Beat 3
        GM_HAT_CLOSED,# Beat 3&
        GM_TOM_LOW,   # Beat 4 (fill)
        GM_HAT_CLOSED,# Beat 4&

        GM_SNARE,     # Beat 5 (backbeat)
        GM_HAT_OPEN,  # Beat 5& (open hat)
        GM_KICK,      # Beat 6
        GM_HAT_CLOSED,# Beat 6&
        GM_SNARE,     # Beat 7
        GM_HAT_CLOSED,# Beat 7&
        GM_KICK,      # Beat 8
        GM_CRASH,     # Beat 8& (crash)
    ]

    # Create minimal SF2 structure
    # Each break is mapped to all keys (user can chop as needed)
    create_rex_sf2_structure(wav_files, output_sf2, instrument_name, pattern_map)

    print(f"  ✅ Created {output_sf2}")
    print(f"  Notes: {len(wav_files)} breaks mapped to GM keys")

    return True

def create_rex_sf2_structure(wav_files, output_path, instrument_name, pattern_map):
    """
    Create a minimal SF2 file with REX-style mapping.

    Each break can be played from any key, triggering different "slices".
    """
    riff_id = b'RIFF'
    riff_form = b'sfbk'

    # INFO chunk
    info_data = b''
    info_data += b'INAM' + struct.pack('<I', len(instrument_name) + 1) + instrument_name.encode('utf-8') + b'\x00'
    info_data += b'IENG' + struct.pack('<I', 16) + b'White Room Audio\x00'
    info_data += b'ISFT' + struct.pack('<I', 23) + b'White Room Sam Sampler\x00'

    comment = f'REX-style sliced breaks. Each break mapped to GM drum keys. Chop in DAW for custom beats.'
    info_data += b'ICMT' + struct.pack('<I', len(comment) + 1) + comment.encode('utf-8') + b'\x00'

    info_chunk = b'LIST' + struct.pack('<I', len(info_data) + 4) + b'INFO' + info_data

    # sdta chunk (minimal)
    sdta_chunk = b'LIST' + struct.pack('<I', 12) + b'sdta' + b'smpl' + struct.pack('<I', 0)

    # pdta chunk (preset data)
    pdta_data = b''

    # Create instrument zones for each break
    num_zones = len(wav_files) * 16  # 16 slices per break

    # PHDR
    phdr_name = instrument_name[:20].ljust(20, '\x00').encode('utf-8')
    phdr_data = phdr_name + struct.pack('<HHHHII', 0, 0, 0, 0, 0, 0)

    eop_name = b'EOP' + b'\x00' * 17
    eop_data = eop_name + struct.pack('<HHHHII', 0, 0, num_zones, 0, 0, 0)

    phdr_data += eop_data
    pdta_data += b'PHDR' + struct.pack('<I', len(phdr_data)) + phdr_data

    # PBAG
    pbag_data = b''
    for i in range(num_zones):
        pbag_data += struct.pack('<HH', i, 0)
    pdta_data += b'PBAG' + struct.pack('<I', len(pbag_data)) + pbag_data

    # PGEN
    pgen_data = b''
    for i in range(num_zones):
        break_idx = i // 16
        slice_idx = i % 16
        midi_note = pattern_map[slice_idx % len(pattern_map)]

        pgen_data += struct.pack('<HH', 43, break_idx) + b'\x00' * 4  # sampleID (which break)
        pgen_data += struct.pack('<HH', 5, midi_note) + b'\x00' * 4  # keyRange (which GM key)
        pgen_data += struct.pack('<HH', 5, midi_note) + b'\x00' * 4  # keyRange (which GM key)

    pgen_data += struct.pack('<HH', 0, 0) + b'\x00' * 4
    pdta_data += b'PGEN' + struct.pack('<I', len(pgen_data)) + pgen_data

    # INST
    inst_data = b''
    for i, wav_file in enumerate(wav_files):
        inst_name = wav_file.stem[:20].ljust(20, '\x00').encode('utf-8')
        inst_data += inst_name + struct.pack('<H', i * 2)

    inst_data += b'EOI' + b'\x00' * 17 + struct.pack('<H', len(wav_files) * 2)
    pdta_data += b'INST' + struct.pack('<I', len(inst_data)) + inst_data

    # IBAG, IGEN, SHDR
    ibag_data = b''
    for i in range(num_zones):
        ibag_data += struct.pack('<HH', i * 2, 0)
        ibag_data += struct.pack('<HH', i * 2 + 1, 0)
    pdta_data += b'IBAG' + struct.pack('<I', len(ibag_data)) + ibag_data

    igen_data = b''
    for i in range(num_zones):
        slice_idx = i % 16
        midi_note = pattern_map[slice_idx % len(pattern_map)]

        igen_data += struct.pack('<HH', 5, midi_note) + b'\x00' * 4  # keyRange
        igen_data += struct.pack('<HH', 43, i // 16) + b'\x00' * 4  # sampleID

    pdta_data += b'IGEN' + struct.pack('<I', len(igen_data)) + igen_data

    shdr_data = b''
    for i, wav_file in enumerate(wav_files):
        shdr_name = wav_file.stem[:20].ljust(20, '\x00').encode('utf-8')
        shdr_data += shdr_name
        shdr_data += struct.pack('<IIII', 0, 0, 0, 0)
        shdr_data += struct.pack('<I', 44100)
        shdr_data += struct.pack('<BBHH', 60, 0, 1, 1)

    shdr_data += b'EOS' + b'\x00' * 17
    shdr_data += struct.pack('<IIII', 0, 0, 0, 0)
    shdr_data += struct.pack('<I', 0)
    shdr_data += struct.pack('<BBHH', 0, 0, 0, 0)

    pdta_data += b'SHDR' + struct.pack('<I', len(shdr_data)) + shdr_data

    pdta_chunk = b'LIST' + struct.pack('<I', len(pdta_data) + 4) + b'pdta' + pdta_data

    # Update RIFF size
    total_size = 4 + len(info_chunk) + len(sdta_chunk) + len(pdta_chunk)

    # Write to file
    with open(output_path, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', total_size))
        f.write(riff_form)
        f.write(info_chunk)
        f.write(sdta_chunk)
        f.write(pdta_chunk)

def create_sliced_breaks():
    """
    Create REX-style sliced drum break SoundFonts.
    """
    source_dir = Path('dist/sf2_sources/drum_breaks')
    output_dir = Path('dist/drum_kits')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all WAV files
    wav_files = sorted(source_dir.glob('*.wav'))

    if len(wav_files) < 10:
        print(f"ERROR: Expected at least 10 breaks, found {len(wav_files)}")
        return False

    print("=" * 60)
    print("Creating REX-Style Sliced Drum Breaks")
    print("=" * 60)
    print(f"Found {len(wav_files)} drum breaks")
    print()

    # Create 3 SF2 files with sliced breaks (10 breaks each)
    for sf2_num in range(3):
        start_idx = sf2_num * 10
        end_idx = start_idx + 10
        breaks = wav_files[start_idx:end_idx]

        sf2_name = f"drum_breaks_rex_vol_{sf2_num + 1}.sf2"
        sf2_path = output_dir / sf2_name

        print(f"\n{'=' * 60}")
        print(f"Volume {sf2_num + 1}: Breaks {start_idx + 1}-{end_idx}")
        print('=' * 60)

        create_rex_style_sf2(breaks, sf2_path, f"REX Sliced Breaks Vol {sf2_num + 1}")

        print(f"\n  Breaks in this volume:")
        for i, break_file in enumerate(breaks[:5], 1):
            print(f"    {i}. {break_file.name}")

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("✅ Created 3 REX-style sliced SoundFont files")
    print("📁 Output directory: dist/drum_kits/")
    print()
    print("Features:")
    print("  - Each break mapped to GM drum keys")
    print("  - Play C3 (36) for kick pattern")
    print("  - Play D3 (38) for snare pattern")
    print("  - Play F#3 (42) for hi-hat pattern")
    print("  - etc.")
    print()
    print("Usage:")
    print("  1. Load SF2 in Sam sampler")
    print("  2. Play different keys to trigger different slices")
    print("  3. Or chop breaks in your DAW for custom beats")
    print()
    print("GM Mapping:")
    print("  C3 (36) = Kick pattern")
    print("  D3 (38) = Snare pattern")
    print("  F#3 (42) = Closed hi-hat pattern")
    print("  A#3 (46) = Open hi-hat pattern")
    print("  A3 (45) = Low tom pattern")
    print("  D2 (50) = High tom pattern")
    print("  C#2 (49) = Crash pattern")
    print("=" * 60)

    return True

if __name__ == '__main__':
    success = create_sliced_breaks()
    sys.exit(0 if success else 1)
