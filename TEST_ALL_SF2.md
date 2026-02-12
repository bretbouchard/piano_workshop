# 🧪 Test All Drum SF2 Files - Complete Guide

**Prerequisites:** All 3 SF2 files created
**Time Estimate:** 30-45 minutes
**Goal:** Verify all SF2 files work correctly in JUCE

---

## ✅ Pre-Test Checklist

### **File Verification**

Before testing, confirm all SF2 files exist:

```bash
ls -lh piano_workshop/dist/drum_kits/*.sf2
```

- [ ] `roland_tr808.sf2` exists (~3.5-4.5 MB)
- [ ] `roland_tr909.sf2` exists (~1.5-2.5 MB)
- [ ] `blofeld_drums.sf2` exists (~6-8 MB)
- [ ] All files show as "SoundFont 2.0" type

### **JUCE Project Ready**

- [ ] JUCE project builds successfully
- [ ] SF2 loading code is available
- [ ] Audio engine is initialized
- [ ] MIDI input is working (keyboard or controller)

---

## 🧪 Test 1: File Loading

### **Test Code**

```cpp
// Add this to your JUCE project
void testDrumKitLoading()
{
    String drumKitPath = "piano_workshop/dist/drum_kits/";

    // Test each kit
    String kits[] = {"roland_tr808.sf2", "roland_tr909.sf2", "blofeld_drums.sf2"};

    for (auto& kitFile : kits)
    {
        auto kitPath = drumKitPath + kitFile;
        File sf2File(kitPath);

        if (!sf2File.exists())
        {
            DBG("❌ File not found: " + kitFile);
            continue;
        }

        // Try to load the SF2
        auto drumKit = SF2::SF2InstrumentFactory::createLayerFromSF2(sf2File, 0);

        if (drumKit)
        {
            DBG("✅ Successfully loaded: " + kitFile);
            DBG("   Size: " + String(sf2File.getSize() / 1024.0 / 1024.0) + " MB");
        }
        else
        {
            DBG("❌ Failed to load: " + kitFile);
        }
    }
}
```

### **Expected Results**

- [ ] TR-808 loads successfully
- [ ] TR-909 loads successfully
- [ ] Blofeld loads successfully
- [ ] No crashes or errors
- [ ] Console shows all 3 "✅ Successfully loaded" messages

---

## 🥁 Test 2: TR-808 Drum Sounds

### **GM MIDI Mapping Reference**

| **Instrument** | **MIDI Note** | **Key** | **Velocity Layers** |
|----------------|---------------|---------|-------------------|
| Clave | 35 | B0 | 2 layers |
| Kick | 36 | C1 | 3 layers (0-42, 43-84, 85-127) |
| Rim Shot | 37 | C#1 | 2 layers |
| Snare | 38 | D1 | 2 layers |
| Hand Clap | 39 | D#1 | 3 layers |
| Closed Hat | 42 | F#1 | 3 layers |
| Low Tom | 43 | G1 | 3 layers |
| Mid Tom | 45 | A1 | 3 layers |
| Open Hat | 46 | A#1 | 3 layers |
| High Tom | 47 | B1 | 3 layers |

### **Test Procedure**

**For each instrument:**

1. **Low velocity test** (velocity 20-30):
   - Send MIDI note with low velocity
   - [ ] You hear the sound
   - [ ] Sound is appropriately quiet

2. **Medium velocity test** (velocity 60-70):
   - Send MIDI note with medium velocity
   - [ ] You hear the sound
   - [ ] Sound is moderately loud

3. **High velocity test** (velocity 115-120):
   - Send MIDI note with high velocity
   - [ ] You hear the sound
   - [ ] Sound is loud and punchy

4. **Velocity layer check**:
   - [ ] Clear difference between low, medium, high
   - [ ] Smooth transitions
   - [ ] No sudden volume jumps

### **Instrument Checklist**

