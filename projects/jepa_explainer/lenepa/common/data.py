"""Continuity constants shared between LeNEPA scenes 2 and 3.

Scene classes are separate ``Scene`` subclasses with no direct object
sharing, so cross-scene continuity -- the same token row, the same landing
y-positions, the same displayed values -- is enforced by importing from a
shared module rather than by hand-copying literals into each scene file.
This is the repository's prescribed pattern for a continuity seam
(``docs/VISUAL_SYSTEM.md`` section 7).
"""

from __future__ import annotations

import numpy as np

# Scene 2's vector heights and its post-chamber landing rows (beat 8's
# ``TGT_ROW_Y``/``PRD_ROW_Y``).  Scene 3 opens exactly where scene 2 left
# off, at these same heights and the same two y-positions.
TOKEN_H = 1.48
PRED_H = 1.24
TGT_ROW_Y = 1.30
PRD_ROW_Y = -1.18


def _token_values() -> tuple[np.ndarray, ...]:
    """Scene 1's exit state: six 9-dimensional token vectors, ``z_1..z_6``.

    ``z_3`` (index 2) is scene 1's hand-set encoder output
    (``scenes.py``'s ``output_values``), not a random draw -- it is the one
    token whose numbers the viewer watched arrive from real propagation.
    """
    rng = np.random.default_rng(21)
    values = [rng.normal(size=9) for _ in range(6)]
    values[2] = np.array([
        0.72, -0.34, 0.18, 0.91, -0.57, 0.43, -0.11, 0.61, -0.26,
    ])
    return tuple(values)


TOKEN_VALUES: tuple[np.ndarray, ...] = _token_values()


def _mixed_values() -> tuple[np.ndarray, ...]:
    """The four carriers' post-mixing values (scene 2's beat 5, ``z_1..z_4``).

    These are arbitrary by design -- scene 2 mixes token vectors through
    invented attention weights, not a real trained model -- so the exact
    numbers do not matter beyond staying legible and in-band.  What matters
    is reproducing scene 2's original ``value_rng = np.random.default_rng(97)``
    draw order exactly, so this extraction leaves scene 2's already-approved
    render bit-identical.

    Two phases against the *same* rng stream, in this order:

    1. All 16 "shown" draws first, four per carrier, carrier by carrier --
       exactly the original loop's order (``for carrier: for entry in
       decimal_entries(carrier)``), with nothing interleaved.  These land at
       positions 0, 1, -2, -1 of each 9-vector, the four coordinates
       ``numeric_embedding``'s abbreviated display actually shows.
    2. Five more draws per carrier, *after* all 16 shown draws, to fill out
       a real 9-vector for scene 3's projector input, which scene 2 never
       displays and therefore never constrained.  Interleaving these with
       phase 1 (drawing a carrier's filler before the next carrier's shown
       values) would shift every later carrier's shown draws off the
       original sequence -- that was the bug caught by diffing scene 2's
       before/after render.

    Every entry lies in the open interval ``(-0.95, 0.95)``: scene 2 animates
    the four displayed entries into place via ``ChangeDecimalToValue``, and
    ``numeric_embedding``'s docstring records the glyph-desync failure that
    crossing a digit/sign boundary mid-animation causes.
    """
    rng = np.random.default_rng(97)
    shown_positions = (0, 1, 7, 8)
    fill_positions = (2, 3, 4, 5, 6)

    shown = [
        [float(np.clip(rng.normal(scale=0.45), -0.95, 0.95)) for _ in range(4)]
        for _ in range(4)
    ]

    values = []
    for carrier_shown in shown:
        vec = np.zeros(9)
        for pos, value in zip(shown_positions, carrier_shown):
            vec[pos] = value
        for pos in fill_positions:
            vec[pos] = float(np.clip(rng.normal(scale=0.45), -0.95, 0.95))
        values.append(vec)
    return tuple(values)


MIXED_VALUES: tuple[np.ndarray, ...] = _mixed_values()


# ---------------------------------------------------------------------------
# Scene 4 (temporal SIGReg): a (B, T) batch of layer-0 tokens, a shared 2-D
# latent plane those tokens project into, and a layer-8 row reusing scene 2's
# post-mixing carriers.  T=6 is forced by continuity, not a free choice: scene
# 1 cuts six patches and scene 2 shows z_1..z_6, so a batch row here has to
# hold six positions to keep reading as "the same kind of sequence."
# ---------------------------------------------------------------------------

BATCH_B = 3
BATCH_T = 6


def _batch_tokens() -> tuple[tuple[np.ndarray, ...], ...]:
    """u^(0)_{b,t}: three sequences of six layer-0 tokens.

    Row b=1 IS ``TOKEN_VALUES`` unmodified -- the exact sequence the viewer
    already watched arrive in scenes 1-3.  Rows b=2, b=3 are statistical
    siblings drawn the same way (``rng.normal(size=9)``, see
    ``_token_values`` above) from a separate seed, so they read as more of
    the same kind of object rather than a new kind of data.
    """
    rng = np.random.default_rng(58)
    row_b2 = tuple(rng.normal(size=9) for _ in range(BATCH_T))
    row_b3 = tuple(rng.normal(size=9) for _ in range(BATCH_T))
    return (TOKEN_VALUES, row_b2, row_b3)


BATCH_TOKENS: tuple[tuple[np.ndarray, ...], ...] = _batch_tokens()

# The vector every b=1 token collapses onto in beat 2 -- scene 1's hand-
# computed encoder output for token 3, reused rather than inventing a new
# vector for the collapse to land on.
COLLAPSED_TOKEN: np.ndarray = TOKEN_VALUES[2]


