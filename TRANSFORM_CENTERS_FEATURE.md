# Transform Centers Feature

## Overview

The AnalogueClock library now supports reading transform centers directly from SVG elements, allowing each clock hand to rotate around different pivot points for creative clock designs.

## Feature Summary

### Transform Center IDs

The library recognizes these special element IDs in your SVG:

| ID                        | Purpose                         | Priority |
| ------------------------- | ------------------------------- | -------- |
| `transform-center`        | General center for all hands    | Low      |
| `transform-center-hour`   | Specific center for hour hand   | High     |
| `transform-center-minute` | Specific center for minute hand | High     |
| `transform-center-second` | Specific center for second hand | High     |

**Priority Rule**: Hand-specific centers (`transform-center-hour`, etc.) override the general `transform-center`.

### Supported Attributes

Transform center elements can use:

- **`cx`/`cy`** attributes (e.g., circles: `<circle id="transform-center" cx="150" cy="150" r="5"/>`)
- **`x`/`y`** attributes (e.g., rectangles: `<rect id="transform-center" x="150" y="150" width="10" height="10"/>`)

## Implementation Details

### Code Changes

1. **New Method**: `_extract_transform_centers()`

   - Called during `__post_init__`
   - Parses SVG to find transform center elements
   - Stores centers in `_transform_centers` dictionary

2. **Updated Method**: `_set_transform(element, angle, hand_type)`

   - Added `hand_type` parameter
   - Checks for hand-specific centers first
   - Falls back to general `transform_center` if no specific center found

3. **Updated Calls**: All `_set_transform()` calls now include hand type
   - `_set_transform(hour_hand, hour_angle, "hour")`
   - `_set_transform(minute_hand, minute_angle, "minute")`
   - `_set_transform(second_hand, second_angle, "second")`

### Fallback Priority

1. Hand-specific SVG element (`transform-center-hour`, etc.) ← **Highest priority**
2. General SVG element (`transform-center`)
3. Programmatic parameter (`transform_center=(x, y)`)
4. SVG geometric center (from viewBox or width/height) ← **Default fallback**

## Usage Examples

### Example 1: General Transform Center

```python
svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
    <circle id="transform-center" cx="150" cy="150" r="5"/>
    <line id="hour-hand" x1="150" y1="150" x2="150" y2="80"/>
    <line id="minute-hand" x1="150" y1="150" x2="150" y2="50"/>
    <line id="second-hand" x1="150" y1="150" x2="150" y2="40"/>
</svg>"""

clock = AnalogueClock(svg=svg)
# All hands rotate around (150, 150)
```

### Example 2: Hand-Specific Override

```python
svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
    <circle id="transform-center" cx="150" cy="150" r="5"/>
    <circle id="transform-center-second" cx="150" cy="180" r="5"/>
    <line id="hour-hand" x1="150" y1="150" x2="150" y2="80"/>
    <line id="minute-hand" x1="150" y1="150" x2="150" y2="50"/>
    <line id="second-hand" x1="150" y1="180" x2="150" y2="40"/>
</svg>"""

clock = AnalogueClock(svg=svg)
# Hour and minute hands: (150, 150)
# Second hand: (150, 180)
```

### Example 3: All Individual Centers

```python
svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
    <circle id="transform-center-hour" cx="150" cy="150" r="5"/>
    <circle id="transform-center-minute" cx="160" cy="160" r="5"/>
    <circle id="transform-center-second" cx="140" cy="140" r="5"/>
    <line id="hour-hand" x1="150" y1="150" x2="150" y2="80"/>
    <line id="minute-hand" x1="160" y1="160" x2="160" y2="80"/>
    <line id="second-hand" x1="140" y1="140" x2="140" y2="80"/>
</svg>"""

clock = AnalogueClock(svg=svg)
# Each hand rotates around its own center
```

## Testing

New test class `TestTransformCenters` with 6 comprehensive tests:

1. ✅ `test_general_transform_center` - General center applies to all hands
2. ✅ `test_hand_specific_transform_center` - Specific centers override general
3. ✅ `test_all_hand_specific_centers` - Each hand can have unique center
4. ✅ `test_transform_center_with_x_y_attributes` - Supports x/y attributes
5. ✅ `test_no_transform_center_uses_svg_center` - Falls back to SVG center
6. ✅ `test_transform_applied_with_hand_specific_center` - Verifies CSS output

All 41 tests passing ✓

## Demo Script

Run `demo_transform_centers.py` to see examples:

```bash
python demo_transform_centers.py
```

Generates three example SVGs:

- `output_general_center.svg` - All hands use general center
- `output_specific_center.svg` - Second hand uses different center
- `output_all_centers.svg` - Each hand has unique center

## Benefits

1. **Flexibility**: Create unique clock designs with offset hands
2. **No Code Changes**: Define centers directly in SVG markup
3. **Backward Compatible**: Existing code works unchanged
4. **Intuitive**: Hand-specific centers naturally override general center
5. **Fallback Safe**: Multiple fallback layers ensure always-working transforms

## Files Modified

- `analogue_clock/clock.py` - Core implementation
- `tests/test_clock.py` - Added TestTransformCenters class
- `README.md` - Comprehensive documentation
- `demo_transform_centers.py` - Usage examples
- `test_transform_centers.svg` - Example SVG with centers

## Breaking Changes

None. The feature is fully backward compatible. Existing code continues to work without modification.
