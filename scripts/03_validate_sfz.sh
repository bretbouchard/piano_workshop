#!/bin/bash
# Validate SFZ file and verify all referenced samples exist
# Phase 1, Step 3: Validation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_ROOT="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$WORKSHOP_ROOT/build/salamander_wav"
SFZ_FILE="$BUILD_DIR/Salamander Grand Piano V3.wav.sfz"

echo "========================================"
echo "SFZ Validation"
echo "========================================"
echo ""

if [ ! -f "$SFZ_FILE" ]; then
    echo "✗ ERROR: SFZ file not found: $SFZ_FILE"
    echo "Run 02_create_modified_sfz.sh first"
    exit 1
fi

# Extract sample references from SFZ
echo "Checking sample references..."
MISSING=0
FOUND=0
TOTAL=0

while IFS= read -r line; do
    # Look for sample= directives
    if [[ $line =~ sample=[[:space:]]*([^[:space:]]+) ]]; then
        sample_ref="${BASH_REMATCH[1]}"

        # Remove quotes if present
        sample_ref="${sample_ref%\"}"
        sample_ref="${sample_ref#\"}"

        # Skip if it's a wildcard or control file
        if [[ $sample_ref == *"*"* ]] || [[ $sample_ref == *".txt"* ]]; then
            continue
        fi

        TOTAL=$((TOTAL + 1))
        sample_path="$BUILD_DIR/Samples/$sample_ref"

        if [ -f "$sample_path" ]; then
            FOUND=$((FOUND + 1))
        else
            echo "  ✗ Missing: $sample_ref"
            MISSING=$((MISSING + 1))
        fi
    fi
done < "$SFZ_FILE"

echo ""
echo "========================================"
echo "Validation Results"
echo "========================================"
echo "Total samples referenced: $TOTAL"
echo "Found:                    $FOUND"
echo "Missing:                  $MISSING"
echo ""

if [ $MISSING -eq 0 ]; then
    echo "✓ All samples present!"
    echo ""
    echo "Next step: Run 04_build_sf2.sh (requires Polyphone)"
else
    echo "✗ Validation failed - missing samples"
    exit 1
fi
