# Master Drum Machine SF2 Creation Plan

## 📊 Collection Overview

**Total Samples:** 10,823 WAV files
**Drum Machines:** 14 collections
**Estimated SF2 Files:** 11-12 files

---

## 🎯 Strategy Overview

### **Architecture: Modular SF2 Files**

Each drum machine (or closely related group) gets its own SF2 file:
- ✅ Fast load times
- ✅ Easy to manage
- ✅ Distributable separately
- ✅ Fits GM Standard where applicable

### **Velocity Layer Strategy**

Different machines have different velocity layer approaches:

| **Machine Type** | **Samples Per Instrument** | **Strategy** |
|------------------|---------------------------|--------------|
| **Classic Roland** (808/909) | 1-3 variations | Multi-layer SF2 |
| **Blofeld** | 3-37 samples | Adaptive velocity mapping |
| **Vermona DRM-1** | ~15-20 avg | Multi-layer SF2 |
| **XL7** | Mixed | Multi-layer SF2 |
| **Synth/Techno** | Single samples | Single-layer + velocity volume |

---

## 📋 Collection Breakdown

### **Group A: Classic Roland Machines** (Priority 1)

#### 1. **Roland TR-808** (1980)
- **Source:** `/Volumes/Storage/samples/Roland - JeuneLys_Beatz/ROLAND_TR-808_(1980)/`
- **Samples:** 173 WAV files
- **Structure:** Organized by instrument type (BD, SD, CH, OH, etc.)
- **Output:** `roland_tr808.sf2` (~8-10MB)
- **Velocity Layers:** 2-3 per instrument (kick has variations)
- **GM Mapping:** Full GM Standard support
- **Priority:** ⭐⭐⭐ HIGHEST (most iconic)

**Sample Breakdown:**
```
Kick (BD): 20+ samples → 3 velocity layers
Snare (SD): 15+ samples → 2 velocity layers
Closed Hat (CH): 12 samples → 1-2 layers
Open Hat (OH): 8 samples → 1-2 layers
Toms: 6-8 each → 1-2 layers each
Percussion: Rim, Clap, Cowbell, Conga, Cymbal, Clave, Maracas
```

**SFZ Structure:**
```sfz
<region> sample=kick/808_kick_c1_v1.wav lokey=36 hikey=36 lovel=0 hivel=42
<region> sample=kick/808_kick_c1_v2.wav lokey=36 hikey=36 lovel=43 hivel=84
<region> sample=kick/808_kick_c1_v3.wav lokey=36 hikey=36 lovel=85 hivel=127
```

---

#### 2. **Roland TR-909** (1983)
- **Source:** `/Volumes/Storage/samples/Roland - JeuneLys_Beatz/ROLAND_TR-909_(1983)/`
- **Samples:** ~120 WAV files
- **Structure:** Organized (Kicks, Snares, Hats, etc.)
- **Output:** `roland_tr909.sf2` (~8-10MB)
- **Velocity Layers:** 10 variations per instrument
- **GM Mapping:** Full GM Standard
- **Priority:** ⭐⭐⭐ HIGHEST

**Sample Breakdown:**
```
Kick: 10 variations → 3 velocity layers (0-42, 43-84, 85-127)
Snare: 10 variations → 3 velocity layers
Closed Hat: 10 variations → 3 velocity layers
Open Hat: 10 variations → 3 velocity layers
Crash, Ride, Rim, Toms, Clap
```

---

#### 3. **Roland TR-606 Drumatix** (1981)
- **Source:** `/Volumes/Storage/samples/Roland - JeuneLys_Beatz/ROLAND_TR-606_Drumatix_(1981)/`
- **Samples:** ~100 WAV files
- **Output:** `roland_tr606.sf2` (~5-7MB)
- **GM Mapping:** Partial (subset of GM)
- **Priority:** ⭐⭐ HIGH

---

#### 4. **Roland TR-707** (1985)
- **Source:** `/Volumes/Storage/samples/Roland - JeuneLys_Beatz/ROLAND_TR-707_(1985)/`
- **Samples:** ~120 WAV files
- **Output:** `roland_tr707.sf2` (~5-7MB)
- **GM Mapping:** Partial
- **Priority:** ⭐⭐ HIGH

