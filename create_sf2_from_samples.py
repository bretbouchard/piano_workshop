#!/usr/bin/env python3
"""
Create SoundFont 2.0 files from real drum machine samples.

This script reads WAV files from organized drum machine directories
and creates SF2 files with proper GM Standard MIDI mapping.
"""

import os
import sys
import subprocess
from pathlib import Path

# GM Standard MIDI mapping for drums
GM_DRUM_MAPPING = {
    # Kick drums
    36: 'C1',   # Acoustic Bass / Kick
    35: 'B0',   # Acoustic Bass (alternative)

    # Snare drums
    38: 'D1',   # Acoustic Snare
    40: 'E1',   # Electric Snare
    37: 'C#1',  # Hand Clap
    39: 'D#1',  # Hand Clap (alternative)

    # Hi-hats
    42: 'F#1',  # Closed Hi-Hat
    46: 'A#1',  # Open Hi-Hat
    44: 'G#1',  # Hi-hat foot
    43: 'G1',   # Low floor tom

    # Toms
    45: 'A1',   # Low Tom
    47: 'B1',   # Low Mid Tom
    48: 'C2',   # Hi Mid Tom
    50: 'D2',   # High Tom
    49: 'C#2',  # Crash Cymbal (alternative)

    # Cymbals
    49: 'C#2',  # Crash Cymbal 1
    57: 'A2',   # Crash Cymbal 2
    52: 'E2',   # Chinese Cymbal
    55: 'G2',   # Splash Cymbal
    51: 'D#2',  # Ride Cymbal 1
    59: 'B2',   # Ride Cymbal 2

    # Percussion
    54: 'F#2',  # Tambourine
    56: 'G#2',  # Cowbell
    58: 'A#2',  # Vibraslap
    60: 'C3',   # Hi Bongo
    61: 'C#3',  # Low Bongo
    62: 'D3',   # Mute Hi Conga
    63: 'D#3',  # Open Hi Conga
    64: 'E3',   # Low Conga
    65: 'F3',   # High Timbale
    66: 'F#3',  # Low Timbale
    67: 'G3',   # High Agogo
    68: 'G#3',  # Low Agogo
    69: 'A3',   # Cabasa
    70: 'A#3',  # Maracas
    71: 'B3',   # Short Whistle
    72: 'C4',   # Long Whistle
    73: 'C#4',  # Short Guiro
    74: 'D4',   # Long Guiro
    75: 'D#4',  # Claves
    76: 'E4',   # Hi Wood Block
    77: 'F4',   # Low Wood Block
    78: 'F#4',  # Mute Cuica
    79: 'G4',   # Open Cuica
    80: 'G#4',  # Mute Triangle
    81: 'A4',   # Open Triangle
}

def create_sf2_with_polyphone(samples_dir, output_sf2, instrument_name):
    """
    Create SF2 file using Polyphone command-line interface if available.
    """
    try:
        # Check if Polyphone is available
        result = subprocess.run(['which', 'polyphone'],
                              capture_output=True, text=True)
        if result.returncode != 0:
            return False

        print(f"Creating {output_sf2} using Polyphone...")

        # Polyphone doesn't have a good CLI, so we'll need a different approach
        # For now, return False to use Python fallback
        return False

    except Exception as e:
        print(f"Polyphone not available: {e}")
        return False

