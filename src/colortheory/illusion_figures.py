"""Figures of the colour illusions, drawn from scratch as vector shapes.

A Figure is a list of shapes on a WIDTH x HEIGHT surface (origin at the top left). The same
list is written as SVG (for the Markdown document) or drawn on a ReportLab canvas (for the
PDF), so both show exactly the same picture. Figures carry no words, only the letters A and B,
and are shared by every language.

Some shapes belong to a layer, used by the interactive page (illusion_page.py) to help the eye:
"remove" is shown in the documents and hidden when the help is on; "aid" appears only with the
help; "guide" is shown in the documents and, in the page, only with the help. Colours are (r, g, b) tuples of floats in 0..1.
"""
import contextlib
import math

from colortheory.colour import hex_rgb, mix

WIDTH, HEIGHT = 480, 320

BLACK, WHITE = (0.0, 0.0, 0.0), (1.0, 1.0, 1.0)
AID = hex_rgb("D02028")                                             # help lines of the page


def grey(v):
    return (v, v, v)


def css(c):
    return "#%02x%02x%02x" % tuple(int(round(max(0.0, min(1.0, v)) * 255)) for v in c)


class Figure:
    def __init__(self, background=WHITE, width=WIDTH, height=HEIGHT):
        self.w, self.h = width, height
        self.shapes, self.tags, self._tag = [], [], None
        if background is not None:
            self.rect(0, 0, width, height, background)

    # ----------------------------------------------------------------- shapes
    @contextlib.contextmanager
    def layer(self, tag):
        """Shapes added inside belong to this layer (None, "remove", "aid" or "guide")."""
        previous, self._tag = self._tag, tag
        try:
            yield
        finally:
            self._tag = previous

    def _add(self, shape):
        self.shapes.append(shape)
        self.tags.append(self._tag)

    def poly(self, pts, fill=None, stroke=None, sw=1.0, closed=True):
        self._add(("poly", list(pts), fill, stroke, sw, closed))

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=1.0):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, sw)

    def line(self, x1, y1, x2, y2, colour=BLACK, sw=1.5):
        self.poly([(x1, y1), (x2, y2)], None, colour, sw, closed=False)

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=1.0, blink=None):
        """blink=(index, count, seconds): the shape disappears during its 1/count of the cycle
        (animated in SVG; the PDF shows the cycle at index 0)."""
        self._add(("circle", (cx, cy, r), fill, stroke, sw, blink))

    def text(self, x, y, s, size=20, colour=BLACK):
        """Short Latin label centred on (x, y)."""
        self._add(("text", (x, y), s, size, colour))

    # ---------------------------------------------------------------- outputs
    def svg(self, page=False):
        """SVG of the document figure; page=True keeps every layer, marked with a class."""
        out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
               % (self.w, self.h, self.w, self.h)]
        for s, tag in zip(self.shapes, self.tags):
            if tag == "aid" and not page:
                continue
            mark = ' class="t-%s"' % tag if page and tag else ""
            if s[0] == "poly":
                _, pts, fill, stroke, sw, closed = s
                d = "M" + " L".join("%.2f %.2f" % p for p in pts) + (" Z" if closed else "")
                out.append('<path d="%s" %s%s/>' % (d, _paint(fill, stroke, sw), mark))
            elif s[0] == "circle":
                _, (cx, cy, r), fill, stroke, sw, blink = s
                head = '<circle cx="%.2f" cy="%.2f" r="%.2f" %s%s' % (cx, cy, r, _paint(fill, stroke, sw), mark)
                if blink is None:
                    out.append(head + "/>")
                else:
                    k, n, seconds = blink
                    times = ";".join("%.4f" % (i / n) for i in range(n))
                    values = ";".join("0" if i == k else "1" for i in range(n))
                    out.append(head + '><animate attributeName="opacity" calcMode="discrete" dur="%gs" '
                               'repeatCount="indefinite" keyTimes="%s" values="%s"/></circle>'
                               % (seconds, times, values))
            else:
                _, (x, y), text, size, colour = s
                out.append('<text x="%.2f" y="%.2f" font-family="Helvetica, Arial, sans-serif" '
                           'font-weight="bold" font-size="%g" text-anchor="middle" fill="%s"%s>%s</text>'
                           % (x, y + size * 0.35, size, css(colour), mark, text))
        out.append("</svg>")
        return "\n".join(out) + "\n"

    def draw(self, c, x, y, width):
        """Draw on a ReportLab canvas: top-left corner at (x, y) in PDF points, scaled to width."""
        k = width / self.w
        c.saveState()
        c.translate(x, y)
        c.scale(k, -k)
        clip = c.beginPath()
        clip.rect(0, 0, self.w, self.h)
        c.clipPath(clip, stroke=0, fill=0)
        for s, tag in zip(self.shapes, self.tags):
            if tag == "aid":
                continue
            if s[0] == "poly":
                _, pts, fill, stroke, sw, closed = s
                path = c.beginPath()
                path.moveTo(*pts[0])
                for p in pts[1:]:
                    path.lineTo(*p)
                if closed:
                    path.close()
                _set_paint(c, fill, stroke, sw)
                c.drawPath(path, stroke=int(stroke is not None), fill=int(fill is not None))
            elif s[0] == "circle":
                _, (cx, cy, r), fill, stroke, sw, blink = s
                if blink is not None and blink[0] == 0:
                    continue
                _set_paint(c, fill, stroke, sw)
                c.circle(cx, cy, r, stroke=int(stroke is not None), fill=int(fill is not None))
            else:
                _, (tx, ty), text, size, colour = s
                c.saveState()
                c.translate(tx, ty + size * 0.35)
                c.scale(1, -1)
                c.setFillColorRGB(*colour)
                c.setFont("Helvetica-Bold", size)
                c.drawCentredString(0, 0, text)
                c.restoreState()
        c.restoreState()


