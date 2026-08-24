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


def _latent_basis(seed: int = 1) -> np.ndarray:
    """A fixed 9x2 orthonormal subspace every latent-plane visual projects into."""
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(9, 2))
    basis, _ = np.linalg.qr(raw)
    return basis


LATENT_BASIS: np.ndarray = _latent_basis()
LATENT_SCALE = 0.62


def latent(u: np.ndarray) -> np.ndarray:
    """Project a 9-vector (or an (N, 9) batch) into the shared 2-D plane."""
    return np.asarray(u, dtype=float) @ LATENT_BASIS


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

# The fixed projection direction beats 4-6 sweep along.  Chosen together with
# LATENT_BASIS's seed so that the collapsed row's projected coordinate,
# |latent(COLLAPSED_TOKEN) . TIME_DIR|, lands in [0.9, 1.6]: below ~0.6 the
# collapsed row's score sinks toward its floor (~2.45 for six coincident
# points) and stops reading as clearly different from a healthy row's score
# (~0.1-0.8 for six genuine draws through this basis).
def _time_dir(seed: int = 1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    d = rng.normal(size=2)
    return d / np.linalg.norm(d)


TIME_DIR: np.ndarray = _time_dir()