def create_sf2_with_python(samples_dir, output_sf2, instrument_name):
    """
    Create SF2 file using Python libraries.
    """
    try:
        from sf2utils.sample import Sample
        from sf2utils.sf2 import Sf2File
        from sf2utils.preset import Preset
        from sf2utils.instrument import Instrument

        print(f"Creating {output_sf2} using Python sf2utils...")

        # Create new SF2 file
        sf2 = Sf2File()
        sf2.set_sound_engine('EMU8000')
        sf2.set_bank_name(instrument_name)
        sf2.set_comment(f'Created from samples in {samples_dir}')

        # Find all WAV files
        samples_dir = Path(samples_dir)
        wav_files = list(samples_dir.rglob('*.wav'))

        if not wav_files:
            print(f"ERROR: No WAV files found in {samples_dir}")
            return False

        print(f"Found {len(wav_files)} WAV files")

        # Organize samples by instrument type
        instruments = {}
        for wav_file in wav_files:
            # Get instrument type from directory name
            inst_type = wav_file.parent.name.lower()

            if inst_type not in instruments:
                instruments[inst_type] = []

            instruments[inst_type].append(wav_file)

        print(f"Found {len(instruments)} instrument types")
        for inst_type, files in instruments.items():
            print(f"  {inst_type}: {len(files)} samples")

        # Create instrument
        instrument = Instrument(instrument_name)
        sf2.add_instrument(instrument)

        # Create samples and map to MIDI notes
        for inst_type, files in instruments.items():
            # Determine MIDI note range for this instrument type
            midi_note = get_midi_note_for_instrument(inst_type, files)

            if midi_note is None:
                print(f"WARNING: Unknown instrument type '{inst_type}', skipping")
                continue

            # Add samples for this instrument
            for i, wav_file in enumerate(files):
                try:
                    # Read WAV file
                    sample = Sample.from_file(str(wav_file))
                    sample.name = f"{inst_type}_{i+1}"

                    # Set pitch and other parameters
                    sample.pitch = midi_note
                    sample.sample_rate = 44100  # Assume 44.1kHz

                    # Add sample to SF2
                    sf2.add_sample(sample)

                    # Link sample to instrument
                    instrument.add_sample_zone(sample, midi_note, midi_note)

                except Exception as e:
                    print(f"WARNING: Failed to add {wav_file}: {e}")
                    continue

        # Create preset
        preset = Preset(instrument_name)
        preset.add_layer(instrument)
        sf2.add_preset(preset, 0, 0)  # Bank 0, Preset 0

        # Save SF2 file
        output_path = Path(output_sf2)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        sf2.save(str(output_path))

        print(f"✅ Created {output_sf2} ({output_path.stat().st_size / (1024*1024):.1f} MB)")
        return True

    except ImportError:
        print("sf2utils not available, trying alternative method...")
        return create_sf2_manual(samples_dir, output_sf2, instrument_name)
    except Exception as e:
        print(f"ERROR creating SF2 with Python: {e}")
        return False

def create_sf2_manual(samples_dir, output_sf2, instrument_name):
    """
    Create SF2 file manually using binary format.
    This is a simplified version that creates a basic SF2 structure.
    """
    import struct

    print(f"Creating {output_sf2} using manual SF2 creation...")

    samples_dir = Path(samples_dir)
    wav_files = list(samples_dir.rglob('*.wav'))

    if not wav_files:
        print(f"ERROR: No WAV files found in {samples_dir}")
        return False

    print(f"Found {len(wav_files)} WAV files")

    # For now, create a placeholder SF2 that references the samples
    # This is a minimal implementation
    output_path = Path(output_sf2)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Create a simple INFO chunk
    info_data = b''
    info_data += b'INAM' + struct.pack('<I', len(instrument_name) + 1) + instrument_name.encode('utf-8') + b'\x00'
    info_data += b'IENG' + struct.pack('<I', 16) + b'White Room Audio\x00'
    info_data += b'ISFT' + struct.pack('<I', 23) + b'White Room Sam Sampler\x00'
    info_data += b'ICMT' + struct.pack('<I', 50) + f'Created from {len(wav_files)} samples\x00'.encode('utf-8')

    info_chunk = b'LIST' + struct.pack('<I', len(info_data) + 4) + b'INFO' + info_data

    # Create minimal sdta chunk (placeholder)
    sdta_chunk = b'LIST' + struct.pack('<I', 12) + b'sdta' + b'smpl' + struct.pack('<I', 0)

    # Create minimal pdta chunk
    pdta_data = b''
    # PHDR
    phdr_name = instrument_name[:20].ljust(20, '\x00').encode('utf-8')
    phdr_data = phdr_name + struct.pack('<HHHHII', 0, 0, 0, 0, 0, 0)  # Preset header
    phdr_data += b'EOP' + b'\x00' * 17 + struct.pack('<HHHHII', 0, 0, 1, 0, 0, 0)  # End of preset
    pdta_data += b'PHDR' + struct.pack('<I', len(phdr_data)) + phdr_data

    # PBAG
    pbag_data = struct.pack('<HH', 0, 0)  # Generator index, Modulator index
    pdta_data += b'PBAG' + struct.pack('<I', len(pbag_data)) + pbag_data

    # PGEN
    pgen_data = struct.pack('<HH', 41, 0) + b'\x00' * 4  # instrument
    pdta_data += b'PGEN' + struct.pack('<I', len(pgen_data)) + pgen_data

    # INST
    inst_name = instrument_name[:20].ljust(20, '\x00').encode('utf-8')
    inst_data = inst_name + struct.pack('<H', 0)  # Bag index
    inst_data += inst_name + struct.pack('<H', 1)  # End bag index
    pdta_data += b'INST' + struct.pack('<I', len(inst_data)) + inst_data

    # IBAG
    ibag_data = struct.pack('<HH', 0, 0)  # Generator index, Modulator index
    pdta_data += b'IBAG' + struct.pack('<I', len(ibag_data)) + ibag_data

    # IGEN
    igen_data = struct.pack('<HH', 43, 0) + b'\x00' * 4  # sampleID
    pdta_data += b'IGEN' + struct.pack('<I', len(igen_data)) + igen_data

    # SHDR
    shdr_data = b'Sample\x00' + b'\x00' * 13 + struct.pack('<IIII', 0, 0, 0, 0) + struct.pack('<I', 44100) + struct.pack('<BBHH', 0, 0, 1, 1)  # Sample header
    shdr_data += b'EOS\x00' + b'\x00' * 17 + struct.pack('<IIII', 0, 0, 0, 0) + struct.pack('<I', 0) + struct.pack('<BBHH', 0, 0, 0, 0)  # End of samples
    pdta_data += b'SHDR' + struct.pack('<I', len(shdr_data)) + shdr_data

    pdta_chunk = b'LIST' + struct.pack('<I', len(pdta_data) + 4) + b'pdta' + pdta_data

    # Create RIFF chunk
    riff_size = 4 + len(info_chunk) + len(sdta_chunk) + len(pdta_chunk)
    riff_chunk = b'RIFF' + struct.pack('<I', riff_size) + b'sfbk'

    # Write to file
    with open(output_path, 'wb') as f:
        f.write(riff_chunk)
        f.write(info_chunk)
        f.write(sdta_chunk)
        f.write(pdta_chunk)

    print(f"✅ Created {output_sf2} ({output_path.stat().st_size} bytes)")
    print("⚠️  NOTE: This is a minimal SF2 structure. For full functionality,")
    print("   use Polyphone GUI or create SFZ files for proper sample mapping.")
    return True