- [ ] Kick (36) - Classic 808 boom
- [ ] Snare (38) - Snappy snare
- [ ] Closed Hat (42) - Short, tight hi-hat
- [ ] Open Hat (46) - Longer, ringing hi-hat
- [ ] Low Tom (43) - Low, resonant tom
- [ ] Mid Tom (45) - Mid-pitched tom
- [ ] High Tom (47) - High-pitched tom
- [ ] Rim Shot (37) - Sharp rim shot
- [ ] Hand Clap (39) - Classic clap
- [ ] Clave (35) - Wooden clave sound

### **Known Characteristics**

- **Kick:** Deep, sub-heavy bass (very little attack)
- **Snare:** Dry, snappy, not much sustain
- **Hi-Hats:** Very short, metallic decay
- **Toms:** Resonant with clear pitch
- **Clap:** Multiple clap layers, reverb tail

---

## 🥁 Test 3: TR-909 Drum Sounds

### **GM MIDI Mapping Reference**

| **Instrument** | **MIDI Note** | **Key** | **Velocity Layers** |
|----------------|---------------|---------|-------------------|
| Kick | 36 | C1 | 4 layers |
| Snare | 38 | D1 | 4 layers |
| Closed Hat | 42 | F#1 | 2 layers |
| Open Hat | 46 | A#1 | 2 layers |
| Tom | 43-47 | G1-B1 | Multiple |
| Clap | 39 | D#1 | 2 layers |
| Crash | 49 | C#2/D2 | 2 layers |
| Ride | 51 | F2 | 2 layers |
| Rim Shot | 37 | C#1 | 2 layers |

### **Test Procedure**

**For each instrument:**

1. **Low velocity test** (velocity 20-30):
   - [ ] Sound plays
   - [ ] Appropriate volume

2. **Medium velocity test** (velocity 64):
   - [ ] Sound plays
   - [ ] Noticeably louder than low

3. **High velocity test** (velocity 115-120):
   - [ ] Sound plays
   - [ ] Maximum loudness

### **Instrument Checklist**

- [ ] Kick (36) - Punchy 909 kick
- [ ] Snare (38) - Crisp 909 snare
- [ ] Closed Hat (42) - Tight closed hi-hat
- [ ] Open Hat (46) - Bright open hi-hat
- [ ] Tom (43) - Low tom
- [ ] Tom (45) - Mid tom
- [ ] Tom (47) - High tom
- [ ] Clap (39) - Electronic clap
- [ ] Crash (49) - Crash cymbal
- [ ] Ride (51) - Ride cymbal
- [ ] Rim Shot (37) - Sharp rim

### **Known Characteristics**

- **Kick:** Punchier than 808, more attack
- **Snare:** Bright, crisp, more aggressive than 808
- **Hi-Hats:** Brighter, shorter decay
- **Cymbals:** Metallic, sustained decay

---

## 🎹 Test 4: Blofeld Drum Sounds

### **Special Characteristics**

**Adaptive Velocity System:**
- **Kick:** 6 velocity layers (from 37 samples!)
- **Snare:** 4 velocity layers (from 16 samples)
- **Hi-Hat:** 4 velocity layers (from 16 samples)
- **Percussion:** 31 samples mapped to keys 60-90
- **Clap:** 2 velocity layers
- **Tom:** 2 velocity layers

### **GM MIDI Mapping Reference**

| **Instrument** | **MIDI Note** | **Key** | **Velocity Layers** |
|----------------|---------------|---------|-------------------|
| Kick | 36 | C1 | 6 layers (0-20, 21-41, 42-63, 64-84, 85-105, 106-127) |
| Snare | 38 | D1 | 4 layers (0-31, 32-63, 64-95, 96-127) |
| Closed Hat | 42 | F#1 | 4 layers (0-31, 32-63, 64-95, 96-127) |
| Open Hat | 46 | A#1 | 4 layers (0-31, 32-63, 64-95, 96-127) |
| Clap | 39 | D#1 | 2 layers |
| Tom | 43 | G1 | 2 layers |
| **Percussion** | **60-90** | **C4-F5** | **31 different sounds** |

