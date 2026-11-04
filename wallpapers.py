#!/usr/bin/env python3
"""
wallpapers.py
-------------
Abstract wallpapers for desktops (landscape) and phones (portrait), in the most
common screen sizes, with the colour schemes of colour theory (the RYB palettes
of tilings.py):

  - mesh:     soft blobs of colour melting into each other (mesh gradient);
  - aurora:   curtains of light over a dark sky;
  - waves:    layers of paper-cut waves, each casting a soft shadow;
  - ribbons:  twisting silk ribbons made of fine coloured threads;
  - fluid:    liquid paint, folded by domain warping, glossy and striated;
  - silk:     folds of satin with soft highlights;
  - orbs:     overlapping spheres with gradients and a rim of light;
  - trails:   long exposure arcs of glowing light.

Every picture is drawn from a seed, so the same options give the same picture.

    pip install numpy scipy pillow
    python3 wallpapers.py ribbons                         # -> wallpaper_ribbons_fhd_1.png
    python3 wallpapers.py fluid --size 4k --scheme triad --hue blue -o fluid.png
    python3 wallpapers.py waves --size iphone --seed 7 -o waves.jpg
    python3 wallpapers.py orbs --size 2560x1080 --background black
    python3 wallpapers.py mesh --count 5                  # five pictures, seeds 1 .. 5
    python3 wallpapers.py --gallery                       # every style side by side
    python3 wallpapers.py --show                          # preview window
    python3 wallpapers.py --list                          # styles, sizes and parameters
"""
import argparse
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

import i18n
import tilings as tl

WHITE, BLACK = (1.0, 1.0, 1.0), (0.0, 0.0, 0.0)


# ==========================================================================
# 1. SCREEN SIZES
# ==========================================================================
SIZES = {
    # desktops and laptops (landscape)
    "hd": (1366, 768), "hd+": (1600, 900), "fhd": (1920, 1080), "wuxga": (1920, 1200),
    "qhd": (2560, 1440), "wqxga": (2560, 1600), "4k": (3840, 2160), "5k": (5120, 2880),
    "ultrawide": (2560, 1080), "uwqhd": (3440, 1440), "macbook-air": (2560, 1664),
    "macbook-pro": (3024, 1964), "imac": (4480, 2520),
    # phones (portrait)
    "phone-hd": (720, 1280), "phone-fhd": (1080, 1920), "android": (1080, 2400),
    "android-qhd": (1440, 3200), "iphone-se": (750, 1334), "iphone-13": (1170, 2532),
    "iphone": (1179, 2556), "iphone-pro-max": (1290, 2796),
    # tablets (portrait; --orientation landscape turns them)
    "ipad": (1640, 2360), "ipad-pro": (2048, 2732), "tablet": (1600, 2560),
}
SIZE_GROUPS = [("g_desktop", ["hd", "hd+", "fhd", "wuxga", "qhd", "wqxga", "4k", "5k", "ultrawide", "uwqhd",
                              "macbook-air", "macbook-pro", "imac"]),
               ("g_phone", ["phone-hd", "phone-fhd", "android", "android-qhd", "iphone-se", "iphone-13",
                            "iphone", "iphone-pro-max"]),
               ("g_tablet", ["ipad", "ipad-pro", "tablet"])]


def parse_size(text, orientation=None):
    """'fhd', 'iphone' or '2560x1080'; orientation 'landscape' or 'portrait' turns it if needed."""
    t = str(text).lower().strip()
    if t in SIZES:
        w, h = SIZES[t]
    else:
        try:
            w, h = (int(x) for x in t.split("x"))
        except ValueError:
            raise SystemExit("unknown size %r (see --list)" % text)
    if (orientation == "landscape" and h > w) or (orientation == "portrait" and w > h):
        w, h = h, w
    return w, h


# ==========================================================================
# 2. COLOURS, NOISE AND HELPERS
# ==========================================================================
def ramp(cols, t):
    """Colour ramp through cols (a list of RGB) for t in 0 .. 1 (any shape)."""
    c = np.asarray(cols, float)
    xs = np.linspace(0, 1, len(c))
    t = np.clip(t, 0, 1)
    return np.stack([np.interp(t, xs, c[:, k]) for k in range(3)], -1)


def luma(c):
    return .299 * c[0] + .587 * c[1] + .114 * c[2]


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


class Noise:
    """Fractal value noise: periodic random grids sampled with cubic splines."""

    def __init__(self, rng, n=64, layers=8):
        self.n = n
        self.grids = [ndimage.spline_filter(rng.random((n, n)), order=3, mode="grid-wrap")
                      for _ in range(layers)]

    def __call__(self, x, y, octaves=4, layer=0):
        """fbm in 0 .. 1 (roughly); x, y in grid cells (one cell = one bump)."""
        total, amp, f, norm = 0.0, 1.0, 1.0, 0.0
        for o in range(octaves):
            g = self.grids[(layer + o) % len(self.grids)]
            total = total + amp * ndimage.map_coordinates(g, [np.asarray(y) * f + 17.3 * o,
                                                              np.asarray(x) * f + 31.7 * o],
                                                          order=3, mode="grid-wrap", prefilter=False)
            norm += amp
            amp *= .5
            f *= 2.0
        return total / norm


def grid(W, H, max_px):
    """Pixel centres of a working grid of at most max_px pixels, with the aspect of
    W x H; coordinates in picture heights (y from 0 at the top to 1 at the bottom)."""
    s = min(1.0, math.sqrt(max_px / float(W * H)))
    w, h = max(2, int(round(W * s))), max(2, int(round(H * s)))
    u = (np.arange(w) + .5) / h
    v = (np.arange(h) + .5) / h
    return np.meshgrid(u, v)


def background(spec):
    b = spec["background"]
    base = tl.ryb_hue(spec["hue"])
    if b == "dark":
        return tl.mix(base, BLACK, .9)
    if b == "light":
        return tl.mix(base, WHITE, .9)
    if b == "black":
        return (.02, .02, .025)
    if b == "white":
        return (.97, .97, .96)
    return tl.hexc(b.lstrip("#"))


def gradient_bg(spec, u, v, rng):
    """The background, a little lighter on one side."""
    bg = np.array(background(spec))
    a = rng.uniform(0, 2 * math.pi)
    t = (u * math.cos(a) + v * math.sin(a))
    t = (t - t.min()) / (np.ptp(t) or 1)
    light = tl.mix(tuple(bg), WHITE if luma(bg) < .5 else BLACK, .12)
    return ramp([tuple(bg), light], t)


