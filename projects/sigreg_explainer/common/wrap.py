"""The number-line wrap: geometry shared by Acts 4, 5, 6 and 10.

Validated by proto_wrap.py before any act was built.

A point at arc-length `a` along a straight line, rolled up to curvature `kappa`,
sits at (r*sin(a*kappa), r*(1-cos(a*kappa))) with r = 1/kappa. As kappa -> 0 that
tends to (a, 0), the straight line; at kappa = 1 it is the unit circle centred at
(0, 1), tangent to the x-axis at the origin.

Composing with `rigid` at s = 1 (translate down 1, rotate +90 CCW) sends
a -> (cos a, sin a) exactly. So with a = t*x the finished roll IS the complex-plane
parametrisation e^{itx}, with no fudge factor. That exactness is why this
construction was chosen over cross-fading a line into a circle.
"""

from __future__ import annotations

import numpy as np

PI = np.pi


def roll(a, kappa: float) -> np.ndarray:
    """Position of arc-length `a` on a line rolled to curvature `kappa`."""
    a = np.atleast_1d(np.asarray(a, dtype=float))
    if kappa < 1e-6:
        x, y = a, np.zeros_like(a)
    else:
        r = 1.0 / kappa
        x, y = r * np.sin(a * kappa), r * (1.0 - np.cos(a * kappa))
    return np.stack([x, y, np.zeros_like(x)], axis=-1)


def rigid(points: np.ndarray, s: float) -> np.ndarray:
    """Interpolate the rigid move carrying the rolled circle into standard
    complex-plane position (centre at origin, a=0 at (1,0)). s in [0, 1]."""
    pts = np.array(points, dtype=float, copy=True)
    pts[..., 1] -= s
    ang = s * PI / 2
    c, sn = np.cos(ang), np.sin(ang)
    x, y = pts[..., 0].copy(), pts[..., 1].copy()
    pts[..., 0] = c * x - sn * y
    pts[..., 1] = sn * x + c * y
    return pts


def wrapped(a, kappa: float = 1.0, s: float = 1.0, radius: float = 1.0,
            centre=None) -> np.ndarray:
    """Full pipeline: arc-length -> rolled -> rigid -> scaled -> placed."""
    pts = rigid(roll(a, kappa), s) * radius
    if centre is not None:
        pts = pts + np.asarray(centre, dtype=float)
    return pts


def unit_arrow_tips(h, t: float, radius: float = 1.0, centre=None) -> np.ndarray:
    """Where the sample arrows point: e^{i t h_n}, scaled and placed."""
    return wrapped(np.asarray(h, dtype=float) * t, 1.0, 1.0, radius, centre)


def ecf(h: np.ndarray, t) -> np.ndarray:
    """Empirical characteristic function (1/N) sum exp(i t h_n)."""
    t = np.atleast_1d(np.asarray(t, dtype=float))
    return np.exp(1j * t[:, None] * np.asarray(h)[None, :]).mean(axis=1)


def gaussian_cf(t) -> np.ndarray:
    """Characteristic function of N(0,1): the target fingerprint."""
    return np.exp(-np.asarray(t, dtype=float) ** 2 / 2)