---

#### 5. **Roland TR-505** (1986)
- **Source:** `/Volumes/Storage/samples/Roland - JeuneLys_Beatz/ROLAND_TR-505_(1986)/`
- **Samples:** ~100 WAV files
- **Output:** `roland_tr505.sf2` (~5-7MB)
- **GM Mapping:** Partial
- **Priority:** ⭐⭐ HIGH

---

#### 6. **Roland TR-626** (1987)
- **Source:** `/Volumes/Storage/samples/Roland - JeuneLys_Beatz/ROLAND_TR-626_(1987)/`
- **Samples:** ~100 WAV files
- **Output:** `roland_tr626.sf2` (~5-7MB)
- **GM Mapping:** Partial
- **Priority:** ⭐ MEDIUM

---

### **Group B: Modern Digital Machines** (Priority 2)

#### 7. **Waldorf Blofeld** (Combined Collection)
- **Source:** `/Volumes/Storage/samples/retro drum-machine/blofeld drumkit/`
- **Samples:** 108 WAV files
- **Structure:** Flat file naming (cw_blofeld_bd01.wav, etc.)
- **Output:** `blofeld_drums.sf2` (~5-8MB)
- **Velocity Layers:** ADAPTIVE (see below)
- **Priority:** ⭐⭐⭐ HIGH

**⚠️ Special Handling: Variable Velocity Layers**

The Blofeld has wildly different sample counts per instrument:

```
Kick (bd):        37 samples → 5-6 velocity layers (6 samples each)
Snare (sd):       16 samples → 3 velocity layers (5 samples each)
Hi-Hat (hat):     16 samples → 3 velocity layers (5 samples each)
Percussion (perc): 31 samples → 5-6 layers, or map to different keys
Clap:              4 samples → 2 velocity layers
Tom:               4 samples → 2 velocity layers
```

**Velocity Mapping Strategy for Blofeld:**

**Option A: Adaptive Layers** (RECOMMENDED)
```sfz
// Kick: 37 samples → 6 velocity ranges
<region> sample=bd01.wav lokey=36 hikey=36 lovel=0 hivel=21   // 0-16%
<region> sample=bd07.wav lokey=36 hikey=36 lovel=22 hivel=42  // 17-33%
<region> sample=bd13.wav lokey=36 hikey=36 lovel=43 hivel=63  // 34-50%
<region> sample=bd19.wav lokey=36 hikey=36 lovel=64 hivel=84  // 51-67%
<region> sample=bd25.wav lokey=36 hikey=36 lovel=85 hivel=105 // 68-83%
<region> sample=bd31.wav lokey=36 hikey=36 lovel=106 hivel=127 // 84-100%

// Clap: 4 samples → 2 velocity ranges
<region> sample=clap01.wav lokey=39 hikey=39 lovel=0 hivel=63
<region> sample=clap03.wav lokey=39 hikey=39 lovel=64 hivel=127

// Percussion: 31 samples → Map to different keys
// Instead of velocity layers, spread across MIDI range
<region> sample=perc01.wav lokey=60 hikey=60 pitch_keycenter=60  // Perc 1
<region> sample=perc02.wav lokey=61 hikey=61 pitch_keycenter=61  // Perc 2
// ... up to 31 different percussion sounds
```

**Option B: Round Robin** (Alternative)
```sfz
// Use SFZ <group> for round-robin variation
<group> lokey=36 hikey=36
<region> sample=bd01.wav seq_length=6 seq_position=1
<region> sample=bd02.wav seq_length=6 seq_position=2
<region> sample=bd03.wav seq_length=6 seq_position=3
// ... etc
```

**Recommendation:** Use **Option A (Adaptive Layers)** for drums (kick, snare, hat) and **key mapping** for the 31 percussion samples.

---

#### 8. **Vermona DRM-1**
- **Source:** `/Volumes/Storage/samples/retro drum-machine/Vermona DRM-1/`
- **Samples:** 138 WAV files
- **Output:** `vermona_drm1.sf2` (~5-7MB)
- **Structure:** TBD (need to analyze)
- **Priority:** ⭐⭐ HIGH