def _paint(fill, stroke, sw):
    out = 'fill="%s"' % (css(fill) if fill is not None else "none")
    if stroke is not None:
        out += ' stroke="%s" stroke-width="%g"' % (css(stroke), sw)
    return out


def _set_paint(c, fill, stroke, sw):
    if fill is not None:
        c.setFillColorRGB(*fill)
    if stroke is not None:
        c.setStrokeColorRGB(*stroke)
        c.setLineWidth(sw)


def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def wedge(f, cx, cy, r0, r1, a0, a1, fill, steps=6):
    """Ring sector between radii r0 < r1 and angles a0 < a1 (degrees)."""
    angles = [a0 + (a1 - a0) * i / steps for i in range(steps + 1)]
    f.poly([polar(cx, cy, r1, a) for a in angles] + [polar(cx, cy, r0, a) for a in reversed(angles)], fill)


# ==========================================================================
# COLOUR
# ==========================================================================
def bezold():
    f = Figure(WHITE)
    red = hex_rgb("C8323C")
    for x0, stripe in ((20, BLACK), (250, WHITE)):
        f.rect(x0, 30, 210, 260, red)
        with f.layer("remove"):
            for k in range(13):
                f.rect(x0, 40 + k * 20, 210, 7, stripe)
    return f


SIMULTANEOUS_PATCH = grey(0.55)


def simultaneous_contrast():
    f = Figure(WHITE)
    for x0, y0, back, patch in ((20, 15, grey(0.12), SIMULTANEOUS_PATCH), (250, 15, grey(0.90), SIMULTANEOUS_PATCH),
                                (20, 170, hex_rgb("1E3FA8"), SIMULTANEOUS_PATCH),
                                (250, 170, hex_rgb("F2C318"), SIMULTANEOUS_PATCH)):
        with f.layer("remove"):
            f.rect(x0, y0, 210, 135, back)
        f.rect(x0 + 75, y0 + 40, 60, 55, patch)
    return f


