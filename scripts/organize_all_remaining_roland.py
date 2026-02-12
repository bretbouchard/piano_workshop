#!/usr/bin/env python3
"""
Master script to organize all remaining Roland drum machines
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name: str) -> bool:
    """Run a single organization script"""
    print(f"\n{'='*70}")
    print(f"Running {script_name}...")
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
            timeout=60
        )

        print(result.stdout)
        if result.stderr:
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
    print("ORGANIZING ALL REMAINING ROLAND DRUM MACHINES")
    print("="*70)

    scripts_to_run = [
        "organize_606.py",
        "organize_707.py",
        "organize_505.py",
        "organize_626.py",
    ]

    results = {}

    for script in scripts_to_run:
        success = run_script(script)
        results[script] = success

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    for script, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{script:30} {status}")

    print("\n" + "="*70)
    print("All Roland machines organized!")
    print("="*70)
    print()
    print("Next steps:")
    print("1. Create SF2 files using Polyphone")
    print("2. See piano_workshop/CREATE_ALL_SF2.md for instructions")
    print()

    # Check if all succeeded
    if all(results.values()):
        print("✅ All scripts completed successfully!")
        return 0
    else:
        print("⚠️  Some scripts failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