---

#### 9. **Alesis SR-16 (XL7)**
- **Source:** `/Volumes/Storage/samples/retro drum-machine/xl7 drumkit/`
- **Samples:** 438 WAV files (LARGE!)
- **Output:** `alesis_sr16.sf2` (~15-20MB)
- **Note:** XL7 might include SR-16 samples
- **Priority:** ⭐⭐ HIGH (large collection)

**XL7 Strategy:**
- May need multiple SF2 files if too large
- Consider splitting: `xl7_drum_kit.sf2` + `xl7_percussion.sf2`
- Or create separate presets

---

### **Group C: Synth & Electronic** (Priority 3)

#### 10. **Synth Drums Collection**
- **Source:** `/Volumes/Storage/samples/retro drum-machine/synthdrums/`
- **Samples:** TBD (need to check file types)
- **Output:** `synth_drums.sf2` (~3-5MB)
- **Priority:** ⭐ MEDIUM

---

#### 11. **Techno Drum Samples**
- **Source:** `/Volumes/Storage/samples/retro drum-machine/techno drum samples/`
- **Samples:** 102 WAV files
- **Output:** `techno_drums.sf2` (~3-5MB)
- **GM Mapping:** Partial (electronic drums)
- **Priority:** ⭐⭐ HIGH (electronic music)

---

#### 12. **Drum Hits**
- **Source:** `/Volumes/Storage/samples/retro drum-machine/Drums Hits/`
- **Samples:** TBD
- **Output:** `drum_hits.sf2` (~2-4MB)
- **Priority:** ⭐ LOW (utility sounds)

---

### **Group D: Special Collections** (Priority 4)

#### 13. **E-mu Sound Collection**
- **Source:** `/Volumes/Storage/samples/E-mu Sound Collection/`
- **Samples:** ~100-200 files
- **Output:** `emu_drums.sf2` (~5-8MB)
- **Priority:** ⭐⭐ HIGH (vintage digital)

---

#### 14. **Vintage Collection** (Combined)
- **Sources:** R100, Mars, Odd Sounds
- **Samples:** ~500+ files
- **Output:** `vintage_collection.sf2` (~15-20MB)
- **Priority:** ⭐ MEDIUM (eclectic collection)

**Decision:** Combine into single SF2 with multiple presets for each sub-collection.

---

## 🚫 Excluded Collections

- **808 & 909 Reimagined** - Keep as WAV loops (processed, creative)
- **Amen Breaks** - Keep as WAV loops (breakbeats)
- **The Breaks** - Keep as WAV loops (breakbeats)
- **Loops folders** - Not suitable for SF2 (already looped)

---

## 📅 Implementation Order

### **Phase 1: Classic Roland** (Week 1)
1. ✅ TR-808 (most important)
2. ✅ TR-909 (second most important)
3. ✅ TR-606
4. ✅ TR-707

**Deliverables:**
- `roland_tr808.sf2`
- `roland_tr909.sf2`
- `roland_tr606.sf2`
- `roland_tr707.sf2`

---

### **Phase 2: Digital Vintage** (Week 2)
5. ✅ TR-505
6. ✅ TR-626
7. ✅ E-mu Collection

**Deliverables:**
- `roland_tr505.sf2`
- `roland_tr626.sf2`
- `emu_drums.sf2`

---

### **Phase 3: Modern Machines** (Week 2-3)
8. ✅ **Blofeld** (special velocity handling)
9. ✅ Vermona DRM-1
10. ✅ Alesis SR-16 (XL7)

**Deliverables:**
- `blofeld_drums.sf2`
- `vermona_drm1.sf2`
- `alesis_sr16.sf2`

