#!/usr/bin/env python3
"""Executable claims ledger — every number this video says out loud.

PLAN.md section 7 used to assert these in a markdown table. Prose cannot be
rerun, so it rots silently the moment a seed, a range or a sample size changes
and nothing anywhere complains. Each claim is a function here instead: it
recomputes the value and asserts it, and its docstring names the scene that
speaks it.

    python3 projects/sigreg_explainer/facts.py

Exit status is 1 if any claim no longer holds, so a stale number is a build
failure rather than a line of confident narration that happens to be wrong.

Each function's `spoken` attribute is the phrase as the viewer hears it, so a
grep from a scene file lands here.
"""

from __future__ import annotations

import sys
import traceback

import numpy as np
from scipy.special import j0

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from common import data
from common.wrap import ecf, gaussian_cf

REGISTRY: list = []


def claim(scene: str, spoken: str):
    """Register a checked claim, tagged with the scene that speaks it."""
    def wrap(fn):
        fn.scene, fn.spoken = scene, spoken
        REGISTRY.append(fn)
        return fn
    return wrap


# ------------------------------------------------------------------ geometry
@claim("b02", "here it is exactly zero, because these six are evenly spaced")
def roots_of_unity_cancel():
    ang = np.linspace(0, 2 * np.pi, 6, endpoint=False)
    z = np.mean(np.exp(1j * ang))
    assert abs(z) < 1e-15, abs(z)
    return f"|mean of 6 evenly spaced arrows| = {abs(z):.2e}"


@claim("b03", "the roll lands exactly on e^{ia}")
def roll_is_exact():
    from common.wrap import wrapped
    a = np.linspace(-8, 8, 400)
    got = wrapped(a, 1.0, 1.0, 1.0, None)[:, :2]
    want = np.stack([np.cos(a), np.sin(a)], axis=-1)
    err = np.abs(got - want).max()
    assert err < 1e-12, err
    return f"max deviation from e^(ia) = {err:.1e}"


# ------------------------------------------------------------ worked examples
@claim("b05", "the curve it traces is exactly the cosine")
def two_point_is_cosine():
    t = np.linspace(0, 6.5, 700)
    z = ecf(np.array([-1.0, 1.0]), t)
    assert np.abs(z.real - np.cos(t)).max() < 1e-12
    assert np.abs(z.imag).max() < 1e-15
    return f"max|Re phi - cos t| = {np.abs(z.real - np.cos(t)).max():.1e}, " \
           f"max|Im phi| = {np.abs(z.imag).max():.1e}"


@claim("b05", "the curve stays pinned at one")
def constant_batch_has_unit_modulus():
    t = np.linspace(0, 6.5, 700)
    m = np.abs(ecf(np.full(7, 0.9), t))
    assert np.abs(m - 1.0).max() < 1e-12
    return f"max||phi| - 1| = {np.abs(m - 1.0).max():.1e}"


@claim("b05", "the amber one lands back on its own ghost")
def shift_moves_only_the_phase():
    """The translation example is the final experiment in b05."""
    t = np.linspace(0.05, 6.5, 700)
    h = np.array([-1.4, -0.7, -0.2, 0.3, 0.9, 1.5])
    mu = 0.8
    lhs, rhs = ecf(h + mu, t), np.exp(1j * mu * t) * ecf(h, t)
    assert np.abs(lhs - rhs).max() < 1e-12
    mag = np.abs(np.abs(lhs) - np.abs(ecf(h, t))).max()
    assert mag < 1e-12
    # "only the phase" is empty unless the phase actually moved.
    dphase = np.abs(np.angle(lhs) - np.angle(ecf(h, t))).max()
    assert dphase > 1.0, dphase
    return f"|phi_(X+mu) - e^(i mu t) phi_X| = {np.abs(lhs - rhs).max():.1e}; " \
           f"magnitude unchanged to {mag:.1e}; phase moves {dphase:.2f} rad"


@claim("b03", "the red curve sits at exactly zero across the whole range")
def symmetric_batch_is_real():
    """b05 was folded into b03, and so was its batch.

    The scene no longer swaps in a batch nobody has met to make Im phi visible:
    it uses the seven-value clump slice it has been running all along, which is
    lopsided enough on its own, and mirrors *that*. So this claim has to check
    the batch the scene actually draws.
    """
    base = data.bimodal_1d(7)
    sym = np.concatenate([base, -base])
    t = np.linspace(0, 6.5, 700)
    im = np.abs(ecf(sym, t).imag).max()
    assert im < 1e-14, im
    # and the claim is only interesting because the unmirrored batch is NOT real
    lopsided = np.abs(ecf(base, t).imag).max()
    assert lopsided > 0.1, lopsided
    return f"mirrored: max|Im phi| = {im:.1e};  unmirrored: {lopsided:.3f}"


@claim("b05", "the amber curve drops almost to zero before creeping back up")
def shift_batch_magnitude_dips():
    """Spoken over the first sweep, so it has to match the drawn curve."""
    h = np.array([-1.4, -0.7, -0.2, 0.3, 0.9, 1.5])
    t = np.linspace(0, 6.5, 700)
    mag = np.abs(ecf(h, t))
    lo = mag.min()
    assert lo < 0.01, lo                     # "almost to zero"
    assert mag[-1] > 10 * lo, (mag[-1], lo)  # "creeping back up"
    return f"min |phi| = {lo:.3f} at t = {t[mag.argmin()]:.2f}; ends at {mag[-1]:.3f}"


