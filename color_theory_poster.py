#!/usr/bin/env python3
"""
color_theory_poster.py
----------------------
Draws a "Colour Theory" poster (page 1) as a vector PDF with ReportLab,
including a 12-hue colour wheel built on the RYB (Red-Yellow-Blue) model.

    pip install reportlab
    python color_theory_poster.py                 # -> colour_theory.pdf
    python color_theory_poster.py my_file.pdf

Everything is drawn as vector graphics, so it stays sharp at any zoom.
More pages can be added by writing another build_page_N(c) function and
calling c.showPage() between them (see main()).
"""
import math
import sys

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

# --------------------------------------------------------------------------
# Page geometry
# --------------------------------------------------------------------------
W, H = landscape(letter)          # 792 x 612 pt
# Layout was designed on a 750 x 570 grid; these helpers map it to the page.
SX, SY = W / 750.0, H / 570.0


def X(x):
    return x * SX


def Y(y):
    return H - y * SY


# --------------------------------------------------------------------------
# RYB colour model
# --------------------------------------------------------------------------
# Colours of the 8 corners of the RYB cube (r, y, b -> sRGB 0..1).
# Trilinear interpolation inside the cube (with a smoothstep easing, as in
# Gossett & Chen, "Paint Inspired Color Mixing and Compositing", 2004)
# gives any RYB mixture. Tweak these corner values to restyle the wheel.
RYB_CORNERS = {
    (0, 0, 0): (1.00, 1.00, 1.00),   # white (no pigment)
    (1, 0, 0): (0.89, 0.12, 0.13),   # red
    (0, 1, 0): (1.00, 0.92, 0.00),   # yellow
    (0, 0, 1): (0.10, 0.30, 0.85),   # blue
    (1, 1, 0): (0.97, 0.55, 0.08),   # orange  = red + yellow
    (0, 1, 1): (0.20, 0.66, 0.20),   # green   = yellow + blue
    (1, 0, 1): (0.52, 0.10, 0.58),   # violet  = red + blue
    (1, 1, 1): (0.20, 0.10, 0.08),   # all three pigments -> near black
}


def ryb_to_rgb(r, y, b):
    """Convert an RYB mixture (each 0..1) to an sRGB tuple (0..1)."""
    r, y, b = (t * t * (3 - 2 * t) for t in (r, y, b))
    out = [0.0, 0.0, 0.0]
    for (cr, cy, cb), col in RYB_CORNERS.items():
        w = (r if cr else 1 - r) * (y if cy else 1 - y) * (b if cb else 1 - b)
        for k in range(3):
            out[k] += w * col[k]
    return tuple(out)


# The 12 hues, clockwise from the top: yellow, yellow-orange, orange,
# red-orange, red, red-violet, violet, blue-violet, blue, blue-green,
# green, yellow-green  -> each as an (r, y, b) mixture on the RYB cube edges.
HUE_RYB = [
    (0.0, 1.0, 0.0),   # 0  yellow        (primary)
    (0.5, 1.0, 0.0),   # 1  yellow-orange (tertiary)
    (1.0, 1.0, 0.0),   # 2  orange        (secondary)
    (1.0, 0.5, 0.0),   # 3  red-orange    (tertiary)
    (1.0, 0.0, 0.0),   # 4  red           (primary)
    (1.0, 0.0, 0.5),   # 5  red-violet    (tertiary)
    (1.0, 0.0, 1.0),   # 6  violet        (secondary)
    (0.5, 0.0, 1.0),   # 7  blue-violet   (tertiary)
    (0.0, 0.0, 1.0),   # 8  blue          (primary)
    (0.0, 0.5, 1.0),   # 9  blue-green    (tertiary)
    (0.0, 1.0, 1.0),   # 10 green         (secondary)
    (0.0, 1.0, 0.5),   # 11 yellow-green  (tertiary)
]
HUE_NAMES = ["YELLOW", "YELLOW-ORANGE", "ORANGE", "RED-ORANGE", "RED",
             "RED-VIOLET", "VIOLET", "BLUE-VIOLET", "BLUE", "BLUE-GREEN",
             "GREEN", "YELLOW-GREEN"]


