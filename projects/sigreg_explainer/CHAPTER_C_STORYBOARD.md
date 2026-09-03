# Chapter C — storyboard

**Status (2026-09-03).** C01–C05 are implemented and have final-quality
1080p60 Archer renders; C05's is awaiting owner approval. C06 has a
2026-08-21 review render (154 s) and an in-progress "one continuous proof"
revision in the working tree, designed in `C06_REVISION_DESIGN.md`, which
replaces the two-field morph with a single radial-slice comparison. C07–C10
are planned below and not started.

The narration authority for implemented scenes is `SCRIPT_chapterC.md`,
generated from the scene source by `tools/script_dump.py` after every
voiceover edit. Per-scene render findings and the revision history live in
`RENDER_REVIEW.md`. This file holds the plan: the arc, the scene contracts,
the transition contracts and the claim ledger.

Governed by `PLAN.md`, `SOURCE_MAP.md`, `docs/NARRATION_SPEC.md`,
`docs/VISUAL_SYSTEM.md`, `docs/RENDER_REVIEW_SPEC.md`, `docs/SCENE_CRAFT.md`.

---

## 0. The causal arc, in one pass

Chapter B ended holding a machine that eats a line of numbers and returns one
number saying how far that line is from a standard Gaussian. Chapter C's whole
job is to feed a cloud of vectors into that machine without building a second
machine.

> A model gives one vector per sample, so before scoring anything we have to say what shape we want the collection to have. Assigning each vector its own Gaussian partner looks like a way to force that shape, and it isn't one — the partner is arbitrary, and averaging over partners pulls everything to the origin. Gaussianity belongs to the collection.
>
> A collection can be turned into numbers by picking a direction and reading how far along it each vector sits. Those numbers are an ordinary batch, so Chapter B's score applies unchanged. One direction, one number.
>
> One direction is not enough: rotate it and the same cloud produces both an alarming shadow and an innocent one. Nor are the coordinate directions enough, and `Z = (X, X)` is the proof — both coordinates are exactly standard Gaussian while every sample lies on a line.
>
> So the test has to be every direction. For the cloud we want, every direction gives the same standard Gaussian, so one target serves all of them; and Cramér–Wold, cited, supplies the converse.
>
> "Every direction" is a sphere, and "every frequency" is an integral. A computer replaces the first with `M` sampled directions and the second with `K` frequency knots. Assembling those two approximations around the score we already have gives SIGReg.
>
> The finished loss scores collapsed and low-rank clouds high and the round one low. At the population level, zero means exactly `N(0, I_D)`. With finite `N`, `M`, `K` it is an estimator, and the guarantee describes the global minimum only.

Three load-bearing choices, all approved 2026-08-11:

1. **Isotropic-target constancy is a beat, not a footnote** (C06). It is why one
   amber target curve serves every direction, and without it the averaging in
   C07 is unmotivated.
2. **The two directions of the Cramér–Wold biconditional are kept separate.**
   `Z ~ N(0,I_D) ⟹ u^T Z ~ N(0,1) ∀u` is demonstrated; the converse is the
   cited theorem. One on-screen "⟺" without saying which half was shown is the
   proof-strength failure `SOURCE_MAP.md` §6e forbids.
3. **C04 and C05 are two different failures.** C04: an arbitrary direction can
   be innocent. C05: the *privileged* directions can be innocent. The
   escalation is what makes "every direction" feel forced rather than asserted.

---

## 1. What Chapter B hands over

`chapterB/b11_fingerprint_to_loss.py` ends on `common.bridge.vector_bridge()`:
three vector columns in `CLOUD`, an amber `?` arrow, `𝒯 ∈ ℝ`, and the spoken
line *"In the next chapter, we'll discuss how to do the same thing with a
whole batch of vectors."* C01 opens by compressing Chapter B to the
Epps–Pulley equation it earned, then reconnects it to encoder outputs.

The viewer arrives knowing: samples become unit directions via
`x ↦ e^{itx}`; their average is the empirical characteristic function; one
frequency can be fooled while the whole function is unique; the standard
Gaussian's characteristic function is `e^{−t²/2}`; squared gaps accumulate
into the Epps–Pulley statistic; a finite Gaussian batch scores small but
positive. Chapter C reuses all of it and re-teaches none of it.