@claim("b07", "indistinguishable from total collapse")
def aliased_batch_looks_collapsed():
    h = data.aliased_1d(3.0, k=3)
    m = abs(ecf(h, [3.0])[0])
    assert abs(m - 1.0) < 1e-12
    assert h.std() > 4.0          # genuinely spread out
    return f"|phi(3.0)| = {m:.4f} on a batch with sd {h.std():.2f}"


@claim("b07", "spread across nearly thirteen units")
def aliased_batch_range():
    """The number printed on screen beside the batch.

    Spoken as "nearly thirteen units" and drawn as "range = 12.6", so it is the
    extent, not the standard deviation -- which is 4.19 and would read as a
    contradiction if the label were vague about which it is.
    """
    h = data.aliased_1d(3.0, k=3)
    rng = float(h.max() - h.min())
    assert abs(rng - 12.6) < 0.05, rng
    return f"range = {rng:.2f} (sd {h.std():.2f})"


@claim("b07", "nudging t collapses the average to almost nothing")
def aliased_batch_breaks_off_resonance():
    """Correction 3's evidence: several nearby frequencies expose the batch.

    The scene now says a handful of frequencies break THIS coincidence, rather
    than that sweeping removes the problem -- so the handful has to be real.
    """
    h = data.aliased_1d(3.0, k=3)
    probes = [1.0, 1.7, 2.4, 4.1, 5.2]
    mags = [abs(ecf(h, [t])[0]) for t in probes]
    assert max(mags) < 0.35, mags
    return "|phi| at t = " + ", ".join(f"{t}:{m:.2f}"
                                       for t, m in zip(probes, mags))


# ------------------------------------------------------- which frequencies
@claim("b09", "at t point three the vertical gap is less than one thousandth")
def low_t_is_blind():
    """Check the vertical gap drawn between the two real-coordinate curves."""
    g, b = data.gaussian_1d(40), data.bimodal_1d(40)
    lo = abs(ecf(g, [0.3])[0].real - ecf(b, [0.3])[0].real)
    hi = abs(ecf(g, [3.0])[0].real - ecf(b, [3.0])[0].real)
    assert lo < 0.001, lo
    assert abs(hi - 0.7623) < 5e-4, hi
    # the batches must actually agree on mean and variance, or the point is moot
    assert abs(g.mean() - b.mean()) < 5e-3 and abs(g.std() - b.std()) < 5e-3
    return f"vertical gap at t=0.3 is {lo:.4f}; at t=3.0 is {hi:.4f}"


@claim("b09", "the expected squared length settles at one over N")
def noise_floor_is_one_over_n():
    rng = np.random.default_rng(0)
    vals = [abs(ecf(rng.standard_normal(40), [6.0])[0]) ** 2 for _ in range(4000)]
    got = float(np.mean(vals))
    assert abs(got - 0.025) < 0.003, got
    assert gaussian_cf(6.0) ** 2 < 1e-15
    return f"E|phi_40(6)|^2 = {got:.4f} vs 1/N = 0.0250; truth = {gaussian_cf(6.0)**2:.1e}"


@claim("b11", "the numerical integration window holds over ninety nine per cent of the weighted comparison")
def window_holds_the_mass():
    """The fraction is BATCH-DEPENDENT, so the claim must be a bound.

    PLAN.md rev 4 recorded a single figure, 99.78%, as though it were a
    constant. Measured across batches it runs 99.63% to 99.98%, so any one
    figure is spurious precision and b09 originally spoke one. The honest,
    batch-independent claim is the bound.
    """
    # Integrand of the Epps-Pulley statistic: w(t)|phi_N - phi_0|^2, lambda = 1.
    t = np.linspace(1e-6, 12.0, 200_001)
    w = np.exp(-t ** 2 / 2)
    inside = (t >= 0.2) & (t <= 4.0)
    fracs = {}
    for name, h in (("gaussian-40", data.gaussian_1d(40)),
                    ("bimodal-40", data.bimodal_1d(40)),
                    ("collapsed", data.collapsed_1d(40)),
                    ("gaussian-256",
                     np.random.default_rng(1).standard_normal(256))):
        integrand = w * np.abs(ecf(h, t) - gaussian_cf(t)) ** 2
        fracs[name] = (np.trapezoid(integrand[inside], t[inside])
                       / np.trapezoid(integrand, t))
    lo, hi = min(fracs.values()), max(fracs.values())
    assert lo > 0.99, fracs
    return f"[0.2, 4] holds {100 * lo:.2f}%-{100 * hi:.2f}% of the mass " \
           f"across 4 batches (never a single fixed figure)"


@claim("b09", "the shape gap crosses sampling variation near one point one and four point six")
def signal_noise_crossings():
    grid = np.linspace(0.0, 6.4, 700)
    gaussian = data.gaussian_1d(40)
    bimodal = data.bimodal_1d(40)
    gap = np.abs(ecf(gaussian, grid).real - ecf(bimodal, grid).real)
    rng = np.random.default_rng(20260806)
    estimates = np.asarray([
        ecf(rng.standard_normal(40), grid).real
        for _ in range(14)
    ])
    variation = estimates.std(axis=0)
    changes = np.flatnonzero(np.diff(np.sign(gap - variation)))
    crossings = [grid[index] for index in changes if grid[index] > 0.1]
    assert len(crossings) == 2, crossings
    assert abs(crossings[0] - 1.1) < 0.05, crossings
    assert abs(crossings[1] - 4.6) < 0.05, crossings
    return f"signal/noise crossings at t={crossings[0]:.2f} and {crossings[1]:.2f}"


