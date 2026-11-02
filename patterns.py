#!/usr/bin/env python3
"""
patterns.py
-----------
Decorated and special mosaics, built on the engine of tilings.py (palettes,
colourings, PNG / SVG / PDF output, sheets, preview window and catalogue):

  - facets: every tile of any tiling cut into triangles from its centre and lit
    from one side, so it reads as a pyramid (studs, 3D stars, hourglass blocks);
  - bands: concentric bands round the centre or a corner of each tile (courthouse
    steps, log cabin, striped pyramids), in a ramp or a sweep of hues;
  - isometric voxels: cubes, Rubik cubes, Y tripods and bar frameworks drawn with
    three shades, one per face direction;
  - quilt layouts of half-square triangles (pinwheels, diamonds, chevrons ...);
  - jigsaw puzzles, woven strips and kaleidoscopic beadwork in pixels;
  - mazes (random, seamless), square spirals and Greek keys, flat or isometric,
    and whirling polygons whose cut-off triangles make spiral arms.

    pip install reportlab pillow
    python3 patterns.py                         # catalogue -> patterns_en.pdf
    python3 patterns.py --lang pt               # Portuguese catalogue
    python3 patterns.py --list                  # patterns, colourings, parameters
    python3 patterns.py --show                  # preview window
    python3 patterns.py facets -p base=triangular --scheme triad -o stars.png
    python3 patterns.py bands -p bands=7 -p anchor=alternate --scheme sweep -o cabin.svg
    python3 patterns.py rubik -c rings --scheme rainbow -o rubik.pdf
    python3 patterns.py maze -p seed=7 -c flow --scheme rainbow -o maze.png
    python3 patterns.py spiral -p link=1 -p flat=1 -o greek_key.svg

Every option of tilings.py works here too (--scheme, --hue, --colours, -c, -p,
--vary, sheets of several patterns, --show ...).
"""
import math
import random
import sys

import tilings as tl
from tilings import Patch, Tile, add, ccw, centroid, mul, sub, unit

S3 = math.sqrt(3)


# ==========================================================================
# 1. FACETS AND BANDS ON ANY TILING
# ==========================================================================
def _anchor(rule, pts, i, j, seed):
    """Where the bands of a tile shrink to: its centre, or one of its corners."""
    m = len(pts)
    if rule == "centre":
        return centroid(pts), None
    if rule == "alternate":
        v = 0 if (i + j) % 2 == 0 else m // 2
    elif rule == "pinwheel":
        v = (0, 1, 3, 2)[(i % 2) + 2 * (j % 2)] % m
    elif rule == "random":
        v = random.Random(hash((i, j, seed))).randrange(m)
    else:
        v = int(rule) % m
    return pts[v], v


def decorate(box, base="square", bands=1, anchor="centre", facets=1, light=0.0, sun=60.0,
             gap=0.0, gap_colour="1b1b1f", seed=1, shear=0.0, turn=0.0):
    """Facets and bands on every tile of a base tiling (see the module docstring)."""
    t0 = tl.TILINGS[base]
    kw = {"shear": shear, "turn": turn} if t0.make.__name__ == "make" else {}
    tiles = t0.make(box, **kw).tiles
    bands = max(1, int(bands))
    out, lines = [], []
    for n, t in enumerate(tiles):
        pts = ccw(t.pts)
        m = len(pts)
        i, j, k = t.cell if t.cell and len(t.cell) == 3 else (n, 0, 0)
        a, v = _anchor(str(anchor), pts, i, j, seed)
        for e in range(m):
            p, q = pts[e], pts[(e + 1) % m]
            if v is not None and (e == v or (e + 1) % m == v):
                continue                  # the two edges at the anchor corner have no band
            normal = math.degrees(math.atan2(q[0] - p[0], -(q[1] - p[1])))     # outward
            shade = float(light) * math.cos(math.radians(normal - float(sun)))
            direction = int(round(normal / 15.0)) * 15 % 360
            for b in range(bands):
                f0, f1 = 1 - b / bands, 1 - (b + 1) / bands
                P0, Q0 = add(a, mul(sub(p, a), f0)), add(a, mul(sub(q, a), f0))
                P1, Q1 = add(a, mul(sub(p, a), f1)), add(a, mul(sub(q, a), f1))
                poly = [P0, Q0, a] if b == bands - 1 else [P0, Q0, Q1, P1]
                out.append(Tile(poly, t.kind, (i, j, k, b, direction, bands), shade=shade, stroke=False))
        if facets and int(facets):
            for p in pts:
                if p is not a:
                    lines.append(([a, p], "line:0.6", False))
        for b in range(1, bands):
            f = 1 - b / bands
            ring = [add(a, mul(sub(p, a), f)) for p in pts]
            if v is None:
                lines.append((ring, "line:0.6", True))
            else:                         # an L: from one edge next to the anchor to the other
                lines.append((ring[v + 1:] + ring[:v], "line:0.6", False))
        lines.append((pts, "line:%g:%s" % (1 + float(gap), gap_colour) if float(gap) else "line:1", True))
    return Patch(out, lines)


def _cellkey(f):
    def colour(t):
        return f(*t.cell)
    return colour


DECOR_COLOURINGS = {
    "band": _cellkey(lambda i, j, k, b, d, n: b),
    "band_checker": _cellkey(lambda i, j, k, b, d, n: b if (i + j) % 2 == 0 else n - 1 - b),
    "checker": _cellkey(lambda i, j, k, b, d, n: (i + j) % 2),
    "three": _cellkey(lambda i, j, k, b, d, n: (i - j) % 3),
    "facet": _cellkey(lambda i, j, k, b, d, n: d),
    "tile": _cellkey(lambda i, j, k, b, d, n: k),
}
DECOR_PARAMS = {"base": "square", "bands": 1, "anchor": "centre", "facets": 1, "light": .5, "sun": 60.0,
                "gap": 0.0, "gap_colour": "1b1b1f", "seed": 1, "shear": 0.0, "turn": 0.0}


# ==========================================================================
# 2. ISOMETRIC VOXELS
# ==========================================================================
EX, EY = unit(-30), unit(210)


def iso(x, y, z):
    return (x * EX[0] + y * EY[0], x * EX[1] + y * EY[1] + z)


def iso_faces(v, s=1.0):
    """The three visible faces of the cube at v (side s): +x, +y, +z."""
    x, y, z = v
    return {
        "x": [(x + s, y, z), (x + s, y + s, z), (x + s, y + s, z + s), (x + s, y, z + s)],
        "y": [(x, y + s, z), (x, y + s, z + s), (x + s, y + s, z + s), (x + s, y + s, z)],
        "z": [(x, y, z + s), (x + s, y, z + s), (x + s, y + s, z + s), (x, y + s, z + s)],
    }


FACE_INDEX = {"z": 0, "x": 1, "y": 2}
NEIGHBOUR = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}
# the voxel beyond each edge of a face, in the order of the corners of iso_faces
EDGE_NEIGHBOURS = {"x": [(0, 0, -1), (0, 1, 0), (0, 0, 1), (0, -1, 0)],
                   "y": [(-1, 0, 0), (0, 0, 1), (1, 0, 0), (0, 0, -1)],
                   "z": [(0, -1, 0), (1, 0, 0), (0, 1, 0), (-1, 0, 0)]}


def _edge_strip(p, q, w):
    d = sub(q, p)
    n = math.hypot(*d) or 1
    o = (-d[1] / n * w / 2, d[0] / n * w / 2)
    return [sub(p, o), sub(q, o), add(q, o), add(p, o)]


