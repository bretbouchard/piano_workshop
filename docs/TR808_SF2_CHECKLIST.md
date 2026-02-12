# ✅ TR-808 SF2 Creation Checklist

Use this checklist as you create the SF2 file in Polyphone.

## 📋 Pre-Flight Checks

- [x] Polyphone installed ✅
- [x] Samples organized (52 samples, 14 instruments) ✅
- [x] SFZ file generated with GM mapping ✅
- [ ] Open Polyphone application

---

## 🎛️ Step-by-Step SF2 Creation

### **Step 1: Import SFZ**

- [ ] Open Polyphone
- [ ] Click **File → Import → SFZ**
- [ ] Navigate to: `piano_workshop/piano_workshop/build/drum_kits/tr808_gm/`
- [ ] Select: `roland_tr808.sfz`
- [ ] Click **Open**

**Verify:**
- [ ] Polyphone shows samples loaded (should see 52 samples)
- [ ] All instruments visible in left panel
- [ ] No error messages about missing samples

---

### **Step 2: Verify Structure**

**In Polyphone's tree view, check:**

- [ ] **Instruments** folder exists
- [ ] **Kick** instrument has 4 samples (3 velocity layers)
- [ ] **Snare** instrument has 4 samples (3 velocity layers)
- [ ] **Closed Hat** has 4 samples
- [ ] **Open Hat** has 4 samples
- [ ] All 14 instruments present

**Click on each instrument and verify:**
- [ ] Samples appear in right panel
- [ ] Waveforms visible
- [ ] Sample names correct (e.g., `808_kick_c1_v1.wav`)

---

### **Step 3: Check Velocity Layers**

**For Kick instrument:**
- [ ] Click on "Kick" instrument
- [ ] Right panel shows 4 samples
- [ ] Double-click each sample → Opens in editor
- [ ] Verify regions have correct velocity ranges:
  - [ ] `808_kick_c1_v1.wav` → velocity 0-42
  - [ ] `808_kick_c1_v2.wav` → velocity 43-84
  - [ ] `808_kick_c1_v3.wav` → velocity 85-127

**Repeat for Snare and check:**
- [ ] `808_snare_d1_v1.wav` → velocity 0-42
- [ ] `808_snare_d1_v2.wav` → velocity 43-127

---

### **Step 4: Test Playback**

**In Polyphone:**
- [ ] Click on a sample (e.g., Kick)
- [ ] Press spacebar or click play button
- [ ] Verify you hear the drum sound
- [ ] Try a few different instruments

**If no sound:**
- [ ] Check system audio is not muted
- [ ] Check Polyphone audio preferences
- [ ] Try different sample

---

### **Step 5: Export as SF2**

- [ ] **File → Export → SoundFont2**
- [ ] Navigate to: `piano_workshop/dist/drum_kits/`
- [ ] Filename: `roland_tr808.sf2`
- [ ] Click **Save**

**Export Settings:**
- [ ] **Format:** SoundFont 2 (NOT SF2 v3!)
- [ ] **Sample Rate:** 44.1 kHz (should be default)
- [ ] **Bit Depth:** 16-bit PCM
- [ ] **Compression:** None (recommended)

**Click:**
- [ ] **Export** or **Save**

---

### **Step 6: Verify Output**

**In Finder:**
- [ ] Navigate to: `piano_workshop/dist/drum_kits/`
- [ ] Verify `roland_tr808.sf2` exists
- [ ] Check file size: Should be 3.5-4.5 MB
- [ ] Right-click → Get Info → Verify it's type "SoundFont2 file"

---

## 🧪 Post-Export Tests

### **Test 1: Load in JUCE**

```cpp
// Test loading code (copy this to test)
auto drumKit = SF2::SF2InstrumentFactory::createLayerFromSF2(
    File("/path/to/piano_workshop/dist/drum_kits/roland_tr808.sf2"),
    0  // Preset 0 = GM Standard
);

if (drumKit)
{
    DBG("✅ TR-808 loaded successfully!");
    engine->addLayer(std::move(drumKit));
}
else
{
    DBG("❌ Failed to load TR-808");
}
```

