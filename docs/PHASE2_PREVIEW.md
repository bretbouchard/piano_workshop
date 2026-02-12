# Phase 2 Preview: SF2 Loader Implementation

## Overview

This document outlines the implementation plan for Phase 2: SF2 Loader in JUCE/C++.

## Architecture

### File Structure

```
src/engine/sf2/
├── SF2Loader.h                  # Main loader interface
├── SF2Loader.cpp                # Implementation
├── SF2Structures.h              # RIFF/IFF structure definitions
├── SF2Reader.h                  # Low-level chunk reading
├── SF2Reader.cpp
└── SF2SampleExtractor.h         # Extract samples to memory
```

### Integration Point

```cpp
// In MinimalSamEngine.h
#include "sf2/SF2Loader.h"

class MinimalSamEngine {
private:
    std::unique_ptr<SF2Loader> sf2Loader;

public:
    bool loadInstrument(const juce::File& sf2File);
    // ... existing methods
};
```

## SF2 Format Overview

### RIFF Structure

```
RIFF (size)
├── LIST (INFO) - Metadata
│   ├── ifil = 2.01 (version)
│   ├── isng = EMU8000
│   ├── INAM = "Salamander Grand Piano"
│   └── IENG = "Alexander Holm"
│
├── LIST (sdta) - Sample Data
│   └── smpl (raw 16-bit PCM)
│
└── LIST (pdta) - Orchestration
    ├── phdr (Preset Headers)
    ├── pbag (Preset Zones)
    ├── pmod (Preset Modulators)
    ├── pgen (Preset Generators)
    ├── ihdr (Instrument Headers)
    ├── ibag (Instrument Zones)
    ├── imod (Instrument Modulators)
    ├── igen (Instrument Generators)
    └── shdr (Sample Headers)
```

## Implementation Plan

### Step 1: SF2 Structures (SF2Structures.h)

```cpp
#pragma once
#include <JuceHeader.h>

namespace SF2 {

// Chunk identifiers
static constexpr const char* RIFF_ID = "RIFF";
static constexpr const char* LIST_ID = "LIST";
static constexpr const char* SFBK_ID = "sfbk";
static constexpr const char* INFO_ID = "INFO";
static constexpr const char* SDTA_ID = "sdta";
static constexpr const char* PDTA_ID = "pdta";

// Generators
enum class GeneratorType : uint16_t {
    startAddrsOffset = 0,
    endAddrsOffset = 1,
    startLoopAddrsOffset = 2,
    endLoopAddrsOffset = 3,
    startAddrsCoarseOffset = 4,
    modLfoToPitch = 5,
    vibLfoToPitch = 6,
    modEnvToPitch = 7,
    initialFilterFc = 8,
    initialFilterQ = 9,
    modLfoToFilterFc = 10,
    modEnvToFilterFc = 11,
    endAddrsCoarseOffset = 12,
    modLfoToVolume = 13,
    // ... more generators
    keyRange = 43,
    velRange = 44,
    keynum = 46,
    velocity = 47,
    initialAttenuation = 48,
    // ... etc
};

struct SampleHeader {
    char name[20];
    uint32_t start;
    uint32_t end;
    uint32_t startLoop;
    uint32_t endLoop;
    uint32_t sampleRate;
    uint8_t originalPitch;
    char pitchCorrection;
    uint16_t sampleLink;
    uint16_t sampleType;
};

struct InstrumentZone {
    uint16_t generatorIndex;
    uint16_t modulatorIndex;
};

struct Instrument {
    char name[20];
    uint16_t firstZoneIndex;
    uint16_t lastZoneIndex;
};

struct PresetHeader {
    char name[20];
    uint16_t preset;
    uint16_t bank;
    uint16_t firstZoneIndex;
    uint32_t library;
    uint32_t genre;
    uint32_t morphology;
};

struct Generator {
    GeneratorType type;
    int16_t amount;
    // uint16_t amountWord; // for some generators
};

} // namespace SF2
```

### Step 2: SF2 Reader (SF2Reader.h/cpp)

```cpp
#pragma once
#include "SF2Structures.h"
#include <JuceHeader.h>

class SF2Reader {
public:
    SF2Reader(const juce::File& file);
    ~SF2Reader();

    bool load();
    bool isValid() const { return valid; }

    // Chunk access
    const juce::MemoryBlock& getSampleData() const { return sampleData; }
    const std::vector<SF2::SampleHeader>& getSampleHeaders() const { return sampleHeaders; }
    const std::vector<SF2::Instrument>& getInstruments() const { return instruments; }
    const std::vector<SF2::PresetHeader>& getPresetHeaders() const { return presetHeaders; }
    const std::vector<SF2::Generator>& getGenerators() const { return generators; }

private:
    juce::File file;
    bool valid = false;

    // Chunk data
    juce::MemoryBlock sampleData;  // sdta/smpl
    std::vector<SF2::SampleHeader> sampleHeaders;  // pdta/shdr
    std::vector<SF2::Instrument> instruments;  // pdta/ihdr
    std::vector<SF2::InstrumentZone> instrumentZones;  // pdta/ibag
    std::vector<SF2::PresetHeader> presetHeaders;  // pdta/phdr
    std::vector<SF2::Generator> generators;  // pdta/igen

    // Parsing
    bool parseRIFF();
    bool parseINFO(juce::InputStream& stream);
    bool parseSDTA(juce::InputStream& stream);
    bool parsePDTA(juce::InputStream& stream);

    // Helpers
    juce::String readFourCC(juce::InputStream& stream);
    uint32_t readChunkSize(juce::InputStream& stream);
};
```