# ----------------------------------------------------------------- histograms
@claim("b01", "same forty numbers, different answer")
def bins_are_arbitrary():
    g = data.gaussian_1d(40)
    a, _ = np.histogram(g, bins=np.arange(-3, 3.01, 0.5))
    b, _ = np.histogram(g, bins=np.arange(-3, 3.01, 0.5) + 0.15)
    assert a.tolist() == [0, 1, 1, 4, 5, 10, 7, 7, 2, 1, 2, 0], a.tolist()
    assert b.tolist() == [1, 0, 2, 6, 5, 10, 6, 5, 2, 3, 0, 0], b.tolist()
    return f"offset 0.00 -> {a.tolist()};  offset 0.15 -> {b.tolist()}"


@claim("b01", "at a width of one and a half the counts read two, fourteen, twenty four, zero")
def bins_delete_structure():
    c, _ = np.histogram(data.bimodal_1d(40), bins=np.arange(-3, 3.0001, 1.5))
    assert c.tolist() == [2, 14, 24, 0], c.tolist()
    return f"bimodal at width 1.5 -> {c.tolist()} (two clumps gone)"


@claim("b01", "it sits at seven, and then it is six")
def bins_are_a_staircase():
    g = data.gaussian_1d(40)
    i = int(np.argmin(np.abs(g - 0.5)))
    edges = np.arange(-3, 3.01, 0.5)
    before = g.copy(); before[i] = 0.4990
    after = g.copy(); after[i] = 0.5000
    cb, _ = np.histogram(before, bins=edges)
    ca, _ = np.histogram(after, bins=edges)
    assert cb[6] == 7 and ca[6] == 6, (cb[6], ca[6])
    return f"x_i 0.4990 -> count {cb[6]};  x_i 0.5000 -> count {ca[6]}"


# ---------------------------------------------------------------- the target
@claim("b10", "the fingerprint of a standard Gaussian is e to the minus t squared over two")
def gaussian_cf_solves_ode():
    t = np.linspace(0, 6, 2001)
    phi = gaussian_cf(t)
    dphi = np.gradient(phi, t)
    interior = slice(1, -1)
    assert np.abs(dphi[interior] + t[interior] * phi[interior]).max() < 1e-5
    assert abs(phi[0] - 1.0) < 1e-15
    return f"max|phi' + t phi| = {np.abs(dphi[interior] + t[interior] * phi[interior]).max():.1e}; phi(0) = {phi[0]:.1f}"


@claim("b06", "phi of zero is one")
def phi_at_zero_is_one():
    for h in (data.gaussian_1d(40), data.bimodal_1d(40), np.full(24, 1.3)):
        assert abs(ecf(h, [0.0])[0] - 1.0) < 1e-15
    return "phi(0) = 1 for all three batches, to machine precision"


@claim("b06", "the hump decays and stays down, while the clumps swing the "
              "average all the way over to the negative side")
def toy_batches_have_different_curves():
    """Part 1's closing claim: the opening experiment, answered.

    b00 shows two batches agreeing on count, mean and variance. b06 draws both
    characteristic functions on one pair of axes and says they are nothing
    alike. Every part of that has to hold on the batches actually drawn --
    including the direction of the difference, since the narration says the
    clumps go *negative* and the hump does not.
    """
    bell, clumps = data.gaussian_1d(40), data.bimodal_1d(40)
    assert len(bell) == len(clumps) == 40
    assert abs(bell.mean() - clumps.mean()) < 5e-3
    assert abs(bell.var() - clumps.var()) < 5e-3

    t = np.linspace(0, 6.5, 700)
    b, c = ecf(bell, t).real, ecf(clumps, t).real
    assert abs(b[0] - 1.0) < 1e-15 and abs(c[0] - 1.0) < 1e-15  # one anchor
    assert b.min() > 0.0, b.min()          # "stays down", never negative
    assert c.min() < -0.6, c.min()         # "all the way over to the negative"
    gap = np.abs(b - c)
    assert gap.max() > 0.7, gap.max()
    return (f"same 40 numbers, mean {bell.mean():+.4f}/{clumps.mean():+.4f}, "
            f"var {bell.var():.4f}/{clumps.var():.4f}; "
            f"Re phi: hump min {b.min():+.3f}, clumps min {c.min():+.3f}; "
            f"widest gap {gap.max():.3f} at t = {t[gap.argmax()]:.2f}")


# ----------------------------------------------------------------- the score
@claim("b11", "a factor of fifty six")
def score_separates_batches():
    t = np.linspace(0.2, 4.0, 4001)
    tgt = gaussian_cf(t)
    g = np.trapezoid(np.abs(ecf(data.gaussian_1d(40), t) - tgt) ** 2, t)
    b = np.trapezoid(np.abs(ecf(data.bimodal_1d(40), t) - tgt) ** 2, t)
    assert abs(g - 0.0184) < 5e-4 and abs(b - 1.0369) < 5e-3, (g, b)
    assert 55 < b / g < 58
    return f"unweighted: gaussian {g:.4f}, bimodal {b:.4f}, ratio {b / g:.1f}x"


