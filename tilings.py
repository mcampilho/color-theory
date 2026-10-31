#!/usr/bin/env python3
"""
tilings.py
----------
Tilings and mosaics: the tilings of the Wikipedia articles listed in tiles.md
(regular, uniform and dual tilings, Pythagorean, herringbone, pentagonal,
Cairo, Penrose, the "hat" monotile, Robinson, Wang, girih, zellij and Islamic
star patterns), each with several ways of colouring it, and the colours taken
from the colour schemes of colour theory (RYB wheel of color_theory_document.py).

    pip install reportlab pillow
    python3 tilings.py                          # catalogue -> tilings_en.pdf
    python3 tilings.py --lang pt                # Portuguese catalogue
    python3 tilings.py --list                   # tiling names and colourings
    python3 tilings.py hexagonal -c 7 --scheme rainbow -o hex.svg
    python3 tilings.py penrose_p3 --scheme complementary --hue blue -o p3.png
    python3 tilings.py herringbone -p ratio=3 -p angle=45 -o h.pdf

All geometry is computed. Periodic tilings are a motif of polygons repeated
over a lattice (Periodic); gaps between placed polygons are found as the
faces of the planar graph of their edges (faces), duals join the centres of
the tiles around each vertex (dual), and Islamic star patterns follow Hankin's
"polygons in contact" method (hankin). Penrose tilings come from Robinson
triangle deflation, the hat from Smith, Myers, Kaplan and Goodman-Strauss'
metatile substitution, and the Wang tiling from a backtracking search.
"""
import argparse
import math
import random
import sys
from collections import defaultdict

from color_theory_document import STRINGS as CTD_STRINGS
from color_theory_document import hue_ryb, luma, mix, ryb_to_rgb

S3 = math.sqrt(3)
H3 = S3 / 2
PHI = (1 + math.sqrt(5)) / 2
WHITE, BLACK = (1.0, 1.0, 1.0), (0.0, 0.0, 0.0)
STROKE = (0.13, 0.13, 0.13)


# ==========================================================================
# 1. TRANSLATIONS
# ==========================================================================
# The STRINGS table (en, pt, es) is at the end of the file, because it is long.
_LANG = "en"


def T(key):
    table = STRINGS.get(_LANG, STRINGS["en"])
    return table.get(key, STRINGS["en"].get(key, key))


# ==========================================================================
# 2. GEOMETRY
# ==========================================================================
def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def mul(p, k):
    return (p[0] * k, p[1] * k)


def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def unit(deg):
    r = math.radians(deg)
    return (math.cos(r), math.sin(r))


def norm(v):
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n)


def ngon(c, n, r, a0=0.0):
    """Regular n-gon centred at c, circumradius r, first vertex at a0 degrees."""
    return [add(c, mul(unit(a0 + 360.0 * k / n), r)) for k in range(n)]


def circumradius(n, side=1.0):
    return side / (2 * math.sin(math.pi / n))


def inradius(n, side=1.0):
    return side / (2 * math.tan(math.pi / n))


def area(pts):
    s = 0.0
    for i in range(len(pts)):
        s += cross(pts[i - 1], pts[i])
    return s / 2


def centroid(pts):
    a = area(pts)
    if abs(a) < 1e-12:
        return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    cx = cy = 0.0
    for i in range(len(pts)):
        p, q = pts[i - 1], pts[i]
        f = cross(p, q)
        cx += (p[0] + q[0]) * f
        cy += (p[1] + q[1]) * f
    return (cx / (6 * a), cy / (6 * a))


def ccw(pts):
    return list(pts) if area(pts) > 0 else list(pts)[::-1]


def rotate(pts, deg, c=(0.0, 0.0)):
    co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [(c[0] + (x - c[0]) * co - (y - c[1]) * si, c[1] + (x - c[0]) * si + (y - c[1]) * co)
            for x, y in pts]


def linear(pts, m):
    """Apply the 2x2 matrix m = (a, b, c, d): (x, y) -> (a x + b y, c x + d y)."""
    a, b, c, d = m
    return [(a * x + b * y, c * x + d * y) for x, y in pts]


def interior_angles(pts):
    """Interior angle in degrees at each vertex of a counter-clockwise polygon."""
    out = []
    n = len(pts)
    for i in range(n):
        p, v, q = pts[i - 1], pts[i], pts[(i + 1) % n]
        a, b = sub(q, v), sub(p, v)
        out.append(math.degrees(math.atan2(cross(a, b), dot(a, b))) % 360)
    return out


def simplify(pts, eps=1e-7):
    """Drop repeated points and straight (180 degree) vertices."""
    pts = list(pts)
    changed = True
    while changed and len(pts) > 3:
        changed = False
        for i in range(len(pts)):
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % len(pts)]
            u, v = sub(b, a), sub(c, b)
            lu, lv = math.hypot(*u), math.hypot(*v)
            if lu < 1e-9 or lv < 1e-9 or abs(cross(u, v)) < eps * lu * lv:
                del pts[i]
                changed = True
                break
    return pts


def inside(pt, pts):
    """Even-odd point in polygon test."""
    x, y = pt
    res = False
    for i in range(len(pts)):
        (x1, y1), (x2, y2) = pts[i - 1], pts[i]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            res = not res
    return res


class PointIndex:
    """Merge points closer than tol, so shared vertices get one id."""

    def __init__(self, tol=1e-6):
        self.tol = tol
        self.cell = tol * 4
        self.grid = defaultdict(list)
        self.pts = []

    def id(self, p):
        gx, gy = int(math.floor(p[0] / self.cell)), int(math.floor(p[1] / self.cell))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for k in self.grid.get((gx + dx, gy + dy), ()):
                    if dist(self.pts[k], p) < self.tol:
                        return k
        self.pts.append(p)
        self.grid[(gx, gy)].append(len(self.pts) - 1)
        return len(self.pts) - 1