def hue_ryb(t):
    """Position t in [0, 12) around the wheel -> RYB mixture (linear)."""
    t %= 12
    i = int(math.floor(t))
    f = t - i
    a, b = HUE_RYB[i], HUE_RYB[(i + 1) % 12]
    return tuple(a[k] + (b[k] - a[k]) * f for k in range(3))


def hue_rgb(i):
    return ryb_to_rgb(*HUE_RYB[i % 12])


def mix(c1, c2, t):
    return tuple(a + (b - a) * t for a, b in zip(c1, c2))


def luma(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def text_on(c):
    """Readable text colour (black or white) for background c."""
    return (1, 1, 1) if luma(c) < 0.62 else (0.1, 0.1, 0.1)


# --------------------------------------------------------------------------
# Small drawing helpers
# --------------------------------------------------------------------------
def pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def fill_poly(c, pts, fill, stroke=(1, 1, 1), lw=1.4):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    c.setFillColorRGB(*fill)
    c.setStrokeColorRGB(*stroke)
    c.setLineWidth(lw)
    c.drawPath(p, fill=1, stroke=1)


def ring_wedge(cx, cy, r_in, r_out, a0, a1, steps=24):
    """Polygon approximating an annular sector from angle a0 to a1 (deg)."""
    outer = [pol(cx, cy, r_out, a0 + (a1 - a0) * k / steps) for k in range(steps + 1)]
    inner = [pol(cx, cy, r_in, a1 + (a0 - a1) * k / steps) for k in range(steps + 1)]
    return outer + inner


def arc_text(c, text, cx, cy, base_r, mid_deg, font, size, color,
             inward=False, tracking=0.0):
    """
    Draw text along a circular arc, centred on angle mid_deg.
    inward=False -> glyph tops point away from the centre (read clockwise);
    inward=True  -> glyph tops point to the centre (read counter-clockwise),
                    which keeps text upright on the lower half of a wheel.
    base_r is the radius of the text baseline.
    """
    widths = [stringWidth(ch, font, size) + tracking for ch in text]
    total = sum(widths)
    pos = 0.0
    for ch, w in zip(text, widths):
        ang = (pos + w / 2.0) / base_r
        if not inward:
            theta = math.radians(mid_deg) + total / (2 * base_r) - ang
            rot = math.degrees(theta) - 90
        else:
            theta = math.radians(mid_deg) - total / (2 * base_r) + ang
            rot = math.degrees(theta) + 90
        c.saveState()
        c.translate(cx + base_r * math.cos(theta), cy + base_r * math.sin(theta))
        c.rotate(rot)
        c.setFillColorRGB(*color)
        c.setFont(font, size)
        c.drawCentredString(0, 0, ch)
        c.restoreState()
        pos += w


def arc_arrow(c, cx, cy, r, a_from, a_to, color=(0.35, 0.35, 0.35)):
    """Thin arc from a_from to a_to (deg) with an arrow head at a_to."""
    sgn = 1 if a_to > a_from else -1
    end = a_to - sgn * 4.5
    steps = 20
    pts = [pol(cx, cy, r, a_from + (end - a_from) * k / steps) for k in range(steps + 1)]
    c.setStrokeColorRGB(*color)
    c.setLineWidth(0.9)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, fill=0, stroke=1)
    tip = pol(cx, cy, r, a_to)
    back_o = pol(cx, cy, r + 3.2, end)
    back_i = pol(cx, cy, r - 3.2, end)
    c.setFillColorRGB(*color)
    q = c.beginPath()
    q.moveTo(*tip)
    q.lineTo(*back_o)
    q.lineTo(*back_i)
    q.close()
    c.drawPath(q, fill=1, stroke=0)


def swatch_row(c, cx_px, top_px, colors, w=29, h=15, gap=7, radius=3.5):
    total = len(colors) * w + (len(colors) - 1) * gap
    x0 = X(cx_px) - total / 2.0
    y0 = Y(top_px) - h
    for i, col in enumerate(colors):
        c.setFillColorRGB(*col)
        light = luma(col) > 0.93
        c.setStrokeColorRGB(0.55, 0.55, 0.55) if light else c.setStrokeColorRGB(*col)
        c.setLineWidth(0.6)
        c.roundRect(x0 + i * (w + gap), y0, w, h, radius, fill=1, stroke=1)