def to_image(arr):
    return Image.fromarray((np.clip(arr, 0, 1) * 255 + .5).astype(np.uint8), "RGB")


def from_image(img):
    return np.asarray(img, dtype=np.float32) / 255.0


def blur(arr, radius):
    """Gaussian blur of a float RGB array in 0 .. 1 (through Pillow, which is fast)."""
    if radius <= 0:
        return arr
    return from_image(to_image(arr).filter(ImageFilter.GaussianBlur(radius)))


def bezier(pts, n):
    """Points (n x 2) of a cubic Bezier curve and its unit normals."""
    p = np.asarray(pts, float)
    t = np.linspace(0, 1, n)[:, None]
    c = ((1 - t) ** 3) * p[0] + 3 * ((1 - t) ** 2) * t * p[1] + 3 * (1 - t) * t * t * p[2] + t ** 3 * p[3]
    d = 3 * ((1 - t) ** 2) * (p[1] - p[0]) + 6 * (1 - t) * t * (p[2] - p[1]) + 3 * t * t * (p[3] - p[2])
    d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-9
    return c, np.stack([-d[:, 1], d[:, 0]], 1)


def sweep_curve(rng, A, wobble=.35):
    """Control points of a curve that crosses the picture (A = width / height) from one
    side to the other, along the longer side."""
    if A >= 1:
        p0 = (-.25, rng.uniform(.1, .9))
        p3 = (A + .25, rng.uniform(.1, .9))
        p1 = (rng.uniform(.1, .5) * A, rng.uniform(-wobble, 1 + wobble))
        p2 = (rng.uniform(.5, .9) * A, rng.uniform(-wobble, 1 + wobble))
    else:
        p0 = (rng.uniform(.1, .9) * A, -.25)
        p3 = (rng.uniform(.1, .9) * A, 1.25)
        p1 = (rng.uniform(-wobble, 1 + wobble) * A, rng.uniform(.1, .5))
        p2 = (rng.uniform(-wobble, 1 + wobble) * A, rng.uniform(.5, .9))
    return [p0, p1, p2, p3]


# ==========================================================================
# 3. STYLES
# ==========================================================================
# Each style is f(spec, W, H, rng, noise, cols, p) -> float RGB array (any size with
# the aspect W x H; it is resized to W x H afterwards). p holds its parameters.
def mesh(spec, W, H, rng, noise, cols, p):
    u, v = grid(W, H, 300_000)
    A = W / H
    k = int(p["blobs"])
    warp = float(p["warp"])
    x = u + warp * (noise(u * 1.5, v * 1.5, 3, 0) - .5)
    y = v + warp * (noise(u * 1.5, v * 1.5, 3, 1) - .5)
    num = np.zeros(u.shape + (3,))
    den = np.zeros(u.shape)
    for i in range(k):
        cx, cy = rng.uniform(-.15, A + .15), rng.uniform(-.15, 1.15)
        r = rng.uniform(.3, .65) * float(p["spread"]) * min(A, 1) ** .6
        w = np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (r * r)) + 1e-6
        num += w[..., None] * np.array(cols[i % len(cols)])
        den += w
    return num / den[..., None]


def aurora(spec, W, H, rng, noise, cols, p):
    u, v = grid(W, H, 1_200_000)
    bg = gradient_bg(spec, u, v, rng)
    light = np.zeros(u.shape + (3,))
    n = int(p["bands"])
    xs = u[0]
    for i in range(n):
        base = rng.uniform(.25, .8)
        amp = rng.uniform(.08, .22)
        f = rng.uniform(.6, 1.6)
        yc = base + amp * 2 * (noise(xs * f + 10 * i, np.full_like(xs, 3.7 * i), 3, i) - .5)
        d = v - yc[None, :]
        up = rng.uniform(.12, .35)
        down = rng.uniform(.015, .04)
        inten = np.where(d < 0, np.exp(d / up), np.exp(-(d / down) ** 2))
        rays = .55 + .45 * noise(u * 28 + 5 * i, np.full_like(u, 1.3 * i), 2, i + 3)
        inten *= rays ** float(p["rays"]) * rng.uniform(.6, 1.0)
        light += inten[..., None] * np.array(cols[i % len(cols)])
    out = bg + (1 - bg) * (1 - np.exp(-1.6 * light))
    stars = (rng.random(u.shape) > 1 - .0006 * float(p["stars"])) * rng.random(u.shape)
    return np.clip(out + stars[..., None] * (1 - v[..., None]), 0, 1)


def waves(spec, W, H, rng, noise, cols, p):
    u, v = grid(W, H, 4_000_000)
    A = W / H
    n = int(p["layers"])
    px = u.shape[0]                      # pixels per picture height
    light = max(cols, key=luma)
    sky = ramp([tl.mix(light, WHITE, .35), light], v)
    out = sky.copy()
    xs = u[0]
    order = list(range(n))
    seq = [cols[i % len(cols)] for i in range(len(cols))]
    seq = sorted(seq, key=luma, reverse=True) if p["sort"] else seq
    for k in order:
        top = .12 + .8 * (k / max(n - 1, 1)) ** .9
        amp = float(p["height"]) * rng.uniform(.5, 1.2)
        f = rng.uniform(.8, 2.2) / max(A, 1)
        yk = top + amp * 2 * (noise(xs * f + 7 * k, np.full_like(xs, 2.3 * k), 4, k) - .5)
        d = v - yk[None, :]
        shadow = np.where(d < 0, np.exp(d / float(p["shadow"])), 0.0)
        out *= 1 - .6 * shadow[..., None]
        c = np.array(ramp(seq, k / max(n - 1, 1)))
        rim = np.exp(-np.maximum(d, 0) / .05)
        body = np.exp(-np.maximum(d, 0) / .25)      # each layer darkens away from its crest
        fill = c * (.6 + .35 * body[..., None] + .35 * rim[..., None])
        cover = np.clip(d * px + .5, 0, 1)[..., None]
        out = out * (1 - cover) + fill * cover
    return out


