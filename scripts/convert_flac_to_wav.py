#!/usr/bin/env python3
"""
Convert Salamander Grand Piano FLAC samples to WAV
Phase 1, Step 1: Audio format conversion

Converts 48kHz/24-bit FLAC to 16-bit/44.1kHz WAV for SF2 compatibility.
"""

import os
import sys
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
SCRIPT_DIR = Path(__file__).parent
WORKSHOP_ROOT = SCRIPT_DIR.parent
SOURCE_DIR = WORKSHOP_ROOT / "src/SalamanderGrandPiano/Samples"
BUILD_DIR = WORKSHOP_ROOT / "build/salamander_wav/Samples"

# Conversion settings
TARGET_SAMPLE_RATE = 44100
TARGET_BIT_DEPTH = 16
TARGET_CHANNELS = 1
MAX_WORKERS = 8  # Parallel conversions


def convert_file(flac_path: Path, wav_path: Path) -> tuple[bool, str]:
    """
    Convert a single FLAC file to WAV using ffmpeg.

    Returns:
        (success: bool, message: str)
    """
    try:
        # Create output directory
        wav_path.parent.mkdir(parents=True, exist_ok=True)

        # Build ffmpeg command
        cmd = [
            "ffmpeg",
            "-i", str(flac_path),  # Input file
            "-ar", str(TARGET_SAMPLE_RATE),  # Sample rate
            "-ac", str(TARGET_CHANNELS),  # Channels
            "-sample_fmt", "s16",  # 16-bit PCM
            "-y",  # Overwrite output
            str(wav_path)
        ]

        # Run ffmpeg, suppress output
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30
        )

        if result.returncode == 0:
            return True, f"✓ {flac_path.name}"
        else:
            return False, f"✗ {flac_path.name}: ffmpeg error"

    except subprocess.TimeoutExpired:
        return False, f"✗ {flac_path.name}: timeout"
    except Exception as e:
        return False, f"✗ {flac_path.name}: {e}"


def main():
    """Main conversion workflow"""
    print("=" * 60)
    print("Salamander Grand Piano FLAC → WAV Converter")
    print("=" * 60)
    print()

    # Verify source directory
    if not SOURCE_DIR.exists():
        print(f"✗ ERROR: Source directory not found: {SOURCE_DIR}")
        print("  Ensure Salamander Grand Piano is cloned correctly")
        sys.exit(1)

    # Find all FLAC files
    flac_files = list(SOURCE_DIR.rglob("*.flac"))

    if not flac_files:
        print(f"✗ ERROR: No FLAC files found in {SOURCE_DIR}")
        sys.exit(1)

    print(f"Source: {SOURCE_DIR}")
    print(f"Build:  {BUILD_DIR}")
    print(f"Found: {len(flac_files)} FLAC files")
    print(f"Target: {TARGET_SAMPLE_RATE}Hz, {TARGET_BIT_DEPTH}-bit, {TARGET_CHANNELS}ch")
    print()

    # Create build directory
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # Track progress
    success_count = 0
    fail_count = 0
    total = len(flac_files)

    print("Converting...")
    print()

    # Convert in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all conversion jobs
        futures = {}
        for flac_path in flac_files:
            # Calculate output path
            rel_path = flac_path.relative_to(SOURCE_DIR)
            wav_path = BUILD_DIR / rel_path.with_suffix(".wav")

            # Submit job
            future = executor.submit(convert_file, flac_path, wav_path)
            futures[future] = flac_path

        # Process results
        for i, future in enumerate(as_completed(futures), 1):
            success, message = future.result()

            if success:
                success_count += 1
            else:
                fail_count += 1
                print(message)

            # Progress update every 50 files
            if i % 50 == 0:
                print(f"Progress: {i}/{total} files processed...")

    print()
    print("=" * 60)
    print("Conversion Complete!")
    print("=" * 60)
    print(f"Successfully converted: {success_count} files")
    print(f"Failed:                {fail_count} files")
    print(f"Output directory:      {BUILD_DIR}")
    print()

    if fail_count > 0:
        print("⚠ Some files failed to convert")
        sys.exit(1)
    else:
        print("✓ All files converted successfully!")
        print()
        print("Next step: python3 ../scripts/02_create_modified_sfz.py")


if __name__ == "__main__":
    main()
