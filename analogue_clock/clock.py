"""Core clock functionality for generating analogue clock SVGs."""

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import time
from typing import Dict, Union, Tuple, Optional


@dataclass
class AnalogueClock:
    """Generate analogue clock SVG with specified time."""

    svg: str = field(default_factory=lambda: DEFAULT_CLOCK_SVG)

    transform_center: Optional[Tuple[float, float]] = None
    transform_center_second: Optional[Tuple[float, float]] = None
    transform_center_minute: Optional[Tuple[float, float]] = None
    transform_center_hour: Optional[Tuple[float, float]] = None

    def __post_init__(self):
        """Initialize derived attributes after dataclass initialization."""
        # Validate that required hand elements are present
        self._validate_svg()

        transform_center_elem = self._find_element_by_id(
            ET.fromstring(self.svg), "transform-center"
        )
        transform_center_seconds_elem = self._find_element_by_id(
            ET.fromstring(self.svg), "transform-center-second"
        )
        transform_center_minute_elem = self._find_element_by_id(
            ET.fromstring(self.svg), "transform-center-minute"
        )
        transform_center_hour_elem = self._find_element_by_id(
            ET.fromstring(self.svg), "transform-center-hour"
        )

        # If transform_center not provided, try to extract from SVG, else take as exact center of SVG
        if self.transform_center is None and transform_center_elem is not None:
            self.transform_center = self._extract_transform_center_of(
                transform_center_elem
            )
        if self.transform_center is None:
            self.transform_center = self._get_svg_center()

        ####

        if (
            self.transform_center_second is None
            and transform_center_seconds_elem is not None
        ):
            self.transform_center_second = self._extract_transform_center_of(
                transform_center_seconds_elem
            )

        if (
            self.transform_center_minute is None
            and transform_center_minute_elem is not None
        ):
            self.transform_center_minute = self._extract_transform_center_of(
                transform_center_minute_elem
            )

        if (
            self.transform_center_hour is None
            and transform_center_hour_elem is not None
        ):
            self.transform_center_hour = self._extract_transform_center_of(
                transform_center_hour_elem
            )

    def _validate_svg(self):
        """
        Validate that the SVG contains required hand elements.

        Required: hour-hand, minute-hand
        Optional: second-hand

        Raises:
            ValueError: If any required hand element is missing
        """
        required_ids = ["hour-hand", "minute-hand"]
        optional_ids = ["second-hand"]

        try:
            root = ET.fromstring(self.svg)
        except ET.ParseError as e:
            raise ValueError(f"Invalid SVG: {e}")

        # Find all elements with IDs
        found_ids = set()
        for elem in root.iter():
            elem_id = elem.get("id")
            if elem_id in required_ids or elem_id in optional_ids:
                found_ids.add(elem_id)

        # Check which required IDs are missing
        missing_ids = set(required_ids) - found_ids

        if missing_ids:
            missing_list = ", ".join(sorted(missing_ids))
            raise ValueError(
                f"SVG is missing required elements with IDs: {missing_list}. "
                f"Required IDs are: hour-hand, minute-hand (second-hand is optional)"
            )

    def _extract_transform_center_of(
        self, elem: ET.Element
    ) -> Optional[Tuple[float, float]]:
        center = None
        cx = elem.get("cx")
        cy = elem.get("cy")
        x = elem.get("x")
        y = elem.get("y")

        if cx and cy:
            center = (float(cx), float(cy))
            return center
        elif x and y:
            center = (float(x), float(y))
            return center

    def _get_svg_center(self) -> Tuple[float, float]:
        """
        Extract the center point of the SVG from its viewBox or width/height.

        Returns:
            Tuple of (center_x, center_y)
        """
        root = ET.fromstring(self.svg)

        # Try to get viewBox first (preferred method)
        viewbox = root.get("viewBox")
        if viewbox:
            # viewBox format: "min-x min-y width height"
            parts = viewbox.strip().split()
            if len(parts) == 4:
                min_x, min_y, width, height = map(float, parts)
                center_x = min_x + width / 2
                center_y = min_y + height / 2
                return (center_x, center_y)

        # Fallback to width/height attributes
        width = root.get("width")
        height = root.get("height")
        if width and height:
            # Extract numeric values, handling units like "300px" or "300"
            width_val = float(re.sub(r"[^\d.]", "", width))
            height_val = float(re.sub(r"[^\d.]", "", height))
            return (width_val / 2, height_val / 2)

        raise ValueError("SVG must have either viewBox or width/height attributes.")

    @property
    def transform_center_by_hand_type(self) -> Dict[str, Tuple[float, float]]:
        assert self.transform_center is not None
        return {
            "hour": self.transform_center_hour
            if self.transform_center_hour is not None
            else self.transform_center,
            "minute": self.transform_center_minute
            if self.transform_center_minute is not None
            else self.transform_center,
            "second": self.transform_center_second
            if self.transform_center_second is not None
            else self.transform_center,
        }

    def _calculate_angles(self, clock_time: time) -> Tuple[float, float, float]:
        """
        Calculate rotation angles for clock hands.

        Args:
            clock_time: Time to display on the clock

        Returns:
            Tuple of (hour_angle, minute_angle, second_angle) in degrees
        """
        # Second hand: 6 degrees per second (360 / 60)
        second_angle = clock_time.second * 6

        # Minute hand: 6 degrees per minute + additional from seconds
        minute_angle = clock_time.minute * 6 + clock_time.second * 0.1

        # Hour hand: 30 degrees per hour (360 / 12) + additional from minutes
        hour_angle = (clock_time.hour % 12) * 30 + clock_time.minute * 0.5

        return hour_angle, minute_angle, second_angle

    def _apply_transforms(
        self,
        svg_content: str,
        hour_angle: float,
        minute_angle: float,
        second_angle: float,
    ) -> str:
        """
        Apply CSS transforms to clock hands in the SVG.

        Args:
            svg_content: Original SVG content
            hour_angle: Rotation angle for hour hand
            minute_angle: Rotation angle for minute hand
            second_angle: Rotation angle for second hand

        Returns:
            Modified SVG with transforms applied
        """
        # Parse SVG
        root = ET.fromstring(svg_content)

        # Find and update hour hand
        hour_hand = self._find_element_by_id(root, "hour-hand")
        if hour_hand is not None:
            self._set_transform(hour_hand, hour_angle, "hour")

        # Find and update minute hand
        minute_hand = self._find_element_by_id(root, "minute-hand")
        if minute_hand is not None:
            self._set_transform(minute_hand, minute_angle, "minute")

        # Find and update second hand
        second_hand = self._find_element_by_id(root, "second-hand")
        if second_hand is not None:
            self._set_transform(second_hand, second_angle, "second")

        # Convert back to string
        return ET.tostring(root, encoding="unicode")

    def _find_element_by_id(
        self, root: ET.Element, element_id: str
    ) -> Optional[ET.Element]:
        """
        Find an element by its id attribute.

        Args:
            root: Root element to search from
            element_id: ID to search for

        Returns:
            Element if found, None otherwise
        """
        for elem in root.iter():
            if elem.get("id") == element_id:
                return elem
        return None

    def _set_transform(self, element: ET.Element, angle: float, hand_type: str):
        """
        Set the CSS transform on an element.

        Args:
            element: Element to modify
            angle: Rotation angle in degrees
            hand_type: Type of hand ('hour', 'minute', or 'second')
        """

        # Get the center point - use hand-specific center if available, otherwise fall back to instance's transform_center
        style = element.get("style", "")

        # Determine which transform center to use
        center_x, center_y = self.transform_center_by_hand_type[hand_type]

        # Add or update transform-origin if not present
        if "transform-origin" not in style:
            if style and not style.endswith(";"):
                style += ";"
            style += f"transform-origin: {center_x}px {center_y}px;"

        # Add or update transform
        # Remove existing transform if present
        style_parts = [
            s.strip()
            for s in style.split(";")
            if s.strip() and not s.strip().startswith("transform:")
        ]
        style_parts.append(f"transform: rotate({angle}deg)")

        element.set("style", "; ".join(style_parts))

    def generate(self, clock_time: Union[time, str]) -> str:
        """
        Generate an SVG displaying the specified time.

        Args:
            clock_time: Time to display. Can be a datetime.time object or string in HH:MM:SS format

        Returns:
            SVG content as string with hands positioned for the specified time

        Examples:
            >>> clock = AnalogueClock()
            >>> svg = clock.generate(time(3, 15, 30))
            >>> svg = clock.generate("14:30:45")
        """
        # Parse time if it's a string
        if isinstance(clock_time, str):
            parts = clock_time.split(":")
            if len(parts) == 2:
                parts.append("0")  # Add seconds if not provided
            hour, minute, second = map(int, parts)
            clock_time = time(hour, minute, second)

        # Calculate angles
        hour_angle, minute_angle, second_angle = self._calculate_angles(clock_time)

        # Apply transforms and return
        return self._apply_transforms(self.svg, hour_angle, minute_angle, second_angle)


