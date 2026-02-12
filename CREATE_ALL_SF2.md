# 🎯 Create All Drum SF2 Files - Master Checklist

**Goal:** Create SF2 files for all 3 organized drum kits in one session
**Time Estimate:** 30-45 minutes
**Polyphone Status:** ✅ Already open and ready!

---

## 📋 Prerequisites

- [x] Polyphone installed
- [x] Polyphone opened
- [x] Samples organized (3 kits ready)
- [x] SFZ files generated
- [x] Dist directory created

---

## 🥁 Kit 1: Roland TR-808

### **Step 1: Import SFZ**

In Polyphone:
1. **File → Import → SFZ**
2. Navigate to: `piano_workshop/piano_workshop/build/drum_kits/tr808_gm/`
3. Select: `roland_tr808.sfz`
4. Click **Open**

### **Step 2: Verify Import**

- [ ] You see 52 samples loaded
- [ ] All 14 instruments visible in left panel
- [ ] No error messages
- [ ] Waveforms visible in right panel

**Quick check:** Click on "Kick" instrument → Should see 4 samples

### **Step 3: Export as SF2**

1. **File → Export → SoundFont2**
2. Navigate to: `piano_workshop/dist/drum_kits/`
3. Filename: `roland_tr808.sf2`
4. Settings:
   - Format: **SoundFont 2** (NOT SF2 v3!)
   - Sample Rate: **44.1 kHz**
   - Bit Depth: **16-bit PCM**
   - Compression: **None**
5. Click **Save**
6. Wait 10-30 seconds for export

### **Step 4: Verify Output**

```bash
ls -lh piano_workshop/dist/drum_kits/roland_tr808.sf2
# Expected: 3.5-4.5 MB
```

- [ ] File exists
- [ ] File size is 3.5-4.5 MB
- [ ] No errors during export

**✅ TR-808 Complete!** Move to next kit.

---

## 🥁 Kit 2: Roland TR-909

### **Step 1: Import SFZ**

In Polyphone:
1. **File → Import → SFZ**
2. Navigate to: `piano_workshop/piano_workshop/build/drum_kits/tr909_gm/`
3. Select: `roland_tr909.sfz`
4. Click **Open**

### **Step 2: Verify Import**

- [ ] You see 26 samples loaded
- [ ] All 9 instruments visible in left panel
- [ ] No error messages
- [ ] Waveforms visible in right panel

**Quick check:** Click on "Kick" instrument → Should see 3 samples

### **Step 3: Export as SF2**

1. **File → Export → SoundFont2**
2. Navigate to: `piano_workshop/dist/drum_kits/`
3. Filename: `roland_tr909.sf2`
4. Settings:
   - Format: **SoundFont 2**
   - Sample Rate: **44.1 kHz**
   - Bit Depth: **16-bit PCM**
   - Compression: **None**
5. Click **Save**
6. Wait 10-30 seconds for export

### **Step 4: Verify Output**

```bash
ls -lh piano_workshop/dist/drum_kits/roland_tr909.sf2
# Expected: 1.5-2.5 MB
```

- [ ] File exists
- [ ] File size is 1.5-2.5 MB
- [ ] No errors during export

**✅ TR-909 Complete!** Move to final kit.

---

## 🎹 Kit 3: Waldorf Blofeld

### **Step 1: Import SFZ**

In Polyphone:
1. **File → Import → SFZ**
2. Navigate to: `piano_workshop/piano_workshop/build/drum_kits/blofeld_adaptive/`
3. Select: `blofeld_adaptive.sfz`
4. Click **Open**

### **Step 2: Verify Import**

- [ ] You see 108 samples loaded
- [ ] All 6 instruments visible in left panel
- [ ] No error messages
- [ ] Waveforms visible in right panel

**Quick check:**
- Click on "Kick" → Should see 37 samples (6 velocity layers)
- Click on "percussion" → Should see 31 samples

### **Step 3: Export as SF2**

1. **File → Export → SoundFont2**
2. Navigate to: `piano_workshop/dist/drum_kits/`
3. Filename: `blofeld_drums.sf2`
4. Settings:
   - Format: **SoundFont 2**
   - Sample Rate: **44.1 kHz**
   - Bit Depth: **16-bit PCM**
   - Compression: **None**