def _ribbon(img, rng, cols, A, H, ss, p, width, twists):
    """One twisting ribbon: its soft shadow, then its threads as filled strips side by side
    (no gaps between them, so nothing breaks up where the ribbon narrows in a twist)."""
    n = 600
    pts, nrm = bezier(sweep_curve(rng, A), n)
    t = np.linspace(0, 1, n)
    phase = rng.uniform(0, 2 * math.pi) + twists * 2 * math.pi * t
    w = width * (.3 + .7 * np.sin(math.pi * t) ** .6)
    face = np.cos(phase)                           # > 0 front of the ribbon, < 0 its back
    k = H * ss                                     # picture units -> pixels
    span = rng.uniform(.5, 1.0)
    off = rng.uniform(0, 1 - span)
    hi = rng.uniform(.2, .8)
    lines = int(p["threads"])
    tex = float(p["texture"])
    shade = rng.random(lines)

    edge = np.abs(w * face)[:, None] * nrm / 2
    poly = np.concatenate([pts + edge, (pts - edge)[::-1]]) + np.array([.012, .025])
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).polygon([tuple(q) for q in poly * k], fill=140)
    mask = mask.filter(ImageFilter.GaussianBlur(k * .018))
    img.paste((0, 0, 0), (0, 0), mask)

    draw = ImageDraw.Draw(img)
    edges = [(pts + ((j / lines - .5) * w * face)[:, None] * nrm) * k for j in range(lines + 1)]
    gloss = np.abs(face)
    step = 2
    for j in range(lines):
        s = (j + .5) / lines
        base = np.array(ramp(cols, off + span * s))
        fibre = 1 - tex * (.18 * shade[j] + .1 * (j % 2))            # neighbouring threads differ a little
        light = (.42 + .5 * gloss + .4 * np.exp(-((s - hi) / .1) ** 2) * gloss ** 3) * fibre
        light = np.where(face < 0, light * .78, light)
        rgb = np.clip(base[None, :] * light[:, None], 0, 1)
        a_, b_ = edges[j], edges[j + 1]
        for a in range(0, n - 1, step):
            b = min(a + step, n - 1)
            quad = [tuple(z) for z in a_[a:b + 1]] + [tuple(z) for z in b_[b:a - 1 if a else None:-1]]
            c = tuple(int(255 * x) for x in rgb[a])
            draw.polygon(quad, fill=c, outline=c)


def ribbons(spec, W, H, rng, noise, cols, p):
    ss = 2 if W * H <= 9_000_000 else 1
    A = W / H
    u, v = grid(W, H, 400_000)
    img = to_image(gradient_bg(spec, u, v, rng)).resize((W * ss, H * ss), Image.BICUBIC)
    for r in range(int(p["ribbons"])):
        _ribbon(img, rng, cols, A, H, ss, p, float(p["width"]) * min(A, 1) * rng.uniform(.7, 1.3),
                float(p["twist"]) * rng.uniform(.6, 1.4))
    return from_image(img.resize((W, H), Image.LANCZOS))


def trails(spec, W, H, rng, noise, cols, p):
    ss = 2 if W * H <= 9_000_000 else 1
    A = W / H
    u, v = grid(W, H, 300_000)
    bg = gradient_bg(spec, u, v, rng)
    lay = Image.new("RGB", (W * ss, H * ss), (0, 0, 0))
    d = ImageDraw.Draw(lay)
    k = H * ss
    cx, cy = rng.choice([-.1, A + .1]), rng.uniform(.7, 1.3)
    a0 = math.atan2(.5 - cy, A / 2 - cx)
    n = int(p["lines"])
    r0 = rng.uniform(.5, .9) * max(A, 1)
    for i in range(n):
        s = i / max(n - 1, 1)
        r = r0 * (.55 + .9 * s + rng.normal(0, .02))
        span = rng.uniform(.6, 1.0) * float(p["sweep"])
        start = a0 - span / 2 + rng.normal(0, .08)
        th = np.linspace(start, start + span, 400)
        grow = 1 + float(p["spiral"]) * (th - start)
        x = cx + r * grow * np.cos(th)
        y = cy + r * grow * np.sin(th)
        c = np.array(ramp(cols, (s + rng.normal(0, .08)) % 1.0)) * rng.uniform(.35, 1.0)
        fade = np.sin(np.linspace(0, math.pi, len(th))) ** .7
        lw = max(1, int(round(ss * rng.choice([1, 1, 1, 2, 2, 3]) * H / 1080)))
        for a in range(0, len(th) - 1, 8):
            col = tuple(int(255 * z) for z in np.clip(c * fade[a], 0, 1))
            d.line([(x[b] * k, y[b] * k) for b in range(a, min(a + 9, len(th)))], fill=col, width=lw)
    arr = from_image(lay.resize((W, H), Image.LANCZOS))
    glow = .8 * blur(arr, H * .004) + .7 * blur(arr, H * .025)
    base = from_image(to_image(bg).resize((W, H), Image.BICUBIC))
    return base + (1 - base) * (1 - np.exp(-2.2 * (arr + glow)))


def fluid(spec, W, H, rng, noise, cols, p):
    u, v = grid(W, H, 1_500_000)
    f = float(p["scale"])
    x, y = u * f, v * f
    w = float(p["warp"])
    qx, qy = noise(x, y, 4, 0), noise(x + 5.2, y + 1.3, 4, 1)
    rx = noise(x + w * qx + 1.7, y + w * qy + 9.2, 4, 2)
    ry = noise(x + w * qx + 8.3, y + w * qy + 2.8, 4, 3)
    fld = noise(x + w * rx, y + w * ry, 4, 4)
    t = fld + .6 * (rx - .5)
    t = (t - np.percentile(t, 1)) / (np.percentile(t, 99) - np.percentile(t, 1) + 1e-9)
    col = ramp(cols, t)
    if float(p["lines"]):
        bands = (.5 + .5 * np.cos(t * 2 * math.pi * float(p["bands"]))) ** 6
        col *= 1 - float(p["lines"]) * bands[..., None]
    gy, gx = np.gradient(t * float(p["relief"]) * u.shape[0] / 60)
    nz = 1 / np.sqrt(gx * gx + gy * gy + 1)
    nx, ny = -gx * nz, -gy * nz
    L = np.array([-.5, -.6, .62])
    L /= np.linalg.norm(L)
    diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    hx, hy, hz = L[0], L[1], L[2] + 1                # half vector to a viewer straight above
    hn = math.sqrt(hx * hx + hy * hy + hz * hz)
    spec_ = np.clip((nx * hx + ny * hy + nz * hz) / hn, 0, 1) ** 40
    return col * (.55 + .55 * diff[..., None]) + float(p["gloss"]) * spec_[..., None]


