# Drum Integration Guide for Piano Workshop

## Overview

This guide extends the Piano Workshop workflow to handle drum machine samples in SF2 format. While piano_workshop was originally designed for the Salamander Grand Piano, the same pipeline can process drum kits with minor modifications.

## Architecture Decision: One SF2 Per Drum Machine

### ✅ RECOMMENDED: Modular SF2 Files

**Structure:**
```
dist/drum_kits/
├── roland_tr808.sf2        # ~5-10MB, 173 samples
├── roland_tr909.sf2        # ~5-10MB
├── roland_tr606.sf2
├── roland_tr707.sf2
├── roland_tr505.sf2
├── retro_machines.sf2      # Blofeld, DRM-1, XL-7 combined
└── vintage_collection.sf2  # E-mu, R100, Mars
```

### Why Modular?

1. **Performance**: Load only the kit you need
2. **Memory**: Smaller RAM footprint per kit
3. **Organization**: Easier to manage and version control
4. **Distribution**: Can distribute individual kits
5. **Flexibility**: Easy to add/remove kits

---

## Drum Kit Organization

### Source Structure

```
/Volumes/Storage/samples/
└── organized_for_sf2/
    ├── tr808_gm/
    │   ├── kick/
    │   │   ├── 808_kick_c1_v1.wav    # C1, vel 0-42
    │   │   ├── 808_kick_c1_v2.wav    # C1, vel 43-84
    │   │   └── 808_kick_c1_v3.wav    # C1, vel 85-127
    │   ├── snare/
    │   │   ├── 808_snare_d1_v1.wav   # D1, vel 0-42
    │   │   └── 808_snare_d1_v2.wav   # D1, vel 43-127
    │   ├── hihat_closed/
    │   │   └── 808_ch_fsharp1.wav    # F#1
    │   └── [other instruments]
    │
    └── tr909_gm/
        └── [similar structure]
```

### Naming Convention

**Format:** `[machine]_[instrument]_[key]_[velocity].wav`

**Examples:**
- `808_kick_c1_v1.wav` - TR-808 Kick, C1, velocity layer 1
- `808_snare_d1_v2.wav` - TR-808 Snare, D1, velocity layer 2
- `908_kick_c1_full.wav` - TR-909 Kick, C1, full range

---

## Workflow: Creating SF2 from Drum Samples

### Phase 1: Organize Samples

```bash
# 1. Create organized directory structure
mkdir -p piano_workshop/build/drum_kits/{tr808_gm,tr909_gm,tr606_gm}

# 2. Copy samples with proper naming (automated script coming)
python3 piano_workshop/scripts/organize_drum_samples.py
```

### Phase 2: Create SFZ Definition

Each drum kit needs an SFZ file to define the mapping:

```sfz
// roland_tr808.sfz
// Roland TR-808 GM Standard Mapping

// Kick (C1, MIDI 36)
<region>
sample=808_kick_c1_v1.wav
lokey=36 hikey=36 lovel=0 hivel=42 pitch_keycenter=36
ampeg_release=0.5
<region>
sample=808_kick_c1_v2.wav
lokey=36 hikey=36 lovel=43 hivel=84 pitch_keycenter=36
ampeg_release=0.5
<region>
sample=808_kick_c1_v3.wav
lokey=36 hikey=36 lovel=85 hivel=127 pitch_keycenter=36
ampeg_release=0.5

// Snare (D1, MIDI 38)
<region>
sample=808_snare_d1_v1.wav
lokey=38 hikey=38 lovel=0 hivel=42 pitch_keycenter=38
ampeg_release=0.3
<region>
sample=808_snare_d1_v2.wav
lokey=38 hikey=38 lovel=43 hivel=127 pitch_keycenter=38
ampeg_release=0.3

// Closed Hi-Hat (F#1, MIDI 42)
<region>
sample=808_ch_fsharp1.wav
lokey=42 hikey=42 pitch_keycenter=42
ampeg_release=0.1

// Open Hi-Hat (A#1, MIDI 46)
<region>
sample=808_oh_asharp1.wav
lokey=46 hikey=46 pitch_keycenter=46
ampeg_release=0.5

// ... continue for all instruments
```

