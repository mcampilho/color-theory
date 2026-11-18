"""The RYB colours match the 12-colour wheel of w3schools / Canva (see the README)."""
import pytest

from colortheory import colour

# hue index (clockwise from the top, as in HUE_RYB) -> hex of the wheel
WHEEL = {
    0: "FEFE33",   # yellow
    1: "FCCC1A",   # yellow-orange
    2: "FB9902",   # orange
    3: "FC600A",   # red-orange
    4: "FE2712",   # red
    5: "C21460",   # red-violet
    6: "8601AF",   # violet
    7: "4424D6",   # blue-violet
    8: "0247FE",   # blue
    9: "347C98",   # blue-green
    10: "66B032",  # green
    11: "B2D732",  # yellow-green
}


def to_255(colour):
    return tuple(round(255 * v) for v in colour)


@pytest.mark.parametrize("index", sorted(WHEEL))
def test_wheel_colour(index):
    want = tuple(int(WHEEL[index][k:k + 2], 16) for k in (0, 2, 4))
    got = to_255(colour.hue_rgb(index))
    # the tertiaries are averages of their neighbours, so one unit of rounding is allowed
    assert all(abs(a - b) <= 1 for a, b in zip(got, want)), "%s: %s instead of %s" % (index, got, want)


def test_hue_ryb_is_periodic_and_continuous():
    assert colour.hue_ryb(0) == colour.hue_ryb(12)
    mid = colour.hue_ryb(0.5)
    a, b = colour.HUE_RYB[0], colour.HUE_RYB[1]
    assert mid == pytest.approx(tuple((x + y) / 2 for x, y in zip(a, b)))


def test_cube_corners_are_the_pure_colours():
    assert to_255(colour.ryb_to_rgb(0, 0, 0)) == (255, 255, 255)      # no pigment: the white of the paper
    assert to_255(colour.ryb_to_rgb(1, 1, 1)) == to_255(colour.RYB_CORNERS[(1, 1, 1)])   # all pigments: near black
    red, blue = colour.ryb_to_rgb(1, 0, 0), colour.ryb_to_rgb(0, 0, 1)
    assert red[0] > 0.9 and blue[2] > 0.9


def test_mix_and_luma():
    assert colour.mix((0, 0, 0), (1, 1, 1), 0.25) == (0.25, 0.25, 0.25)
    assert colour.luma((1, 1, 1)) == pytest.approx(1.0)
    assert colour.luma((0, 0, 0)) == 0

def test_hsb_primaries():
    assert colour.hsb(0, 1, 1) == (1.0, 0.0, 0.0)
    assert colour.hsb(120, 1, 1) == (0.0, 1.0, 0.0)
    assert colour.hsb(360, 0, 0.5) == (0.5, 0.5, 0.5)          # hue wraps; no saturation: grey


def test_hex_rgb():
    assert colour.hex_rgb("FF8000") == (1.0, 128 / 255, 0.0)


def test_cmy_inks_multiply_to_white_and_darker():
    assert colour.cmy_to_rgb((0, 0, 0)) == (1.0, 1.0, 1.0)      # no ink: the paper
    assert colour.luma(colour.cmy_to_rgb((1, 1, 1))) < 0.2      # all three inks: near black


def test_cie_white_point_is_displayable_and_grey():
    r, g, b = colour.xy_colour(0.3127, 0.3290)                  # D65
    assert max(r, g, b) - min(r, g, b) < 0.02


def test_planck_xy_moves_from_orange_to_blue():
    warm, cool = colour.planck_xy(2000), colour.planck_xy(10000)
    assert warm[0] > cool[0]                                    # warmer light has the larger x