@claim("b11", "putting the weight in barely moves it")
def weighting_preserves_the_verdict():
    """Source fidelity: the displayed formula carries w(t) and an N prefactor.

    The animation shows the UNWEIGHTED area, so b11 must be able to say the
    refinement does not change the verdict. It does not -- 56.4x becomes 57.3x.
    """
    t = np.linspace(0.2, 4.0, 4001)
    w, tgt = np.exp(-t ** 2 / 2), gaussian_cf(t)
    gw = np.trapezoid(w * np.abs(ecf(data.gaussian_1d(40), t) - tgt) ** 2, t)
    bw = np.trapezoid(w * np.abs(ecf(data.bimodal_1d(40), t) - tgt) ** 2, t)
    assert 55 < bw / gw < 60, bw / gw
    return f"weighted ratio {bw / gw:.1f}x (unweighted 56.4x); " \
           f"T = N*int: gaussian {40 * gw:.3f}, bimodal {40 * bw:.3f}"


# ------------------------------------------------------- Chapter C (unbuilt)
@claim("c05", "both marginals are exactly standard normal, and the cloud is a line")
def diagonal_is_rank_one():
    """C05's construction, asserted as construction rather than measured.

    `exactly` is the load-bearing word and it is why `data.diagonal_2d`
    standardizes: a raw draw of 200 has sample mean 0.043 and sd 1.021, so the
    sentence would be true only of the population it was drawn from and not of
    the 200 points on screen.
    """
    z = data.diagonal_2d(200)
    eig = np.linalg.eigvalsh(np.cov(z.T))
    u = np.array([1.0, -1.0]) / np.sqrt(2)
    proj = z @ u
    assert eig[0] < 1e-12, eig
    assert np.abs(proj).max() < 1e-12
    # Both coordinates, and both of them the same numbers in the same order --
    # which is what makes score(x) and score(y) agree to every place printed.
    for column in z.T:
        assert abs(float(column.mean())) < 1e-12, column.mean()
        assert abs(float(column.std()) - 1.0) < 1e-12, column.std()
    assert np.array_equal(z[:, 0], z[:, 1])
    return f"covariance eigenvalues ({eig[1]:.2f}, {eig[0]:.1e}); " \
           f"projection on (1,-1)/sqrt2 max |{np.abs(proj).max():.1e}|; " \
           f"both columns mean {z[:, 0].mean():.1e}, sd {z[:, 0].std():.12f}"


@claim("c05", "exactly two make this cloud look right")
def only_the_axes_look_right():
    """C05's closing claim, read off the same trace the scene draws.

    `u^T Z = (u_1 + u_2) X`, so the score depends on the direction only through
    the scale `|u_1 + u_2|`, which is 1 exactly on the two coordinate axes and
    ranges over [0, sqrt(2)] elsewhere. "Exactly two" therefore has to mean:
    the set of directions scoring near the floor is two arcs, and each one
    contains a coordinate axis. Both halves are checked, along with the
    uniformity of the grid -- a half turn's node fraction is only a fraction of
    directions when the nodes are evenly spaced.

    The level is a reading aid, not a threshold the chapter has defined, and it
    is never printed. It is set an order of magnitude above the two minima and
    an order below the 45-degree bump the scene calls "too wide", so the two
    arcs it isolates are the two the picture shows touching the floor.
    """
    from common.score import EP_GRID, EP_LAMBDA, epps_pulley

    z = data.diagonal_2d()
    angles = np.linspace(0.0, np.pi, 361)
    scores = np.array([
        epps_pulley(z @ np.array([np.cos(a), np.sin(a)]), EP_LAMBDA, EP_GRID)
        for a in angles
    ])
    steps = np.diff(angles)
    assert float(steps.max() - steps.min()) < 1e-12, steps

    # The two coordinate directions, and the two the scene calls out as wrong.
    first, second = float(scores[0]), float(scores[180])
    wide, collapsed = float(scores[90]), float(scores[270])
    # "The same number, exactly", spoken -- and the scene prints three places.
    # The two are not bit-identical because `cos(pi/2)` is 6.1e-17 rather than
    # zero, so the agreement is asserted at the precision the viewer is shown
    # and a little beyond, not at the precision of the float.
    assert abs(first - second) < 1e-9, (first, second)
    assert abs(first - float(scores[360])) < 1e-9   # 180 degrees is 0 degrees
    assert wide > 30 * first, (wide, first)
    assert collapsed > 7 * wide, (collapsed, wide)

    # Two arcs on the half turn, one around each coordinate axis. The last node
    # is dropped because 180 degrees IS 0 degrees, and the remaining 360 are
    # then treated as a circle -- so the run straddling the wrap counts once,
    # which is the only way "exactly two" can be counted honestly here.
    low = scores[:-1] < 1.0
    boundaries = int(np.count_nonzero(low != np.roll(low, 1)))
    assert boundaries == 2 * 2, boundaries
    assert low[0] and low[180], (low[0], low[180])  # one arc per axis
    fraction = float(low.mean())
    assert 0.10 <= fraction <= 0.16, fraction
    return (f"score {first:.3f} on both axes, {wide:.3f} at 45 deg, "
            f"{collapsed:.3f} at 135 deg; {fraction:.2f} of the half turn "
            f"below 1.0, in exactly two arcs")