Shared apparatus, all in `common/`:

| Module | Chapter C use |
|---|---|
| `rig.ThreePanelRig` | C03 mounts it literally on the projected dots (`mount(dots=...)`) |
| `wrap.ecf`, `wrap.gaussian_cf` | every scalar characteristic function |
| `score.epps_pulley`, `score.sigreg`, `EP_GRID`, `EP_LAMBDA` | every displayed score, and `facts.py` |
| `cloud.CloudRig` | the 3-D dot cloud: build-once dots registered fixed-orientation, one updater, ellipsoid rescaled from pristine points |
| `project.CloudProjectionRig`, `project.TurningProjection` | one direction state → arrow, line, guides, scalar shadow, stacked dot plot, score, score-vs-angle table |
| `fingerprint.CharacteristicFunctionPlot` | C08's knot beat |
| `bridge.vector_bridge` | the B11 → C01 seam, built from one definition |
| `data.gaussian_3d`, `clumped_3d`, `diagonal_2d`, `gaussian_2d`, `ring_2d`, `whiten` | seeded for exactly these scenes |
| `beat.ActScene` (`across`, `inspect`, `freeze`, `clear_beat`, `clear_overlay`, `settle_frame`) | all scenes |

---

## 2. Scenes and colour

| # | File | Beat | Runtime |
|---|---|---|---|
| 1 | `c01_vectors.py` | scalars become vectors | 0:46 final |
| 2 | `c02_the_shape_is_the_goal.py` | shape ladder + the wrong fix | 2:44 final |
| 3 | `c03_one_shadow.py` | the rig returns on one shadow | 1:50 final |
| 4 | `c04_one_shadow_is_not_enough.py` | turn `u`, the shadow lies | 0:47 final |
| 5 | `c05_gaussian_marginals.py` | `Z = (X, X)` | 0:52 review |
| 6 | `c06_every_direction.py` | every direction; Cramér–Wold | 2:34 review, revision in progress |
| 7 | `c07_sampling_directions.py` | `M` | planned ~1:50 |
| 8 | `c08_frequency_knots.py` | `K` | planned ~1:20 |
| 9 | `c09_sigreg.py` | assemble the formula | planned ~1:30 |
| 10 | `c10_what_it_claims.py` | anti-collapse, population limit, honest scope | planned ~2:00 |

Per-scene estimates have not tracked delivered runtimes (C04 came in at 0:47
against 1:30) and are not a forecast.

**Colour roles, fixed for the chapter.** No new hex values.

| Role | Palette |
|---|---|
| embedding cloud, samples, their fingerprint | `CLOUD` |
| direction `u`, its line, guides, shadow dots, `score(u)`, score-vs-angle curve | `DIRECTION` |
| the standard-Gaussian target and its curve | `TARGET` |
| the gap, failure shapes, a high score | `COLLAPSE` |
| the direction-averaged score, the SIGReg value | `AVERAGE` — the purple that meant "average of many arrows" in B now means "average of many directions" |
| a competing distribution's fingerprint (C06's ring) | `RIVAL` |
| `φ_Z` and its slices | `MAGNITUDE` |
| axes, wireframe, captions, region boundaries | `AXIS` / `GRID` / `MUTED` |

---

## 3. Scene contracts

Each: causal beat, persistent objects, claim flags. Narration is in
`SCRIPT_chapterC.md` for C01–C06 and drafted here for C07–C10 (drafts, not
yet audited).

Spoken aliases, decided once: "Cramer Wold" spoken, `Cramér–Wold` displayed;
"u transpose z", "z sub i"; "the score", never "T", which collides with
frequency `t`; "a neural network produces those numbers" rather than
"encoder", which ElevenLabs mispronounced.

### C01 — From a number line to an embedding cloud *(density: low)*

Inherited: Chapter B's mechanism scores a scalar batch.
Experiment: run it on a Gaussian batch (`0.063`) and a two-mode batch
(`3.581`), then reveal those scalars as the one-coordinate output of a
network. Seven large 5×7 digits propagate through a `35 → 8 → 6 → 8` network
(`_2017/nn/part1.py::NetworkMobject` grammar: literal pixel-to-input
correspondence, edges behind neurons, complete edge-group waves).
Observation: widening the output head `D = 1 → 2 → 3` (then `4, 6, 8`) turns
the batch from a line into a plane into a cloud.
Conclusion: the score must now act on a batch of vectors.
Handed on: the standard Gaussian in `D` dimensions is adopted as the target.

