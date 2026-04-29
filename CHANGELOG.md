# Changelog

## 0.2.0 (2026-04-29)

- Add `Color.mix(other, weight=0.5)` to blend two colors in RGB space
- Replace import-only stub with comprehensive test suite (parsing, factory round-trips, manipulation, palettes, contrast, mixing)

## 0.1.9 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template

## 0.1.8

- Add css_color_names() function for discovering available CSS colors
- Add method chaining example to README

## 0.1.7

- Trim keywords to match pyproject template guide

## 0.1.6

- Add pytest and mypy tool configuration to pyproject.toml

## 0.1.5

- Add basic import test

## 0.1.4

- Add Development section to README

## 0.1.1

- Re-release for PyPI publishing

## 0.1.0 (2026-03-15)

- Initial release
- `Color` class with hex, RGB, HSL, HSV, and CMYK conversion
- Color manipulation: lighten, darken, saturate, desaturate, complement, invert
- Palette generation: analogous, triadic, split-complementary
- WCAG contrast ratio calculation
- 148 named CSS colors supported