@claim("c06", "their distribution keeps the same bell")
def isotropic_sweep_stays_representative():
    """Guard C06's finite visual sweep against a misleading sample draw.

    The theorem is population-level, but the animation necessarily moves a
    finite dot plot.  Every inspected direction should therefore remain within
    ordinary Gaussian sampling variation rather than producing one visibly bad
    shadow that contradicts the narration.
    """
    from common.score import EP_GRID, EP_LAMBDA, epps_pulley

    z = data.whiten(data.gaussian_2d())
    angles = np.linspace(0.0, np.pi, 37)
    scores = np.array([
        epps_pulley(
            z @ np.array([np.cos(angle), np.sin(angle)]),
            EP_LAMBDA,
            EP_GRID,
        )
        for angle in angles
    ])
    assert float(scores.max()) < 0.25, scores
    return (f"37 half-turn shadows: score {scores.min():.3f}--"
            f"{scores.max():.3f}, mean {scores.mean():.3f}")


@claim("c06", "it's the whole cloud's own characteristic function, "
              "evaluated at the point t u")
def projection_cf_equals_radial_slice():
    """C06's central identity: phi_{u^T Z}(t) = phi_Z(t u), by substitution.

    Not asymptotic: for any finite sample, exp(i t (u^T z_n)) and
    exp(i (t u)^T z_n) are the same complex number term by term, so their
    sample means agree to machine precision regardless of what Z's
    distribution is. This is the identity the scene derives on screen and
    then reads geometrically (SOURCE_MAP.md SS6e) -- checked here on the
    actual cloud c06 draws, at several directions and several t, because the
    animation claims to derive this, not merely illustrate it.
    """
    z = data.whiten(data.gaussian_2d())
    worst = 0.0
    for angle in (0.35, 1.1, 2.4):
        u = np.array([np.cos(angle), np.sin(angle)])
        for t in (0.5, 1.7, 3.0):
            direct = np.mean(np.exp(1j * t * (z @ u)))
            regrouped = np.mean(np.exp(1j * (t * u) @ z.T))
            worst = max(worst, abs(direct - regrouped))
    assert worst < 1e-9, worst
    return f"phi_(u^T Z)(t) = phi_Z(t u) to {worst:.1e}, 3 directions x 3 t"


@claim("c06", "each shadow's characteristic function is e to the minus t "
              "squared over two — the standard Gaussian's own fingerprint")
def swept_projections_match_the_gaussian_fingerprint():
    """The resolved field's formula, grounded in the actual sampled cloud.

    C06 draws phi_Z(xi) = e^{-|xi|^2/2} as the resolved field on the strength
    of "every one of our shadows was standard Gaussian." Checked against the
    same whitened isotropic cloud c06_every_direction.py's
    _standardized_isotropic_points builds (data.gaussian_2d, seed 76), at
    the t values the drawn ring field actually
    spans: several projections' empirical characteristic functions should
    track the population target within ordinary finite-sample noise, and
    stay close to real-valued -- the field is this cloud's real target, not
    a generic complex phi_Z.
    """
    points = data.whiten(data.gaussian_2d(n=200))
    angles = np.deg2rad([10, 95, 200, 300])
    ts = np.array([0.5, 1.5, 2.5, 3.5])
    target = gaussian_cf(ts)
    worst_real, worst_imag = 0.0, 0.0
    for angle in angles:
        u = np.array([np.cos(angle), np.sin(angle)])
        empirical = ecf(points @ u, ts)
        worst_real = max(worst_real, float(np.max(np.abs(empirical.real - target))))
        worst_imag = max(worst_imag, float(np.max(np.abs(empirical.imag))))
    assert worst_real < 0.13, worst_real
    assert worst_imag < 0.15, worst_imag
    return (f"4 directions x 4 t: empirical CF within {worst_real:.3f} of "
            f"e^-t^2/2, imaginary part within {worst_imag:.3f} of 0")


@claim("c06", "the mixture keeps mean zero and covariance identity while "
              "its characteristic functions blend")
def mixture_keeps_moments_and_blends_cfs():
    """The exact population path used to deform Ring into N(0, I).

    Both endpoints are centred with identity covariance, and characteristic
    functions are linear under mixtures. Check several mixture weights and
    several two-dimensional frequencies so the scene's profile formula and
    moment claim stay coupled in the executable ledger.
    """
    ring_sample = data.ring_2d(
        n=220, radius=np.sqrt(2.0), jitter=0.0, seed=31,
    )
    ring_mean_error = float(np.max(np.abs(ring_sample.mean(axis=0))))
    ring_covariance_error = float(np.max(np.abs(
        ring_sample.T @ ring_sample / len(ring_sample) - np.eye(2)
    )))
    assert ring_mean_error < 1e-14, ring_mean_error
    assert ring_covariance_error < 1e-14, ring_covariance_error

    component_means = np.zeros((2, 2))
    component_covariances = np.stack([np.eye(2), np.eye(2)])
    frequencies = np.array([
        [0.0, 0.0], [0.3, -0.8], [1.2, 0.4], [-2.1, 1.7],
    ])
    radii = np.linalg.norm(frequencies, axis=1)
    component_cfs = np.stack([
        j0(np.sqrt(2.0) * radii),
        np.exp(-0.5 * radii ** 2),
    ])

    worst_mean = worst_covariance = worst_cf = 0.0
    for s in np.linspace(0.0, 1.0, 7):
        weights = np.array([1.0 - s, s])
        mean = weights @ component_means
        covariance = sum(
            weight * (
                component_covariance
                + np.outer(component_mean - mean, component_mean - mean)
            )
            for weight, component_mean, component_covariance in zip(
                weights, component_means, component_covariances,
            )
        )
        mixture_cf = weights @ component_cfs
        expected_cf = (
            (1.0 - s) * j0(np.sqrt(2.0) * radii)
            + s * np.exp(-0.5 * radii ** 2)
        )
        worst_mean = max(worst_mean, float(np.max(np.abs(mean))))
        worst_covariance = max(
            worst_covariance,
            float(np.max(np.abs(covariance - np.eye(2)))),
        )
        worst_cf = max(
            worst_cf, float(np.max(np.abs(mixture_cf - expected_cf))),
        )

    assert worst_mean < 1e-15, worst_mean
    assert worst_covariance < 1e-15, worst_covariance
    assert worst_cf < 1e-15, worst_cf
    return (f"ring sample mean/covariance errors {ring_mean_error:.1e}/"
            f"{ring_covariance_error:.1e}; 7 mixtures: mean error "
            f"{worst_mean:.1e}, covariance error {worst_covariance:.1e}, "
            f"CF blend error {worst_cf:.1e}")


