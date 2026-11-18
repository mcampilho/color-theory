"""The RYB colours match the 12-colour wheel of w3schools / Canva (see the README)."""
import pytest

import color_theory_document as doc

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
    got = to_255(doc.hue_rgb(index))
    # the tertiaries are averages of their neighbours, so one unit of rounding is allowed
    assert all(abs(a - b) <= 1 for a, b in zip(got, want)), "%s: %s instead of %s" % (index, got, want)


def test_hue_ryb_is_periodic_and_continuous():
    assert doc.hue_ryb(0) == doc.hue_ryb(12)
    mid = doc.hue_ryb(0.5)
    a, b = doc.HUE_RYB[0], doc.HUE_RYB[1]
    assert mid == pytest.approx(tuple((x + y) / 2 for x, y in zip(a, b)))


def test_cube_corners_are_the_pure_colours():
    assert to_255(doc.ryb_to_rgb(0, 0, 0)) == (255, 255, 255)      # no pigment: the white of the paper
    assert to_255(doc.ryb_to_rgb(1, 1, 1)) == to_255(doc.RYB_CORNERS[(1, 1, 1)])   # all pigments: near black
    red, blue = doc.ryb_to_rgb(1, 0, 0), doc.ryb_to_rgb(0, 0, 1)
    assert red[0] > 0.9 and blue[2] > 0.9


def test_mix_and_luma():
    assert doc.mix((0, 0, 0), (1, 1, 1), 0.25) == (0.25, 0.25, 0.25)
    assert doc.luma((1, 1, 1)) == pytest.approx(1.0)
    assert doc.luma((0, 0, 0)) == 0