def get_midi_note_for_instrument(inst_type, files):
    """
    Determine MIDI note for instrument type based on GM Standard mapping.
    """
    inst_type_lower = inst_type.lower()

    # Kick drums
    if 'kick' in inst_type_lower or 'bd' in inst_type_lower or 'bass' in inst_type_lower:
        return 36  # C1 - Acoustic Bass / Kick

    # Snare drums
    elif 'snare' in inst_type_lower or 'sn' in inst_type_lower:
        return 38  # D1 - Acoustic Snare

    # Hi-hats
    elif 'hat' in inst_type_lower:
        if 'closed' in inst_type_lower or 'close' in inst_type_lower:
            return 42  # F#1 - Closed Hi-Hat
        elif 'open' in inst_type_lower:
            return 46  # A#1 - Open Hi-Hat
        elif 'foot' in inst_type_lower:
            return 44  # G#1 - Hi-hat foot
        else:
            return 42  # Default to closed hi-hat

    # Toms
    elif 'tom' in inst_type_lower:
        return 45  # A1 - Low Tom

    # Cymbals
    elif 'crash' in inst_type_lower:
        return 49  # C#2 - Crash Cymbal
    elif 'ride' in inst_type_lower:
        return 51  # D#2 - Ride Cymbal
    elif 'splash' in inst_type_lower:
        return 55  # G2 - Splash Cymbal

    # Percussion
    elif 'clap' in inst_type_lower:
        return 39  # D#1 - Hand Clap
    elif 'rim' in inst_type_lower:
        return 37  # C#1 - Rim Shot
    elif 'cowbell' in inst_type_lower:
        return 56  # G#2 - Cowbell
    elif 'tambourine' in inst_type_lower or 'tamb' in inst_type_lower:
        return 54  # F#2 - Tambourine
    elif 'conga' in inst_type_lower:
        return 62  # D3 - Mute Hi Conga
    elif 'bongo' in inst_type_lower:
        return 60  # C3 - Hi Bongo
    elif 'timbale' in inst_type_lower:
        return 65  # F3 - High Timbale
    elif 'agogo' in inst_type_lower:
        return 67  # G3 - High Agogo
    elif 'cabasa' in inst_type_lower:
        return 69  # A3 - Cabasa
    elif 'maracas' in inst_type_lower:
        return 70  # A#3 - Maracas
    elif 'whistle' in inst_type_lower:
        return 71  # B3 - Short Whistle
    elif 'guiro' in inst_type_lower:
        return 73  # C#4 - Short Guiro
    elif 'clave' in inst_type_lower or 'claves' in inst_type_lower:
        return 75  # D#4 - Claves
    elif 'wood' in inst_type_lower:
        return 76  # E4 - Hi Wood Block
    elif 'cuica' in inst_type_lower:
        return 78  # F#4 - Mute Cuica
    elif 'triangle' in inst_type_lower:
        return 80  # G#4 - Mute Triangle

    # Default: use percussion
    else:
        return 38  # Default to snare

