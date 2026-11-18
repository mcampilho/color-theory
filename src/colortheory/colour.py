"""Colour maths shared by the programs: the RYB model, CMY inks, HSB, and the CIE 1931 / CIELAB
conversions. Colours are (r, g, b) tuples of floats in 0..1. No drawing happens here."""
import colorsys
import math


def hex_rgb(code):
    """'FE2712' -> (r, g, b) in 0..1."""
    return tuple(int(code[k:k + 2], 16) / 255.0 for k in (0, 2, 4))

def luma(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def text_on(c):
    return (1, 1, 1) if luma(c) < 0.62 else (0.1, 0.1, 0.1)


def mix(c1, c2, t):
    return tuple(a + (b - a) * t for a, b in zip(c1, c2))


# sRGB colours of the 8 corners of the RYB cube; inside the cube colours are
# trilinearly interpolated with smoothstep easing (Gossett & Chen, 2004).
# Primaries and secondaries are the RYB wheel of w3schools and Canva; the
# tertiaries, halfway along the edges, come out as the averages of their two
# neighbours, which are exactly the tertiaries of that wheel too.
RYB_CORNERS = {
    (0, 0, 0): (1.00, 1.00, 1.00),   # white
    (1, 0, 0): hex_rgb("FE2712"),       # red
    (0, 1, 0): hex_rgb("FEFE33"),       # yellow
    (0, 0, 1): hex_rgb("0247FE"),       # blue
    (1, 1, 0): hex_rgb("FB9902"),       # orange  = red + yellow
    (0, 1, 1): hex_rgb("66B032"),       # green   = yellow + blue
    (1, 0, 1): hex_rgb("8601AF"),       # violet  = red + blue
    (1, 1, 1): (0.20, 0.10, 0.08),   # all pigments -> near black
}


def ryb_to_rgb(r, y, b):
    r, y, b = (t * t * (3 - 2 * t) for t in (r, y, b))
    out = [0.0, 0.0, 0.0]
    for (cr, cy, cb), col in RYB_CORNERS.items():
        w = (r if cr else 1 - r) * (y if cy else 1 - y) * (b if cb else 1 - b)
        for k in range(3):
            out[k] += w * col[k]
    return tuple(out)


# 12 hues clockwise from the top (points on the edges of the RYB cube)
HUE_RYB = [(0, 1, 0), (.5, 1, 0), (1, 1, 0), (1, .5, 0), (1, 0, 0), (1, 0, .5),
           (1, 0, 1), (.5, 0, 1), (0, 0, 1), (0, .5, 1), (0, 1, 1), (0, 1, .5)]


def hue_ryb(t):
    t %= 12
    i = int(math.floor(t))
    f = t - i
    a, b = HUE_RYB[i], HUE_RYB[(i + 1) % 12]
    return tuple(a[k] + (b[k] - a[k]) * f for k in range(3))


def hue_rgb(i):
    return ryb_to_rgb(*HUE_RYB[i % 12])


def hsb(h, s, v):
    """Hue in degrees, s and v in 0..1 -> RGB tuple."""
    return colorsys.hsv_to_rgb((h % 360) / 360.0, max(0, min(1, s)), max(0, min(1, v)))


CMY_INKS = ((0.0, .62, .90), (.90, 0.0, .52), (1.0, .93, 0.0))


def cmy_to_rgb(cmy):
    """Cyan, magenta and yellow ink coverage (0..1) -> sRGB, by multiplying
    the filtering of each ink."""
    out = [1.0, 1.0, 1.0]
    for v, ink in zip(cmy, CMY_INKS):
        out = [o * (1 - v * (1 - ink[k])) for k, o in enumerate(out)]
    return tuple(out)


# CIE 1931 chromaticity (x, y) of the pure spectral colours, 380-700 nm
# every 5 nm (the official table; the Gaussian fit below drifts at the ends).
SPECTRAL_LOCUS = [
    (.1741, .0050), (.1740, .0050), (.1738, .0049), (.1736, .0049), (.1733, .0048),
    (.1730, .0048), (.1726, .0048), (.1721, .0048), (.1714, .0051), (.1703, .0058),
    (.1689, .0069), (.1669, .0086), (.1644, .0109), (.1611, .0138), (.1566, .0177),
    (.1510, .0227), (.1440, .0297), (.1355, .0399), (.1241, .0578), (.1096, .0868),
    (.0913, .1327), (.0687, .2007), (.0454, .2950), (.0235, .4127), (.0082, .5384),
    (.0039, .6548), (.0139, .7502), (.0389, .8120), (.0743, .8338), (.1142, .8262),
    (.1547, .8059), (.1929, .7816), (.2296, .7543), (.2658, .7243), (.3016, .6923),
    (.3373, .6589), (.3731, .6245), (.4087, .5896), (.4441, .5547), (.4788, .5202),
    (.5125, .4866), (.5448, .4544), (.5752, .4242), (.6029, .3965), (.6270, .3725),
    (.6482, .3514), (.6658, .3340), (.6801, .3197), (.6915, .3083), (.7006, .2993),
    (.7079, .2920), (.7140, .2859), (.7190, .2809), (.7230, .2770), (.7260, .2740),
    (.7283, .2717), (.7300, .2700), (.7311, .2689), (.7320, .2680), (.7327, .2673),
    (.7334, .2666), (.7340, .2660), (.7344, .2656), (.7346, .2654), (.7347, .2653),
]


def locus_xy(lam):
    """Chromaticity of wavelength lam (nm), interpolated in SPECTRAL_LOCUS
    with a Catmull-Rom spline."""
    n = len(SPECTRAL_LOCUS)
    t = min(max((lam - 380) / 5.0, 0), n - 1)
    i = min(int(t), n - 2)
    f = t - i
    p0, p1, p2, p3 = (SPECTRAL_LOCUS[min(max(k, 0), n - 1)] for k in (i - 1, i, i + 1, i + 2))
    return tuple(.5 * (2 * b + (c - a) * f + (2 * a - 5 * b + 4 * c - d) * f * f
                       + (3 * b - a - 3 * c + d) * f ** 3) for a, b, c, d in zip(p0, p1, p2, p3))


def cmf(lam):
    """CIE 1931 2-degree colour-matching functions x, y, z at wavelength lam
    (nm), from the multi-lobe Gaussian fit of Wyman, Sloan & Shirley (2013)."""
    def g(mu, s1, s2):
        return math.exp(-.5 * ((lam - mu) / (s1 if lam < mu else s2)) ** 2)
    return (1.056 * g(599.8, 37.9, 31.0) + .362 * g(442.0, 16.0, 26.7)
            - .065 * g(501.1, 20.4, 26.2),
            .821 * g(568.8, 46.9, 40.5) + .286 * g(530.9, 16.3, 31.1),
            1.217 * g(437.0, 11.8, 36.0) + .681 * g(459.0, 26.0, 13.8))


def xy_of(xyz):
    s = sum(xyz)
    return xyz[0] / s, xyz[1] / s


def xyz_to_linear_srgb(X, Y, Z):
    return (3.2406 * X - 1.5372 * Y - .4986 * Z,
            -.9689 * X + 1.8758 * Y + .0415 * Z,
            .0557 * X - .2040 * Y + 1.0570 * Z)


def srgb_gamma(v):
    v = max(0.0, min(1.0, v))
    return 12.92 * v if v <= .0031308 else 1.055 * v ** (1 / 2.4) - .055


def displayable(rgb):
    """Pull a linear RGB colour outside sRGB toward white (by adding grey)
    until no channel is negative."""
    lo = min(rgb)
    return tuple(v - lo for v in rgb) if lo < 0 else tuple(rgb)


def xy_colour(x, y):
    """Brightest displayable colour of chromaticity (x, y)."""
    rgb = displayable(xyz_to_linear_srgb(x / y, 1.0, max(0.0, 1 - x - y) / y))
    hi = max(rgb)
    return tuple(srgb_gamma(v / hi) for v in rgb)


def planck_xy(T):
    """Chromaticity of a black body at temperature T (kelvin)."""
    acc = [0.0, 0.0, 0.0]
    for lam in range(380, 785, 5):
        l = lam * 1e-9
        e = 1.0 / (l ** 5 * (math.exp(1.4388e-2 / (l * T)) - 1))
        for k, v in enumerate(cmf(lam)):
            acc[k] += e * v
    return xy_of(acc)


def lab_to_linear_srgb(L, a, b):
    """CIELAB (D65 white) -> linear sRGB (may fall outside 0..1)."""
    def inv(t):
        return t ** 3 if t > 6 / 29.0 else 3 * (6 / 29.0) ** 2 * (t - 4 / 29.0)
    fy = (L + 16) / 116.0
    return xyz_to_linear_srgb(.95047 * inv(fy + a / 500.0), inv(fy), 1.08883 * inv(fy - b / 200.0))


def cusp_colour(h):
    """Most saturated sRGB colour of CIELAB hue angle h: for each lightness,
    the largest chroma still inside sRGB (bisection), then the best of all."""
    ca, sa = math.cos(math.radians(h)), math.sin(math.radians(h))
    best_c, best = 0.0, (0.5, 0.5, 0.5)
    for L in range(20, 99):
        lo, hi = 0.0, 150.0
        for _ in range(16):
            mid = (lo + hi) / 2
            rgb = lab_to_linear_srgb(L, mid * ca, mid * sa)
            if min(rgb) >= 0 and max(rgb) <= 1:
                lo = mid
            else:
                hi = mid
        if lo > best_c:
            best_c, best = lo, lab_to_linear_srgb(L, lo * ca, lo * sa)
    return tuple(srgb_gamma(v) for v in best)