def silk(spec, W, H, rng, noise, cols, p):
    u, v = grid(W, H, 1_500_000)
    bg = np.array(background(spec))
    f = float(p["scale"])
    a = rng.uniform(0, math.pi)
    along = u * math.cos(a) + v * math.sin(a)       # folds run along this direction
    across = -u * math.sin(a) + v * math.cos(a)
    x, y = along * .35 * f, across * 1.4 * f
    qx, qy = noise(x, y, 3, 0), noise(x + 3.1, y + 7.7, 3, 1)
    fld = noise(x + .8 * qx, y + .8 * qy, 3, 2) + .5 * across
    hgt = np.sin(fld * 2 * math.pi * float(p["folds"]))       # the cloth: a height field of folds
    gy, gx = np.gradient(hgt * u.shape[0] / 40 * float(p["depth"]))
    nz = 1 / np.sqrt(gx * gx + gy * gy + 1)
    nx, ny = -gx * nz, -gy * nz
    L = np.array([-.4, -.7, .6])
    L /= np.linalg.norm(L)
    diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1) ** float(p["softness"])
    hv = L + np.array([0, 0, 1])
    hv /= np.linalg.norm(hv)
    sheen = np.clip(nx * hv[0] + ny * hv[1] + nz * hv[2], 0, 1) ** 30
    tone = noise(u * .6, v * .6, 2, 5)
    tone = (tone - tone.min()) / (np.ptp(tone) + 1e-9)
    c = ramp(cols, tone)
    out = bg[None, None, :] * (1 - diff[..., None]) + c * diff[..., None]
    return out + float(p["sheen"]) * sheen[..., None] * (.6 + .4 * c)


def orbs(spec, W, H, rng, noise, cols, p):
    u, v = grid(W, H, 6_000_000)
    A = W / H
    px = u.shape[0]
    out = gradient_bg(spec, u, v, rng)
    n = int(p["orbs"])
    discs = sorted(((rng.uniform(-.1, A + .1), rng.uniform(-.1, 1.1), rng.uniform(.18, .55) * float(p["size"]) * min(A, 1) ** .7)
                    for _ in range(n)), key=lambda d: -d[2])
    la = rng.uniform(0, 2 * math.pi)
    for i, (cx, cy, r) in enumerate(discs):
        d = np.sqrt((u - cx) ** 2 + (v - cy) ** 2)
        sd = np.sqrt((u - cx - .02) ** 2 + (v - cy - .035) ** 2)
        shadow = 1 - smoothstep(r - .06, r + .1, sd)
        out *= 1 - .5 * shadow[..., None]
        ga = la + rng.normal(0, .4)
        t = ((u - cx) * math.cos(ga) + (v - cy) * math.sin(ga)) / (2 * r) + .5
        c1 = cols[i % len(cols)]
        c2 = tl.mix(c1, cols[(i + 1) % len(cols)], .5)
        fill = ramp([tl.mix(c1, BLACK, .55), c1, c2, tl.mix(c2, WHITE, .35)], t)
        if p["rings"]:
            fill *= (.92 + .08 * np.cos(d / r * 2 * math.pi * float(p["rings"])))[..., None]
        ang = np.arctan2(v - cy, u - cx)
        rim = np.exp(-((d - r) * px / 2.0) ** 2) * np.clip(np.cos(ang - la - math.pi), 0, 1)
        cover = np.clip((r - d) * px + .5, 0, 1)[..., None] * float(p["opacity"])
        out = out * (1 - cover) + fill * cover
        out += rim[..., None] * np.array(tl.mix(c2, WHITE, .6)) * .8
    return out


# --------------------------------------------------------------------------
# Recolouring an existing picture (style "image", with --input)
# --------------------------------------------------------------------------
def rgb_to_hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn
    h = np.zeros_like(mx)
    safe = np.where(d > 1e-9, d, 1)
    h = np.where(mx == r, ((g - b) / safe) % 6, h)
    h = np.where(mx == g, (b - r) / safe + 2, h)
    h = np.where(mx == b, (r - g) / safe + 4, h)
    h = np.where(d > 1e-9, h / 6.0, 0)
    s = np.where(mx > 1e-9, d / np.where(mx > 1e-9, mx, 1), 0)
    return np.stack([h % 1.0, s, mx], -1)


def hsv_to_rgb(a):
    h, s, v = a[..., 0] % 1.0, a[..., 1], a[..., 2]
    i = np.floor(h * 6).astype(int) % 6
    f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    choices = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]
    out = np.zeros(a.shape)
    for k, (r, g, b) in enumerate(choices):
        m = i == k
        out[..., 0] = np.where(m, r, out[..., 0])
        out[..., 1] = np.where(m, g, out[..., 1])
        out[..., 2] = np.where(m, b, out[..., 2])
    return out


def dominant_hue(hsv):
    """The main hue of a picture (0 .. 1): mean angle of the hues, weighted by how
    saturated and bright each pixel is."""
    w = hsv[..., 1] * hsv[..., 2]
    ang = hsv[..., 0] * 2 * math.pi
    return (math.atan2((w * np.sin(ang)).sum(), (w * np.cos(ang)).sum()) / (2 * math.pi)) % 1.0


def nearest_ryb(h):
    """The RYB hue (0 .. 11) whose colour has the HSV hue closest to h."""
    def gap(k):
        hk = rgb_to_hsv(np.array(tl.ryb_hue(k), float))[0]
        return min(abs(hk - h), 1 - abs(hk - h))
    return min(range(12), key=gap)