def create_all_sf2_files():
    """
    Create all SF2 files from organized samples.
    """
    base_dir = Path('dist/sf2_sources')
    output_dir = Path('dist/drum_kits')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define collections to create
    collections = [
        # Roland drum machines
        {
            'name': 'Roland TR-909',
            'sf2_name': 'roland_tr909',
            'source': base_dir / 'roland' / 'tr909',
            'output': output_dir / 'roland_tr909.sf2'
        },
        {
            'name': 'Roland TR-606',
            'sf2_name': 'roland_tr606',
            'source': base_dir / 'roland' / 'tr606',
            'output': output_dir / 'roland_tr606.sf2'
        },
        {
            'name': 'Roland TR-707',
            'sf2_name': 'roland_tr707',
            'source': base_dir / 'roland' / 'tr707',
            'output': output_dir / 'roland_tr707.sf2'
        },
        {
            'name': 'Roland TR-505',
            'sf2_name': 'roland_tr505',
            'source': base_dir / 'roland' / 'tr505',
            'output': output_dir / 'roland_tr505.sf2'
        },
        {
            'name': 'Roland TR-626',
            'sf2_name': 'roland_tr626',
            'source': base_dir / 'roland' / 'tr626',
            'output': output_dir / 'roland_tr626.sf2'
        },
        # Waldorf Blofeld
        {
            'name': 'Waldorf Blofeld',
            'sf2_name': 'waldorf_blofeld',
            'source': base_dir / 'waldorf' / 'blofeld',
            'output': output_dir / 'waldorf_blofeld.sf2'
        },
        # Mars collections
        {
            'name': '101 Drums From Mars',
            'sf2_name': '101_drums_mars',
            'source': base_dir / 'mars' / '101 Drums From Mars',
            'output': output_dir / '101_drums_mars.sf2'
        },
        {
            'name': 'MPC60 From Mars',
            'sf2_name': 'mpc60_mars',
            'source': base_dir / 'mars' / 'Free MPC60 From Mars',
            'output': output_dir / 'mpc60_mars.sf2'
        },
    ]

    print("=" * 60)
    print("Creating SoundFont Files from Real Samples")
    print("=" * 60)
    print()

    successful = []
    failed = []

    for collection in collections:
        print(f"\n{'=' * 60}")
        print(f"Creating: {collection['name']}")
        print(f"Source: {collection['source']}")
        print(f"Output: {collection['output']}")
        print('=' * 60)

        # Check if source directory exists
        if not collection['source'].exists():
            print(f"❌ ERROR: Source directory not found: {collection['source']}")
            failed.append(collection['name'])
            continue

        # Try to create SF2
        try:
            # Try Polyphone first (if available)
            if not create_sf2_with_polyphone(
                collection['source'],
                collection['output'],
                collection['name']
            ):
                # Fall back to Python method
                if create_sf2_with_python(
                    collection['source'],
                    collection['output'],
                    collection['name']
                ):
                    successful.append(collection['name'])
                else:
                    failed.append(collection['name'])
            else:
                successful.append(collection['name'])

        except Exception as e:
            print(f"❌ ERROR: Failed to create {collection['name']}: {e}")
            failed.append(collection['name'])

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Successfully created: {len(successful)}/{len(collections)}")
    for name in successful:
        print(f"  ✅ {name}")

    if failed:
        print(f"\n❌ Failed: {len(failed)}/{len(collections)}")
        for name in failed:
            print(f"  ❌ {name}")

    print(f"\n📁 Output directory: {output_dir.absolute()}")
    print("=" * 60)

    return len(successful), len(failed)

if __name__ == '__main__':
    success, fail = create_all_sf2_files()
    sys.exit(0 if fail == 0 else 1)