### Phase 3: Convert to SF2

**Using Polyphone (GUI):**

```bash
# Install Polyphone
brew install --cask polyphone

# Launch Polyphone
open -a Polyphone

# In Polyphone:
# 1. File → Import → SFZ
# 2. Select: piano_workshop/build/drum_kits/tr808_gm/roland_tr808.sfz
# 3. Verify: All samples loaded, velocity layers correct
# 4. File → Export → SoundFont2
# 5. Save as: piano_workshop/dist/drum_kits/roland_tr808.sf2
# 6. Settings: 16-bit, 44.1kHz, no compression
```

**Using Polyphone (CLI - if available):**

```bash
polyphone-cli --import sfz \
  --input piano_workshop/build/drum_kits/tr808_gm/roland_tr808.sfz \
  --output piano_workshop/dist/drum_kits/roland_tr808.sf2 \
  --format 16-bit
```

---

## Drum Manifest File

Create a manifest for all drum kits:

```json
{
  "version": "1.0",
  "last_updated": "2024-12-24",
  "drum_kits": [
    {
      "id": "roland_tr808",
      "name": "Roland TR-808",
      "manufacturer": "Roland",
      "year": 1980,
      "file": "roland_tr808.sf2",
      "size_mb": 8.5,
      "num_samples": 173,
      "num_presets": 3,
      "midi_mapping": "gm_standard",
      "instruments": [
        {"name": "Kick", "midi_key": 36, "velocity_layers": 3},
        {"name": "Snare", "midi_key": 38, "velocity_layers": 2},
        {"name": "Closed Hat", "midi_key": 42, "velocity_layers": 1},
        {"name": "Open Hat", "midi_key": 46, "velocity_layers": 1}
      ],
      "tags": ["vintage", "analog", "drum_machine", "808"],
      "license": "_samples_public_domain"
    },
    {
      "id": "roland_tr909",
      "name": "Roland TR-909",
      "manufacturer": "Roland",
      "year": 1983,
      "file": "roland_tr909.sf2",
      "size_mb": 9.2,
      "num_samples": 180,
      "num_presets": 3,
      "midi_mapping": "gm_standard",
      "tags": ["vintage", "analog", "drum_machine", "909"]
    }
  ]
}
```

---

## Automation Scripts

### Script 1: Organize Drum Samples

```python
# piano_workshop/scripts/organize_drum_samples.py

import os
import shutil
from pathlib import Path

SOURCE_DIR = "/Volumes/Storage/samples"
BUILD_DIR = "piano_workshop/build/drum_kits"

def organize_808():
    """Organize TR-808 samples into GM structure"""
    src = f"{SOURCE_DIR}/Roland - JeuneLys_Beatz/ROLAND_TR-808_(1980)"
    dest = f"{BUILD_DIR}/tr808_gm"

    # Create directories
    os.makedirs(f"{dest}/kick", exist_ok=True)
    os.makedirs(f"{dest}/snare", exist_ok=True)
    os.makedirs(f"{dest}/hihat_closed", exist_ok=True)
    os.makedirs(f"{dest}/hihat_open", exist_ok=True)

    # Copy and rename samples based on folder structure
    # [BD]_Bass_Drum → kick/
    # [SD]_Snare_Drum → snare/
    # [CH]_Closed_Hat → hihat_closed/
    # [OH]_Open_Hat → hihat_open/

    print("✅ TR-808 organized")

def organize_909():
    """Organize TR-909 samples"""
    # Similar structure
    pass

def organize_retro():
    """Organize retro drum machines into single SF2"""
    # Blofeld, Vermona DRM-1, XL-7 → retro_machines.sf2
    pass

if __name__ == "__main__":
    organize_808()
    organize_909()
    organize_retro()
```

### Script 2: Generate SFZ from Samples

