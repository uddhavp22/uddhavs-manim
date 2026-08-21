"""Numerical Gaussianity scores shared by Chapter C.

This module is deliberately pure NumPy.  Scene geometry may display these
values, but it must not own a second implementation of the statistic.
"""

from __future__ import annotations

import numpy as np

from .wrap import ecf, gaussian_cf

# Chapter C's settings, carried over from `b11_fingerprint_to_loss.py`'s
# approved inline computation. They live here rather than in each scene so a
# scene and `facts.py` cannot drift apart on the grid or the weight while both
# call the same function -- which would give a checked claim and a rendered
# number that quietly disagree.
EP_GRID = np.linspace(-8.0, 8.0, 4000)
EP_LAMBDA = 1.0


def epps_pulley(samples, lam: float, grid) -> float:
    """Empirical Epps--Pulley statistic on a supplied frequency grid.

    The operation order matches Chapter B's approved inline computation:
    ``N * trapezoid(w * |hat(phi) - phi_0|^2, grid)``.
    """
    samples = np.asarray(samples, dtype=float)
    grid = np.asarray(grid, dtype=float)
    weight = np.exp(-grid ** 2 / (2 * lam ** 2))
    return float(len(samples) * np.trapezoid(
        weight * np.abs(ecf(samples, grid) - gaussian_cf(grid)) ** 2,
        grid,
    ))


def sigreg(Z, U, lam: float, knots) -> float:
    """Average Epps--Pulley score of the projections in ``U``.

    ``Z`` has shape ``(N, D)`` and ``U`` has shape ``(M, D)``.  Rows of ``U``
    are the sampled unit directions; normalization remains the caller's job so
    the directions driving the geometry are exactly those being scored.
    """
    Z = np.asarray(Z, dtype=float)
    U = np.asarray(U, dtype=float)
    if Z.ndim != 2 or U.ndim != 2 or Z.shape[1] != U.shape[1]:
        raise ValueError(
            "Z and U must have shapes (N, D) and (M, D) with the same D"
        )
    if len(U) == 0:
        raise ValueError("U must contain at least one direction")
    return float(np.mean([
        epps_pulley(Z @ direction, lam, knots)
        for direction in U
    ]))
