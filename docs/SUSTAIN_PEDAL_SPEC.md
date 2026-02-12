# Sustain Pedal Implementation Specification

## Overview

This document defines the **non-negotiable** sustain pedal behavior for Sam Sampler's piano implementation. The pedal logic is critical for authentic piano performance.

## Pedal State Detection

### MIDI CC64 Handling

```
CC64 < 64  → pedal UP
CC64 ≥ 64  → pedal DOWN
```

**Implementation:**

```cpp
// In MinimalSamEngine or MIDI handler
void processMidiController(int channel, int controllerNumber, float value) {
    if (controllerNumber == 64) {  // Sustain pedal
        bool pedalDown = (value >= 0.5f);  // 64/127 ≈ 0.5

        if (pedalDown && !sustainPedalState) {
            // Pedal pressed: transition UP → DOWN
            onPedalDown();
        } else if (!pedalDown && sustainPedalState) {
            // Pedal released: transition DOWN → UP
            onPedalUp();
        }

        sustainPedalState = pedalDown;
    }
}
```

## Note-Off Logic

### Pedal UP State (Normal)

When sustain pedal is **UP**, note-off triggers immediate release:

```cpp
void stopNote(int noteNumber, float velocity) {
    if (!sustainPedalState) {
        // Normal note-off: trigger release sample
        for (auto* voice : activeVoices) {
            if (voice->isPlayingNote(noteNumber)) {
                voice->triggerReleaseSample();
                voice->startReleaseEnvelope();
            }
        }
    }
    // If pedal DOWN: do nothing (see below)
}
```

### Pedal DOWN State (Sustain)

When sustain pedal is **DOWN**, note-off is **suppressed**:

```cpp
void stopNote(int noteNumber, float velocity) {
    if (sustainPedalState) {
        // Sustain: keep voice alive, suppress release
        // Voice continues playing natural sample tail
        // NO release sample triggered
        return;  // Early exit, no action
    }

    // Normal release logic (as above)
}
```

## Pedal Release (DOWN → UP Transition)

**Critical:** Release samples must fire **at pedal lift**, not at note-off.

```cpp
void onPedalUp() {
    // Trigger release samples for ALL sustained voices
    for (auto* voice : sustainedVoices) {
        voice->triggerReleaseSample();
        voice->startReleaseEnvelope();
    }

    sustainedVoices.clear();
}

void onPedalDown() {
    // Optional: Trigger pedal-down noise sample
    // playPedalDownSample();
}
```

## Voice State Management

Each voice tracks whether it's sustained:

```cpp
class SamVoice {
    bool isSustained = false;  // Flag for pedal state

    void stopNote(float velocity, bool allowTailOff) override {
        if (sustainPedalState) {
            // Mark as sustained, don't stop yet
            isSustained = true;
            return;  // Keep voice alive
        }

        // Normal note-off
        triggerReleaseSample();
        startReleaseEnvelope();
    }

    void onPedalUp() {
        if (isSustained) {
            triggerReleaseSample();
            startReleaseEnvelope();
            isSustained = false;
        }
    }
};
```

## Envelope Behavior

### Attack Samples (Note-On)

```
Attack: 0-5 ms (very fast)
Sustain: 0 (no sustain level)
Decay: natural sample tail
```

**Implementation:**

```cpp
// No synth-style ADSR for attack samples
// Play sample natural decay, let it ring
```

### Release Samples (Note-Off / Pedal-Up)

```
One-shot playback
No looping
No artificial sustain
Natural decay only
```

**Implementation:**

```cpp
void triggerReleaseSample() {
    // Load release sample for this note
    // Play once, no loop
    // Let sample decay naturally
    // Voice dies when sample ends
}
```

## Optional: Pedal Noise Samples

### Pedal Down Noise

```cpp
void onPedalDown() {
    // Trigger pedal_down.wav
    // Very low level
    // Non-velocity-scaled
    // One-shot playback
}
```

