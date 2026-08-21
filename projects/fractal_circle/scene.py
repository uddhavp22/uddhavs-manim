"""A circle tiled by a grid of rectangles (clipped to the circle at the
boundary, so edge cells are partial while interior cells are full), where a
small formation of squares is built once inside one full cell and then
replicated identically into every other full cell.

Render:
    ./render.sh projects/fractal_circle/scene.py FractalCircle -ql   # draft
    ./render.sh projects/fractal_circle/scene.py FractalCircle       # 1080p60
"""

from manim import *
from manim.mobject.geometry.boolean_ops import Intersection
import numpy as np

BG_COLOR = "#0C0E12"          # must match manim.cfg background_color
CIRCLE_COLOR = "#E8E8E8"
FULL_COLOR = "#3E7CB1"
PARTIAL_COLOR = "#2C5170"
PATTERN_COLOR = "#F2A65A"
PATTERN_ACCENT = "#E85D75"

R = 3.0   # circle radius
S = 1.0   # grid cell size


def cell_classification(x0, y0, s, radius):
    """Return 'out', 'full', or 'partial' for the cell with lower-left
    corner (x0, y0) and side s, against a circle of the given radius
    centred at the origin."""
    cx = np.clip(0.0, x0, x0 + s)
    cy = np.clip(0.0, y0, y0 + s)
    min_dist = np.hypot(cx, cy)
    if min_dist > radius:
        return "out"
    corners = [(x0, y0), (x0 + s, y0), (x0, y0 + s), (x0 + s, y0 + s)]
    max_dist = max(np.hypot(cxc, cyc) for cxc, cyc in corners)
    return "full" if max_dist <= radius else "partial"


def make_formation(center, s):
    """The small formation replicated into every full cell: four corner
    squares in a pinwheel arrangement plus a rotated diamond at the centre.
    Sampled once here; every cell gets an identical copy of this layout."""
    off = 0.26 * s
    sq_side = 0.30 * s
    pieces = VGroup()
    for dx, dy in [(off, off), (-off, off), (-off, -off), (off, -off)]:
        sq = Square(
            side_length=sq_side,
            fill_color=PATTERN_COLOR,
            fill_opacity=0.9,
            stroke_color=BG_COLOR,
            stroke_width=1.5,
        )
        sq.move_to(center + np.array([dx, dy, 0]))
        pieces.add(sq)
    diamond = Square(
        side_length=sq_side * 0.85,
        fill_color=PATTERN_ACCENT,
        fill_opacity=0.95,
        stroke_color=BG_COLOR,
        stroke_width=1.5,
    )
    diamond.rotate(PI / 4)
    diamond.move_to(center)
    pieces.add(diamond)
    return pieces


class FractalCircle(Scene):
    def construct(self):
        circle = Circle(radius=R, color=CIRCLE_COLOR, stroke_width=3)
        self.play(Create(circle), run_time=1.2)
        self.wait(0.2)

        half = R + S
        starts = np.arange(-half, half, S)

        full_cells = []      # (Rectangle mobject, center)
        partial_mobs = []    # clipped VMobjects

        for x0 in starts:
            for y0 in starts:
                kind = cell_classification(x0, y0, S, R)
                if kind == "out":
                    continue

                center = np.array([x0 + S / 2, y0 + S / 2, 0])
                rect = Rectangle(
                    width=S, height=S,
                    stroke_width=1.5, stroke_color=CIRCLE_COLOR,
                )
                rect.move_to(center)

                if kind == "full":
                    rect.set_fill(FULL_COLOR, opacity=0.55)
                    full_cells.append((rect, center))
                else:
                    clipped = Intersection(
                        rect, circle,
                        stroke_width=1.5, stroke_color=CIRCLE_COLOR,
                        fill_color=PARTIAL_COLOR, fill_opacity=0.55,
                    )
                    # A cell whose corners straddle the classification
                    # boundary can still produce a degenerate (pointless)
                    # intersection; skip it rather than animate nothing.
                    if clipped.family_members_with_points():
                        partial_mobs.append(clipped)

        grid_group = VGroup(*(rect for rect, _ in full_cells), *partial_mobs)
        self.play(LaggedStartMap(FadeIn, grid_group, lag_ratio=0.02), run_time=3.0)
        self.wait(0.3)

        # Seed the formation in the full cell nearest the centre.
        source_rect, source_center = min(
            full_cells, key=lambda item: np.linalg.norm(item[1])
        )
        source_formation = make_formation(source_center, S)

        self.play(Indicate(source_rect, color=PATTERN_COLOR, scale_factor=1.08), run_time=0.8)
        self.play(LaggedStartMap(GrowFromCenter, source_formation, lag_ratio=0.15), run_time=1.5)
        self.wait(0.4)

        # Replicate the exact same formation into every other full cell.
        replicate_anims = []
        for rect, center in full_cells:
            if np.allclose(center, source_center):
                continue
            target_formation = make_formation(center, S)
            replicate_anims.append(
                AnimationGroup(
                    *[
                        TransformFromCopy(src_piece, tgt_piece)
                        for src_piece, tgt_piece in zip(source_formation, target_formation)
                    ]
                )
            )

        self.play(LaggedStart(*replicate_anims, lag_ratio=0.12), run_time=4.5)
        self.wait(1.5)