CONSTANCY_TARGET = grey(0.56)


def color_constancy():
    """The same mosaic under warm and cool light; the marked tile is the same grey in both."""
    f = Figure(grey(0.15))
    tiles = ["B8402E", "E0C04A", "3E8E4F", "D9D4CC", "2F5FA6", "8C4A8F", "C96A28", "6BAFC0", "9A9A9A",
             "447A3A", "C84E6E", "F0E6C8", "5B4A9E", "B0B84A", "2E7F80", "D47F55"]
    for x0, light in ((20, (1.0, 0.82, 0.52)), (250, (0.55, 0.78, 1.0))):
        with f.layer("remove"):
            for k in range(16):
                row, col = divmod(k, 4)
                base = hex_rgb(tiles[k])
                f.rect(x0 + col * 52.5, 55 + row * 52.5, 52.5, 52.5, tuple(a * b for a, b in zip(base, light)))
        # the target is painted after the light: identical pixels on both sides
        f.rect(x0 + 52.5, 55 + 52.5, 52.5, 52.5, CONSTANCY_TARGET)
        with f.layer("remove"):
            f.circle(x0 + 105, 27, 14, light)
    return f


def chromostereopsis():
    f = Figure(BLACK)
    red, blue = (1.0, 0.0, 0.0), (0.0, 0.15, 1.0)
    for k, r in enumerate((120, 96, 72, 48, 24)):
        f.circle(140, 160, r, red if k % 2 == 0 else blue)
        if k % 2 == 0:
            f.circle(140, 160, r - 14, BLACK)
    for i in range(5):
        for j in range(8):
            colour = red if 1 <= i <= 3 and 2 <= j <= 5 else blue
            f.rect(290 + i * 34, 45 + j * 30, 22, 18, colour)
    return f


def afterimage():
    f = Figure(WHITE)
    f.rect(0, 0, 240, 320, grey(0.93))
    f.circle(120, 160, 92, (0.0, 0.75, 0.75))                       # cyan   -> red
    f.circle(120, 160, 62, (0.9, 0.1, 0.9))                         # magenta -> green
    f.circle(120, 160, 32, (0.15, 0.15, 0.9))                       # blue   -> yellow
    f.circle(120, 160, 5, BLACK)
    f.circle(360, 160, 5, BLACK)
    return f


LILAC, LILAC_GREY = (0.86, 0.52, 0.86), grey(0.75)


def lilac_chaser():
    f = Figure(LILAC_GREY)
    for k in range(12):
        x, y = polar(240, 160, 112, -90 + 30 * k)
        for r, t in ((27, 0.12), (24, 0.28), (21, 0.46), (18, 0.66), (15, 0.84), (12, 1.0)):
            f.circle(x, y, r, mix(LILAC_GREY, LILAC, t), blink=(k, 12, 1.2))
    f.line(228, 160, 252, 160, BLACK, 3)
    f.line(240, 148, 240, 172, BLACK, 3)
    return f


def _grating(f, x, y, size, vertical, back, bars=11):
    f.rect(x, y, size, size, back)
    w = size / (2 * bars - 1)
    for k in range(bars):
        if vertical:
            f.rect(x + 2 * k * w, y, w, size, BLACK)
        else:
            f.rect(x, y + 2 * k * w, size, w, BLACK)


def mccollough():
    f = Figure(grey(0.5))
    _grating(f, 40, 12, 140, False, (0.95, 0.05, 0.05))             # induction: red, horizontal
    _grating(f, 300, 12, 140, True, (0.05, 0.75, 0.15))             # induction: green, vertical
    for k, vertical in enumerate((False, True, True, False)):       # test: black and white
        row, col = divmod(k, 2)
        _grating(f, 160 + col * 80, 166 + row * 74, 72, vertical, WHITE, bars=8)
    return f


