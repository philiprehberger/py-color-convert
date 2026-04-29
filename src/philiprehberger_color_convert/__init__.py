"""Convert between color formats: hex, RGB, HSL, HSV, CMYK, and named CSS colors."""

from __future__ import annotations

import colorsys
import re

__all__ = ["Color", "css_color_names"]

_CSS_COLORS: dict[str, str] = {
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgreen": "#006400",
    "darkgrey": "#a9a9a9",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "grey": "#808080",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgray": "#d3d3d3",
    "lightgreen": "#90ee90",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
}


def _clamp(value: float, low: float, high: float) -> float:
    """Clamp a value between low and high."""
    return max(low, min(high, value))


def _hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Convert a hex string to an RGB tuple."""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = hex_str[0] * 2 + hex_str[1] * 2 + hex_str[2] * 2
    return (
        int(hex_str[0:2], 16),
        int(hex_str[2:4], 16),
        int(hex_str[4:6], 16),
    )


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to a hex string."""
    return f"#{r:02x}{g:02x}{b:02x}"


def _rgb_to_hsl(r: int, g: int, b: int) -> tuple[int, int, int]:
    """Convert RGB (0-255) to HSL (h: 0-360, s: 0-100, l: 0-100)."""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return (round(h * 360) % 360, round(s * 100), round(l * 100))


def _hsl_to_rgb(h: int, s: int, l: int) -> tuple[int, int, int]:
    """Convert HSL (h: 0-360, s: 0-100, l: 0-100) to RGB (0-255)."""
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return (round(r * 255), round(g * 255), round(b * 255))


def _rgb_to_hsv(r: int, g: int, b: int) -> tuple[int, int, int]:
    """Convert RGB (0-255) to HSV (h: 0-360, s: 0-100, v: 0-100)."""
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return (round(h * 360) % 360, round(s * 100), round(v * 100))


def _hsv_to_rgb(h: int, s: int, v: int) -> tuple[int, int, int]:
    """Convert HSV (h: 0-360, s: 0-100, v: 0-100) to RGB (0-255)."""
    r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
    return (round(r * 255), round(g * 255), round(b * 255))


def _rgb_to_cmyk(r: int, g: int, b: int) -> tuple[int, int, int, int]:
    """Convert RGB (0-255) to CMYK (0-100 each)."""
    if r == 0 and g == 0 and b == 0:
        return (0, 0, 0, 100)
    r_norm = r / 255
    g_norm = g / 255
    b_norm = b / 255
    k = 1 - max(r_norm, g_norm, b_norm)
    c = (1 - r_norm - k) / (1 - k)
    m = (1 - g_norm - k) / (1 - k)
    y = (1 - b_norm - k) / (1 - k)
    return (round(c * 100), round(m * 100), round(y * 100), round(k * 100))


def _cmyk_to_rgb(c: int, m: int, y: int, k: int) -> tuple[int, int, int]:
    """Convert CMYK (0-100 each) to RGB (0-255)."""
    r = 255 * (1 - c / 100) * (1 - k / 100)
    g = 255 * (1 - m / 100) * (1 - k / 100)
    b = 255 * (1 - y / 100) * (1 - k / 100)
    return (round(r), round(g), round(b))