### Step 3: Sample Extraction (SF2SampleExtractor.h)

```cpp
#pragma once
#include "SF2Structures.h"
#include <JuceHeader.h>

struct SampleRegion {
    int rootKey;
    int keyLow, keyHigh;
    int velLow, velHigh;

    juce::AudioBuffer<float> sampleData;
    double sampleRate;

    bool hasLoop;
    int loopStart, loopEnd;

    // Envelope
    float attack;
    float decay;
    float sustain;
    float release;
};

class SF2SampleExtractor {
public:
    static std::vector<SampleRegion> extractRegions(
        const SF2::SampleHeader& header,
        const juce::MemoryBlock& sampleData,
        const std::vector<SF2::Generator>& generators,
        int zoneIndex
    );

private:
    static juce::AudioBuffer<float> decodeSamples(
        const juce::MemoryBlock& sampleData,
        uint32_t start,
        uint32_t end
    );

    static void applyGenerators(
        SampleRegion& region,
        const std::vector<SF2::Generator>& generators,
        int genStart,
        int genEnd
    );
};
```

### Step 4: Main Loader (SF2Loader.h/cpp)

```cpp
#pragma once
#include "SF2Reader.h"
#include "SF2SampleExtractor.h"
#include <JuceHeader.h>

class SF2Loader {
public:
    SF2Loader();
    ~SF2Loader();

    bool loadFromFile(const juce::File& sf2File);

    // Query interface
    std::vector<SampleRegion> getRegionsForNote(int noteNumber, int velocity);
    SampleRegion* getRegion(int index);
    int getNumRegions() const { return regions.size(); }

    // Metadata
    juce::String getInstrumentName() const;
    juce::String getAuthor() const;
    juce::String getLicense() const;

private:
    std::unique_ptr<SF2Reader> reader;
    std::vector<SampleRegion> regions;

    bool buildSampleRegions();
    void mapInstrumentsToRegions();
};
```

### Step 5: Integration with MinimalSamEngine

```cpp
// In MinimalSamEngine.cpp
bool MinimalSamEngine::loadInstrument(const juce::File& sf2File) {
    auto loader = std::make_unique<SF2Loader>();

    if (!loader->loadFromFile(sf2File)) {
        return false;
    }

    // Create new layer from SF2 regions
    auto layer = std::make_unique<MinimalSamLayer>();

    for (int i = 0; i < loader->getNumRegions(); i++) {
        auto* region = loader->getRegion(i);
        layer->addSampleRegion(*region);
    }

    addLayer(std::move(layer));
    return true;
}
```

## Implementation Order

1. **SF2Structures.h** - Data structures (1-2 hours)
2. **SF2Reader** - Low-level RIFF parsing (4-6 hours)
3. **SF2SampleExtractor** - Convert SF2 samples to AudioBuffer (3-4 hours)
4. **SF2Loader** - High-level interface (2-3 hours)
5. **MinimalSamEngine integration** - Wire into engine (2-3 hours)

**Total estimate:** 12-18 hours

## Testing Strategy

```cpp
// Unit test: SF2ReaderTest.cpp
void testLoadSF2() {
    auto testFile = getTestResourceFile("test_piano.sf2");
    SF2Reader reader(testFile);

    EXPECT(reader.load());
    EXPECT(reader.isValid());
    EXPECT(reader.getSampleHeaders().size() > 0);
    EXPECT(reader.getInstruments().size() > 0);
}

// Unit test: SF2SampleExtractorTest.cpp
void testExtractSample() {
    auto loader = loadTestSF2();
    auto regions = loader.getRegionsForNote(60, 64);

    EXPECT(regions.size() > 0);
    EXPECT(regions[0].sampleData.getNumSamples() > 0);
    EXPECT(regions[0].rootKey == 60);
}
```

## Known Challenges

### 1. Endianness
SF2 uses little-endian. JUCE handles this, but verify on big-endian systems.

```cpp
uint16_t readUint16(juce::InputStream& stream) {
    return stream.readShort();  // JUCE handles endianness
}
```

### 2. Sample Linking
Some samples reference others (stereo pairs, release layers).

```cpp
if (header.sampleLink != 0) {
    // Handle linked samples
    auto& linkedHeader = sampleHeaders[header.sampleLink];
    // Process linked sample
}
```

### 3. Generator Amounts
Some generators use `uint16_t` amounts, others use `int16_t`.

```cpp
union GeneratorAmount {
    int16_t asInt16;
    uint16_t asUint16;
};
```

## References

- **SF2 2.01 Spec:** https://www.synthfont.com/SoundFont2.0.pdf
- **RIFF Format:** https://en.wikipedia.org/wiki/Resource_Interchange_File_Format
- **JUCE AudioFormat:** `juce_audio_formats/codecs/juce_AudioFormatReader.h`
- **JUCE MemoryBlock:** `juce_core/memory/juce_MemoryBlock.h`

---

**Status:** Specification complete, ready for implementation
**Dependencies:** Phase 1 complete (SF2 asset required)
**Estimated Effort:** 12-18 hours
**Risk Level:** Medium (RIFF parsing is well-documented)
