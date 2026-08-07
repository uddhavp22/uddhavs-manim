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
@claim("b01", "here it is exactly zero, because these six are evenly spaced")
def roots_of_unity_cancel():
    ang = np.linspace(0, 2 * np.pi, 6, endpoint=False)
    z = np.mean(np.exp(1j * ang))
    assert abs(z) < 1e-15, abs(z)
    return f"|mean of 6 evenly spaced arrows| = {abs(z):.2e}"


@claim("b02", "the roll lands exactly on e^{ia}")
def roll_is_exact():
    from common.wrap import wrapped
    a = np.linspace(-8, 8, 400)
    got = wrapped(a, 1.0, 1.0, 1.0, None)[:, :2]
    want = np.stack([np.cos(a), np.sin(a)], axis=-1)
    err = np.abs(got - want).max()
    assert err < 1e-12, err
    return f"max deviation from e^(ia) = {err:.1e}"


# ------------------------------------------------------------ worked examples
@claim("b06", "the curve it traces is exactly the cosine")
def two_point_is_cosine():
    t = np.linspace(0, 6.5, 700)
    z = ecf(np.array([-1.0, 1.0]), t)
    assert np.abs(z.real - np.cos(t)).max() < 1e-12
    assert np.abs(z.imag).max() < 1e-15
    return f"max|Re phi - cos t| = {np.abs(z.real - np.cos(t)).max():.1e}, " \
           f"max|Im phi| = {np.abs(z.imag).max():.1e}"


@claim("b06", "the curve stays pinned at one")
def constant_batch_has_unit_modulus():
    t = np.linspace(0, 6.5, 700)
    m = np.abs(ecf(np.full(7, 0.9), t))
    assert np.abs(m - 1.0).max() < 1e-12
    return f"max||phi| - 1| = {np.abs(m - 1.0).max():.1e}"


@claim("b06b", "the amber one lands back on its own ghost")
def shift_moves_only_the_phase():
    """Retagged from b06: the shift example is its own scene now (b06b)."""
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


@claim("b02", "the red curve sits at exactly zero across the whole range")
def symmetric_batch_is_real():
    """b05 was folded into b02, and so was its batch.

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


@claim("b06", "the amber curve drops almost to zero before creeping back up")
def shift_batch_magnitude_dips():
    """Spoken over the first sweep, so it has to match the drawn curve."""
    h = np.array([-1.4, -0.7, -0.2, 0.3, 0.9, 1.5])
    t = np.linspace(0, 6.5, 700)
    mag = np.abs(ecf(h, t))
    lo = mag.min()
    assert lo < 0.01, lo                     # "almost to zero"
    assert mag[-1] > 10 * lo, (mag[-1], lo)  # "creeping back up"
    return f"min |phi| = {lo:.3f} at t = {t[mag.argmin()]:.2f}; ends at {mag[-1]:.3f}"


@claim("b06a", "indistinguishable from total collapse")
def aliased_batch_looks_collapsed():
    h = data.aliased_1d(3.0, k=3)
    m = abs(ecf(h, [3.0])[0])
    assert abs(m - 1.0) < 1e-12
    assert h.std() > 4.0          # genuinely spread out
    return f"|phi(3.0)| = {m:.4f} on a batch with sd {h.std():.2f}"


@claim("b06a", "spread across nearly thirteen units")
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


@claim("b06a", "nudging t collapses the average to almost nothing")
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
@claim("b08", "at a frequency of nought point three the two differ by two thousandths")
def low_t_is_blind():
    g, b = data.gaussian_1d(40), data.bimodal_1d(40)
    lo = abs(ecf(g, [0.3])[0] - ecf(b, [0.3])[0])
    hi = abs(ecf(g, [3.0])[0] - ecf(b, [3.0])[0])
    assert abs(lo - 0.0021) < 5e-4, lo
    assert abs(hi - 0.8989) < 5e-4, hi
    # the batches must actually agree on mean and variance, or the point is moot
    assert abs(g.mean() - b.mean()) < 5e-3 and abs(g.std() - b.std()) < 5e-3
    return f"gap at t=0.3 is {lo:.4f}; at t=3.0 is {hi:.4f}"


@claim("b08", "the expected squared length settles at one over N")
def noise_floor_is_one_over_n():
    rng = np.random.default_rng(0)
    vals = [abs(ecf(rng.standard_normal(40), [6.0])[0]) ** 2 for _ in range(4000)]
    got = float(np.mean(vals))
    assert abs(got - 0.025) < 0.003, got
    assert gaussian_cf(6.0) ** 2 < 1e-15
    return f"E|phi_40(6)|^2 = {got:.4f} vs 1/N = 0.0250; truth = {gaussian_cf(6.0)**2:.1e}"


@claim("b08", "that band holds over ninety nine per cent of what is worth measuring")
def window_holds_the_mass():
    """The fraction is BATCH-DEPENDENT, so the claim must be a bound.

    PLAN.md rev 4 recorded a single figure, 99.78%, as though it were a
    constant. Measured across batches it runs 99.63% to 99.98%, so any one
    figure is spurious precision and b08 originally spoke one. The honest,
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


