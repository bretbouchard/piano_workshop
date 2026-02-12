#!/bin/bash
# Create modified SFZ file pointing to WAV files instead of FLAC
# Phase 1, Step 2: Update SFZ mappings

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_ROOT="$(dirname "$SCRIPT_DIR")"
SOURCE_SFZ="$WORKSHOP_ROOT/src/SalamanderGrandPiano/Salamander Grand Piano V3.sfz"
OUTPUT_SFZ="$WORKSHOP_ROOT/build/salamander_wav/Salamander Grand Piano V3.wav.sfz"

echo "========================================"
echo "Creating WAV-compatible SFZ file"
echo "========================================"
echo ""
echo "Source: $SOURCE_SFZ"
echo "Output: $OUTPUT_SFZ"
echo ""

# Create modified SFZ by replacing FLAC references with WAV
sed 's/\.flac/.wav/g; s/#define \$EXT flac/#define $EXT wav/g' "$SOURCE_SFZ" > "$OUTPUT_SFZ"

# Verify the conversion
if [ -f "$OUTPUT_SFZ" ]; then
    WAV_REFS=$(grep -c "\.wav" "$OUTPUT_SFZ")
    FLAC_REFS=$(grep -c "\.flac" "$OUTPUT_SFZ")

    echo "✓ Modified SFZ created successfully"
    echo "  - WAV references:  $WAV_REFS"
    echo "  - FLAC references: $FLAC_REFS (should be 0 in header)"
    echo ""
    echo "Next step: Run 03_validate_sfz.sh"
else
    echo "✗ ERROR: Failed to create modified SFZ"
    exit 1
fi
