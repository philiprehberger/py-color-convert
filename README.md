# philiprehberger-color-convert

[![Tests](https://github.com/philiprehberger/py-color-convert/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-color-convert/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-color-convert.svg)](https://pypi.org/project/philiprehberger-color-convert/)
[![License](https://img.shields.io/github/license/philiprehberger/py-color-convert)](LICENSE)

Convert between color formats: hex, RGB, HSL, HSV, CMYK, and named CSS colors.

## Install

```bash
pip install philiprehberger-color-convert
```

## Usage

```python
from philiprehberger_color_convert import Color

# Create from hex
c = Color("#ff6b35")

# Create from CSS named color
c = Color("tomato")

# Create from RGB string
c = Color("rgb(255, 107, 53)")

# Create from another Color
c2 = Color(c)
```

### Factory Methods

```python
c = Color.from_rgb(255, 107, 53)
c = Color.from_hsl(20, 100, 60)
c = Color.from_hsv(20, 79, 100)
c = Color.from_cmyk(0, 58, 79, 0)
```

### Format Properties

```python
c = Color("#ff6b35")

c.rgb   # (255, 107, 53)
c.hex   # "#ff6b35"
c.hsl   # (16, 100, 60)
c.hsv   # (16, 79, 100)
c.cmyk  # (0, 58, 79, 0)
```

### Manipulation

```python
c = Color("#ff6b35")

lighter = c.lighten(20)
darker = c.darken(20)
more = c.saturate(10)
less = c.desaturate(10)
comp = c.complement()
inv = c.invert()
```

### Palette Generation

```python
c = Color("#ff6b35")

c.analogous()            # [Color, Color, Color]
c.triadic()              # [Color, Color, Color]
c.split_complementary()  # [Color, Color, Color]
```

### Contrast Ratio

```python
white = Color("#ffffff")
black = Color("#000000")

white.contrast_ratio(black)  # 21.0
```

## API

| Method / Property | Description |
|-------------------|-------------|
| `Color(value)` | Create from hex, RGB string, CSS name, or Color |
| `Color.from_rgb(r, g, b)` | Create from RGB values (0-255) |
| `Color.from_hsl(h, s, l)` | Create from HSL (h: 0-360, s/l: 0-100) |
| `Color.from_hsv(h, s, v)` | Create from HSV (h: 0-360, s/v: 0-100) |
| `Color.from_cmyk(c, m, y, k)` | Create from CMYK (0-100 each) |
| `.rgb` | RGB tuple `(r, g, b)` |
| `.hex` | Hex string `"#rrggbb"` |
| `.hsl` | HSL tuple `(h, s, l)` |
| `.hsv` | HSV tuple `(h, s, v)` |
| `.cmyk` | CMYK tuple `(c, m, y, k)` |
| `.lighten(percent)` | Return lighter Color |
| `.darken(percent)` | Return darker Color |
| `.saturate(percent)` | Return more saturated Color |
| `.desaturate(percent)` | Return less saturated Color |
| `.complement()` | Return complementary Color |
| `.invert()` | Return inverted Color |
| `.analogous()` | List of 3 analogous Colors |
| `.triadic()` | List of 3 triadic Colors |
| `.split_complementary()` | List of 3 split-complementary Colors |
| `.contrast_ratio(other)` | WCAG contrast ratio (float) |

## License

MIT