def para(c, text, cx_px, top_px, width_px, size=6.8, leading=8.4,
         font="Helvetica", color=(0.12, 0.12, 0.12), align="center"):
    """Wrapped paragraph; (cx, top) in layout px. Returns the last baseline y."""
    lines = simpleSplit(text, font, size, width_px * SX)
    y = Y(top_px) - size
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    for ln in lines:
        if align == "center":
            c.drawCentredString(X(cx_px), y, ln)
        else:
            c.drawString(X(cx_px), y, ln)
        y -= leading
    return y + leading


def heading(c, text, cx_px, y_px, size=8.4, align="center"):
    c.setFont("Helvetica-Bold", size)
    c.setFillColorRGB(0, 0, 0)
    if align == "center":
        c.drawCentredString(X(cx_px), Y(y_px), text)
    else:
        c.drawString(X(cx_px), Y(y_px), text)


# --------------------------------------------------------------------------
# The main RYB colour wheel
# --------------------------------------------------------------------------
def draw_ryb_wheel(c, cx, cy, R, segments=12):
    """
    Outer ring: `segments` hues sampled around the RYB wheel (12 = classic).
    Centre: Itten-style hexagon -- the primary triangle split in three kites,
    with a secondary-colour triangle on each side.
    Use segments=24/36/60 for a finer (even smooth-looking) ring; the
    tertiary labels are only drawn for the classic 12-hue ring.
    """
    r_in = 0.72 * R
    step = 360.0 / segments

    # --- outer ring ------------------------------------------------------
    for i in range(segments):
        rgb = ryb_to_rgb(*hue_ryb(i * 12.0 / segments))
        mid = 90 - step * i
        pts = ring_wedge(cx, cy, r_in, R, mid - step / 2, mid + step / 2)
        fill_poly(c, pts, rgb, stroke=(1, 1, 1), lw=1.6 if segments <= 12 else 0.4)

    # --- tertiary labels on the ring (12-hue wheel only) --------------------
    if segments == 12:
        mid_r = (r_in + R) / 2.0
        size = 5.4
        cap = size * 0.72
        for i in (1, 3, 5, 7, 9, 11):
            mid = 90 - 30 * i
            col = text_on(hue_rgb(i))
            line1, line2 = "TERTIARY", HUE_NAMES[i]
            upper = math.sin(math.radians(mid)) >= -1e-9   # top half (incl. 0 and 180 deg)
            if upper:
                arc_text(c, line1, cx, cy, mid_r + cap * 0.35, mid, "Helvetica-Bold", size, col, False, 0.5)
                arc_text(c, line2, cx, cy, mid_r - cap * 1.45, mid, "Helvetica-Bold", size, col, False, 0.5)
            else:
                arc_text(c, line1, cx, cy, mid_r - cap * 0.35, mid, "Helvetica-Bold", size, col, True, 0.5)
                arc_text(c, line2, cx, cy, mid_r + cap * 1.45, mid, "Helvetica-Bold", size, col, True, 0.5)

    # --- centre hexagon ----------------------------------------------------
    rh = r_in - 0.5
    Yv, Ov, Rv = pol(cx, cy, rh, 90), pol(cx, cy, rh, 30), pol(cx, cy, rh, -30)
    Vv, Bv, Gv = pol(cx, cy, rh, -90), pol(cx, cy, rh, -150), pol(cx, cy, rh, 150)
    C = (cx, cy)

    def mid(p, q):
        return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)

    mYB, mYR, mRB = mid(Yv, Bv), mid(Yv, Rv), mid(Rv, Bv)

    col_y, col_r, col_b = hue_rgb(0), hue_rgb(4), hue_rgb(8)
    col_o, col_v, col_g = hue_rgb(2), hue_rgb(6), hue_rgb(10)

    # secondary triangles (base = a side of the primary triangle)
    fill_poly(c, [Gv, Yv, Bv], col_g)
    fill_poly(c, [Ov, Yv, Rv], col_o)
    fill_poly(c, [Vv, Rv, Bv], col_v)
    # primary kites
    fill_poly(c, [Yv, mYB, C, mYR], col_y)
    fill_poly(c, [Rv, mYR, C, mRB], col_r)
    fill_poly(c, [Bv, mYB, C, mRB], col_b)

    def centroid(pts):
        return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)

    def label(pts, l1, l2, col, rot=0, size=7.4):
        gx, gy = centroid(pts)
        c.saveState()
        c.translate(gx, gy)
        c.rotate(rot)
        c.setFillColorRGB(*text_on(col))
        c.setFont("Helvetica-Bold", size)
        c.drawCentredString(0, 1.2, l1)
        c.drawCentredString(0, -size - 0.4, l2)
        c.restoreState()

    label([Yv, mYB, C, mYR], "PRIMARY", "YELLOW", col_y)
    label([Rv, mYR, C, mRB], "PRIMARY", "RED", col_r)
    label([Bv, mYB, C, mRB], "PRIMARY", "BLUE", col_b)
    # secondary labels run parallel to the side of the primary triangle
    label([Gv, Yv, Bv], "SECONDARY", "GREEN", col_g, rot=60)
    label([Ov, Yv, Rv], "SECONDARY", "ORANGE", col_o, rot=-60)
    label([Vv, Rv, Bv], "SECONDARY", "VIOLET", col_v, rot=0)

    # --- warm / cold indicators around the wheel ------------------------------
    rr = R + 13
    tick_a, tick_b = pol(cx, cy, R + 6, 90), pol(cx, cy, R + 21, 90)
    for ang in (90, 270):
        a = pol(cx, cy, R + 6, ang)
        b = pol(cx, cy, R + 21, ang)
        c.setStrokeColorRGB(0.35, 0.35, 0.35)
        c.setLineWidth(0.9)
        c.line(a[0], a[1], b[0], b[1])
    grey = (0.2, 0.2, 0.2)
    # top (text reads clockwise, tops outward)
    arc_text(c, "COLD", cx, cy, rr, 90 + 13, "Helvetica", 6.4, grey, False, 0.9)
    arc_text(c, "WARM", cx, cy, rr, 90 - 13, "Helvetica", 6.4, grey, False, 0.9)
    arc_arrow(c, cx, cy, rr + 2.5, 90 + 22, 90 + 40)
    arc_arrow(c, cx, cy, rr + 2.5, 90 - 22, 90 - 40)
    # bottom (upright: tops point to the centre)
    arc_text(c, "COLD", cx, cy, rr + 5, 270 - 13, "Helvetica", 6.4, grey, True, 0.9)
    arc_text(c, "WARM", cx, cy, rr + 5, 270 + 13, "Helvetica", 6.4, grey, True, 0.9)
    arc_arrow(c, cx, cy, rr + 2.5, 270 - 22, 270 - 40)
    arc_arrow(c, cx, cy, rr + 2.5, 270 + 22, 270 + 40)