| | |
|---|---|
| Enters | the Epps–Pulley equation with two computed examples |
| Transforms | digits through the network; the fifteen output dots grow line → plane → cloud |
| Remains | the fifteen dot instances into the centred 3-D cloud, named `Z` only once it exists |
| Exits | input cards, network, dimensionality label |

Flags: `D = 3` is a display choice, said once. No mathematical claim.

### C02 — The shape is a property of the collection *(density: medium)*

Inherited: a standard-Gaussian target for the cloud.
Experiment 1: remove the spread along one axis, then another, then the last;
`rank(Z) = 3 → 2 → 1 → 0`. Rank zero is named as collapse once. Chapter A
owns the model-failure explanation; no network or prediction loss here.
Experiment 2: restore the target, motivate it (LeJEPA's cited downstream-risk
result, immediately qualified), unpack `N(0, I_D)` as zero mean and identity
covariance while a `DIRECTION` arrow sweeps 3-D orientations inside the amber
shell — if the direction turns and the target stays unchanged, no direction
is preferred. Then try to build a loss by assigning each embedding an
independently sampled Gaussian partner: one explicit pair, thirteen faint
pairs, resampling changes only the amber side, thirty candidates accumulate
on "infinitely many draws", 48 partners around one fixed embedding, arrows
contract to one origin-directed average.
Observation: `E‖z − z*‖² = ‖z‖² + D`, expanded on screen in a lower panel —
cross term vanishes because `E[z*] = 0`, `E‖z*‖² = D` from `D` unit-variance
coordinates — so the pointwise minimum pulls every embedding to zero.
Conclusion: assigned partners cannot impose a property of the collection; the
loss has to compare distributions.

| | |
|---|---|
| Enters | the C01 cloud, `ThreeDAxes`, a fixed-frame rank readout |
| Transforms | one shape tracker walks the ladder and back; target shell and sweeping direction; camera drops to a 2-D slice for the pairing beat; algebra panel with blue radius and amber halo; a field of red origin-directed arrows |
| Remains | the same 220 dot instances throughout |
| Exits | ellipsoid, pairing arrows, partner dots; the cloud stays for C03 |

Flags: `source_statement` for the isotropic-Gaussian-minimises-worst-case
result; `exact_derivation` (in `facts.py`) for the expected pull `2z`;
`QUALIFICATION` that the expectation is over a continuum independent of `N`,
that Monte Carlo would be possible, and that the closed form uses known
moments rather than a Gaussian-only trick. **Hard boundary:** nothing about
gradient descent on this objective or any trajectory.

### C03 — One projection gives a scalar batch *(density: low)*

Inherited: measure the collection.
Experiment: the type mismatch (`{x_i} ⊂ ℝ` needed, `{z_i} ⊂ ℝ^D` given) clears
into the `ℝ^D → ℝ` bridge. A `DIRECTION` arrow exactly one axis unit long
carries `‖u‖ = 1`; normalisation is motivated as preventing the choice of
direction from also rescaling the numbers. One embedding drops
perpendicularly to `u^T z_i = +1.93`; one on the other side to `−1.53`; then
44 representative guides and all 220 dots descend into the shadow.
Observation: the shadow dots flatten into screen space, land on
`layout.RIG_LINE_CENTRE`, and the rig mounts on those exact instances. `t`
sweeps `0 → 6.5`, the amber target appears on its clause, a red marker sweeps
the gap, the score `0.055` appears.
Conclusion: one direction gives one number. The rig fades in place while the
score crosses to `score(u_1) = 0.055`; the cloud returns; two purposeful
camera moves accompany `u_2` (`0.046`) and `u_3` (`0.872`) with every shadow
point moving.
Handed on: evidence about one shadow versus a conclusion about the cloud.