**Blofeld Special Implementation:**
```python
# Adaptive velocity layer calculation
def calculate_velocity_ranges(num_samples):
    if num_samples >= 30:
        return 6  # 6 velocity layers
    elif num_samples >= 15:
        return 4  # 4 velocity layers
    elif num_samples >= 8:
        return 3  # 3 velocity layers
    elif num_samples >= 4:
        return 2  # 2 velocity layers
    else:
        return 1  # 1 layer

# For Blofeld:
# Kick (37 samples) → 6 layers
# Snare (16 samples) → 4 layers
# Hat (16 samples) → 4 layers
# Perc (31 samples) → Map to keys (not velocity)
```

---

### **Phase 4: Synth & Electronic** (Week 3)
11. ✅ Techno Drum Samples
12. ✅ Synth Drums
13. ✅ Drum Hits

**Deliverables:**
- `techno_drums.sf2`
- `synth_drums.sf2`
- `drum_hits.sf2`

---

### **Phase 5: Collections** (Week 4)
14. ✅ Vintage Collection (R100 + Mars + Odd Sounds)

**Deliverables:**
- `vintage_collection.sf2`

---

## 🎛️ SF2 File Specs

### **Standard Structure**

Each SF2 will contain:
- **Preset 0:** GM Standard Mapping (if applicable)
- **Preset 1:** Full Velocity Layers (all variations)
- **Preset 2:** Raw/Single Layer (for consistency)

### **File Size Targets**

| **Collection** | **Target Size** | **Max Size** |
|----------------|-----------------|--------------|
| Single Roland (808/909) | 8-10MB | 15MB |
| Smaller machines | 5-7MB | 10MB |
| Blofeld | 5-8MB | 12MB |
| XL7 | 15-20MB | 25MB |
| Combined collections | 15-20MB | 30MB |

---

## 🛠️ Automation Scripts

### **Script 1: Master Organizer** (`organize_all_drums.py`)

```python
#!/usr/bin/env python3
"""
Master drum sample organization script
Processes all 14 collections automatically
"""

COLLECTIONS = {
    # Phase 1: Classic Roland
    "roland_tr808": {
        "source": "Roland - JeuneLys_Beatz/ROLAND_TR-808_(1980)",
        "type": "roland_vintage",
        "priority": 1,
        "gm_mapping": True,
    },
    "roland_tr909": {
        "source": "Roland - JeuneLys_Beatz/ROLAND_TR-909_(1983)",
        "type": "roland_vintage",
        "priority": 1,
        "gm_mapping": True,
    },
    # ... etc for all collections
}

def organize_collection(collection_name):
    """Organize a single collection"""
    config = COLLECTIONS[collection_name]

    if config["type"] == "roland_vintage":
        organize_roland_vintage(config)
    elif config["type"] == "blofeld":
        organize_blofeld_adaptive(config)
    elif config["type"] == "modern_digital":
        organize_modern_digital(config)

if __name__ == "__main__":
    # Organize by priority
    for priority in [1, 2, 3, 4]:
        for name, config in COLLECTIONS.items():
            if config["priority"] == priority:
                print(f"Organizing {name}...")
                organize_collection(name)
```

---

### **Script 2: Blofeld Velocity Calculator** (`blofeld_velocity_calc.py`)

```python
#!/usr/bin/env python3
"""
Adaptive velocity layer calculator for Blofeld
Handles 3-37 samples per instrument intelligently
"""

def calculate_velocity_mapping(num_samples, instrument_type):
    """
    Calculate velocity ranges for variable sample counts

    Returns: List of (lovel, hivel) tuples
    """

    if instrument_type == "percussion" and num_samples > 20:
        # Map to different keys instead of velocity
        return [{"type": "key_mapping", "count": num_samples}]

    # Calculate optimal number of layers
    if num_samples >= 30:
        num_layers = 6
    elif num_samples >= 20:
        num_layers = 5
    elif num_samples >= 15:
        num_layers = 4
    elif num_samples >= 8:
        num_layers = 3
    elif num_samples >= 4:
        num_layers = 2
    else:
        num_layers = 1

    # Calculate velocity ranges
    samples_per_layer = num_samples // num_layers
    ranges = []

    for i in range(num_layers):
        start_vel = i * (128 // num_layers)
        end_vel = (i + 1) * (128 // num_layers) - 1
        if i == num_layers - 1:
            end_vel = 127  # Last layer extends to 127

        ranges.append({
            "layer": i + 1,
            "lovel": start_vel,
            "hivel": end_vel,
            "samples": samples_per_layer
        })

    return ranges

# Example usage:
# Kick: 37 samples → 6 layers, 6 samples each
# Snare: 16 samples → 4 layers, 4 samples each
# Clap: 4 samples → 2 layers, 2 samples each
```

