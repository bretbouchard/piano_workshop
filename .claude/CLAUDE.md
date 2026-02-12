# Piano Workshop - Claude Code Instructions

## Project Overview

This repository is a **Phase 1 asset preparation pipeline** for integrating Salamander Grand Piano into Sam Sampler. It handles FLAC → WAV conversion, SFZ file processing, and SF2 soundfont creation for the Schillinger music ecosystem.

**Status:** Phase 1 complete (assets prepared), Phase 2-4 pending (C++ implementation)

**Language:** Python (scripts), C++ (planned for Phase 2)

**Parent Project:** Schillinger Song Writing App (Flutter/Dart)

---

## Before Processing

Read from: `~/.claude/agent_scripts/agents.mmd`

---

## Mandatory Protocols

### 1. Beads Task Tracking (MANDATORY)

**ALWAYS check bd status before starting work:**

```bash
bd ready --json
```

**Create bd issues for ALL work:**

```bash
bd create "Task description" --type task
```

**No work proceeds without bd tracking.**

### 2. SLC Development Philosophy (MANDATORY)

**Simple, Lovable, Complete** - Every feature must meet ALL criteria:
- **Simple:** Obvious purpose, minimal learning
- **Lovable:** Delightful to use, builds trust
- **Complete:** Full user journey, no gaps

**SLC Anti-Patterns (FORBIDDEN):**
- No workarounds ("it works but..." solutions)
- No stub methods (empty/null placeholders)
- No "good enough" temporary solutions
- No UnimplementedError in production code

### 3. Project Context

This is an **asset preparation pipeline**, not the main application:
- **Current Phase:** Phase 1 (asset conversion) - COMPLETE
- **Next Phases:** Phase 2-4 (C++ implementation in parent project)
- **Location:** Subdirectory of Schillinger ecosystem
- **Dependencies:** ffmpeg, Python 3, Polyphone (for SF2 creation)

---

## Project-Specific Instructions

### Code Style

**Python:**
- Follow PEP 8
- Use type hints for all functions
- Docstrings for all public functions
- Maximum line length: 100 characters

**C++ (Phase 2+):**
- Follow JUCE coding style
- Use modern C++17/20 features
- RAII for resource management
- Const correctness

### Testing

**Python scripts must:**
- Validate inputs before processing
- Provide clear error messages
- Log progress for long operations
- Handle missing dependencies gracefully

**Asset validation:**
- Always verify sample counts (should be 641 WAV files)
- Validate SFZ file references
- Check file sizes (~500MB total)

### Common Commands

```bash
# Convert FLAC to WAV
python3 scripts/convert_flac_to_wav.py

# Update SFZ files
python3 scripts/create_complete_sfz.py

# Validate samples
python3 scripts/validate_sfz.py

# Check bd status
bd ready --json

# List bd issues
bd list
```

---

## Dependencies

### Required Tools

- **Python 3.8+**: Script execution
- **ffmpeg**: Audio conversion (FLAC → WAV)
- **Polyphone**: SF2 soundfont creation (GUI or CLI)

### Installation

```bash
# Install ffmpeg
brew install ffmpeg

# Install Polyphone
brew install polyphone

# Verify installation
ffmpeg -version
polyphone --version
```

---

## Phase Status

### ✅ Phase 1: Asset Preparation (COMPLETE)
- [x] FLAC → WAV conversion
- [x] SFZ file updates
- [x] Sample validation
- [ ] SF2 creation (manual step with Polyphone)

### ⏳ Phase 2: SF2 Loader (PENDING - C++ in parent project)
- [ ] RIFF/IFF parser
- [ ] Sample loading
- [ ] Preset/instrument mapping

### ⏳ Phase 3: Sustain Pedal (PENDING - C++ in parent project)
- [ ] CC64 detection
- [ ] Pedal state management
- [ ] Release sample triggering

### ⏳ Phase 4: Engine Integration (PENDING - C++ in parent project)
- [ ] MinimalSamEngine integration
- [ ] Voice/layer mapping
- [ ] Velocity curve implementation

---

## File Structure

```
piano_workshop/
├── src/SalamanderGrandPiano/     # Original source (FLAC + SFZ)
├── build/salamander_wav/         # Converted samples (WAV + SFZ)
├── dist/                         # Final distribution (SF2)
├── scripts/                      # Conversion and build scripts
└── docs/                         # Documentation
```

---

## Validation

**Before committing changes:**

1. **Run bd checks:**
   ```bash
   bd ready --json
   ```

2. **Validate assets:**
   ```bash
   python3 scripts/validate_sfz.py
   ```

3. **SLC validation:**
   - No workarounds or stubs
   - Complete functionality
   - Clear error messages

---

## Contact & References

- **Parent Project:** `../` (Schillinger Song Writing App)
- **Sample Source:** https://github.com/sfzinstruments/SalamanderGrandPiano
- **License:** CC-BY 3.0 (attribution required)

---

**Last Updated:** 2025-01-13
**Claude Code Version:** Compatible with Bret's AI Stack
