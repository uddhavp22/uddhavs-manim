# Source map — SIGReg

**Deliverable 1** of `EXPLAINER_PROCESS.md`. Written retroactively (2026-08-06),
after Chapter B was already built, as part of the option-2 retrofit.

## Sources

| | |
|---|---|
| Primary | <https://rezabyt.github.io/blogposts/sigreg-tutorial.html> — "SIGReg tutorial" |
| Underlying paper | LeJEPA, arXiv:2511.08544 |
| Fetched and re-read | 2026-08-12, including §§4–5 on quadrature and projections |

**Honesty note on this document.** Chapter B was built from prose pasted into a
session, and PLAN.md — a *derived* artifact — was treated as the source of truth
for several days. The blog was re-fetched on 2026-08-06 specifically to run the
source-fidelity diagnostic, and that fetch found two defects in already-rendered
scenes (§6 below). Everything here is checked against the fetched text, not
against PLAN.md.

---

## 1. What problem is being solved?

Joint-embedding predictive architectures collapse. The source states the failure
exactly:

> "The trivial solution `enc_θ(o) = c` (a constant function that maps every
> observation to the same point) gives `z_t = z_{t+1} = c`, and any predictor
> that outputs `c` achieves `L_pred = 0` exactly."

A perfect prediction loss is therefore compatible with a representation that
carries no information. The fix must be a regularizer `R(Z)` that forbids the
degenerate encoder by forcing the embedding distribution to a non-collapsed
target.

## 2. What is the central idea?

Pick the isotropic Gaussian `N(0, I_D)` as that target, then *test for it* using
only samples, differentiably. Three moves compose:

1. **Characteristic functions** turn "is this batch Gaussian" into "does this
   curve match `e^{−t²/2}`". `φ_X(t) = E[e^{itX}]`.
2. **Cramér–Wold** reduces a `D`-dimensional question to infinitely many
   one-dimensional ones: `Z ~ N(0, I_D)` iff `uᵀZ ~ N(0,1)` for every unit `u`.
3. **Sketching** makes that finite: sample `M` random directions, `K` frequency
   knots.

## 3. Why is it difficult?

- Gaussianity is a property of a **collection**, not of any individual point, so
  the naive "match each embedding to a Gaussian sample" is not merely worse —
  it has the wrong fixed point and pulls everything to the origin.
- A test computed from samples must stay **differentiable**, which rules out the
  obvious estimators (histograms, rank statistics, KS distance).
- The multivariate problem is genuinely infinite: "every direction" cannot be
  checked, only sampled.

## 4. What background is necessary?

Complex numbers as points in a plane; expectation as an average; unit vectors
and projection; covariance and eigenvalues; that gradient descent needs
derivatives. Fourier analysis is **not** needed and introducing it early is the
main way this topic gets explained badly.

## 5. Which part makes the strongest visual explanation?

The characteristic function as an **average of unit arrows**. Every sample
becomes an angle `t·x`, hence an arrow; the CF is where those arrows average to.
Agreement gives a long average, spread cancels. This is not an analogy — it is
literally the computation, so the picture carries the reasoning rather than
decorating it. It is the basis of the three-panel rig and of Chapter B.

Second strongest: **shadows**. A cloud, a direction, and the 1-D distribution
you get by projecting — with `Z = [X, X]` as the counterexample that makes
Cramér–Wold necessary rather than decorative.

## 6. Which claims require particular care?

Verbatim from the source, with how the video handles each:

### 6a. The statistic carries an `N` prefactor

$$\mathcal{T} = N\int_{-\infty}^{\infty} w(t)\,|\varphi_N(t) - \varphi_0(t)|^2\,dt$$

**Defect found 2026-08-06:** `b11` displayed this formula without the `N`, and
called it "the Epps–Pulley statistic". As a *loss* the prefactor is a constant
and does not move the argmin, but the named statistic has it. **Fixed.**

### 6b. The weight is a smooth Gaussian, not the integration window

$$w(t) = e^{-t^2/(2\lambda^2)}, \qquad \lambda > 0 \text{ a bandwidth parameter}$$

The range `[0.2, 4]` is the **truncation** used when `λ = 1`; it is not itself
the weighting. `b09` conflated the two and asserted the weighting is "not a
tuning knob". The source explicitly calls `λ` a *bandwidth parameter*, so it
plainly is one. **Fixed** — what is forced by finite samples is the *existence*
of high-frequency suppression, not the particular `λ`.

### 6c. The animated quantity was not the displayed formula

`b11` animated and spoke `∫|φ̂ − φ₀|² dt` (unweighted, no `N`) while showing a
formula containing `w_λ(t)`. Visual-symbolic correspondence broken: a symbol on
screen had no visual counterpart. **Fixed** by building the formula in two
steps. Measured, so the viewer can be told the refinement does not change the
story:

| | unweighted `∫|gap|²` | `∫w|gap|²` | `𝒯 = N∫w|gap|²` |
|---|---|---|---|
| Gaussian batch, N=40 | 0.0184 | 0.0008 | 0.031 |
| bimodal batch, N=40 | 1.0369 | 0.0448 | 1.790 |
| **ratio** | **56.4×** | **57.3×** | **57.3×** |

### 6d. The Gaussian CF derivation differs from the source *by choice*

The source completes the square and shifts a contour, justified by Cauchy's
theorem:

> `itx − x²/2 = −½(x − it)² − t²/2`

The video uses the ODE route instead (`p′ = −xp ⇒ φ′ = −tφ`). Same answer, no
complex analysis. This is a **declared pedagogical divergence**, recorded here
so it is never mistaken for what the source does.

### 6e. What is derived about projections, and what is cited