def _relative_luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance per WCAG 2.0."""
    def linearize(c: float) -> float:
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


class Color:
    """Immutable color representation with conversion between formats.

    Stores color internally as RGB (0-255 integers). Supports construction
    from hex strings, CSS rgb() strings, CSS named colors, and other Color
    instances.
    """

    __slots__ = ("_r", "_g", "_b")

    def __init__(self, value: str | Color) -> None:
        if isinstance(value, Color):
            self._r = value._r
            self._g = value._g
            self._b = value._b
            return

        if not isinstance(value, str):
            raise TypeError(f"Expected str or Color, got {type(value).__name__}")

        value = value.strip()

        # Try hex
        if value.startswith("#") or re.fullmatch(r"[0-9a-fA-F]{3}([0-9a-fA-F]{3})?", value):
            hex_str = value.lstrip("#")
            if len(hex_str) not in (3, 6):
                raise ValueError(f"Invalid hex color: {value}")
            r, g, b = _hex_to_rgb(hex_str)
            self._r = r
            self._g = g
            self._b = b
            return

        # Try rgb() string
        match = re.fullmatch(r"rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)", value)
        if match:
            r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError(f"RGB values must be 0-255, got ({r}, {g}, {b})")
            self._r = r
            self._g = g
            self._b = b
            return

        # Try CSS named color
        name = value.lower()
        if name in _CSS_COLORS:
            r, g, b = _hex_to_rgb(_CSS_COLORS[name])
            self._r = r
            self._g = g
            self._b = b
            return

        raise ValueError(f"Cannot parse color: {value!r}")

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> Color:
        """Create a Color from RGB values (0-255 each)."""
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError(f"RGB values must be 0-255, got ({r}, {g}, {b})")
        color = object.__new__(cls)
        color._r = r
        color._g = g
        color._b = b
        return color

    @classmethod
    def from_hsl(cls, h: int, s: int, l: int) -> Color:
        """Create a Color from HSL values (h: 0-360, s: 0-100, l: 0-100)."""
        r, g, b = _hsl_to_rgb(h, s, l)
        return cls.from_rgb(r, g, b)

    @classmethod
    def from_hsv(cls, h: int, s: int, v: int) -> Color:
        """Create a Color from HSV values (h: 0-360, s: 0-100, v: 0-100)."""
        r, g, b = _hsv_to_rgb(h, s, v)
        return cls.from_rgb(r, g, b)

    @classmethod
    def from_cmyk(cls, c: int, m: int, y: int, k: int) -> Color:
        """Create a Color from CMYK values (0-100 each)."""
        r, g, b = _cmyk_to_rgb(c, m, y, k)
        return cls.from_rgb(r, g, b)

    @property
    def rgb(self) -> tuple[int, int, int]:
        """RGB tuple (r, g, b) with values 0-255."""
        return (self._r, self._g, self._b)

    @property
    def hex(self) -> str:
        """Hex string in the format '#rrggbb'."""
        return _rgb_to_hex(self._r, self._g, self._b)

    @property
    def hsl(self) -> tuple[int, int, int]:
        """HSL tuple (h, s, l) with h: 0-360, s: 0-100, l: 0-100."""
        return _rgb_to_hsl(self._r, self._g, self._b)

    @property
    def hsv(self) -> tuple[int, int, int]:
        """HSV tuple (h, s, v) with h: 0-360, s: 0-100, v: 0-100."""
        return _rgb_to_hsv(self._r, self._g, self._b)

    @property
    def cmyk(self) -> tuple[int, int, int, int]:
        """CMYK tuple (c, m, y, k) with values 0-100."""
        return _rgb_to_cmyk(self._r, self._g, self._b)

    def lighten(self, percent: float) -> Color:
        """Return a new Color lightened by the given percentage."""
        h, s, l = self.hsl
        new_l = round(_clamp(l + percent, 0, 100))
        return Color.from_hsl(h, s, new_l)

    def darken(self, percent: float) -> Color:
        """Return a new Color darkened by the given percentage."""
        h, s, l = self.hsl
        new_l = round(_clamp(l - percent, 0, 100))
        return Color.from_hsl(h, s, new_l)

    def saturate(self, percent: float) -> Color:
        """Return a new Color with increased saturation."""
        h, s, l = self.hsl
        new_s = round(_clamp(s + percent, 0, 100))
        return Color.from_hsl(h, new_s, l)

    def desaturate(self, percent: float) -> Color:
        """Return a new Color with decreased saturation."""
        h, s, l = self.hsl
        new_s = round(_clamp(s - percent, 0, 100))
        return Color.from_hsl(h, new_s, l)

    def complement(self) -> Color:
        """Return the complementary Color (180 degrees on the color wheel)."""
        h, s, l = self.hsl
        return Color.from_hsl((h + 180) % 360, s, l)

    def invert(self) -> Color:
        """Return the inverted Color."""
        return Color.from_rgb(255 - self._r, 255 - self._g, 255 - self._b)

    def analogous(self) -> list[Color]:
        """Return a list of 3 analogous Colors (self, +30, -30 degrees)."""
        h, s, l = self.hsl
        return [
            Color.from_hsl(h, s, l),
            Color.from_hsl((h + 30) % 360, s, l),
            Color.from_hsl((h - 30) % 360, s, l),
        ]

    def triadic(self) -> list[Color]:
        """Return a list of 3 triadic Colors (self, +120, +240 degrees)."""
        h, s, l = self.hsl
        return [
            Color.from_hsl(h, s, l),
            Color.from_hsl((h + 120) % 360, s, l),
            Color.from_hsl((h + 240) % 360, s, l),
        ]

    def split_complementary(self) -> list[Color]:
        """Return a list of 3 split-complementary Colors (self, +150, +210 degrees)."""
        h, s, l = self.hsl
        return [
            Color.from_hsl(h, s, l),
            Color.from_hsl((h + 150) % 360, s, l),
            Color.from_hsl((h + 210) % 360, s, l),
        ]

    def mix(self, other: Color, weight: float = 0.5) -> Color:
        """Return a new Color blended with ``other`` in RGB space.

        Args:
            other: The Color to blend with.
            weight: Blend ratio. ``0.0`` returns ``self`` unchanged,
                ``1.0`` returns ``other``, ``0.5`` (the default) is an
                even mix.

        Raises:
            ValueError: If ``weight`` is outside ``[0.0, 1.0]``.
        """
        if not 0.0 <= weight <= 1.0:
            raise ValueError(f"weight must be between 0.0 and 1.0, got {weight}")
        r = round(self._r * (1 - weight) + other._r * weight)
        g = round(self._g * (1 - weight) + other._g * weight)
        b = round(self._b * (1 - weight) + other._b * weight)
        return Color.from_rgb(r, g, b)

    def contrast_ratio(self, other: Color) -> float:
        """Calculate the WCAG 2.0 contrast ratio between this Color and another.

        Returns a value between 1.0 (no contrast) and 21.0 (maximum contrast).
        """
        l1 = _relative_luminance(self._r, self._g, self._b)
        l2 = _relative_luminance(other._r, other._g, other._b)
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return round((lighter + 0.05) / (darker + 0.05), 2)

    def __repr__(self) -> str:
        return f"Color('{self.hex}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return self._r == other._r and self._g == other._g and self._b == other._b

    def __hash__(self) -> int:
        return hash((self._r, self._g, self._b))


def css_color_names() -> list[str]:
    """Return a sorted list of all supported CSS color names."""
    return sorted(_CSS_COLORS)