@claim("c03", "the arrows average to a pull toward the origin")
def random_target_pulls_to_origin():
    rng = np.random.default_rng(3)
    D, z = 10, rng.standard_normal(10) * 1.5
    targets = rng.standard_normal((200_000, D))
    lhs = float(np.mean(np.sum((z - targets) ** 2, axis=1)))
    rhs = float(z @ z + D)
    assert abs(lhs - rhs) / rhs < 0.01, (lhs, rhs)
    return f"E||z - z*||^2 = {lhs:.3f} vs ||z||^2 + D = {rhs:.3f}"


@claim("c04", "half of every direction in this plane sits down in that band")
def half_the_plane_is_innocent():
    """C04's closing claim, and the shaded band it is read off.

    The scene brackets every direction scoring below `BAND_LEVEL` between two
    dashed boundaries and says half of the plane sits in there. A half turn is every distinct direction (u and -u
    give the same shadow up to sign), so the fraction of the tabulated half
    turn IS the fraction of directions -- provided the table is the uniform
    grid the scene plots, which is asserted here too.
    """
    from common.score import EP_GRID, EP_LAMBDA, epps_pulley

    band_level = 0.5           # chapterC/c04_one_shadow_is_not_enough.BAND_LEVEL
    z = data.clumped_3d()
    angles = np.linspace(0.0, np.pi, 361)
    scores = np.array([
        epps_pulley(z @ np.array([np.cos(a), np.sin(a), 0.0]),
                    EP_LAMBDA, EP_GRID)
        for a in angles
    ])
    low = scores < band_level
    fraction = float(low.mean())
    # "Half", spoken. Anything outside this and the sentence needs rewriting.
    assert 0.45 <= fraction <= 0.55, fraction
    spread = np.degrees(angles[low])
    assert spread.min() > 5.0 and spread.max() < 175.0, spread
    # A uniform grid, so counting nodes is counting directions.
    steps = np.diff(angles)
    assert float(steps.max() - steps.min()) < 1e-12, steps
    return (f"{fraction:.2f} of the half turn scores below {band_level}: "
            f"{spread.min():.0f} to {spread.max():.0f} degrees")


@claim("c04", "the score climbs / drops to almost nothing")
def one_shadow_can_be_innocent():
    """C04's two settled directions, exactly as the meter and the marks read.

    The scene displays 17.095 along the axis the clumps separate on and 0.046 a
    quarter turn later. Both come from `common/score.py` on the same array that
    positions the shadow dots, so this recomputes them from the scene's own
    `clumped_cloud()` rather than from a transcribed constant.
    """
    from common.score import EP_GRID, EP_LAMBDA, epps_pulley

    z = data.clumped_3d()
    alarming = epps_pulley(z @ np.array([1.0, 0.0, 0.0]), EP_LAMBDA, EP_GRID)
    innocent = epps_pulley(z @ np.array([0.0, 1.0, 0.0]), EP_LAMBDA, EP_GRID)
    # Displayed to three places, so the assertion is on what the viewer reads.
    assert f"{alarming:.3f}" == "17.095", alarming
    assert f"{innocent:.3f}" == "0.046", innocent
    # The claim is about shape, not spread: every direction in the turning
    # plane reads a batch at the same scale, so a scale mismatch cannot be
    # what the alarming direction is detecting.
    sd = z.std(axis=0)
    assert abs(sd[0] - 1.0) < 0.02 and abs(sd[1] - 1.0) < 0.02, sd
    return f"score(x-axis) = {alarming:.3f}, score(y-axis) = {innocent:.3f}; " \
           f"coordinate sd ({sd[0]:.3f}, {sd[1]:.3f})"


# ------------------------------------------------------------ C08 knots
def _c08_batch_and_integrand():
    from common.score import EP_LAMBDA
    points = data.whiten(data.gaussian_2d(n=len(data.diagonal_2d())))
    _g, u = data.sampled_directions()
    batch = points @ u[1]

    def integrand(t):
        t = np.atleast_1d(np.asarray(t, dtype=float))
        weight = np.exp(-t ** 2 / (2 * EP_LAMBDA ** 2))
        return len(batch) * weight * np.abs(ecf(batch, t) - gaussian_cf(t)) ** 2

    return batch, integrand


