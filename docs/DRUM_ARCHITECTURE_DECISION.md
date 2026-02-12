# Drum SF2 Architecture Decision

## Question

**Should we create one SF2 per drum machine, or one big SF2 with all drum machines?**

---

## 🎯 Decision: **One SF2 Per Drum Machine** (Modular)

### ✅ Recommended Structure

```
piano_workshop/dist/drum_kits/
├── roland_tr808.sf2           # ~8-10MB, 173 samples
├── roland_tr909.sf2           # ~8-10MB
├── roland_tr606.sf2           # ~5-7MB
├── roland_tr707.sf2           # ~5-7MB
├── roland_tr505.sf2           # ~5-7MB
├── retro_machines.sf2         # ~15-20MB (Blofeld, DRM-1, XL-7)
└── vintage_collection.sf2     # ~10-15MB (E-mu, R100, Mars)
```

---

## 📊 Comparison: Modular vs Monolithic

| **Criterion** | **Modular (One SF2 Each)** ✅ | **Monolithic (All-in-One)** ❌ |
|---------------|------------------------------|-------------------------------|
| **Load Time** | Fast (5-10MB per kit) | Slow (50-100MB) |
| **Memory** | Load only what you need | Must load everything |
| **Organization** | Clear, manageable | Difficult to navigate |
| **Distribution** | Share individual kits | All or nothing |
| **Version Control** | Small commits | Large binary blobs |
| **Updates** | Update one kit | Rebuild entire library |
| **Flexibility** | Easy to add/remove kits | Complex restructuring |
| **File Size** | 8-20MB each | 50-100MB total |
| **Preset Switching** | SF2 file switching | Internal preset switching |

---

## 🎹 Why Modular is Better for Drums

### 1. **Fast Switching Between Kits**
```cpp
// Quick kit change
void loadDrumKit(const String& kitName) {
    auto kitFile = "drum_kits/" + kitName + ".sf2";
    auto layer = SF2::SF2InstrumentFactory::createLayerFromSF2(File(kitFile));
    engine->addLayer(std::move(layer));
}

// Usage:
loadDrumKit("roland_tr808");  // 8MB load
loadDrumKit("roland_tr909");  // 8MB load
```

### 2. **Memory Efficient**
- Only load the kit you're using
- Unload old kit when switching
- Better for mobile/resource-constrained environments

### 3. **Better User Experience**
- Faster app startup
- Quicker kit browsing
- Smaller downloads if distributing

### 4. **Easier Development**
- Test one kit at a time
- Smaller files for version control
- Modular testing workflow

---

## 🎼 When to Use Monolithic SF2

Monolithic (all-in-one) makes sense for:

1. **Pianos with multiple mic positions**
   - One SF2 per piano, but all mics included
   - Presets for "Close", "Room", "Mix"

2. **Orchestral libraries**
   - All sections in one file (strings, brass, winds)
   - Key switching for articulations

3. **Sound effects libraries**
   - Related sounds grouped together
   - Categories as presets

**For drums? Modular is better.**

---

## 🚀 Implementation Strategy

### Phase 1: Create Individual SF2 Files

```bash
# 1. Organize samples
python3 piano_workshop/scripts/organize_drum_samples.py

# 2. Create SF2 for each machine
# Using Polyphone:
# - Import: piano_workshop/build/drum_kits/tr808_gm/roland_tr808.sfz
# - Export: piano_workshop/dist/drum_kits/roland_tr808.sf2

# 3. Repeat for each kit
# roland_tr808.sf2  ✅
# roland_tr909.sf2  ✅
# roland_tr606.sf2  ✅
# retro_machines.sf2 ✅
```

### Phase 2: JUCE Integration

```cpp
// Drum kit manager
class DrumKitManager {
public:
    struct KitInfo {
        String id;
        String name;
        String filename;
        int sizeMB;
    };

    Array<KitInfo> getAvailableKits() {
        return {
            {"tr808", "Roland TR-808", "roland_tr808.sf2", 8},
            {"tr909", "Roland TR-909", "roland_tr909.sf2", 8},
            {"retro", "Retro Machines", "retro_machines.sf2", 15}
        };
    }

    std::unique_ptr<MinimalSamLayer> loadKit(const String& kitId) {
        auto kit = getAvailableKits()[indexOf(kitId)];
        auto path = resourcesPath + "drum_kits/" + kit.filename;

        return SF2::SF2InstrumentFactory::createLayerFromSF2(File(path));
    }
};
```

