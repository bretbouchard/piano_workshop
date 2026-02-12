#!/bin/bash
# Convert Salamander Grand Piano FLAC samples to WAV (16-bit, 44.1kHz)
# Phase 1, Step 1: Audio format conversion

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_ROOT="$(dirname "$SCRIPT_DIR")"
SOURCE_DIR="$WORKSHOP_ROOT/src/SalamanderGrandPiano/Samples"
BUILD_DIR="$WORKSHOP_ROOT/build/salamander_wav"

echo "========================================"
echo "Salamander Grand Piano FLAC → WAV Converter"
echo "========================================"
echo ""
echo "Source: $SOURCE_DIR"
echo "Build:  $BUILD_DIR"
echo ""

# Create build directory
mkdir -p "$BUILD_DIR"

# Count FLAC files
FLAC_COUNT=$(find "$SOURCE_DIR" -name "*.flac" | wc -l | tr -d ' ')
echo "Found $FLAC_COUNT FLAC files to convert"
echo ""

# Track progress
PROCESSED=0
FAILED=0

# Convert each FLAC file
find "$SOURCE_DIR" -name "*.flac" -print0 | while IFS= read -r -d '' flac_file; do
    # Get relative path
    rel_path="${flac_file#$SOURCE_DIR/}"
    wav_file="$BUILD_DIR/${rel_path%.flac}.wav"

    # Create subdirectory if needed
    wav_dir=$(dirname "$wav_file")
    mkdir -p "$wav_dir"

    # Convert: FLAC (48kHz/24-bit) → WAV (44.1kHz/16-bit)
    if ffmpeg -i "$flac_file" -ar 44100 -ac 1 -sample_fmt s16 -y "$wav_file" 2>/dev/null; then
        PROCESSED=$((PROCESSED + 1))
        if [ $((PROCESSED % 50)) -eq 0 ]; then
            echo "Progress: $PROCESSED/$FLAC_COUNT files converted"
        fi
    else
        echo "ERROR: Failed to convert $flac_file"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "========================================"
echo "Conversion Complete!"
echo "========================================"
echo "Successfully converted: $PROCESSED files"
echo "Failed:                $FAILED files"
echo "Output directory:      $BUILD_DIR"
echo ""
echo "Next step: Run 02_create_modified_sfz.sh"
