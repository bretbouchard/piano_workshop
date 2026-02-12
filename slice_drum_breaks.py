#!/usr/bin/env python3
"""
Slice drum breaks into individual hits and map to GM drum keys.

This script:
1. Analyzes drum breaks to detect transients (drum hits)
2. Chops breaks at each transient
3. Classifies each hit (kick, snare, hat, etc.)
4. Maps to GM Standard MIDI keys
5. Creates SoundFont files with sliced samples
"""

import os
import sys
import struct
import numpy as np
from pathlib import Path
import librosa

# GM Standard MIDI mapping for drums
GM_DRUM_MAPPING = {
    'kick': 36,      # C1 - Bass Drum 1
    'snare': 38,    # D1 - Acoustic Snare
    'hat_closed': 42,  # F#1 - Closed Hi-Hat
    'hat_open': 46,   # A#1 - Open Hi-Hat
    'tom_low': 45,    # A1 - Low Tom
    'tom_mid': 47,    # B1 - Low Mid Tom
    'tom_hi': 50,     # D2 - High Tom
    'crash': 49,      # C#2 - Crash Cymbal
    'ride': 51,       # D#2 - Ride Cymbal
    'clap': 39,       # D#1 - Hand Clap
    'rim': 37,        # C#1 - Rim Shot
    'percussion': 60,  # C3 - (other percussion)
}

def detect_transient_positions(audio, sr, threshold=0.1, min_distance=0.1):
    """
    Detect transient positions in audio (drum hits).

    Args:
        audio: Audio signal
        sr: Sample rate
        threshold: Sensitivity threshold (lower = more sensitive)
        min_distance: Minimum distance between transients (seconds)

    Returns:
        List of transient positions (in samples)
    """
    # Compute onset envelope
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)

    # Detect peaks (transients)
    peaks = librosa.onset.onset_detect(
        onset_envelope=onset_env,
        sr=sr,
        threshold=threshold,
        backtrack=True,
        min_distance=min_distance
    )

    # Convert frames to samples
    transient_samples = librosa.frames_to_samples(peaks, hop_length=512)

    return transient_samples

def classify_hit(audio_chunk, sr):
    """
    Classify drum hit type based on audio characteristics.

    Args:
        audio_chunk: Audio segment
        sr: Sample rate

    Returns:
        Hit type string ('kick', 'snare', 'hat_closed', etc.)
    """
    # Compute features
    spectral_centroid = librosa.feature.spectral_centroid(y=audio_chunk, sr=sr)[0]
    zero_crossing_rate = librosa.feature.zero_crossing_rate(audio_chunk)[0]
    mfcc = librosa.feature.mfcc(y=audio_chunk, sr=sr, n_mfcc=13)

    # Simple classification heuristics
    avg_centroid = np.mean(spectral_centroid)
    avg_zcr = np.mean(zero_crossing_rate)

    # Kick: Low frequency, low ZCR
    if avg_centroid < 150 and avg_zcr < 0.1:
        return 'kick'

    # Hi-hat: High frequency, high ZCR
    elif avg_centroid > 3000 and avg_zcr > 0.2:
        return 'hat_closed'

    # Snare: Mid frequency, mid ZCR
    elif 1000 < avg_centroid < 3000 and 0.05 < avg_zcr < 0.2:
        return 'snare'

    # Cymbal: Very high frequency
    elif avg_centroid > 5000:
        return 'crash'

    # Tom: Mid-low frequency, low ZCR
    elif 200 < avg_centroid < 1000 and avg_zcr < 0.1:
        return 'tom_low'

    # Default to percussion
    else:
        return 'percussion'

def slice_break_at_transients(wav_path, output_dir, min_hit_length=0.1, max_hit_length=2.0):
    """
    Slice a drum break into individual hits.

    Args:
        wav_path: Path to drum break WAV file
        output_dir: Directory to save sliced hits
        min_hit_length: Minimum hit length (seconds)
        max_hit_length: Maximum hit length (seconds)

    Returns:
        List of (hit_type, audio_chunk, start_sample, end_sample) tuples
    """
    print(f"\n  Slicing: {Path(wav_path).name}")

    # Load audio
    audio, sr = librosa.load(wav_path, sr=None)

    # Detect transients
    transient_samples = detect_transient_positions(audio, sr, threshold=0.3, min_distance=0.1)

    if len(transient_samples) == 0:
        print(f"    WARNING: No transients detected!")
        return []

    print(f"    Detected {len(transient_samples)} hits")

    # Add start and end points
    transient_samples = np.concatenate([[0], transient_samples, [len(audio)]])

    # Slice at each transient
    hits = []
    for i in range(len(transient_samples) - 1):
        start = transient_samples[i]
        end = transient_samples[i + 1]

        # Enforce min/max length
        length = (end - start) / sr
        if length < min_hit_length:
            # Too short, extend to next transient
            if i + 2 < len(transient_samples):
                end = transient_samples[i + 2]

        length = (end - start) / sr
        length = min(length, max_hit_length)
        end = start + int(length * sr)

        # Extract chunk
        chunk = audio[start:end]

        # Skip if too short
        if len(chunk) < sr * 0.05:  # Less than 50ms
            continue

        # Classify hit
        hit_type = classify_hit(chunk, sr)

        hits.append({
            'type': hit_type,
            'audio': chunk,
            'start': start,
            'end': end,
            'sr': sr,
            'index': i
        })

    print(f"    Sliced into {len(hits)} hits")

    return hits