Flags: `OBSERVATION` only — a small score is not evidence the cloud is
Gaussian. Every displayed number comes from the array driving the dots.
`mount()` is called without `link=True`: the centroid-to-curve dashed link
drew as a stray diagonal across two panels.

### C04 — One shadow can be innocent *(density: medium)*

Inherited: one direction gives one number.
Experiment: `data.clumped_3d()` — bimodal along x, the isotropic cloud's own
y and z, every column at unit variance so the failure is shape, not scale.
One `ValueTracker` angle sweeps `0 → 180°` monotonically, driving arrow,
line, all 220 shadow feet stacked along the line's own normal
(`layout.stack_levels`), the live `score(u)` readout and the trace.
Observation: two piles with a hole at `17.095`; one hump at `0.046` a quarter
turn later; the hole reopens by `180°`. A standard normal drawn top-left in
`TARGET` on "a Gaussian has no hole in the middle", never named, fades in
the silence after beat 3.
Conclusion: the completed trace is the product. Both settled scores are
marked; the half of the half-turn scoring below `0.5` (`50°–140°`) is
bracketed by two dashed `MUTED` lines. "A low score tells you about the
direction you picked. It tells you nothing about the cloud behind it."

| | |
|---|---|
| Enters | C03's exact last frame |
| Transforms | C03's apparatus fades first; one camera move flattens onto the turning plane and slides the world left to clear the panels while the same dots morph into two clumps |
| Remains | cloud, arrow, meter, completed trace with marks and band |
| Exits | axis tips and z axis with the camera |

Flags: `CLAIM`, the weak one — one projection is insufficient; do not reach
for "all of them" yet. `facts.py` checks both scores, unit variance, the
band fraction and that the angle grid is uniform.

### C05 — Both coordinates Gaussian, every point on a line *(density: medium)*

Inherited: one direction was not enough; the coordinate axes are the two
natural directions to try next.
Experiment: `Z = (X, X)` is visible as a diagonal line from frame one.
Representative guides drop points onto the x-axis; the feet spread into a
dot plot under an amber `N(0,1)`; `score(x) = 0.244`. The same apparatus
rotates continuously onto y; `score(y) = 0.244`. It turns `45°` further
toward `y − x`; the dot plot contracts to one point at zero;
`score(u) = 81.785`.
Conclusion: the axes never compared the two coordinates. A mixed direction
exposes the dependence, so testing must extend beyond the axes.

The camera is locked flat (`phi=0, theta=−90°`) so `CloudRig` and
`TurningProjection` work unchanged on an honestly 2-D scene. Positions are
derived from screen layout through `_framed`, not copied from C04 (see
`docs/SCENE_CRAFT.md` §5, trap 9). `data.diagonal_2d` standardises `X` so the
score minima sit exactly on the axes and the ledger's "exactly standard
normal" is true of the 200 rendered points. The dot-plot stack is capped
(`stack_max_level`) because at the anti-diagonal every sample projects to
the same value.

Flags: `exact_derivation` — both marginals exactly `N(0,1)`, covariance
eigenvalues `(2, 0)`; `exact_computation` in `facts.py` for all three
scores; `CLAIM` — Gaussian marginals do not imply joint Gaussianity, proved
by construction, and shown **before** Cramér–Wold is named.

### C06 — Every direction gives a batch *(density: high)*

Inherited: C05 found one revealing mixed direction; C03/C04 already taught
projection, so nothing is recalled.
Spine of the current revision (`C06_REVISION_DESIGN.md` has the beat sheet):

```text
turn u → target: every projection is N(0,1)
       → ONE shadow's CF is a radial slice φ_Z(tu)          [derivation, on screen]
       → two clouds, same mean & covariance, different slices  [the stake: the ring]
       → deform until the slices agree                       [the attempt]
       → every u ⇒ every slice ⇒ the whole CF                [field built HERE, once]
       → Chapter B uniqueness ⇒ same distribution            [citation]
       → that implication is Cramér–Wold                     [the name]
       → specialise to Z ~ N(0, I_D)                         [the payoff]
```