# --------------------------------------------------------------------------
# Mini wheels for colour schemes
# --------------------------------------------------------------------------
def draw_mini_wheel(c, cx, cy, r, picks=None):
    r_in = r * 0.42
    for i in range(12):
        mid = 90 - 30 * i
        fill_poly(c, ring_wedge(cx, cy, r_in, r, mid - 15, mid + 15, steps=8),
                  hue_rgb(i), stroke=(1, 1, 1), lw=0.5)
    if picks:
        mr = (r + r_in) / 2.0
        pts = [pol(cx, cy, mr, 90 - 30 * i) for i in picks]
        c.setStrokeColorRGB(0.1, 0.1, 0.1)
        c.setLineWidth(0.9)
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        if len(pts) > 2:
            p.close()
        c.drawPath(p, fill=0, stroke=1)
        for (px, py) in pts:
            c.setFillColorRGB(1, 1, 1)
            c.setStrokeColorRGB(0.1, 0.1, 0.1)
            c.setLineWidth(0.7)
            c.circle(px, py, r * 0.085, fill=1, stroke=1)


def scheme_item(c, cx_px, cy_px, r_pt, picks, caption_lines, cap_dx=0):
    cx, cy = X(cx_px), Y(cy_px)
    draw_mini_wheel(c, cx, cy, r_pt, picks)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColorRGB(0, 0, 0)
    x = cx + r_pt + 6 + cap_dx
    y = cy + 3 * (len(caption_lines) - 1)
    for ln in caption_lines:
        c.drawString(x, y, ln)
        y -= 8