def _c08_knot_sum(integrand, k: int) -> float:
    knots = np.linspace(0.2, 4.0, k)
    return float(2.0 * np.trapezoid(integrand(knots), knots))


@claim("c08", "take the second direction, whose score was 0.049; the score is "
              "the area under that curve")
def windowed_area_is_the_second_direction_score():
    """The area shown is the dense trapezoid integral of the weighted squared
    gap over Chapter B's window, doubled for negative frequencies. It rounds
    to the same three decimals as the full-grid score C07 spoke."""
    from common.score import EP_GRID, EP_LAMBDA, epps_pulley
    batch, integrand = _c08_batch_and_integrand()
    full = epps_pulley(batch, EP_LAMBDA, EP_GRID)
    dense = _c08_knot_sum(integrand, 2000)
    assert f"{dense:.3f}" == f"{full:.3f}" == "0.049", (dense, full)
    return f"full-grid score {full:.5f}, windowed area {dense:.5f}, both 0.049"


@claim("c08", "with four knots the sum comes out at 0.071, well off; with "
              "eight it is already 0.049, within a twentieth of a percent; "
              "sixteen matches the area to every digit we show")
def knot_sums_converge_on_this_batch():
    """Recomputed on the batch actually shown (storyboard C08 flag): the
    source's 0.04% / 0.01% figures are not reused. On this batch four knots
    are 44% off, eight are within 0.05%, sixteen within 0.01%."""
    _batch, integrand = _c08_batch_and_integrand()
    dense = _c08_knot_sum(integrand, 2000)
    sums = {k: _c08_knot_sum(integrand, k) for k in (4, 8, 16)}
    errors = {k: abs(v - dense) / dense for k, v in sums.items()}
    assert f"{sums[4]:.3f}" == "0.071", sums[4]
    assert errors[4] > 0.2, errors[4]
    assert f"{sums[8]:.3f}" == "0.049" and errors[8] < 0.0005, (sums[8], errors[8])
    assert f"{sums[16]:.3f}" == "0.049" and errors[16] < 0.0001, (sums[16], errors[16])
    return (f"sums 4: {sums[4]:.4f} ({errors[4]:.1%}), 8: {sums[8]:.4f} "
            f"({errors[8]:.3%}), 16: {sums[16]:.4f} ({errors[16]:.4%}); "
            f"dense {dense:.4f}")


# ---------------------------------------------------------------------- main
# ------------------------------------------------------------ C07 sampling
@claim("c07", "a Gauss-ian is round, so it has no preferred direction")
def normalised_gaussian_is_uniform_on_the_sphere():
    """SOURCE_MAP.md section 8: u ~ N(0, I_D), u <- u / ||u||.

    In two dimensions the angle of a normalised Gaussian vector must be
    uniform on the circle. Bin one million draws into 36 sectors: each
    sector expects 27,778 with a binomial spread of 0.6%, so the worst of
    36 sectors sits below 2.5% unless the angles are not uniform.
    """
    rng = np.random.default_rng(0)
    g = rng.standard_normal((1_000_000, 2))
    angles = np.arctan2(g[:, 1], g[:, 0]) % (2 * np.pi)
    counts, _ = np.histogram(angles, bins=36, range=(0.0, 2 * np.pi))
    expected = len(g) / 36
    worst = float(np.max(np.abs(counts / expected - 1.0)))
    assert worst < 0.025, worst
    return f"36 sectors of 1M normalised draws: worst deviation {worst:.3%}"


def _c07_scores():
    from common.score import EP_GRID, EP_LAMBDA, epps_pulley
    points = data.whiten(data.gaussian_2d(n=len(data.diagonal_2d())))
    # The same stream the scene draws: seed and count live in common/data.py.
    _g, u = data.sampled_directions()
    scores = np.array([
        epps_pulley(points @ direction, EP_LAMBDA, EP_GRID) for direction in u
    ])
    return scores, np.cumsum(scores) / np.arange(1, len(scores) + 1)


@claim("c07", "we get a lower score, because its shadow is different")
def second_sampled_direction_scores_lower():
    scores, _ = _c07_scores()
    assert scores[1] < scores[0] - 0.04, scores[:2]
    return f"score(u_1) = {scores[0]:.3f}, score(u_2) = {scores[1]:.3f}"


@claim("c07", "after the first few draws the average has mostly settled, and "
              "by thirty-two it barely moves")
def running_average_settles_by_thirty_two():
    """QUALIFICATION (storyboard claim 12): more directions reduce the
    Monte Carlo scatter of the average, not the finite-batch score itself.
    The average over 32 directions is within 0.006 of the average over 8,
    while the individual scores keep spreading over more than 0.1."""
    scores, running = _c07_scores()
    early_jump = float(np.max(np.abs(np.diff(running[:4]))))
    late_drift = float(abs(running[31] - running[7]))
    spread = float(scores.max() - scores.min())
    assert late_drift < 0.006, late_drift
    assert spread > 0.1, spread
    assert running[31] > 0.05, running[31]
    return (f"average: M=2 {running[1]:.3f}, M=8 {running[7]:.3f}, "
            f"M=32 {running[31]:.3f}; early step up to {early_jump:.3f}, "
            f"late drift {late_drift:.3f}, score spread {spread:.3f}")