Design decisions that bind the revision: the 1-D radial slice is the object
that is compared and deformed, because a brightness field cannot show sign
and the ring's characteristic function crosses zero where the Gaussian's
never does; the frequency field appears exactly once, after the slices agree,
as the accumulation of slices — so "sweeping `u` fills the plane" has
something to do; brightness only ever encodes a non-negative characteristic
function. `_standardized_isotropic_points` whitens, so the live `Var[u^T Z]`
readout reads `1.00` for every `u`. The scene ends on the Cramér–Wold payoff
and leaves eight direction lines and four plots for C07; the
continuum-of-directions training line is parked verbatim in the file
docstring for C07's opening.

Flags: `exact_derivation` in `facts.py` — `φ_{u^T Z}(t) = φ_Z(tu)` to machine
precision, and the swept projections match the Gaussian fingerprint;
`exact_derivation` — `u^T Z ~ N(0, u^T I u) = N(0,1)`; `theorem_statement` —
Fourier uniqueness, cited from Chapter B, stated in plain language, never
re-derived. `SOURCE_MAP.md` §6e holds the derived/cited split. Never
"therefore" across the cited half.

### C07 — `M` sampled directions *(planned · density: medium)*

Inherited: the test needs every direction.
Experiment: draw a direction the only unbiased way available — a Gaussian
vector divided by its length — and score its shadow. Then another. Then many.
Observation: individual scores scatter; their average steadies as more are
drawn.
Conclusion: replace the expectation over directions with an average over `M`
sampled ones. `M` is introduced here and nowhere earlier.
Handed on: each score is still an integral over every frequency.

> Every direction is a whole sphere of them, and a computer can't visit a sphere. <bookmark mark='draw'/>It can draw one: take a Gaussian vector and divide by its length, and you land somewhere on the sphere with no direction favoured.
>
> <bookmark mark='first'/>Each one gives a shadow and a score. <bookmark mark='second'/>Here's another, and it disagrees with the first, because the two directions see different things.
>
> <bookmark mark='many'/>Draw M of them and average. <bookmark mark='M'/>More directions steady that average. They don't turn a finite batch into a proof.

Choreography from `_2017/nn/part3.py::ConstructGradientFromAllTrainingExamples`
(show two → show all → average → collapse into one), paced as fixed pulses:

| Stage | Screen |
|---|---|
| 1 | one Gaussian vector appears inside the cloud, snaps outward to unit length on a faint sphere; ~1.2 s, settled |
| 2 | its shadow and score `𝒯₁` in `DIRECTION`; settled |
| 3 | a second direction, same rhythm, different score |
| 4 | ~30 more at ~0.15 s each in a `LaggedStart` fan, each dropping its score into a growing column |
| 5 | the column collapses into one `AVERAGE` number |
| 6 | `M` is written beside the column as the count of rows |

Active direction bright, earlier ones dimmed. Reuses `CloudProjectionRig`,
`common/score.py`; the fan and column are scene-local.

Flags: `SOURCE_MAP.md` §8 verbatim: `u ~ N(0, I_D)`, `u ← u/‖u‖`.
`QUALIFICATION`, required: more `M` reduces Monte Carlo variation, not
finite-batch uncertainty. Do **not** state `1/√M` here (deferred to C10).
Typical `M` is 32–1024; say once if at all.

### C08 — `K` frequency knots *(planned · density: medium)*

Inherited: `M` scores, each an integral.
Experiment: return to one scalar score — B11's weighted squared-gap area,
reconstructed identically — and evaluate the integrand at finitely many
frequencies.
Observation: at `K = 16` the finite sum already tracks a dense reference.
Conclusion: replace each integral with `K` knots. `K` is introduced here.
Handed on: both approximations are in place; assemble.

> One of those scores is still an integral over every frequency, and a computer can't visit those either. <bookmark mark='knots'/>Evaluate the integrand at K frequencies inside the window from Chapter B, and add up what you find.
>
> <bookmark mark='eight'/>Eight knots already follow the shape. <bookmark mark='sixteen'/>Sixteen tracks a far denser reference to within a hundredth of a percent, on this batch. The error falls like one over K squared, so there's not much left to gain.

| | |
|---|---|
| Enters | B11's gap picture — `gap_axes`, the `COLLAPSE` curve, the filled area, the amber `w_λ(t)` taper |
| Transforms | `K = 8` knots drop onto the `t` axis as `TARGET` ticks with sampled values; then `K = 16`; the finite sum ticks against the dense reference |
| Remains | `K` and the discretised score expression |
| Exits | the gap axes at the cut |

