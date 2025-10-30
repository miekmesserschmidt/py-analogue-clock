"""Example usage of the analogue clock library."""

from datetime import time
from analogue_clock import AnalogueClock


def main():
    """Demonstrate clock generation."""
    # Create a clock instance
    clock = AnalogueClock()

    # Generate SVG for different times
    print("Generating clock for 3:15:30...")
    svg = clock.generate(time(3, 15, 30))

    # Save to file
    with open("clock_3_15_30.svg", "w") as f:
        f.write(svg)
    print("Saved to clock_3_15_30.svg")

    # Generate using string format
    print("\nGenerating clock for 12:00:00...")
    svg = clock.generate("12:00:00")
    with open("clock_12_00_00.svg", "w") as f:
        f.write(svg)
    print("Saved to clock_12_00_00.svg")

    # Generate current time example
    print("\nGenerating clock for 6:30:45...")
    svg = clock.generate("06:30:45")
    with open("clock_6_30_45.svg", "w") as f:
        f.write(svg)
    print("Saved to clock_6_30_45.svg")


if __name__ == "__main__":
    main()