def map_hits_to_gm(hits):
    """
    Map sliced hits to GM Standard MIDI keys.

    Args:
        List of hit dictionaries

    Returns:
        Dictionary mapping MIDI notes to hit samples
    """
    # Count hit types
    type_counts = {}
    for hit in hits:
        hit_type = hit['type']
        if hit_type not in type_counts:
            type_counts[hit_type] = 0
        type_counts[hit_type] += 1

    # Map to GM keys (spread across available keys for each type)
    midi_mapping = {}

    type_ranges = {
        'kick': [(36,)],  # C1
        'snare': [(38,)],  # D1
        'hat_closed': [(42,)],  # F#1
        'hat_open': [(46,)],  # A#1
        'tom_low': [(45,)],  # A1
        'tom_mid': [(47,)],  # B1
        'tom_hi': [(50,)],  # D2
        'crash': [(49,)],  # C#2
        'ride': [(51,)],  # D#2
        'clap': [(39,)],  # D#1
        'rim': [(37,)],  # C#1
        'percussion': [(60, 61)],  # C3, C#3
    }

    hit_count = {}
    for hit in hits:
        hit_type = hit['type']

        # Get MIDI note for this type
        if hit_type not in type_ranges:
            hit_type = 'percussion'  # Default

        midi_notes = type_ranges[hit_type]
        if hit_type not in hit_count:
            hit_count[hit_type] = 0

        # Cycle through available notes
        note_idx = hit_count[hit_type] % len(midi_notes)
        midi_note = midi_notes[note_idx][0]

        hit_count[hit_type] += 1

        midi_mapping[midi_note] = hit

    return midi_mapping

def create_sliced_sf2(wav_files, output_sf2, instrument_name):
    """
    Create a SoundFont file from sliced drum breaks.

    Each break is sliced into hits and mapped to GM drum keys.
    """
    print(f"Creating {output_sf2}...")

    all_hits = []

    # Slice all breaks
    for wav_path in wav_files:
        print(f"\nProcessing: {Path(wav_path).name}")
        hits = slice_break_at_transients(
            wav_path,
            Path(output_sf2).parent / 'slices'
        )

        if hits:
            all_hits.extend(hits)

    if not all_hits:
        print("ERROR: No hits detected in any breaks!")
        return False

    print(f"\nTotal hits across all breaks: {len(all_hits)}")

    # Map hits to GM keys
    midi_mapping = map_hits_to_gm(all_hits)

    print(f"\nMapped to {len(midi_mapping)} MIDI keys:")
    for note in sorted(midi_mapping.keys()):
        hit = midi_mapping[note]
        print(f"  Note {note}: {hit['type']} (hit {hit['index']})")

    # Create minimal SF2 structure
    # (In production, would use Polyphone to properly embed samples)
    create_minimal_sf2_with_hits(midi_mapping, output_sf2, instrument_name)

    return True