- [ ] Update file path to your actual path
- [ ] Build and run your JUCE app
- [ ] Check console for "✅ TR-808 loaded successfully!"

---

### **Test 2: MIDI Playback**

**Send MIDI notes to test:**

- [ ] Note 36 (C1), velocity 100 → Should hear Kick
- [ ] Note 38 (D1), velocity 100 → Should hear Snare
- [ ] Note 42 (F#1), velocity 100 → Should hear Closed Hi-Hat
- [ ] Note 46 (A#1), velocity 100 → Should hear Open Hi-Hat
- [ ] Note 37 (C#1), velocity 100 → Should hear Rim Shot

**Test velocity layers:**
- [ ] Note 36, velocity 20 → Soft kick
- [ ] Note 36, velocity 64 → Medium kick
- [ ] Note 36, velocity 115 → Loud kick

**Verify:** You should hear clear difference between velocity layers!

---

### **Test 3: All Instruments**

**Test each MIDI note:**

| **Note** | **Key** | **Instrument** | **Heard?** |
|----------|---------|----------------|------------|
| 35 | B0 | Clave | [ ] |
| 36 | C1 | Kick | [ ] |
| 37 | C#1 | Rim Shot | [ ] |
| 38 | D1 | Snare | [ ] |
| 39 | D#1 | Clap | [ ] |
| 42 | F#1 | Closed Hat | [ ] |
| 43 | G1 | Low Tom | [ ] |
| 45 | A1 | Mid Tom | [ ] |
| 46 | A#1 | Open Hat | [ ] |
| 47 | B1 | High Tom | [ ] |
| 49 | C#2 | Maracas | [ ] |
| 56 | G#1 | Cowbell | [ ] |

---

## 🐛 Troubleshooting

### **Polyphone won't import SFZ**

**Problem:** "Cannot open file" or missing samples error

**Solution:**
- [ ] Check SFZ file path is correct
- [ ] Verify all WAV files exist in expected locations
- [ ] Check that SFZ file references samples with relative paths
- [ ] Try opening SFZ file in text editor to verify paths

### **SF2 file too large**

**Problem:** File size > 10 MB

**Solution:**
- [ ] Check if compression was accidentally enabled
- [ ] Verify bit depth is 16-bit (not 24 or 32)
- [ ] Re-export with correct settings

### **Velocity layers not working**

**Problem:** No difference between soft and loud notes

**Solution:**
- [ ] Verify SFZ has correct `lovel`/`hivel` ranges
- [ ] Check that samples are assigned to regions
- [ ] Test with MIDI monitor to verify velocities are 0-127
- [ ] In JUCE, verify velocity is being passed through correctly

### **JUCE can't load SF2**

**Problem:** Factory::createLayerFromSF2() returns nullptr

**Solution:**
- [ ] Verify file path is correct (use absolute path)
- [ ] Check SF2 isn't corrupted (try re-exporting)
- [ ] Verify SF2 format version (must be SoundFont 2, not v3)
- [ ] Check file permissions (must be readable)

---

## 📊 Results

**Once complete, fill in these values:**

- **SF2 file created:** [ ] `roland_tr808.sf2`
- **File size:** [ ] ___ MB
- **Load time in JUCE:** [ ] ___ seconds
- **All instruments work:** [ ] Yes / No
- **Velocity layers work:** [ ] Yes / No
- **GM mapping correct:** [ ] Yes / No

---

## ✅ Completion Checklist

**When all tests pass:**

- [ ] SF2 file created and verified
- [ ] Loads successfully in JUCE
- [ ] All 14 instruments play correctly
- [ ] Velocity layers work as expected
- [ ] GM Standard mapping verified
- [ ] No audio artifacts or issues
- [ ] Performance acceptable (fast load, low CPU)

**🎉 Congratulations! You've created your first drum kit SF2!**

**Next:** Create TR-909 SF2 using same workflow!

---

**Last Updated:** 2024-12-24
**Status:** Ready for SF2 creation
**Estimated Time:** 1-2 hours