Two claims live here, and keeping them apart is the whole point of this
entry. Until 2026-08-22, `c06` ended on a card reading "Cramér–Wold — cited
theorem, not proved here", covering both at once. The owner's review called
that a dodge: most of what the card hid is elementary substitution plus a
covering argument, and the video had every ingredient for both already —
characteristic functions and their uniqueness from Chapter B, projections
from `c03`–`c05`. The card is gone. `c06` now derives the argument live, on
the same wheel the rest of the chapter built, re-read as frequency space.

**(1) The projection identity, and the covering argument it enables —
derived, and shown on screen in `c06`.**
For a unit vector `u` and `Y = u^\top Z`,

$$\varphi_Y(t) = \mathbb E\!\left[e^{itY}\right] = \mathbb E\!\left[e^{i(tu)^\top Z}\right] = \varphi_Z(tu).$$

This is regrouping a scalar inside an exponent — not a theorem, nothing
cited. `c06` performs the substitution on screen, then reads it
geometrically: as `t \ge 0` runs and `u` runs over the unit sphere,
`\xi = tu` runs over all of `\mathbb R^D` (`t = \|\xi\|`, `u = \xi/\|\xi\|`),
so the family of one-dimensional projection characteristic functions *is*
`\varphi_Z`, written in polar coordinates. Given (2) below, this is the
complete argument for Cramér–Wold's "if" direction — same projections force
the same joint characteristic function, hence (by uniqueness) the same law.
Not a special case of that direction, not an approximation to it: `c06` may
say "so" about this step, and may name Cramér–Wold as what it has just
shown, not merely gestured at. (The converse "only if" direction — same law
implies same projections — is definitional and was never in question.)

**(2) Fourier uniqueness — still cited, still not proved.**
"Two probability distributions are equal if and only if their characteristic
functions are equal." Not proved in the source; stated as a theorem in
`b08`, which says out loud that the proof is skipped. `c06` *invokes* it as
the closing step and marks it visibly as a recall from Chapter B, on screen
and in narration ("we already know..."), rather than presenting it as
something this scene has newly established. Proof status:
`theorem_statement`. The old prohibition still applies to this step alone:
never "we have shown", never "proves" — it is inherited, not re-derived.
Everything in (1) is downstream of granting (2); take (2) away and `c06`'s
argument shows only that the projections determine `\varphi_Z`, not that
`\varphi_Z` determines the distribution.

**The citation boundary did not move, it was redrawn around the right
fact.** (2) is cited exactly as it always was. What changed is that the
boundary used to sit around the whole theorem, which made an elementary step
look unavailable; it now sits only around the one fact that is genuinely
external.

**Two things the animation must not imply.**
- The frequency-plane field is amber and real-valued: that is
  `e^{-\|\xi\|^2/2}`, the value *this cloud's* premise forces (every
  projection standard Gaussian), not a generic `\varphi_Z(\xi)`, which is
  complex in general. The picture is this cloud's target field, never "what
  a characteristic function looks like" in general — same family as the
  `three_panel_rig` risk in `concepts.yaml`: `\operatorname{Re}\varphi` alone
  does not determine a distribution.
- Painting the plane shows that the family of projections *determines*
  `\varphi_Z`. It says nothing, on its own, about `\varphi_Z` determining the
  law — that step is entirely (2), and (2) alone.

### 6f. The `1/N` noise floor is a source-stated limitation

> "With finite `N`, even perfectly-Gaussian samples yield `SIGReg(Z) > 0` at
> order `1/N` from empirical CF noise floor."

`b09` verifies this empirically (0.0251 measured against `1/N` = 0.0250 at
`N = 40`, `t = 6`, over 4000 draws). The empirical verification is **ours**; the
claim is the source's. Both statuses recorded separately in `concepts.yaml`.

### 6g. Anti-collapse is an equivalence chain, and its guarantee is global only

$$\text{SIGReg}(Z) = 0 \iff u^\top Z \sim \mathcal{N}(0,1)\ \forall u \iff Z \sim \mathcal{N}(0, I_D)$$

The source is explicit that this covers the **global minimum only**:

> "Cramér-Wold guarantees only the global minimum, not local minima or
> convergence rates for gradient descent."

Chapter C.9 must not let the animation imply gradient descent is guaranteed to
get there. This is the single highest-risk false inference in the project.

## 7. What should be omitted?

- The PyTorch implementation. Already cut.
- Trapezoidal quadrature weights `α_k` beyond the fact that a computer must
  discretize. Engineering, not insight.
- The contour-integration derivation (replaced, see 6d).
- `λ` tuning. One sentence that it sets the bandwidth; no sweep.
- Estimator variance `1/√M` — state it in Chapter C.10 as a limitation, do not
  derive it.

## 8. Source facts to carry verbatim

| Fact | Value | Where |
|---|---|---|
| CF of `N(0,1)` | `e^{−t²/2}` | B.11 |
| empirical CF | `φ_N(t) = (1/N)Σ e^{itz_n}` | B.2–4 |
| real/imag split | `C(t) = (1/N)Σcos(t z_n)`, `S(t) = (1/N)Σsin(t z_n)` | B.5 |
| weight | `w(t) = e^{−t²/(2λ²)}` | B.12, C.4 |
| range at `λ=1` | `[0.2, 4]` | B.8, C.5 |
| quadrature | `K=16` → 0.01% error vs `K=2000`; `K=8` → 0.04%; `O(1/K²)` | C.5 |
| direction sampling | `u ~ N(0, I_D)`, then `u ← u/‖u‖` | C.7 |
| typical `M` | 32 to 1024, variance `~1/√M` | C.7, C.10 |
| SIGReg | `(1/M) Σ_m 𝒯(u^(m)ᵀ Z; λ)` | C.9 |