# ==========================================================================
# BRIGHTNESS AND CONTRAST
# ==========================================================================
CHECKER_LIGHT, CHECKER_DARK = 0.78, 0.468
CHECKER_SHADOW = CHECKER_DARK / CHECKER_LIGHT                       # light square in shadow == dark square
CHECKER_A, CHECKER_B = (1, 1), (3, 4)                               # (column, row) of the squares A and B


def _checker_shade(u, v):
    """Light reaching point (u, v) of the board, in squares: 1 lit, CHECKER_SHADOW in full shadow."""
    # a wide band falling from the cylinder, on the right, toward the lower left
    (x0, y0), (x1, y1), radius, soft = (3.35, 4.45), (6.0, 3.9), 1.2, 0.45
    dx, dy = x1 - x0, y1 - y0
    s = min(max(((u - x0) * dx + (v - y0) * dy) / (dx * dx + dy * dy), 0.0), 1.0)
    d = math.hypot(u - x0 - s * dx, v - y0 - s * dy)
    t = min(max((radius + soft - d) / soft, 0.0), 1.0)
    return 1.0 + (CHECKER_SHADOW - 1.0) * t * t * (3 - 2 * t)


def checker_square(col, row):
    base = CHECKER_LIGHT if (col + row) % 2 else CHECKER_DARK
    return grey(base * _checker_shade(col + 0.5, row + 0.5))


def checker_shadow(proof=False):
    f = Figure(WHITE)
    n, size, x0, y0, sub = 6, 50, 90, 10, 12
    for col in range(n):
        for row in range(n):
            base = CHECKER_LIGHT if (col + row) % 2 else CHECKER_DARK
            x, y = x0 + col * size, y0 + row * size
            corners = {_checker_shade(col + a / 4, row + b / 4) for a in range(5) for b in range(5)}
            f.rect(x, y, size, size, grey(base * _checker_shade(col + 0.5, row + 0.5)))
            if len(corners) == 1:
                continue                                    # evenly lit: one flat square
            step = size / sub
            for i in range(sub):                            # the soft edge of the shadow
                for j in range(sub):
                    k = _checker_shade(col + (i + .5) / sub, row + (j + .5) / sub)
                    f.rect(x + i * step, y + j * step, min(step + .6, size - i * step),
                           min(step + .6, size - j * step), grey(base * k))
    centre = {}
    for name, (col, row) in (("A", CHECKER_A), ("B", CHECKER_B)):
        # a flat square on top, so the compared areas are exactly one grey
        f.rect(x0 + col * size + 2, y0 + row * size + 2, size - 4, size - 4, checker_square(col, row))
        centre[name] = (x0 + (col + .5) * size, y0 + (row + .5) * size)
    (ax, ay), (bx, by) = centre["A"], centre["B"]
    length = math.hypot(bx - ax, by - ay)
    nx, ny = -(by - ay) / length * 11, (bx - ax) / length * 11
    with f.layer(None if proof else "aid"):                         # a strip joining A and B
        f.poly([(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)],
               grey(CHECKER_DARK))
    for name, (x, y) in centre.items():
        f.text(x, y, name, 22, BLACK)
    # the cylinder that casts the shadow
    cx, top, bottom, rx = 90 + 5.35 * size, 150, 265, 34
    green, dark = hex_rgb("4F9A63"), hex_rgb("2E6B42")
    f.poly([(cx - rx, top), (cx + rx, top), (cx + rx, bottom), (cx - rx, bottom)], green)
    for fill, y in ((dark, bottom), (hex_rgb("7FC291"), top)):
        f.poly([(cx + rx * math.cos(math.radians(a)), y + 12 * math.sin(math.radians(a))) for a in range(0, 360, 10)],
               fill)
    return f


WHITE_GREY = grey(0.5)


def white_illusion():
    f = Figure(WHITE)
    with f.layer("remove"):
        for k in range(0, 16, 2):
            f.rect(20, k * 20, 440, 20, BLACK)
    for k in range(4, 12, 2):
        f.rect(80, k * 20, 110, 20, WHITE_GREY)                     # on a black stripe
        f.rect(290, (k + 1) * 20, 110, 20, WHITE_GREY)              # on a white stripe
    return f


