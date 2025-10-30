# py-analogue-clock

A Python library for generating SVG analogue clock faces displaying specified times.

## Features

- 🕐 Generate analogue clock SVGs for any time
- 🎨 Use the default elegant clock face or provide your own custom SVG
- ⚡ Fast and lightweight - uses only standard library XML parsing
- 🎯 Precise angle calculations for hour, minute, and second hands
- 🔄 Automatic SVG center detection from viewBox or width/height attributes
- 🎛️ Optional custom transform center for non-standard layouts
- ✅ SVG validation ensures required hand elements are present
- 📐 Dataclass-based API for clean, immutable clock instances
- 💻 Command-line interface for easy SVG generation
- ✅ Fully tested with comprehensive pytest suite
- 📦 Simple, clean API

## Installation

```bash
pip install py-analogue-clock
```

For development:

```bash
git clone <repository-url>
cd py-analogue-clock
pip install -e ".[dev]"
```

## Quick Start

### Command-Line Interface

Generate a clock SVG from the command line:

```bash
# Show current time (output to stdout)
python main.py test_clock.svg

# Show specific time
python main.py test_clock.svg --time 15:30:45

# Save to file
python main.py test_clock.svg --time 12:00:00 --output clock_noon.svg

# Get help
python main.py --help
```

### Python Library

```python
from datetime import time
from analogue_clock import AnalogueClock

# Create a clock instance
clock = AnalogueClock()

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
from analogue_clock import AnalogueClock

clock = AnalogueClock()

# Generate clock for 3:15:30 PM
svg = clock.generate(time(15, 15, 30))
```

### Using time strings

```python
from analogue_clock import AnalogueClock

clock = AnalogueClock()

# HH:MM:SS format
svg = clock.generate("14:30:45")

# HH:MM format (seconds default to 0)
svg = clock.generate("09:15")
```

### Using custom SVG templates

You can provide your own SVG template as long as it contains elements with the IDs `hour-hand`, `minute-hand`, and `second-hand`:

```python
from analogue_clock import AnalogueClock

custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="90" fill="white" stroke="black"/>
  <line id="hour-hand" x1="100" y1="100" x2="100" y2="50" stroke="black" stroke-width="4"/>
  <line id="minute-hand" x1="100" y1="100" x2="100" y2="30" stroke="blue" stroke-width="2"/>
  <line id="second-hand" x1="100" y1="100" x2="100" y2="20" stroke="red" stroke-width="1"/>
</svg>"""

clock = AnalogueClock(svg=custom_svg)
svg = clock.generate("12:30:00")
```

**Important**: The SVG **must** contain elements with IDs `hour-hand`, `minute-hand`, and `second-hand`. If any are missing, a `ValueError` will be raised during initialization:

```python
# This will raise ValueError: SVG is missing required elements
invalid_svg = """<svg viewBox="0 0 200 200">
  <line id="hour-hand" x1="100" y1="100" x2="100" y2="50"/>
  <!-- Missing minute-hand! -->
</svg>"""

clock = AnalogueClock(svg=invalid_svg)  # Raises ValueError
```

The library automatically detects the SVG center from the `viewBox` attribute (preferred) or `width`/`height` attributes. For a `viewBox="0 0 200 200"`, the center is automatically calculated as (100, 100).

### Custom Transform Center

If your clock hands don't rotate around the geometric center of the SVG, you can specify a custom transform center:

```python
from analogue_clock import AnalogueClock

custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <circle id="transform-center" cx="100" cy="100" r="90" fill="white" stroke="black"/>
  <line id="hour-hand" x1="100" y1="100" x2="100" y2="50"/>
  <line id="minute-hand" x1="100" y1="100" x2="100" y2="30"/>
  <line id="second-hand" x1="100" y1="100" x2="100" y2="20"/>
</svg>"""

# Hands rotate around (100, 100) instead of SVG center (150, 150)
clock = AnalogueClock(svg=custom_svg, transform_center=(100.0, 100.0))
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
from analogue_clock import AnalogueClock

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <!-- Define transform center with a circle -->
  <circle id="transform-center" cx="150" cy="150" r="5"/>

  <!-- All hands will rotate around (150, 150) -->
  <line id="hour-hand" x1="150" y1="150" x2="150" y2="80"/>
  <line id="minute-hand" x1="150" y1="150" x2="150" y2="50"/>
  <line id="second-hand" x1="150" y1="150" x2="150" y2="40"/>
</svg>"""

clock = AnalogueClock(svg=svg)
# No need to specify transform_center - it's read from the SVG!
```

#### Example: Hand-Specific Centers

```python
from analogue_clock import AnalogueClock

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

clock = AnalogueClock(svg=svg)
svg_result = clock.generate("15:30:45")
# Hour and minute hands rotate around (150, 150)
# Second hand rotates around (150, 180)
```

#### Example: Individual Centers for Each Hand

```python
from analogue_clock import AnalogueClock

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <!-- Each hand has its own pivot point -->
  <circle id="transform-center-hour" cx="150" cy="150" r="5"/>
  <circle id="transform-center-minute" cx="160" cy="160" r="5"/>
  <circle id="transform-center-second" cx="140" cy="140" r="5"/>

  <line id="hour-hand" x1="150" y1="150" x2="150" y2="80"/>
  <line id="minute-hand" x1="160" y1="160" x2="160" y2="80"/>
  <line id="second-hand" x1="140" y1="140" x2="140" y2="80"/>
</svg>"""

clock = AnalogueClock(svg=svg)
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
python main.py my_clock.svg

# Display specific time
python main.py my_clock.svg --time 15:30:45

# Save to file
python main.py my_clock.svg --time 12:00:00 --output clock_noon.svg
```