# Default SVG template
DEFAULT_CLOCK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" width="300" height="300">
  <defs>
    <style>
      .clock-face { fill: white; stroke: black; stroke-width: 2; }
      .hour-marker { fill: black; }
      .number { font-family: Arial, sans-serif; font-size: 20px; text-anchor: middle; dominant-baseline: middle; }
      .hand { stroke-linecap: round; }
      .hour-hand { stroke: black; stroke-width: 6; }
      .minute-hand { stroke: black; stroke-width: 4; }
      .second-hand { stroke: red; stroke-width: 2; }
      .center-dot { fill: black; }
    </style>
  </defs>
  
  <!-- Clock face -->
  <circle class="clock-face" cx="150" cy="150" r="140"/>
  
  <!-- Hour markers -->
  <rect class="hour-marker" x="148" y="20" width="4" height="15"/>
  <rect class="hour-marker" x="148" y="265" width="4" height="15"/>
  <rect class="hour-marker" x="20" y="148" width="15" height="4"/>
  <rect class="hour-marker" x="265" y="148" width="15" height="4"/>
  
  <!-- Numbers -->
  <text class="number" x="150" y="40">12</text>
  <text class="number" x="220" y="70">1</text>
  <text class="number" x="260" y="150">3</text>
  <text class="number" x="220" y="230">5</text>
  <text class="number" x="150" y="260">6</text>
  <text class="number" x="80" y="230">7</text>
  <text class="number" x="40" y="150">9</text>
  <text class="number" x="80" y="70">11</text>
  
  <!-- Clock hands (starting at 12 o'clock position) -->
  <line id="hour-hand" class="hand hour-hand" x1="150" y1="150" x2="150" y2="80" style="transform-origin: 150px 150px; transform: rotate(0deg)"/>
  <line id="minute-hand" class="hand minute-hand" x1="150" y1="150" x2="150" y2="50" style="transform-origin: 150px 150px; transform: rotate(0deg)"/>
  <line id="second-hand" class="hand second-hand" x1="150" y1="150" x2="150" y2="40" style="transform-origin: 150px 150px; transform: rotate(0deg)"/>
  
  <!-- Center dot -->
  <circle class="center-dot" cx="150" cy="150" r="5"/>
</svg>"""