def munker():
    """Munker-White: the same red looks orange or purple-pink between yellow and blue stripes."""
    f = Figure(WHITE)
    yellow, blue, red = (1.0, 0.9, 0.1), (0.1, 0.25, 0.85), (0.9, 0.2, 0.3)
    with f.layer("remove"):
        for k in range(40):
            f.rect(0, k * 8, 480, 8, blue if k % 2 == 0 else yellow)
    for k in range(10, 30, 2):
        f.rect(70, k * 8, 120, 8, red)                              # replaces blue stripes
        f.rect(290, (k + 1) * 8, 120, 8, red)                       # replaces yellow stripes
    return f


def mach_bands():
    f = Figure(WHITE)
    for k in range(8):
        f.rect(k * 60, 0, 60.5, 320, grey(0.16 + 0.1 * k))
    with f.layer("aid"):                                            # separate the bands
        for k in range(1, 8):
            f.rect(k * 60 - 8, 0, 16, 320, WHITE)
    return f


def cornsweet():
    """Two halves of the same grey separated by a light-to-dark edge."""
    base = 0.55
    f = Figure(grey(base))
    width, amp = 90, 0.22
    for i in range(-width, width):
        d = (width - abs(i + 0.5)) / width
        sign = 1 if i < 0 else -1
        f.rect(240 + i, 0, 1.5, 320, grey(base + sign * amp * d * d))
    with f.layer("aid"):                                            # hide the edge
        f.rect(240 - width, 0, 2 * width + 1.5, 320, WHITE)
    return f


def hermann_grid():
    f = Figure(BLACK)
    for k in range(5):
        f.rect(0, 40 + k * 56, 480, 13, WHITE)
    for k in range(8):
        f.rect(30 + k * 58, 0, 13, 320, WHITE)
    return f


def scintillating_grid():
    f = Figure(BLACK)
    ys, xs = [24 + k * 45 for k in range(7)], [20 + k * 49 for k in range(10)]
    for y in ys:
        f.rect(0, y - 5, 480, 10, grey(0.5))
    for x in xs:
        f.rect(x - 5, 0, 10, 320, grey(0.5))
    for x in xs:
        for y in ys:
            f.circle(x, y, 7.5, WHITE)
    return f


def ehrenstein():
    """Lines that stop short of their crossings: a bright disc seems to sit on each gap."""
    f = Figure(WHITE)
    for i in range(8):
        x = 30 + i * 60
        for j in range(6):
            f.line(x, j * 60 - 17, x, j * 60 + 17, BLACK, 2.5)
    for j in range(5):
        y = 30 + j * 60
        for i in range(9):
            f.line(i * 60 - 17, y, i * 60 + 17, y, BLACK, 2.5)
    with f.layer("aid"):                                            # complete the lines
        for i in range(8):
            f.line(30 + i * 60, 0, 30 + i * 60, 320, BLACK, 2.5)
        for j in range(5):
            f.line(0, 30 + j * 60, 480, 30 + j * 60, BLACK, 2.5)
    return f


def irradiation():
    f = Figure(WHITE)
    f.rect(0, 0, 240, 320, BLACK)
    f.rect(70, 110, 100, 100, WHITE)
    f.rect(310, 110, 100, 100, BLACK)
    with f.layer("aid"):
        for y in (110, 210):
            f.line(30, y, 450, y, AID, 2)
    return f


# ==========================================================================
# SIZE AND LENGTH
# ==========================================================================
def ebbinghaus():
    f = Figure(WHITE)
    orange, blue = hex_rgb("E8702A"), hex_rgb("4A78B8")
    for cx, ring_n, ring_r, dist in ((130, 6, 38, 82), (355, 9, 11, 43)):
        f.circle(cx, 160, 27, orange)
        for k in range(ring_n):
            x, y = polar(cx, 160, dist, 360 * k / ring_n)
            f.circle(x, y, ring_r, blue)
    with f.layer("aid"):                                            # parallels touching both centres
        for y in (160 - 27, 160 + 27):
            f.line(60, y, 425, y, AID, 2)
    return f


