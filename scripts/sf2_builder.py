#!/usr/bin/env python3
"""
Direct SF2 Writer - Build SoundFont2 from WAV samples
Phase 1, Step 4: Create SF2 without external tools

This writes proper SF2 RIFF/IFF structure with minimal dependencies.
"""

import struct
import wave
from pathlib import Path
from typing import List, Dict, Tuple

# Configuration
SCRIPT_DIR = Path(__file__).parent
WORKSHOP_ROOT = SCRIPT_DIR.parent
BUILD_DIR = WORKSHOP_ROOT / "build/salamander_wav"
SAMPLES_DIR = BUILD_DIR / "Samples"
DATA_DIR = BUILD_DIR / "Data"
OUTPUT_SF2 = WORKSHOP_ROOT / "dist/salamander_grand_v1.sf2"


class SF2Builder:
    """Build SoundFont2 files from scratch"""

    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.samples: List[Dict] = []
        self.instruments: List[Dict] = []
        self.presets: List[Dict] = []

    def add_sample(self, wav_path: Path, name: str, root_key: int):
        """Add a WAV sample to the SF2"""
        with wave.open(str(wav_path), 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            channels = wf.getnchannels()
            width = wf.getsampwidth()

            # Read audio data
            data = wf.readframes(frames)

            if width == 2:  # 16-bit
                samples = struct.unpack(f'<{frames * channels}h', data)
            else:
                raise ValueError(f"Unsupported width: {width}")

            self.samples.append({
                'name': name[:20].ljust(20, '\x00'),
                'data': data,  # Raw bytes
                'start': 0,
                'end': frames,
                'startLoop': 0,
                'endLoop': 0,
                'sampleRate': rate,
                'originalPitch': root_key,
                'pitchCorrection': 0,
                'sampleLink': 0,
                'sampleType': 1,  # Mono sample
                'path': wav_path
            })

    def write(self):
        """Write complete SF2 file"""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, 'wb') as f:
            # RIFF header
            f.write(b'RIFF')

            # Calculate total size (will update later)
            size_pos = f.tell()
            f.write(struct.pack('<I', 0))  # Placeholder

            # sfbk identifier
            f.write(b'sfbk')

            # INFO chunk
            info_data = self._write_info_chunk(f)

            # SDTA chunk (sample data)
            sdta_data = self._write_sdta_chunk(f)

            # PDTA chunk (orchestration)
            pdta_data = self._write_pdta_chunk(f)

            # Update RIFF size
            end_pos = f.tell()
            total_size = end_pos - 8
            f.seek(size_pos)
            f.write(struct.pack('<I', total_size))

    def _write_info_chunk(self, f) -> int:
        """Write INFO chunk with metadata"""
        chunk_start = f.tell()

        f.write(b'LIST')
        list_size_pos = f.tell()
        f.write(struct.pack('<I', 0))  # Placeholder

        f.write(b'INFO')

        # Version
        self._write_named_chunk(f, b'ifil', struct.pack('<H', 2) + struct.pack('<H', 1))

        # Sound engine
        self._write_named_chunk(f, b'isng', b'EMU8000\x00')

        # Bank name
        self._write_named_chunk(f, b'INAM', b'Salamander Grand Piano V3\x00')

        # Author
        self._write_named_chunk(f, b'IENG', b'Alexander Holm\x00')

        # Copyright
        self._write_named_chunk(f, b'ICOP', b'CC-BY 3.0\x00')

        # Update LIST size
        list_end = f.tell()
        list_size = list_end - chunk_start - 8
        f.seek(list_size_pos)
        f.write(struct.pack('<I', list_size))
        f.seek(list_end)

        return list_end - chunk_start

    def _write_sdta_chunk(self, f) -> int:
        """Write SDTA chunk with sample data"""
        chunk_start = f.tell()

        f.write(b'LIST')
        list_size_pos = f.tell()
        f.write(struct.pack('<I', 0))  # Placeholder

        f.write(b'sdta')

        # smpl sub-chunk
        smpl_pos = f.tell()
        f.write(b'smpl')
        smpl_size_pos = f.tell()
        f.write(struct.pack('<I', 0))  # Placeholder

        # Concatenate all sample data
        for sample in self.samples:
            f.write(sample['data'])

        # Update smpl size
        smpl_end = f.tell()
        smpl_size = smpl_end - smpl_pos - 8
        f.seek(smpl_size_pos)
        f.write(struct.pack('<I', smpl_size))
        f.seek(smpl_end)

        # Update LIST size
        list_end = f.tell()
        list_size = list_end - chunk_start - 8
        f.seek(list_size_pos)
        f.write(struct.pack('<I', list_size))
        f.seek(list_end)

        return list_end - chunk_start

    def _write_pdta_chunk(self, f) -> int:
        """Write PDTA chunk with orchestration data"""
        chunk_start = f.tell()

        f.write(b'LIST')
        list_size_pos = f.tell()
        f.write(struct.pack('<I', 0))  # Placeholder

        f.write(b'pdta')

        # Build chunk structures
        phdr_data = self._build_preset_headers()
        pbag_data = self._build_preset_bags()
        pmod_data = self._build_modulators()  # Empty
        pgen_data = self._build_preset_generators()
        ihdr_data = self._build_instrument_headers()
        ibag_data = self._build_instrument_bags()
        imod_data = self._build_modulators()  # Empty
        igen_data = self._build_instrument_generators()
        shdr_data = self._build_sample_headers()

        # Write each sub-chunk
        for name, data in [
            (b'phdr', phdr_data),
            (b'pbag', pbag_data),
            (b'pmod', pmod_data),
            (b'pgen', pgen_data),
            (b'ihdr', ihdr_data),
            (b'ibag', ibag_data),
            (b'imod', imod_data),
            (b'igen', igen_data),
            (b'shdr', shdr_data),
        ]:
            self._write_named_chunk(f, name, data)

        # Update LIST size
        list_end = f.tell()
        list_size = list_end - chunk_start - 8
        f.seek(list_size_pos)
        f.write(struct.pack('<I', list_size))
        f.seek(list_end)

        return list_end - chunk_start

    def _build_preset_headers(self) -> bytes:
        """Build preset header list (PHDR)"""
        data = b''

        # Piano preset
        data += b'Salamander Grand Piano\x00'  # Name (20 chars)
        data += b'\x00\x00'  # Preset number
        data += b'\x00\x00'  # Bank
        data += b'\x00\x00'  # First preset zone index
        data += self._build_zone_index(len(self.samples))  # Last preset zone (will update)
        data += b'\x00\x00\xd9\x44'  # Library
        data += b'\x00\x00\x00\x00'  # Genre
        data += b'\x00\x00\x00\x00'  # Morphology

        # Terminal preset (required)
        data += b'EOP\x00' + b'\x00' * 16
        data += b'\xFF\xFF'  # Preset
        data += b'\xFF\xFF'  # Bank
        data += self._build_zone_index(len(self.samples))
        data += self._build_zone_index(len(self.samples))

        return data

    def _build_instrument_headers(self) -> bytes:
        """Build instrument header list (IHDR)"""
        data = b''

        # Piano instrument
        data += b'Salamander Grand Piano\x00'  # Name
        data += b'\x00\x00'  # First instrument zone index
        data += self._build_zone_index(len(self.samples))  # Last zone (will update)

        # Terminal instrument (required)
        data += b'EOI\x00' + b'\x00' * 17
        data += self._build_zone_index(len(self.samples))
        data += self._build_zone_index(len(self.samples))

        return data

    def _build_sample_headers(self) -> bytes:
        """Build sample header list (SHDR)"""
        data = b''

        current_sample = 0
        for sample in self.samples:
            name_bytes = sample['name'].encode('latin1')[:20]
            name_bytes = name_bytes + b'\x00' * (20 - len(name_bytes))
            data += name_bytes
            data += struct.pack('<I', current_sample)  # Start
            data += struct.pack('<I', current_sample + len(sample['data']) // 2)  # End (in samples)
            data += struct.pack('<I', 0)  # Start loop
            data += struct.pack('<I', 0)  # End loop
            data += struct.pack('<I', sample['sampleRate'])
            data += struct.pack('B', sample['originalPitch'])
            data += struct.pack('b', sample['pitchCorrection'])
            data += struct.pack('<H', sample['sampleLink'])
            data += struct.pack('<H', sample['sampleType'])

            current_sample += len(sample['data']) // 2

        # Terminal sample (required)
        data += b'EOS\x00' + b'\x00' * 17
        data += struct.pack('<I', current_sample)
        data += struct.pack('<I', current_sample)
        data += struct.pack('<I', 0) * 2
        data += struct.pack('<I', 44100)
        data += struct.pack('B', 0)
        data += struct.pack('b', 0)
        data += struct.pack('<H', 0)
        data += struct.pack('<H', 0)

        return data

    def _build_preset_bags(self) -> bytes:
        """Build preset zone list (PBAG)"""
        # Two zones: global zone + terminal
        data = b''
        data += b'\x00\x00'  # Generator index
        data += b'\x00\x00'  # Modulator index
        data += b'\x01\x00'  # Generator index (next zone)
        data += b'\x00\x00'  # Modulator index
        return data

    def _build_instrument_bags(self) -> bytes:
        """Build instrument zone list (IBAG)"""
        # One zone per sample + terminal
        data = b''
        for i, sample in enumerate(self.samples):
            gen_idx = i * 3  # 3 generators per zone (keyrange, velrange, sample)
            data += struct.pack('<H', gen_idx)
            data += b'\x00\x00'  # No modulators

        # Terminal
        data += struct.pack('<H', len(self.samples) * 3)
        data += b'\x00\x00'

        return data

    def _build_preset_generators(self) -> bytes:
        """Build preset generator list (PGEN)"""
        data = b''

        # Global zone: instrument generator
        data += struct.pack('<H', 41)  # Instrument
        data += struct.pack('<h', 0)   # First instrument

        # Terminal
        data += b'\x00\x00'
        data += b'\x00\x00'

        return data

    def _build_instrument_generators(self) -> bytes:
        """Build instrument generator list (IGEN)"""
        data = b''

        for i, sample in enumerate(self.samples):
            # Key range
            data += struct.pack('<H', 43)  # keyRange
            key_low = sample['originalPitch']
            key_high = sample['originalPitch']
            data += struct.pack('<h', (key_low << 8) | key_high)

            # Velocity range (full range)
            data += struct.pack('<H', 44)  # velRange
            data += struct.pack('<h', (0 << 8) | 127)

            # Sample ID
            data += struct.pack('<H', 53)  # sampleID
            data += struct.pack('<h', i)

        # Terminal
        data += b'\x00\x00'
        data += b'\x00\x00'

        return data

    def _build_modulators(self) -> bytes:
        """Build modulator list (empty)"""
        return b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    def _write_named_chunk(self, f, name: bytes, data: bytes):
        """Write a named chunk with size and data"""
        f.write(name)
        f.write(struct.pack('<I', len(data)))
        f.write(data)

        # Pad to word boundary
        if len(data) % 2 != 0:
            f.write(b'\x00')

    def _build_zone_index(self, value: int) -> bytes:
        """Build a zone index (16-bit)"""
        return struct.pack('<H', value)


def scan_samples() -> List[Tuple[Path, str, int]]:
    """Scan Samples directory and extract note/velocity info"""
    samples = []

    for wav_path in SAMPLES_DIR.rglob('*.wav'):
        filename = wav_path.stem

        # Parse note from filename (e.g., "A4v7" -> A4, vel 7)
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        for i, name in enumerate(note_names):
            if filename.upper().startswith(name):
                try:
                    parts = filename[len(name):].split('v')
                    octave = int(parts[0])
                    velocity = int(parts[1]) if len(parts) > 1 else 1

                    note_num = (octave + 1) * 12 + i
                    samples.append((wav_path, filename, note_num))
                    break
                except (ValueError, IndexError):
                    pass

    return sorted(samples, key=lambda x: (x[2], x[0]))


def main():
    print("=" * 60)
    print("Building SF2 from WAV Samples")
    print("=" * 60)
    print()

    print(f"Source: {SAMPLES_DIR}")
    print(f"Output: {OUTPUT_SF2}")
    print()

    # Scan for samples
    print("Scanning for samples...")
    sample_files = scan_samples()
    print(f"  Found {len(sample_files)} WAV files")
    print()

    if not sample_files:
        print("✗ ERROR: No samples found!")
        return 1

    # Create builder
    builder = SF2Builder(OUTPUT_SF2)

    # Add samples
    print("Loading samples...")
    for i, (wav_path, name, note) in enumerate(sample_files, 1):
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(sample_files)}")

        builder.add_sample(wav_path, name, note)

    print(f"  Loaded {len(builder.samples)} samples")
    print()

    # Write SF2
    print("Writing SF2 file...")
    builder.write()

    # Get file size
    size_bytes = OUTPUT_SF2.stat().st_size
    size_mb = size_bytes / 1024 / 1024

    print()
    print("=" * 60)
    print("SF2 Build Complete!")
    print("=" * 60)
    print(f"Output: {OUTPUT_SF2}")
    print(f"Size:   {size_mb:.1f} MB")
    print(f"SAMPLES: {len(builder.samples)}")
    print()

    print("✓ SF2 file created successfully!")
    print()
    print("Next: Run packaging script")
    print(f"  python3 {SCRIPT_DIR / '05_package_piano.py'}")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