def _latent_basis(seed: int = 2818) -> np.ndarray:
    """A fixed 9x2 orthonormal subspace every latent-plane visual projects into.

    Five constraints pick the seed, and all five are about legibility rather
    than about the mathematics -- every orthonormal 9->2 slice is an equally
    valid view of the same tokens, so choosing among them costs nothing:

    1. the pooled batch's bounding box comes out near 16:9, so the cloud fills
       a wide frame instead of sitting square in the middle of one;
    2. the twelve healthy points cover every cell of a 4x2 partition of that
       box, so the cloud has no conspicuously empty quadrant;
    3. the closest pair of healthy points is far enough apart to read as two
       points rather than as a smudge -- this seed's minimum pair separation
       is roughly double the next candidate's;
    4. the collapsed row's point is at least a third of the plane's height
       away from every other point, so its knot reads as its own object;
    5. the collapsed row's coordinate along the sweep direction is well inside
       the pooled range and well separated from every other shadow, so the
       spike it makes is not confused with a neighbour's.

    A rotation into the pooled cloud's principal axes is folded in, and the
    result is recentred on its bounding box.  Both are orthogonal/rigid moves
    that leave every distance and every projection intact; they only decide
    which way up the slice is drawn and where its middle is.  Rescaling the
    axes *independently* would not be harmless -- it would break the identity
    between a projection of the cloud and the cloud of projections, which is
    the whole content of the shadow beat -- so the scene applies one isotropic
    world scale and no more.
    """
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(9, 2))
    basis, _ = np.linalg.qr(raw)

    pooled = np.array(
        [COLLAPSED_TOKEN @ basis]
        + [u @ basis for row in BATCH_TOKENS[1:] for u in row]
    )
    _, _, principal = np.linalg.svd(pooled - pooled.mean(axis=0))
    rotated = (pooled - pooled.mean(axis=0)) @ principal.T
    centre = 0.5 * (rotated.min(axis=0) + rotated.max(axis=0))
    return basis @ principal.T, pooled.mean(axis=0) @ principal.T + centre


LATENT_BASIS, _LATENT_ORIGIN = _latent_basis()

# The one direction the shadow beat projects along: the plane's own wide axis,
# which ``_latent_basis`` has already rotated onto x.  Nothing is cherry-picked
# by choosing it -- a collapsed sequence spikes under *every* direction, since
# its points are identical -- and it is the direction under which a healthy
# batch's spread is most visible, which is exactly the claim the beat makes.
SWEEP_DIR: np.ndarray = np.array([1.0, 0.0])


def latent(u: np.ndarray) -> np.ndarray:
    """Project a 9-vector (or an (N, 9) batch) into the shared 2-D plane."""
    return np.asarray(u, dtype=float) @ LATENT_BASIS - _LATENT_ORIGIN


def _layer8_row() -> tuple[np.ndarray, ...]:
    """u^(8)_{1,t}: sample b=1's row at transformer layer 8.

    The first four positions ARE ``MIXED_VALUES`` unmodified (scene 2's
    post-mixing carriers).  The last two draw from a separate
    ``default_rng(112)`` stream -- deliberately not an extension of the
    seed-97 stream ``_mixed_values`` uses, since interleaving a second
    consumer into that stream is exactly the ordering bug its own docstring
    records.
    """
    rng = np.random.default_rng(112)
    extra = tuple(rng.normal(scale=0.45, size=9) for _ in range(2))
    return tuple(MIXED_VALUES) + extra


LAYER8_ROW: tuple[np.ndarray, ...] = _layer8_row()


def _layer8_rows() -> tuple[tuple[np.ndarray, ...], ...]:
    """u^(8)_{b,t} for all three samples.

    Sample b=1 IS ``LAYER8_ROW`` -- scene 2's post-mixing carriers, unchanged.
    Samples b=2 and b=3 are statistical siblings from their own seed.

    Scene 4's depth beat needs a *healthy* row to carry through the layer
    stack: b=1 is the sequence the scene has just supposed into collapse, and
    watching a collapsed row's cells evolve with depth would contradict the
    supposition it is still standing under.  b=2 is used instead, which is
    why a per-sample layer-8 row has to exist at all.
    """
    rng = np.random.default_rng(305)
    others = tuple(
        tuple(rng.normal(scale=0.62, size=9) for _ in range(BATCH_T))
        for _ in range(BATCH_B - 1)
    )
    return (LAYER8_ROW,) + others


LAYER8_ROWS: tuple[tuple[np.ndarray, ...], ...] = _layer8_rows()

# The transformer depth scene 4's beat 6 walks: layer 0 (patch embeddings)
# through layer 8, inclusive, so nine plates and nine states.
DEPTH_LAYERS = 9


def depth_values(b: int, t: int, ell: float) -> np.ndarray:
    """Sample ``b``'s token ``t`` at (possibly fractional) depth ``ell``.

    One scalar drives the whole row: every cell pattern in the depth beat is a
    function of ``ell`` alone, so the same ``ValueTracker`` that moves the row
    down the stack also evolves what the row contains.  Linear between the
    layer-0 and layer-8 endpoints, which is not a claim about how transformers
    actually transport representations -- it is the minimum that makes "the
    representation changes with depth" legible without inventing structure.
    """
    frac = float(ell) / (DEPTH_LAYERS - 1)
    u0 = np.asarray(BATCH_TOKENS[b][t], dtype=float)
    u8 = np.asarray(LAYER8_ROWS[b][t], dtype=float)
    return (1.0 - frac) * u0 + frac * u8

# ``TIME_DIR`` lived here.  It was chosen to put a *numeric* Epps-Pulley score
# in a readable band, and the scene no longer prints a score: a bare number on
# a scale the viewer was never taught is not evidence.  The direction the
# shadow beat uses is ``SWEEP_DIR``, chosen for legibility of the picture
# instead.