def muller_lyer():
    f = Figure(WHITE)
    for y, direction in ((80, 1), (165, -1)):
        f.line(110, y, 370, y, BLACK, 4)
        with f.layer("remove"):
            for x, s in ((110, 1), (370, -1)):
                for up in (-26, 26):
                    f.line(x, y, x + 30 * s * direction, y + up, BLACK, 4)
    red = hex_rgb("D03030")
    with f.layer("guide"):                                          # both shafts span the same
        for x in (110, 370):
            for y in range(215, 290, 12):
                f.line(x, y, x, y + 5, red, 1.5)
        f.line(110, 255, 370, 255, red, 4)
    return f


def ponzo():
    f = Figure(WHITE)
    with f.layer("remove"):
        for k in range(11):                                         # sleepers, closer toward the horizon
            t = (k / 10) ** 1.6
            y, half = 40 + 270 * t, 24 + 170 * t
            f.line(240 - half, y, 240 + half, y, grey(0.6), 1 + 5 * t)
        for s in (-1, 1):
            f.line(240 + s * 14, 10, 240 + s * 190, 320, grey(0.25), 6)
    yellow = hex_rgb("F0B400")
    for y in (90, 240):
        f.rect(180, y - 7, 120, 14, yellow)
    return f


# ==========================================================================
# DISTORTED LINES
# ==========================================================================
def cafe_wall():
    mortar = grey(0.5)
    f = Figure(mortar)
    tile, h, gap = 48, 34, 3
    shifts = (0, 12, 24, 12)
    for row in range(9):
        y = row * (h + gap)
        x = -2 * tile + shifts[row % 4]
        k = 0
        while x < 480:
            f.rect(x, y, tile, h, BLACK if k % 2 == 0 else WHITE)
            x += tile
            k += 1
    with f.layer("aid"):                                            # the mortar lines are straight
        for row in range(1, 9):
            f.line(0, row * (h + gap) - gap / 2, 480, row * (h + gap) - gap / 2, AID, 2)
    return f


def fraser_spiral():
    f = Figure(grey(0.78))
    cx, cy = 240, 160
    # background: a spiralling checker pattern
    radii = [14 * 1.22 ** k for k in range(14)]
    for i in range(len(radii) - 1):
        for s in range(36):
            if (s + i) % 2:
                continue
            a = s * 10 + i * 7
            f.poly([polar(cx, cy, radii[i], a), polar(cx, cy, radii[i + 1], a + 7),
                    polar(cx, cy, radii[i + 1], a + 17), polar(cx, cy, radii[i], a + 10)], grey(0.45))
    # concentric circles made of tilted black and white strands
    for r in (36, 62, 90, 120, 152):
        n = int(round(2 * math.pi * r / 17))
        step = 360 / n
        for s in range(n):
            a = s * step
            colour = BLACK if s % 2 == 0 else WHITE
            f.poly([polar(cx, cy, r - 6, a), polar(cx, cy, r - 1, a), polar(cx, cy, r + 6, a + step * 1.25),
                    polar(cx, cy, r + 1, a + step * 1.25)], colour)
    with f.layer("aid"):                                            # they are circles
        for r in (36, 62, 90, 120, 152):
            f.circle(cx, cy, r, None, AID, 3)
    return f


def _spokes(f, cx, cy, n, length, colour=BLACK, sw=1.2):
    for k in range(n):
        x1, y1 = polar(cx, cy, length, 180 * k / n)
        f.line(2 * cx - x1, 2 * cy - y1, x1, y1, colour, sw)


def hering():
    f = Figure(WHITE)
    with f.layer("remove"):
        _spokes(f, 240, 160, 30, 330)
    for x in (185, 295):
        f.line(x, 12, x, 308, AID, 5)
    return f


