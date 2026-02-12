# Piano Workshop Validation Command

## Overview

Comprehensive validation for the Piano Workshop asset preparation pipeline.

## Usage

```bash
/validate
```

---

## Validation Phases

### Phase 1: Dependency Check

**Check for required tools:**

```bash
# Check Python 3.8+
python3 --version

# Check ffmpeg
ffmpeg -version

# Check Polyphone (optional for Phase 1)
polyphone --version || echo "Polyphone not installed (required for SF2 creation)"
```

**Exit on failure:**
- Python 3 not found
- ffmpeg not found

### Phase 2: Python Syntax Validation

**Validate all Python scripts:**

```bash
# Check syntax for all scripts
python3 -m py_compile scripts/*.py

# Run pylint if available
command -v pylint >/dev/null 2>&1 && pylint scripts/*.py || echo "pylint not installed, skipping"
```

**Exit on failure:**
- Syntax errors in any .py file

### Phase 3: Asset Validation

**Check build directory:**

```bash
# Verify build directory exists
test -d build/salamander_wav || echo "ERROR: build/salamander_wav not found"

# Verify sample count (should be 641 WAV files)
sample_count=$(find build/salamander_wav/Samples -name "*.wav" | wc -l)
if [ "$sample_count" -ne 641 ]; then
    echo "ERROR: Expected 641 samples, found $sample_count"
    exit 1
fi
```

**Validate SFZ files:**

```bash
# Run SFZ validation script
python3 scripts/validate_sfz.py
```

**Exit on failure:**
- Missing samples
- Incorrect sample count
- Invalid SFZ references

### Phase 4: Script Functionality Test

**Test core scripts:**

```bash
# Test validation script
python3 scripts/validate_sfz.py --dry-run

# Test SFZ analysis (dry run)
python3 scripts/analyze_sfz_structure.py --check-only
```

**Exit on failure:**
- Script execution errors
- Missing dependencies

### Phase 5: Documentation Check

**Verify required documentation:**

```bash
# Check README exists
test -f README.md || echo "WARNING: README.md not found"

# Check for phase documentation
test -f docs/PHASE1_COMPLETE.md || echo "WARNING: Phase 1 docs not found"
```

---

## Success Criteria

All phases must pass:
- ✅ Dependencies installed (Python 3, ffmpeg)
- ✅ No Python syntax errors
- ✅ All 641 WAV samples present
- ✅ SFZ files valid
- ✅ Scripts execute without errors
- ✅ Documentation present

---

## Common Issues

### "python3: command not found"
**Solution:** Install Python 3
```bash
brew install python3
```

### "ffmpeg: command not found"
**Solution:** Install ffmpeg
```bash
brew install ffmpeg
```

### "Sample count mismatch"
**Solution:** Re-run conversion
```bash
python3 scripts/convert_flac_to_wav.py
```

---

## Integration with CI/CD

Add to `.github/workflows/validate.yml`:

```yaml
name: Validate Piano Workshop

on: [push, pull_request]

jobs:
  validate:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: brew install ffmpeg
      - name: Validate assets
        run: /validate
```