### Pedal Up Noise

```cpp
void onPedalUp() {
    // Trigger pedal_up.wav
    // Very low level
    // Non-velocity-scaled
    // One-shot playback
}
```

**Sample filenames (Salamander):**
- `pedalDn.wav` (pedal down)
- `pedalUp.wav` (pedal up)

## Velocity Curve (Recommended)

Apply soft-biased curve for realistic dynamics:

```cpp
float applyVelocityCurve(float inputVelocity) {
    // Input: 0.0 - 1.0
    // Output: 0.0 - 1.0 with bias toward soft

    return std::pow(inputVelocity, 1.6f);
}
```

**Rationale:**
- Pianists play softly more often than loudly
- `^1.6` gives more resolution at low velocities
- Loud playing doesn't collapse dynamically
- Matches Salamander's `amp_veltrack=73%` (0.73)

## Testing Scenarios

### Scenario 1: Single Note, Pedal Up

```
1. Press C4 (note-on)
2. Release C4 (note-off)
3. Expected: Release sample triggers immediately
```

### Scenario 2: Single Note, Pedal Down

```
1. Press sustain pedal
2. Press C4 (note-on)
3. Release C4 (note-off)
4. Expected: Note continues (no release sample)
5. Release pedal
6. Expected: Release sample triggers NOW
```

### Scenario 3: Repeated Notes, Pedal Down

```
1. Press sustain pedal
2. Play C4, D4, E4 rapidly
3. Release all keys
4. Expected: All notes sustain (no releases)
5. Release pedal
6. Expected: All release samples trigger simultaneously
```

### Scenario 4: Pedal Sync

```
1. Play C4, hold
2. Press pedal (while holding C4)
3. Release C4
4. Expected: Note sustains
5. Release pedal
6. Expected: Release sample triggers
```

## Non-Goals (v1)

**NOT implementing in initial release:**
- Half-pedaling (continuous CC64 values)
- Sympathetic resonance modeling
- Una corda (soft pedal)
- Pedal-down attack sample variations
- Round-robin sample cycling

## Integration Points

### SamVoice

```cpp
class SamVoice {
    bool isSustained = false;

    void stopNote(float velocity, bool allowTailOff) override;
    void onPedalUp();  // New method
    void triggerReleaseSample();  // New method
};
```

### MinimalSamEngine

```cpp
class MinimalSamEngine {
    bool sustainPedalState = false;
    std::vector<SamVoice*> sustainedVoices;

    void processMidiController(int channel, int controllerNumber, float value) override;
    void onPedalDown();
    void onPedalUp();
};
```

### MIDI Routing

```
MIDI Input → MinimalSamEngine::processMidiController()
           ↓
           CC64 detected
           ↓
           Update sustainPedalState
           ↓
           Trigger onPedalDown() / onPedalUp()
           ↓
           Notify all voices
```

## Validation Checklist

Before marking piano complete:

- [ ] Pedal UP: Note-off triggers immediate release
- [ ] Pedal DOWN: Note-off suppresses release
- [ ] Pedal DOWN → UP: Release samples fire
- [ ] Repeated notes with pedal: All sustain properly
- [ ] No "choked" notes when pedal down
- [ ] Release samples trigger at pedal lift, not before
- [ ] Pedal noise samples (optional) trigger correctly
- [ ] Velocity curve applied (input^1.6)
- [ ] No double-release artifacts

## References

- **Salamander SFZ:** Check `Salamander Grand Piano V3.sfz` for release triggers
- **SFZ `off_by` opcode:** Used for note self-masking
- **SFZ `sw_last`:** Keyswitch implementation
- **JUCE MPENote:** MIDI message handling
- **JUCE SynthesiserVoice:** Voice lifecycle

---

**Status:** Specification complete, ready for implementation
**Priority:** CRITICAL (non-negotiable for authentic piano behavior)
**Dependencies:** Phase 1 (SF2 asset), Phase 2 (SF2 loader)