def wundt():
    """The opposite of Hering: two fans centred outside the lines, which seem to bow inward."""
    f = Figure(WHITE)
    with f.layer("remove"):
        for cx in (40, 440):
            _spokes(f, cx, 160, 30, 420)
    for x in (185, 295):
        f.line(x, 12, x, 308, AID, 5)
    return f


def orbison():
    f = Figure(WHITE)
    with f.layer("remove"):
        for r in range(14, 330, 15):
            f.circle(180, 120, r, None, grey(0.35), 1.2)
    red = hex_rgb("D02028")
    f.rect(180, 80, 170, 170, None, red, 4.5)
    return f


def zollner():
    f = Figure(WHITE)
    for k in range(-2, 6):
        x0, y0 = k * 80 + 10, 330                                   # long line at 45 degrees
        f.line(x0, y0, x0 + 340, y0 - 340, BLACK, 4)
        with f.layer("remove"):
            for t in range(10, 340, 24):
                x, y = x0 + t, y0 - t
                if k % 2 == 0:
                    f.line(x - 17, y, x + 17, y, BLACK, 3)
                else:
                    f.line(x, y - 17, x, y + 17, BLACK, 3)
    return f


def poggendorff(proof=False):
    f = Figure(WHITE)
    slope = 0.62

    def y_at(x):
        return 250 - slope * (x - 60)

    f.line(60, y_at(60), 190, y_at(190), BLACK, 3.5)
    f.line(290, y_at(290), 420, y_at(420), BLACK, 3.5)
    blue = hex_rgb("2060C0")
    f.line(290, y_at(290) + 34, 420, y_at(420) + 34, blue, 3.5)     # a decoy below
    if not proof:
        with f.layer("remove"):
            f.rect(190, 20, 100, 280, grey(0.72), BLACK, 2)
    with f.layer(None if proof else "aid"):                         # the hidden part of the line
        f.line(190, y_at(190), 290, y_at(290), AID, 2)
        f.rect(190, 20, 100, 280, None, grey(0.5), 2)
    return f


def tilt():
    """Tilt illusion: the vertical grating in each disc, inside gratings tilted opposite ways."""
    f = Figure(grey(0.5))

    def stripes(cx, cy, radius, angle, period=18):
        a = math.radians(angle)
        ux, uy = math.sin(a), -math.cos(a)                          # along the stripes
        vx, vy = math.cos(a), math.sin(a)                           # across them
        x = -radius
        while x < radius:
            x1, x2 = max(x, -radius), min(x + period / 2, radius)
            pts = []
            for i in range(9):
                v = x1 + (x2 - x1) * i / 8
                u = math.sqrt(max(radius * radius - v * v, 0))
                pts.append((cx + v * vx + u * ux, cy + v * vy + u * uy))
            for i in range(8, -1, -1):
                v = x1 + (x2 - x1) * i / 8
                u = math.sqrt(max(radius * radius - v * v, 0))
                pts.append((cx + v * vx - u * ux, cy + v * vy - u * uy))
            f.poly(pts, BLACK)
            x += period

    for cx, angle in ((130, 15), (350, -15)):
        with f.layer("remove"):                                     # the surround
            f.circle(cx, 160, 100, WHITE)
            stripes(cx, 160, 100, angle)
        f.circle(cx, 160, 46, grey(0.5))
        f.circle(cx, 160, 43, WHITE)
        stripes(cx, 160, 43, 0)
    return f


# ==========================================================================
# MOTION
# ==========================================================================
DRIFT_STEPS = (BLACK, hex_rgb("2B5CD6"), WHITE, hex_rgb("E8D21D"))  # dark -> light, repeated