```python
# piano_workshop/scripts/generate_drum_sfz.py

def generate_808_sfz():
    """Auto-generate SFZ file for TR-808"""
    sfz_content = """// Roland TR-808 GM Standard
// Generated automatically

// Kick (C1)
<region>
sample=kick/808_kick_c1.wav
lokey=36 hikey=36 pitch_keycenter=36
ampeg_attack=0.001 ampeg_decay=0.1 ampeg_sustain=0 ampeg_release=0.5

// Snare (D1)
<region>
sample=snare/808_snare_d1.wav
lokey=38 hikey=38 pitch_keycenter=38
ampeg_attack=0.001 ampeg_decay=0.15 ampeg_sustain=0 ampeg_release=0.3
"""

    with open("build/drum_kits/tr808_gm/roland_tr808.sfz", "w") as f:
        f.write(sfz_content)
```

---

## Integration with JUCE

### Loading Drum Kits

```cpp
// In your JUCE audio engine

// Load a drum kit SF2
SF2::SF2InstrumentFactory factory;
auto drumKit808 = factory.createLayerFromSF2(
    File("piano_workshop/dist/drum_kits/roland_tr808.sf2"),
    0  // preset 0 = GM Standard
);

if (drumKit808)
{
    // Add to engine
    engine->addLayer(std::move(drumKit808));
}

// Play drum sounds via MIDI
// MIDI note 36 (C1) = Kick
// MIDI note 38 (D1) = Snare
// MIDI note 42 (F#1) = Closed Hi-Hat
```

### Drum Kit Selector UI

```cpp
// Drum kit selection in UI
juce::StringArray drumKits = {
    "Roland TR-808",
    "Roland TR-909",
    "Roland TR-606",
    "Retro Machines"
};

// Load selected kit
void loadDrumKit(int index)
{
    auto kitFile = drumKits[index] + ".sf2";
    auto kitPath = File("piano_workshop/dist/drum_kits/" + kitFile);

    auto layer = SF2::SF2InstrumentFactory::createLayerFromSF2(kitPath);
    engine->addLayer(std::move(layer));
}
```

---

## Velocity Layer Strategy

### Option A: Multiple Samples (Best for Drums)

```
Kick: 3 velocity layers
- v1: vel 0-42  (soft)
- v2: vel 43-84 (medium)
- v3: vel 85-127 (hard)
```

### Option B: Single Sample (Simpler)

```
Kick: 1 sample, full velocity range
- Use velocity for volume only
```

**Recommendation:** Use **Option A** for drums like kick/snare with distinct timbre changes. Use **Option B** for hi-hats and percussion.

---

## Testing & Validation

### SF2 Validation Checklist

- [ ] All samples load correctly
- [ ] GM Standard mapping works (C1=Kick, D1=Snare)
- [ ] Velocity layers trigger correctly
- [ ] No missing samples
- [ ] Release times appropriate
- [ ] File size reasonable (< 15MB per kit)

### MIDI Validation

```cpp
// Test script to verify drum mapping
void testDrumKit(SF2Loader& loader)
{
    // Test kick
    auto kickSamples = loader.findSamplesForNote(36, 100);
    jassert(kickSamples.size() > 0);

    // Test snare
    auto snareSamples = loader.findSamplesForNote(38, 100);
    jassert(snareSamples.size() > 0);

    // Test hi-hat
    auto hatSamples = loader.findSamplesForNote(42, 100);
    jassert(hatSamples.size() > 0);
}
```

---

## Next Steps

1. ✅ Review this architecture
2. ⏳ Create `organize_drum_samples.py` script
3. ⏳ Organize TR-808 samples
4. ⏳ Generate SFZ for TR-808
5. ⏳ Convert to SF2 using Polyphone
6. ⏳ Test in JUCE
7. ⏳ Repeat for TR-909, TR-606, etc.
8. ⏳ Create drum manifest JSON

---

## References

- **GM Drum Mapping**: https://www.midi.org/specifications-old/item/gm-standard
- **SFZ Format**: https://sfzformat.com/
- **Polyphone**: https://www.polyphone-soundfonts.com/
- **Roland TR-808 Documentation**: Available in `/Volumes/Storage/samples/Roland - JeuneLys_Beatz/ROLAND_TR-808_(1980)/TR-808_infos.txt`

---

**Status:** Architecture defined
**Last Updated:** 2024-12-24
**Next:** Implement organization scripts
