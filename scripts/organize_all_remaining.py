#!/usr/bin/env python3
"""
MASTER ORGANIZER - ALL Remaining Drum Collections
Runs all remaining organizers in one go
"""

import subprocess
import sys
from pathlib import Path

def run_organizer(script_name: str, display_name: str) -> bool:
    """Run a single organizer script"""
    print(f"\n{'='*70}")
    print(f"RUNNING: {display_name}")
    print(f"{'='*70}\n")

    script_path = Path(f"scripts/{script_name}")
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max per script
        )

        print(result.stdout)
        if result.stderr and "error" in result.stderr.lower():
            print("STDERR:", result.stderr)

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"❌ Script {script_name} timed out")
        return False
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("🥁 MASTER DRUM ORGANIZER - ALL REMAINING COLLECTIONS")
    print("="*70)
    print("\nThis will organize ALL remaining drum machine collections:")
    print("  • Modern Digital (2 kits)")
    print("  • Mars Collections (7 kits)")
    print("  • Synth/Electronic (3 kits)")
    print("  • Vintage/Custom (2 kits)")
    print(f"\nTotal: 14 additional collections (~2,400 samples)")
    print("\nEstimated time: 5-10 minutes")

    # Ask for confirmation
    response = input("\nProceed? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return 0

    organizers = [
        ("organize_modern_digital.py", "Modern Digital (Vermona DRM-1, Alesis SR-16)"),
        ("organize_mars_collections.py", "Mars Collections (7 kits)"),
        ("organize_synthetic_drums.py", "Synth/Electronic (3 kits)"),
        ("organize_vintage_custom.py", "Vintage/Custom (2 kits)"),
    ]

    results = {}

    for script, name in organizers:
        success = run_organizer(script, name)
        results[name] = success

    # Summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)

    for name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{name:50} {status}")

    # Count total collections
    total_org = 7 + sum(1 for s in results.values() if s)  # 7 Roland + successful
    print(f"\n🎉 TOTAL DRUM COLLECTIONS ORGANIZED: {total_org}/22")

    print("\n" + "="*70)
    print("ALL ORGANIZATION COMPLETE!")
    print("="*70)
    print("\n📁 Location: piano_workshop/build/drum_kits/")
    print("\n🚀 Next steps:")
    print("1. Open Polyphone")
    print("2. Import SFZ files")
    print("3. Export as SF2")
    print("4. See CURRENT_STATUS.md for details")
    print()

    if all(results.values()):
        print("✅ ALL SCRIPTS COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print("⚠️  Some scripts had issues. Check output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