# --------------------------------------------------------------------------
# Page 1
# --------------------------------------------------------------------------
MEANINGS = [
    ("RED:", hue_rgb(4), "Passion, Love, Fire, Anger, Blood"),
    ("ORANGE:", hue_rgb(2), "Energy, Happiness, Vitality, Stimulation"),
    ("YELLOW:", (0.90, 0.72, 0.0), "Sunshine, Happiness, Hope, Deceit"),
    ("GREEN:", hue_rgb(10), "New Beginnings, Abundance, Nature"),
    ("BLUE:", hue_rgb(8), "Sky, Calm, Responsible, Sadness, Sea"),
    ("VIOLET:", hue_rgb(6), "Creativity, Royalty, Wealth, Ambition"),
    ("BLACK:", (0, 0, 0), "Mystery, Elegance, Evil, Death, Power"),
    ("GRAY:", (0.4, 0.4, 0.4), "Moody, Conservative, Formality"),
    ("WHITE:", (0.72, 0.72, 0.72), "Purity, Cleanliness, Virtue, Innocence"),
    ("BROWN:", (0.50, 0.32, 0.16), "Nature, Wholesomeness, Dependability"),
    ("TAN OR BEIGE:", (0.82, 0.62, 0.25), "Conservative, Piety, Dull"),
    ("CREAM OR IVORY:", (0.88, 0.80, 0.50), "Calm, Elegant, Purity"),
]