def voxel_patch(box, voxels, shades=(.38, 0.0, -.38), grid=1, gap=0.0, gap_colour=(.07, .09, .18), s=1.0,
                edge=.035, edge_colour=(.1, .1, .1)):
    """voxels: {(x, y, z): (group, i, j)}, (i, j) naming the object a voxel belongs to.
    Faces are drawn back to front (painter's order, by x + y + z); faces hidden by a
    neighbour are skipped. Edges are drawn only where the surface of an object folds
    or ends, as thin strips right after their face so that nearer faces cover them.
    With grid > 1 each face is cut into grid x grid stickers with gaps between them."""
    tiles = []
    for v in sorted(voxels, key=lambda v: (v[0] + v[1] + v[2], v)):
        group, i, j = voxels[v]
        for name, corners in iso_faces(v, s).items():
            dx, dy, dz = NEIGHBOUR[name]
            if (v[0] + dx * s, v[1] + dy * s, v[2] + dz * s) in voxels:
                continue
            P = [iso(*c) for c in corners]
            if not tl.meets(tl.bbox(P), box):
                continue
            f = FACE_INDEX[name]
            if grid <= 1 and not gap:
                tiles.append(Tile(P, "face%d" % f, (i, j, group, f), shade=shades[f], stroke=False))
                if edge:
                    for e, (ex, ey, ez) in enumerate(EDGE_NEIGHBOURS[name]):
                        w = (v[0] + ex * s, v[1] + ey * s, v[2] + ez * s)
                        same = w in voxels and voxels[w][1:] == (i, j)
                        covered = (w[0] + dx * s, w[1] + dy * s, w[2] + dz * s) in voxels
                        if not same or covered:
                            tiles.append(Tile(_edge_strip(P[e], P[(e + 1) % 4], edge), "edge",
                                              (i, j, group, f), colour=edge_colour, stroke=False))
                continue
            tiles.append(Tile(P, "gap", (i, j, group, f), colour=gap_colour, stroke=False))
            A, B, C, D = P
            for u in range(grid):
                for w in range(grid):
                    def at(a, b):         # bilinear point of the face, a along A->B, b along A->D
                        return add(add(A, mul(sub(B, A), a)), mul(sub(D, A), b))
                    g = gap / 2
                    q = [at((u + g) / grid, (w + g) / grid), at((u + 1 - g) / grid, (w + g) / grid),
                         at((u + 1 - g) / grid, (w + 1 - g) / grid), at((u + g) / grid, (w + 1 - g) / grid)]
                    tiles.append(Tile(q, "face%d" % f, (i, j, group, f), shade=shades[f], stroke=False))
    return Patch(tiles)


def _plane_points(box, step, margin=3):
    """Lattice points (a, b, -a-b) * step of the plane x + y + z = 0 that project into box."""
    R = max(abs(box[0]), abs(box[1]), abs(box[2]), abs(box[3])) / step + margin
    n = int(R * 1.3) + 2
    for a in range(-n, n + 1):
        for b in range(-n, n + 1):
            x, y = iso(a * step, b * step, -(a + b) * step)
            if box[0] - 3 * step < x < box[2] + 3 * step and box[1] - 3 * step < y < box[3] + 3 * step:
                yield a, b


def cubes(box, grid=1, gap=0.0, top=.38, side=-.38):
    """Stacked cubes: one cube for each point of the plane x + y + z = 0."""
    vox = {(a, b, -a - b): (0, a, b) for a, b in _plane_points(box, 1)}
    return voxel_patch(box, vox, (top, 0.0, side), int(grid), float(gap))


def rubik(box, grid=3, gap=.14, top=.3, side=-.3):
    return cubes(box, grid, gap, top, side)


def tripods(box, arm=2, top=.38, side=-.38):
    """Y tripods: the near corner of a cube frame, three bars along -x, -y and -z.
    The corners sit on the lattice (2, -1, -1), (-1, 2, -1) of the plane
    x + y + z = 0, where the tripods interlock and cover the plane (arm 1 or 2)."""
    L = int(arm)
    A, B = (2, -1, -1), (-1, 2, -1)
    vox = {}
    n = int(max(box[2] - box[0], box[3] - box[1])) + 6
    for a in range(-n, n + 1):
        for b in range(-n, n + 1):
            c = tuple(a * A[k] + b * B[k] for k in range(3))
            px, py = iso(*c)
            if not (box[0] - L - 3 < px < box[2] + L + 3 and box[1] - L - 3 < py < box[3] + L + 3):
                continue
            for t in range(L + 1):
                for d in ((-1, 0, 0), (0, -1, 0), (0, 0, -1)):
                    vox[(c[0] + d[0] * t, c[1] + d[1] * t, c[2] + d[2] * t)] = ((a - b) % 3, a, b)
    return voxel_patch(box, vox, (top, 0.0, side))


def framework(box, spacing=3, depth=2, top=.38, side=-.38):
    """Bars along x, y and z through the points where two coordinates are multiples
    of spacing, kept to a slab of the plane x + y + z = 0 (the background shows
    through the holes)."""
    k = int(spacing)
    vox = {}
    span = int(max(box[2] - box[0], box[3] - box[1])) + 4 * k
    for x in range(-span, span + 1):
        for y in range(-span, span + 1):
            for z in range(-span, span + 1):
                if not (-k * int(depth) <= x + y + z <= 0):
                    continue
                zeros = (x % k == 0) + (y % k == 0) + (z % k == 0)
                if zeros >= 2:
                    px, py = iso(x, y, z)
                    if box[0] - 2 < px < box[2] + 2 and box[1] - 2 < py < box[3] + 2:
                        vox[(x, y, z)] = (0, 0, 0)        # one object: edges only where it folds
    return voxel_patch(box, vox, (top, 0.0, side))


ISO_COLOURINGS = {
    "face": lambda t: t.cell[3],
    "group": lambda t: t.cell[2],
    "lattice3": lambda t: (t.cell[0] - t.cell[1]) % 3,
}


# ==========================================================================
# 3. QUILTS OF HALF-SQUARE TRIANGLES
# ==========================================================================
# corner holding the coloured triangle of each cell: 0 lower left, 1 lower right,
# 2 upper right, 3 upper left; rows of the table run from the top
QUILT_LAYOUTS = {
    "pinwheel": [[0, 3], [1, 2]],
    "diamonds": [[1, 0], [2, 3]],
    "chevron": [[1, 0], [1, 0]],
    "streak": [[0]],
    "broken_dishes": [[0, 1], [3, 2]],
    "zigzag": [[0, 1], [1, 0]],
    "pinwheel_big": [[0, 0, 3, 3], [0, 0, 3, 3], [1, 1, 2, 2], [1, 1, 2, 2]],
    "storm": [[1, 0, 1, 0], [2, 3, 2, 3], [0, 1, 0, 1], [3, 2, 3, 2]],
}
CORNERS = [(0, 0), (1, 0), (1, 1), (0, 1)]


