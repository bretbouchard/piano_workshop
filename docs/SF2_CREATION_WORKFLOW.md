# 🎹 SF2 Creation Workflow

**Purpose:** Complete guide for creating SF2 files from organized SFZ projects using Polyphone

**Last Updated:** 2025-01-19
**Status:** Manual GUI workflow (CLI automation in development)

---

## 📋 Quick Start

### For Drum Kits (TR-808, TR-909, Blofeld, etc.)

1. **Open Polyphone**
   ```bash
   open -a Polyphone
   ```

2. **Import SFZ**
   - File → Import → SFZ
   - Navigate to: `piano_workshop/piano_workshop/build/drum_kits/[kit_name]/`
   - Select the `.sfz` file
   - Click **Open**

3. **Verify Import**
   - Check that samples loaded correctly
   - Look at instrument count and sample count
   - Verify waveforms are visible

4. **Export as SF2**
   - File → Export → SoundFont2
   - Save to: `piano_workshop/dist/drum_kits/`
   - Filename: `[kit_name].sf2`
   - Settings:
     - Format: **SoundFont 2** (NOT SF2 v3!)
     - Sample Rate: **44.1 kHz**
     - Bit Depth: **16-bit PCM**
     - Compression: **None**

5. **Verify Output**
   ```bash
   ls -lh piano_workshop/dist/drum_kits/[kit_name].sf2
   ```

---

## 🥁 Drum Kits Ready for SF2 Creation

| **Drum Kit** | **SFZ Path** | **Samples** | **Output Name** | **Status** |
|--------------|--------------|-------------|-----------------|------------|
| Roland TR-808 | `build/drum_kits/tr808_gm/roland_tr808.sfz` | 52 | `roland_tr808.sf2` | ✅ Ready |
| Roland TR-909 | `build/drum_kits/tr909_gm/roland_tr909.sfz` | 26 | `roland_tr909.sf2` | ✅ Ready |
| Waldorf Blofeld | `build/drum_kits/blofeld_adaptive/blofeld_adaptive.sfz` | 108 | `blofeld_drums.sf2` | ✅ Ready |

**Expected file sizes:**
- TR-808: ~3.5-4.5 MB
- TR-909: ~1.5-2.5 MB
- Blofeld: ~6-8 MB

---

## 🎹 For Piano (Salamander Grand)

1. **Open Polyphone**
   ```bash
   open -a Polyphone
   ```

2. **Import Piano SFZ**
   - File → Import → SFZ
   - Navigate to: `piano_workshop/build/salamander_wav/`
   - Select: `Salamander Grand Piano V3.wav.sfz`
   - Click **Open**

3. **Verify Piano Structure**
   - Check for 16 velocity layers per note
   - Note range: A0 (21) to C8 (108)
   - Look for release samples

4. **Export as SF2**
   - File → Export → SoundFont2
   - Save to: `piano_workshop/dist/`
   - Filename: `salamander_grand_v1.sf2`
   - Settings:
     - Format: SoundFont 2
     - Sample Rate: 44.1 kHz
     - Bit Depth: 16-bit PCM
     - Compression: None

5. **Verify Output**
   ```bash
   ls -lh piano_workshop/dist/salamander_grand_v1.sf2
   # Expected: ~500-600 MB
   ```

---

## 🧪 Testing SF2 Files

### Test 1: File Verification

```bash
# Check file exists and size
ls -lh piano_workshop/dist/*.sf2

# Verify file type
file piano_workshop/dist/roland_tr808.sf2
# Should output: "RIFF (little-endian) data, SoundFont 2.0"
```

### Test 2: JUCE Loading Test

```cpp
// Test loading drum kit
auto drumKit = SF2::SF2InstrumentFactory::createLayerFromSF2(
    File("/path/to/piano_workshop/dist/drum_kits/roland_tr808.sf2"),
    0  // Preset 0 = GM Standard
);

if (drumKit)
{
    engine->addLayer(std::move(drumKit));
    DBG("✅ Drum kit loaded successfully!");

    // Test drums:
    // MIDI Note 36 = Kick (C1)
    // MIDI Note 38 = Snare (D1)
    // MIDI Note 42 = Closed Hi-Hat (F#1)
    // MIDI Note 46 = Open Hi-Hat (A#1)
}
else
{
    DBG("❌ Failed to load drum kit");
}
```

### Test 3: MIDI Playback Test

Send MIDI notes to test each instrument:

