# py-analogue-clock

A Python library and cli for generating SVG analogue clock faces displaying specified times.

## Features

- 🕐 Generate analogue clock SVGs for any time
- Use the default clock face or provide your own custom SVG
- Can be used as library, or cli

## Installation

```bash
uv add git+https://github.com/miekmesserschmidt/py-analogue-clock

```

## Quick Start

### Command-Line Interface

Generate a clock SVG from the command line:

```bash
# Get help
uv run analogueclock --help

# Show current time (output to stdout)
uv run analogueclock test_clock.svg

# Show specific time
uv run analogueclock test_clock.svg --time 15:30:45

# Save to file
uv run analogueclock test_clock.svg --time 12:00:00 --output clock_noon.svg

```

### Python Library

```python
from datetime import time
from analogue_clock import uv run AnalogueClock

# Create a clock instance
clock = uv run AnalogueClock()

# Generate SVG for a specific time
svg = clock.generate(time(3, 15, 30))

# Save to file
with open("clock.svg", "w") as f:
    f.write(svg)
```

## Usage

### Using datetime.time objects

```python
from datetime import time
from analogue_clock import uv run AnalogueClock

clock = uv run AnalogueClock()

# Generate clock for 3:15:30 PM
svg = clock.generate(time(15, 15, 30))
```

### Using time strings

```python
from analogue_clock import uv run AnalogueClock

clock = uv run AnalogueClock()

# HH:MM:SS format
svg = clock.generate("14:30:45")

# HH:MM format (seconds default to 0)
svg = clock.generate("09:15")
```

### Using custom SVG templates

You can provide your own SVG template as long as it contains elements with the IDs `hour-hand`, `minute-hand`, and `second-hand`:

```python
from analogue_clock import uv run AnalogueClock

custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="90" fill="white" stroke="black"/>
  <line id="hour-hand" x1="100" y1="100" x2="100" y2="50" stroke="black" stroke-width="4"/>
  <line id="minute-hand" x1="100" y1="100" x2="100" y2="30" stroke="blue" stroke-width="2"/>
  <line id="second-hand" x1="100" y1="100" x2="100" y2="20" stroke="red" stroke-width="1"/>
</svg>"""

clock = uv run AnalogueClock(svg=custom_svg)
svg = clock.generate("12:30:00")
```

**Important**: The SVG **must** contain elements with IDs `hour-hand`, `minute-hand`. The ID`second-hand` is optional. If any are missing, a `ValueError` will be raised during initialization:

```python
# This will raise ValueError: SVG is missing required elements
invalid_svg = """<svg viewBox="0 0 200 200">
  <line id="hour-hand" x1="100" y1="100" x2="100" y2="50"/>
  <!-- Missing minute-hand! -->
</svg>"""

clock = uv run AnalogueClock(svg=invalid_svg)  # Raises ValueError
```

The library automatically detects the SVG center from the `viewBox` attribute (preferred) or `width`/`height` attributes. For a `viewBox="0 0 200 200"`, the center is automatically calculated as (100, 100).

### Custom Transform Center

If your clock hands don't rotate around the geometric center of the SVG, you can specify a custom transform center:

```python
from analogue_clock import uv run AnalogueClock

custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <circle id="transform-center" cx="100" cy="100" r="90" fill="white" stroke="black"/>
  <line id="hour-hand" x1="100" y1="100" x2="100" y2="50"/>
  <line id="minute-hand" x1="100" y1="100" x2="100" y2="30"/>
  <line id="second-hand" x1="100" y1="100" x2="100" y2="20"/>
</svg>"""

# Hands rotate around (100, 100) instead of SVG center (150, 150)
clock = uv run AnalogueClock(svg=custom_svg, transform_center=(100.0, 100.0))
svg = clock.generate("12:30:00")
```

### Transform Centers from SVG Elements

The library can automatically read transform centers from special elements in your SVG. This allows different hands to rotate around different pivot points, enabling creative clock designs.

#### Available Transform Center IDs

You can add elements with these IDs to your SVG:

- **`transform-center`**: General center used for all hands (unless overridden)
- **`transform-center-hour`**: Specific center for hour hand only
- **`transform-center-minute`**: Specific center for minute hand only
- **`transform-center-second`**: Specific center for second hand only

Hand-specific centers always override the general `transform-center`.

#### Example: General Transform Center

```python
from analogue_clock import uv run AnalogueClock

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <!-- Define transform center with a circle -->
  <circle id="transform-center" cx="150" cy="150" r="5"/>

  <!-- All hands will rotate around (150, 150) -->
  <line id="hour-hand" x1="150" y1="150" x2="150" y2="80"/>
  <line id="minute-hand" x1="150" y1="150" x2="150" y2="50"/>
  <line id="second-hand" x1="150" y1="150" x2="150" y2="40"/>
</svg>"""

clock = uv run AnalogueClock(svg=svg)
# No need to specify transform_center - it's read from the SVG!
```

#### Example: Hand-Specific Centers

