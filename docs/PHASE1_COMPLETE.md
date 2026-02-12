# Piano Implementation - Phase 1 Complete

## Overview
This document describes the Phase 1 asset preparation workflow for integrating Salamander Grand Piano into Sam Sampler.

## Directory Structure

```
piano_workshop/
├── src/
│   └── SalamanderGrandPiano/       # Original source (FLAC + SFZ)
├── build/
│   └── salamander_wav/             # Converted samples (WAV + modified SFZ)
├── dist/
│   └── salamander_grand_v1.sf2     # Final SoundFont2 output
├── scripts/
│   ├── 01_convert_flac_to_wav.sh   # FLAC → WAV (16-bit, 44.1kHz)
│   ├── 02_create_modified_sfz.sh   # Update SFZ for WAV references
│   ├── 03_validate_sfz.sh          # Verify all samples present
│   └── build_sf2.py                # Python SF2 builder
└── docs/
    └── PHASE1_COMPLETE.md          # This document
```

## Step-by-Step Instructions

### 1. Convert FLAC to WAV

The Salamander Grand Piano source is in FLAC format (48kHz/24-bit). We need 16-bit/44.1kHz WAV for SF2.

```bash
bash piano_workshop/scripts/01_convert_flac_to_wav.sh
```

**What it does:**
- Reads all 641 FLAC files from `src/SalamanderGrandPiano/Samples/`
- Converts each to WAV (16-bit PCM, 44.1kHz, mono)
- Outputs to `build/salamander_wav/Samples/`

**Expected output:**
- 641 WAV files (~500-600 MB total)
- Preserves original sample names (e.g., `A4v7.wav`)
- Maintains directory structure

### 2. Create Modified SFZ

The original SFZ references FLAC files. We create a WAV-compatible version.

```bash
bash piano_workshop/scripts/02_create_modified_sfz.sh
```

**What it does:**
- Replaces `.flac` → `.wav` in all sample references
- Changes `#define $EXT flac` → `#define $EXT wav`
- Outputs to `build/salamander_wav/Salamander Grand Piano V3.wav.sfz`

### 3. Validate SFZ

Verify all referenced samples exist before building SF2.

```bash
bash piano_workshop/scripts/03_validate_sfz.sh
```

**What it does:**
- Parses SFZ file for all `sample=` directives
- Checks each referenced file exists in build directory
- Reports missing files

**Expected output:**
```
✓ All samples present!
Total samples referenced: 641
Found:                    641
Missing:                  0
```

### 4. Build SF2 File

Convert SFZ+WAV to single SoundFont2 file.

**Option A: Using Polyphone (Recommended)**

```bash
# Install Polyphone (macOS)
brew install polyphone

# Or download from: https://www.polyphone-soundfonts.com/

# Open Polyphone and:
# 1. File → Import → SFZ
# 2. Select: build/salamander_wav/Salamander Grand Piano V3.wav.sfz
# 3. Verify: 16 velocity layers, release samples, key ranges
# 4. File → Export → SoundFont2
# 5. Settings: 16-bit, 44.1kHz, no dithering
# 6. Save as: dist/salamander_grand_v1.sf2
```

**Option B: Using Python Script (Experimental)**

```bash
python3 piano_workshop/scripts/build_sf2.py
```

**Note:** Python script is a placeholder. Full SF2 RIFF structure implementation required.

### 5. Create Attribution

```bash
cat > piano_workshop/dist/attribution.txt << 'EOF'
Salamander Grand Piano
© Alexander Holm
Licensed under Creative Commons Attribution 3.0 (CC-BY 3.0)
Source: https://github.com/sfzinstruments/SalamanderGrandPiano

Original recordings: 48kHz/24-bit FLAC
Converted for Sam Sampler: 16-bit/44.1kHz WAV (SF2 format)
EOF
```

## Technical Specifications

### Source Format (Salamander Grand Piano V3)
- **Format:** SFZ with FLAC samples
- **Sample Rate:** 48 kHz
- **Bit Depth:** 24-bit
- **Channels:** Mono (stereo mic pair mixed to mono)
- **Velocity Layers:** 16 layers per note
- **Note Range:** A0 (21) to C8 (108)
- **Release Samples:** Yes (string resonance, hammer noise)
- **License:** CC-BY 3.0

### Output Format (SF2 for Sam Sampler)
- **Format:** SoundFont 2
- **Sample Rate:** 44.1 kHz
- **Bit Depth:** 16-bit PCM
- **Channels:** Mono (stereo output via engine)
- **Velocity Layers:** 16 (preserved)
- **Note Range:** A0-C8 (preserved)
- **Release Samples:** Included
- **Size:** ~500-600 MB
- **License:** CC-BY 3.0 (attribution required)

## Validation Checklist

Before proceeding to Phase 2, verify:

- [ ] All 641 samples converted successfully
- [ ] No missing sample errors in validation
- [ ] SF2 file created (< 700 MB)
- [ ] SF2 loads without errors in test tool
- [ ] All 16 velocity layers present
- [ ] Release samples included
- [ ] Attribution file created

## Next Steps (Phase 2)

Once SF2 asset is ready:

1. **Implement SF2 Loader** (JUCE C++)
   - Parse SF2 RIFF structure
   - Extract presets, instruments, samples
   - Map to SamSampler voice/layer architecture

2. **Sustain Pedal Logic** (Critical)
   - CC64 detection
   - Note-off behavior with pedal state
   - Release sample triggering

3. **Engine Integration**
   - Load SF2 into MinimalSamEngine
   - Velocity curve implementation
   - Testing and validation

## Troubleshooting

### Conversion Errors

**Problem:** `ffmpeg: command not found`
```bash
brew install ffmpeg
```

**Problem:** "Permission denied" running scripts
```bash
chmod +x piano_workshop/scripts/*.sh
```

### Missing Samples

**Problem:** Validation reports missing samples
- Check FLAC download completed successfully
- Verify build directory exists
- Check for permission errors

### SF2 Creation Issues

**Problem:** Polyphone won't import SFZ
- Verify WAV files exist
- Check modified SFZ references `.wav` not `.flac`
- Try importing individual sample files

**Alternative:** Use existing SF2 conversion tools:
- `sfizz` (SFZ player, can export to SF2)
- `rgc:audio SFZ tools`
- Custom Python SF2 writer (full implementation needed)

## References

- **Salamander Grand Piano:** https://github.com/sfzinstruments/SalamanderGrandPiano
- **SoundFont 2 Spec:** https://www.synthfont.com/SoundFont2.0.pdf
- **SFZ Format:** https://sfzformat.com/
- **Polyphone:** https://www.polyphone-soundfonts.com/

---

**Document Status:** Phase 1 workflow defined
**Last Updated:** 2024-12-24
**Next Phase:** Phase 2 - SF2 Loader Implementation (JUCE)
