"""Shared 3-D point-cloud geometry for Chapter C.

Everything live here is built ONCE and moved by an updater, rather than rebuilt
per frame by `always_redraw`. Two reasons, both specific to 3-D:

  * the cairo renderer draws a Sphere as a mesh of quads, so rebuilding one
    every frame is the difference between a render that finishes and one that
    does not;
  * `add_fixed_orientation_mobjects` and `add_fixed_in_frame_mobjects` register
    the mobject *instance* with the camera, and an `always_redraw` hands back a
    new instance each frame -- which silently drops the registration and lets
    the readout tumble away with the camera.
"""

from __future__ import annotations

import numpy as np
from manim import AnimationGroup, Dot, Sphere, ThreeDAxes, ValueTracker, VGroup

from .palette import CLOUD, MUTED, TARGET


class CloudRig:
    """A stable cloud, shape state, axes, and covariance ellipsoid.

    The dot instances survive every shape change.  ``current_points()`` is the
    numerical source of truth future projection geometry should read.
    """

    SCALE = 1.15  # world units per standard deviation

    def __init__(self, points, *, shape=(1.0, 1.0, 1.0), scale: float = SCALE,
                 dot_radius: float = 0.035, dot_colour=CLOUD):
        self.base_points = self._checked_points(points)
        self._target_points = np.array(self.base_points, copy=True)
        self._point_mix = ValueTracker(0.0)
        self.scale = float(scale)
        self.shape_trackers = tuple(
            ValueTracker(float(value)) for value in self._checked_shape(shape)
        )

        self.axes = ThreeDAxes(
            x_range=(-3, 3, 1), y_range=(-3, 3, 1), z_range=(-3, 3, 1),
            x_length=6.4, y_length=6.4, z_length=6.4,
        )
        self.axes.set_stroke(MUTED, 1.5, opacity=0.6)

        # --- the cloud -----------------------------------------------------
        # Flat dots, billboarded by the camera, rather than 260 Dot3D spheres.
        # A Dot3D is a Sphere, and 260 meshes redrawn per frame does not render
        # in any useful amount of time; a flat Dot kept facing the camera is
        # indistinguishable at this size and costs one VMobject each.
        self.dots = VGroup(*(
            Dot(radius=dot_radius, color=dot_colour, fill_opacity=0.9)
            .move_to(point)
            for point in self.current_points()
        ))

        def move_cloud(group):
            for dot, point in zip(group, self.current_points()):
                dot.move_to(point)

        self._move_cloud = move_cloud
        self.dots.add_updater(move_cloud)

        # --- the covariance ellipsoid --------------------------------------
        self.ellipsoid = Sphere(radius=1.0, resolution=(24, 12))
        self.ellipsoid.set_fill(TARGET, opacity=0.16)
        self.ellipsoid.set_stroke(TARGET, width=0.5, opacity=0.25)

        # The pristine unit-sphere geometry, so each frame scales the ORIGINAL
        # rather than compounding stretch factors -- which drifts, and cannot
        # come back once an axis has been squashed to 1e-3.
        self.unit_points = [
            np.array(submob.points)
            for submob in self.ellipsoid.family_members_with_points()
        ]

        def reshape_ellipsoid(mob):
            shape_now = np.clip(self.shape_values(), 1e-3, None) * self.scale
            for submob, unit_points in zip(
                mob.family_members_with_points(), self.unit_points
            ):
                submob.set_points(unit_points * shape_now)

        self._reshape_ellipsoid = reshape_ellipsoid
        reshape_ellipsoid(self.ellipsoid)
        self.ellipsoid.add_updater(reshape_ellipsoid)

    @staticmethod
    def _checked_points(points) -> np.ndarray:
        points = np.asarray(points, dtype=float)
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("points must have shape (N, 3)")
        return np.array(points, copy=True)

    @staticmethod
    def _checked_shape(shape) -> np.ndarray:
        shape = np.asarray(shape, dtype=float)
        if shape.shape != (3,):
            raise ValueError("shape must contain three axis scales")
        return shape

    def shape_values(self) -> np.ndarray:
        """Current standard-deviation scale along each world axis."""
        return np.array([
            tracker.get_value() for tracker in self.shape_trackers
        ])

    def current_points(self) -> np.ndarray:
        """Current world positions, shared by dots and future projections."""
        mix = self._point_mix.get_value()
        base = (
            (1.0 - mix) * self.base_points
            + mix * self._target_points
        )
        return base * self.shape_values() * self.scale

    def set_shape(self, shape) -> None:
        """Set all three axis scales without animation."""
        for tracker, value in zip(
            self.shape_trackers, self._checked_shape(shape)
        ):
            tracker.set_value(float(value))
        self.dots.update(0)
        self.ellipsoid.update(0)

    def animate_shape(self, shape) -> AnimationGroup:
        """Animate all shape coordinates as one scene-level operation."""
        return AnimationGroup(*(
            tracker.animate.set_value(float(value))
            for tracker, value in zip(
                self.shape_trackers, self._checked_shape(shape)
            )
        ), lag_ratio=0.0)

    def set_base_points(self, points) -> None:
        """Adopt new geometry while preserving every existing dot instance."""
        points = self._checked_points(points)
        if points.shape != self.base_points.shape:
            raise ValueError(
                "replacement points must preserve the existing dot count"
            )
        self.base_points = points
        self._target_points = np.array(points, copy=True)
        self._point_mix.set_value(0.0)
        self.dots.update(0)

    def animate_base_points(self, points):
        """Morph to a new point set through the existing dot updater."""
        points = self._checked_points(points)
        if points.shape != self.base_points.shape:
            raise ValueError(
                "replacement points must preserve the existing dot count"
            )
        mix = self._point_mix.get_value()
        self.base_points = (
            (1.0 - mix) * self.base_points
            + mix * self._target_points
        )
        self._target_points = points
        self._point_mix.set_value(0.0)
        self.dots.update(0)
        return self._point_mix.animate.set_value(1.0)

    def mount(self, scene, *, axes: bool = True,
              ellipsoid: bool = True) -> None:
        """Add the requested furniture and register the stable dot instances."""
        if axes:
            scene.add(self.axes)
        if ellipsoid:
            scene.add(self.ellipsoid)
        scene.add_fixed_orientation_mobjects(*self.dots)
        # Registering the individual billboards restructures the scene's
        # top-level mobjects and removes their parent VGroup. Re-add that SAME
        # group afterward: it owns the one cloud updater, while the camera's
        # fixed-orientation registry still owns the same Dot instances.
        scene.add(self.dots)
        self.dots.update(0)
        if ellipsoid:
            self.ellipsoid.update(0)

    def freeze(self) -> None:
        """Bake the current endpoint before a transform, removal, or handoff."""
        self.dots.update(0)
        self.ellipsoid.update(0)
        self.dots.clear_updaters()
        self.ellipsoid.clear_updaters()
