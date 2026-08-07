"""Chapter C.2 — what shape should embeddings have? (3-D covariance)

The second risky bet in the build order (PLAN.md section 9): does 3-D actually
read in a rendered frame, where there is no interactivity and depth has to come
from motion parallax alone?

A cloud in R^3 with its covariance ellipsoid, squashed through
    (1,1,1) ball  ->  (1,1,0) pancake  ->  (1,0,0) rod  ->  (0,0,0) point
with the eigenvalues counting down alongside. This is the shot that makes
"collapse" mean something precise, and it is the main justification for 3-D.

Everything live here is built ONCE and moved by an updater, rather than rebuilt
per frame by `always_redraw`. Two reasons, both specific to 3-D:

  * the cairo renderer draws a Sphere as a mesh of quads, so rebuilding one
    every frame is the difference between a render that finishes and one that
    does not;
  * `add_fixed_orientation_mobjects` and `add_fixed_in_frame_mobjects` register
    the mobject *instance* with the camera, and an `always_redraw` hands back a
    new instance each frame -- which silently drops the registration and lets
    the readout tumble away with the camera.

Render:
    ./render.sh projects/sigreg_explainer/chapterC/c02_covariance.py C02 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data
from common.palette import CLOUD, COLLAPSE, MUTED, TARGET
from common.type import Text

SCALE = 1.15   # world units per standard deviation


class C02(ThreeDScene):
    def construct(self):
        base = data.gaussian_3d(n=260)

        # Eigenvalue trackers: the standard deviation along each axis.
        ex, ey, ez = (ValueTracker(1.0) for _ in range(3))

        def eigs():
            return np.array([ex.get_value(), ey.get_value(), ez.get_value()])

        axes = ThreeDAxes(
            x_range=(-3, 3, 1), y_range=(-3, 3, 1), z_range=(-3, 3, 1),
            x_length=6.4, y_length=6.4, z_length=6.4,
        )
        axes.set_stroke(MUTED, 1.5, opacity=0.6)

        # --- the cloud -----------------------------------------------------
        # Flat dots, billboarded by the camera, rather than 260 Dot3D spheres.
        # A Dot3D is a Sphere, and 260 meshes redrawn per frame does not render
        # in any useful amount of time; a flat Dot kept facing the camera is
        # indistinguishable at this size and costs one VMobject each.
        cloud = VGroup(*(
            Dot(radius=0.035, color=CLOUD, fill_opacity=0.9).move_to(p)
            for p in base * SCALE))

        def move_cloud(group):
            for dot, point in zip(group, base * eigs() * SCALE):
                dot.move_to(point)

        cloud.add_updater(move_cloud)

        # --- the covariance ellipsoid --------------------------------------
        ellipsoid = Sphere(radius=1.0, resolution=(24, 12))
        ellipsoid.set_fill(TARGET, opacity=0.16)
        ellipsoid.set_stroke(TARGET, width=0.5, opacity=0.25)

        # The pristine unit-sphere geometry, so each frame scales the ORIGINAL
        # rather than compounding stretch factors -- which drifts, and cannot
        # come back once an axis has been squashed to 1e-3.
        unit_points = [np.array(sm.points)
                       for sm in ellipsoid.family_members_with_points()]

        def reshape_ellipsoid(mob):
            e = np.clip(eigs(), 1e-3, None) * SCALE
            for submob, points in zip(mob.family_members_with_points(),
                                      unit_points):
                submob.set_points(points * e)

        reshape_ellipsoid(ellipsoid)
        ellipsoid.add_updater(reshape_ellipsoid)

        # --- readout, pinned to the screen rather than the 3-D world --------
        label = MathTex(R"(\lambda_1, \lambda_2, \lambda_3) = ", font_size=34)
        values = VGroup(*(DecimalNumber(1.0, num_decimal_places=2, font_size=34)
                          for _ in range(3)))
        readout = VGroup(label, *values).arrange(RIGHT, buff=0.16)
        readout.to_edge(DOWN, buff=0.45)

        def update_readout(group):
            e = eigs()
            for number, value in zip(group[1:], e ** 2):
                number.set_value(value)
            group.arrange(RIGHT, buff=0.16).to_edge(DOWN, buff=0.45)
            group.set_color(COLLAPSE if (e ** 2 < 0.05).any() else TARGET)

        update_readout(readout)
        readout.add_updater(update_readout)

        caption = self._cap("full rank")

        self.set_camera_orientation(phi=70 * DEGREES, theta=-32 * DEGREES)
        # Motion parallax: with no interactivity, a still 3-D frame reads as a
        # flat drawing. 3 degrees per second is enough to separate the axes
        # without the shot feeling like it is spinning.
        self.begin_ambient_camera_rotation(rate=3 * DEGREES)

        self.add(axes, ellipsoid, cloud)
        self.add_fixed_orientation_mobjects(*cloud)
        self.add_fixed_in_frame_mobjects(readout, caption)
        self.wait(2.5)

        # ball -> pancake
        self.play(
            ez.animate.set_value(0.03),
            Transform(caption, self._cap("rank 2 — a pancake")),
            run_time=3,
        )
        self.wait(2)

        # pancake -> rod
        self.play(
            ey.animate.set_value(0.03),
            Transform(caption, self._cap("rank 1 — a rod")),
            run_time=3,
        )
        self.wait(2)

        # rod -> point
        self.play(
            ex.animate.set_value(0.03),
            Transform(caption, self._cap("rank 0 — total collapse")),
            run_time=3,
        )
        self.wait(2.5)

        self.stop_ambient_camera_rotation()
        cloud.clear_updaters()
        ellipsoid.clear_updaters()
        readout.clear_updaters()

    def _cap(self, s: str) -> Text:
        return Text(s, font_size=34).to_edge(UP, buff=0.5)
