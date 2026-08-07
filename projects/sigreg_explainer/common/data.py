"""Fixed sample data for the SIGReg explainer.

Every cloud is generated from a named, fixed seed so that a re-render of one act
produces the byte-identical cloud used in another. Without this, "the same cloud"
continuity silently breaks between separately-rendered files (PLAN.md section 8).
"""

from __future__ import annotations

import numpy as np

# Arrows drawn on the unit circle. Capped for legibility and frame rate; the
# plan's measured ceiling before the picture turns to soup.
N_ARROWS = 40

# Hand-placed points for the first wrap reveal. Deliberately not random: that
# shot is about geometry, and a jittery cloud distracts from it.
DEMO_LINE = np.array([-2.5, -1.7, -1.0, -0.4, 0.0, 0.5, 1.1, 1.8, 2.6])


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def gaussian_1d(n: int = N_ARROWS, seed: int = 34094) -> np.ndarray:
    """The standard-normal sample used across Acts 4, 5, 6 and 10.

    Seed chosen (by search over 60k seeds) so this particular draw of 40 has
    sample mean -0.0005 and sd 1.0001 -- i.e. a *representative* draw rather
    than a lopsided one. This is honest: the sample is real, and the residual
    departure of its empirical CF from e^{-t^2/2} at large t survives intact.
    That departure is the finite-sample noise floor, and Act 6 uses it.
    """
    return _rng(seed).standard_normal(n)


def collapsed_1d(n: int = N_ARROWS, scale: float = 0.02,
                 seed: int = 11) -> np.ndarray:
    """A near-collapsed projection: all mass at ~0, with a whisper of noise so
    it is not the exact-zero stationary point discussed in Act 9."""
    return _rng(seed).standard_normal(n) * scale


def bimodal_1d(n: int = N_ARROWS, seed: int = 7) -> np.ndarray:
    """Mean 0, variance ~1, but plainly not Gaussian. Act 6 uses this to show a
    narrow frequency window failing to notice the difference."""
    rng = _rng(seed)
    signs = rng.choice([-1.0, 1.0], size=n)
    x = signs * 1.0 + rng.standard_normal(n) * 0.25
    return (x - x.mean()) / x.std()


ALIAS_T = 3.0


def aliased_1d(t: float = ALIAS_T, k: int = 3) -> np.ndarray:
    """A batch that is plainly spread out, yet whose arrows all coincide at
    wrapping speed `t`.

    Every value is a multiple of 2*pi/t, so t*h_n is a multiple of 2*pi and every
    arrow lands on the same spot: |phi(t)| = 1, exactly what total collapse gives.
    Any other frequency exposes it immediately. This is the honest reason a single
    wrapping speed is not enough, and it is why Act 4 sweeps t.
    """
    return np.arange(-k, k + 1) * (2 * np.pi / t)


def ring_2d(n: int = 240, radius: float = 1.0, jitter: float = 0.06,
            seed: int = 31) -> np.ndarray:
    """A ring with the same mean and (isotropic) covariance as a Gaussian.
    Act 10's counterexample to matching only the first two moments."""
    rng = _rng(seed)
    ang = rng.uniform(0, 2 * np.pi, n)
    r = radius + rng.standard_normal(n) * jitter
    return np.stack([r * np.cos(ang), r * np.sin(ang)], axis=1)


def gaussian_3d(n: int = 220, seed: int = 5) -> np.ndarray:
    """Isotropic cloud in R^3 for the latent-space (3-D) acts."""
    return _rng(seed).standard_normal((n, 3))


def degenerate_3d(eigs=(1.0, 1.0, 1.0), n: int = 220,
                  seed: int = 5) -> np.ndarray:
    """The same cloud squashed to given standard deviations along the axes.
    Act 3 walks eigs from (1,1,1) -> (1,1,0) -> (1,0,0) -> (0,0,0):
    ball -> pancake -> rod -> point."""
    return gaussian_3d(n, seed) * np.asarray(eigs, dtype=float)


def diagonal_2d(n: int = 200, seed: int = 13) -> np.ndarray:
    """Z = [X, X]. Both marginals are exactly N(0,1) and both pass a
    coordinate-wise normality test, yet the cloud is a line: covariance
    eigenvalues (2, 0). Act 7's counterexample."""
    x = _rng(seed).standard_normal(n)
    return np.stack([x, x], axis=1)