# ----------------------------------------------------------------- histograms
@claim("b10", "same forty numbers, different answer")
def bins_are_arbitrary():
    g = data.gaussian_1d(40)
    a, _ = np.histogram(g, bins=np.arange(-3, 3.01, 0.5))
    b, _ = np.histogram(g, bins=np.arange(-3, 3.01, 0.5) + 0.15)
    assert a.tolist() == [0, 1, 1, 4, 5, 10, 7, 7, 2, 1, 2, 0], a.tolist()
    assert b.tolist() == [1, 0, 2, 6, 5, 10, 6, 5, 2, 3, 0, 0], b.tolist()
    return f"offset 0.00 -> {a.tolist()};  offset 0.15 -> {b.tolist()}"


@claim("b10", "at a width of one and a half the counts read two, fourteen, twenty four, zero")
def bins_delete_structure():
    c, _ = np.histogram(data.bimodal_1d(40), bins=np.arange(-3, 3.0001, 1.5))
    assert c.tolist() == [2, 14, 24, 0], c.tolist()
    return f"bimodal at width 1.5 -> {c.tolist()} (two clumps gone)"


@claim("b10", "it sits at seven, and then it is six")
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
@claim("b11", "the fingerprint of a standard Gaussian is e to the minus t squared over two")
def gaussian_cf_solves_ode():
    t = np.linspace(0, 6, 2001)
    phi = gaussian_cf(t)
    dphi = np.gradient(phi, t)
    interior = slice(1, -1)
    assert np.abs(dphi[interior] + t[interior] * phi[interior]).max() < 1e-5
    assert abs(phi[0] - 1.0) < 1e-15
    return f"max|phi' + t phi| = {np.abs(dphi[interior] + t[interior] * phi[interior]).max():.1e}; phi(0) = {phi[0]:.1f}"


@claim("b07", "phi of zero is one")
def phi_at_zero_is_one():
    for h in (data.gaussian_1d(40), data.bimodal_1d(40), np.full(24, 1.3)):
        assert abs(ecf(h, [0.0])[0] - 1.0) < 1e-15
    return "phi(0) = 1 for all three batches, to machine precision"


@claim("b07", "the hump decays and stays down, while the clumps swing the "
              "average all the way over to the negative side")
def toy_batches_have_different_curves():
    """Part 1's closing claim: the opening experiment, answered.

    b00 shows two batches agreeing on count, mean and variance. b07 draws both
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
@claim("b12", "a factor of fifty six")
def score_separates_batches():
    t = np.linspace(0.2, 4.0, 4001)
    tgt = gaussian_cf(t)
    g = np.trapezoid(np.abs(ecf(data.gaussian_1d(40), t) - tgt) ** 2, t)
    b = np.trapezoid(np.abs(ecf(data.bimodal_1d(40), t) - tgt) ** 2, t)
    assert abs(g - 0.0184) < 5e-4 and abs(b - 1.0369) < 5e-3, (g, b)
    assert 55 < b / g < 58
    return f"unweighted: gaussian {g:.4f}, bimodal {b:.4f}, ratio {b / g:.1f}x"


@claim("b12", "putting the weight in barely moves it")
def weighting_preserves_the_verdict():
    """Source fidelity: the displayed formula carries w(t) and an N prefactor.

    The animation shows the UNWEIGHTED area, so b12 must be able to say the
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
@claim("c06", "both marginals are exactly standard normal, and the cloud is a line")
def diagonal_is_rank_one():
    z = data.diagonal_2d(200)
    eig = np.linalg.eigvalsh(np.cov(z.T))
    u = np.array([1.0, -1.0]) / np.sqrt(2)
    proj = z @ u
    assert eig[0] < 1e-12, eig
    assert np.abs(proj).max() < 1e-12
    return f"covariance eigenvalues ({eig[1]:.2f}, {eig[0]:.1e}); " \
           f"projection on (1,-1)/sqrt2 max |{np.abs(proj).max():.1e}|"


@claim("c03", "the arrows average to a pull toward the origin")
def random_target_pulls_to_origin():
    rng = np.random.default_rng(3)
    D, z = 10, rng.standard_normal(10) * 1.5
    targets = rng.standard_normal((200_000, D))
    lhs = float(np.mean(np.sum((z - targets) ** 2, axis=1)))
    rhs = float(z @ z + D)
    assert abs(lhs - rhs) / rhs < 0.01, (lhs, rhs)
    return f"E||z - z*||^2 = {lhs:.3f} vs ||z||^2 + D = {rhs:.3f}"


# ---------------------------------------------------------------------- main
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
