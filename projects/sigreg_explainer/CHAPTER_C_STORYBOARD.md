# Chapter C — storyboard

**Status (2026-09-05).** C01–C05 are implemented and have final-quality
1080p60 Archer renders; C05's is awaiting owner approval. C06 went through
three owner review rounds (2026-09-04/05) and its 1080p60 master is awaiting
the owner. C07 was implemented on 2026-09-05 on C06's last frame, rebuilt on
2026-09-06 around the score-versus-angle curve, and its 1080p60 master is
awaiting the owner; `RENDER_REVIEW.md` has the findings.
C08 was implemented on 2026-09-07 and C09 on 2026-09-08; both masters are
awaiting the owner. C10 is planned below and not started.

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
| 6 | `c06_every_direction.py` | every direction; Cramér–Wold | 4:04 master (2026-09-05), awaiting owner |
| 7 | `c07_sampling_directions.py` | `M` | 1:54 master (2026-09-07, spoken voice), awaiting owner |
| 8 | `c08_frequency_knots.py` | `K` | 1:16 master (2026-09-07, derivation pass), awaiting owner |
| 9 | `c09_assembling_sigreg.py` | assemble the line, name it | 1:24 master (2026-09-08), awaiting owner |
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
`SCRIPT_chapterC.md` for C01–C08 and drafted here for C09–C10 (drafts, not
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
       → height becomes brightness; turn u; the field        [field built HERE, once]
       → two clouds, same mean & covariance                   [back where B started]
       → their CFs differ: the Epps–Pulley gap, one direction  [the stake: the ring]
       → deform the ring until the slices and fields agree     [the attempt]
       → same shadow ∀u ⇒ same field ⇒ same distribution      [chain, field left, statement right]
       → that implication is Cramér–Wold                       [the name]
       → specialise to Z ~ N(0, I_D); the cloud condenses out of the field
       → back to the problem: pick u, project, score the batch, turn, repeat
       → the family closes as u goes round; "in every direction" hands to C07
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

### C07 — `M` sampled directions *(implemented 2026-09-05, rebuilt 2026-09-06 · density: medium)*

Inherited: the test needs every direction; C06's last frame.
Experiment: make "every direction" cost something, draw one direction the
only unbiased way available (a Gaussian vector divided by its length) and
show the draw is fair, score two of them, reveal the score as a function of
direction, then let sampled directions read that function.
Observation: the score-versus-angle curve spans `0.03–0.19`; two draws of
32 average `0.088` and `0.090` against the curve's mean of `0.095`.
Conclusion: replace the expectation over directions with an average over `M`
sampled ones. `M` is named after the settling has been watched, and nowhere
earlier.
Handed on: each score is still an integral over every frequency (C08 says
it; C07 does not).

Narration authority: `SCRIPT_chapterC.md`. Beats, each answering one
question a first-time viewer has at that moment:

| Beat | Viewer's question | Screen |
|---|---|---|
| 1 | why not every direction? | the sixteen spokes densify to 32, 64, 256 until the disc is solid and the eight plots are buried; the disc clears to the bare ring, named as the sphere of directions; a sphere has no single sweep |
| 2 | how do you pick one fairly? | `g` grows from the origin, `u = g/‖g‖` writes, the arrow is scaled to length one and lands on the ring as `u_1`; fifty round draws are pushed to the ring and land evenly; "round" is said only after that is seen |
| 3 | what does one direction give? | the 36 sample points fly onto `u_1`'s rim plot, the bell draws, the mismatch pulses, `score(u_1) = 0.101`; `u_2` is drawn straight to the ring (the recipe is known), its plot and `0.049` |
| 4 | why do they differ, and what is the average of? | the wheel slides left; a score-versus-angle panel enters (C04's object); u sweeps a half turn over at least six seconds while a pen traces `score(u)` (its own passage, ending in silence if the words run out); then the two numbers sit on the curve and a dashed `AVERAGE` line marks the curve's mean, captioned `every direction = 0.095` |
| 5 | so why sample at all? | said: a sphere in D dimensions has no single sweep, so the loss reads the curve where its draws land; a third draw is shown alone (spoke, reading, the average of three), then thirty more in two waves; a solid `AVERAGE` line with a live `average =` readout settles against the dashed one; `M = 32` written after |
| 6 | what does more `M` buy, and what not? | a different thirty-two from `REDRAW_SEED` land elsewhere and average almost the same; the cloud pulses, the dashed line pulses: the curve belongs to the batch, only a different batch would move it |

Geometry shared with C06 and C09 lives in `common/wheel.py`. Every draw is
a named seed in `common/data.py` (`sampled_directions`, `REDRAW_SEED`,
`direction_spray`) so the scene and `facts.py` draw the
same points. C09 assembles `(1/M) Σ` from a compact copy of the score panel
(the redraw's marks, purple line, `average` readout and `M = 32`), so the
number it writes is the one this scene's last frame shows.

Flags: `SOURCE_MAP.md` §8 verbatim: `u ~ N(0, I_D)`, `u ← u/‖u‖`
(`facts.py`: a million normalised draws within 1.4% of uniform over 36
sectors; the fifty shown put 5–7 in each of eight). `QUALIFICATION`, required: more `M`
reduces Monte Carlo variation, not finite-batch uncertainty — shown as the
redraw and spoken as "only a different batch would move it"; `facts.py`
checks both draw averages against the curve's mean. `1/√M` is not said
(C10). Typical `M` range is not said.

### C08 — `K` frequency knots *(implemented 2026-09-07 · density: medium)*

Inherited: `M` scores, each an integral over every frequency.
Experiment: take the second sampled direction's score from C07 (`0.049`),
draw its weighted squared gap over frequency as the area B11 defined, and
replace the area by trapezoids on `K` knots inside Chapter B's window.
Observation, on this batch: four knots give `0.071` (44% off), eight give
`0.049` (within 0.05%), sixteen match every shown digit (within 0.01%).
Conclusion: replace each integral with `K` knots. `K` is named after the
convergence has been watched.
Handed on: both approximations are in place; the integral in the formula is
now a sum.

The point, once: each direction's score is an integral over every frequency,
and we cannot compute that either. So we read the integrand at K frequencies
and add up the trapezoids. A handful of knots already reproduces the area,
and that count is K.

| Beat | Viewer's question | Screen |
|---|---|---|
| 1 | which integral, and where does that curve come from? | B11's formula returns at the top; axes over `t` at fingerprint scale (0–1) with `score(u_2) = 0.049` beside them; `u_2`'s shadow fingerprint `\hat\varphi_N(t)` draws in `CLOUD`; the Gaussian's `\varphi_0(t)` draws over it in `TARGET` and a probe (dashed line, two dots, the gap between them in `COLLAPSE`) walks `t` from 0 to 5 on "at every frequency"; on "square the gap" both fingerprints fade and `N|\hat\varphi_N-\varphi_0|^2` rises in `COLLAPSE`, growing towards high `t` where the fingerprint is only noise, while the formula's red term pulses; on "weight it with the taper" `w_\lambda(t)` draws in `TARGET`, the formula's amber term pulses, and the red curve is crushed under it; on "we get this curve" the y-axis relabels to 0–0.03 and the crushed curve grows into the score curve; the area fills; on "we cannot add up over every frequency" the fill pulses |
| 2 | how do you add up with finitely many? | Chapter B's `[0.2, 4]` bracket under the axis; four `TARGET` knot lines and dots; the trapezoid polygon fills over the area; `K = 4`, `sum = 0.071`, `off by 44%` |
| 3 | how many is enough? | eight knots, polygon reshapes, `sum = 0.049`, `off by 0.03%`; sixteen, `off by 0.004%`; the sum and the score pulse together; `K` pulses when named |
| 4 | what changed in the formula? | the integral and `dt` become `\sum_{k=1}^{K}` and `\Delta t`, `t` becomes `t_k` |

Hard cut from C07 (a different picture, deliberately). The batch is
`data.sampled_directions()[1][1]` applied to the C06 cloud, so the number on
screen is the one C07 spoke; the area is the dense trapezoid integral over
the window, doubled for `t < 0`, which rounds to the same three decimals as
the full-grid score.

Flags: the source's `K = 16 → 0.01%`, `K = 8 → 0.04%` and `O(1/K²)` are
**not** spoken; the narration says what this batch gives ("on this batch"
is implicit in "the area" being the one on screen) and `facts.py` checks
the three sums and their errors. The window and the weight are settled
inputs and are not reopened; trapezoidal end-weights are not shown (the
formula reads `\Delta t`, with `\approx`).

### C09 — Assembling SIGReg *(implemented 2026-09-08 · density: low)*

Inherited: two motivated finite approximations, and C08's last frame.
Experiment: write down what has been happening; each symbol already has a
picture attached.
Conclusion: `SIGReg(Z) = (1/M) Σ_{m=1}^{M} 𝒯(u^{(m)T} Z; λ)`, named here for the
first time in the explainer, and evaluated on the batch on screen: `0.090`,
the number C07's purple line already showed.
Handed on: the line alone, parked small at the top, where C10 finds it.

The point, once: everything the loss does has now been watched one piece at a
time. Written in order, the pieces are one line. LeJEPA calls that line
SIGReg, and on the batch on screen it comes out at the number the purple line
was already showing.

| Beat | Viewer's question | Screen |
|---|---|---|
| 0 | what is left to do? | C08's last frame, continued through the shared builder in `c08_frequency_knots.py` (exact seam); the knot panel and its numbers clear; the discretised score formula shrinks and parks at the top |
| 1 | where does the argument come from? | bottom-left, a compact cloud in its ring with one drawn direction `u` (the one C08 scored), the projection line, and its rim shadow against the bell, labelled `u^T Z`; the label rises into the line and cross-fades into `u^{(m)T} Z`; the argument pulses on "the little m just counts which of our draws it was" |
| 2 | what is `𝒯`? | the bell pulses on "score those numbers against the standard Gaussian"; the parked formula pulses, then its `Σ_k` and `w_λ` on "K knots" and "the taper of width lambda"; the whole formula folds into `𝒯( · ; λ)` around the argument; `;λ)` pulses on "keep lambda inside the brackets" |
| 3 | what is `(1/M) Σ`? | bottom-right, the compact score-versus-angle panel: curve, the redraw's thirty-two marks, `M = 32`; the purple average line and `average = 0.090` on "take the average"; copies of the readout and `M` rise into `1/M` and `Σ_{m=1}^{M}` |
| 4 | what is it called? | the line pulses on "the whole regularizer"; `SIGReg(Z) =` writes as the name is spoken for the first time; the `Σ` and the marks pulse on "sketched", the bell and `𝒯(` on "isotropic Gaussian" |
| 5 | what does it give on the batch we watched? | the cloud pulses; `M = 32, K = 16` above the line's right end, one at a time as spoken; `= 0.090` after the line; the purple readout, the purple line and the value pulse together on "the number the purple line was already showing"; pictures and numbers leave; the line shrinks to its parked position while the last sentence is spoken |

Pictures indicate, labels transform: every symbol arrives from a small text
proxy (`u^T Z`, the parked formula, the `average` readout, `M = 32`) that
moves into its slot and cross-fades, never from the cloud or the fan of
marks, so nothing jumbles. The line is laid out once (`common/formula.py`,
shared with C10, verbatim `SOURCE_MAP.md` §8 including `;λ`) and does not
move until it parks.

Flags: the acronym expansion "sketched isotropic Gaussian regularization" is
spoken; it is not in `SOURCE_MAP.md` §8 and should be checked against the
paper's abstract before the chapter is assembled. The number is framed as
agreement, not magnitude — `facts.py` (`c09`) asserts that the `K = 16` knot
average over the redraw directions prints the same three decimals as C07's
full-grid readout (`0.0897` vs `0.0900`); calibration is C10's. `N` is in
the picture (the parked formula's prefactor) but not spoken.

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
| **C06 → C07** | "…and we never had to look at it in D dimensions." | Gaussian cloud in the wheel, u at 45°, eight plots, `Z ~ N(0, I_D)` | "So the test has to pass in every direction." | the identical frame, rebuilt from `common/wheel.py` and the same seeds (last/first-frame diff checked 2026-09-05) | Exact visual seam; C07 opens the continuum-to-finite question. |
| **C07 → C08** | "…and the only thing that would move it is a different batch." | wheel left with two rim plots and two dimmed fans; score panel right with the curve, its marks, dashed `every direction = 0.095`, solid `average = 0.090`, `M = 32` | "Now, each of those scores is still an integral…" | B11's formula, then the gap axes | Deliberate object return; hard cut. |
| **C08 → C09** | "…and now the score is something we can actually compute." | sixteen knots on the gap axes, `K = 16`, `sum = 0.049`, `score(u_2) = 0.049`, the discretised formula | "So now we have everything we need, and we can write the whole loss down in one line." | the same frame, built by `c08_frequency_knots.final_frame` | Continuity seam through shared code; last/first frame diff is codec noise only (mean 0.44/255, no shift). |
| **C09 → C10** | "…What we have not seen yet is what it does to a cloud." | the line alone, parked at `common/formula.py`'s `PARK` (font 34, top centre) | "Run it on the shapes from earlier." | the same parked line (`parked_sigreg_formula()`), C02's rig entering | Line persists through shared code; rig returns. |
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
| 13 | on the shown batch: `K = 4 → 0.071` (44% off), `K = 8 → 0.049` (0.03%), `K = 16` (0.004%) vs `K = 2000` | C08 | `exact_computation`, `facts.py`; the source's 0.04% / 0.01% figures are not spoken |
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
2. ~~C09~~ — done 2026-09-08; it continues C08's frame and brings back
   compact copies of C07's objects rather than restoring C07's last frame.
3. C10, reviewed against the claim ledger line by line; it must open on
   `common.formula.parked_sigreg_formula()` exactly as C09 leaves it.
4. `tools/script_dump.py` → `SCRIPT_chapterC.md`, `tools/narration_audit.py`,
   `facts.py`, the Archer pass, then `build.sh chapterC -qh --voice eleven`
   and the seam checks.

Voice budget: the ElevenLabs Creator account carries 127,467 characters per
month; a chapter pass is ~20,000. Audio is cached per passage, so freeze
narration at the draft-voice stage before an Archer pass.