```python
from analogue_clock import uv run AnalogueClock

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <!-- General center for hour and minute hands -->
  <circle id="transform-center" cx="150" cy="150" r="5"/>

  <!-- Different center for second hand -->
  <circle id="transform-center-second" cx="150" cy="180" r="5"/>

  <line id="hour-hand" x1="150" y1="150" x2="150" y2="80"/>
  <line id="minute-hand" x1="150" y1="150" x2="150" y2="50"/>
  <!-- Second hand starts at (150, 180) and rotates around that point -->
  <line id="second-hand" x1="150" y1="180" x2="150" y2="40"/>
</svg>"""

clock = uv run AnalogueClock(svg=svg)
svg_result = clock.generate("15:30:45")
# Hour and minute hands rotate around (150, 150)
# Second hand rotates around (150, 180)
```

#### Example: Individual Centers for Each Hand

```python
from analogue_clock import uv run AnalogueClock

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <!-- Each hand has its own pivot point -->
  <circle id="transform-center-hour" cx="150" cy="150" r="5"/>
  <circle id="transform-center-minute" cx="160" cy="160" r="5"/>
  <circle id="transform-center-second" cx="140" cy="140" r="5"/>

  <line id="hour-hand" x1="150" y1="150" x2="150" y2="80"/>
  <line id="minute-hand" x1="160" y1="160" x2="160" y2="80"/>
  <line id="second-hand" x1="140" y1="140" x2="140" y2="80"/>
</svg>"""

clock = uv run AnalogueClock(svg=svg)
# Each hand rotates around its own unique center!
```

**Note**: Transform center elements can use either `cx`/`cy` attributes (circles) or `x`/`y` attributes (rectangles, etc.). The elements themselves can be visible or invisible in your design.

#### Fallback Behavior

The library uses this priority order for determining transform centers:

1. **Hand-specific center** (`transform-center-hour`, etc.) - highest priority
2. **General center** (`transform-center`) - if no hand-specific center exists
3. **Programmatic center** (`transform_center` parameter) - if no SVG centers defined
4. **SVG geometric center** - calculated from viewBox or width/height (default fallback)

````

## Command-Line Interface

The package includes a CLI tool for generating clock SVGs from the command line.

### Basic Usage

```bash
# Display current time (output to stdout)
uv run analogueclock my_clock.svg

# Display specific time
uv run analogueclock my_clock.svg --time 15:30:45

# Save to file
uv run analogueclock my_clock.svg --time 12:00:00 --output clock_noon.svg
```

### CLI Options

- **`svg_file`** (required): Path to the input SVG file containing elements with IDs `hour-hand`, `minute-hand`, and `second-hand`
- **`--time` / `-t`**: Time to display in `HH:MM:SS` format. If omitted, uses current system time
- **`--output` / `-o`**: Output file path. If omitted, prints the SVG to stdout

### Examples

```bash
# Generate clock showing current time, save to file
uv run analogueclock test_clock.svg -o current_time.svg

# Generate multiple times
uv run analogueclock test_clock.svg -t 09:15:00 -o morning.svg
uv run analogueclock test_clock.svg -t 14:30:00 -o afternoon.svg
uv run analogueclock test_clock.svg -t 21:45:00 -o evening.svg

# Pipe to other tools
uv run analogueclock test_clock.svg -t 12:00:00 | some-svg-processor
````

### CLI Options

- **`svg_file`** (required): Path to the input SVG file containing elements with IDs `hour-hand`, `minute-hand`, and `second-hand`
- **`--time` / `-t`**: Time to display in `HH:MM:SS` format. If omitted, uses current system time
- **`--output` / `-o`**: Output file path. If omitted, prints the SVG to stdout

### Examples

```bash
# Generate clock showing current time, save to file
uv run analogueclock test_clock.svg -o current_time.svg

# Generate multiple times
uv run analogueclock test_clock.svg -t 09:15:00 -o morning.svg
uv run analogueclock test_clock.svg -t 14:30:00 -o afternoon.svg
uv run analogueclock test_clock.svg -t 21:45:00 -o evening.svg

# Pipe to other tools
uv run analogueclock test_clock.svg -t 12:00:00 | some-svg-processor

# View help
uv run analogueclock --help
```

## How It Works

The library works by:

1. **Validating** the SVG contains required elements with IDs: `hour-hand`, `minute-hand`, and `second-hand`
2. **Parsing** the SVG template and detecting its center point from the `viewBox` or `width`/`height` attributes
3. **Calculating** rotation angles for each hand based on the time:
   - Hour hand: 30° per hour + 0.5° per minute
   - Minute hand: 6° per minute + 0.1° per second
   - Second hand: 6° per second
4. **Applying** CSS transforms to rotate each hand around the clock center (or custom transform center)
5. **Returning** the modified SVG as a string

### Running Tests

```bash
pytest
```

## Requirements

- Python >= 3.14
- svgwrite >= 1.4.3
- pytest >= 8.3.5 (for development)