def illusory_motion():
    """Rings of black, blue, white and yellow blocks; neighbouring rings run opposite ways."""
    f = Figure(grey(0.6))
    for cx, cy, flip in ((120, 85, 1), (360, 85, -1), (120, 235, -1), (360, 235, 1)):
        for k, (r0, r1) in enumerate(((52, 74), (32, 52), (16, 32), (4, 16))):
            direction = flip if k % 2 == 0 else -flip
            units = (14, 11, 8, 5)[k]
            offset = k * 9
            for u in range(units):
                span = 360 / units
                parts = ((0.0, 0.2), (0.2, 0.5), (0.5, 0.7), (0.7, 1.0))
                for colour, (p0, p1) in zip(DRIFT_STEPS, parts):
                    a0, a1 = u + p0, u + p1
                    if direction < 0:
                        a0, a1 = u + 1 - p1, u + 1 - p0
                    wedge(f, cx, cy, r0, r1, offset + a0 * span, offset + a1 * span + .3, colour, 3)
    return f


def peripheral_drift():
    """Sawtooth grey ramps around a ring."""
    f = Figure(grey(0.65))
    for cx in (125, 355):
        direction = 1 if cx < 240 else -1
        for k, (r0, r1) in enumerate(((78, 108), (45, 75), (14, 42))):
            cycles, steps = (12, 9, 6)[k], 8
            for c in range(cycles):
                for s in range(steps):
                    a0 = (c + s / steps) * 360 / cycles
                    a1 = (c + (s + 1) / steps) * 360 / cycles + .4
                    level = s / (steps - 1)
                    if direction * (1 if k % 2 == 0 else -1) < 0:
                        level = 1 - level
                    wedge(f, cx, 160, r0, r1, a0, a1, grey(level), 2)
    return f


# ==========================================================================
# FIGURE, GROUND AND IMPOSSIBLE OBJECTS
# ==========================================================================
def _spline(points, steps=8):
    """Catmull-Rom curve through points."""
    out = []
    pts = [points[0]] + list(points) + [points[-1]]
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1:i + 3]
        for s in range(steps):
            t = s / steps
            out.append(tuple(.5 * (2 * b + (c - a) * t + (2 * a - 5 * b + 4 * c - d) * t * t
                                   + (3 * b - a - 3 * c + d) * t ** 3) for a, b, c, d in zip(p0, p1, p2, p3)))
    out.append(points[-1])
    return out


def rubin_vase():
    f = Figure(hex_rgb("1B1B2F"))
    # half-width of the vase from top to bottom: forehead, nose, lips, chin and neck of the two faces
    profile = [(110, 14), (96, 40), (74, 70), (66, 100), (70, 118), (56, 138), (30, 166), (28, 174), (48, 182),
               (46, 190), (34, 200), (50, 209), (38, 220), (52, 230), (48, 248), (68, 262), (74, 280),
               (96, 296), (120, 306)]
    right = _spline([(240 + dx, y) for dx, y in profile])
    left = [(480 - x, y) for x, y in reversed(right)]
    f.poly(right + left, hex_rgb("F4F1E8"))
    return f


# face polygons of the tribar in distances (u, v, w) to the three sides, u + v + w = 9
_N = 9
TRIBAR_FACE = [(0, _N - 1, 1), (0, 1, _N - 1), (1, 0, _N - 1), (1, 1, _N - 2), (_N - 3, 1, 2), (_N - 4, 2, 2), (1, 2, _N - 3), (1, _N - 2, 1)]


def penrose_triangle():
    f = Figure(WHITE)
    top, left, right = (240, 18), (75, 18 + 165 * math.sqrt(3)), (405, 18 + 165 * math.sqrt(3))

    def point(u, v, w):
        return tuple((u * a + v * b + w * c) / _N for a, b, c in zip(top, left, right))

    face = TRIBAR_FACE
    for colour in (hex_rgb("E4572E"), hex_rgb("F3A712"), hex_rgb("2E86AB")):
        f.poly([point(*p) for p in face], colour, BLACK, 2.5)
        face = [(w, u, v) for u, v, w in face]                      # turn by 120 degrees
    return f