Do not reopen hard-bounds-versus-smooth-weights; the `[0.2, 4]` window and
`w_λ(t) = e^{−t²/(2λ²)}` are settled inputs. Trapezoidal weights stay
deferred. Reuses `CharacteristicFunctionPlot`, `layout.frequency_axes`,
`common/score.py`.

Flags: the `K = 16 → 0.01%`, `K = 8 → 0.04%`, `O(1/K²)` figures are source
facts whose batch, `λ` and window `SOURCE_MAP.md` §8 does not record.
**Before this scene renders:** `facts.py` recomputes the relative error on
the batch actually shown at `λ = 1` over `[0.2, 4]` and the narration says
"on this batch" (the draft assumes this); or the narration attributes the
figure to the source and the demo shows only qualitative agreement.

### C09 — Assembling SIGReg *(planned · density: low)*

Inherited: two motivated finite approximations.
Experiment: write down what has been happening; each symbol already has a
picture attached.
Conclusion: `SIGReg(Z) = (1/M) Σₘ 𝒯(u⁽ᵐ⁾ᵀ Z; λ)`.
Handed on: what does it do, and what does it promise?

> Every piece of this is already on screen. <bookmark mark='project'/>The projection u transpose z turns the batch into numbers. <bookmark mark='score'/>The score compares those numbers with the standard Gaussian, using K knots inside the weighted window. <bookmark mark='average'/>And the average over M directions is the whole regularizer.

| Step | Symbol | Arrives from |
|---|---|---|
| 1 | `u^{(m)T} z_i` | `TransformFromCopy` off the projection arrow and one shadow dot, still on screen from C07 |
| 2 | `𝒯( · ; λ)` wraps it | `TransformFromCopy` off the score meter |
| 3 | `(1/M) Σ_{m=1}^{M}` wraps that | the purple score column collapsing again |
| 4 | held | the source's one-line form |

Optionally `𝒯` expands once into its `K`-knot sum and collapses back. Symbols
isolated at construction for `TransformMatchingTex`. Nothing structural is
new; the C07 frame is held from the previous cut.

Flags: the formula must match `SOURCE_MAP.md` §8 character for character,
including `λ` — B11 once shipped `𝒯` without its `N` prefactor. No new claim
is made here; if a sentence asserts something, it is in the wrong scene.

### C10 — What the loss opposes, and what it promises *(planned · density: high · highest-risk scene)*

Inherited: the assembled loss.
Experiment: score the shapes from C02.
Observation: the rod scores high, the round cloud low.
Conclusion (population): zero exactly when the cloud is `N(0, I_D)`.
Conclusion (finite): what we compute is an estimator; the guarantee is about
the global minimum.
Handed on: calibration.

> <bookmark mark='shapes'/>Run it on the shapes from earlier. <bookmark mark='rod'/>The rod scores high, because almost every direction sees a distribution with hardly any spread in it. <bookmark mark='ball'/>The round cloud scores low. That's what this loss pushes against.
>
> <bookmark mark='chain'/>At the population level the statement is exact. The score is zero precisely when every projection is a standard Gaussian, and by Cramer Wold, that happens precisely when the cloud is the standard Gaussian in D dimensions.
>
> What we actually compute is an estimator of that. <bookmark mark='N'/>N samples leave a positive score even for a perfectly Gaussian batch. <bookmark mark='M'/>M directions leave sampling noise in the average, falling like one over the square root of M. <bookmark mark='K'/>K knots leave quadrature error.
>
> <bookmark mark='global'/>And the population result describes the global minimum. It says nothing about local minima, and nothing about whether gradient descent reaches the minimum at all.
>
> So what's left is calibration — for a given N, M and K, deciding how small the score has to be before a batch counts as Gaussian.

| | |
|---|---|
| Enters | the C02 cloud rig with the primary readout now the `AVERAGE` SIGReg score; the eigenvalue triple demoted to a `MUTED` caption |
| Transforms | one shape tracker walks rod → pancake → ball while the score falls; the equivalence chain writes; three finite-parameter cards |
| Remains | the honest-scope statement |
| Exits | everything at `clear_beat()` |