def _c07_curve():
    from common.score import EP_GRID, EP_LAMBDA, epps_pulley
    points = data.whiten(data.gaussian_2d(n=len(data.diagonal_2d())))
    theta = np.deg2rad(np.arange(0.0, 180.0, 0.5))
    curve = np.array([
        epps_pulley(points @ np.array([np.cos(a), np.sin(a)]), EP_LAMBDA, EP_GRID)
        for a in theta
    ])
    return theta, curve


@claim("c07", "the score averaged over every direction is the average height "
              "of the curve; draw a different thirty-two and the average "
              "comes out almost the same")
def sampled_averages_sit_near_the_curve_mean():
    """The dashed line is the mean of score(u) over the half turn (u and -u
    cast the same shadow, so a half turn is every direction). Both draws of
    32 land within 0.008 of it and within 0.003 of each other, while the
    curve itself spans more than 0.1: the directions are the estimator's
    luck, the curve is the batch's."""
    from common.score import EP_GRID, EP_LAMBDA, epps_pulley
    points = data.whiten(data.gaussian_2d(n=len(data.diagonal_2d())))
    _theta, curve = _c07_curve()
    mean = float(curve.mean())
    averages = []
    for seed in (data.DIRECTION_SEED, data.REDRAW_SEED):
        _g, u = data.sampled_directions(seed=seed)
        averages.append(float(np.mean([
            epps_pulley(points @ d, EP_LAMBDA, EP_GRID) for d in u
        ])))
    assert abs(averages[0] - mean) < 0.008, (averages[0], mean)
    assert abs(averages[1] - mean) < 0.008, (averages[1], mean)
    assert abs(averages[0] - averages[1]) < 0.003, averages
    assert curve.max() - curve.min() > 0.1, (curve.min(), curve.max())
    assert mean > 0.05, mean
    return (f"curve mean {mean:.4f}, span {curve.min():.3f}-{curve.max():.3f}; "
            f"32-draw averages {averages[0]:.4f} and {averages[1]:.4f}")


@claim("c07", "if we do that fifty times, the landings spread evenly all the "
              "way round")
def shown_spray_lands_evenly():
    """The fifty round draws on screen put 5 to 7 landings in each of the
    eight 45-degree sectors."""
    round_draws = data.direction_spray()
    angles = np.degrees(np.arctan2(round_draws[:, 1], round_draws[:, 0])) % 360.0
    counts, _ = np.histogram(angles, bins=8, range=(0.0, 360.0))
    assert counts.min() >= 5 and counts.max() <= 7, counts.tolist()
    return f"round sectors {counts.tolist()}"



# ------------------------------------------------------------------ C09
def _c09_knot_score(batch: np.ndarray, k: int = 16) -> float:
    """The score C08 settled on: K knots across the window, doubled for t<0."""
    from common import layout
    lo, hi = layout.FREQUENCY_WINDOW
    t = np.linspace(lo, hi, k)
    v = len(batch) * np.exp(-t ** 2 / 2) * np.abs(ecf(batch, t) - gaussian_cf(t)) ** 2
    return float(2.0 * np.trapezoid(v, t))


@claim("c09", "with thirty-two directions and sixteen knots, the whole line "
              "comes out at 0.090, which is the number the purple line was "
              "already showing")
def assembled_line_reproduces_the_purple_readout():
    """C07's last frame shows the average over the *redraw* directions
    (seed data.REDRAW_SEED), computed on the full frequency grid. The line
    C09 writes averages the K=16 knot score over the same directions. Both
    must print the same three decimals, or the number is not shown."""
    from common.score import EP_GRID, EP_LAMBDA, epps_pulley
    points = data.whiten(data.gaussian_2d(n=len(data.diagonal_2d())))
    _g, u = data.sampled_directions(seed=data.REDRAW_SEED)
    shown = np.mean([epps_pulley(points @ d, EP_LAMBDA, EP_GRID) for d in u])
    line = np.mean([_c09_knot_score(points @ d) for d in u])
    assert f"{shown:.3f}" == f"{line:.3f}", (shown, line)
    assert abs(shown - line) < 0.001, abs(shown - line)
    return f"C07 purple readout {shown:.4f}, C09 line with K=16 {line:.4f}, both print {line:.3f}"


def main() -> int:
    print("=" * 74)
    print("CLAIMS LEDGER — sigreg_explainer")
    print("=" * 74)
    failed = []
    for fn in REGISTRY:
        try:
            detail = fn()
            print(f"  PASS  {fn.scene:<5} {fn.__name__}")
            print(f"        {detail}")
        except AssertionError:
            failed.append(fn)
            print(f"  FAIL  {fn.scene:<5} {fn.__name__}")
            print(f'        spoken as: "{fn.spoken}"')
            print("        " + traceback.format_exc().strip().splitlines()[-1])
        except Exception as exc:                      # noqa: BLE001
            failed.append(fn)
            print(f"  ERROR {fn.scene:<5} {fn.__name__}: {exc!r}")

    print("-" * 74)
    print(f"{len(REGISTRY) - len(failed)}/{len(REGISTRY)} claims hold")
    if failed:
        print("\nA failing claim means a scene is SPEAKING A NUMBER THAT IS NO "
              "LONGER TRUE.\nFix the scene or the claim before rendering.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