def fit_image(img, W, H, fit):
    """cover: fill W x H and crop the overflow; contain: the whole picture over a blurred
    copy of itself; stretch: change the proportions."""
    w, h = img.size
    if fit == "stretch":
        return img.resize((W, H), Image.LANCZOS)
    k = max(W / w, H / h)
    big = img.resize((max(W, round(w * k)), max(H, round(h * k))), Image.LANCZOS)
    x, y = (big.width - W) // 2, (big.height - H) // 2
    cover = big.crop((x, y, x + W, y + H))
    if fit == "cover":
        return cover
    k = min(W / w, H / h)
    small = img.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)
    back = cover.filter(ImageFilter.GaussianBlur(max(W, H) * .03))
    back = Image.eval(back, lambda c: int(c * .7))
    back.paste(small, ((W - small.width) // 2, (H - small.height) // 2))
    return back


def recolour(spec, W, H, rng, noise, cols, p):
    img = fit_image(Image.open(spec["input"]).convert("RGB"), W, H, p["fit"])
    arr = from_image(img).astype(float)
    hsv = rgb_to_hsv(arr)
    mode = p["mode"]
    if spec["hue"] is not None and mode in ("shift", "tint"):
        target = rgb_to_hsv(np.array(tl.ryb_hue(spec["hue"]), float))[0]
        if mode == "shift":               # turn every hue by the same angle: the variety stays
            hsv[..., 0] = (hsv[..., 0] + target - dominant_hue(hsv)) % 1.0
        else:                             # one hue for everything, saturation and value kept
            hsv[..., 0] = target
    hsv[..., 1] = np.clip(hsv[..., 1] * float(p["saturation"]), 0, 1)
    hsv[..., 2] = np.clip(hsv[..., 2] * float(p["brightness"]), 0, 1)
    out = hsv_to_rgb(hsv)
    if mode == "map":                     # gradient map: lightness through the colour scheme
        lum = .299 * out[..., 0] + .587 * out[..., 1] + .114 * out[..., 2]
        lo, hi = np.percentile(lum, 1), np.percentile(lum, 99.5)
        lum = (lum - lo) / (hi - lo + 1e-9)          # use the whole ramp, even on a dark picture
        stops = sorted(cols, key=luma)
        stops = [tl.mix(stops[0], BLACK, .8)] + stops + [tl.mix(stops[-1], WHITE, .7)]
        out = ramp(stops, lum)
    return out


STYLES = {
    "mesh": (mesh, {"blobs": 8, "warp": .35, "spread": .8},
             dict(scheme="sweep", hue=3, background="dark", grain=.025)),
    "aurora": (aurora, {"bands": 4, "rays": 1.5, "stars": 1.0},
               dict(scheme="analogous", hue=9, background="black", grain=.02)),
    "waves": (waves, {"layers": 7, "height": .16, "shadow": .04, "sort": 1},
              dict(scheme="ramp", hue=7, background="dark", grain=.02)),
    "ribbons": (ribbons, {"ribbons": 3, "threads": 90, "width": .32, "twist": .8, "texture": .9},
                dict(scheme="rainbow", hue=5, background="dark", grain=.015)),
    "fluid": (fluid, {"scale": .7, "warp": 2.5, "lines": .18, "bands": 18, "relief": 1.0, "gloss": .35},
              dict(scheme="split", hue=9, background="dark", grain=.015)),
    "silk": (silk, {"scale": 1.0, "folds": 3.0, "depth": 3.0, "softness": 1.3, "sheen": .7},
             dict(scheme="mono", hue=8, background="black", grain=.02)),
    "orbs": (orbs, {"orbs": 5, "size": 1.0, "opacity": .92, "rings": 0},
             dict(scheme="analogous", hue=8, background="dark", grain=.02)),
    "trails": (trails, {"lines": 160, "sweep": 2.2, "spiral": .12},
               dict(scheme="sweep", hue=2, background="black", grain=.015)),
    "image": (recolour, {"mode": "shift", "fit": "cover", "saturation": 1.0, "brightness": 1.0},
              dict(scheme="ramp", hue=None, background="dark", grain=0.0, vignette=0.0, size="source")),
}
STYLE_KEYS = [k for k in STYLES if k != "image"]       # "image" needs a picture (--input)
IMAGE_MODES = ["shift", "tint", "map"]
FITS = ["cover", "contain", "stretch"]


def size_of(s):
    """The size of a spec in pixels; 'source' is the size of its input picture."""
    if s["size"] == "source":
        if not s.get("input"):
            raise SystemExit("size 'source' needs a picture (--input)")
        w, h = Image.open(s["input"]).size
        return parse_size("%dx%d" % (w, h), s["orientation"])
    return parse_size(s["size"], s["orientation"])


# ==========================================================================
# 4. RENDERING
# ==========================================================================
def spec_defaults(spec):
    fn, params, defaults = STYLES[spec["style"]]
    s = dict(colours=None, seed=1, size="fhd", orientation=None, vignette=.25, input=None)
    s.update(defaults)
    s.update({k: v for k, v in spec.items() if v is not None})
    if s["style"] == "image" and not s["input"]:
        raise SystemExit("the style 'image' needs a picture: --input <file>")
    ps = dict(params)
    for k, val in (spec.get("params") or {}).items():
        if k not in ps:
            raise SystemExit("unknown parameter %r for %s (see --list)" % (k, spec["style"]))
        ps[k] = val
    s["params"] = ps
    return s


def render(spec, W=None, H=None):
    """The wallpaper of a spec as a Pillow image (W x H, by default the spec's size)."""
    s = spec_defaults(spec)
    if W is None:
        W, H = size_of(s)
    fn, _, _ = STYLES[s["style"]]
    rng = np.random.default_rng(int(s["seed"]))
    noise = Noise(np.random.default_rng(int(s["seed"]) + 1000))
    cols = tl.palette(s["scheme"], s["hue"] if s["hue"] is not None else 2, 6, s["colours"])
    arr = fn(s, W, H, rng, noise, cols, s["params"])
    if arr.shape[:2] != (H, W):
        arr = from_image(to_image(arr).resize((W, H), Image.LANCZOS))
    arr = np.asarray(arr, dtype=np.float32)
    if float(s["vignette"]):
        yy, xx = np.ogrid[:H, :W]
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
        arr *= (1 - float(s["vignette"]) * smoothstep(.45, 1.0, r))[..., None]
    if float(s["grain"]):                 # grain is per pixel: lighter on small pictures
        arr += np.random.default_rng(int(s["seed"]) + 7).normal(0, float(s["grain"]) * min(1.0, H / 1080.0), (H, W, 1)).astype(np.float32)
    return to_image(arr)


def default_name(s):
    if s["style"] == "image":
        stem = os.path.splitext(os.path.basename(s["input"]))[0]
        hue = "same" if s["hue"] is None else tl.HUE_KEYS[s["hue"] % 12]
        w, h = size_of(s)
        return "%s_%s_%dx%d.png" % (stem, hue, w, h)
    return "wallpaper_%s_%s_%d.png" % (s["style"], s["size"], s["seed"])


def save(img, path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        img.save(path, quality=95, subsampling=0)
    elif ext == ".webp":
        img.save(path, quality=95)
    else:
        img.save(path)


def caption(spec):
    s = spec_defaults(spec)
    if s["style"] == "image":
        mode = s["params"]["mode"]
        name = os.path.basename(s["input"])
        if mode == "map":
            return "%s  ·  %s  ·  %s" % (name, T("m_map"), scheme_label(s))
        hue = T("hue_keep") if s["hue"] is None else hue_names()[s["hue"] % 12].lower()
        return "%s  ·  %s  ·  %s" % (name, T("m_" + mode), hue)
    return "%s  ·  %s" % (T("st_" + s["style"]), scheme_label(s))


def scheme_label(s):
    return T("own_colours") if s["colours"] else tl.scheme_name(dict(s, hue=s["hue"] or 0))


def hue_names():
    return tl.CTD_STRINGS.get(tl._LANG, tl.CTD_STRINGS["en"])["hue_names"]


def _font(size):
    """A font for the captions, with the letters of the language in use."""
    for name in (i18n.font_file(tl._LANG), "arial.ttf", "DejaVuSans.ttf", "Helvetica.ttc"):
        try:
            return i18n.pil_font(name, size)
        except (OSError, TypeError, AttributeError):
            continue
    return ImageFont.load_default()


def gallery(specs, path, cols=4, width=480, labels=True):
    """Small versions of several wallpapers side by side, each with a caption."""
    W, H = size_of(spec_defaults(specs[0]))
    w = width
    h = int(round(w * H / W))
    pad, lab = 16, (34 if labels else 0)
    rows = (len(specs) + cols - 1) // cols
    sheet = Image.new("RGB", (pad + cols * (w + pad), pad + rows * (h + lab + pad)), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    font = _font(15)
    for i, sp in enumerate(specs):
        x = pad + (i % cols) * (w + pad)
        y = pad + (i // cols) * (h + lab + pad)
        sheet.paste(render(sp, w, h), (x, y))
        if labels:
            text = caption(sp)
            while font.getlength(i18n.visual(text)) > w and len(text) > 4:
                text = text[:-2]
            text = i18n.visual(text)          # Arabic: joined letters, right-aligned
            tx = x + w - font.getlength(text) if i18n.rtl() else x
            d.text((tx, y + h + 8), text, fill=(60, 60, 60), font=font)
    save(sheet, path)


# ==========================================================================
# 5. PREVIEW WINDOW
# ==========================================================================
def run_preview(spec):
    import tkinter as tk
    from tkinter import filedialog, ttk
    from PIL import ImageTk

    root = tk.Tk()
    root.title(T("app_title"))
    s = spec_defaults(spec)
    hues = list(hue_names()) + [T("hue_keep")]
    sizes = ["source"] + [k for _, ks in SIZE_GROUPS for k in ks]
    styles = STYLE_KEYS + ["image"]
    source = {"input": s["input"]}
    vars_ = {
        "style": tk.StringVar(value=s["style"]),
        "size": tk.StringVar(value=s["size"]),
        "scheme": tk.StringVar(value=s["scheme"]),
        "hue": tk.StringVar(value=hues[-1] if s["hue"] is None else hues[s["hue"] % 12]),
        "background": tk.StringVar(value=s["background"]),
        "seed": tk.IntVar(value=int(s["seed"])),
        "params": tk.StringVar(value=" ".join("%s=%s" % kv for kv in (spec.get("params") or {}).items())),
    }
    bar = ttk.Frame(root, padding=6)
    bar.pack(side="top", fill="x")
    view = ttk.Label(root)
    view.pack(side="top", padx=6, pady=6)
    status = ttk.Label(root, padding=(6, 0, 6, 6))
    status.pack(side="top", fill="x")
    state = {"spec": None, "photo": None, "job": None}

    def current():
        params = {}
        for item in vars_["params"].get().split():
            if "=" in item:
                k, val = item.split("=", 1)
                params[k] = tl.parse_value(val)
        return {"style": vars_["style"].get(), "size": vars_["size"].get(), "scheme": vars_["scheme"].get(),
                "hue": None if vars_["hue"].get() == hues[-1] else hues.index(vars_["hue"].get()),
                "background": vars_["background"].get(), "seed": vars_["seed"].get(), "params": params,
                "colours": s["colours"], "orientation": s["orientation"], "input": source["input"]}

    def redraw():
        state["job"] = None
        sp = current()
        try:
            W, H = size_of(spec_defaults(sp))
            k = min(960 / W, 640 / H)
            img = render(sp, max(2, int(W * k)), max(2, int(H * k)))
        except (SystemExit, ValueError, OSError) as e:
            status.config(text=str(e))
            return
        state["spec"] = sp
        state["photo"] = ImageTk.PhotoImage(img)
        view.config(image=state["photo"])
        status.config(text="%s  ·  %d x %d  ·  %s %d" % (caption(sp), W, H, T("app_seed").lower(), sp["seed"]))

    def changed(*_):
        if state["job"]:
            root.after_cancel(state["job"])
        state["job"] = root.after(250, redraw)

    def style_changed(*_):
        st = STYLES[vars_["style"].get()][2]
        vars_["scheme"].set(st["scheme"])
        vars_["hue"].set(hues[-1] if st["hue"] is None else hues[st["hue"]])
        vars_["background"].set(st["background"])
        if vars_["style"].get() == "image":
            vars_["size"].set("source")
            vars_["params"].set("mode=shift fit=cover saturation=1.0 brightness=1.0")
        else:
            if vars_["size"].get() == "source":
                vars_["size"].set("fhd")
            vars_["params"].set("")
        changed()

    def open_image():
        path = filedialog.askopenfilename(filetypes=[(T("app_images"), "*.png *.jpg *.jpeg *.webp *.avif *.bmp *.tif *.tiff"),
                                                     ("*", "*.*")])
        if path:
            source["input"] = path
            vars_["style"].set("image")
            style_changed()

    def new_seed():
        vars_["seed"].set(int(np.random.default_rng().integers(1, 100000)))

    def save_full():
        sp = state["spec"] or current()
        out = spec.get("output")                  # -o on the command line: the name offered here
        name = os.path.basename(out) if out else default_name(spec_defaults(sp))
        folder = os.path.dirname(os.path.abspath(out)) if out else os.getcwd()
        path = filedialog.asksaveasfilename(initialdir=folder, initialfile=name, defaultextension=".png",
                                            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("WebP", "*.webp")])
        if path:
            status.config(text=T("app_saving"))
            root.update()
            save(render(sp), path)
            status.config(text=T("app_saved") % os.path.abspath(path))
            print("wrote", os.path.abspath(path))

    def combo(label, var, values, width):
        ttk.Label(bar, text=T(label)).pack(side="left", padx=(6, 2))
        cb = ttk.Combobox(bar, textvariable=var, values=values, width=width, state="readonly")
        cb.pack(side="left")
        return cb

    combo("app_style", vars_["style"], styles, 9).bind("<<ComboboxSelected>>", style_changed)
    combo("app_size", vars_["size"], sizes, 13)
    combo("app_scheme", vars_["scheme"], tl.SCHEMES, 12)
    combo("app_hue", vars_["hue"], hues, 18)
    combo("app_background", vars_["background"], ["dark", "black", "light", "white"], 7)
    ttk.Label(bar, text=T("app_seed")).pack(side="left", padx=(6, 2))
    ttk.Spinbox(bar, from_=1, to=99999, textvariable=vars_["seed"], width=6).pack(side="left")
    ttk.Button(bar, text=T("app_random"), command=new_seed).pack(side="left", padx=4)
    bar2 = ttk.Frame(root, padding=(6, 0, 6, 0))
    bar2.pack(side="top", fill="x", before=view)
    ttk.Label(bar2, text=T("app_params")).pack(side="left", padx=(6, 2))
    ent = ttk.Entry(bar2, textvariable=vars_["params"], width=60)
    ent.pack(side="left", fill="x", expand=True)
    ttk.Button(bar2, text=T("app_open"), command=open_image).pack(side="left", padx=(6, 0))
    ttk.Button(bar2, text=T("app_save"), command=save_full).pack(side="left", padx=6)
    if s["style"] == "image" and not spec.get("params"):
        vars_["params"].set(" ".join("%s=%s" % kv for kv in s["params"].items()))
    for key, var in vars_.items():
        var.trace_add("write", changed)
    redraw()
    root.mainloop()


# ==========================================================================
# 6. TEXT (en, pt, es)
# ==========================================================================
STRINGS = {
    "en": {
        "st_mesh": "Mesh gradient", "st_aurora": "Aurora", "st_waves": "Layered waves",
        "st_ribbons": "Silk ribbons", "st_fluid": "Liquid paint", "st_silk": "Satin folds",
        "st_orbs": "Orbs", "st_trails": "Light trails", "st_image": "Your picture",
        "d_image": "a picture of yours (--input), with a new hue and size",
        "hue_keep": "(keep)", "m_shift": "hues turned", "m_tint": "one hue", "m_map": "gradient map",
        "app_open": "Open picture...", "app_images": "Pictures",
        "d_mesh": "soft blobs of colour melting into each other",
        "d_aurora": "curtains of light over a dark sky",
        "d_waves": "paper-cut layers of waves, each casting a shadow",
        "d_ribbons": "twisting ribbons of fine coloured threads",
        "d_fluid": "liquid paint folded by domain warping, glossy, with fine striations",
        "d_silk": "folds of satin with soft highlights",
        "d_orbs": "overlapping spheres with gradients and a rim of light",
        "d_trails": "long exposure arcs of glowing light",
        "g_desktop": "desktop (landscape)", "g_phone": "phone (portrait)", "g_tablet": "tablet (portrait)",
        "own_colours": "own colours", "styles": "styles", "sizes": "sizes",
        "app_title": "Wallpapers", "app_style": "Style", "app_size": "Size", "app_scheme": "Scheme",
        "app_hue": "Hue", "app_background": "Background", "app_seed": "Seed", "app_random": "Random",
        "app_params": "Parameters", "app_save": "Save full size...", "app_saving": "Rendering at full size...",
        "app_saved": "Saved %s",
    },
    "pt": {
        "st_mesh": "Gradiente difuso", "st_aurora": "Aurora", "st_waves": "Ondas em camadas",
        "st_ribbons": "Fitas de seda", "st_fluid": "Tinta líquida", "st_silk": "Pregas de cetim",
        "st_orbs": "Esferas", "st_trails": "Rastos de luz", "st_image": "A sua imagem",
        "d_image": "uma imagem sua (--input), com novo matiz e novo tamanho",
        "hue_keep": "(manter)", "m_shift": "matizes rodados", "m_tint": "um só matiz", "m_map": "mapa de degradê",
        "app_open": "Abrir imagem...", "app_images": "Imagens",
        "d_mesh": "manchas suaves de cor que se fundem umas nas outras",
        "d_aurora": "cortinas de luz sobre um céu escuro",
        "d_waves": "camadas de ondas recortadas em papel, cada uma com a sua sombra",
        "d_ribbons": "fitas torcidas feitas de fios de cor finos",
        "d_fluid": "tinta líquida dobrada por deformação do domínio, brilhante, com estrias finas",
        "d_silk": "pregas de cetim com reflexos suaves",
        "d_orbs": "esferas sobrepostas com degradês e um contorno de luz",
        "d_trails": "arcos de luz em longa exposição",
        "g_desktop": "computador (horizontal)", "g_phone": "telemóvel (vertical)", "g_tablet": "tablet (vertical)",
        "own_colours": "cores próprias", "styles": "estilos", "sizes": "tamanhos",
        "app_title": "Wallpapers", "app_style": "Estilo", "app_size": "Tamanho", "app_scheme": "Esquema",
        "app_hue": "Matiz", "app_background": "Fundo", "app_seed": "Semente", "app_random": "Aleatório",
        "app_params": "Parâmetros", "app_save": "Guardar em tamanho real...",
        "app_saving": "A desenhar em tamanho real...", "app_saved": "Guardado em %s",
    },
    "es": {
        "st_mesh": "Degradado difuso", "st_aurora": "Aurora", "st_waves": "Olas en capas",
        "st_ribbons": "Cintas de seda", "st_fluid": "Pintura líquida", "st_silk": "Pliegues de satén",
        "st_orbs": "Esferas", "st_trails": "Estelas de luz", "st_image": "Su imagen",
        "d_image": "una imagen suya (--input), con nuevo matiz y nuevo tamaño",
        "hue_keep": "(mantener)", "m_shift": "matices girados", "m_tint": "un solo matiz", "m_map": "mapa de degradado",
        "app_open": "Abrir imagen...", "app_images": "Imágenes",
        "d_mesh": "manchas suaves de color que se funden unas con otras",
        "d_aurora": "cortinas de luz sobre un cielo oscuro",
        "d_waves": "capas de olas recortadas en papel, cada una con su sombra",
        "d_ribbons": "cintas retorcidas hechas de hilos de color finos",
        "d_fluid": "pintura líquida plegada por deformación del dominio, brillante, con estrías finas",
        "d_silk": "pliegues de satén con reflejos suaves",
        "d_orbs": "esferas superpuestas con degradados y un borde de luz",
        "d_trails": "arcos de luz en larga exposición",
        "g_desktop": "ordenador (horizontal)", "g_phone": "móvil (vertical)", "g_tablet": "tableta (vertical)",
        "own_colours": "colores propios", "styles": "estilos", "sizes": "tamaños",
        "app_title": "Fondos de pantalla", "app_style": "Estilo", "app_size": "Tamaño", "app_scheme": "Esquema",
        "app_hue": "Matiz", "app_background": "Fondo", "app_seed": "Semilla", "app_random": "Aleatorio",
        "app_params": "Parámetros", "app_save": "Guardar a tamaño real...",
        "app_saving": "Dibujando a tamaño real...", "app_saved": "Guardado en %s",
    },
}
# the other languages are in locales/wallpapers.py
from locales.wallpapers import STRINGS as _MORE   # noqa: E402

STRINGS.update(_MORE)


def T(key):
    return STRINGS.get(tl._LANG, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))


# ==========================================================================
# 7. COMMAND LINE
# ==========================================================================
def main():
    ap = argparse.ArgumentParser(description="Abstract wallpapers for desktops and phones.")
    ap.add_argument("styles", nargs="*", help="style(s): " + ", ".join(STYLE_KEYS))
    ap.add_argument("--size", help="a size name (see --list) or WxH; default fhd (1920x1080)")
    ap.add_argument("--orientation", choices=["landscape", "portrait"], help="turn the size if needed")
    ap.add_argument("--scheme", choices=tl.SCHEMES)
    ap.add_argument("--hue", help="base hue: a name (blue, red-orange ...) or 0 .. 11")
    ap.add_argument("--colours", help="your own colours, e.g. '#ff6b6b,#4ecdc4,#1a535c'")
    ap.add_argument("--background", help="dark, black, light, white or a hex colour")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--count", type=int, default=1, help="several pictures, seeds seed .. seed+count-1")
    ap.add_argument("-p", "--param", action="append", default=[], help="style parameter key=value")
    ap.add_argument("--grain", type=float, help="film grain, 0 .. 0.1")
    ap.add_argument("--vignette", type=float, help="darker corners, 0 .. 1 (default 0.25)")
    ap.add_argument("-o", "--output", help="file (.png, .jpg, .webp); with --count a number is added")
    ap.add_argument("--gallery", action="store_true", help="every style (or the given ones) in one sheet")
    ap.add_argument("--cols", type=int, default=4, help="columns of the gallery")
    ap.add_argument("-i", "--input", help="a picture of yours to recolour and resize (style image)")
    ap.add_argument("--mode", choices=IMAGE_MODES, help="with --input: shift (turn all hues so that the main "
                    "one becomes --hue), tint (one hue) or map (lightness through --scheme)")
    ap.add_argument("--fit", choices=FITS, help="with --input: cover (crop, default), contain or stretch")
    ap.add_argument("--show", action="store_true", help="preview window")
    ap.add_argument("--list", action="store_true", help="styles, parameters and sizes")
    ap.add_argument("--lang", choices=[k for k, _ in i18n.LANGS if k in STRINGS], default="en")
    a = ap.parse_args()
    tl._LANG = a.lang
    i18n.use_lang(a.lang)

    if a.list:
        print(T("styles") + ":")
        for k, (fn, params, d) in STYLES.items():
            print("  %-8s %s" % (k, T("d_" + k)))
            print("           %s | scheme=%s hue=%s background=%s" % (
                ", ".join("%s=%s" % kv for kv in params.items()), d["scheme"], d["hue"], d["background"]))
        print(T("sizes") + ":")
        for g, keys in SIZE_GROUPS:
            print("  " + T(g))
            for k in keys:
                print("    %-15s %d x %d" % ((k,) + SIZES[k]))
        print("schemes:", ", ".join(tl.SCHEMES))
        return

    for st in a.styles:
        if st not in STYLES:
            raise SystemExit("unknown style %r (see --list)" % st)
    params = {}
    for item in a.param:
        if "=" not in item:
            raise SystemExit("parameters are key=value, not %r" % item)
        k, v = item.split("=", 1)
        params[k] = tl.parse_value(v)
    base = {"size": a.size, "orientation": a.orientation, "scheme": a.scheme,
            "hue": tl.parse_hue(a.hue) if a.hue is not None else None,
            "colours": tl.parse_colours(a.colours) if a.colours else None,
            "background": a.background, "grain": a.grain, "vignette": a.vignette, "params": params}
    if a.input:
        if not os.path.isfile(a.input):
            raise SystemExit("picture not found: %s" % a.input)
        base["input"] = a.input
        for k in ("mode", "fit"):
            if getattr(a, k):
                params[k] = getattr(a, k)
        if a.vignette is None:
            base["vignette"] = None
    styles = a.styles or (["image"] if a.input else STYLE_KEYS if a.gallery else ["ribbons"])

    if a.show:
        run_preview(dict(base, style=styles[0], seed=a.seed, output=a.output))
        return
    if a.gallery:
        specs = [dict(base, style=st, seed=a.seed + n) for st in styles for n in range(a.count)]
        if params:                         # parameters of one style only make sense for that style
            specs = [dict(sp, params={k: v for k, v in params.items() if k in STYLES[sp["style"]][1]})
                     for sp in specs]
        path = a.output or "wallpapers_gallery.png"
        gallery(specs, path, cols=min(a.cols, len(specs)))
        print("wrote", os.path.abspath(path))
        return
    for st in styles:
        for n in range(a.count):
            sp = dict(base, style=st, seed=a.seed + n)
            s = spec_defaults(sp)
            if a.output and len(styles) == 1 and a.count == 1:
                path = a.output
            elif a.output:
                root, ext = os.path.splitext(a.output)
                path = "%s_%s_%d%s" % (root, st, sp["seed"], ext or ".png")
            else:
                path = default_name(s)
            save(render(sp), path)
            print("wrote", os.path.abspath(path))


if __name__ == "__main__":
    main()