The equivalence chain extends B11's in the same shape and colours:

```text
SIGReg_pop(Z) = 0  ⟺  u^T Z ~ N(0,1) ∀u  ⟺  Z ~ N(0, I_D)
```

Three safeguards for the project's highest-risk moment: the rod → ball morph
is a shape sweep, never framed as training (no step counter, no loss-over-time
plot, "run it on the shapes" is a scoring pass); the global-minimum sentence
is spoken while the chain is on screen and nothing moves; `facts.py` asserts
the displayed scores on the exact shapes shown.

Optional 8-second beat, cut first if C10 runs past 2:15: `data.ring_2d`, same
mean and covariance as a standard Gaussian, plainly not Gaussian, still
rejected — forecloses "this is just a covariance penalty".

Flags: `theorem_statement` — the chain, `SOURCE_MAP.md` §6g;
source-stated limitation — finite `N` leaves a positive score at order `1/N`
(§6f, verified empirically in B09 for the scalar case); stated, not derived —
`1/√M` (§7); **FORBIDDEN** — any inference about convergence rate,
optimisation dynamics, parameter uniqueness or absence of local minima.

---

## 4. Transition contracts

Every scene opens and closes with ~120 ms of held silence inside its first and
last `voiceover` block so `ffmpeg -c copy` concatenation cannot clip a
phoneme. There are no crossfades; a cut is a cut.

| Boundary | Last spoken | Last visible | First spoken | First visible | Persist / transform / disappear |
|---|---|---|---|---|---|
| **B11 → C01** | "…the same thing with a whole batch of vectors." | vector columns, amber `?`, `𝒯 ∈ ℝ` | "In the last chapter, we built the Epps-Pulley statistic…" | the equation | Deliberate recap cut. |
| **C01 → C02** | "Suppose we want it to follow a standard Gaussian in D dimensions." | centred cloud, `Z`, target label | "Suppose the cloud starts losing its spread." | the same cloud | Cloud persists; C02 manipulates the object C01 named. |
| **C02 → C03** | "…the loss has to compare distributions rather than assign partners." | the round cloud, restored | "Choose a unit direction u." | the same cloud | Cloud persists; pairing apparatus gone before the cut. |
| **C03 → C04** | "…but it cannot tell us whether the whole cloud does." | cloud at `phi=76°, theta=12°`, `u_3`, its shadow, `score(u_3)=0.872` | "Now suppose the cloud has structure." | the identical frame | C03's apparatus fades on the first beat before the cloud changes. |
| **C04 → C05** | "…It tells you nothing about the cloud behind it." | two-clump cloud, arrow, trace | "One direction wasn't enough. The coordinate axes give us two natural directions to try next…" | axes pulse, then the `y=x` cloud | Genuine reset; the narration carries the argument across. |
| **C05 → C06** | "…test directions that mix the coordinates." | bare diagonal cloud on a plane, `y=x` | "Keep turning the direction u." | the identical frame, direction returning | Exact visual seam. |
| **C06 → C07** | "…the loss needs a finite sample." | Gaussian cloud, eight retained spokes, four plots | "Every direction is a whole sphere of them…" | the same finite-direction problem | C06 performs the continuum-to-finite collapse itself. |
| **C07 → C08** | "They don't turn a finite batch into a proof." | cloud, fan, purple average | "One of those scores is still an integral…" | B11's gap axes | Deliberate object return; hard cut. |
| **C08 → C09** | "…not much left to gain." | knots on the gap axes, `K` | "Every piece of this is already on screen." | the C07 frame restored | Hard cut; C09 assembles from visible objects. |
| **C09 → C10** | "…the whole regularizer." | the formula | "Run it on the shapes from earlier." | formula pinned small, C02's rig entering | Formula persists, demoted; rig returns. |
| **C10 → end** | "…before a batch counts as Gaussian." | the honest-scope statement | — | — | `clear_beat()`. |

---

## 5. Claim ledger

Every mathematical statement in Chapter C with its status; `facts.py` and the
narration audit check against this.