def quilt(box, layout="pinwheel", groups="block", hourglass=0):
    """Half-square triangles in a grid; layout chooses the corner of the coloured
    triangle in each cell, groups how the coloured triangles share colours."""
    table = QUILT_LAYOUTS[layout]
    rows, cols = len(table), len(table[0])
    tiles = []
    x0, x1 = int(math.floor(box[0])) - 1, int(math.ceil(box[2])) + 1
    y0, y1 = int(math.floor(box[1])) - 1, int(math.ceil(box[3])) + 1
    for cx in range(x0, x1):
        for cy in range(y0, y1):
            sq = [(cx + a, cy + b) for a, b in CORNERS]
            r, c = (-cy) % rows, cx % cols
            if int(hourglass):            # quarter-square triangles: four triangles meeting at the centre
                m = (cx + .5, cy + .5)
                for e in range(4):
                    tiles.append(Tile([sq[e], sq[(e + 1) % 4], m], "q%d" % e, (cx, cy, 0, e)))
                continue
            k = table[r][c]
            corner = sq[k]
            coloured = [sq[(k - 1) % 4], corner, sq[(k + 1) % 4]]
            other = [sq[(k + 1) % 4], sq[(k + 2) % 4], sq[(k + 3) % 4]]
            g = {"block": (cx // cols + cy // rows) % 2, "rows": (cy // rows) % 3,
                 "cells": (cx + cy) % 2, "one": 0}[groups]
            tiles.append(Tile(coloured, "coloured", (cx, cy, 1, g)))
            tiles.append(Tile(other, "background", (cx, cy, 0, g)))
    return Patch(tiles)


QUILT_COLOURINGS = {               # the background sorts last, so it gets the palette's light tint
    "quilt": lambda t: 99 if t.cell[2] == 0 else 1 + t.cell[3],
    "quarters": lambda t: t.cell[3],
}


# ==========================================================================
# 4. JIGSAW, WEAVE, BEADWORK
# ==========================================================================
def _tab_profile(sign, jitter):
    """A jigsaw edge from (0, 0) to (1, 0); the tab bulges to +y if sign > 0."""
    c = .5 + jitter
    r = .12
    pts = [(0, 0), (c - .12, 0), (c - .1, .04 * sign), (c - .08, .09 * sign)]
    for k in range(17):
        a = math.radians(215 - 250 * k / 16)
        pts.append((c + r * math.cos(a), (.19 + r * math.sin(a)) * sign))
    pts += [(c + .08, .09 * sign), (c + .1, .04 * sign), (c + .12, 0), (1, 0)]
    return pts


def jigsaw(box, seed=1):
    rng = random.Random(int(seed))
    x0, x1 = int(math.floor(box[0])) - 1, int(math.ceil(box[2])) + 1
    y0, y1 = int(math.floor(box[1])) - 1, int(math.ceil(box[3])) + 1
    edge = {}

    def side(p, q):                       # shared edge p -> q, the same curve seen from both pieces
        key = (p, q) if p < q else (q, p)
        if key not in edge:
            edge[key] = _tab_profile(rng.choice((-1, 1)), rng.uniform(-.06, .06))
        prof = edge[key]
        a, b = key
        d = (b[0] - a[0], b[1] - a[1])
        pts = [(a[0] + u * d[0] - w * d[1], a[1] + u * d[1] + w * d[0]) for u, w in prof]
        return pts if (p, q) == key else pts[::-1]

    tiles = []
    for cx in range(x0, x1):
        for cy in range(y0, y1):
            sq = [(cx, cy), (cx + 1, cy), (cx + 1, cy + 1), (cx, cy + 1)]
            poly = []
            for e in range(4):
                poly += side(sq[e], sq[(e + 1) % 4])[:-1]
            tiles.append(Tile(poly, "piece", (cx, cy, 0)))
    return Patch(tiles)


def weave(box, width=.78, turn=45.0, twill=0):
    """Two families of strips going over and under each other (plain weave, or twill
    over two under two); a strip darkens where it dives under the other."""
    w = float(width)
    R = math.hypot(box[2] - box[0], box[3] - box[1]) / 2 + 2
    n = int(R) + 2
    tiles = []
    rot = lambda pts: tl.rotate(pts, float(turn))     # noqa: E731

    def rect(x0, y0, x1, y1):
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

    for i in range(-n, n):
        for j in range(-n, n):
            over_h = ((i + j) % 4 < 2) if int(twill) else (i + j) % 2 == 0   # twill steps by one each row
            hy0, hy1 = j + .5 - w / 2, j + .5 + w / 2
            vx0, vx1 = i + .5 - w / 2, i + .5 + w / 2
            hpieces = [(rect(i, hy0, vx0, hy1), .0), (rect(vx0, hy0, vx1, hy1), .15 if over_h else -.45),
                       (rect(vx1, hy0, i + 1, hy1), .0)]
            vpieces = [(rect(vx0, j, vx1, hy0), .0), (rect(vx0, hy0, vx1, hy1), .15 if not over_h else -.45),
                       (rect(vx0, hy1, vx1, j + 1), .0)]
            under, over = (vpieces, hpieces) if over_h else (hpieces, vpieces)
            for group, pieces in ((("v" if over_h else "h"), under), (("h" if over_h else "v"), over)):
                strip = i if group == "v" else j
                for pts, sh in pieces:
                    P = rot(pts)
                    if tl.meets(tl.bbox(P), box):
                        tiles.append(Tile(P, group, (strip, group, 0), shade=sh, stroke=False))
    return Patch(tiles)


WEAVE_COLOURINGS = {"strip": lambda t: t.cell[0] % 9, "direction": lambda t: t.cell[1]}


def beadwork(box, n=21, seed=3, colours_used=6):
    """Pixels in a square tile with the symmetry of the square (mirrors and quarter
    turns), the tile repeated; the colour of a pixel depends on its distance to the
    centre of the tile in a way chosen by the seed."""
    N = int(n) | 1
    rng = random.Random(int(seed))
    k1, k2, k3 = rng.randint(1, 3), rng.randint(0, 3), rng.choice((0, 1, 2))
    shift = [[rng.random() < .18 for _ in range(N)] for _ in range(N)]
    h = N // 2
    tiles = []
    x0, x1 = int(math.floor(box[0])) - 1, int(math.ceil(box[2])) + 1
    y0, y1 = int(math.floor(box[1])) - 1, int(math.ceil(box[3])) + 1
    for x in range(x0, x1):
        for y in range(y0, y1):
            u, v = abs((x % N) - h), abs((y % N) - h)
            a, b = min(u, v), max(u, v)
            val = (k1 * b + k2 * a + k3 * ((a + b) // 2) + (1 if shift[a][b] else 0)) % int(colours_used)
            tiles.append(Tile([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)], "bead", (x, y, val)))
    return Patch(tiles)


# ==========================================================================
# 5. MAZES, MEANDERS AND SPIRALS
# ==========================================================================
# A wall grid is a periodic table of cells, True for a wall, drawn flat (one square
# per cell) or in isometric view (walls of cubes standing on a floor of cubes).
# Floor cells carry a step 0 .. steps-1, their distance along the corridors from a
# source cell, so that a ramp of colours flows through the maze or the spiral.
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def _torus_maze(n, seed, loops):
    """A perfect maze of n x n rooms on a torus (depth-first, seeded), in a grid of
    2n x 2n cells: rooms at odd coordinates, walls and pillars at even ones. The grid
    repeats without seams. loops > 0 knocks down that fraction of the remaining walls."""
    rng = random.Random(int(seed))
    P = 2 * n
    wall = [[True] * P for _ in range(P)]
    seen = {(0, 0)}
    stack = [(0, 0)]
    wall[1][1] = False
    while stack:
        i, j = stack[-1]
        nxt = [(d, ((i + d[0]) % n, (j + d[1]) % n)) for d in DIRS]
        nxt = [(d, c) for d, c in nxt if c not in seen]
        if not nxt:
            stack.pop()
            continue
        d, c = rng.choice(nxt)
        wall[(2 * i + 1 + d[0]) % P][(2 * j + 1 + d[1]) % P] = False
        wall[2 * c[0] + 1][2 * c[1] + 1] = False
        seen.add(c)
        stack.append(c)
    for x in range(P):
        for y in range(P):
            if wall[x][y] and (x + y) % 2 == 1 and rng.random() < float(loops):
                wall[x][y] = False
    return wall, (1, 1)


def _square_spiral(n):
    """A square spiral of wall in an n x n block: walk from a corner, turning right
    whenever going on would touch the wall already drawn."""
    w = [[False] * n for _ in range(n)]

    def free(x, y):
        return not (0 <= x < n and 0 <= y < n) or not w[x][y]

    x, y, d = 0, n - 1, 0                 # top left corner, heading +x (rows run from the top)
    w[x][y] = True
    turns = 0
    while turns < 2:
        dx, dy = DIRS[d]
        qx, qy = x + dx, y + dy
        if 0 <= qx < n and 0 <= qy < n and not w[qx][qy] and free(qx + dx, qy + dy):
            x, y = qx, qy
            w[x][y] = True
            turns = 0
        else:
            d = (d - 1) % 4               # turn right
            turns += 1
    return w


def _spiral_grid(n, link, pinwheel):
    """Square spirals of side n in a grid of period n + 1, a floor line between them.
    link 1 joins the top walls of a row into one line (the Greek key, or meander);
    pinwheel turns the four spirals of a 2 x 2 block a quarter turn each, round
    their common corner."""
    n = max(3, int(n))
    s = _square_spiral(n)
    P = n + 1
    reps = 2 if int(pinwheel) else 1
    wall = [[False] * (P * reps) for _ in range(P * reps)]
    for bi in range(reps):
        for bj in range(reps):
            r = ((0, 1), (3, 2))[bi][bj] if int(pinwheel) else 0
            for x in range(n):
                for y in range(n):
                    u, v = x, y
                    for _ in range(r):    # quarter turns inside the block
                        u, v = n - 1 - v, u
                    wall[bi * P + u][bj * P + v] = s[x][y]
            if int(link):
                wall[bi * P + n][bj * P + n - 1] = True
    return wall, (n, n)


def _distances(wall, src, steps):
    """Steps along the corridors (breadth first, on the torus of the period) from src,
    scaled to 0 .. steps-1; unreachable floor gets the last step."""
    P, Q = len(wall), len(wall[0])
    dist = {src: 0}
    queue = [src]
    for x, y in queue:
        for dx, dy in DIRS:
            c = ((x + dx) % P, (y + dy) % Q)
            if not wall[c[0]][c[1]] and c not in dist:
                dist[c] = dist[(x, y)] + 1
                queue.append(c)
    top = max(dist.values()) + 1
    far = max(dist, key=dist.get)
    path = set()                          # the way from the farthest cell back to the source
    c = far
    while c != src:
        path.add(c)
        x, y = c
        c = min((((x + dx) % P, (y + dy) % Q) for dx, dy in DIRS),
                key=lambda e: dist.get(e, 1 << 30))
    path.add(src)
    step = {c: min(steps - 1, d * steps // top) for c, d in dist.items()}
    return step, path


def _widen(wall, src, wide):
    """Corridors (odd rows and columns) wide cells across, walls (even ones) one cell."""
    wide = max(1, int(wide))
    if wide == 1:
        return wall, src
    cols = [x for x in range(len(wall)) for _ in range(wide if x % 2 else 1)]
    rows = [y for y in range(len(wall[0])) for _ in range(wide if y % 2 else 1)]
    new = [[wall[x][y] for y in rows] for x in cols]
    return new, (cols.index(src[0]), rows.index(src[1]))


def wall_patch(box, wall, src, flat=0, height=1, steps=12, top=.38, side=-.38, wide=1):
    """Draws a periodic wall grid; cells (kind, 0, step, face): kind 0 floor, 1 wall,
    2 floor on the longest way from the source."""
    wall, src = _widen(wall, src, wide)
    P, Q = len(wall), len(wall[0])
    steps = max(1, int(steps))
    step, path = _distances(wall, src, steps)

    def info(x, y):
        c = (x % P, y % Q)
        if wall[c[0]][c[1]]:
            return 1, steps
        return (2 if c in path else 0), step.get(c, steps - 1)

    if int(flat):
        tiles = []
        for x in range(int(math.floor(box[0])) - 1, int(math.ceil(box[2])) + 1):
            for y in range(int(math.floor(box[1])) - 1, int(math.ceil(box[3])) + 1):
                kind, st = info(x, -y - 1)        # rows of the grid run downwards
                tiles.append(Tile([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)],
                                  ("floor", "wall", "path")[kind], (kind, 0, st, 0), stroke=False))
        return Patch(tiles)
    h = max(1, int(height))
    c30 = EX[0]
    vox = {}
    for x in range(-int(box[2] - box[0]) * 2 - 8, int(box[2] - box[0]) * 2 + 8):
        for y in range(-int(box[2] - box[0]) * 2 - 8, int(box[2] - box[0]) * 2 + 8):
            px, py = (x - y) * c30, -(x + y) / 2
            if not (box[0] - 5 < px < box[2] + 5 and box[1] - 5 - h < py < box[3] + 5):
                continue
            kind, st = info(x, y)
            vox[(x, y, 0)] = ((kind if kind != 1 else 0, st), 0, 0)     # one floor, one wall object
            if kind == 1:
                for z in range(1, h + 1):
                    vox[(x, y, z)] = ((1, st), 1, 0)
    patch = voxel_patch(box, vox, (float(top), 0.0, float(side)))
    for t in patch.tiles:
        (kind, st), f = t.cell[2], t.cell[3]
        t.cell = (kind, 0, st, f)
    return patch


def maze(box, n=8, seed=1, loops=0.0, flat=0, height=1, steps=12, top=.38, side=-.38, wide=2):
    wall, src = _torus_maze(max(2, int(n)), seed, loops)
    return wall_patch(box, wall, src, flat, height, steps, top, side, wide)


def spiral(box, n=7, link=0, pinwheel=0, flat=0, height=1, steps=12, top=.38, side=-.38, wide=2):
    wall, src = _spiral_grid(n, link, pinwheel)
    return wall_patch(box, wall, src, flat, height, steps, top, side, wide)


MAZE_COLOURINGS = {               # floor sorts last (99), so it gets the palette's light tint
    "walls": lambda t: 0 if t.cell[0] == 1 else 99,
    "path": lambda t: {1: 0, 2: 1}.get(t.cell[0], 99),
    "flow": lambda t: 99 if t.cell[0] == 1 else t.cell[2],
    "face": lambda t: t.cell[3] if t.cell[0] == 1 else 99,
}
MAZE_PARAMS = {"flat": 0, "wide": 2, "height": 1, "steps": 12, "top": .38, "side": -.38}


def whirl(box, base="square", steps=10, t=.18, mirror=1, shear=0.0, turn=0.0):
    """Whirling polygons: each tile of a base tiling holds a polygon whose corners
    slide a fraction t along its edges, again and again; the triangles cut off line
    up in spiral arms. mirror 1 turns neighbouring tiles the other way (checkerboard),
    so that the arms run on from tile to tile."""
    t0 = tl.TILINGS[base]
    kw = {"shear": shear, "turn": turn} if t0.make.__name__ == "make" else {}
    out = []
    for n, tile in enumerate(t0.make(box, **kw).tiles):
        pts = ccw(tile.pts)
        i, j, k = tile.cell if tile.cell and len(tile.cell) == 3 else (n, 0, 0)
        f = float(t)
        if int(mirror) and (i + j) % 2:
            f = 1 - f                         # the other hand
        m = len(pts)
        for s in range(int(steps)):
            nxt = [add(pts[e], mul(sub(pts[(e + 1) % m], pts[e]), f)) for e in range(m)]
            for e in range(m):
                out.append(Tile([nxt[e - 1], pts[e], nxt[e]], "arm", (i, j, k, s, e, m)))
            pts = nxt
        out.append(Tile(pts, "core", (i, j, k, int(steps), -1, m)))
    return Patch(out)


WHIRL_COLOURINGS = {
    "step": _cellkey(lambda i, j, k, s, e, m: s),
    "arm": _cellkey(lambda i, j, k, s, e, m: 99 if e < 0 else (e - s) % 2 if m % 2 == 0 else (e - s) % m),
    "twist": _cellkey(lambda i, j, k, s, e, m: 99 if e < 0 else (e + s) % m),
    "corner": _cellkey(lambda i, j, k, s, e, m: 99 if e < 0 else e),
}


# ==========================================================================
# 6. REGISTRY
# ==========================================================================
def _make(fn, names):
    def make(box, **p):
        return fn(box, **{k: v for k, v in p.items() if k in names})
    make.__name__ = "pattern_" + fn.__name__
    return make


def reg(key, fn, params, **kw):
    tl.register(key, _make(fn, params), params=dict(params), **kw)


reg("facets", decorate, DECOR_PARAMS, colourings=DECOR_COLOURINGS, default="checker", size=8,
    scheme="analogous", hue=5, stroke=False)
reg("bands", decorate, dict(DECOR_PARAMS, bands=6, facets=0, light=0.0), colourings=DECOR_COLOURINGS,
    default="band", size=8, scheme="sweep", hue=6, stroke=False)
reg("cubes", cubes, {"grid": 1, "gap": 0.0, "top": .38, "side": -.38}, colourings=ISO_COLOURINGS,
    default="single", size=10, scheme="mono", hue=5, stroke=False)
reg("rubik", rubik, {"grid": 3, "gap": .14, "top": .3, "side": -.3}, colourings=ISO_COLOURINGS,
    default="rings", size=12, scheme="rainbow", hue=0, stroke=False, background="12182e")
reg("tripods", tripods, {"arm": 2, "top": .38, "side": -.38}, colourings=ISO_COLOURINGS,
    default="group", size=14, scheme="triad", hue=0, stroke=True)
reg("framework", framework, {"spacing": 3, "depth": 2, "top": .38, "side": -.38}, colourings=ISO_COLOURINGS,
    default="single", size=16, scheme="mono", hue=1, stroke=False, background="0b0b0b")
reg("quilt", quilt, {"layout": "pinwheel", "groups": "block", "hourglass": 0}, colourings=QUILT_COLOURINGS,
    default="quilt", size=10, scheme="complementary", hue=8)
reg("jigsaw", jigsaw, {"seed": 1}, default="proper", size=9, scheme="square", hue=4, lw=1.4)
reg("weave", weave, {"width": .78, "turn": 45.0, "twill": 0}, colourings=WEAVE_COLOURINGS, default="strip",
    size=10, scheme="rainbow", hue=0, stroke=False, background="101010")
reg("beadwork", beadwork, {"n": 21, "seed": 3, "colours_used": 6}, default="kind", size=42,
    scheme="rainbow", hue=0, stroke=False)
tl.TILINGS["beadwork"].colourings["value"] = lambda t: t.cell[2]
tl.TILINGS["beadwork"].default = "value"
reg("maze", maze, dict({"n": 8, "seed": 1, "loops": 0.0}, **MAZE_PARAMS), colourings=MAZE_COLOURINGS,
    default="walls", size=14, scheme="mono", hue=8, stroke=False)
reg("spiral", spiral, dict({"n": 7, "link": 0, "pinwheel": 0}, **MAZE_PARAMS), colourings=MAZE_COLOURINGS,
    default="flow", size=14, scheme="rainbow", hue=0, stroke=False)
reg("whirl", whirl, {"base": "square", "steps": 10, "t": .18, "mirror": 1, "shear": 0.0, "turn": 0.0},
    colourings=WHIRL_COLOURINGS, default="arm", size=6, scheme="complementary", hue=8, lw=.5)

PATTERN_KEYS = ["facets", "bands", "cubes", "rubik", "tripods", "framework", "quilt", "jigsaw", "weave",
                "beadwork", "maze", "spiral", "whirl"]


# ==========================================================================
# 6. CATALOGUE
# ==========================================================================
V = tl.V
CATALOGUE = [
    ("facets", None, [
        V("p_studs", "facets", "checker", "analogous", 5, params={"light": .55}),
        V("p_hourglass", "facets", "facet", colours=[tl.hexc(h) for h in ("F4F1E8", "E3A72F", "2B2B2B", "8F8A84")],
          params={"light": 0.0}),
        V("p_star3d", "facets", "tile", "complementary", 8, params={"base": "triangular", "light": .5}, size=9),
        V("p_hexpyramids", "facets", "three", "triad", 0, params={"base": "hexagonal", "light": .5}, size=10),
        V("p_octpyramids", "facets", "tile", "split", 9, params={"base": "truncated_square", "light": .5}),
        V("p_cairo_facets", "facets", "gradient", "sweep", 8, params={"base": "cairo", "light": .45}),
    ]),
    ("bands", None, [
        V("p_courthouse", "bands", "band_checker", "sweep", 6, params={"bands": 7, "facets": 1}),
        V("p_logcabin", "bands", "band", "rainbow", 0,
          params={"bands": 7, "anchor": "alternate", "gap": 2.5, "gap_colour": "2ED3C6"}),
        V("p_cabin_diamonds", "bands", "band", "ramp", 5,
          params={"bands": 6, "anchor": 0, "turn": 45.0, "gap": 3.0, "gap_colour": "111111"}),
        V("p_pinwheel_cabin", "bands", "band", "sweep", 2, params={"bands": 6, "anchor": "pinwheel"}),
        V("p_hexrings", "bands", "band", "ramp", 8, params={"base": "hexagonal", "bands": 5}, size=10),
        V("p_trirings", "bands", "band_checker", "sweep", 10, params={"base": "triangular", "bands": 4,
                                                                       "facets": 1}),
    ]),
    ("iso_cubes", None, [
        V("p_cubes", "cubes", "single", "mono", 5),
        V("p_cubes_faces", "cubes", "face", "triad", 4, params={"top": 0.0, "side": 0.0}),
        V("p_cubes_gradient", "cubes", "gradient", "rainbow", 0),
        V("p_rubik", "rubik", "rings", "rainbow", 0, size=7),
        V("p_rubik_lattice", "rubik", "lattice3", "complementary", 2, size=7),
    ]),
    ("iso_bars", None, [
        V("p_tripods", "tripods", "group", "triad", 0),
        V("p_tripods_warm", "tripods", "group", "sweep", 3, params={"arm": 1}, size=10),
        V("p_tripods_gold", "tripods", "single", "mono", 1),
        V("p_tripods_gradient", "tripods", "gradient", "rainbow", 0),
        V("p_framework", "framework", "single", "mono", 1),
        V("p_framework2", "framework", "single", "mono", 8, params={"spacing": 4, "depth": 1}, size=20),
    ]),
    ("quilts", None, [
        V("p_q_pinwheel", "quilt", "quilt", "complementary", 8, params={"layout": "pinwheel"}),
        V("p_q_diamonds", "quilt", "quilt", "split", 4, params={"layout": "diamonds"}),
        V("p_q_chevron", "quilt", "quilt", "analogous", 10, params={"layout": "chevron", "groups": "rows"}),
        V("p_q_storm", "quilt", "quilt", "triad", 7, params={"layout": "storm"}, size=12),
        V("p_q_big", "quilt", "quilt", "tetrad", 2, params={"layout": "pinwheel_big"}, size=12),
        V("p_q_hourglass", "quilt", "quarters", "square", 1, params={"hourglass": 1}),
    ]),
    ("jigsaw", None, [
        V("p_jigsaw", "jigsaw", "proper", "square", 4),
        V("p_jigsaw_gradient", "jigsaw", "gradient", "rainbow", 0, params={"seed": 4}),
    ]),
    ("weave", None, [
        V("p_weave", "weave", "strip", "rainbow", 0),
        V("p_weave_two", "weave", "direction", "complementary", 8, params={"turn": 0.0}),
        V("p_twill", "weave", "direction", "split", 3, params={"twill": 1, "turn": 0.0}),
    ]),
    ("beadwork", None, [
        V("p_beads1", "beadwork", "value", "rainbow", 0),
        V("p_beads2", "beadwork", "value", "sweep", 3, params={"seed": 7, "n": 25}),
        V("p_beads3", "beadwork", "value", "triad", 8, params={"seed": 11, "colours_used": 5}),
        V("p_beads4", "beadwork", "value", "zellij", params={"seed": 5, "n": 17}),
    ]),
    ("mazes", None, [
        V("p_maze", "maze", "walls", "mono", 8),
        V("p_maze_path", "maze", "path", "complementary", 2),
        V("p_maze_flow", "maze", "flow", "rainbow", 0, params={"seed": 3}),
        V("p_maze_tall", "maze", "face", "triad", 0, params={"height": 2, "wide": 3}, size=20),
        V("p_maze_flat", "maze", "path", "complementary", 8, params={"flat": 1, "wide": 1}, size=22),
        V("p_maze_loops", "maze", "flow", "sweep", 6, params={"flat": 1, "wide": 1, "loops": .15, "n": 12},
          size=26),
    ]),
    ("meanders", None, [
        V("p_spiral", "spiral", "walls", "mono", 1, params={"link": 1}, size=16),
        V("p_spiral_flow", "spiral", "flow", "rainbow", 0, size=16),
        V("p_spiral_pinwheel", "spiral", "walls", "mono", 4, params={"pinwheel": 1}, size=22),
        V("p_greek_key", "spiral", "walls", "mono", 8, params={"link": 1, "flat": 1, "wide": 1}, size=20),
        V("p_spiral_flat", "spiral", "flow", "rainbow", 0, params={"pinwheel": 1, "flat": 1, "wide": 1}, size=20),
        V("p_spiral_small", "spiral", "path", "split", 9, params={"n": 9}, size=22),
    ]),
    ("whirls", None, [
        V("p_whirl", "whirl", "arm", "complementary", 8),
        V("p_whirl_ramp", "whirl", "step", "ramp", 5, params={"steps": 14, "t": .12}),
        V("p_whirl_hex", "whirl", "twist", "rainbow", 0, params={"base": "hexagonal", "mirror": 0}, size=7),
        V("p_whirl_tri", "whirl", "step", "sweep", 2, params={"base": "triangular", "steps": 8}, size=5),
        V("p_whirl_cairo", "whirl", "arm", "analogous", 3, params={"base": "cairo"}, size=8),
        V("p_whirl_corner", "whirl", "corner", "tetrad", 1, params={"mirror": 0, "steps": 12}),
    ]),
]


# ==========================================================================
# 7. TEXT (en, pt, es); merged into the table of tilings.py
# ==========================================================================
STRINGS = {
    # ------------------------------------------------------------------ EN
    "en": {
        "title": "DECORATED MOSAICS",
        "subtitle": "Facets, bands, isometric 3D, quilts, jigsaws, weaves, beadwork, mazes and spirals",
        "intro": "In these mosaics the basic shape is more than a polygon. Each tile of a tiling can be cut "
                 "into facets lit from one side, so that it stands out like a pyramid, or into concentric "
                 "bands that shrink towards its centre or one of its corners. Seen in isometric view, "
                 "cubes and bars turn the plane into stacks, tripods and frameworks, with three shades "
                 "for the three directions of their faces. Quilts, jigsaw puzzles, woven strips and "
                 "beadwork, mazes, meanders and whirling spirals complete the set. Colours come from the RYB colour schemes; the ramp and the "
                 "sweep give the smooth steps that bands and gradients need.",
        "f_facets": "Facets and pyramids",
        "f_facets_d": "Every tile is cut into triangles from its centre; each triangle is lit according to "
                      "the direction it faces, so squares become studs, triangles three-dimensional stars "
                      "and hexagons hexagonal pyramids. Without light the same cut makes the hourglass "
                      "blocks of quilts. Works on any tiling (-p base=...).",
        "f_bands": "Concentric bands",
        "f_bands_d": "Each tile is filled with bands that shrink towards its centre (courthouse steps) or "
                     "towards one of its corners (log cabin). Coloured in order with a ramp or a sweep of "
                     "hues, the bands give depth; a wide gap of another colour frames the blocks.",
        "f_iso_cubes": "Isometric cubes",
        "f_iso_cubes_d": "Cubes seen along their diagonal: three faces, one light, one mid, one dark. Stacked "
                         "on a plane they make the tumbling blocks pattern; cut into stickers they become "
                         "Rubik's cubes, here with a rainbow that spreads from the centre.",
        "f_iso_bars": "Tripods and frameworks",
        "f_iso_bars_d": "Bars of cubes drawn in isometric view. Three bars meeting at a corner make a "
                        "Y-shaped tripod, and tripods on the right lattice interlock and cover the plane. "
                        "Bars along the three axes make a framework with the background showing through.",
        "f_quilts": "Quilts",
        "f_quilts_d": "Squares cut along a diagonal into two triangles (half-square triangles), turned "
                      "according to a small table: pinwheels, diamonds, chevrons, storms. Cut along both "
                      "diagonals they make the four-triangle hourglass blocks.",
        "f_jigsaw": "Jigsaw puzzle",
        "f_jigsaw_d": "Square pieces whose edges carry a tab or a hole, chosen at random for every edge and "
                      "shared by the two pieces, so that they fit. Colours so that neighbours differ, or a "
                      "gradient.",
        "f_weave": "Weaves",
        "f_weave_d": "Two families of strips going over and under each other: a plain weave alternates at "
                     "every crossing, a twill every two, stepping by one each row. A strip darkens where it "
                     "dives under the other.",
        "f_beadwork": "Beadwork",
        "f_beadwork_d": "Pixel patterns with the symmetry of the square: a tile of beads whose colour "
                        "depends on the distance to its centre in a way chosen by a seed (-p seed=...), "
                        "repeated over the plane as in bead and cross-stitch embroidery.",
        "p_studs": "Pyramid studs on a square grid",
        "p_hourglass": "Hourglass blocks: the same cut without light",
        "p_star3d": "Three-dimensional stars from triangles",
        "p_hexpyramids": "Hexagonal pyramids in three colours",
        "p_octpyramids": "Facets on the 4.8.8 tiling",
        "p_cairo_facets": "Facets on the Cairo tiling, with a gradient",
        "p_courthouse": "Courthouse steps: rings cut by the diagonals",
        "p_logcabin": "Log cabin: bands from a corner, framed",
        "p_cabin_diamonds": "Log cabin diamonds, ramp of one hue",
        "p_pinwheel_cabin": "Bands round four different corners",
        "p_hexrings": "Rings in hexagons",
        "p_trirings": "Striped triangles, alternating",
        "p_cubes": "Tumbling blocks: one hue in three values",
        "p_cubes_faces": "One colour for each direction of face",
        "p_cubes_gradient": "Cubes in a rainbow gradient",
        "p_rubik": "Rubik's cubes, rainbow from the centre",
        "p_rubik_lattice": "Rubik's cubes in two colours and a tint",
        "p_tripods": "Interlocking Y tripods",
        "p_tripods_warm": "Short tripods in a sweep of warm hues",
        "p_tripods_gold": "Golden tripods",
        "p_tripods_gradient": "Tripods in a rainbow gradient",
        "p_framework": "Framework of bars",
        "p_framework2": "A thinner framework",
        "p_q_pinwheel": "Pinwheels",
        "p_q_diamonds": "Diamonds",
        "p_q_chevron": "Chevrons",
        "p_q_storm": "Storm at sea",
        "p_q_big": "Big pinwheels",
        "p_q_hourglass": "Hourglass: four triangles per square",
        "p_jigsaw": "Jigsaw, neighbours differ",
        "p_jigsaw_gradient": "Jigsaw in a gradient",
        "p_weave": "Plain weave turned 45°, rainbow strips",
        "p_weave_two": "Plain weave in two colours",
        "p_twill": "Twill",
        "p_beads1": "Beadwork, seed 3",
        "p_beads2": "Beadwork, seed 7",
        "p_beads3": "Beadwork, seed 11",
        "p_beads4": "Beadwork in zellij colours",
        "c_band": "by band", "c_band_checker": "by band, alternating", "c_facet": "by facet direction",
        "c_tile": "by tile", "c_three": "three colours", "c_face": "by face", "c_group": "by object",
        "c_lattice3": "three colours", "c_quilt": "coloured triangles", "c_quarters": "by quarter",
        "c_strip": "by strip", "c_direction": "by direction", "c_value": "by distance to the centre",
        "f_mazes": "Mazes",
        "f_mazes_d": "Perfect mazes (exactly one way between any two points) dug at random from a seed "
                     "(-p seed=...) on a torus, so that the maze repeats without seams. Drawn as walls of "
                     "cubes in isometric view or flat from above; the floor can follow a ramp of colours "
                     "along the corridors, or show the longest way through the maze.",
        "f_meanders": "Square spirals and meanders",
        "f_meanders_d": "Square spirals of wall, each turn one corridor further in. Joined along the top they "
                        "make the Greek key (meander); turned a quarter turn each round a corner they make "
                        "pinwheels of four spirals. The colours can flow along the corridor into each spiral.",
        "f_whirls": "Whirling polygons",
        "f_whirls_d": "In every tile a polygon whose corners slide a little along its edges, again and "
                      "again: the cut-off triangles line up in spiral arms. Neighbouring tiles turn the other "
                      "way, so that the arms run on from tile to tile. Works on any tiling (-p base=...).",
        "p_maze": "Isometric maze",
        "p_maze_path": "The longest way through the maze",
        "p_maze_flow": "Colours flowing along the corridors",
        "p_maze_tall": "Tall walls, wide corridors",
        "p_maze_flat": "Maze from above, longest way",
        "p_maze_loops": "Maze with loops, in a sweep of hues",
        "p_spiral": "Isometric meander",
        "p_spiral_flow": "Square spirals, rainbow corridors",
        "p_spiral_pinwheel": "Pinwheels of four spirals",
        "p_greek_key": "Greek key",
        "p_spiral_flat": "Spiral pinwheels from above",
        "p_spiral_small": "Larger spirals, the longest way",
        "p_whirl": "Whirling squares",
        "p_whirl_ramp": "Whirling squares in a ramp",
        "p_whirl_hex": "Whirling hexagons",
        "p_whirl_tri": "Whirling triangles",
        "p_whirl_cairo": "Whirls on the Cairo tiling",
        "p_whirl_corner": "One colour per corner, all turning the same way",
        "c_walls": "walls and floor", "c_path": "longest way", "c_flow": "along the corridors",
        "c_step": "by step", "c_arm": "spiral arms", "c_twist": "spiral arms, other hand",
        "c_corner": "by corner",
    },
    # ------------------------------------------------------------------ PT
    "pt": {
        "title": "MOSAICOS DECORADOS",
        "subtitle": "Facetas, faixas, 3D isométrico, patchwork, puzzles, tecelagens, missangas, labirintos e espirais",
        "intro": "Nestes mosaicos a forma de base é mais do que um polígono. Cada peça de uma pavimentação "
                 "pode ser cortada em facetas iluminadas de um lado, para sobressair como uma pirâmide, ou "
                 "em faixas concêntricas que encolhem para o centro ou para um dos cantos. Em vista "
                 "isométrica, cubos e barras transformam o plano em pilhas, tripés e estruturas, com três "
                 "tons para as três direções das faces. Patchwork, puzzles, tiras entrelaçadas e "
                 "missangas, labirintos, meandros e espirais em remoinho completam o conjunto. As cores vêm dos esquemas RYB; o degradê e a passagem "
                 "de matizes dão os passos suaves de que as faixas e os gradientes precisam.",
        "f_facets": "Facetas e pirâmides",
        "f_facets_d": "Cada peça é cortada em triângulos a partir do centro; cada triângulo recebe luz "
                      "conforme a direção para onde está virado, e assim os quadrados ficam pirâmides, os "
                      "triângulos estrelas em relevo e os hexágonos pirâmides hexagonais. Sem luz, o mesmo "
                      "corte dá os blocos em ampulheta do patchwork. Serve para qualquer pavimentação "
                      "(-p base=...).",
        "f_bands": "Faixas concêntricas",
        "f_bands_d": "Cada peça enche-se de faixas que encolhem para o centro (degraus do tribunal) ou para "
                     "um dos cantos (cabana de troncos). Coloridas por ordem com um degradê ou uma passagem "
                     "de matizes, as faixas dão profundidade; uma junta larga de outra cor emoldura os blocos.",
        "f_iso_cubes": "Cubos isométricos",
        "f_iso_cubes_d": "Cubos vistos ao longo da diagonal: três faces, uma clara, uma média e uma escura. "
                         "Empilhados num plano dão o padrão dos blocos em cascata; cortados em quadradinhos "
                         "tornam-se cubos de Rubik, aqui com um arco-íris que se espalha do centro.",
        "f_iso_bars": "Tripés e estruturas",
        "f_iso_bars_d": "Barras de cubos em vista isométrica. Três barras que se juntam num canto formam um "
                        "tripé em Y, e os tripés na rede certa encaixam uns nos outros e cobrem o plano. "
                        "Barras segundo os três eixos formam uma estrutura com o fundo à vista.",
        "f_quilts": "Patchwork",
        "f_quilts_d": "Quadrados cortados por uma diagonal em dois triângulos (triângulos de meio quadrado), "
                      "rodados segundo uma pequena tabela: cataventos, losangos, chevrons, tempestades. "
                      "Cortados pelas duas diagonais dão os blocos em ampulheta de quatro triângulos.",
        "f_jigsaw": "Puzzle",
        "f_jigsaw_d": "Peças quadradas com um encaixe ou um buraco em cada aresta, escolhido ao acaso e "
                      "partilhado pelas duas peças, para que encaixem. Cores com vizinhas diferentes, ou um "
                      "degradê.",
        "f_weave": "Tecelagens",
        "f_weave_d": "Duas famílias de tiras que passam por cima e por baixo umas das outras: o tafetá "
                     "alterna em cada cruzamento, a sarja de dois em dois, avançando um em cada fila. A tira "
                     "escurece onde mergulha por baixo da outra.",
        "f_beadwork": "Missangas",
        "f_beadwork_d": "Padrões de píxeis com a simetria do quadrado: um quadro de missangas cuja cor "
                        "depende da distância ao centro de uma maneira escolhida por uma semente "
                        "(-p seed=...), repetido no plano como nos bordados de missangas e de ponto cruz.",
        "p_studs": "Pirâmides numa grelha quadrada",
        "p_hourglass": "Blocos em ampulheta: o mesmo corte sem luz",
        "p_star3d": "Estrelas em relevo a partir de triângulos",
        "p_hexpyramids": "Pirâmides hexagonais em três cores",
        "p_octpyramids": "Facetas na pavimentação 4.8.8",
        "p_cairo_facets": "Facetas na pavimentação do Cairo, em degradê",
        "p_courthouse": "Degraus do tribunal: anéis cortados pelas diagonais",
        "p_logcabin": "Cabana de troncos: faixas a partir de um canto, emolduradas",
        "p_cabin_diamonds": "Losangos em cabana de troncos, degradê de um matiz",
        "p_pinwheel_cabin": "Faixas à volta de quatro cantos diferentes",
        "p_hexrings": "Anéis em hexágonos",
        "p_trirings": "Triângulos às riscas, alternados",
        "p_cubes": "Blocos em cascata: um matiz em três valores",
        "p_cubes_faces": "Uma cor para cada direção de face",
        "p_cubes_gradient": "Cubos num degradê arco-íris",
        "p_rubik": "Cubos de Rubik, arco-íris a partir do centro",
        "p_rubik_lattice": "Cubos de Rubik em duas cores e uma tinta",
        "p_tripods": "Tripés em Y encaixados",
        "p_tripods_warm": "Tripés curtos numa passagem de matizes quentes",
        "p_tripods_gold": "Tripés dourados",
        "p_tripods_gradient": "Tripés num degradê arco-íris",
        "p_framework": "Estrutura de barras",
        "p_framework2": "Uma estrutura mais fina",
        "p_q_pinwheel": "Cataventos",
        "p_q_diamonds": "Losangos",
        "p_q_chevron": "Chevrons",
        "p_q_storm": "Tempestade no mar",
        "p_q_big": "Cataventos grandes",
        "p_q_hourglass": "Ampulheta: quatro triângulos por quadrado",
        "p_jigsaw": "Puzzle, vizinhas diferentes",
        "p_jigsaw_gradient": "Puzzle em degradê",
        "p_weave": "Tafetá rodado 45°, tiras arco-íris",
        "p_weave_two": "Tafetá em duas cores",
        "p_twill": "Sarja",
        "p_beads1": "Missangas, semente 3",
        "p_beads2": "Missangas, semente 7",
        "p_beads3": "Missangas, semente 11",
        "p_beads4": "Missangas nas cores do zellij",
        "c_band": "por faixa", "c_band_checker": "por faixa, alternada", "c_facet": "pela direção da faceta",
        "c_tile": "por peça", "c_three": "três cores", "c_face": "por face", "c_group": "por objeto",
        "c_lattice3": "três cores", "c_quilt": "triângulos coloridos", "c_quarters": "por quarto",
        "c_strip": "por tira", "c_direction": "pela direção", "c_value": "pela distância ao centro",
        "f_mazes": "Labirintos",
        "f_mazes_d": "Labirintos perfeitos (exatamente um caminho entre quaisquer dois pontos), escavados ao "
                     "acaso a partir de uma semente (-p seed=...) num toro, para que o labirinto se repita "
                     "sem costuras. Desenhados com paredes de cubos em vista isométrica ou planos, vistos de "
                     "cima; o chão pode seguir um degradê de cores ao longo dos corredores, ou mostrar o "
                     "caminho mais longo do labirinto.",
        "f_meanders": "Espirais quadradas e meandros",
        "f_meanders_d": "Espirais quadradas de parede, cada volta um corredor mais para dentro. Ligadas por "
                        "cima dão a grega (meandro); rodadas um quarto de volta cada à volta de um canto dão "
                        "cataventos de quatro espirais. As cores podem correr pelo corredor até ao centro de "
                        "cada espiral.",
        "f_whirls": "Polígonos em remoinho",
        "f_whirls_d": "Em cada peça, um polígono cujos cantos deslizam um pouco ao longo das arestas, uma e "
                      "outra vez: os triângulos cortados alinham-se em braços de espiral. As peças vizinhas "
                      "rodam ao contrário, para que os braços continuem de peça para peça. Serve para "
                      "qualquer pavimentação (-p base=...).",
        "p_maze": "Labirinto isométrico",
        "p_maze_path": "O caminho mais longo do labirinto",
        "p_maze_flow": "Cores a correr pelos corredores",
        "p_maze_tall": "Paredes altas, corredores largos",
        "p_maze_flat": "Labirinto visto de cima, caminho mais longo",
        "p_maze_loops": "Labirinto com voltas, numa passagem de matizes",
        "p_spiral": "Meandro isométrico",
        "p_spiral_flow": "Espirais quadradas, corredores arco-íris",
        "p_spiral_pinwheel": "Cataventos de quatro espirais",
        "p_greek_key": "Grega",
        "p_spiral_flat": "Cataventos de espirais vistos de cima",
        "p_spiral_small": "Espirais maiores, o caminho mais longo",
        "p_whirl": "Quadrados em remoinho",
        "p_whirl_ramp": "Quadrados em remoinho, em degradê",
        "p_whirl_hex": "Hexágonos em remoinho",
        "p_whirl_tri": "Triângulos em remoinho",
        "p_whirl_cairo": "Remoinhos na pavimentação do Cairo",
        "p_whirl_corner": "Uma cor por canto, todos a rodar para o mesmo lado",
        "c_walls": "paredes e chão", "c_path": "caminho mais longo", "c_flow": "ao longo dos corredores",
        "c_step": "por passo", "c_arm": "braços da espiral", "c_twist": "braços da espiral, ao contrário",
        "c_corner": "por canto",
    },
    # ------------------------------------------------------------------ ES
    "es": {
        "title": "MOSAICOS DECORADOS",
        "subtitle": "Facetas, franjas, 3D isométrico, patchwork, puzles, tejidos, abalorios, laberintos y espirales",
        "intro": "En estos mosaicos la forma base es más que un polígono. Cada pieza de un teselado puede "
                 "cortarse en facetas iluminadas desde un lado, para que resalte como una pirámide, o en "
                 "franjas concéntricas que se encogen hacia el centro o hacia una de sus esquinas. En vista "
                 "isométrica, cubos y barras convierten el plano en pilas, trípodes y estructuras, con tres "
                 "tonos para las tres direcciones de las caras. Patchwork, puzles, tiras entrelazadas y "
                 "abalorios, laberintos, meandros y espirales en remolino completan el conjunto. Los colores vienen de los esquemas RYB; el degradado y "
                 "el recorrido de matices dan los pasos suaves que necesitan las franjas y los gradientes.",
        "f_facets": "Facetas y pirámides",
        "f_facets_d": "Cada pieza se corta en triángulos desde su centro; cada triángulo recibe luz según la "
                      "dirección hacia la que mira, y así los cuadrados se vuelven pirámides, los triángulos "
                      "estrellas en relieve y los hexágonos pirámides hexagonales. Sin luz, el mismo corte da "
                      "los bloques en reloj de arena del patchwork. Sirve para cualquier teselado "
                      "(-p base=...).",
        "f_bands": "Franjas concéntricas",
        "f_bands_d": "Cada pieza se llena de franjas que se encogen hacia el centro (escalones del juzgado) o "
                     "hacia una de sus esquinas (cabaña de troncos). Coloreadas en orden con un degradado o "
                     "un recorrido de matices, las franjas dan profundidad; una junta ancha de otro color "
                     "enmarca los bloques.",
        "f_iso_cubes": "Cubos isométricos",
        "f_iso_cubes_d": "Cubos vistos a lo largo de su diagonal: tres caras, una clara, una media y una "
                         "oscura. Apilados en un plano dan el patrón de bloques en cascada; cortados en "
                         "cuadraditos se vuelven cubos de Rubik, aquí con un arcoíris que se extiende desde "
                         "el centro.",
        "f_iso_bars": "Trípodes y estructuras",
        "f_iso_bars_d": "Barras de cubos en vista isométrica. Tres barras que se unen en una esquina forman "
                        "un trípode en Y, y los trípodes en la red adecuada encajan entre sí y cubren el "
                        "plano. Barras según los tres ejes forman una estructura con el fondo a la vista.",
        "f_quilts": "Patchwork",
        "f_quilts_d": "Cuadrados cortados por una diagonal en dos triángulos (triángulos de medio cuadrado), "
                      "girados según una pequeña tabla: molinillos, rombos, chevrones, tormentas. Cortados "
                      "por las dos diagonales dan los bloques en reloj de arena de cuatro triángulos.",
        "f_jigsaw": "Puzle",
        "f_jigsaw_d": "Piezas cuadradas con una lengüeta o un hueco en cada arista, elegido al azar y "
                      "compartido por las dos piezas, para que encajen. Colores con vecinas distintas, o un "
                      "degradado.",
        "f_weave": "Tejidos",
        "f_weave_d": "Dos familias de tiras que pasan por encima y por debajo unas de otras: el tafetán "
                     "alterna en cada cruce, la sarga de dos en dos, avanzando una en cada fila. La tira se "
                     "oscurece donde se hunde bajo la otra.",
        "f_beadwork": "Abalorios",
        "f_beadwork_d": "Patrones de píxeles con la simetría del cuadrado: un cuadro de cuentas cuyo color "
                        "depende de la distancia a su centro de un modo elegido por una semilla "
                        "(-p seed=...), repetido en el plano como en los bordados de abalorios y punto de cruz.",
        "p_studs": "Pirámides en una cuadrícula",
        "p_hourglass": "Bloques en reloj de arena: el mismo corte sin luz",
        "p_star3d": "Estrellas en relieve a partir de triángulos",
        "p_hexpyramids": "Pirámides hexagonales en tres colores",
        "p_octpyramids": "Facetas en el teselado 4.8.8",
        "p_cairo_facets": "Facetas en el teselado de El Cairo, en degradado",
        "p_courthouse": "Escalones del juzgado: anillos cortados por las diagonales",
        "p_logcabin": "Cabaña de troncos: franjas desde una esquina, enmarcadas",
        "p_cabin_diamonds": "Rombos en cabaña de troncos, degradado de un matiz",
        "p_pinwheel_cabin": "Franjas alrededor de cuatro esquinas distintas",
        "p_hexrings": "Anillos en hexágonos",
        "p_trirings": "Triángulos a rayas, alternados",
        "p_cubes": "Bloques en cascada: un matiz en tres valores",
        "p_cubes_faces": "Un color para cada dirección de cara",
        "p_cubes_gradient": "Cubos en un degradado arcoíris",
        "p_rubik": "Cubos de Rubik, arcoíris desde el centro",
        "p_rubik_lattice": "Cubos de Rubik en dos colores y un tinte",
        "p_tripods": "Trípodes en Y encajados",
        "p_tripods_warm": "Trípodes cortos en un recorrido de matices cálidos",
        "p_tripods_gold": "Trípodes dorados",
        "p_tripods_gradient": "Trípodes en un degradado arcoíris",
        "p_framework": "Estructura de barras",
        "p_framework2": "Una estructura más fina",
        "p_q_pinwheel": "Molinillos",
        "p_q_diamonds": "Rombos",
        "p_q_chevron": "Chevrones",
        "p_q_storm": "Tormenta en el mar",
        "p_q_big": "Molinillos grandes",
        "p_q_hourglass": "Reloj de arena: cuatro triángulos por cuadrado",
        "p_jigsaw": "Puzle, vecinas distintas",
        "p_jigsaw_gradient": "Puzle en degradado",
        "p_weave": "Tafetán girado 45°, tiras arcoíris",
        "p_weave_two": "Tafetán en dos colores",
        "p_twill": "Sarga",
        "p_beads1": "Abalorios, semilla 3",
        "p_beads2": "Abalorios, semilla 7",
        "p_beads3": "Abalorios, semilla 11",
        "p_beads4": "Abalorios en colores del zellige",
        "c_band": "por franja", "c_band_checker": "por franja, alterna", "c_facet": "por dirección de faceta",
        "c_tile": "por pieza", "c_three": "tres colores", "c_face": "por cara", "c_group": "por objeto",
        "c_lattice3": "tres colores", "c_quilt": "triángulos coloreados", "c_quarters": "por cuarto",
        "c_strip": "por tira", "c_direction": "por dirección", "c_value": "por distancia al centro",
        "f_mazes": "Laberintos",
        "f_mazes_d": "Laberintos perfectos (exactamente un camino entre dos puntos cualesquiera), excavados "
                     "al azar a partir de una semilla (-p seed=...) en un toro, para que el laberinto se "
                     "repita sin costuras. Dibujados con paredes de cubos en vista isométrica o planos, "
                     "vistos desde arriba; el suelo puede seguir un degradado de colores a lo largo de los "
                     "pasillos, o mostrar el camino más largo del laberinto.",
        "f_meanders": "Espirales cuadradas y meandros",
        "f_meanders_d": "Espirales cuadradas de pared, cada vuelta un pasillo más adentro. Unidas por arriba "
                        "dan la greca (meandro); giradas un cuarto de vuelta cada una alrededor de una "
                        "esquina dan molinillos de cuatro espirales. Los colores pueden correr por el "
                        "pasillo hasta el centro de cada espiral.",
        "f_whirls": "Polígonos en remolino",
        "f_whirls_d": "En cada pieza, un polígono cuyas esquinas se deslizan un poco a lo largo de sus "
                      "aristas, una y otra vez: los triángulos recortados se alinean en brazos de espiral. "
                      "Las piezas vecinas giran al revés, para que los brazos sigan de pieza en pieza. Sirve "
                      "para cualquier teselado (-p base=...).",
        "p_maze": "Laberinto isométrico",
        "p_maze_path": "El camino más largo del laberinto",
        "p_maze_flow": "Colores que corren por los pasillos",
        "p_maze_tall": "Paredes altas, pasillos anchos",
        "p_maze_flat": "Laberinto visto desde arriba, camino más largo",
        "p_maze_loops": "Laberinto con vueltas, en un recorrido de matices",
        "p_spiral": "Meandro isométrico",
        "p_spiral_flow": "Espirales cuadradas, pasillos arcoíris",
        "p_spiral_pinwheel": "Molinillos de cuatro espirales",
        "p_greek_key": "Greca",
        "p_spiral_flat": "Molinillos de espirales vistos desde arriba",
        "p_spiral_small": "Espirales mayores, el camino más largo",
        "p_whirl": "Cuadrados en remolino",
        "p_whirl_ramp": "Cuadrados en remolino, en degradado",
        "p_whirl_hex": "Hexágonos en remolino",
        "p_whirl_tri": "Triángulos en remolino",
        "p_whirl_cairo": "Remolinos en el teselado de El Cairo",
        "p_whirl_corner": "Un color por esquina, todos girando hacia el mismo lado",
        "c_walls": "paredes y suelo", "c_path": "camino más largo", "c_flow": "a lo largo de los pasillos",
        "c_step": "por paso", "c_arm": "brazos de la espiral", "c_twist": "brazos de la espiral, al revés",
        "c_corner": "por esquina",
    },
}


def main():
    for lang, table in STRINGS.items():
        tl.STRINGS[lang].update(table)
    tl.PROGRAM.update(catalogue=CATALOGUE, keys=PATTERN_KEYS, out="patterns", start="tripods")
    tl.main()
    if "--list" in sys.argv:
        print("quilt layouts:", ", ".join(QUILT_LAYOUTS))
        print("bases for facets / bands (base=...):", ", ".join(k for k in tl.TILINGS if k not in PATTERN_KEYS))
        print("anchors for bands: centre, alternate, pinwheel, random, or a corner number")


if __name__ == "__main__":
    main()