5. Click **Save**
6. Wait 20-40 seconds for export (larger file)

### **Step 4: Verify Output**

```bash
ls -lh piano_workshop/dist/drum_kits/blofeld_drums.sf2
# Expected: 6-8 MB
```

- [ ] File exists
- [ ] File size is 6-8 MB
- [ ] No errors during export

**✅ Blofeld Complete!** All three kits done!

---

## ✅ Final Verification

### **Check All Files Created**

```bash
ls -lh piano_workshop/dist/drum_kits/*.sf2
```

**Expected output:**
```
roland_tr808.sf2     (~3.5-4.5 MB)
roland_tr909.sf2     (~1.5-2.5 MB)
blofeld_drums.sf2    (~6-8 MB)
```

- [ ] All 3 SF2 files exist
- [ ] File sizes are in expected ranges
- [ ] Total size: ~11-15 MB

### **Verify File Types**

```bash
file piano_workshop/dist/drum_kits/*.sf2
```

- [ ] All show as "RIFF (little-endian) data, SoundFont 2.0"

---

## 🐛 Troubleshooting

### **Polyphone won't import SFZ**

**Problem:** "Cannot open file" error

**Solutions:**
1. Check the SFZ file path is correct
2. Verify all WAV files exist in the expected directories
3. Open the SFZ file in a text editor to check paths
4. Make sure you're in the right directory

### **Export fails or creates empty file**

**Problem:** SF2 file is 0 bytes or very small

**Solutions:**
1. Make sure you selected "SoundFont 2" (not SF2 v3)
2. Check you have write permissions to the destination
3. Verify the dist directory exists
4. Try exporting to a different location

### **File size seems wrong**

**Problem:** SF2 file is too large or too small

**Check expected sizes:**
- TR-808: 3.5-4.5 MB (52 samples)
- TR-909: 1.5-2.5 MB (26 samples)
- Blofeld: 6-8 MB (108 samples)

**If too large:**
- Check if compression was enabled (should be "None")
- Verify bit depth is 16-bit (not 24 or 32)
- Re-export with correct settings

**If too small:**
- Verify all samples loaded during import
- Check for missing samples in the directory
- Re-import and check sample count

### **Can't find the exported file**

**Solutions:**
1. Check the exact save path you used
2. Use Finder: Go to folder → `piano_workshop/dist/drum_kits/`
3. Use terminal: `find piano_workshop -name "*.sf2"`

---

## 📊 Completion Summary

After finishing this checklist, you should have:

- [x] `roland_tr808.sf2` (3.5-4.5 MB)
- [x] `roland_tr909.sf2` (1.5-2.5 MB)
- [x] `blofeld_drums.sf2` (6-8 MB)

**Total:** 3 SF2 files, ~11-15 MB, ready for testing!

---

## 🎯 Next Step

**See:** `TEST_ALL_SF2.md` for comprehensive testing guide

**Quick Test:**
```cpp
// Load and test each kit
auto tr808 = SF2::SF2InstrumentFactory::createLayerFromSF2(
    File("piano_workshop/dist/drum_kits/roland_tr808.sf2"), 0);

auto tr909 = SF2::SF2InstrumentFactory::createLayerFromSF2(
    File("piano_workshop/dist/drum_kits/roland_tr909.sf2"), 0);

auto blofeld = SF2::SF2InstrumentFactory::createLayerFromSF2(
    File("piano_workshop/dist/drum_kits/blofeld_drums.sf2"), 0);
```

---

## 💡 Tips

1. **Work sequentially:** Complete one kit before moving to the next
2. **Verify each import:** Check sample count before exporting
3. **Use consistent settings:** 16-bit, 44.1kHz, no compression for all
4. **Save in the same place:** All to `piano_workshop/dist/drum_kits/`
5. **Take your time:** Rushing leads to mistakes

---

**Ready? Let's create some SF2 files!** 🥁🎹

**Time estimate:** 30-45 minutes for all three kits
**Difficulty:** Easy (just import → export, repeat)
**Reward:** 3 iconic drum machine kits ready to use!

**Good luck! 🚀**