def build_page_1(c):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ---- title -------------------------------------------------------------
    c.saveState()          # keep the title's character spacing from leaking
    t = c.beginText()
    t.setFont("Helvetica-Oblique", 43)
    t.setCharSpace(1.2)
    title = "COLOUR THEORY"
    tw = stringWidth(title, "Helvetica-Oblique", 43) + 1.2 * (len(title) - 1)
    t.setTextOrigin(X(375) - tw / 2.0, Y(50))
    t.setFillColorRGB(0.05, 0.05, 0.05)
    t.textOut(title)
    c.drawText(t)
    c.restoreState()

    # ---- left column -----------------------------------------------------------
    LX, LW = 76, 140
    Yel, Red, Blu = hue_rgb(0), hue_rgb(4), hue_rgb(8)
    Ora, Gre, Vio = hue_rgb(2), hue_rgb(10), hue_rgb(6)

    swatch_row(c, LX, 16, [Yel, Red, Blu], w=34, gap=10)
    heading(c, "Primary Colours", LX, 52)
    para(c, "3 pigment colours that can not be mixed or formed by any combination "
            "of other colours. All other colours are derived from these 3 hues.",
         LX, 58, LW)

    swatch_row(c, LX, 136, [Ora, Gre, Vio], w=34, gap=10)
    heading(c, "Secondary Colours", LX, 173)
    para(c, "These are the colours formed by mixing two primary colours.", LX, 180, LW)

    swatch_row(c, LX, 226, [hue_rgb(1), hue_rgb(3), hue_rgb(5)], w=34, gap=10)
    swatch_row(c, LX, 249, [hue_rgb(7), hue_rgb(9), hue_rgb(11)], w=34, gap=10)
    heading(c, "Tertiary Colours", LX, 283)
    para(c, "These are the colours formed by mixing a primary and a secondary colour. "
            "That's why the hue is a two word name, such as blue-green, red-violet, "
            "and yellow-orange.", LX, 289, LW)

    swatch_row(c, LX, 388, [hue_rgb(11), hue_rgb(10), hue_rgb(9)], w=34, gap=10)
    heading(c, "Analogous", LX, 425)
    para(c, "Analogous colours sit next to one another on the colour wheel. "
            "These colours are in harmony with one another.", LX, 431, LW)

    swatch_row(c, LX, 495, [(1, 1, 1), (0.72, 0.72, 0.72), (0.05, 0.05, 0.05)], w=34, gap=10)
    para(c, "White, black and gray are considered to be neutral.", LX, 520, LW)

    # ---- right column -------------------------------------------------------------
    RX, RW = 669, 138
    base = hue_rgb(4)
    white, grey, black = (1, 1, 1), (0.5, 0.5, 0.5), (0, 0, 0)

    tints = [mix(base, white, k) for k in (0.0, 0.3, 0.6, 0.8)]
    tones = [mix(base, grey, k) for k in (0.0, 0.3, 0.55, 0.8)]
    shades = [mix(base, black, k) for k in (0.0, 0.3, 0.55, 0.8)]
    mono = [mix(base, white, 0.55), mix(base, white, 0.25), base, mix(base, black, 0.4)]

    swatch_row(c, RX, 16, tints, w=27, gap=5)
    heading(c, "Tint", RX, 50)
    para(c, "A tint describes a colour that is mixed with white.", RX, 56, RW)

    swatch_row(c, RX, 82, tones, w=27, gap=5)
    heading(c, "Tone", RX, 114)
    para(c, "A tone describes a colour that is mixed with grey.", RX, 120, RW)

    swatch_row(c, RX, 146, shades, w=27, gap=5)
    heading(c, "Shade", RX, 177)
    para(c, "A shade describes a colour that is mixed with black.", RX, 183, RW)

    swatch_row(c, RX, 212, mono, w=27, gap=5)
    heading(c, "Monochromatic", RX, 244)
    para(c, "The term monochrome refers to the use of one colour or various shades "
            "and tints of one colour in a single form.", RX, 250, RW)

    heading(c, "Meaning of Colour", RX, 306, size=8.2)
    c.setFont("Helvetica", 5.6)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawCentredString(X(RX), Y(315), "(Western Culture)")
    y = 331
    for lab, col, txt in MEANINGS:
        c.setFont("Helvetica-Bold", 6.2)
        c.setFillColorRGB(*col)
        c.drawCentredString(X(RX), Y(y), lab)
        c.setFont("Helvetica", 5.6)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.drawCentredString(X(RX), Y(y + 9), txt)
        y += 19.2

    # ---- cold / warm descriptions -----------------------------------------------------
    heading(c, "Cold Colours", 166, 99, size=7.6, align="left")
    para(c, "They give an impression of calm, and create a soothing impression. "
            "They remind us of cold water.", 166, 104, 98, size=6.2, leading=7.6,
         align="left")
    heading(c, "Warm Colours", 484, 82, size=7.6, align="left")
    para(c, "They are vivid and energetic, they are visually and emotionally exciting. "
            "They remind us of fire and heat.", 484, 87, 112, size=6.2, leading=7.6,
         align="left")

    # ---- the RYB colour wheel ------------------------------------------------------------
    draw_ryb_wheel(c, X(347), Y(265), 172, segments=12)

    # ---- complementary + colour schemes ----------------------------------------------------
    cx, cy = X(200), Y(418)
    draw_mini_wheel(c, cx, cy, 25, picks=[4, 10])
    heading(c, "Complementary", 212, 458, size=8, align="center")
    heading(c, "Colours", 212, 468, size=8, align="center")
    para(c, "Colours that are opposite each other on the colour wheel are considered "
            "to be complementary colours (example: red and green).",
         160, 473, 106, size=6.2, leading=7.6, align="left")
    para(c, "When put together, they appear more vivid then when apart.",
         160, 512, 106, size=6.2, leading=7.6, align="left")

    # two "vibrance" boxes: red inside green, green inside red
    gcol, rcol = hue_rgb(10), hue_rgb(4)
    for k, (outer, inner) in enumerate([(gcol, rcol), (rcol, gcol)]):
        bx, by = X(272), Y(478 + k * 27) - 21
        c.setFillColorRGB(*outer)
        c.roundRect(bx, by, 36, 21, 3, fill=1, stroke=0)
        c.setFillColorRGB(*inner)
        c.roundRect(bx + 10, by + 5, 16, 11, 2, fill=1, stroke=0)

    scheme_item(c, 345, 497, 24, [0, 4, 8], ["Triadic", "colour scheme"])
    scheme_item(c, 468, 493, 24, [1, 3, 7, 9], ["Rectangle (tetradic)", "colour scheme"])
    scheme_item(c, 366, 546, 24, [0, 5, 7], ["Split-Complementary", "colour scheme"])
    scheme_item(c, 497, 546, 24, [0, 3, 6, 9], ["Square", "colour scheme"])


# --------------------------------------------------------------------------
def main(out="colour_theory.pdf"):
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("Colour Theory")
    c.setAuthor("color_theory_poster.py")
    build_page_1(c)
    c.showPage()
    # build_page_2(c); c.showPage()   # <- add more pages here
    c.save()
    print("Saved", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "colour_theory.pdf")
