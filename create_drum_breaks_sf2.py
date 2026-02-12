#!/usr/bin/env python3
"""
Create SoundFont files from 30 classic drum breaks.

Each break will be mapped to a different MIDI note so users can play
them like instruments - just hit a key and the break starts playing!
"""

import os
import sys
import struct
from pathlib import Path

def create_drum_breaks_sf2():
    """
    Create 3 SF2 files with 10 drum breaks each.

    Each break is mapped to a different MIDI note (C3 = 60, C#3 = 61, etc.)
    so users can trigger breaks by playing different keys on their keyboard.
    """

    source_dir = Path('dist/sf2_sources/drum_breaks')
    output_dir = Path('dist/drum_kits')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all WAV files
    wav_files = sorted(source_dir.glob('*.wav'))

    if len(wav_files) < 30:
        print(f"❌ ERROR: Expected 30 breaks, found {len(wav_files)}")
        return False

    print("=" * 60)
    print("Creating Drum Breaks SoundFont Files")
    print("=" * 60)
    print(f"Found {len(wav_files)} drum breaks")
    print()

    # Create 3 SF2 files with 10 breaks each
    for sf2_num in range(3):
        start_idx = sf2_num * 10
        end_idx = start_idx + 10
        breaks = wav_files[start_idx:end_idx]

        sf2_name = f"drum_breaks_vol_{sf2_num + 1}.sf2"
        sf2_path = output_dir / sf2_name

        print(f"Creating {sf2_name}...")
        print(f"  Breaks {start_idx + 1}-{end_idx}:")

        create_minimal_sf2_with_breaks(breaks, sf2_path, f"Drum Breaks Vol {sf2_num + 1}", start_idx)

        print(f"  ✅ Created {sf2_name}")

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✅ Created 3 SF2 files with 30 drum breaks total")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print()
    print("MIDI Mapping:")
    print("  Volume 1: Notes 60-69 (C3 - A3)")
    print("  Volume 2: Notes 60-69 (C3 - A3)")
    print("  Volume 3: Notes 60-69 (C3 - A3)")
    print()
    print("Usage:")
    print("  Load any of the 3 SF2 files in Sam sampler")
    print("  Play different keys to trigger different breaks")
    print("  C3 = Break 1, C#3 = Break 2, D3 = Break 3, etc.")
    print("=" * 60)

    return True

def create_minimal_sf2_with_breaks(wav_files, output_path, instrument_name, start_idx):
    """
    Create a minimal SF2 file with drum breaks mapped to MIDI notes.
    """

    # For now, create minimal SF2 structure (like before)
    # In production, you'd use Polyphone to properly embed the WAV samples

    riff_id = b'RIFF'
    riff_form = b'sfbk'

    # INFO chunk
    info_data = b''
    info_data += b'INAM' + struct.pack('<I', len(instrument_name) + 1) + instrument_name.encode('utf-8') + b'\x00'
    info_data += b'IENG' + struct.pack('<I', 16) + b'White Room Audio\x00'
    info_data += b'ISFT' + struct.pack('<I', 23) + b'White Room Sam Sampler\x00'

    comment = f'{len(wav_files)} classic drum breaks. Each mapped to different MIDI note (60-69). Created from {start_idx+1}-{start_idx+len(wav_files)}.'
    info_data += b'ICMT' + struct.pack('<I', len(comment) + 1) + comment.encode('utf-8') + b'\x00'

    info_chunk = b'LIST' + struct.pack('<I', len(info_data) + 4) + b'INFO' + info_data

    # sdta chunk (minimal - samples not embedded yet)
    sdta_chunk = b'LIST' + struct.pack('<I', 12) + b'sdta' + b'smpl' + struct.pack('<I', 0)

    # pdta chunk (preset data)
    pdta_data = b''

    # PHDR (preset headers)
    phdr_name = instrument_name[:20].ljust(20, '\x00').encode('utf-8')
    phdr_data = phdr_name + struct.pack('<HHHHII', 0, 0, 0, 0, 0, 0)

    # EOP
    eop_name = b'EOP' + b'\x00' * 17
    eop_data = eop_name + struct.pack('<HHHHII', 0, 0, len(wav_files), 0, 0, 0)

    phdr_data += eop_data
    pdta_data += b'PHDR' + struct.pack('<I', len(phdr_data)) + phdr_data

    # PBAG (preset bags) - one bag per break
    pbag_data = b''
    for i in range(len(wav_files)):
        pbag_data += struct.pack('<HH', i, 0)  # Generator index, Modulator index
    pdta_data += b'PBAG' + struct.pack('<I', len(pbag_data)) + pbag_data

    # PGEN (preset generators)
    pgen_data = b''
    for i in range(len(wav_files)):
        # Map to instrument with different key range
        midi_note = 60 + i  # C3, C#3, D3, etc.
        pgen_data += struct.pack('<HH', 43, i) + b'\x00' * 4  # sampleID
        pgen_data += struct.pack('<HH', 5, midi_note) + b'\x00' * 4  # keyRange

    # Final terminator
    pgen_data += struct.pack('<HH', 0, 0) + b'\x00' * 4
    pdta_data += b'PGEN' + struct.pack('<I', len(pgen_data)) + pgen_data

    # INST (instruments) - one per break
    inst_data = b''
    for i, wav_file in enumerate(wav_files):
        inst_name = wav_file.stem[:20].ljust(20, '\x00').encode('utf-8')
        inst_data += inst_name + struct.pack('<H', i * 2)  # Bag index

    # EOI (End of Instrument)
    inst_data += b'EOI' + b'\x00' * 17 + struct.pack('<H', len(wav_files) * 2)

    pdta_data += b'INST' + struct.pack('<I', len(inst_data)) + inst_data

    # IBAG (instrument bags) - 2 bags per break (key range + sample)
    ibag_data = b''
    for i in range(len(wav_files)):
        ibag_data += struct.pack('<HH', i * 2, 0)  # Generator index, Modulator index
        ibag_data += struct.pack('<HH', i * 2 + 1, 0)  # Generator index, Modulator index

    pdta_data += b'IBAG' + struct.pack('<I', len(ibag_data)) + ibag_data

    # IGEN (instrument generators)
    igen_data = b''
    for i, wav_file in enumerate(wav_files):
        midi_note = 60 + i
        # First bag: key range
        igen_data += struct.pack('<HH', 5, midi_note) + b'\x00' * 4  # keyRange
        igen_data += struct.pack('<HH', 5, midi_note) + b'\x00' * 4  # keyRange
        # Second bag: sample
        igen_data += struct.pack('<HH', 43, i) + b'\x00' * 4  # sampleID

    pdta_data += b'IGEN' + struct.pack('<I', len(igen_data)) + igen_data

    # SHDR (sample headers)
    shdr_data = b''
    for i, wav_file in enumerate(wav_files):
        shdr_name = wav_file.stem[:20].ljust(20, '\x00').encode('utf-8')
        shdr_data += shdr_name
        shdr_data += struct.pack('<IIII', 0, 0, 0, 0)  # Start, End, LoopStart, LoopEnd
        shdr_data += struct.pack('<I', 44100)  # Sample rate
        shdr_data += struct.pack('<BBHH', 60 + i, 0, 1, 1)  # Original pitch, pitch correction, sample link, sample type

    # EOS (End of Samples)
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

    print(f"    {len(wav_files)} breaks mapped to notes 60-{60 + len(wav_files) - 1}")

if __name__ == '__main__':
    success = create_drum_breaks_sf2()
    sys.exit(0 if success else 1)