### CLI Options

- **`svg_file`** (required): Path to the input SVG file containing elements with IDs `hour-hand`, `minute-hand`, and `second-hand`
- **`--time` / `-t`**: Time to display in `HH:MM:SS` format. If omitted, uses current system time
- **`--output` / `-o`**: Output file path. If omitted, prints the SVG to stdout

### Examples

```bash
# Generate clock showing current time, save to file
python main.py test_clock.svg -o current_time.svg

# Generate multiple times
python main.py test_clock.svg -t 09:15:00 -o morning.svg
python main.py test_clock.svg -t 14:30:00 -o afternoon.svg
python main.py test_clock.svg -t 21:45:00 -o evening.svg

# Pipe to other tools
python main.py test_clock.svg -t 12:00:00 | some-svg-processor
````

### CLI Options

- **`svg_file`** (required): Path to the input SVG file containing elements with IDs `hour-hand`, `minute-hand`, and `second-hand`
- **`--time` / `-t`**: Time to display in `HH:MM:SS` format. If omitted, uses current system time
- **`--output` / `-o`**: Output file path. If omitted, prints the SVG to stdout

### Examples

```bash
# Generate clock showing current time, save to file
python main.py test_clock.svg -o current_time.svg

# Generate multiple times
python main.py test_clock.svg -t 09:15:00 -o morning.svg
python main.py test_clock.svg -t 14:30:00 -o afternoon.svg
python main.py test_clock.svg -t 21:45:00 -o evening.svg

# Pipe to other tools
python main.py test_clock.svg -t 12:00:00 | some-svg-processor

# View help
python main.py --help
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

### Angle Calculations

```python
# Example: 3:15:30
hour_angle = 3 * 30 + 15 * 0.5 = 97.5°
minute_angle = 15 * 6 + 30 * 0.1 = 93°
second_angle = 30 * 6 = 180°
```

### SVG Center Detection

The library automatically extracts the center point:

1. **From viewBox**: `viewBox="0 0 300 300"` → center is (150, 150)
2. **From width/height**: `width="400" height="400"` → center is (200, 200)
3. **Handles units**: `width="500px"` → strips units and uses 500
4. **Fallback**: If neither is available, defaults to (150, 150)

## API Reference

### `AnalogueClock`

`AnalogueClock` is a dataclass with the following attributes:

#### `svg: str`

The SVG template string containing elements with IDs `hour-hand`, `minute-hand`, and `second-hand`.
Defaults to a built-in clock face if not provided.

#### `transform_center: Optional[Tuple[float, float]]`

The (x, y) coordinates for the rotation center of clock hands.
If `None` (default), the center is automatically calculated from the SVG's `viewBox` or `width`/`height` attributes.

#### Creating an AnalogueClock

```python
# Using defaults
clock = AnalogueClock()

# With custom SVG
clock = AnalogueClock(svg=my_svg_string)

# With custom SVG and transform center
clock = AnalogueClock(svg=my_svg_string, transform_center=(100.0, 100.0))
```

#### `generate(clock_time: Union[time, str]) -> str`

Generate an SVG displaying the specified time.

- **Parameters:**
  - `clock_time` (Union[time, str]): Time to display. Can be a `datetime.time` object or string in "HH:MM:SS" or "HH:MM" format.
- **Returns:**
  - str: SVG content with clock hands positioned for the specified time.

#### `generate(clock_time: Union[time, str]) -> str`

Generate an SVG displaying the specified time.

- **Parameters:**
  - `clock_time` (Union[time, str]): Time to display. Can be a `datetime.time` object or string in "HH:MM:SS" or "HH:MM" format.
- **Returns:**

  - str: SVG content with clock hands positioned for the specified time.

- **Examples:**
  ```python
  svg = clock.generate(time(3, 15, 30))
  svg = clock.generate("14:30:45")
  svg = clock.generate("09:15")
  ```

## Default Clock Face

The library includes a beautiful default clock face with:

- Classic round design with 140px radius
- Hour markers at 12, 3, 6, and 9 o'clock
- Numbers at key positions
- Black hour and minute hands
- Red second hand
- Centered dot at the pivot point
- Clean, minimal styling

## Development

### Running Tests

```bash
pytest
```

### Running Tests with Coverage

```bash
pytest --cov=analogue_clock --cov-report=html
```

### Project Structure

```
py-analogue-clock/
├── analogue_clock/
│   ├── __init__.py
│   └── clock.py          # Main clock implementation
├── tests/
│   ├── __init__.py
│   └── test_clock.py     # Comprehensive test suite
├── main.py               # Example usage
├── pyproject.toml        # Project configuration
└── README.md
```

## Requirements

- Python >= 3.8
- svgwrite >= 1.4.3 (installed automatically)
- pytest >= 8.3.5 (for development)

## Testing

The library includes a comprehensive test suite covering:

- ✅ Initialization with default and custom SVGs
- ✅ Angle calculations for all times
- ✅ 12-hour clock wrapping (15:00 = 3:00)
- ✅ String time parsing (HH:MM:SS and HH:MM)
- ✅ Edge cases (midnight, noon, 23:59:59)
- ✅ XML/SVG validity
- ✅ Transform application
- ✅ Multiple generations
- ✅ Missing hand elements

Run with: `pytest -v`

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Examples

Check out `main.py` for complete working examples:

```bash
python main.py
```

This will generate three example clock SVGs:

- `clock_3_15_30.svg` - 3:15:30
- `clock_12_00_00.svg` - 12:00:00
- `clock_6_30_45.svg` - 6:30:45