| **Note** | **Key** | **Instrument** | **Expected Velocity Response** |
|----------|---------|----------------|-------------------------------|
| 36 | C1 | Kick | 3 layers: soft (0-42), med (43-84), loud (85-127) |
| 38 | D1 | Snare | 2 layers: soft (0-42), loud (43-127) |
| 42 | F#1 | Closed Hat | 3 layers |
| 46 | A#1 | Open Hat | 3 layers |
| 37 | C#1 | Rim Shot | 2 layers |
| 39 | D#1 | Hand Clap | 2 layers |

---

## 🔧 Troubleshooting

### Polyphone Won't Open

**Problem:** Gatekeeper security warning

**Solution:**
```bash
# Remove quarantine attribute
sudo xattr -d com.apple.quarantine /Applications/Polyphone.app

# Try opening again
open -a Polyphone
```

### SFZ Import Fails

**Problem:** "Cannot open file" or missing samples

**Solutions:**
1. Check SFZ file path is correct
2. Verify all WAV files exist in expected locations
3. Open SFZ file in text editor to verify relative paths
4. Ensure working directory is correct

### Velocity Layers Not Working

**Problem:** No difference between soft and loud notes

**Solutions:**
1. Verify SFZ has correct `lovel`/`hivel` ranges
2. Check samples are assigned to regions
3. Test with MIDI monitor to verify velocities 0-127
4. In JUCE, verify velocity is passed through correctly

### File Size Too Large

**Problem:** SF2 file > 20 MB (drums) or > 700 MB (piano)

**Solutions:**
1. Check if compression was accidentally enabled
2. Verify bit depth is 16-bit (not 24 or 32)
3. Re-export with correct settings

---

## 📊 Expected Results

### Drum Kit SF2 Files

| **Kit** | **Samples** | **Instruments** | **Velocity Layers** | **Expected Size** |
|---------|-------------|-----------------|-------------------|-------------------|
| TR-808 | 52 | 14 | 2-3 per inst | 3.5-4.5 MB |
| TR-909 | 26 | 9 | 2-4 per inst | 1.5-2.5 MB |
| Blofeld | 108 | 6 | 2-6 per inst | 6-8 MB |
| TR-606 | ~100 | ~10 | 3 per inst | ~7 MB |
| TR-707 | ~120 | ~15 | 3 per inst | ~9 MB |

### Piano SF2 File

| **Instrument** | **Samples** | **Velocity Layers** | **Note Range** | **Expected Size** |
|----------------|-------------|-------------------|----------------|-------------------|
| Salamander Grand | ~640 | 16 per note | A0-C8 (88 keys) | 500-600 MB |

---

## 🚀 CLI Automation (Experimental)

**Status:** Work in progress - Manual GUI workflow recommended

The Polyphone CLI command format is:
```bash
/Applications/Polyphone.app/Contents/MacOS/polyphone --convert \
  [input.sfz] \
  [output.sf2] \
  --format sf2
```

**Current Issue:** CLI returns "Write 'man polyphone' to show usage" - syntax needs investigation.

**Alternative Approach:** Use Python script with GUI automation (pyautogui) or build custom SF2 writer using `sf2forge` library.

**For now:** Use the manual GUI workflow documented above.

---

## 📚 Related Documentation

- **`DRUM_START_HERE.md`** - Drum project overview
- **`MASTER_DRUM_PLAN.md`** - All 14 drum machine collections
- **`DRUM_INTEGRATION_GUIDE.md`** - JUCE integration details
- **`TR808_SF2_CHECKLIST.md`** - Detailed SF2 creation checklist
- **`CREATE_SF2_NOW.md`** - Quick start for immediate SF2 creation

---

## ✅ Completion Checklist

After creating each SF2 file:

- [ ] File exists in `piano_workshop/dist/`
- [ ] File size is within expected range
- [ ] File is correct type (SoundFont2)
- [ ] Loads successfully in JUCE
- [ ] All instruments play correctly
- [ ] Velocity layers work as expected
- [ ] GM mapping verified (for drums)
- [ ] No audio artifacts or issues
- [ ] Performance acceptable (fast load, low CPU)

---

## 📝 Notes

### Why Manual GUI?

1. **Reliability:** Polyphone GUI is well-tested and stable
2. **Verification:** You can see samples loaded before export
3. **Troubleshooting:** Easier to diagnose issues visually
4. **Settings Control:** Full access to all export options

### Future Automation

Once CLI syntax is resolved, we can create batch scripts:
```bash
# Create all drum SF2 files
for sfz in build/drum_kits/*/ *.sfz; do
    polyphone --convert "$sfz" "dist/drum_kits/$(basename $sfz .sf2).sf2" --format sf2
done
```

---

**Workflow Status:** ✅ Documented and ready for use
**Priority:** High - Complete SF2 creation for TR-808, TR-909, Blofeld
**Next Step:** Use Polyphone GUI to create first drum SF2 file

**Good luck! 🎹**
