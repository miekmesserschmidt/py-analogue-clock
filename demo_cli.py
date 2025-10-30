#!/usr/bin/env python3
"""Demo script showing CLI usage examples."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and display output."""
    print(f"\n{'=' * 60}")
    print(f"Example: {description}")
    print(f"Command: {cmd}")
    print("=" * 60)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("Messages:", result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f"Exit code: {result.returncode}", file=sys.stderr)
    print()


def main():
    """Run CLI examples."""
    print("=== Analogue Clock CLI Demonstration ===\n")

    # Check if test_clock.svg exists
    if not Path("test_clock.svg").exists():
        print("Error: test_clock.svg not found in current directory")
        sys.exit(1)

    # Example 1: Help
    run_command("analogueclock --help", "Display help information")

    # Example 2: Current time to stdout
    run_command(
        "analogueclock test_clock.svg | head -20",
        "Generate clock with current time (showing first 20 lines)",
    )

    # Example 3: Specific time to file
    run_command(
        "analogueclock test_clock.svg --time 15:30:45 --output demo_clock_1.svg",
        "Generate clock showing 15:30:45 and save to demo_clock_1.svg",
    )

    # Example 4: Noon to file
    run_command(
        "analogueclock test_clock.svg -t 12:00:00 -o demo_clock_2.svg",
        "Generate clock showing noon (using short options)",
    )

    # Example 5: Morning time
    run_command(
        "analogueclock test_clock.svg -t 09:15:30 -o demo_clock_3.svg",
        "Generate clock showing 09:15:30",
    )

    run_command(
        "analogueclock test_transform_centers.svg -t 09:15:30 -o demo_clock_4.svg",
        "Generate clock showing 09:15:30",
    )

    print("=" * 60)
    print("Demo complete! Check the generated files:")
    print("  - demo_clock_1.svg (15:30:45)")
    print("  - demo_clock_2.svg (12:00:00)")
    print("  - demo_clock_3.svg (09:15:30)")
    print("  - demo_clock_4.svg (09:15:30)")
    print("=" * 60)


if __name__ == "__main__":
    main()