### Phase 3: UI Integration

```dart
// Flutter UI for kit selection
class DrumKitSelector extends StatelessWidget {
  final kits = [
    'Roland TR-808',
    'Roland TR-909',
    'Roland TR-606',
    'Retro Machines',
  ];

  @override
  Widget build(BuildContext context) {
    return DropdownButton(
      items: kits.map((kit) {
        return DropdownMenuItem(
          value: kit,
          child: Text(kit),
        );
      }).toList(),
      onChanged: (value) {
        // Load kit via JUCE backend
        loadDrumKit(value);
      },
    );
  }
}
```

---

## 📁 File Organization

### Source Structure
```
/Volumes/Storage/samples/
├── Roland - JeuneLys_Beatz/
│   ├── ROLAND_TR-808_(1980)/    → roland_tr808.sf2
│   ├── ROLAND_TR-909_(1983)/    → roland_tr909.sf2
│   └── [other Roland kits]
│
└── retro drum-machine/
    ├── blofeld drumkit/          } → retro_machines.sf2
    ├── Vermona DRM-1/            }    (combined)
    └── xl7 drumkit/              }
```

### Built Structure
```
piano_workshop/
├── build/drum_kits/
│   ├── tr808_gm/                # Organized samples + SFZ
│   ├── tr909_gm/
│   └── retro_machines/
│
└── dist/drum_kits/              # Final SF2 files
    ├── roland_tr808.sf2         # ← Distribution ready
    ├── roland_tr909.sf2
    └── retro_machines.sf2
```

---

## 🎛️ Preset Strategy

### Each SF2 Contains Multiple Presets

```
roland_tr808.sf2
├── Preset 0: "TR-808 GM Standard"    # General MIDI mapping
├── Preset 1: "TR-808 Extended"       # Full velocity layers
└── Preset 2: "TR-808 Raw"            # Unprocessed samples
```

**Benefits:**
- Multiple articulations in one file
- Faster than loading multiple SF2s
- Still modular across different drum machines

---

## 📦 Distribution Strategy

### Option A: Individual Downloads
```
drum-kits/
├── roland-tr808-v1.0.0.sf2      # 8MB
├── roland-tr909-v1.0.0.sf2      # 8MB
└── retro-machines-v1.0.0.sf2    # 15MB
```

### Option B: Collection Bundle
```
drum-kits-bundle/
├── roland_tr808.sf2
├── roland_tr909.sf2
├── roland_tr606.sf2
├── retro_machines.sf2
└── manifest.json
```

**Recommendation:** Both!
- Individual downloads for flexibility
- Bundle for convenience

---

## ✅ Decision Summary

| **Aspect** | **Choice** | **Reason** |
|------------|------------|------------|
| **Architecture** | Modular (one SF2 per machine) | Performance, flexibility |
| **File Size** | 8-20MB each | Fast load, memory efficient |
| **Presets** | 3 per SF2 | Multiple articulations |
| **Distribution** | Individual + bundle | Flexibility + convenience |
| **Organization** | By drum machine | Clear, logical structure |

---

## 🎯 Success Criteria

- [ ] Each drum machine has its own SF2 file
- [ ] File sizes are reasonable (8-20MB each)
- [ ] GM Standard MIDI mapping works
- [ ] Fast load times (< 2 seconds per kit)
- [ ] Easy kit switching in UI
- [ ] All samples accounted for
- [ ] Proper attribution included

---

## 🔄 Next Steps

1. ✅ Review architecture decision
2. ⏳ Run `organize_drum_samples.py`
3. ⏳ Create SF2 files in Polyphone
4. ⏳ Test in JUCE
5. ⏳ Implement UI kit selector
6. ⏳ Create drum manifest JSON

---

**Decision Date:** 2024-12-24
**Status:** Approved
**Next Action:** Run organization script
