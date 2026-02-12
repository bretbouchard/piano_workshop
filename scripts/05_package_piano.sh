#!/bin/bash
# Package the completed piano for distribution
# Phase 1, Step 5: Create distribution package

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_ROOT="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$WORKSHOP_ROOT/dist"

echo "========================================"
echo "Packaging Salamander Grand Piano"
echo "========================================"
echo ""

# Verify SF2 exists
SF2_FILE="$DIST_DIR/salamander_grand_v1.sf2"
if [ ! -f "$SF2_FILE" ]; then
    echo "✗ ERROR: SF2 file not found: $SF2_FILE"
    echo "Complete SF2 conversion first (Step 4)"
    exit 1
fi

# Get file size
SIZE_BYTES=$(stat -f%z "$SF2_FILE" 2>/dev/null || stat -c%s "$SF2_FILE" 2>/dev/null)
SIZE_MB=$((SIZE_BYTES / 1024 / 1024))

echo "Found SF2: $SF2_FILE"
echo "Size: ${SIZE_MB} MB"
echo ""

# Create manifest
cat > "$DIST_DIR/piano_manifest.json" << EOF
{
  "name": "Salamander Grand Piano",
  "version": "1.0.0",
  "format": "SF2",
  "sample_rate": 44100,
  "bit_depth": 16,
  "channels": 1,
  "velocity_layers": 16,
  "note_range": {
    "min": 21,
    "max": 108,
    "min_name": "A0",
    "max_name": "C8"
  },
  "release_samples": true,
  "file_size_mb": $SIZE_MB,
  "license": "CC-BY 3.0",
  "attribution": "Alexander Holm",
  "source_url": "https://github.com/sfzinstruments/SalamanderGrandPiano",
  "converted_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "converter": "Sam Sampler Piano Build Pipeline",
  "features": {
    "sustain_pedal": true,
    "release_samples": true,
    "hammer_noise": true,
    "string_resonance": true,
    "pedal_noise": true,
    "velocity_response": "dynamic",
    "polyphony": "optimized"
  }
}
EOF

echo "✓ Created manifest: piano_manifest.json"
echo ""

# Create package structure
PKG_DIR="$DIST_DIR/sam_sampler_piano"
mkdir -p "$PKG_DIR/piano"

# Copy files
cp "$SF2_FILE" "$PKG_DIR/piano/"
cp "$DIST_DIR/attribution.txt" "$PKG_DIR/piano/"
cp "$DIST_DIR/piano_manifest.json" "$PKG_DIR/"

echo "Package structure:"
echo "  sam_sampler_piano/"
echo "    ├── piano/"
echo "    │   ├── salamander_grand_v1.sf2"
echo "    │   └── attribution.txt"
echo "    └── piano_manifest.json"
echo ""

# Create archive
cd "$DIST_DIR"
tar -czf "sam_sampler_piano.tar.gz" "sam_sampler_piano/"
ARCHIVE_SIZE=$(stat -f%z "sam_sampler_piano.tar.gz" 2>/dev/null || stat -c%s "sam_sampler_piano.tar.gz" 2>/dev/null)
ARCHIVE_MB=$((ARCHIVE_SIZE / 1024 / 1024))

echo "========================================"
echo "Packaging Complete!"
echo "========================================"
echo ""
echo "Created: $DIST_DIR/sam_sampler_piano.tar.gz"
echo "Archive size: ${ARCHIVE_MB} MB"
echo ""
echo "Contents:"
ls -lh "$PKG_DIR/piano/"
echo ""
echo "Installation:"
echo "  1. Extract archive to Sam Sampler assets directory"
echo "  2. Load SF2 via Sam Sampler instrument loader"
echo "  3. Enable sustain pedal (CC64) for proper behavior"