---

### **Script 3: GM Mapping Generator** (`generate_gm_sfz.py`)

```python
#!/usr/bin/env python3
"""
Generate GM Standard SFZ files for organized samples
"""

GM_STANDARD_MAP = {
    35: "Kick_2",
    36: "Kick",
    37: "Snare_2_Rimshot",
    38: "Snare",
    39: "Hand_Clap",
    40: "Tom_2",
    41: "Tom_2",
    42: "Closed_Hat",
    43: "Tom_3",
    44: "HiHat_Pedal",
    45: "Tom_1",
    46: "Open_Hat",
    47: "Tom_3",
    48: "Crash_Cymbal",
    49: "Ride_Cymbal",
    # ... etc
}

def generate_gm_sfz(instrument_samples):
    """Generate SFZ with GM mapping"""
    sfz_content = "// GM Standard Drum Mapping\n"
    sfz_content += "<control> set_cc7=127\n\n"
    sfz_content += "<global>\n"
    sfz_content += "ampeg_attack=0.001 ampeg_release=0.3\n\n"

    for midi_key, instrument_name in GM_STANDARD_MAP.items():
        if instrument_name in instrument_samples:
            samples = instrument_samples[instrument_name]
            for i, sample in enumerate(samples):
                # Calculate velocity range for this sample
                lovel = (i * 128) // len(samples)
                hivel = ((i + 1) * 128) // len(samples) - 1
                if i == len(samples) - 1:
                    hivel = 127

                sfz_content += f"<region>\n"
                sfz_content += f"sample={instrument_name}/{sample}\n"
                sfz_content += f"lokey={midi_key} hikey={midi_key}\n"
                sfz_content += f"lovel={lovel} hivel={hivel}\n"
                sfz_content += f"pitch_keycenter={midi_key}\n\n"

    return sfz_content
```

---

## 📊 Summary Statistics

### **Collection Breakdown**

| **Category** | **Count** | **Total SF2s** | **Est. Total Size** |
|--------------|-----------|----------------|---------------------|
| Classic Roland | 6 | 6 | 40-50MB |
| Modern Digital | 3 | 3 | 25-35MB |
| Synth/Electronic | 3 | 3 | 10-15MB |
| Collections | 2 | 2 | 20-30MB |
| **TOTAL** | **14** | **14** | **95-130MB** |

### **Workflow Estimates**

| **Phase** | **Collections** | **Time** | **Output Size** |
|-----------|-----------------|----------|----------------|
| Phase 1 | 4 Roland | 3-4 days | 30-40MB |
| Phase 2 | 3 Roland + E-mu | 2-3 days | 20-30MB |
| Phase 3 | 3 Modern | 3-4 days | 25-35MB |
| Phase 4 | 3 Synth | 2 days | 10-15MB |
| Phase 5 | 1 Collection | 1-2 days | 15-20MB |
| **TOTAL** | **14** | **2-3 weeks** | **100-140MB** |

---

## ✅ Success Criteria

For each SF2 file:
- [ ] All samples load correctly
- [ ] GM Standard mapping works (where applicable)
- [ ] Velocity layers trigger smoothly
- [ ] File size under target
- [ ] No missing samples
- [ ] Appropriate release times
- [ ] Validated in Polyphone
- [ ] Tested in JUCE

---

## 🎯 Next Actions

1. ✅ **Start with TR-808** (highest priority, most iconic)
2. ⏳ Create Blofeld adaptive velocity system (complex case)
3. ⏳ Build master organization script
4. ⏳ Set up automated SF2 generation pipeline
5. ⏳ Create drum manifest JSON

---

**Status:** Master plan defined
**Last Updated:** 2024-12-24
**Next:** Execute Phase 1 (TR-808 organization)