def faces(segs, tol=1e-6):
    """Bounded faces of the planar graph made by the segments [(p, q), ...].

    Segments are split where they cross or touch, so T-junctions and
    crossing lines are handled. Faces come back counter-clockwise."""
    segs = [(p, q) for p, q in segs if dist(p, q) > tol]
    if not segs:
        return []
    cs = 2 * sum(dist(p, q) for p, q in segs) / len(segs)
    grid = defaultdict(list)
    for i, (p, q) in enumerate(segs):
        for gx in range(int(math.floor(min(p[0], q[0]) / cs)), int(math.floor(max(p[0], q[0]) / cs)) + 1):
            for gy in range(int(math.floor(min(p[1], q[1]) / cs)), int(math.floor(max(p[1], q[1]) / cs)) + 1):
                grid[(gx, gy)].append(i)
    cuts = [[0.0, 1.0] for _ in segs]
    seen = set()

    def hit(a, b):
        p, p2 = segs[a]
        q, q2 = segs[b]
        r, s, qp = sub(p2, p), sub(q2, q), sub(q, p)
        lr, ls = math.hypot(*r), math.hypot(*s)
        den = cross(r, s)
        if abs(den) < 1e-10 * lr * ls:
            if abs(cross(qp, r)) > tol * lr:
                return
            for pt in (q, q2):
                t = dot(sub(pt, p), r) / (lr * lr)
                if 0 < t < 1:
                    cuts[a].append(t)
            for pt in (p, p2):
                t = dot(sub(pt, q), s) / (ls * ls)
                if 0 < t < 1:
                    cuts[b].append(t)
            return
        t, w = cross(qp, s) / den, cross(qp, r) / den
        ea, eb = tol / lr, tol / ls
        if -ea <= t <= 1 + ea and -eb <= w <= 1 + eb:
            cuts[a].append(min(max(t, 0.0), 1.0))
            cuts[b].append(min(max(w, 0.0), 1.0))

    for ids in grid.values():
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                a, b = ids[x], ids[y]
                key = (a, b) if a < b else (b, a)
                if key not in seen:
                    seen.add(key)
                    hit(a, b)
    index = PointIndex(tol)
    nbrs = defaultdict(set)
    for (p, q), ts in zip(segs, cuts):
        ts = sorted(ts)
        ids = []
        for t in ts:
            k = index.id((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
            if not ids or ids[-1] != k:
                ids.append(k)
        for a, b in zip(ids, ids[1:]):
            nbrs[a].add(b)
            nbrs[b].add(a)
    P = index.pts
    order, pos = {}, {}
    for v, ws in nbrs.items():
        lst = sorted(ws, key=lambda w: math.atan2(P[w][1] - P[v][1], P[w][0] - P[v][0]))
        order[v] = lst
        pos[v] = {w: i for i, w in enumerate(lst)}
    used, out = set(), []
    for v in order:
        for w in order[v]:
            if (v, w) in used:
                continue
            face, a, b = [], v, w
            while (a, b) not in used:
                used.add((a, b))
                face.append(a)
                lst = order[b]
                c = lst[(pos[b][a] - 1) % len(lst)]
                a, b = b, c
            poly = [P[k] for k in face]
            if len(poly) >= 3 and area(poly) > tol:
                out.append(simplify(poly))
    return out


# ---- shape classes, used by the universal colourings ----------------------
def shape_info(pts):
    """(shape, chirality, orientation) of a polygon.

    shape is the same for congruent polygons (mirror images included),
    chirality tells a polygon from its mirror image (0 for symmetric shapes),
    and orientation is the turn of the polygon in degrees, modulo its own
    rotational symmetry."""
    pts = simplify(ccw(pts))
    n = len(pts)
    ang = interior_angles(pts)
    lens = [dist(pts[i], pts[(i + 1) % n]) for i in range(n)]
    seq = [(round(ang[i]), round(lens[i] * 200)) for i in range(n)]
    mir = [(round(ang[-i % n]), round(lens[(-i - 1) % n] * 200)) for i in range(n)]
    rots = [tuple(seq[i:] + seq[:i]) for i in range(n)]
    mrots = [tuple(mir[i:] + mir[:i]) for i in range(n)]
    best = min(rots + mrots)
    k = sum(1 for r in rots if r == best) or 1
    symmetric = best in rots and best in mrots
    if best in rots:
        chir, start = 0, pts[rots.index(best)]
    else:
        chir, start = 1, pts[(-mrots.index(best)) % n]
    if symmetric:
        chir = 0
    c = centroid(pts)
    per = 360.0 / k
    a = math.degrees(math.atan2(start[1] - c[1], start[0] - c[0])) % 360
    ori = int(round((a % per) * 2)) % int(round(per * 2))
    return best, chir, ori


# ==========================================================================
# 3. TILES, PATCHES AND PERIODIC TILINGS
# ==========================================================================
class Tile:
    __slots__ = ("pts", "kind", "cell", "colour")

    def __init__(self, pts, kind="", cell=None, colour=None):
        self.pts = pts
        self.kind = kind        # prototile name, used by the "kind" colouring
        self.cell = cell        # (i, j, k) lattice cell and motif index, or other data
        self.colour = colour    # fixed colour (Wang tiles), or None


class Patch:
    def __init__(self, tiles, lines=None, extras=None):
        self.tiles = tiles
        self.lines = lines or []      # (points, role, closed)
        self.extras = extras or []    # ("poly", pts, rgb) drawn over the tiles (Penrose arcs, Wang)


def bbox(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def meets(bb, box):
    return bb[0] <= box[2] and bb[2] >= box[0] and bb[1] <= box[3] and bb[3] >= box[1]


class Periodic:
    """A motif of polygons [(points, kind), ...] repeated over the lattice a1, a2.

    lines is an optional motif of open polylines [(points, role)], repeated the
    same way (girih and strapwork)."""

    def __init__(self, a1, a2, motif, lines=None):
        self.a1, self.a2 = a1, a2
        self.motif = [(list(p), k) for p, k in motif]
        self.lines = lines or []

    def frac(self, p):
        det = cross(self.a1, self.a2)
        return cross(p, self.a2) / det, cross(self.a1, p) / det

    def cells(self, box):
        reach = max(math.hypot(*q) for p, _ in self.motif for q in p)
        x0, y0, x1, y1 = box[0] - reach, box[1] - reach, box[2] + reach, box[3] + reach
        fr = [self.frac(c) for c in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
        i0, i1 = int(math.floor(min(f[0] for f in fr))) - 1, int(math.ceil(max(f[0] for f in fr))) + 1
        j0, j1 = int(math.floor(min(f[1] for f in fr))) - 1, int(math.ceil(max(f[1] for f in fr))) + 1
        for i in range(i0, i1 + 1):
            for j in range(j0, j1 + 1):
                yield i, j, add(mul(self.a1, i), mul(self.a2, j))

    def patch(self, box):
        tiles, lines = [], []
        for i, j, o in self.cells(box):
            for k, (pts, kind) in enumerate(self.motif):
                P = [(x + o[0], y + o[1]) for x, y in pts]
                if meets(bbox(P), box):
                    tiles.append(Tile(P, kind, (i, j, k)))
            for pts, role in self.lines:
                P = [(x + o[0], y + o[1]) for x, y in pts]
                if meets(bbox(P), box):
                    lines.append((P, role, False))
        return Patch(tiles, lines)

    def transformed(self, m):
        return Periodic(linear([self.a1], m)[0], linear([self.a2], m)[0],
                        [(linear(p, m), k) for p, k in self.motif],
                        [(linear(p, m), r) for p, r in self.lines])

    def area(self):
        return abs(cross(self.a1, self.a2))

    def around(self, n=2):
        """A box holding the cells -n..n around the origin."""
        pts = [add(mul(self.a1, i), mul(self.a2, j)) for i in (-n, n) for j in (-n, n)]
        return bbox(pts)

    def in_cell(self, p, eps=1e-7):
        s, t = self.frac(p)
        return -eps <= s < 1 - eps and -eps <= t < 1 - eps


def with_gaps(per, kind="gap"):
    """Add to the motif the polygons left uncovered between its tiles."""
    tiles = per.patch(per.around(2)).tiles
    known = PointIndex(1e-5)
    for t in tiles:
        known.id(centroid(t.pts))
    n0 = len(known.pts)
    new = []
    for f in faces([(t.pts[i - 1], t.pts[i]) for t in tiles for i in range(len(t.pts))]):
        c = centroid(f)
        if known.id(c) >= n0 and per.in_cell(c):
            new.append((f, kind))
            n0 = len(known.pts)
    return Periodic(per.a1, per.a2, per.motif + new, per.lines)


def dual(per, kind="dual"):
    """The dual tiling: one tile per vertex, joining the centres of the tiles
    around it (for tilings by regular polygons this is the Laves tiling)."""
    tiles = per.patch(per.around(2)).tiles
    index = PointIndex(1e-5)
    around = defaultdict(list)
    turn = defaultdict(float)
    for t in tiles:
        pts = ccw(t.pts)
        c = centroid(pts)
        for v, a in zip(pts, interior_angles(pts)):
            k = index.id(v)
            around[k].append(c)
            turn[k] += a
    motif = []
    for k, cs in around.items():
        v = index.pts[k]
        if abs(turn[k] - 360) < 1e-3 and per.in_cell(v):
            cs = sorted(cs, key=lambda c: math.atan2(c[1] - v[1], c[0] - v[0]))
            motif.append((cs, kind))
    return Periodic(per.a1, per.a2, motif)


def hankin_rays(pts, theta, delta=0.0):
    """Hankin's polygons in contact: two rays from each edge midpoint at theta
    degrees to the edge; each ray stops where it meets its partner ray."""
    pts = ccw(pts)
    n = len(pts)
    th = math.radians(theta)
    rays = []
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        d = norm(sub(q, p))
        nv = (-d[1], d[0])
        m = mul(add(p, q), .5)
        rays.append((i, add(m, mul(d, delta)), add(mul(d, math.cos(th)), mul(nv, math.sin(th)))))
        rays.append((i, sub(m, mul(d, delta)), add(mul(d, -math.cos(th)), mul(nv, math.sin(th)))))
    cand = []
    for a in range(len(rays)):
        for b in range(a + 1, len(rays)):
            ea, oa, da = rays[a]
            eb, ob, db = rays[b]
            if ea == eb:
                continue
            den = cross(da, db)
            if abs(den) < 1e-12:
                continue
            w = sub(ob, oa)
            s, t = cross(w, db) / den, cross(w, da) / den
            if s > 1e-9 and t > 1e-9:
                x = add(oa, mul(da, s))
                if inside(x, pts) or min(dist(x, v) for v in pts) < 1e-7:
                    cand.append((s + t + 1e-6 * abs(s - t), a, b, x))
    cand.sort()
    done, segs = set(), []
    for _, a, b, x in cand:
        if a in done or b in done:
            continue
        done.update((a, b))
        segs.append((rays[a][1], x))
        segs.append((rays[b][1], x))
    return segs


def hankin(per, theta, delta=0.0, kinds=None):
    """Star pattern of a periodic tiling: strap lines plus the faces between them."""
    cell_lines = []
    for pts, kind in per.motif:
        if kinds is None or kind in kinds:
            for a, b in hankin_rays(pts, theta, delta):
                cell_lines.append(([a, b], "strap"))
    star = Periodic(per.a1, per.a2, [(p, k) for p, k in per.motif], cell_lines)
    patch = star.patch(star.around(2))
    segs = [(p[0], p[1]) for p, _, _ in patch.lines]
    motif = []
    for f in faces(segs):
        if per.in_cell(centroid(f)):
            motif.append((f, "star"))
    return Periodic(per.a1, per.a2, motif, cell_lines)


# ==========================================================================
# 4. THE TILINGS
# ==========================================================================
R8, R12 = circumradius(8), circumradius(12)
r12 = inradius(12)


def triangular():
    return Periodic((1, 0), (.5, H3), [([(0, 0), (1, 0), (.5, H3)], "up"),
                                       ([(1, 0), (1.5, H3), (.5, H3)], "down")])


def square():
    return Periodic((1, 0), (0, 1), [([(0, 0), (1, 0), (1, 1), (0, 1)], "square")])


def hexagonal():
    return Periodic((S3, 0), (H3, 1.5), [(ngon((0, 0), 6, 1, 90), "hexagon")])


def trihexagonal():
    return Periodic((2, 0), (1, S3), [(ngon((0, 0), 6, 1, 0), "hexagon"),
                                      ([(1, 0), (1.5, H3), (.5, H3)], "down"),
                                      ([(1.5, H3), (2.5, H3), (2, S3)], "up")])


def truncated_hexagonal():
    d = 2 + S3
    a1, a2 = (d, 0), (d / 2, d * H3)
    up = [mul(unit(15), R12), add(a1, mul(unit(135), R12)), mul(unit(45), R12)]
    down = [sub(add(a1, a2), p) for p in up]
    return Periodic(a1, a2, [(ngon((0, 0), 12, R12, 15), "dodecagon"), (up, "up"), (down, "down")])


def truncated_square():
    s = 1 + math.sqrt(2)
    return Periodic((s, 0), (0, s), [(ngon((0, 0), 8, R8, 22.5), "octagon"),
                                     (ngon((s / 2, s / 2), 4, math.sqrt(.5), 0), "square")])


def truncated_trihexagonal():
    d = 3 + S3
    a1, a2 = (d, 0), (d / 2, d * H3)
    motif = [(ngon((0, 0), 12, R12, 15), "dodecagon")]
    for th in (0, 60, 120):
        motif.append((ngon(mul(unit(th), r12 + .5), 4, math.sqrt(.5), th + 45), "square"))
    g = mul(add(a1, a2), 1 / 3)
    motif += [(ngon(g, 6, 1, 0), "hexagon"), (ngon(mul(g, 2), 6, 1, 0), "hexagon")]
    return Periodic(a1, a2, motif)


def rhombitrihexagonal():
    d = 1 + S3
    a1, a2 = (d, 0), (d / 2, d * H3)
    motif = [(ngon((0, 0), 6, 1, 30), "hexagon")]
    for th in (0, 60, 120):
        motif.append((ngon(mul(unit(th), H3 + .5), 4, math.sqrt(.5), th + 45), "square"))
    g = mul(add(a1, a2), 1 / 3)
    motif += [(ngon(g, 3, 1 / S3, 90), "up"), (ngon(mul(g, 2), 3, 1 / S3, 270), "down")]
    return Periodic(a1, a2, motif)


def snub_hexagonal():
    e1, e2 = (1, 0), (.5, H3)
    a1 = add(mul(e1, 2), e2)
    a2 = add(mul(e1, -1), mul(e2, 3))
    per = Periodic(a1, a2, [(ngon((0, 0), 6, 1, 0), "hexagon")])
    ring = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))

    def centre_pt(i, j):         # the hexagons are centred on an index-7 sublattice
        return (i + 5 * j) % 7 == 0

    def hex_centres(i, j):
        return {(i - di, j - dj) for di, dj in ring if centre_pt(i - di, j - dj)}

    motif = []
    for i in range(-8, 9):
        for j in range(-8, 9):
            for up in (True, False):
                vs = [(i, j), (i + 1, j), (i, j + 1)] if up else [(i + 1, j), (i + 1, j + 1), (i, j + 1)]
                if any(centre_pt(a, b) for a, b in vs):
                    continue
                pts = [add(mul(e1, a), mul(e2, b)) for a, b in vs]
                if per.in_cell(centroid(pts)):
                    cs = [hex_centres(a, b) for a, b in vs]
                    edge_on_hex = bool(cs[0] & cs[1] or cs[1] & cs[2] or cs[0] & cs[2])
                    motif.append((pts, "triangle_a" if edge_on_hex else "triangle_b"))
    return Periodic(a1, a2, per.motif + motif)


def elongated_triangular():
    return Periodic((1, 0), (.5, 1 + H3), [([(0, 0), (1, 0), (1, 1), (0, 1)], "square"),
                                           ([(0, 1), (1, 1), (.5, 1 + H3)], "up"),
                                           ([(1, 1), (1.5, 1 + H3), (.5, 1 + H3)], "down")])


def snub_square():
    L = math.sqrt(2 + S3)
    r = math.sqrt(.5)
    per = with_gaps(Periodic((L, 0), (0, L), [(ngon((0, 0), 4, r, 60), "square"),
                                              (ngon((L / 2, L / 2), 4, r, 30), "square")]), "gap")
    # each gap is a pair of triangles (a 60 degree rhombus): cut it along its short diagonal
    motif = []
    for pts, kind in per.motif:
        if kind == "gap":
            k = 0 if dist(pts[0], pts[2]) < dist(pts[1], pts[3]) else 1
            a, b, c, d = pts[k:] + pts[:k]
            motif += [([a, b, c], "triangle"), ([a, c, d], "triangle")]
        else:
            motif.append((pts, kind))
    return Periodic(per.a1, per.a2, motif)


ARCHIMEDEAN = {
    "triangular": triangular, "square": square, "hexagonal": hexagonal,
    "trihexagonal": trihexagonal, "truncated_hexagonal": truncated_hexagonal,
    "truncated_square": truncated_square, "truncated_trihexagonal": truncated_trihexagonal,
    "rhombitrihexagonal": rhombitrihexagonal, "snub_hexagonal": snub_hexagonal,
    "elongated_triangular": elongated_triangular, "snub_square": snub_square,
}


# ---- variations ------------------------------------------------------------
def trihexagonal_unequal(a=.62):
    """Up triangles of side a, down triangles of side 1 - a."""
    b = 1 - a
    e1, e2 = (1, 0), (.5, H3)
    L = a + b
    up = [(0, 0), mul(e1, a), mul(e2, a)]
    down = [mul(e1, a), mul(e1, L), add(mul(e1, a), mul(sub(e1, e2), b))]
    per = Periodic(mul(e1, L), mul(e2, L), [(up, "up"), (ccw(down), "down")])
    return with_gaps(per, "hexagon")


def trihexagonal_twisted(alpha=15.0):
    """Triangles turned by +alpha / -alpha: the hexagons become stars."""
    rho = 1 / (S3 * math.cos(math.radians(alpha)))
    gu, gd = (2, 2 / S3), (1, 1 / S3)
    per = Periodic((2, 0), (1, S3), [(ngon(gu, 3, rho, 90 + alpha), "up"),
                                     (ngon(gd, 3, rho, 270 - alpha), "down")])
    return with_gaps(per, "star")


def hexagon_hexstar():
    """The triangles of the trihexagonal tiling become hexagons, the hexagons stars."""
    rho = 1 / S3
    gu, gd = (2, 2 / S3), (1, 1 / S3)
    per = Periodic((2, 0), (1, S3), [(ngon(gu, 6, rho, 30), "hexagon"),
                                     (ngon(gd, 6, rho, 30), "hexagon")])
    return with_gaps(per, "star")


def truncated_square_alternate(t=.35):
    """Squares of two sizes (half diagonals a, b) between the octagons."""
    s = 1 + math.sqrt(2)
    a, b = (1 + t) / math.sqrt(2), (1 - t) / math.sqrt(2)
    motif = []
    for (cx, cy), h in (((s / 2, s / 2), a), ((-s / 2, s / 2), b)):
        if h > 1e-9:
            motif.append((ngon((cx, cy), 4, h, 0), "square_big" if h == a else "square_small"))
    oct_pts = []
    for (cx, cy), h in (((s / 2, s / 2), a), ((-s / 2, s / 2), b), ((-s / 2, -s / 2), a), ((s / 2, -s / 2), b)):
        dx, dy = (-1 if cx > 0 else 1), (-1 if cy > 0 else 1)
        oct_pts += [(cx + dx * h, cy), (cx, cy + dy * h)]
    oct_pts = simplify(sorted(oct_pts, key=lambda p: math.atan2(p[1], p[0])))
    motif.append((oct_pts, "octagon"))
    # the octagon around (s, 0) is the mirror image of this one
    motif.append(([(s - x, y) for x, y in oct_pts][::-1], "octagon"))
    return Periodic((s, s), (s, -s), motif)


def pythagorean(ratio=.5):
    a, b = 1.0, ratio
    return Periodic((a, b), (-b, a), [([(0, 0), (a, 0), (a, a), (0, a)], "big"),
                                      ([(a - b, a), (a, a), (a, a + b), (a - b, a + b)], "small")])


def herringbone(ratio=2, angle=0.0, shear=0.0):
    k = float(ratio)
    hor = [(0, 0), (k, 0), (k, 1), (0, 1)]
    ver = [(k, 1 - k), (k + 1, 1 - k), (k + 1, 1), (k, 1)]
    per = Periodic((1, 1), (k, -k), [(hor, "horizontal"), (ver, "vertical")])
    if shear:
        per = per.transformed((1, shear, 0, 1))
    if angle:
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        per = per.transformed((c, -s, s, c))
    return per


def basketweave():
    motif = [([(0, 0), (2, 0), (2, 1), (0, 1)], "horizontal"), ([(0, 1), (2, 1), (2, 2), (0, 2)], "horizontal"),
             ([(2, 0), (3, 0), (3, 2), (2, 2)], "vertical"), ([(3, 0), (4, 0), (4, 2), (3, 2)], "vertical")]
    return Periodic((2, 2), (2, -2), motif)


def stars_and_crosses():
    """Eight-pointed stars {8/2} touching at their points, with crosses between."""
    R = 1.0
    ri = R * math.cos(math.radians(45)) / math.cos(math.radians(22.5))
    star = [mul(unit(22.5 * k), R if k % 2 == 0 else ri) for k in range(16)]
    d = R * math.sqrt(2)
    return with_gaps(Periodic((d, d), (d, -d), [(star, "star")]), "cross")


def girih_lattice():
    """Decagons on a lattice with 72 degree angles; the gaps are bowties."""
    R10, r10 = circumradius(10), inradius(10)
    return with_gaps(Periodic((2 * r10, 0), mul(unit(72), 2 * r10),
                              [(ngon((0, 0), 10, R10, 18), "decagon")]), "bowtie")


# ---- non periodic -----------------------------------------------------------
def penrose_triangles(box, edge, kind):
    """Robinson triangles of a Penrose tiling covering box: kind "p3" (rhombs) or "p2" (kite and dart)."""
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    R = math.hypot(box[2] - box[0], box[3] - box[1]) / 2 * 1.15
    n = max(1, int(math.ceil(math.log(R / edge) / math.log(PHI))))
    if kind == "p2":
        R = edge * PHI ** n
    tris = []
    for i in range(10):
        B = complex(*unit((2 * i - 1) * 18)) * R
        C = complex(*unit((2 * i + 1) * 18)) * R
        if i % 2 == 0:
            B, C = C, B
        tris.append((0, 0j, B, C))
    for _ in range(n):
        out = []
        for col, A, B, C in tris:
            if kind == "p3":
                if col == 0:
                    P = A + (B - A) / PHI
                    out += [(0, C, P, B), (1, P, C, A)]
                else:
                    Q = B + (A - B) / PHI
                    Rr = B + (C - B) / PHI
                    out += [(1, Rr, C, A), (1, Q, Rr, B), (0, Rr, Q, A)]
            else:
                if col == 0:
                    P = A + (B - A) / PHI
                    Q = A + (C - A) / PHI ** 2
                    out += [(1, Q, A, P), (0, C, P, B), (0, C, P, Q)]
                else:
                    Rr = B + (C - B) / PHI
                    out += [(0, B, A, Rr), (1, Rr, C, A)]
        tris = out
    shift = complex(cx, cy)
    return [(col, A + shift, B + shift, C + shift) for col, A, B, C in tris]


def penrose(box, kind="p3", edge=None):
    edge = edge or (box[2] - box[0]) / 11
    tris = penrose_triangles(box, edge, kind)
    pt = lambda z: (z.real, z.imag)      # noqa: E731
    tiles, seen = [], set()
    names = {"p3": ("thin", "thick"), "p2": ("kite", "dart")}[kind]
    if kind == "p3":                     # the two halves of a rhomb share B C
        shapes = [(col, [A, B, B + C - A, C]) for col, A, B, C in tris]
    else:                                # a kite / dart is a half and its mirror image across A B
        r = lambda z: (round(z.real, 4), round(z.imag, 4))      # noqa: E731
        by_edge = defaultdict(list)
        for n, (col, A, B, C) in enumerate(tris):
            by_edge[(col, frozenset((r(A), r(C))))].append(n)
            by_edge[(col, frozenset((r(A), r(B))))].append(n)
        mate = {}
        for n, (col, A, B, C) in enumerate(tris):
            for P, Q, X in ((A, B, C), (A, C, B)):
                if n in mate:
                    break
                ax = (Q - P) / abs(Q - P)
                Xm = P + ((X - P) / ax).conjugate() * ax
                for m in by_edge[(col, frozenset((r(P), r(Q))))]:
                    if m != n and m not in mate and r(Xm) in {r(z) for z in tris[m][1:]}:
                        mate[n], mate[m] = (P, X, Q, Xm), (P, X, Q, Xm)
                        break
        shapes = [(col, list(mate[n]) if n in mate else [A, B, C]) for n, (col, A, B, C) in enumerate(tris)]
    for col, zs in shapes:
        quad = [pt(z) for z in zs]
        key = tuple(sorted((round(x, 5), round(y, 5)) for x, y in quad))
        if key in seen:
            continue
        seen.add(key)
        if not meets(bbox(quad), box):
            continue
        tiles.append(Tile(ccw(quad), names[col]))
    return Patch(tiles)


# ---- the hat monotile (Smith, Myers, Kaplan, Goodman-Strauss 2023) ---------
def _m(A, B):
    return [A[0] * B[0] + A[1] * B[3], A[0] * B[1] + A[1] * B[4], A[0] * B[2] + A[1] * B[5] + A[2],
            A[3] * B[0] + A[4] * B[3], A[3] * B[1] + A[4] * B[4], A[3] * B[2] + A[4] * B[5] + A[5]]


def _inv(T_):
    det = T_[0] * T_[4] - T_[1] * T_[3]
    return [T_[4] / det, -T_[1] / det, (T_[1] * T_[5] - T_[2] * T_[4]) / det,
            -T_[3] / det, T_[0] / det, (T_[2] * T_[3] - T_[0] * T_[5]) / det]


def _tp(M, p):
    return (M[0] * p[0] + M[1] * p[1] + M[2], M[3] * p[0] + M[4] * p[1] + M[5])


def _trans(x, y):
    return [1, 0, x, 0, 1, y]


def _rot_about(p, ang):
    c, s = math.cos(ang), math.sin(ang)
    return _m(_trans(p[0], p[1]), _m([c, -s, 0, s, c, 0], _trans(-p[0], -p[1])))


def _match_seg(p, q):
    return [q[0] - p[0], p[1] - q[1], p[0], q[1] - p[1], q[0] - p[0], p[1]]


def _match_two(p1, q1, p2, q2):
    return _m(_match_seg(p2, q2), _inv(_match_seg(p1, q1)))


def _intersect(p1, q1, p2, q2):
    d = (q2[1] - p2[1]) * (q1[0] - p1[0]) - (q2[0] - p2[0]) * (q1[1] - p1[1])
    ua = ((q2[0] - p2[0]) * (p1[1] - p2[1]) - (q2[1] - p2[1]) * (p1[0] - p2[0])) / d
    return (p1[0] + ua * (q1[0] - p1[0]), p1[1] + ua * (q1[1] - p1[1]))


def _hex_pt(x, y):
    return (x + .5 * y, H3 * y)


HAT = [_hex_pt(*p) for p in ((0, 0), (-1, -1), (0, -2), (2, -2), (2, -1), (4, -2), (5, -1),
                             (4, 0), (3, 0), (2, 2), (0, 3), (0, 2), (-1, 2))]


class _Meta:
    def __init__(self, shape, label=None):
        self.shape, self.label, self.children = shape, label, []

    def add(self, T_, geom):
        self.children.append((T_, geom))

    def eval(self, n, i):
        T_, g = self.children[n]
        return _tp(T_, g.shape[i])

    def recentre(self):
        cx = sum(p[0] for p in self.shape) / len(self.shape)
        cy = sum(p[1] for p in self.shape) / len(self.shape)
        self.shape = [(x - cx, y - cy) for x, y in self.shape]
        M = _trans(-cx, -cy)
        self.children = [(_m(M, T_), g) for T_, g in self.children]


def _hat_seeds():
    hat = {k: _Meta(HAT, k) for k in ("H1", "H", "T", "P", "F")}
    Ho = [(0, 0), (4, 0), (4.5, H3), (2.5, 5 * H3), (1.5, 5 * H3), (-.5, H3)]
    H = _Meta(Ho)
    H.add(_match_two(HAT[5], HAT[7], Ho[5], Ho[0]), hat["H"])
    H.add(_match_two(HAT[9], HAT[11], Ho[1], Ho[2]), hat["H"])
    H.add(_match_two(HAT[5], HAT[7], Ho[3], Ho[4]), hat["H"])
    H.add(_m(_trans(2.5, H3), _m([-.5, -H3, 0, H3, -.5, 0], [.5, 0, 0, 0, -.5, 0])), hat["H1"])
    Tm = _Meta([(0, 0), (3, 0), (1.5, 3 * H3)])
    Tm.add([.5, 0, .5, 0, .5, H3], hat["T"])
    P = _Meta([(0, 0), (4, 0), (3, 2 * H3), (-1, 2 * H3)])
    P.add([.5, 0, 1.5, 0, .5, H3], hat["P"])
    P.add(_m(_trans(0, 2 * H3), _m([.5, H3, 0, -H3, .5, 0], [.5, 0, 0, 0, .5, 0])), hat["P"])
    F = _Meta([(0, 0), (3, 0), (3.5, H3), (3, 2 * H3), (-1, 2 * H3)])
    F.add([.5, 0, 1.5, 0, .5, H3], hat["F"])
    F.add(_m(_trans(0, 2 * H3), _m([.5, H3, 0, -H3, .5, 0], [.5, 0, 0, 0, .5, 0])), hat["F"])
    return [H, Tm, P, F]


_HAT_RULES = [["H"], [0, 0, "P", 2], [1, 0, "H", 2], [2, 0, "P", 2], [3, 0, "H", 2], [4, 4, "P", 2],
              [0, 4, "F", 3], [2, 4, "F", 3], [4, 1, 3, 2, "F", 0], [8, 3, "H", 0], [9, 2, "P", 0],
              [10, 2, "H", 0], [11, 4, "P", 2], [12, 0, "H", 2], [13, 0, "F", 3], [14, 2, "F", 1],
              [15, 3, "H", 4], [8, 2, "F", 1], [17, 3, "H", 0], [18, 2, "P", 0], [19, 2, "H", 2],
              [20, 4, "F", 3], [20, 0, "P", 2], [22, 0, "H", 2], [23, 4, "F", 3], [23, 0, "F", 3],
              [16, 0, "P", 2], [9, 4, 0, 2, "T", 2], [4, 0, "F", 3]]


def _hat_patch(H, Tm, P, F):
    shapes = {"H": H, "T": Tm, "P": P, "F": F}
    ret = _Meta([])
    for r in _HAT_RULES:
        if len(r) == 1:
            ret.add([1, 0, 0, 0, 1, 0], shapes[r[0]])
        elif len(r) == 4:
            T_, g = ret.children[r[0]]
            poly = g.shape
            p = _tp(T_, poly[(r[1] + 1) % len(poly)])
            q = _tp(T_, poly[r[1]])
            ns = shapes[r[2]].shape
            ret.add(_match_two(ns[r[3]], ns[(r[3] + 1) % len(ns)], p, q), shapes[r[2]])
        else:
            Tp, gp = ret.children[r[0]]
            Tq, gq = ret.children[r[2]]
            p = _tp(Tq, gq.shape[r[3]])
            q = _tp(Tp, gp.shape[r[1]])
            ns = shapes[r[4]].shape
            ret.add(_match_two(ns[r[5]], ns[(r[5] + 1) % len(ns)], p, q), shapes[r[4]])
    return ret


def _hat_metatiles(patch):
    bps1 = patch.eval(8, 2)
    bps2 = patch.eval(21, 2)
    rbps = _tp(_rot_about(bps1, -2 * math.pi / 3), bps2)
    p72 = patch.eval(7, 2)
    p252 = patch.eval(25, 2)
    llc = _intersect(bps1, rbps, patch.eval(6, 2), p72)
    w = sub(patch.eval(6, 2), llc)
    Ho = [llc, bps1]
    w = _tp(_rot_about((0, 0), -math.pi / 3), w)
    Ho.append(add(Ho[1], w))
    Ho.append(patch.eval(14, 2))
    w = _tp(_rot_about((0, 0), -math.pi / 3), w)
    Ho.append(sub(Ho[3], w))
    Ho.append(patch.eval(6, 2))
    nH = _Meta(Ho)
    for ch in (0, 9, 16, 27, 26, 6, 1, 8, 10, 15):
        nH.add(*patch.children[ch])
    nP = _Meta([p72, add(p72, sub(bps1, llc)), bps1, llc])
    for ch in (7, 2, 3, 4, 28):
        nP.add(*patch.children[ch])
    nF = _Meta([bps2, patch.eval(24, 2), patch.eval(25, 0), p252, add(p252, sub(llc, bps1))])
    for ch in (21, 20, 22, 23, 24, 25):
        nF.add(*patch.children[ch])
    AAA = Ho[2]
    BBB = add(Ho[1], sub(Ho[4], Ho[5]))
    CCC = _tp(_rot_about(BBB, -math.pi / 3), AAA)
    nT = _Meta([BBB, CCC, AAA])
    nT.add(*patch.children[11])
    for m in (nH, nP, nF, nT):
        m.recentre()
    return [nH, nT, nP, nF]


def hat(box, level=None, edge=None):
    tiles = _hat_seeds()
    level = level or 4
    for _ in range(level):
        tiles = _hat_metatiles(_hat_patch(*tiles))
    out = []

    def walk(meta, M):
        for T_, g in meta.children:
            if g.label:
                out.append(([_tp(_m(M, T_), p) for p in HAT], g.label))
            else:
                walk(g, _m(M, T_))

    walk(tiles[0], [1, 0, 0, 0, 1, 0])
    # scale: hat kites have short edge 0.5 (half of the hex units above)
    allp = [p for poly, _ in out for p in poly]
    x0, y0, x1, y1 = bbox(allp)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    edge = edge or (box[2] - box[0]) / 26
    k = edge / .5
    bx, by = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    tiles_out = []
    for poly, label in out:
        P = [(bx + (x - cx) * k, by + (y - cy) * k) for x, y in poly]
        if meets(bbox(P), box):
            tiles_out.append(Tile(ccw(P), label))
    return Patch(tiles_out)


# ---- Robinson ---------------------------------------------------------------
def robinson(box, edge=None):
    """Robinson's square tiles and the nested squares their markings draw."""
    e = edge or (box[2] - box[0]) / 24
    nx = int(math.ceil((box[2] - box[0]) / e)) + 2
    ny = int(math.ceil((box[3] - box[1]) / e)) + 2
    ox, oy = box[0] - e, box[1] - e
    tiles, lines = [], []
    for i in range(nx):
        for j in range(ny):
            x, y = ox + i * e, oy + j * e
            kind = {(1, 1): "cross", (0, 0): "centre"}.get((i % 2, j % 2), "arm")
            if kind == "arm":
                kind = "arm_h" if j % 2 else "arm_v"
            tiles.append(Tile([(x, y), (x + e, y), (x + e, y + e), (x, y + e)], kind, (i, j)))
    level = 1
    while 2 ** level < max(nx, ny) * 2:
        side, half = 2 ** level, 2 ** (level - 1)
        role = "mark_a" if level % 2 else "mark_b"
        for ci in range(-side, nx + side, 2 * side):
            for cj in range(-side, ny + side, 2 * side):
                cx, cy = ci + side, cj + side
                sq = [(cx - half, cy - half), (cx + half, cy - half), (cx + half, cy + half), (cx - half, cy + half)]
                P = [(ox + (a + .5) * e, oy + (b + .5) * e) for a, b in sq]
                if meets(bbox(P), box):
                    lines.append((P, role, True))
        level += 1
    return Patch(tiles, lines)


# ---- Wang tiles (Jeandel and Rao 2015) ---------------------------------------
WANG_JR = [  # (left, right, top, bottom)
    "WWWR", "WGRB", "RWBB", "RRBW", "RGGB", "GWRR", "GRBB", "GGRG", "BBWR", "BBBW", "GRRR"]


def wang_search(cols, rows, tileset, seed=1, budget=400000):
    rng = random.Random(seed)
    grid = [None] * (cols * rows)
    order = [list(range(len(tileset))) for _ in grid]
    for o in order:
        rng.shuffle(o)
    pos = [0] * len(grid)
    k, steps = 0, 0
    while 0 <= k < len(grid):
        steps += 1
        if steps > budget:
            return None
        x, y = k % cols, k // cols
        placed = False
        while pos[k] < len(tileset):
            t = tileset[order[k][pos[k]]]
            pos[k] += 1
            if x > 0 and tileset[grid[k - 1]][1] != t[0]:
                continue
            if y > 0 and tileset[grid[k - cols]][3] != t[2]:
                continue
            grid[k] = order[k][pos[k] - 1]
            placed = True
            break
        if placed:
            k += 1
        else:
            pos[k] = 0
            grid[k] = None
            k -= 1
    return grid if k == len(grid) else None


WANG_COLOURS = {"W": (.96, .96, .94), "R": (.86, .20, .18), "G": (.30, .66, .30), "B": (.20, .38, .80)}


def wang(box, edge=None, seed=3):
    e = edge or (box[2] - box[0]) / 16
    cols = int(math.ceil((box[2] - box[0]) / e))
    rows = int(math.ceil((box[3] - box[1]) / e))
    grid = None
    for s in range(seed, seed + 40):
        grid = wang_search(cols, rows, WANG_JR, s)
        if grid:
            break
    tiles, extras = [], []
    for k, t in enumerate(grid or []):
        x, y = k % cols, k // cols
        x0, y1 = box[0] + x * e, box[3] - y * e
        sq = [(x0, y1 - e), (x0 + e, y1 - e), (x0 + e, y1), (x0, y1)]
        c = (x0 + e / 2, y1 - e / 2)
        L, R, Tc, B = WANG_JR[t]
        for (p, q), col in zip(((sq[3], sq[0]), (sq[1], sq[2]), (sq[2], sq[3]), (sq[0], sq[1])), (L, R, Tc, B)):
            extras.append(("poly", [p, q, c], col))
        tiles.append(Tile(sq, "wang%d" % t, (x, y, t)))
    return Patch(tiles, extras=extras)


# ---- pentagons ---------------------------------------------------------------
def hexagon_halves(box, mode="same"):
    """Type 1 pentagons: each hexagon cut in two through opposite edge midpoints."""
    top = [(H3, 0), (H3, .5), (0, 1), (-H3, .5), (-H3, 0)]
    bottom = [(x, -y) for x, y in top][::-1]
    tiles = []
    for t in hexagonal().patch(box).tiles:
        i, j, _ = t.cell
        turn = 0 if mode == "same" else 60 * ((i - j) % 3)
        c = centroid(t.pts)
        for k, (half, kind) in enumerate(((top, "top"), (bottom, "bottom"))):
            tiles.append(Tile([add(p, c) for p in rotate(half, turn)], kind, (i, j, k)))
    return Patch(tiles)


def hexagonal_dissected(box, which="third"):
    """2-uniform tilings: some hexagons of the hexagonal tiling cut into six triangles."""
    tiles = []
    for t in hexagonal().patch(box).tiles:
        i, j, _ = t.cell
        m = (i - j) % 3
        cut = {"third": m == 0, "two_thirds": m != 0, "all": True}[which]
        if cut:
            c = centroid(t.pts)
            for k in range(6):
                tiles.append(Tile([c, t.pts[k], t.pts[(k + 1) % 6]], "triangle", t.cell))
        else:
            tiles.append(Tile(t.pts, "hexagon", t.cell))
    return Patch(tiles)


# ==========================================================================
# 5. REGISTRY
# ==========================================================================
class Tiling:
    def __init__(self, key, make, colourings=None, default="kind", size=8.0, params=None,
                 scheme="triad", hue=4, stroke=True):
        self.key = key
        self.make = make                    # make(box, **params) -> Patch
        self.colourings = colourings or {}  # tiling-specific colourings: name -> tile -> key
        self.default = default
        self.size = size                    # width of the default view, in edge lengths
        self.params = params or {}
        self.scheme, self.hue = scheme, hue
        self.stroke = stroke


TILINGS = {}
_cache = {}


def cached(fn, *args):
    key = (fn.__name__,) + args
    if key not in _cache:
        _cache[key] = fn(*args)
    return _cache[key]


def register(key, make, **kw):
    TILINGS[key] = Tiling(key, make, **kw)


def periodic(factory, transform=None):
    """make() for a periodic tiling; params go to the factory (shear and turn are generic)."""
    def make(box, shear=0.0, turn=0.0, **p):
        per = cached(factory, *sorted(p.items()))
        if shear or turn:
            c, s = math.cos(math.radians(turn)), math.sin(math.radians(turn))
            m = (1, shear, 0, 1)
            m = (c * m[0] - s * m[2], c * m[1] - s * m[3], s * m[0] + c * m[2], s * m[1] + c * m[3])
            per = per.transformed(m)
        return per.patch(box)
    return make


def _kw(fn):
    """Adapt fn(**params) to the cached(factory, *items) call of periodic()."""
    def factory(*items):
        return fn(**dict(items))
    factory.__name__ = fn.__name__
    return factory


def cell(t):
    return t.cell or (0, 0, 0)


def _tri(f):
    def colour(t):
        i, j, k = cell(t)
        return f(i, j, k)
    return colour


TRI_COLOURINGS = {
    "111111": _tri(lambda i, j, k: 0),
    "121212": _tri(lambda i, j, k: k),
    "111222": _tri(lambda i, j, k: j % 2),
    "112122": _tri(lambda i, j, k: (i + j // 2) % 2 if k == 0 else (i + (j + 1) // 2 + 1) % 2),
    "121213": _tri(lambda i, j, k: 0 if k == 0 else (1 if (i - j) % 3 else 2)),
    "111212": _tri(lambda i, j, k: 0 if k == 0 or (i - j) % 3 == 0 else 1),
    "111112": _tri(lambda i, j, k: 1 if k == 1 and (i - j) % 3 == 0 else 0),
    "121314": _tri(lambda i, j, k: 0 if k == 0 else 1 + (i - j) % 3),
}
HEX_COLOURINGS = {
    "1": _tri(lambda i, j, k: 0),
    "2": _tri(lambda i, j, k: j % 2),
    "2-1": _tri(lambda i, j, k: 1 if (i - j) % 3 == 0 else 0),
    "3": _tri(lambda i, j, k: (i - j) % 3),
    "4": _tri(lambda i, j, k: 2 * (i % 2) + j % 2),
    "7": _tri(lambda i, j, k: (i + 3 * j) % 7),
}

register("triangular", periodic(_kw(triangular)), colourings=TRI_COLOURINGS, default="121212", size=7)
register("square", periodic(_kw(square)), colourings={"checker": _tri(lambda i, j, k: (i + j) % 2)},
         default="checker", size=7)
register("hexagonal", periodic(_kw(hexagonal)), colourings=HEX_COLOURINGS, default="3", size=11)
register("trihexagonal", periodic(_kw(trihexagonal)),
         colourings={"1212": _tri(lambda i, j, k: min(k, 1)), "1232": _tri(lambda i, j, k: k)},
         default="1232", size=10)
register("truncated_hexagonal", periodic(_kw(truncated_hexagonal)), size=14)
register("truncated_square", periodic(_kw(truncated_square)),
         colourings={"122": _tri(lambda i, j, k: k),
                     "123": _tri(lambda i, j, k: 2 if k else (i + j) % 2)}, default="122", size=10)
register("truncated_trihexagonal", periodic(_kw(truncated_trihexagonal)), size=18)
register("rhombitrihexagonal", periodic(_kw(rhombitrihexagonal)), size=11)
register("snub_hexagonal", periodic(_kw(snub_hexagonal)), size=11)
register("elongated_triangular", periodic(_kw(elongated_triangular)), size=8)
register("snub_square", periodic(_kw(snub_square)), size=9)


def _dual_of(base):
    def factory(*items):
        return dual(ARCHIMEDEAN[base]())
    factory.__name__ = "dual_" + base
    return factory


DUALS = {"triakis_triangular": "truncated_hexagonal", "tetrakis_square": "truncated_square",
         "kisrhombille": "truncated_trihexagonal", "rhombille": "trihexagonal",
         "deltoidal_trihexagonal": "rhombitrihexagonal", "cairo": "snub_square",
         "prismatic_pentagonal": "elongated_triangular", "floret_pentagonal": "snub_hexagonal"}
for _k, _b in DUALS.items():
    register(_k, periodic(_dual_of(_b)), default="orientation", size=TILINGS[_b].size * .9)

register("trihexagonal_unequal", periodic(_kw(trihexagonal_unequal)), params={"a": .62}, size=6)
register("trihexagonal_twisted", periodic(_kw(trihexagonal_twisted)), params={"alpha": 15.0}, size=10)
register("hexagon_hexstar", periodic(_kw(hexagon_hexstar)), size=10)
register("truncated_square_alternate", periodic(_kw(truncated_square_alternate)), params={"t": .35}, size=11)
register("pythagorean", periodic(_kw(pythagorean)), params={"ratio": .5}, size=6)
register("herringbone", periodic(_kw(herringbone)), params={"ratio": 2, "angle": 0.0}, size=12)
register("basketweave", periodic(_kw(basketweave)), size=12)
register("stars_crosses", periodic(_kw(stars_and_crosses)), size=8, scheme="zellij")
register("girih", periodic(_kw(girih_lattice)), size=12, scheme="girih")


def _hankin_factory(*items):
    p = dict(items)
    return hankin(TILINGS_BASE[p["base"]](), p["theta"])


TILINGS_BASE = dict(ARCHIMEDEAN, girih=girih_lattice)
register("hankin", periodic(_hankin_factory), params={"base": "truncated_square", "theta": 67.5},
         default="shape", size=10, scheme="zellij", stroke=False)
register("hexagon_halves", lambda box, mode="same": hexagon_halves(box, mode), params={"mode": "same"}, size=9)
register("hexagonal_dissected", lambda box, which="third": hexagonal_dissected(box, which),
         params={"which": "third"}, size=11)
register("penrose_p3", lambda box: penrose(box, "p3"), size=12, scheme="complementary", hue=8)
register("penrose_p2", lambda box: penrose(box, "p2"), size=12, scheme="complementary", hue=2)
register("hat", lambda box: hat(box), size=12, scheme="square")
register("robinson", lambda box: robinson(box), size=12, scheme="analogous", hue=8)
register("wang", lambda box, seed=3: wang(box, seed=int(seed)), params={"seed": 3}, default="classic",
         size=12, stroke=True)


# ==========================================================================
# 6. COLOURINGS AND PALETTES
# ==========================================================================
UNIVERSAL = ["single", "kind", "shape", "chirality", "orientation", "proper", "random", "rings"]
HUE_KEYS = ["yellow", "yellow-orange", "orange", "red-orange", "red", "red-violet", "violet",
            "blue-violet", "blue", "blue-green", "green", "yellow-green"]
SCHEME_OFFSETS = {"analogous": [0, 1, -1, 2, -2, 3, -3], "complementary": [0, 6],
                  "split": [0, 5, 7], "triad": [0, 4, 8], "tetrad": [0, 2, 6, 8],
                  "square": [0, 3, 6, 9]}


def hexc(h):
    return tuple(int(h[k:k + 2], 16) / 255 for k in (0, 2, 4))


NAMED_PALETTES = {
    # glazed tiles of the western zellij: white ground, green, black, ochre, cobalt, turquoise
    "zellij": [hexc(h) for h in ("F4EFE4", "1F6B4A", "23231F", "C8962E", "234A9A", "3AA5A0", "8C3B2A")],
    # Portuguese azulejos: tin white and cobalt blues
    "azulejo": [hexc(h) for h in ("F5F3EC", "1D3F8F", "6E8FCB", "0E1F4D", "B9C8E6")],
    "girih": [hexc(h) for h in ("2F6E8E", "D9B44A", "B84A3C", "F1E7D0", "5C8D4F", "2B2B33")],
    "earth": [hexc(h) for h in ("B5532F", "E2B77A", "6B4226", "F2E6CF", "8A8F4D", "3C2A21")],
    "grey": [(.92, .92, .92), (.62, .62, .62), (.32, .32, .32), (.78, .78, .78), (.47, .47, .47)],
}
SCHEMES = ["mono", "analogous", "complementary", "split", "triad", "tetrad", "square", "rainbow"] + \
    list(NAMED_PALETTES)


def ryb_hue(h):
    return ryb_to_rgb(*hue_ryb(h))


def palette(scheme, hue, n, custom=None):
    if custom:
        base = list(custom)
    elif scheme == "mono":
        c = ryb_hue(hue)
        base = [c, mix(c, WHITE, .55), mix(c, BLACK, .45), mix(c, WHITE, .8), mix(c, BLACK, .7),
                mix(c, WHITE, .3)]
    elif scheme == "rainbow":
        base = [ryb_hue(hue + 12.0 * k / max(n, 1)) for k in range(max(n, 1))]
    elif scheme in NAMED_PALETTES:
        base = NAMED_PALETTES[scheme]
    else:
        base = [ryb_hue(hue + o) for o in SCHEME_OFFSETS[scheme]]
    out, r = list(base), 1
    while len(out) < n:
        t = min(.15 + .2 * ((r + 1) // 2), .8)
        out += [mix(c, WHITE if r % 2 else BLACK, t) for c in base]
        r += 1
    return out[:max(n, 1)]


def edge_key(p, q):
    a, b = (round(p[0], 4), round(p[1], 4)), (round(q[0], 4), round(q[1], 4))
    return (a, b) if a < b else (b, a)


def proper_colouring(tiles):
    """Greedy colouring: tiles that share an edge get different colours."""
    owner = defaultdict(list)
    for n, t in enumerate(tiles):
        for i in range(len(t.pts)):
            owner[edge_key(t.pts[i - 1], t.pts[i])].append(n)
    adj = defaultdict(set)
    for ids in owner.values():
        for a in ids:
            adj[a].update(b for b in ids if b != a)
    order = sorted(range(len(tiles)), key=lambda n: (-len(adj[n]), centroid(tiles[n].pts)))
    col = {}
    for n in order:
        used = {col[m] for m in adj[n] if m in col}
        col[n] = next(k for k in range(len(tiles) + 1) if k not in used)
    return [col[n] for n in range(len(tiles))]


def colour_keys(tiling, tiles, colouring, centre, size, seed=1):
    """One key per tile; equal keys get equal colours. Returns (keys, ordered distinct keys)."""
    if colouring in tiling.colourings:
        keys = [tiling.colourings[colouring](t) for t in tiles]
    elif colouring == "single":
        keys = [0] * len(tiles)
    elif colouring == "kind":
        keys = [t.kind for t in tiles]
    elif colouring in ("shape", "chirality", "orientation"):
        n = {"shape": 1, "chirality": 2, "orientation": 3}[colouring]
        keys = [shape_info(t.pts)[:n] for t in tiles]
    elif colouring == "proper":
        keys = proper_colouring(tiles)
    elif colouring == "random":
        rng = random.Random(seed)
        keys = [rng.randrange(6) for _ in tiles]
    elif colouring == "rings":
        keys = [int(dist(centroid(t.pts), centre) / (size / 14)) for t in tiles]
    else:
        raise SystemExit("unknown colouring %r for %s" % (colouring, tiling.key))
    if colouring in ("shape", "chirality", "orientation"):
        big = {}
        for k, t in zip(keys, tiles):
            big[k] = max(big.get(k, 0), abs(area(t.pts)))
        order = sorted(big, key=lambda k: (-round(big[k], 3), k))
    elif colouring == "kind":
        order = list(dict.fromkeys(t.kind for t in sorted(tiles, key=lambda t: -abs(area(t.pts)))))
        order = sorted(order, key=lambda k: _kind_rank(tiling, k))
    else:
        order = sorted(set(keys), key=lambda k: (str(type(k)), k))
    return keys, order


def _kind_rank(tiling, kind):
    motif_kinds = ["dodecagon", "decagon", "octagon", "hexagon", "star", "square", "big", "thick", "kite",
                   "up", "down", "triangle", "triangle_a", "triangle_b", "gap", "cross", "bowtie"]
    return (motif_kinds.index(kind) if kind in motif_kinds else 99, kind)


# ==========================================================================
# 7. SCENES AND OUTPUT
# ==========================================================================
def spec_defaults(spec):
    t = TILINGS[spec["key"]]
    out = {"colouring": t.default, "scheme": t.scheme, "hue": t.hue, "colours": None,
           "size": t.size, "params": {}, "overlay": [], "aspect": .75, "seed": 1, "girih": None}
    out.update({k: v for k, v in spec.items() if v is not None})
    return out


def build_scene(spec):
    """Drawing operations for a spec, in tile units with y up, and the view box."""
    s = spec_defaults(spec)
    tiling = TILINGS[s["key"]]
    w = s["size"]
    h = w * s["aspect"]
    box = (-w / 2, -h / 2, w / 2, h / 2)
    params = dict(tiling.params)
    params.update(s["params"])
    patch = tiling.make(box, **params)
    tiles = patch.tiles
    lw = w * .0032
    ops = []
    if s["colouring"] == "classic" or s["key"] == "wang":
        cols_wang = {k: (WANG_COLOURS[k] if s["colouring"] == "classic" else c)
                     for k, c in zip("WRGB", palette(s["scheme"], s["hue"], 4, s["colours"]))}
        keys, order, pal = [0] * len(tiles), [0], [WHITE]
    else:
        keys, order = colour_keys(tiling, tiles, s["colouring"], (0, 0), w, s["seed"])
        pal = palette(s["scheme"], s["hue"], len(order) + 2, s["colours"])
    index = {k: n for n, k in enumerate(order)}
    edges_mode = "edges" in s["overlay"]
    stroke = STROKE if tiling.stroke else None
    for t, k in zip(tiles, keys):
        fill = WHITE if edges_mode and s["colouring"] == "single" else pal[index[k]]
        ops.append(("poly", t.pts, fill, None if edges_mode else stroke, lw))
    for _, pts, letter in patch.extras:        # Wang tiles: one triangle per edge colour
        ops.append(("poly", pts, cols_wang[letter], STROKE, lw * .6))
    if s["key"] == "wang":
        for t in tiles:
            ops.append(("line", t.pts, STROKE, lw * 1.6, True))
    if s["girih"]:
        for t in tiles:
            for a, b in hankin_rays(t.pts, float(s["girih"])):
                ops.append(("line", [a, b], hexc("1D2B6B"), lw * 2.2, False))
    straps = [ln for ln in patch.lines if ln[1] == "strap"]
    if straps:
        band = w * .011
        for pts, _, closed in straps:
            ops.append(("line", pts, (.12, .12, .12), band + 2.2 * lw, closed))
        for pts, _, closed in straps:
            ops.append(("line", pts, (.97, .95, .89), band, closed))
    for pts, role, closed in patch.lines:
        if role.startswith("mark"):
            col, width = ((.10, .10, .10), lw * 3.2) if role == "mark_a" else ((.86, .36, .12), lw * 1.3)
            ops.append(("line", pts, col, width, closed))
    if edges_mode:
        dirs = sorted({int(round(math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 180)) % 180
                       for t in tiles for p, q in zip(t.pts, t.pts[1:] + t.pts[:1])})
        ecol = palette(s["scheme"], s["hue"], len(dirs), s["colours"])
        for t in tiles:
            for p, q in zip(t.pts, t.pts[1:] + t.pts[:1]):
                d = int(round(math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 180)) % 180
                ops.append(("line", [p, q], ecol[dirs.index(d)], lw * 4.5, False))
    if "dual" in s["overlay"]:
        owner = defaultdict(list)
        for t in tiles:
            for i in range(len(t.pts)):
                owner[edge_key(t.pts[i - 1], t.pts[i])].append(centroid(t.pts))
        for cs in owner.values():
            if len(cs) == 2:
                ops.append(("line", cs, (.78, .10, .12), lw * 1.5, False))
    if "circles" in s["overlay"]:
        index_v = PointIndex(1e-5)
        shortest = defaultdict(lambda: 1e9)
        for t in tiles:
            for i in range(len(t.pts)):
                p, q = t.pts[i - 1], t.pts[i]
                for v in (p, q):
                    k = index_v.id(v)
                    shortest[k] = min(shortest[k], dist(p, q))
        fill = mix(WHITE, pal[0], .35)
        for k, r in shortest.items():
            ops.append(("circle", index_v.pts[k], r / 2, fill, STROKE, lw))
    if "incircles" in s["overlay"]:
        for t in tiles:
            c = centroid(t.pts)
            r = min(abs(cross(sub(q, p), sub(c, p))) / dist(p, q) for p, q in zip(t.pts, t.pts[1:] + t.pts[:1]))
            ops.append(("circle", c, r, mix(WHITE, pal[-1], .25), STROKE, lw))
    return ops, box


def _rgb255(c):
    return tuple(max(0, min(255, int(round(v * 255)))) for v in c)


def _hex(c):
    return "#%02x%02x%02x" % _rgb255(c)


def write_svg(ops, box, path, width=1200):
    x0, y0, x1, y1 = box
    k = width / (x1 - x0)
    height = (y1 - y0) * k
    P = lambda p: "%.2f,%.2f" % ((p[0] - x0) * k, (y1 - p[1]) * k)   # noqa: E731
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
           % (width, height, width, height),
           '<defs><clipPath id="v"><rect width="%d" height="%d"/></clipPath></defs>' % (width, height),
           '<rect width="100%" height="100%" fill="#ffffff"/>',
           '<g clip-path="url(#v)" stroke-linejoin="round" stroke-linecap="round">']
    for op in ops:
        if op[0] == "poly":
            _, pts, fill, stroke, lw = op
            st = ' stroke="%s" stroke-width="%.2f"' % (_hex(stroke), lw * k) if stroke else ""
            out.append('<path d="M%sZ" fill="%s"%s/>' % ("L".join(P(p) for p in pts), _hex(fill), st))
        elif op[0] == "line":
            _, pts, col, lw, closed = op
            out.append('<path d="M%s%s" fill="none" stroke="%s" stroke-width="%.2f"/>'
                       % ("L".join(P(p) for p in pts), "Z" if closed else "", _hex(col), lw * k))
        else:
            _, c, r, fill, stroke, lw = op
            x, y = P(c).split(",")
            out.append('<circle cx="%s" cy="%s" r="%.2f" fill="%s" stroke="%s" stroke-width="%.2f"/>'
                       % (x, y, r * k, _hex(fill), _hex(stroke), lw * k))
    out.append("</g></svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))


def render_image(ops, box, width=1200, ss=3):
    from PIL import Image, ImageDraw
    x0, y0, x1, y1 = box
    W = width * ss
    k = W / (x1 - x0)
    H = int(round((y1 - y0) * k))
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    P = lambda p: ((p[0] - x0) * k, (y1 - p[1]) * k)   # noqa: E731
    for op in ops:
        if op[0] == "poly":
            _, pts, fill, stroke, lw = op
            q = [P(p) for p in pts]
            d.polygon(q, fill=_rgb255(fill))
            if stroke:
                d.line(q + [q[0]], fill=_rgb255(stroke), width=max(1, int(round(lw * k))), joint="curve")
        elif op[0] == "line":
            _, pts, col, lw, closed = op
            q = [P(p) for p in pts] + ([P(pts[0])] if closed else [])
            wpx = max(1, int(round(lw * k)))
            d.line(q, fill=_rgb255(col), width=wpx, joint="curve")
            for x, y in (q[0], q[-1]):
                d.ellipse((x - wpx / 2, y - wpx / 2, x + wpx / 2, y + wpx / 2), fill=_rgb255(col))
        else:
            _, c, r, fill, stroke, lw = op
            x, y = P(c)
            d.ellipse((x - r * k, y - r * k, x + r * k, y + r * k), fill=_rgb255(fill),
                      outline=_rgb255(stroke), width=max(1, int(round(lw * k))))
    return img.resize((width, int(round(H / ss))), Image.LANCZOS)


def draw_ops_pdf(c, ops, box, x, y, w, h):
    """Draw ops into the rectangle (x, y, w, h) of a ReportLab canvas, clipped."""
    x0, y0, x1, y1 = box
    k = min(w / (x1 - x0), h / (y1 - y0))
    P = lambda p: (x + (p[0] - x0) * k, y + (p[1] - y0) * k)   # noqa: E731
    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, w, h)
    c.clipPath(clip, stroke=0, fill=0)
    c.setLineJoin(1)
    c.setLineCap(1)
    for op in ops:
        if op[0] in ("poly", "line"):
            pts = op[1]
            path = c.beginPath()
            path.moveTo(*P(pts[0]))
            for p in pts[1:]:
                path.lineTo(*P(p))
            if op[0] == "poly":
                _, _, fill, stroke, lw = op
                path.close()
                c.setFillColorRGB(*fill)
                if stroke:
                    c.setStrokeColorRGB(*stroke)
                    c.setLineWidth(lw * k)
                c.drawPath(path, fill=1, stroke=1 if stroke else 0)
            else:
                _, _, col, lw, closed = op
                if closed:
                    path.close()
                c.setStrokeColorRGB(*col)
                c.setLineWidth(lw * k)
                c.drawPath(path, fill=0, stroke=1)
        else:
            _, cc, r, fill, stroke, lw = op
            c.setFillColorRGB(*fill)
            c.setStrokeColorRGB(*stroke)
            c.setLineWidth(lw * k)
            px, py = P(cc)
            c.circle(px, py, r * k, fill=1, stroke=1)
    c.restoreState()


# ==========================================================================
# 8. CATALOGUE
# ==========================================================================
def V(cap, key, colouring=None, scheme=None, hue=None, **kw):
    d = {"cap": cap, "key": key, "colouring": colouring, "scheme": scheme, "hue": hue}
    d.update(kw)
    return d


# (family, Wikipedia article, variants); hues are RYB wheel steps (0 yellow, 4 red, 8 blue)
CATALOGUE = [
    ("triangular", "Triangular tiling", [
        V("v_tri_regular", "triangular", "111111", "mono", 8),
        V(("v_uniform", "121212"), "triangular", "121212", "complementary", 2),
        V(("v_uniform", "111222"), "triangular", "111222", "split", 4),
        V(("v_uniform", "112122"), "triangular", "112122", "analogous", 9),
        V(("v_uniform", "121213"), "triangular", "121213", "triad", 0),
        V(("v_uniform", "111212"), "triangular", "111212", "complementary", 10),
        V(("v_uniform", "111112"), "triangular", "111112", "tetrad", 6),
        V(("v_uniform", "121314"), "triangular", "121314", "square", 4),
        V("v_kisrhombille", "kisrhombille", "orientation", "rainbow", 0, size=9),
        V("v_triakis", "triakis_triangular", "orientation", "tetrad", 8),
    ]),
    ("truncated_square", "Truncated square tiling", [
        V("v_ts_plain", "truncated_square", "single", "mono", 9),
        V(("v_uniform", "122"), "truncated_square", "122", "complementary", 4),
        V(("v_uniform", "123"), "truncated_square", "123", "triad", 2),
        V("v_circlepack", "truncated_square", "single", "grey", overlay=["circles"]),
        V("v_ts_alt", "truncated_square_alternate", "kind", "split", 8),
        V("v_ts_chamfer", "truncated_square_alternate", "kind", "analogous", 3, params={"t": 1.0}),
        V("v_tetrakis", "tetrakis_square", "orientation", "square", 1),
        V("v_dual_overlay", "truncated_square", "122", "mono", 0, overlay=["dual"]),
    ]),
    ("hexagonal", "Hexagonal tiling", [
        V("v_hex_regular", "hexagonal", "1", "mono", 10),
        V("v_hex_2", "hexagonal", "2", "complementary", 8),
        V("v_hex_21", "hexagonal", "2-1", "complementary", 0),
        V("v_hex_3", "hexagonal", "3", "triad", 4),
        V("v_hex_4", "hexagonal", "4", "tetrad", 9),
        V("v_hex_7", "hexagonal", "7", "rainbow", 0),
        V("v_kissing", "hexagonal", "1", "grey", overlay=["incircles"]),
        V("v_dissect1", "hexagonal_dissected", "kind", "split", 6, params={"which": "third"}),
        V("v_dissect2", "hexagonal_dissected", "kind", "split", 2, params={"which": "two_thirds"}),
    ]),
    ("trihexagonal", "Trihexagonal tiling", [
        V(("v_uniform", "1212"), "trihexagonal", "1212", "complementary", 9),
        V(("v_uniform", "1232"), "trihexagonal", "1232", "triad", 0),
        V("v_circlepack", "trihexagonal", "single", "grey", overlay=["circles"]),
        V("v_kagome", "trihexagonal", "single", "triad", 8, overlay=["edges"]),
        V("v_unequal", "trihexagonal_unequal", "kind", "split", 4),
        V("v_twisted", "trihexagonal_twisted", "kind", "analogous", 7),
        V("v_twisted2", "trihexagonal_twisted", "kind", "triad", 3, params={"alpha": 24.0}),
        V("v_hexstar", "hexagon_hexstar", "kind", "complementary", 5),
    ]),
    ("rhombille", "Rhombille tiling", [
        V("v_rhombille", "rhombille", "single", "mono", 2),
        V("v_siena", "rhombille", "orientation", "earth"),
        V("v_cubes", "rhombille", "orientation", "mono", 8),
        V("v_rh_dual", "rhombille", "orientation", "grey", overlay=["dual"]),
        V("v_skew", "rhombille", "orientation", "triad", 1, params={"shear": .45, "turn": -12}),
    ]),
    ("pythagorean", "Pythagorean tiling", [
        V("v_pyth_half", "pythagorean", "kind", "complementary", 3),
        V("v_pyth_golden", "pythagorean", "kind", "split", 9, params={"ratio": 1 / PHI}),
        V("v_pyth_random", "pythagorean", "random", "earth", params={"ratio": .3}, size=5),
    ]),
    ("regular", "Euclidean tilings by convex regular polygons", [
        V("n_triangular", "triangular", "111111", "mono", 4),
        V("n_square", "square", "checker", "complementary", 1),
        V("n_hexagonal", "hexagonal", "3", "triad", 9),
        V("n_trihexagonal", "trihexagonal", "1212", "complementary", 2),
        V("n_truncated_hexagonal", "truncated_hexagonal", "kind", "split", 8),
        V("n_truncated_square", "truncated_square", "kind", "complementary", 6),
        V("n_truncated_trihexagonal", "truncated_trihexagonal", "kind", "triad", 4),
        V("n_rhombitrihexagonal", "rhombitrihexagonal", "kind", "tetrad", 10),
        V("n_snub_hexagonal", "snub_hexagonal", "kind", "triad", 6),
        V("n_elongated_triangular", "elongated_triangular", "kind", "analogous", 1),
        V("n_snub_square", "snub_square", "kind", "split", 0),
        V("v_dissect1", "hexagonal_dissected", "kind", "complementary", 8),
    ]),
    ("penrose", "Penrose tiling", [
        V("v_p3", "penrose_p3", "kind", "complementary", 8),
        V("v_p3_ori", "penrose_p3", "orientation", "rainbow", 0),
        V("v_p3_proper", "penrose_p3", "proper", "tetrad", 9),
        V("v_p2", "penrose_p2", "kind", "complementary", 2),
        V("v_p2_rings", "penrose_p2", "rings", "analogous", 7),
        V("v_p2_proper", "penrose_p2", "proper", "triad", 4),
    ]),
    ("aperiodic", "Aperiodic tiling", [
        V("v_hat", "hat", "kind", "square", 4),
        V("v_hat_ori", "hat", "orientation", "rainbow", 0),
        V("v_robinson", "robinson", "kind", colours=[(.72, .82, .93), (.97, .96, .93), (.97, .96, .93),
                                                    (.97, .96, .93)]),
        V("v_p3_rings", "penrose_p3", "rings", "rainbow", 8),
    ]),
    ("herringbone", "Herringbone pattern", [
        V("v_hb_2", "herringbone", "kind", "earth"),
        V("v_hb_45", "herringbone", "kind", "complementary", 3, params={"angle": 45.0}),
        V("v_hb_3", "herringbone", "kind", "split", 10, params={"ratio": 3}),
        V("v_hb_long", "herringbone", "random", "earth", params={"ratio": 6.6}, size=18),
        V("v_hb_par", "herringbone", "kind", "triad", 8, params={"shear": .5}),
        V("v_basket", "basketweave", "kind", "complementary", 0),
    ]),
    ("pentagonal", "Pentagonal tiling", [
        V("v_halves", "hexagon_halves", "kind", "complementary", 10),
        V("v_halves_alt", "hexagon_halves", "orientation", "rainbow", 1, params={"mode": "turn"}),
        V("v_cairo_p", "cairo", "orientation", "tetrad", 4),
        V("v_prismatic", "prismatic_pentagonal", "orientation", "split", 2),
        V("v_floret", "floret_pentagonal", "orientation", "rainbow", 0),
        V("v_floret_proper", "floret_pentagonal", "proper", "triad", 9),
    ]),
    ("cairo", "Cairo pentagonal tiling", [
        V("v_cairo", "cairo", "single", "mono", 9),
        V("v_cairo_ori", "cairo", "orientation", "square", 0),
        V("v_cairo_proper", "cairo", "proper", "triad", 7),
        V("v_cairo_dual", "cairo", "orientation", "grey", overlay=["dual"]),
    ]),
    ("girih", "Girih tile", [
        V("v_girih_tiles", "girih", "kind", "girih"),
        V("v_girih_lines", "girih", "kind", "girih", girih=54),
        V("v_girih_star", "hankin", "shape", "girih", params={"base": "girih", "theta": 54.0}),
        V("v_girih_star2", "hankin", "shape", "zellij", params={"base": "girih", "theta": 54.0}),
    ]),
    ("wang", "Wang tile", [
        V("v_wang", "wang", "classic", None),
        V("v_wang_scheme", "wang", "scheme", "square", 2, params={"seed": 5}),
    ]),
    ("zellij", "Zellij", [
        V("v_stars_crosses", "stars_crosses", "kind", "zellij"),
        V("v_sc_azulejo", "stars_crosses", "kind", "azulejo"),
        V("v_z8", "hankin", "shape", "zellij", params={"base": "truncated_square", "theta": 67.5}),
        V("v_z12", "hankin", "shape", "zellij", params={"base": "truncated_trihexagonal", "theta": 60.0},
          size=16),
        V("v_z10", "hankin", "shape", "earth", params={"base": "girih", "theta": 54.0}),
    ]),
    ("islamic", "Islamic geometric patterns", [
        V("v_i6", "hankin", "shape", "azulejo", params={"base": "hexagonal", "theta": 60.0}),
        V("v_i_sq", "hankin", "shape", "zellij", params={"base": "square", "theta": 67.5}, size=7),
        V("v_i_31212", "hankin", "shape", "girih", params={"base": "truncated_hexagonal", "theta": 70.0},
          size=14),
        V("v_i_4612", "hankin", "shape", "earth", params={"base": "truncated_trihexagonal", "theta": 70.0},
          size=16),
        V("v_i_3464", "hankin", "shape", "triad", 8, params={"base": "rhombitrihexagonal", "theta": 60.0}),
        V("v_i_snub", "hankin", "shape", "analogous", 10, params={"base": "snub_square", "theta": 60.0}),
    ]),
]


def write_file(spec, path, width=1200):
    ops, box = build_scene(spec)
    ext = path.lower().rsplit(".", 1)[-1]
    if ext == "svg":
        write_svg(ops, box, path, width)
    elif ext == "pdf":
        from reportlab.pdfgen import canvas
        w = 600.0
        h = w * (box[3] - box[1]) / (box[2] - box[0])
        c = canvas.Canvas(path, pagesize=(w, h))
        draw_ops_pdf(c, ops, box, 0, 0, w, h)
        c.showPage()
        c.save()
    else:
        render_image(ops, box, width).save(path)


def scheme_name(s):
    name = T("s_" + s["scheme"])
    if s["scheme"] in SCHEME_OFFSETS or s["scheme"] in ("mono", "rainbow"):
        name += " (%s)" % CTD_STRINGS.get(_LANG, CTD_STRINGS["en"])["hue_names"][s["hue"] % 12].lower()
    return name


def caption_lines(v):
    cap = v["cap"]
    text = T(cap[0]) % cap[1:] if isinstance(cap, tuple) else T(cap)
    s = spec_defaults(v)
    col = s["colouring"]
    cname = T("c_" + col) if ("c_" + col) in STRINGS["en"] else col
    if v.get("colours") or col == "classic":
        return text, "%s: %s" % (T("colouring"), cname)
    return text, "%s: %s  ·  %s" % (T("colouring"), cname, scheme_name(s))


def paragraph(c, text, x, y, width, font="Helvetica", size=9.5, leading=13, colour=(.25, .25, .25)):
    from reportlab.lib.utils import simpleSplit
    c.setFont(font, size)
    c.setFillColorRGB(*colour)
    for line in simpleSplit(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def build_catalogue(path):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    W, H = A4
    M = 40
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle(T("title").title())
    page = [1]

    def footer():
        c.setFont("Helvetica", 7.5)
        c.setFillColorRGB(.5, .5, .5)
        c.drawString(M, 24, T("title"))
        c.drawRightString(W - M, 24, "%s %d" % (T("page"), page[0]))
        c.showPage()
        page[0] += 1

    # pages of each family, counted first for the contents
    per_page = 6
    starts, n = {}, 2
    for fam, _, vs in CATALOGUE:
        starts[fam] = n
        n += (len(vs) + per_page - 1) // per_page

    # ---- cover: title, introduction, colour schemes, contents
    c.setFillColorRGB(.12, .12, .12)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(M, H - 78, T("title"))
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(.35, .35, .35)
    c.drawString(M, H - 98, T("subtitle"))
    y = paragraph(c, T("intro"), M, H - 128, W - 2 * M)
    y -= 14
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(.12, .12, .12)
    c.drawString(M, y, T("schemes_t"))
    y = paragraph(c, T("schemes_d"), M, y - 16, W - 2 * M, size=8.5, leading=11.5)
    y -= 6
    for k, sch in enumerate(SCHEMES):
        col_x = M + (k % 2) * (W - 2 * M) / 2
        row_y = y - (k // 2) * 22
        s = {"scheme": sch, "hue": 4}
        cols = NAMED_PALETTES.get(sch) or palette(sch, 4, len(SCHEME_OFFSETS.get(sch, range(6))))
        for i, col in enumerate(cols):
            c.setFillColorRGB(*col)
            c.setStrokeColorRGB(.6, .6, .6)
            c.setLineWidth(.4)
            c.rect(col_x + i * 15, row_y - 4, 13, 13, fill=1, stroke=1)
        c.setFillColorRGB(.2, .2, .2)
        c.setFont("Helvetica", 8.5)
        c.drawString(col_x + 112, row_y, scheme_name(s))
    y -= (len(SCHEMES) + 1) // 2 * 22 + 14
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(.12, .12, .12)
    c.drawString(M, y, T("contents"))
    y -= 18
    for fam, art, vs in CATALOGUE:
        c.setFont("Helvetica", 9.5)
        c.setFillColorRGB(.2, .2, .2)
        c.drawString(M + 8, y, T("f_" + fam))
        c.setFillColorRGB(.55, .55, .55)
        c.drawString(M + 230, y, "Wikipedia: " + art)
        c.setFillColorRGB(.2, .2, .2)
        c.drawRightString(W - M, y, str(starts[fam]))
        y -= 13.5
    footer()

    # ---- family pages: header, then a 2 x 3 grid of panels
    pw, gap = (W - 2 * M - 18) / 2, 18
    ph = 168
    for fam, art, vs in CATALOGUE:
        for first in range(0, len(vs), per_page):
            c.setFillColorRGB(.12, .12, .12)
            c.setFont("Helvetica-Bold", 20)
            title = T("f_" + fam) + ("" if first == 0 else "  (%s)" % T("cont"))
            c.drawString(M, H - 66, title)
            c.setFont("Helvetica", 8.5)
            c.setFillColorRGB(.5, .5, .5)
            c.drawString(M, H - 82, "Wikipedia: " + art + "  —  en.wikipedia.org/wiki/" + art.replace(" ", "_"))
            paragraph(c, T("f_%s_d" % fam), M, H - 102, W - 2 * M)
            top = H - 160
            for n_, v in enumerate(vs[first:first + per_page]):
                col, row = n_ % 2, n_ // 2
                x = M + col * (pw + gap)
                y0 = top - row * (ph + 46) - ph
                spec = dict(v)
                spec["aspect"] = ph / pw
                ops, box = build_scene(spec)
                draw_ops_pdf(c, ops, box, x, y0, pw, ph)
                c.setStrokeColorRGB(.55, .55, .55)
                c.setLineWidth(.6)
                c.rect(x, y0, pw, ph, fill=0, stroke=1)
                line1, line2 = caption_lines(v)
                c.setFillColorRGB(.12, .12, .12)
                c.setFont("Helvetica-Bold", 8.6)
                from reportlab.lib.utils import simpleSplit
                yy = y0 - 12
                for ln in simpleSplit(line1, "Helvetica-Bold", 8.6, pw)[:2]:
                    c.drawString(x, yy, ln)
                    yy -= 10.5
                c.setFont("Helvetica", 7.6)
                c.setFillColorRGB(.42, .42, .42)
                c.drawString(x, yy, line2)
            footer()
    c.save()


# ==========================================================================
# 9. MAIN
# ==========================================================================
def parse_value(v):
    try:
        return float(v) if "." in v or "e" in v.lower() else int(v)
    except ValueError:
        return v


def main():
    global _LANG
    ap = argparse.ArgumentParser(description="Tilings and mosaics with colour schemes.")
    ap.add_argument("tiling", nargs="?", help="tiling to draw (see --list); without it, the PDF catalogue")
    ap.add_argument("--list", action="store_true", help="list tilings, colourings, schemes and parameters")
    ap.add_argument("-c", "--colouring", help="colouring (tiling's own, or: %s)" % ", ".join(UNIVERSAL))
    ap.add_argument("--scheme", choices=SCHEMES, help="colour scheme")
    ap.add_argument("--hue", help="base hue of the scheme: RYB step 0-11 or a name (red, blue-green ...)")
    ap.add_argument("--colours", help="your own colours instead of a scheme, e.g. '#1d3f8f,#f5f3ec'")
    ap.add_argument("-p", "--param", action="append", default=[], metavar="NAME=VALUE",
                    help="tiling parameter, e.g. ratio=3, angle=45, theta=60, base=hexagonal")
    ap.add_argument("--overlay", action="append", default=[], choices=["dual", "circles", "incircles", "edges"],
                    help="draw the dual, circles at the vertices, circles in the tiles, or edges by direction")
    ap.add_argument("--girih", type=float, metavar="ANGLE", help="draw Hankin / girih lines over the tiles")
    ap.add_argument("--size", type=float, help="width of the view in tile edges")
    ap.add_argument("--aspect", type=float, default=.75, help="height / width of the image")
    ap.add_argument("--width", type=int, default=1200, help="image width in pixels (PNG, SVG)")
    ap.add_argument("--seed", type=int, default=1, help="seed of the random colouring")
    ap.add_argument("--lang", default="en", choices=sorted(STRINGS), help="language of the catalogue")
    ap.add_argument("-o", "--out", help="output file: .png, .svg or .pdf")
    a = ap.parse_args()
    _LANG = a.lang
    if a.list:
        for key, t in TILINGS.items():
            own = ", ".join(t.colourings) or "-"
            pars = ", ".join("%s=%s" % kv for kv in t.params.items()) or "-"
            print("%-28s colourings: %s | params: %s" % (key, own, pars))
        print("\nuniversal colourings:", ", ".join(UNIVERSAL))
        print("schemes:", ", ".join(SCHEMES))
        print("hues:", ", ".join("%d %s" % kv for kv in enumerate(HUE_KEYS)))
        print("hankin bases:", ", ".join(TILINGS_BASE))
        return
    if not a.tiling:
        out = a.out or "tilings_%s.pdf" % a.lang
        build_catalogue(out)
        print("wrote", out)
        return
    if a.tiling not in TILINGS:
        ap.error("unknown tiling %r (see --list)" % a.tiling)
    hue = None
    if a.hue is not None:
        hue = int(a.hue) if a.hue.isdigit() else HUE_KEYS.index(a.hue.lower())
    spec = {"key": a.tiling, "colouring": a.colouring, "scheme": a.scheme, "hue": hue,
            "size": a.size, "aspect": a.aspect, "seed": a.seed, "overlay": a.overlay, "girih": a.girih,
            "params": dict((k, parse_value(v)) for k, v in (p.split("=", 1) for p in a.param)),
            "colours": [hexc(h.strip().lstrip("#")) for h in a.colours.split(",")] if a.colours else None}
    out = a.out or a.tiling + ".png"
    write_file(spec, out, a.width)
    print("wrote", out)


# ==========================================================================
# 10. TEXT (en, pt, es)
# ==========================================================================
STRINGS = {
    # ------------------------------------------------------------------ EN
    "en": {
        "title": "TILINGS AND MOSAICS",
        "subtitle": "Regular, semiregular, aperiodic and Islamic tilings, coloured with colour theory",
        "intro": "A tiling covers the plane with shapes, without gaps or overlaps. The same tiling "
                 "changes character with its colouring: by kind of tile, by orientation, by mirror "
                 "image, or so that neighbouring tiles always differ. Every page below draws the tilings "
                 "of one Wikipedia article with several colourings; the colours come from the colour "
                 "schemes of the RYB wheel or from traditional tile palettes. All of it is computed: "
                 "lattices of polygons, duals, Penrose deflation, the hat metatiles, a search for Wang "
                 "tilings and Hankin's method for star patterns.",
        "schemes_t": "Colour schemes",
        "schemes_d": "RYB schemes take hues at fixed steps of the 12-hue wheel from a base hue (here "
                     "red); when a tiling needs more colours than a scheme has, tints and shades of "
                     "the same hues are added. The named palettes copy traditional glazed tiles.",
        "contents": "Contents", "colouring": "Colouring", "cont": "continued", "page": "page",
        "c_single": "one colour", "c_kind": "by kind of tile", "c_shape": "by shape",
        "c_chirality": "by mirror image", "c_orientation": "by orientation",
        "c_proper": "neighbours differ", "c_random": "random", "c_rings": "rings from the centre",
        "c_classic": "the four edge colours", "c_scheme": "edge colours from a scheme",
        "c_checker": "checkerboard",
        "s_mono": "monochromatic", "s_analogous": "analogous", "s_complementary": "complementary",
        "s_split": "split complementary", "s_triad": "triad", "s_tetrad": "tetrad (rectangle)",
        "s_square": "square", "s_rainbow": "rainbow", "s_zellij": "zellij palette",
        "s_azulejo": "azulejo palette", "s_girih": "girih palette", "s_earth": "earth tones",
        "s_grey": "greys",
        "f_triangular": "Triangular tiling",
        "f_triangular_d": "Six equilateral triangles meet at every vertex. Its uniform colourings are named "
                          "by the colours around a vertex: 121212 alternates two colours, 121314 needs four. "
                          "Cutting the triangles further gives the kisrhombille and kisdeltile tilings.",
        "f_truncated_square": "Truncated square tiling",
        "f_truncated_square_d": "One square and two regular octagons at each vertex (4.8.8), the floor of "
                                "many kitchens. The squares can take two sizes, and in the limit half "
                                "of them vanish (chamfered tiling). Its dual is the tetrakis square tiling.",
        "f_hexagonal": "Hexagonal tiling",
        "f_hexagonal_d": "Three hexagons at each vertex, as in a honeycomb. Hexagons can be coloured "
                         "with 2, 3, 4 or 7 colours in a regular way; with 7 every hexagon touches all "
                         "the other colours. Cutting some hexagons into triangles gives 2-uniform tilings.",
        "f_trihexagonal": "Trihexagonal tiling",
        "f_trihexagonal_d": "Triangles and hexagons alternate around each vertex (3.6.3.6); its edges "
                            "are three families of straight lines, the kagome pattern of Japanese baskets. "
                            "Turning or resizing the triangles keeps the same structure.",
        "f_rhombille": "Rhombille tiling",
        "f_rhombille_d": "Identical 60° rhombi, three around one corner and six around the other: the dual "
                         "of the trihexagonal tiling. With three values of one hue it reads as a stack "
                         "of cubes, a pattern found on old floors such as Siena Cathedral.",
        "f_pythagorean": "Pythagorean tiling",
        "f_pythagorean_d": "Squares of two sizes, each touching four squares of the other size. It is the "
                           "picture behind a classic proof of Pythagoras' theorem, and a common floor "
                           "pattern (pinwheel or hopscotch).",
        "f_regular": "Regular polygons",
        "f_regular_d": "The eleven uniform (Archimedean) tilings by regular polygons: every vertex has "
                       "the same polygons around it, written as their numbers of sides (3.4.6.4 is "
                       "triangle, square, hexagon, square). Mixing vertex types gives k-uniform tilings.",
        "f_penrose": "Penrose tilings",
        "f_penrose_d": "Two tiles that cover the plane only without repeating: thick and thin rhombs "
                       "(P3), or kites and darts (P2). They are drawn by repeatedly cutting golden "
                       "triangles (deflation) and show five-fold symmetry everywhere.",
        "f_aperiodic": "Aperiodic tilings",
        "f_aperiodic_d": "Tilings that never repeat. The hat (2023) is a single shape, used with its "
                         "mirror image, that tiles only aperiodically; Robinson's six square tiles force "
                         "nested squares of ever larger sizes.",
        "f_herringbone": "Herringbone pattern",
        "f_herringbone_d": "Rectangles laid in a staircase, each at right angles to its neighbours: the "
                           "classic brick and parquet pattern. Longer bricks, a 45° turn or parallelograms "
                           "change its look; the basket weave pairs the bricks instead.",
        "f_pentagonal": "Pentagonal tilings",
        "f_pentagonal_d": "Regular pentagons cannot tile the plane, but 15 families of convex pentagons "
                          "can. Halving hexagons gives type 1; the duals of three uniform tilings give the "
                          "Cairo, prismatic and floret pentagonal tilings.",
        "f_cairo": "Cairo pentagonal tiling",
        "f_cairo_d": "Pentagons with four long sides and one short side, the dual of the snub square "
                     "tiling, named after the streets of Cairo. Four pentagons meet at some vertices, "
                     "three at others, and pairs of pentagons form hexagons.",
        "f_girih": "Girih tiles",
        "f_girih_d": "Five equal-sided tiles (decagon, pentagon, hexagon, bowtie, rhombus) used in Persian "
                     "architecture. Lines drawn on them cross every edge at its midpoint at 54°, so they "
                     "join across tiles into the visible star pattern.",
        "f_wang": "Wang tiles",
        "f_wang_d": "Squares with coloured edges, placed so that touching edges match and never turned. "
                    "The 11 tiles of Jeandel and Rao (2015) tile the plane only aperiodically; this "
                    "patch was found by a backtracking search.",
        "f_zellij": "Zellij",
        "f_zellij_d": "Moroccan and Andalusian mosaic of glazed pieces cut by hand, in white, green, black, "
                      "ochre and blues. Eight-pointed stars with crosses, and 6-, 8-, 10- and 12-pointed "
                      "star systems are typical.",
        "f_islamic": "Islamic geometric patterns",
        "f_islamic_d": "Star patterns made with Hankin's method of polygons in contact: from the middle of "
                       "each edge of a tiling two lines leave at a fixed angle until they meet. The base "
                       "tiling and the angle decide the stars; the straps are drawn as ribbons.",
        "v_uniform": "Uniform colouring %s",
        "v_tri_regular": "Regular triangular tiling {3,6}",
        "v_kisrhombille": "Kisrhombille: 30-60-90 triangles (dual of 4.6.12)",
        "v_triakis": "Kisdeltile: 30-30-120 triangles (dual of 3.12.12)",
        "v_ts_plain": "Truncated square tiling 4.8.8",
        "v_circlepack": "Circle packing: a circle at every vertex",
        "v_ts_alt": "Squares of alternating sizes",
        "v_ts_chamfer": "Chamfered square tiling (small squares vanish)",
        "v_tetrakis": "Tetrakis square tiling (dual of 4.8.8)",
        "v_dual_overlay": "With its dual drawn over it",
        "v_hex_regular": "Regular hexagonal tiling {6,3}",
        "v_hex_2": "Two colours, in rows",
        "v_hex_21": "Two colours, one hexagon in three",
        "v_hex_3": "Three colours: neighbours always differ",
        "v_hex_4": "Four colours",
        "v_hex_7": "Seven colours: each hexagon touches all the others",
        "v_kissing": "Densest packing of circles",
        "v_dissect1": "2-uniform: a third of the hexagons cut into triangles",
        "v_dissect2": "2-uniform: two thirds of the hexagons cut into triangles",
        "v_kagome": "Kagome: edges coloured by direction",
        "v_unequal": "Triangles of two sizes",
        "v_twisted": "Turned triangles: the hexagons become stars",
        "v_twisted2": "Turned further",
        "v_hexstar": "Hexagons and six-pointed stars",
        "v_rhombille": "Rhombille tiling: 60° rhombi",
        "v_siena": "Three shades by orientation, as in Siena Cathedral",
        "v_cubes": "Stacked cubes: one hue in three values",
        "v_rh_dual": "Over its dual, the trihexagonal tiling",
        "v_skew": "Skewed and turned: parallelograms",
        "v_pyth_half": "Squares of sides 1 and 1/2",
        "v_pyth_golden": "Sides in the golden ratio",
        "v_pyth_random": "Sides 1 and 0.3, random earth tones",
        "n_triangular": "3.3.3.3.3.3 triangular",
        "n_square": "4.4.4.4 square",
        "n_hexagonal": "6.6.6 hexagonal",
        "n_trihexagonal": "3.6.3.6 trihexagonal",
        "n_truncated_hexagonal": "3.12.12 truncated hexagonal",
        "n_truncated_square": "4.8.8 truncated square",
        "n_truncated_trihexagonal": "4.6.12 truncated trihexagonal",
        "n_rhombitrihexagonal": "3.4.6.4 rhombitrihexagonal",
        "n_snub_hexagonal": "3.3.3.3.6 snub hexagonal",
        "n_elongated_triangular": "3.3.3.4.4 elongated triangular",
        "n_snub_square": "3.3.4.3.4 snub square",
        "v_p3": "P3: thick and thin rhombs",
        "v_p3_ori": "P3 by the ten orientations of the rhombs",
        "v_p3_proper": "P3, neighbouring rhombs differ",
        "v_p3_rings": "P3 in rings round the centre",
        "v_p2": "P2: kites and darts",
        "v_p2_rings": "P2 in rings round the centre",
        "v_p2_proper": "P2, neighbouring tiles differ",
        "v_hat": "The hat: one shape and its mirror image",
        "v_hat_ori": "Hats by orientation",
        "v_robinson": "Robinson tiles: their marks draw nested squares",
        "v_hb_2": "Bricks 2:1",
        "v_hb_45": "Turned 45°",
        "v_hb_3": "Bricks 3:1",
        "v_hb_long": "Long boards, about 6.6:1",
        "v_hb_par": "Parallelograms",
        "v_basket": "Basket weave",
        "v_halves": "Type 1: hexagons cut in half",
        "v_halves_alt": "Type 1, cut in three directions",
        "v_cairo_p": "Cairo tiling (types 2 and 4)",
        "v_prismatic": "Prismatic pentagonal (dual of 3.3.3.4.4)",
        "v_floret": "Floret pentagonal (dual of 3.3.3.3.6)",
        "v_floret_proper": "Floret pentagonal, neighbours differ",
        "v_cairo": "Cairo tiling: dual of the snub square tiling",
        "v_cairo_ori": "Four orientations",
        "v_cairo_proper": "Neighbouring pentagons differ",
        "v_cairo_dual": "Over its dual, the snub square tiling",
        "v_girih_tiles": "Decagons and bowties",
        "v_girih_lines": "Girih lines, crossing every edge at 54°",
        "v_girih_star": "The girih pattern, coloured",
        "v_girih_star2": "The same pattern, zellij palette",
        "v_wang": "Jeandel–Rao: 11 tiles, 4 colours, aperiodic",
        "v_wang_scheme": "The same tiles, colours from a scheme",
        "v_stars_crosses": "Eight-pointed stars and crosses",
        "v_sc_azulejo": "Stars and crosses in azulejo blues",
        "v_z8": "Eight-pointed stars from octagons in contact",
        "v_z12": "Twelve-, six- and four-pointed stars",
        "v_z10": "Ten-pointed stars (girih base)",
        "v_i6": "Six-pointed stars from hexagons in contact",
        "v_i_sq": "Octagons and four-pointed stars from squares",
        "v_i_31212": "Twelve-pointed stars from 3.12.12",
        "v_i_4612": "Rosettes from 4.6.12",
        "v_i_3464": "Stars from 3.4.6.4",
        "v_i_snub": "Stars from the snub square tiling",
    },
    # ------------------------------------------------------------------ PT
    "pt": {
        "title": "PAVIMENTAÇÕES E MOSAICOS",
        "subtitle": "Pavimentações regulares, semirregulares, aperiódicas e islâmicas, coloridas com teoria da cor",
        "intro": "Uma pavimentação cobre o plano com formas, sem buracos nem sobreposições. A mesma "
                 "pavimentação muda de carácter com a coloração: pelo tipo de peça, pela orientação, pela "
                 "imagem ao espelho, ou de modo que peças vizinhas sejam sempre diferentes. Cada página "
                 "desenha as pavimentações de um artigo da Wikipedia com várias colorações; as cores vêm "
                 "dos esquemas da roda RYB ou de paletas tradicionais de azulejos. Tudo é calculado: "
                 "redes de polígonos, duais, a deflação de Penrose, as metapeças do chapéu, uma procura "
                 "de pavimentações de Wang e o método de Hankin para os padrões de estrelas.",
        "schemes_t": "Esquemas de cores",
        "schemes_d": "Os esquemas RYB escolhem matizes a passos fixos da roda de 12 cores a partir de um "
                     "matiz de base (aqui o vermelho); quando uma pavimentação precisa de mais cores do "
                     "que o esquema tem, juntam-se tintas e sombras dos mesmos matizes. As paletas com "
                     "nome copiam azulejos tradicionais.",
        "contents": "Índice", "colouring": "Coloração", "cont": "continuação", "page": "página",
        "c_single": "uma cor", "c_kind": "por tipo de peça", "c_shape": "por forma",
        "c_chirality": "por imagem ao espelho", "c_orientation": "por orientação",
        "c_proper": "vizinhas diferentes", "c_random": "aleatória", "c_rings": "anéis a partir do centro",
        "c_classic": "as quatro cores das arestas", "c_scheme": "cores das arestas de um esquema",
        "c_checker": "xadrez",
        "s_mono": "monocromático", "s_analogous": "análogo", "s_complementary": "complementar",
        "s_split": "complementar dividido", "s_triad": "tríade", "s_tetrad": "tétrade (retângulo)",
        "s_square": "quadrado", "s_rainbow": "arco-íris", "s_zellij": "paleta zellij",
        "s_azulejo": "paleta de azulejo", "s_girih": "paleta girih", "s_earth": "tons de terra",
        "s_grey": "cinzentos",
        "f_triangular": "Pavimentação triangular",
        "f_triangular_d": "Seis triângulos equiláteros encontram-se em cada vértice. As colorações uniformes "
                          "têm o nome das cores à volta de um vértice: 121212 alterna duas cores, 121314 "
                          "precisa de quatro. Cortando mais os triângulos obtêm-se o kisrhombille e o kisdeltile.",
        "f_truncated_square": "Pavimentação quadrada truncada",
        "f_truncated_square_d": "Um quadrado e dois octógonos regulares em cada vértice (4.8.8), o chão de "
                                "muitas cozinhas. Os quadrados podem ter dois tamanhos e, no limite, metade "
                                "desaparece (pavimentação chanfrada). A dual é a pavimentação tetrakis.",
        "f_hexagonal": "Pavimentação hexagonal",
        "f_hexagonal_d": "Três hexágonos em cada vértice, como num favo de mel. Os hexágonos podem ser "
                         "coloridos de forma regular com 2, 3, 4 ou 7 cores; com 7, cada hexágono toca "
                         "todas as outras cores. Cortando alguns em triângulos obtêm-se pavimentações 2-uniformes.",
        "f_trihexagonal": "Pavimentação tri-hexagonal",
        "f_trihexagonal_d": "Triângulos e hexágonos alternam à volta de cada vértice (3.6.3.6); as arestas "
                            "formam três famílias de retas, o padrão kagome dos cestos japoneses. Rodar ou "
                            "mudar o tamanho dos triângulos mantém a mesma estrutura.",
        "f_rhombille": "Pavimentação de losangos",
        "f_rhombille_d": "Losangos iguais de 60°, três à volta de um canto e seis à volta do outro: a dual "
                         "da pavimentação tri-hexagonal. Com três valores de um matiz parece uma pilha de "
                         "cubos, um padrão de pavimentos antigos como o da Catedral de Siena.",
        "f_pythagorean": "Pavimentação pitagórica",
        "f_pythagorean_d": "Quadrados de dois tamanhos, cada um a tocar quatro quadrados do outro tamanho. "
                           "É a figura de uma demonstração clássica do teorema de Pitágoras e um padrão "
                           "comum de pavimentos.",
        "f_regular": "Polígonos regulares",
        "f_regular_d": "As onze pavimentações uniformes (arquimedianas) por polígonos regulares: todos os "
                       "vértices têm os mesmos polígonos à volta, escritos pelo número de lados (3.4.6.4 é "
                       "triângulo, quadrado, hexágono, quadrado). Misturar tipos de vértice dá "
                       "pavimentações k-uniformes.",
        "f_penrose": "Pavimentações de Penrose",
        "f_penrose_d": "Duas peças que só cobrem o plano sem se repetir: losangos largos e estreitos (P3), "
                       "ou papagaios e dardos (P2). Desenham-se cortando repetidamente triângulos de ouro "
                       "(deflação) e mostram simetria de ordem cinco em todo o lado.",
        "f_aperiodic": "Pavimentações aperiódicas",
        "f_aperiodic_d": "Pavimentações que nunca se repetem. O chapéu (2023) é uma só forma, usada com a "
                         "sua imagem ao espelho, que só pavimenta de forma aperiódica; as seis peças "
                         "quadradas de Robinson obrigam a quadrados encaixados cada vez maiores.",
        "f_herringbone": "Espinha de peixe",
        "f_herringbone_d": "Retângulos em escada, cada um em ângulo reto com os vizinhos: o padrão clássico "
                           "de tijolo e parquet. Peças mais compridas, uma rotação de 45° ou "
                           "paralelogramos mudam o aspeto; a cestaria junta as peças aos pares.",
        "f_pentagonal": "Pavimentações pentagonais",
        "f_pentagonal_d": "Os pentágonos regulares não pavimentam o plano, mas 15 famílias de pentágonos "
                          "convexos sim. Cortar hexágonos ao meio dá o tipo 1; as duais de três "
                          "pavimentações uniformes dão as pentagonais do Cairo, prismática e em flor.",
        "f_cairo": "Pavimentação pentagonal do Cairo",
        "f_cairo_d": "Pentágonos com quatro lados compridos e um curto, a dual da pavimentação quadrada "
                     "achatada, com o nome das ruas do Cairo. Quatro pentágonos encontram-se nalguns "
                     "vértices, três noutros, e os pares de pentágonos formam hexágonos.",
        "f_girih": "Peças girih",
        "f_girih_d": "Cinco peças de lados iguais (decágono, pentágono, hexágono, laço, losango) da "
                     "arquitetura persa. As linhas desenhadas nelas cruzam cada aresta a meio, a 54°, e "
                     "por isso ligam-se de peça para peça no padrão de estrelas visível.",
        "f_wang": "Peças de Wang",
        "f_wang_d": "Quadrados com arestas coloridas, colocados de modo que as arestas em contacto sejam "
                    "iguais, e nunca rodados. As 11 peças de Jeandel e Rao (2015) só pavimentam de forma "
                    "aperiódica; este pedaço foi encontrado por uma procura com retrocesso.",
        "f_zellij": "Zellij",
        "f_zellij_d": "Mosaico marroquino e andaluz de peças vidradas cortadas à mão, em branco, verde, "
                      "preto, ocre e azuis. São típicas as estrelas de oito pontas com cruzes e os sistemas "
                      "de estrelas de 6, 8, 10 e 12 pontas.",
        "f_islamic": "Padrões geométricos islâmicos",
        "f_islamic_d": "Padrões de estrelas feitos com o método de Hankin dos polígonos em contacto: do "
                       "meio de cada aresta de uma pavimentação saem duas linhas com um ângulo fixo até se "
                       "encontrarem. A pavimentação de base e o ângulo decidem as estrelas; as linhas são "
                       "desenhadas como fitas.",
        "v_uniform": "Coloração uniforme %s",
        "v_tri_regular": "Pavimentação triangular regular {3,6}",
        "v_kisrhombille": "Kisrhombille: triângulos 30-60-90 (dual de 4.6.12)",
        "v_triakis": "Kisdeltile: triângulos 30-30-120 (dual de 3.12.12)",
        "v_ts_plain": "Pavimentação quadrada truncada 4.8.8",
        "v_circlepack": "Empacotamento de círculos: um círculo em cada vértice",
        "v_ts_alt": "Quadrados de tamanhos alternados",
        "v_ts_chamfer": "Pavimentação chanfrada (os quadrados pequenos desaparecem)",
        "v_tetrakis": "Pavimentação tetrakis (dual de 4.8.8)",
        "v_dual_overlay": "Com a dual desenhada por cima",
        "v_hex_regular": "Pavimentação hexagonal regular {6,3}",
        "v_hex_2": "Duas cores, em filas",
        "v_hex_21": "Duas cores, um hexágono em cada três",
        "v_hex_3": "Três cores: as vizinhas são sempre diferentes",
        "v_hex_4": "Quatro cores",
        "v_hex_7": "Sete cores: cada hexágono toca todas as outras",
        "v_kissing": "O empacotamento de círculos mais denso",
        "v_dissect1": "2-uniforme: um terço dos hexágonos cortados em triângulos",
        "v_dissect2": "2-uniforme: dois terços dos hexágonos cortados em triângulos",
        "v_kagome": "Kagome: arestas coloridas pela direção",
        "v_unequal": "Triângulos de dois tamanhos",
        "v_twisted": "Triângulos rodados: os hexágonos tornam-se estrelas",
        "v_twisted2": "Rodados ainda mais",
        "v_hexstar": "Hexágonos e estrelas de seis pontas",
        "v_rhombille": "Pavimentação de losangos de 60°",
        "v_siena": "Três tons pela orientação, como na Catedral de Siena",
        "v_cubes": "Cubos empilhados: um matiz em três valores",
        "v_rh_dual": "Sobre a dual, a pavimentação tri-hexagonal",
        "v_skew": "Inclinada e rodada: paralelogramos",
        "v_pyth_half": "Quadrados de lados 1 e 1/2",
        "v_pyth_golden": "Lados na razão de ouro",
        "v_pyth_random": "Lados 1 e 0,3, tons de terra ao acaso",
        "n_triangular": "3.3.3.3.3.3 triangular",
        "n_square": "4.4.4.4 quadrada",
        "n_hexagonal": "6.6.6 hexagonal",
        "n_trihexagonal": "3.6.3.6 tri-hexagonal",
        "n_truncated_hexagonal": "3.12.12 hexagonal truncada",
        "n_truncated_square": "4.8.8 quadrada truncada",
        "n_truncated_trihexagonal": "4.6.12 tri-hexagonal truncada",
        "n_rhombitrihexagonal": "3.4.6.4 rombi-tri-hexagonal",
        "n_snub_hexagonal": "3.3.3.3.6 hexagonal achatada",
        "n_elongated_triangular": "3.3.3.4.4 triangular alongada",
        "n_snub_square": "3.3.4.3.4 quadrada achatada",
        "v_p3": "P3: losangos largos e estreitos",
        "v_p3_ori": "P3 pelas dez orientações dos losangos",
        "v_p3_proper": "P3, losangos vizinhos diferentes",
        "v_p3_rings": "P3 em anéis à volta do centro",
        "v_p2": "P2: papagaios e dardos",
        "v_p2_rings": "P2 em anéis à volta do centro",
        "v_p2_proper": "P2, peças vizinhas diferentes",
        "v_hat": "O chapéu: uma forma e a sua imagem ao espelho",
        "v_hat_ori": "Chapéus pela orientação",
        "v_robinson": "Peças de Robinson: as marcas desenham quadrados encaixados",
        "v_hb_2": "Tijolos 2:1",
        "v_hb_45": "Rodada 45°",
        "v_hb_3": "Tijolos 3:1",
        "v_hb_long": "Tábuas compridas, cerca de 6,6:1",
        "v_hb_par": "Paralelogramos",
        "v_basket": "Cestaria",
        "v_halves": "Tipo 1: hexágonos cortados ao meio",
        "v_halves_alt": "Tipo 1, cortes em três direções",
        "v_cairo_p": "Pavimentação do Cairo (tipos 2 e 4)",
        "v_prismatic": "Pentagonal prismática (dual de 3.3.3.4.4)",
        "v_floret": "Pentagonal em flor (dual de 3.3.3.3.6)",
        "v_floret_proper": "Pentagonal em flor, vizinhas diferentes",
        "v_cairo": "Pavimentação do Cairo: dual da quadrada achatada",
        "v_cairo_ori": "Quatro orientações",
        "v_cairo_proper": "Pentágonos vizinhos diferentes",
        "v_cairo_dual": "Sobre a dual, a pavimentação quadrada achatada",
        "v_girih_tiles": "Decágonos e laços",
        "v_girih_lines": "Linhas girih, que cruzam cada aresta a 54°",
        "v_girih_star": "O padrão girih, colorido",
        "v_girih_star2": "O mesmo padrão, paleta zellij",
        "v_wang": "Jeandel–Rao: 11 peças, 4 cores, aperiódica",
        "v_wang_scheme": "As mesmas peças, cores de um esquema",
        "v_stars_crosses": "Estrelas de oito pontas e cruzes",
        "v_sc_azulejo": "Estrelas e cruzes em azuis de azulejo",
        "v_z8": "Estrelas de oito pontas de octógonos em contacto",
        "v_z12": "Estrelas de doze, seis e quatro pontas",
        "v_z10": "Estrelas de dez pontas (base girih)",
        "v_i6": "Estrelas de seis pontas de hexágonos em contacto",
        "v_i_sq": "Octógonos e estrelas de quatro pontas de quadrados",
        "v_i_31212": "Estrelas de doze pontas a partir de 3.12.12",
        "v_i_4612": "Rosáceas a partir de 4.6.12",
        "v_i_3464": "Estrelas a partir de 3.4.6.4",
        "v_i_snub": "Estrelas a partir da quadrada achatada",
    },
    # ------------------------------------------------------------------ ES
    "es": {
        "title": "TESELADOS Y MOSAICOS",
        "subtitle": "Teselados regulares, semirregulares, aperiódicos e islámicos, coloreados con teoría del color",
        "intro": "Un teselado cubre el plano con formas, sin huecos ni solapamientos. El mismo teselado "
                 "cambia de carácter con el coloreado: por tipo de pieza, por orientación, por imagen "
                 "especular, o de modo que las piezas vecinas siempre sean distintas. Cada página dibuja "
                 "los teselados de un artículo de Wikipedia con varios coloreados; los colores vienen de "
                 "los esquemas de la rueda RYB o de paletas tradicionales de azulejos. Todo se calcula: "
                 "redes de polígonos, duales, la deflación de Penrose, las metapiezas del sombrero, una "
                 "búsqueda de teselados de Wang y el método de Hankin para los patrones de estrellas.",
        "schemes_t": "Esquemas de color",
        "schemes_d": "Los esquemas RYB toman matices a pasos fijos de la rueda de 12 colores a partir de "
                     "un matiz base (aquí el rojo); cuando un teselado necesita más colores de los que "
                     "tiene el esquema, se añaden tintes y sombras de los mismos matices. Las paletas con "
                     "nombre copian azulejos tradicionales.",
        "contents": "Índice", "colouring": "Coloreado", "cont": "continuación", "page": "página",
        "c_single": "un color", "c_kind": "por tipo de pieza", "c_shape": "por forma",
        "c_chirality": "por imagen especular", "c_orientation": "por orientación",
        "c_proper": "vecinas distintas", "c_random": "aleatorio", "c_rings": "anillos desde el centro",
        "c_classic": "los cuatro colores de las aristas", "c_scheme": "colores de las aristas de un esquema",
        "c_checker": "tablero de ajedrez",
        "s_mono": "monocromático", "s_analogous": "análogo", "s_complementary": "complementario",
        "s_split": "complementario dividido", "s_triad": "tríada", "s_tetrad": "tétrada (rectángulo)",
        "s_square": "cuadrado", "s_rainbow": "arcoíris", "s_zellij": "paleta zellige",
        "s_azulejo": "paleta de azulejo", "s_girih": "paleta girih", "s_earth": "tonos tierra",
        "s_grey": "grises",
        "f_triangular": "Teselado triangular",
        "f_triangular_d": "Seis triángulos equiláteros se encuentran en cada vértice. Los coloreados uniformes "
                          "se nombran por los colores alrededor de un vértice: 121212 alterna dos colores, "
                          "121314 necesita cuatro. Cortando más los triángulos se obtienen el kisrhombille y "
                          "el kisdeltile.",
        "f_truncated_square": "Teselado cuadrado truncado",
        "f_truncated_square_d": "Un cuadrado y dos octógonos regulares en cada vértice (4.8.8), el suelo de "
                                "muchas cocinas. Los cuadrados pueden tener dos tamaños y, en el límite, la "
                                "mitad desaparece (teselado biselado). Su dual es el teselado tetrakis.",
        "f_hexagonal": "Teselado hexagonal",
        "f_hexagonal_d": "Tres hexágonos en cada vértice, como en un panal. Los hexágonos pueden colorearse "
                         "de forma regular con 2, 3, 4 o 7 colores; con 7, cada hexágono toca todos los "
                         "demás colores. Cortando algunos en triángulos salen teselados 2-uniformes.",
        "f_trihexagonal": "Teselado trihexagonal",
        "f_trihexagonal_d": "Triángulos y hexágonos se alternan alrededor de cada vértice (3.6.3.6); las "
                            "aristas forman tres familias de rectas, el patrón kagome de las cestas "
                            "japonesas. Girar o cambiar el tamaño de los triángulos mantiene la estructura.",
        "f_rhombille": "Teselado de rombos",
        "f_rhombille_d": "Rombos iguales de 60°, tres alrededor de una esquina y seis alrededor de la otra: "
                         "el dual del teselado trihexagonal. Con tres valores de un matiz parece una pila "
                         "de cubos, un patrón de suelos antiguos como el de la Catedral de Siena.",
        "f_pythagorean": "Teselado pitagórico",
        "f_pythagorean_d": "Cuadrados de dos tamaños, cada uno tocando cuatro cuadrados del otro tamaño. Es "
                           "la figura de una demostración clásica del teorema de Pitágoras y un patrón "
                           "común de suelos.",
        "f_regular": "Polígonos regulares",
        "f_regular_d": "Los once teselados uniformes (arquimedianos) por polígonos regulares: todos los "
                       "vértices tienen los mismos polígonos alrededor, escritos por su número de lados "
                       "(3.4.6.4 es triángulo, cuadrado, hexágono, cuadrado). Mezclar tipos de vértice da "
                       "teselados k-uniformes.",
        "f_penrose": "Teselados de Penrose",
        "f_penrose_d": "Dos piezas que solo cubren el plano sin repetirse: rombos anchos y estrechos (P3), "
                       "o cometas y dardos (P2). Se dibujan cortando repetidamente triángulos áureos "
                       "(deflación) y muestran simetría de orden cinco en todas partes.",
        "f_aperiodic": "Teselados aperiódicos",
        "f_aperiodic_d": "Teselados que nunca se repiten. El sombrero (2023) es una sola forma, usada con "
                         "su imagen especular, que solo tesela de forma aperiódica; las seis piezas "
                         "cuadradas de Robinson obligan a cuadrados anidados cada vez mayores.",
        "f_herringbone": "Espiga",
        "f_herringbone_d": "Rectángulos en escalera, cada uno en ángulo recto con sus vecinos: el patrón "
                           "clásico de ladrillo y parqué. Piezas más largas, un giro de 45° o "
                           "paralelogramos cambian su aspecto; la cestería junta las piezas por pares.",
        "f_pentagonal": "Teselados pentagonales",
        "f_pentagonal_d": "Los pentágonos regulares no teselan el plano, pero 15 familias de pentágonos "
                          "convexos sí. Partir hexágonos por la mitad da el tipo 1; los duales de tres "
                          "teselados uniformes dan los pentagonales de El Cairo, prismático y en flor.",
        "f_cairo": "Teselado pentagonal de El Cairo",
        "f_cairo_d": "Pentágonos con cuatro lados largos y uno corto, el dual del teselado cuadrado "
                     "achatado, con el nombre de las calles de El Cairo. Cuatro pentágonos se encuentran "
                     "en algunos vértices, tres en otros, y los pares de pentágonos forman hexágonos.",
        "f_girih": "Piezas girih",
        "f_girih_d": "Cinco piezas de lados iguales (decágono, pentágono, hexágono, pajarita, rombo) de la "
                     "arquitectura persa. Las líneas dibujadas en ellas cruzan cada arista por su mitad a "
                     "54°, y por eso se unen de pieza en pieza en el patrón de estrellas visible.",
        "f_wang": "Baldosas de Wang",
        "f_wang_d": "Cuadrados con aristas de colores, colocados de modo que las aristas en contacto "
                    "coincidan, y nunca girados. Las 11 baldosas de Jeandel y Rao (2015) solo teselan de "
                    "forma aperiódica; este trozo se encontró con una búsqueda con retroceso.",
        "f_zellij": "Zellige",
        "f_zellij_d": "Mosaico marroquí y andalusí de piezas vidriadas cortadas a mano, en blanco, verde, "
                      "negro, ocre y azules. Son típicas las estrellas de ocho puntas con cruces y los "
                      "sistemas de estrellas de 6, 8, 10 y 12 puntas.",
        "f_islamic": "Patrones geométricos islámicos",
        "f_islamic_d": "Patrones de estrellas hechos con el método de Hankin de los polígonos en contacto: "
                       "desde la mitad de cada arista de un teselado salen dos líneas con un ángulo fijo "
                       "hasta encontrarse. El teselado base y el ángulo deciden las estrellas; las líneas "
                       "se dibujan como cintas.",
        "v_uniform": "Coloreado uniforme %s",
        "v_tri_regular": "Teselado triangular regular {3,6}",
        "v_kisrhombille": "Kisrhombille: triángulos 30-60-90 (dual de 4.6.12)",
        "v_triakis": "Kisdeltile: triángulos 30-30-120 (dual de 3.12.12)",
        "v_ts_plain": "Teselado cuadrado truncado 4.8.8",
        "v_circlepack": "Empaquetamiento de círculos: un círculo en cada vértice",
        "v_ts_alt": "Cuadrados de tamaños alternos",
        "v_ts_chamfer": "Teselado biselado (los cuadrados pequeños desaparecen)",
        "v_tetrakis": "Teselado tetrakis (dual de 4.8.8)",
        "v_dual_overlay": "Con su dual dibujado encima",
        "v_hex_regular": "Teselado hexagonal regular {6,3}",
        "v_hex_2": "Dos colores, en filas",
        "v_hex_21": "Dos colores, un hexágono de cada tres",
        "v_hex_3": "Tres colores: las vecinas siempre son distintas",
        "v_hex_4": "Cuatro colores",
        "v_hex_7": "Siete colores: cada hexágono toca todos los demás",
        "v_kissing": "El empaquetamiento de círculos más denso",
        "v_dissect1": "2-uniforme: un tercio de los hexágonos cortados en triángulos",
        "v_dissect2": "2-uniforme: dos tercios de los hexágonos cortados en triángulos",
        "v_kagome": "Kagome: aristas coloreadas por dirección",
        "v_unequal": "Triángulos de dos tamaños",
        "v_twisted": "Triángulos girados: los hexágonos se vuelven estrellas",
        "v_twisted2": "Girados aún más",
        "v_hexstar": "Hexágonos y estrellas de seis puntas",
        "v_rhombille": "Teselado de rombos de 60°",
        "v_siena": "Tres tonos por orientación, como en la Catedral de Siena",
        "v_cubes": "Cubos apilados: un matiz en tres valores",
        "v_rh_dual": "Sobre su dual, el teselado trihexagonal",
        "v_skew": "Inclinado y girado: paralelogramos",
        "v_pyth_half": "Cuadrados de lados 1 y 1/2",
        "v_pyth_golden": "Lados en la proporción áurea",
        "v_pyth_random": "Lados 1 y 0,3, tonos tierra al azar",
        "n_triangular": "3.3.3.3.3.3 triangular",
        "n_square": "4.4.4.4 cuadrado",
        "n_hexagonal": "6.6.6 hexagonal",
        "n_trihexagonal": "3.6.3.6 trihexagonal",
        "n_truncated_hexagonal": "3.12.12 hexagonal truncado",
        "n_truncated_square": "4.8.8 cuadrado truncado",
        "n_truncated_trihexagonal": "4.6.12 trihexagonal truncado",
        "n_rhombitrihexagonal": "3.4.6.4 rombitrihexagonal",
        "n_snub_hexagonal": "3.3.3.3.6 hexagonal achatado",
        "n_elongated_triangular": "3.3.3.4.4 triangular alargado",
        "n_snub_square": "3.3.4.3.4 cuadrado achatado",
        "v_p3": "P3: rombos anchos y estrechos",
        "v_p3_ori": "P3 por las diez orientaciones de los rombos",
        "v_p3_proper": "P3, rombos vecinos distintos",
        "v_p3_rings": "P3 en anillos alrededor del centro",
        "v_p2": "P2: cometas y dardos",
        "v_p2_rings": "P2 en anillos alrededor del centro",
        "v_p2_proper": "P2, piezas vecinas distintas",
        "v_hat": "El sombrero: una forma y su imagen especular",
        "v_hat_ori": "Sombreros por orientación",
        "v_robinson": "Baldosas de Robinson: sus marcas dibujan cuadrados anidados",
        "v_hb_2": "Ladrillos 2:1",
        "v_hb_45": "Girado 45°",
        "v_hb_3": "Ladrillos 3:1",
        "v_hb_long": "Tablas largas, cerca de 6,6:1",
        "v_hb_par": "Paralelogramos",
        "v_basket": "Cestería",
        "v_halves": "Tipo 1: hexágonos partidos por la mitad",
        "v_halves_alt": "Tipo 1, cortes en tres direcciones",
        "v_cairo_p": "Teselado de El Cairo (tipos 2 y 4)",
        "v_prismatic": "Pentagonal prismático (dual de 3.3.3.4.4)",
        "v_floret": "Pentagonal en flor (dual de 3.3.3.3.6)",
        "v_floret_proper": "Pentagonal en flor, vecinas distintas",
        "v_cairo": "Teselado de El Cairo: dual del cuadrado achatado",
        "v_cairo_ori": "Cuatro orientaciones",
        "v_cairo_proper": "Pentágonos vecinos distintos",
        "v_cairo_dual": "Sobre su dual, el teselado cuadrado achatado",
        "v_girih_tiles": "Decágonos y pajaritas",
        "v_girih_lines": "Líneas girih, que cruzan cada arista a 54°",
        "v_girih_star": "El patrón girih, coloreado",
        "v_girih_star2": "El mismo patrón, paleta zellige",
        "v_wang": "Jeandel–Rao: 11 baldosas, 4 colores, aperiódico",
        "v_wang_scheme": "Las mismas baldosas, colores de un esquema",
        "v_stars_crosses": "Estrellas de ocho puntas y cruces",
        "v_sc_azulejo": "Estrellas y cruces en azules de azulejo",
        "v_z8": "Estrellas de ocho puntas de octógonos en contacto",
        "v_z12": "Estrellas de doce, seis y cuatro puntas",
        "v_z10": "Estrellas de diez puntas (base girih)",
        "v_i6": "Estrellas de seis puntas de hexágonos en contacto",
        "v_i_sq": "Octógonos y estrellas de cuatro puntas de cuadrados",
        "v_i_31212": "Estrellas de doce puntas a partir de 3.12.12",
        "v_i_4612": "Rosetones a partir de 4.6.12",
        "v_i_3464": "Estrellas a partir de 3.4.6.4",
        "v_i_snub": "Estrellas a partir del cuadrado achatado",
    },
}


if __name__ == "__main__":
    main()