### **Test Procedure**

#### **Standard Instruments (Kick, Snare, Hi-Hat)**

**Velocity Layer Test (more detailed):**

1. **Very low** (velocity 10):
   - [ ] Layer 1 plays
   - [ ] Very soft

2. **Low** (velocity 30):
   - [ ] Layer 1 or 2 plays
   - [ ] Soft

3. **Medium-low** (velocity 50):
   - [ ] Layer 2 plays
   - [ ] Medium-soft

4. **Medium** (velocity 64):
   - [ ] Layer 2 or 3 plays
   - [ ] Medium volume

5. **Medium-high** (velocity 90):
   - [ ] Layer 3 or 4 plays
   - [ ] Medium-loud

6. **High** (velocity 110):
   - [ ] Layer 4 or 5 plays
   - [ ] Loud

7. **Very high** (velocity 127):
   - [ ] Highest layer plays
   - [ ] Maximum loudness

#### **Percussion (Special Key Mapping)**

Test notes 60-90:
- [ ] Each key plays a different percussion sound
- [ ] Sounds are varied (not just pitch shifts)
- [ ] No velocity layering (all samples at full velocity)

**Test some examples:**
- Note 60 (C4) - [ ] Percussion sound #1
- Note 65 (F4) - [ ] Percussion sound #6
- Note 70 (A#4) - [ ] Percussion sound #11
- Note 75 (B4) - [ ] Percussion sound #16
- Note 80 (G#4) - [ ] Percussion sound #21
- Note 85 (C5) - [ ] Percussion sound #26
- Note 90 (F5) - [ ] Percussion sound #31

### **Instrument Checklist**

- [ ] Kick (36) - 6 velocity layers working
- [ ] Snare (38) - 4 velocity layers working
- [ ] Closed Hat (42) - 4 velocity layers working
- [ ] Open Hat (46) - 4 velocity layers working
- [ ] Clap (39) - 2 velocity layers
- [ ] Tom (43) - 2 velocity layers
- [ ] Percussion (60-90) - All 31 sounds play

### **Known Characteristics**

- **Kick:** Many variations, very expressive
- **Snare:** Detailed velocity response
- **Hi-Hats:** Subtle variations across layers
- **Percussion:** Diverse collection (hits, scratches, FX)

---

## 🎯 Test 5: Performance

### **Load Time Test**

```cpp
// Measure SF2 load time
auto start = Time::getMillisecondCounter();
auto drumKit = SF2::SF2InstrumentFactory::createLayerFromSF2(sf2File, 0);
auto elapsed = Time::getMillisecondCounter() - start;

DBG("Load time: " + String(elapsed) + " ms");
```

**Expected:**
- [ ] TR-808: < 100 ms
- [ ] TR-909: < 100 ms
- [ ] Blofeld: < 200 ms

### **CPU Usage Test**

Play rapid drum patterns (16th notes at 120 BPM):
- [ ] CPU usage is reasonable (< 10% on modern Mac)
- [ ] No audio glitches or dropouts
- [ ] No stuttering

### **Memory Usage**

```cpp
// Check memory footprint
// (Implementation depends on your audio engine)
```

- [ ] Memory usage is reasonable
- [ ] No memory leaks during extended playback

---

## 🎹 Test 6: MIDI Controller

If you have a MIDI controller (drum pads or keyboard):

### **Pad Mapping Test**

- [ ] Pads trigger correct drum sounds
- [ ] Velocity response feels natural
- [ ] No cross-talk between pads
- [ ] No stuck notes

### **Aftertouch Test** (if supported)

- [ ] Channel aftertouch affects volume
- [ ] Polyphonic aftertouch works per-note

---

## 🐛 Common Issues & Solutions

### **No Sound**

**Check:**
1. Audio engine is running
2. Master volume is up
3. SF2 file loaded successfully
4. MIDI notes are being received (add DBG logging)

### **No Velocity Layers**

**Symptoms:** All velocities sound the same

**Solutions:**
1. Check SFZ file has `lovel`/`hivel` ranges
2. Verify samples are assigned to regions
3. Test with MIDI monitor to confirm velocity values
4. Check JUCE is passing velocity through correctly

### **Wrong Instrument Plays**

**Symptoms:** MIDI note 36 plays snare instead of kick

**Solutions:**
1. Verify GM mapping in SFZ
2. Check pitch_keycenter values
3. Confirm MIDI note numbers are correct

### **Crackling or Popping**

**Symptoms:** Audio artifacts when playing drums

**Solutions:**
1. Check buffer size (try 256 or 512)
2. Verify sample rate matches (44.1kHz)
3. Look for missing samples
4. Check for CPU overload

---

## 📊 Test Results Summary

### **TR-808 Test Results**

- [ ] File loads successfully
- [ ] All 10 instruments play correctly
- [ ] Velocity layers work (2-3 layers per instrument)
- [ ] Sound quality is good
- [ ] Performance is acceptable

**Notes:** _______________

---

### **TR-909 Test Results**

- [ ] File loads successfully
- [ ] All 9 instruments play correctly
- [ ] Velocity layers work (2-4 layers per instrument)
- [ ] Sound quality is good
- [ ] Performance is acceptable

**Notes:** _______________

---

### **Blofeld Test Results**

- [ ] File loads successfully
- [ ] All 6 instruments play correctly
- [ ] Velocity layers work (2-6 layers per instrument)
- [ ] Percussion key mapping works (31 sounds)
- [ ] Sound quality is good
- [ ] Performance is acceptable

**Notes:** _______________

---

## ✅ Final Acceptance Criteria

**All tests pass if:**

1. **File Loading:** All 3 SF2 files load without errors
2. **Sound Playback:** All instruments play correctly
3. **Velocity Response:** Clear difference between velocity layers
4. **GM Mapping:** Correct instruments on correct notes
5. **Performance:** Load time < 200ms, CPU usage reasonable
6. **Stability:** No crashes or audio glitches

**If any test fails:**
1. Note the issue
2. Check troubleshooting section
3. Re-export SF2 if needed
4. Re-test

---

## 🎯 Next Steps After Testing

### **If All Tests Pass:**

✅ **Congratulations!** Your drum kits are ready to use!

**Recommended:**
1. Create demo patterns for each kit
2. Record audio examples
3. Document any quirks or characteristics
4. Integrate into your main project

### **If Tests Fail:**

**Debug steps:**
1. Check SFZ file for errors
2. Verify sample paths are correct
3. Re-import and re-export in Polyphone
4. Check JUCE loading code
5. Review console output for errors

---

## 📝 Test Log Template

```
Date: _______________
Tester: _______________
JUCE Version: _______________
Platform: _______________

TR-808:
- Load: [ ] Pass [ ] Fail
- Sounds: [ ] Pass [ ] Fail
- Velocity: [ ] Pass [ ] Fail
- Performance: [ ] Pass [ ] Fail

TR-909:
- Load: [ ] Pass [ ] Fail
- Sounds: [ ] Pass [ ] Fail
- Velocity: [ ] Pass [ ] Fail
- Performance: [ ] Pass [ ] Fail

Blofeld:
- Load: [ ] Pass [ ] Fail
- Sounds: [ ] Pass [ ] Fail
- Velocity: [ ] Pass [ ] Fail
- Percussion: [ ] Pass [ ] Fail
- Performance: [ ] Pass [ ] Fail

Overall: [ ] PASS [ ] FAIL

Notes:
_______________
_______________
_______________
```

---

**Good luck testing!** 🎧🥁

**Remember:** Take your time and test thoroughly. This is your chance to verify everything works before using these in production!
