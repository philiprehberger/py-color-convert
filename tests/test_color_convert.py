"""Tests for philiprehberger_color_convert."""

from __future__ import annotations

import pytest

from philiprehberger_color_convert import Color, css_color_names


class TestParsing:
    def test_hex_six_digits(self) -> None:
        assert Color("#ff0000").rgb == (255, 0, 0)

    def test_hex_three_digits(self) -> None:
        assert Color("#f00").rgb == (255, 0, 0)

    def test_hex_no_hash(self) -> None:
        assert Color("00ff00").rgb == (0, 255, 0)

    def test_rgb_string(self) -> None:
        assert Color("rgb(10, 20, 30)").rgb == (10, 20, 30)

    def test_named_color(self) -> None:
        assert Color("red").rgb == (255, 0, 0)
        assert Color("BLUE").rgb == (0, 0, 255)

    def test_from_existing_color(self) -> None:
        c = Color("#abcdef")
        c2 = Color(c)
        assert c == c2
        assert c is not c2

    def test_invalid_color_raises(self) -> None:
        with pytest.raises(ValueError):
            Color("not-a-color")

    def test_non_string_raises(self) -> None:
        with pytest.raises(TypeError):
            Color(123)  # type: ignore[arg-type]

    def test_rgb_out_of_range_raises(self) -> None:
        with pytest.raises(ValueError):
            Color("rgb(300, 0, 0)")


class TestFactories:
    def test_from_rgb(self) -> None:
        c = Color.from_rgb(10, 20, 30)
        assert c.rgb == (10, 20, 30)

    def test_from_rgb_validates_range(self) -> None:
        with pytest.raises(ValueError):
            Color.from_rgb(-1, 0, 0)

    def test_from_hsl_round_trip(self) -> None:
        red = Color("#ff0000")
        h, s, l = red.hsl
        assert Color.from_hsl(h, s, l).hex == "#ff0000"

    def test_from_hsv_round_trip(self) -> None:
        green = Color("#00ff00")
        h, s, v = green.hsv
        assert Color.from_hsv(h, s, v).hex == "#00ff00"

    def test_from_cmyk_round_trip(self) -> None:
        # Pure colors round-trip exactly through CMYK
        c = Color("#0000ff")
        cmyk = c.cmyk
        assert Color.from_cmyk(*cmyk).hex == "#0000ff"


class TestProperties:
    def test_hex(self) -> None:
        assert Color.from_rgb(255, 0, 128).hex == "#ff0080"

    def test_rgb(self) -> None:
        assert Color("#102030").rgb == (16, 32, 48)

    def test_hsl_pure_red(self) -> None:
        h, s, l = Color("#ff0000").hsl
        assert h == 0 and s == 100 and l == 50


class TestManipulation:
    def test_lighten(self) -> None:
        c = Color("#ff0000")
        light = c.lighten(20)
        assert light.hsl[2] > c.hsl[2]

    def test_darken(self) -> None:
        c = Color("#ff0000")
        dark = c.darken(20)
        assert dark.hsl[2] < c.hsl[2]

    def test_saturate(self) -> None:
        c = Color.from_hsl(0, 50, 50)
        sat = c.saturate(20)
        assert sat.hsl[1] >= c.hsl[1]

    def test_desaturate(self) -> None:
        c = Color.from_hsl(0, 50, 50)
        desat = c.desaturate(20)
        assert desat.hsl[1] <= c.hsl[1]

    def test_invert(self) -> None:
        assert Color("#000000").invert() == Color("#ffffff")

    def test_complement_180_degrees(self) -> None:
        c = Color.from_hsl(120, 100, 50)
        comp = c.complement()
        assert comp.hsl[0] == 300


class TestMix:
    def test_mix_default_is_midpoint(self) -> None:
        red = Color("#ff0000")
        blue = Color("#0000ff")
        mixed = red.mix(blue)
        # 50/50 between (255,0,0) and (0,0,255) is approx (128,0,128)
        assert mixed.rgb == (128, 0, 128)

    def test_mix_weight_zero_returns_self(self) -> None:
        red = Color("#ff0000")
        blue = Color("#0000ff")
        assert red.mix(blue, weight=0.0) == red

    def test_mix_weight_one_returns_other(self) -> None:
        red = Color("#ff0000")
        blue = Color("#0000ff")
        assert red.mix(blue, weight=1.0) == blue

    def test_mix_invalid_weight(self) -> None:
        red = Color("#ff0000")
        blue = Color("#0000ff")
        with pytest.raises(ValueError):
            red.mix(blue, weight=1.5)
        with pytest.raises(ValueError):
            red.mix(blue, weight=-0.1)


class TestPalettes:
    def test_analogous_returns_three(self) -> None:
        assert len(Color("#ff0000").analogous()) == 3

    def test_triadic_returns_three(self) -> None:
        assert len(Color("#ff0000").triadic()) == 3

    def test_split_complementary_returns_three(self) -> None:
        assert len(Color("#ff0000").split_complementary()) == 3


class TestContrast:
    def test_white_on_black_is_max(self) -> None:
        ratio = Color("#ffffff").contrast_ratio(Color("#000000"))
        assert ratio == 21.0

    def test_same_color_is_one(self) -> None:
        assert Color("#888888").contrast_ratio(Color("#888888")) == 1.0


class TestEqualityAndRepr:
    def test_equal_colors(self) -> None:
        assert Color("#abc") == Color("#aabbcc")

    def test_repr(self) -> None:
        assert repr(Color("#ff0000")) == "Color('#ff0000')"

    def test_hashable(self) -> None:
        s = {Color("#fff"), Color("#ffffff")}
        assert len(s) == 1


class TestCssColorNames:
    def test_returns_sorted_list(self) -> None:
        names = css_color_names()
        assert "red" in names
        assert "blue" in names
        assert names == sorted(names)
