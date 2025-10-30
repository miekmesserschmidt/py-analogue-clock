# Custom Transform Center CLI Feature

## Overview

Added `--center` / `-c` option to the CLI to allow users to specify a custom transform center for clock hands, overriding the automatic center detection.

## Changes Made

### 1. Updated main.py CLI

**Location**: `main.py`

#### New Parameter:

```python
center: Optional[str] = typer.Option(
    None,
    "--center",
    "-c",
    help="Custom transform center as 'x,y' (e.g., '150,150'). If not provided, center is auto-detected from SVG.",
    metavar="X,Y",
)
```

#### Implementation Details:

- Accepts center as a string in format "x,y" (e.g., "150,150")
- Parses and validates the format
- Converts to tuple of floats: `(x, y)`
- Passes to `AnalogueClock` constructor as `transform_center` parameter
- Provides helpful error messages for invalid formats

#### Error Handling:

```python
# Invalid format examples that raise errors:
--center 150           # Missing Y coordinate
--center 150,         # Missing Y value
--center abc,def      # Non-numeric values
--center "150 150"    # Wrong separator (space instead of comma)
```

Error message:

```
Error: Invalid center format - Center must be in format 'x,y'
Center must be in format 'x,y' (e.g., '150,150')
```

### 2. Updated Documentation

**Files Modified**:

- `README.md`: Updated Quick Start, CLI Options, and Examples sections
- `CLI_SUMMARY.md`: Added center option to features and examples
- `demo_cli.py`: Added example 6 demonstrating custom center usage

#### README Updates:

**Quick Start**:

```bash
# Custom transform center (for non-standard layouts)
python main.py test_clock.svg --time 15:30:45 --center 100,100 --output clock.svg
```

**CLI Options**:

- Added `--center` / `-c` description
- Explained auto-detection fallback behavior

**Examples**:

```bash
# Use custom transform center for non-standard clock layouts
python main.py custom_clock.svg -t 15:30:00 -c 100,100 -o output.svg
```

## Use Cases

### 1. Off-Center Clock Faces

When the clock face is not centered in the SVG canvas:

```bash
# SVG is 300x300 but clock face centered at (100, 100)
python main.py clock.svg -t 12:00:00 -c 100,100 -o output.svg
```

### 2. Multiple Clock Faces

For SVGs with multiple clocks, specify center for each:

```bash
# Top-left clock centered at (75, 75)
python main.py multi_clock.svg -t 12:00:00 -c 75,75 -o output.svg
```

### 3. Non-Standard Viewports

When viewBox doesn't match the actual clock center:

```bash
# viewBox="0 0 400 400" but clock centered at (150, 150)
python main.py clock.svg -t 15:30:00 -c 150,150 -o output.svg
```

### 4. Auto-Detection Override

When automatic detection gets it wrong:

```bash
# Override auto-detected center with correct value
python main.py clock.svg -t 09:00:00 -c 200,200 -o output.svg
```

## Behavior

### Without `--center`:

- Center is auto-detected from SVG's `viewBox` attribute
- Falls back to `width`/`height` attributes if no viewBox
- Uses calculated geometric center

### With `--center`:

- Uses provided coordinates exactly
- Bypasses auto-detection completely
- User has full control over rotation pivot point

### Status Messages:

When custom center is used, CLI prints confirmation:

```
Using custom transform center: (100.0, 100.0)
```

## Examples

### Basic Usage:

```bash
# Specify center as X,Y coordinates
python main.py clock.svg -t 12:00:00 -c 150,150
```

### With All Options:

```bash
# Complete example with all options
python main.py clock.svg -t 15:30:45 -c 100,100 -o output.svg
```

### Short Option:

```bash
# Using short form -c
python main.py clock.svg -t 12:00 -c 200,200 -o noon.svg
```

## Testing

### Valid Formats:

```bash
python main.py clock.svg -c 150,150      # ✅ Integers
python main.py clock.svg -c 150.5,150.5  # ✅ Floats
python main.py clock.svg -c "100, 100"   # ✅ With spaces
```

### Invalid Formats:

```bash
python main.py clock.svg -c 150          # ❌ Missing Y
python main.py clock.svg -c 150,         # ❌ Empty Y
python main.py clock.svg -c abc,def      # ❌ Non-numeric
python main.py clock.svg -c "150 150"    # ❌ Wrong separator
```

## Integration with Library

The CLI option directly maps to the library's `transform_center` parameter:

**CLI**:

```bash
python main.py clock.svg -c 100,100
```

**Library equivalent**:

```python
clock = AnalogueClock(svg=svg_content, transform_center=(100.0, 100.0))
```

## Backwards Compatibility

- **No breaking changes**: `--center` is optional
- **Default behavior unchanged**: Auto-detection still works when not specified
- **Existing scripts work**: All previous CLI usage patterns remain valid