| # | Claim | Scene | Status |
|---|---|---|---|
| 1 | `D = 3` on screen is a display choice | C01 | `QUALIFICATION`, said once |
| 2 | Ranks `3→2→1→0`; rank zero is the collapsed endpoint | C02 | exact construction; motivation deferred to Chapter A |
| 2a | In LeJEPA's setup, the isotropic Gaussian minimises worst-case downstream error | C02 | `source_statement`, cited |
| 3 | `E‖z − z*‖² = ‖z‖² + D`; expected pull `2z`; continuum independent of `N`; closed form from known moments | C02 | `exact_derivation`, `facts.py` |
| 4 | Anything about the optimisation trajectory of the pairing loss | C02 | **FORBIDDEN** |
| 5 | `u^T z_i` for unit `u` is an ordinary scalar batch | C03 | definition |
| 6 | A small `score(u)` is evidence about `u` alone | C03, C04 | `CLAIM`, earned by C04 |
| 6a | On `clumped_3d`: `score(x) = 17.095`, `score(y) = 0.046`, unit-variance coordinates | C04 | `exact_computation`, `facts.py` |
| 6b | On `clumped_3d`: half of the half-turn (`50°–140°`) scores below `0.5`, uniform grid | C04 | `exact_computation`, `facts.py` |
| 7 | `Z = (X, X)`: marginals exactly `N(0,1)`, eigenvalues `(2, 0)` | C05 | `exact_derivation`, `facts.py` |
| 7a | On `diagonal_2d`: `score(x) = score(y) = 0.244`, `81.785` at `135°` | C05 | `exact_computation`, `facts.py` |
| 8 | Gaussian marginals do not imply joint Gaussianity | C05 | `CLAIM`, by construction |
| 9 | `Z ~ N(0, I_D) ⟹ u^T Z ~ N(0,1)` for every unit `u` | C06 | `exact_derivation` |
| 9a | `φ_{u^T Z}(t) = φ_Z(tu)` | C06 | `exact_derivation`, `facts.py` |
| 10 | Every projection standard Gaussian ⟹ joint is `N(0, I_D)` | C06 | **`theorem_statement`** — Cramér–Wold via Fourier uniqueness, cited, never "therefore" |
| 11 | `u ~ N(0, I_D)`, `u ← u/‖u‖` is uniform on the sphere | C07 | `SOURCE_MAP.md` §8 |
| 12 | Larger `M` reduces Monte Carlo variation, not finite-batch uncertainty | C07 | `QUALIFICATION`, required |
| 13 | `K = 16 → 0.01%` vs `K = 2000`; `K = 8 → 0.04%`; `O(1/K²)` | C08 | source fact, **provenance unresolved** (C08 flags) |
| 14 | `SIGReg(Z) = (1/M) Σₘ 𝒯(u⁽ᵐ⁾ᵀ Z; λ)` | C09 | `SOURCE_MAP.md` §8, verbatim |
| 15 | Collapsed and low-rank clouds receive a high score | C10 | empirical evidence, this run — never "guarantee" |
| 16 | `SIGReg_pop = 0 ⟺ u^T Z ~ N(0,1) ∀u ⟺ Z ~ N(0, I_D)` | C10 | `theorem_statement`, §6g |
| 17 | Finite `N` leaves a positive score at order `1/N` | C10 | source-stated limitation, §6f |
| 18 | Estimator variance `~ 1/√M` | C10 | stated, not derived (§7) |
| 19 | Convergence rate, local minima, dynamics, parameter uniqueness | C10 | **FORBIDDEN** |

---

## 6. Remaining sequence

1. Ship the C06 revision: render, review against `RENDER_REVIEW_SPEC.md`,
   owner sign-off, then delete `C06_REVISION_DESIGN.md`.
2. C07, C08, C09 — the formula assembly last because it consumes their
   objects. Resolve the `K = 16` provenance (C08 flags) before C08 renders.
3. C10, reviewed against the claim ledger line by line.
4. `tools/script_dump.py` → `SCRIPT_chapterC.md`, `tools/narration_audit.py`,
   `facts.py`, the Archer pass, then `build.sh chapterC -qh --voice eleven`
   and the seam checks.

Voice budget: the ElevenLabs Creator account carries 127,467 characters per
month; a chapter pass is ~20,000. Audio is cached per passage, so freeze
narration at the draft-voice stage before an Archer pass.
