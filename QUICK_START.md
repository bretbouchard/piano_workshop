# Quick Start: Creating the Piano SF2

## Status

✅ **Phase 1 Asset Preparation Complete** - All conversion work done
⏳ **SF2 Creation** - One manual step remaining (requires Polyphone)

## What's Ready

```
piano_workshop/
├── build/salamander_wav/           ✅ Ready for SF2 creation
│   ├── Salamander Grand Piano V3.wav.sfz  (Main SFZ file)
│   ├── Data/                        (23 include files, updated)
│   └── Samples/                     (641 WAV files, 574 MB)
│
├── docs/                            (Complete documentation)
│   ├── PHASE1_SUMMARY.md            (Read this first)
│   ├── PHASE1_COMPLETE.md           (Full workflow)
│   ├── SUSTAIN_PEDAL_SPEC.md        (Pedal behavior spec)
│   └── PHASE2_PREVIEW.md            (Implementation plan)
│
└── scripts/                         (Conversion tools)
```

## Create SF2 in 5 Minutes

### Step 1: Install Polyphone

```bash
brew install polyphone
```

Or download from: https://www.polyphone-soundfonts.com/

### Step 2: Import SFZ

1. Open Polyphone
2. File → Import → SFZ
3. Navigate to: `piano_workshop/build/salamander_wav/`
4. Open: `Salamander Grand Piano V3.wav.sfz`

### Step 3: Verify Import

Check that:
- ✓ 16 velocity layers are visible
- ✓ Release samples loaded (look for "rel" files)
- ✓ Note range: A0 to C8
- ✓ Total samples: ~640

### Step 4: Export as SF2

1. File → Export → SoundFont2
2. Save location: `piano_workshop/dist/salamander_grand_v1.sf2`
3. Settings:
   - Format: SF2
   - Bit depth: 16
   - Sample rate: 44.1kHz
   - No dithering
   - No embedded effects

### Step 5: Package

```bash
python3 piano_workshop/scripts/05_package_piano.py
```

This creates the final distribution package.

## What Happens Next

After SF2 creation, you're ready for **Phase 2: SF2 Loader Implementation**

See `piano_workshop/docs/PHASE2_PREVIEW.md` for the complete implementation plan.

**Key files to implement:**
- `src/engine/sf2/SF2Structures.h` - RIFF format definitions
- `src/engine/sf2/SF2Reader.h/cpp` - Chunk parser
- `src/engine/sf2/SF2Loader.h/cpp` - High-level interface

**Estimated effort:** 12-18 hours

## Troubleshooting

**Polyphone won't import:**
- Verify WAV samples exist: `ls piano_workshop/build/salamander_wav/Samples/`
- Should show 641 .wav files (~574 MB total)

**Missing velocity layers:**
- Check that Data directory was copied: `ls piano_workshop/build/salamander_wav/Data/`
- Should show 23 .txt files

**Wrong file size:**
- Expected: 500-600 MB
- If smaller: samples not included, recheck export settings
- If larger: wrong bit depth, ensure 16-bit selected

## Complete Documentation

- **Phase 1 Summary:** `docs/PHASE1_SUMMARY.md` - Overview and status
- **Full Workflow:** `docs/PHASE1_COMPLETE.md` - Detailed guide
- **Pedal Spec:** `docs/SUSTAIN_PEDAL_SPEC.md` - Critical for Phase 3
- **Phase 2 Plan:** `docs/PHASE2_PREVIEW.md` - Implementation roadmap
- **Workshop README:** `README.md` - Complete reference

---

**Status:** Ready for SF2 creation
**Time to SF2:** ~5 minutes (with Polyphone installed)
**Next Phase:** Phase 2 - SF2 Loader (12-18 hours)
