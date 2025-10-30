"""Tests for the AnalogueClock class."""

import pytest
import xml.etree.ElementTree as ET
from datetime import time

from analogue_clock import AnalogueClock


class TestAnalogueClock:
    """Test cases for AnalogueClock class."""

    def test_initialization_with_default_svg(self):
        """Test that clock initializes with default SVG template."""
        clock = AnalogueClock()
        assert clock.svg is not None
        assert clock.svg is not None  # Test backward compatibility alias
        assert "hour-hand" in clock.svg
        assert "minute-hand" in clock.svg
        assert "second-hand" in clock.svg

    def test_initialization_with_custom_svg(self):
        """Test that clock initializes with custom SVG."""
        custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
            <line id="hour-hand" x1="0" y1="0" x2="0" y2="100"/>
            <line id="minute-hand" x1="0" y1="0" x2="0" y2="100"/>
            <line id="second-hand" x1="0" y1="0" x2="0" y2="100"/>
        </svg>"""
        clock = AnalogueClock(svg=custom_svg)
        assert clock.svg == custom_svg
        assert clock.svg == custom_svg  # Test backward compatibility alias

    def test_calculate_angles_midnight(self):
        """Test angle calculation for midnight (12:00:00)."""
        clock = AnalogueClock()
        hour_angle, minute_angle, second_angle = clock._calculate_angles(time(0, 0, 0))
        assert hour_angle == 0
        assert minute_angle == 0
        assert second_angle == 0

    def test_calculate_angles_three_oclock(self):
        """Test angle calculation for 3:00:00."""
        clock = AnalogueClock()
        hour_angle, minute_angle, second_angle = clock._calculate_angles(time(3, 0, 0))
        assert hour_angle == 90  # 3 * 30
        assert minute_angle == 0
        assert second_angle == 0

    def test_calculate_angles_six_thirty(self):
        """Test angle calculation for 6:30:00."""
        clock = AnalogueClock()
        hour_angle, minute_angle, second_angle = clock._calculate_angles(time(6, 30, 0))
        assert hour_angle == 195  # 6 * 30 + 30 * 0.5
        assert minute_angle == 180  # 30 * 6
        assert second_angle == 0

    def test_calculate_angles_with_seconds(self):
        """Test angle calculation with seconds component."""
        clock = AnalogueClock()
        hour_angle, minute_angle, second_angle = clock._calculate_angles(
            time(3, 15, 30)
        )
        assert hour_angle == 97.5  # 3 * 30 + 15 * 0.5
        assert minute_angle == 93  # 15 * 6 + 30 * 0.1
        assert second_angle == 180  # 30 * 6

    def test_calculate_angles_twelve_hour_wrap(self):
        """Test that hours wrap correctly (15:00 = 3:00)."""
        clock = AnalogueClock()
        hour_angle_am, _, _ = clock._calculate_angles(time(3, 0, 0))
        hour_angle_pm, _, _ = clock._calculate_angles(time(15, 0, 0))
        assert hour_angle_am == hour_angle_pm

    def test_generate_with_time_object(self):
        """Test SVG generation with time object."""
        clock = AnalogueClock()
        svg = clock.generate(time(3, 15, 30))

        # Verify it's valid XML
        root = ET.fromstring(svg)
        assert root is not None

        # Check that hands have transforms applied
        assert "rotate(97.5deg)" in svg  # hour hand
        assert "rotate(93" in svg  # minute hand (allowing for floating point)
        assert "rotate(180deg)" in svg  # second hand

    def test_generate_with_string_hhmmss(self):
        """Test SVG generation with HH:MM:SS string."""
        clock = AnalogueClock()
        svg = clock.generate("03:15:30")

        # Verify it's valid XML
        root = ET.fromstring(svg)
        assert root is not None

        # Check that hands have transforms applied
        assert "rotate(97.5deg)" in svg

    def test_generate_with_string_hhmm(self):
        """Test SVG generation with HH:MM string (no seconds)."""
        clock = AnalogueClock()
        svg = clock.generate("03:15")

        # Verify it's valid XML
        root = ET.fromstring(svg)
        assert root is not None

        # Check hour hand angle (should be 3*30 + 15*0.5 = 97.5)
        assert "rotate(97.5deg)" in svg

    def test_find_element_by_id(self):
        """Test finding elements by ID in SVG."""
        clock = AnalogueClock()
        root = ET.fromstring(clock.svg)

        hour_hand = clock._find_element_by_id(root, "hour-hand")
        assert hour_hand is not None
        assert hour_hand.get("id") == "hour-hand"

        minute_hand = clock._find_element_by_id(root, "minute-hand")
        assert minute_hand is not None
        assert minute_hand.get("id") == "minute-hand"

        second_hand = clock._find_element_by_id(root, "second-hand")
        assert second_hand is not None
        assert second_hand.get("id") == "second-hand"

    def test_find_element_by_id_not_found(self):
        """Test that finding non-existent ID returns None."""
        clock = AnalogueClock()
        root = ET.fromstring(clock.svg)

        element = clock._find_element_by_id(root, "nonexistent-id")
        assert element is None

    def test_set_transform(self):
        """Test setting transform on an element."""
        clock = AnalogueClock()
        element = ET.Element("line")

        clock._set_transform(element, 45.5)

        style = element.get("style")
        assert style is not None
        assert "transform: rotate(45.5deg)" in style
        assert "transform-origin" in style

    def test_apply_transforms(self):
        """Test applying transforms to all hands."""
        clock = AnalogueClock()
        svg = clock._apply_transforms(clock.svg, 90, 180, 270)

        assert "rotate(90deg)" in svg
        assert "rotate(180deg)" in svg
        assert "rotate(270deg)" in svg

    def test_output_is_valid_svg(self):
        """Test that generated output is valid SVG."""
        clock = AnalogueClock()
        svg = clock.generate(time(12, 30, 45))

        # Parse to verify it's valid XML/SVG
        root = ET.fromstring(svg)
        assert root.tag.endswith("svg")

    def test_default_svg_structure(self):
        """Test that default SVG has required structure."""
        clock = AnalogueClock()
        root = ET.fromstring(clock.svg)

        # Check for required IDs
        ids = {elem.get("id") for elem in root.iter() if elem.get("id")}
        assert "hour-hand" in ids
        assert "minute-hand" in ids
        assert "second-hand" in ids

    def test_multiple_generations(self):
        """Test that clock can generate multiple different times."""
        clock = AnalogueClock()

        svg1 = clock.generate(time(3, 0, 0))
        svg2 = clock.generate(time(6, 0, 0))
        svg3 = clock.generate(time(9, 0, 0))

        # Each should be different
        assert svg1 != svg2
        assert svg2 != svg3
        assert svg1 != svg3

        # But all should be valid
        ET.fromstring(svg1)
        ET.fromstring(svg2)
        ET.fromstring(svg3)

    def test_edge_case_noon(self):
        """Test noon (12:00:00)."""
        clock = AnalogueClock()
        hour_angle, minute_angle, second_angle = clock._calculate_angles(time(12, 0, 0))
        assert hour_angle == 0  # 12 % 12 = 0
        assert minute_angle == 0
        assert second_angle == 0

    def test_edge_case_almost_midnight(self):
        """Test 23:59:59."""
        clock = AnalogueClock()
        hour_angle, minute_angle, second_angle = clock._calculate_angles(
            time(23, 59, 59)
        )
        assert hour_angle == pytest.approx(359.5, rel=0.1)  # Almost full circle
        assert minute_angle == pytest.approx(359.9, rel=0.1)
        assert second_angle == 354  # 59 * 6

    def test_custom_svg_with_missing_hands(self):
        """Test with custom SVG that's missing some hands."""
        custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <line id="hour-hand" x1="0" y1="0" x2="0" y2="100"/>
        </svg>"""
        clock = AnalogueClock(svg=custom_svg)

        # Should not raise an error
        svg = clock.generate(time(3, 15, 30))
        assert svg is not None
        assert "rotate(97.5deg)" in svg

    def test_svg_center_from_viewbox(self):
        """Test that SVG center is correctly extracted from viewBox."""
        custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
            <line id="hour-hand" x1="200" y1="200" x2="200" y2="100"/>
            <line id="minute-hand" x1="200" y1="200" x2="200" y2="80"/>
            <line id="second-hand" x1="200" y1="200" x2="200" y2="60"/>
        </svg>"""
        clock = AnalogueClock(svg=custom_svg)

        # viewBox is "0 0 400 400", so center should be (200, 200)
        assert clock.transform_center == (200.0, 200.0)

    def test_svg_center_from_width_height(self):
        """Test that SVG center is extracted from width/height attributes."""
        custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500">
            <line id="hour-hand" x1="250" y1="250" x2="250" y2="150"/>
            <line id="minute-hand" x1="250" y1="250" x2="250" y2="130"/>
            <line id="second-hand" x1="250" y1="250" x2="250" y2="110"/>
        </svg>"""
        clock = AnalogueClock(svg=custom_svg)

        # width=500, height=500, so center should be (250, 250)
        assert clock.transform_center == (250.0, 250.0)

    def test_svg_center_with_units(self):
        """Test that SVG center handles width/height with units (px)."""
        custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="600px" height="600px">
            <line id="hour-hand" x1="300" y1="300" x2="300" y2="200"/>
        </svg>"""
        clock = AnalogueClock(svg=custom_svg)

        # Should strip 'px' and calculate center
        assert clock.transform_center == (300.0, 300.0)

    def test_custom_transform_center(self):
        """Test that custom transform_center can be provided."""
        custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
            <line id="hour-hand" x1="100" y1="100" x2="100" y2="50"/>
            <line id="minute-hand" x1="100" y1="100" x2="100" y2="40"/>
            <line id="second-hand" x1="100" y1="100" x2="100" y2="30"/>
        </svg>"""
        # Override with custom center point
        clock = AnalogueClock(svg=custom_svg, transform_center=(100.0, 100.0))

        assert clock.transform_center == (100.0, 100.0)

        # Generate and check the transform uses the custom center
        svg = clock.generate(time(3, 0, 0))
        assert "transform-origin: 100.0px 100.0px" in svg

    def test_transform_center_in_generated_svg(self):
        """Test that generated SVG uses the correct transform center."""
        custom_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
            <line id="hour-hand" x1="100" y1="100" x2="100" y2="50"/>
        </svg>"""
        clock = AnalogueClock(svg=custom_svg)

        svg = clock.generate(time(12, 0, 0))

        # Should use center (100, 100) derived from viewBox
        assert "transform-origin: 100.0px 100.0px" in svg

    def test_default_svg_has_correct_center(self):
        """Test that default SVG calculates correct center."""
        clock = AnalogueClock()

        # Default SVG has viewBox="0 0 300 300", so center is (150, 150)
        assert clock.transform_center == (150.0, 150.0)

    def test_dataclass_immutability(self):
        """Test that AnalogueClock works as a dataclass."""
        svg1 = """<svg viewBox="0 0 300 300"><line id="hour-hand"/></svg>"""
        svg2 = """<svg viewBox="0 0 400 400"><line id="hour-hand"/></svg>"""

        clock1 = AnalogueClock(svg=svg1)
        clock2 = AnalogueClock(svg=svg2)

        # Each instance should have its own values
        assert clock1.svg != clock2.svg
        assert clock1.transform_center != clock2.transform_center