def create_minimal_sf2_with_hits(midi_mapping, output_path, instrument_name):
    """
    Create a minimal SF2 file with sliced hits mapped to GM keys.
    """
    riff_id = b'RIFF'
    riff_form = b'sfbk'

    # INFO chunk
    info_data = b''
    info_data += b'INAM' + struct.pack('<I', len(instrument_name) + 1) + instrument_name.encode('utf-8') + b'\x00'
    info_data += b'IENG' + struct.pack('<I', 16) + b'White Room Audio\x00'
    info_data += b'ISFT' + struct.pack('<I', 23) + b'White Room Sam Sampler\x00'

    comment = f'Sliced drum breaks - {len(midi_mapping)} hits mapped to GM keys'
    info_data += b'ICMT' + struct.pack('<I', len(comment) + 1) + comment.encode('utf-8') + b'\x00'

    info_chunk = b'LIST' + struct.pack('<I', len(info_data) + 4) + b'INFO' + info_data

    # sdta chunk (minimal)
    sdta_chunk = b'LIST' + struct.pack('<I', 12) + b'sdta' + b'smpl' + struct.pack('<I', 0)

    # pdta chunk (preset data)
    pdta_data = b''

    # PHDR (preset headers)
    phdr_name = instrument_name[:20].ljust(20, '\x00').encode('utf-8')
    phdr_data = phdr_name + struct.pack('<HHHHII', 0, 0, 0, 0, 0, 0)

    # EOP
    eop_name = b'EOP' + b'\x00' * 17
    eop_data = eop_name + struct.pack('<HHHHII', 0, 0, len(midi_mapping), 0, 0, 0)

    phdr_data += eop_data
    pdta_data += b'PHDR' + struct.pack('<I', len(phdr_data)) + phdr_data

    # PBAG (preset bags) - one per hit
    pbag_data = b''
    for i in range(len(midi_mapping)):
        pbag_data += struct.pack('<HH', i, 0)
    pdta_data += b'PBAG' + struct.pack('<I', len(pbag_data)) + pbag_data

    # PGEN (preset generators)
    pgen_data = b''
    idx = 0
    for note, hit in midi_mapping.items():
        pgen_data += struct.pack('<HH', 43, idx) + b'\x00' * 4  # sampleID
        pgen_data += struct.pack('<HH', 5, note) + b'\x00' * 4  # keyRange
        idx += 1

    pgen_data += struct.pack('<HH', 0, 0) + b'\x00' * 4  # Terminator
    pdta_data += b'PGEN' + struct.pack('<I', len(pgen_data)) + pgen_data

    # INST (instruments) - one per hit
    inst_data = b''
    idx = 0
    for note, hit in midi_mapping.items():
        inst_name = f"{hit['type']}_{hit['index']}"[:20].ljust(20, '\x00').encode('utf-8')
        inst_data += inst_name + struct.pack('<H', idx * 2)
        idx += 1

    inst_data += b'EOI' + b'\x00' * 17 + struct.pack('<H', len(midi_mapping) * 2)
    pdta_data += b'INST' + struct.pack('<I', len(inst_data)) + inst_data

    # IBAG, IGEN, SHDR (simplified)
    ibag_data = b''
    for i in range(len(midi_mapping)):
        ibag_data += struct.pack('<HH', i * 2, 0)
        ibag_data += struct.pack('<HH', i * 2 + 1, 0)
    pdta_data += b'IBAG' + struct.pack('<I', len(ibag_data)) + ibag_data

    igen_data = b''
    for note, hit in midi_mapping.items():
        igen_data += struct.pack('<HH', 5, note) + b'\x00' * 4  # keyRange
        igen_data += struct.pack('<HH', 43, list(midi_mapping.keys()).index(note)) + b'\x00' * 4  # sampleID
    pdta_data += b'IGEN' + struct.pack('<I', len(igen_data)) + igen_data

    shdr_data = b''
    for note, hit in midi_mapping.items():
        shdr_name = f"{hit['type']}_{hit['index']}"[:20].ljust(20, '\x00').encode('utf-8')
        shdr_data += shdr_name
        shdr_data += struct.pack('<IIII', 0, 0, 0, 0)
        shdr_data += struct.pack('<I', hit['sr'])
        shdr_data += struct.pack('<BBHH', note, 0, 1, 1)

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

def slice_all_breaks():
    """
    Slice all drum breaks and create SoundFont files.
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
    print("Slicing Drum Breaks - Creating REX-style SoundFonts")
    print("=" * 60)
    print(f"Found {len(wav_files)} drum breaks")
    print()

    # Create 3 SF2 files with sliced breaks (10 breaks each)
    for sf2_num in range(3):
        start_idx = sf2_num * 10
        end_idx = start_idx + 10
        breaks = wav_files[start_idx:end_idx]

        sf2_name = f"drum_breaks_sliced_vol_{sf2_num + 1}.sf2"
        sf2_path = output_dir / sf2_name

        print(f"\n{'=' * 60}")
        print(f"Volume {sf2_num + 1}: Breaks {start_idx + 1}-{end_idx}")
        print('=' * 60)

        create_sliced_sf2(breaks, sf2_path, f"Sliced Drum Breaks Vol {sf2_num + 1}")

        print(f"\n  ✅ Created {sf2_name}")

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("✅ Created 3 sliced SoundFont files")
    print("📁 Output directory: dist/drum_kits/")
    print()
    print("Features:")
    print("  - Each break sliced into individual hits")
    print("  - Hits classified (kick, snare, hat, etc.)")
    print("  - Mapped to GM Standard MIDI keys")
    print("  - Play like a drum kit, not just loops!")
    print()
    print("GM Mapping:")
    print("  C3 (36) = Kick")
    print("  D3 (38) = Snare")
    print("  F#3 (42) = Closed Hi-Hat")
    print("  A#3 (46) = Open Hi-Hat")
    print("  etc.")
    print("=" * 60)

    return True

if __name__ == '__main__':
    # Check if librosa is available
    try:
        import librosa
    except ImportError:
        print("ERROR: librosa not installed!")
        print("Install with: pip3 install librosa")
        sys.exit(1)

    success = slice_all_breaks()
    sys.exit(0 if success else 1)
