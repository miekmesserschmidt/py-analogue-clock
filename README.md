# py-analogue-clock

A Python library for generating SVG analogue clock faces displaying specified times.

## Features

- 🕐 Generate analogue clock SVGs for any time
- 🎨 Use the default elegant clock face or provide your own custom SVG
- ⚡ Fast and lightweight - uses only standard library XML parsing
- 🎯 Precise angle calculations for hour, minute, and second hands
- 🔄 Automatic SVG center detection from viewBox or width/height attributes
- 🎛️ Optional custom transform center for non-standard layouts
- 📐 Dataclass-based API for clean, immutable clock instances
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

The library automatically detects the SVG center from the `viewBox` attribute (preferred) or `width`/`height` attributes. For a `viewBox="0 0 200 200"`, the center is automatically calculated as (100, 100).

### Custom Transform Center

If your clock hands don't rotate around the geometric center of the SVG, you can specify a custom transform center:

```python
from analogue_clock import AnalogueClock

custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <circle cx="100" cy="100" r="90" fill="white" stroke="black"/>
  <line id="hour-hand" x1="100" y1="100" x2="100" y2="50"/>
  <line id="minute-hand" x1="100" y1="100" x2="100" y2="30"/>
  <line id="second-hand" x1="100" y1="100" x2="100" y2="20"/>
</svg>"""

# Hands rotate around (100, 100) instead of SVG center (150, 150)
clock = AnalogueClock(svg=custom_svg, transform_center=(100.0, 100.0))
svg = clock.generate("12:30:00")
```

## How It Works

The library works by:

1. **Parsing** the SVG template and detecting its center point from the `viewBox` or `width`/`height` attributes
2. **Calculating** rotation angles for each hand based on the time:
   - Hour hand: 30° per hour + 0.5° per minute
   - Minute hand: 6° per minute + 0.1° per second
   - Second hand: 6° per second
3. **Applying** CSS transforms to rotate each hand around the clock center (or custom transform center)
4. **Returning** the modified SVG as a string

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
