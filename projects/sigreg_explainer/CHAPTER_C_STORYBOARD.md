# Chapter C — script & storyboard

**Status:** living production storyboard. C01–C04 are implemented and
render-verified. C05 has an owner-directed 2026-08-20 low-quality review draft;
C06–C10 remain planned. The generated narration authority for implemented
scenes is `SCRIPT_chapterC.md`, which must be regenerated from the scene source
after every voiceover edit.

**C01–C03 revision note (updated 2026-08-16):** their detailed narration blocks below
are retained as design history and are superseded by `SCRIPT_chapterC.md`.
C01 now recalls Chapter B with the actual Epps–Pulley equation and two computed
scalar examples, then uses a 3Blue1Brown-2017-derived `35 → 8 → 6 → 8` network.
Seven large 5×7 digits run at a readable pace before the compact batch appears.
Each digit has an exact flattened-pixel correspondence with the 35 input
neurons, the whole network propagates with a subdued blue wave, and the centred
output head grows through `D=1`, `D=2`, and `D=3`, then continuously through
`D=4,6,8`. There is no matrix panel and no early `Z` label. The geometry remains
the visible `D=3` preview while the wider heads establish practical scale; the
diagram then clears into the centred cloud, which is named `Z` only after it
exists.
C01's final ElevenLabs wording uses “a neural network produces those numbers”
instead of the repeatedly mispronounced “encoder.” C02 is now a 476-word
pedagogical construction with no decorative top captions. Its brief collapse
ladder is organized by `rank(Z)=3→2→1→0`; collapse is named once, and the old
constant-network/input-card explanation is gone because Chapter A owns it.
The restored target is unpacked as zero mean and identity covariance while a
unit direction rotates through the unchanged round cloud. One blue embedding
and one sampled amber partner establish the pointwise loss before thirteen
fainter pairs extend it to the batch. Resampling leaves the blue cloud fixed;
the averaging beat then follows one fixed embedding. The lower equation panel
expands the square and accounts separately for the zero cross term and the
partner's expected squared length `D` before simplifying. C02 has a final
ElevenLabs 1080p60 delivery (163.87 s).
C03 is now a 344-word, 110.27 s Archer cut (updated 2026-08-17: removed
`ThreePanelRig.link()`'s dashed centroid-to-curve connector, which read as a
stray diagonal line across the circle and characteristic-function panels;
tightened the narration — dropped a literal repeat of C02's closing line, the
flagged "simply," and duplicated "now"/"So now" openers; and fixed three
animation defects with no narration change — an unregistered frame-coordinate
seed arrow that the 3-D camera projected into a stray skewed arrow over the
circle, a `FadeIn` on `always_redraw` mobjects that silently did nothing and
let the rig pop, and a `Group` `FadeOut` that forced the already-hidden
discrepancy formula back to visible on top of the score. See the handoff's
current-status section for the three Manim traps involved, all of which render
without an error.) It motivates
projection as the
missing `R^D -> R` bridge, projects one embedding before the full batch,
then projects a second embedding on the opposite side so the signed readout
visibly changes from positive to negative. It
preserves the resulting signed coordinates as they enter the established
Epps--Pulley rig, and visibly runs the frequency sweep. A moving red marker
shows the instantaneous curve separation while the weighted squared gap grows
behind `t`. The final 3-D beat then turns the same finite cloud through three
directions and recomputes the exact scores `0.055`, `0.046`, and `0.872`. See
the current-status section of `NEXT_MODEL_HANDOFF_chapterC.md` for the render
contract.

**Governed by:** `NEXT_MODEL_HANDOFF_chapterC.md` (binding), `PLAN.md`, `SOURCE_MAP.md`, `docs/NARRATION_SPEC.md`, `docs/VISUAL_SYSTEM.md`, `docs/RENDER_REVIEW_SPEC.md`, `ANIMATION_PLAYBOOK_chapterB.md`, `CHAPTER_B_REVIEW_GUIDE.md`.

---

## 0. The Chapter C causal arc, in one pass

Chapter B ended holding a machine that eats a line of numbers and returns one number saying how far that line is from a standard Gaussian. Chapter C's whole job is to feed a cloud of vectors into that machine without building a second machine.

The chain, stated as the reasoning a viewer actually performs:

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

This does not contradict §4 of the handoff. It sharpens it in three places, each flagged for approval:

1. **The isotropic-Gaussian target constancy is promoted to a load-bearing beat, not a footnote** (Scene F). It is the reason a single amber target curve can be reused in every direction, and without it the averaging in Scene G is unmotivated.
2. **The two directions of the Cramér–Wold biconditional are separated.** `Z ~ N(0,I_D) ⟹ u^T Z ~ N(0,1) ∀u` is demonstrated visually (rotate `u` on an isotropic cloud; the bell never changes). The converse is the cited theorem. Collapsing these into one on-screen "⟺" without saying which half we showed would be exactly the proof-strength failure `SOURCE_MAP.md` §6e forbids.
3. **Scenes D and E are two different failures, not one repeated twice.** D: an arbitrary direction can be innocent. E: the *privileged* directions can be innocent. The escalation is what makes "every direction" feel forced rather than asserted.

---

## 1. What Chapter B literally hands over

This is not paraphrase. `chapterB/b11_fingerprint_to_loss.py` ends (lines 891–915) on `_vector_bridge()`:

- three vector columns `z_1`, `z_2`, `…`, `z_N`, each a 3-entry bracket in `CLOUD` blue;
- an amber arrow labelled `?`;
- `𝒯 ∈ ℝ` in `INK`;
- final spoken line: *"In the next chapter, we'll discuss how to do the same thing with a whole batch of vectors."*
- then `inspect(1.35)` and `settle_frame()`.

**Chapter C opens on that frame.** Not a variation of it — that frame. This is the single largest continuity asset in the project and every choice below is downstream of it.

Available and reused throughout:

| Asset | Path | Chapter C use |
|---|---|---|
| `ThreePanelRig` | `common/rig.py` | Scene C mounts it literally; D–E use its score only |
| `ecf`, `gaussian_cf`, `wrapped` | `common/wrap.py` | every scalar score computed in C |
| `CharacteristicFunctionPlot` | `common/fingerprint.py` | Scene H's knot beat |
| `layout.RIG_*`, `fit_in_frame`, `stack_levels` | `common/layout.py` | Scene C's shadow→number-line landing |
| `data.gaussian_3d`, `degenerate_3d`, `diagonal_2d`, `ring_2d`, `bimodal_1d`, `gaussian_1d` | `common/data.py` | already seeded for exactly these scenes |
| `ActScene` (`across`, `inspect`, `freeze`, `clear_beat`, `clear_overlay`, `settle_frame`) | `common/beat.py` | all scenes |
| `ty.*`, `palette` roles | `common/type.py`, `common/palette.py` | all scenes |
| build-once + updater 3-D cloud, pristine `unit_points` ellipsoid, `add_fixed_orientation_mobjects` | `chapterC/c02_covariance.py` | technique preserved, rehomed (§3) |

`data.py` already contains `diagonal_2d` documented as *"Act 7's counterexample"* and `degenerate_3d` documented as the ball→pancake→rod→point walk. The data layer was written for this chapter. It does not need to change.

---

## 2. Scene architecture

Ten scenes, the handoff's Scene A–J order preserved. Files follow `PLAN.md` §6 (`<letter><number>_<slug>.py`, class = uppercased prefix, `build.sh` sorts on filename).

| # | File | Class | Handoff | Beat | Target |
|---|---|---|---|---|---|
| 1 | `c01_vectors.py` | `C01` | A | scalars become vectors | 1:10 |
| 2 | `c02_the_shape_is_the_goal.py` | `C02` | B | shape ladder + the wrong fix | 1:50 |
| 3 | `c03_one_shadow.py` | `C03` | C | the rig returns on one shadow | 1:38 |
| 4 | `c04_one_shadow_is_not_enough.py` | `C04` | D | turn `u`, the shadow lies | **0:47 built** (est. 1:30) |
| 5 | `c05_gaussian_marginals.py` | `C05` | E | `Z = (X, X)` | **0:45 owner-review draft** |
| 6 | `c06_every_direction.py` | `C06` | F | one target, all directions; Cramér–Wold | 1:30 |
| 7 | `c07_sampling_directions.py` | `C07` | G | `M` | 1:50 |
| 8 | `c08_frequency_knots.py` | `C08` | H | `K` | 1:20 |
| 9 | `c09_sigreg.py` | `C09` | I | assemble the formula | 1:30 |
| 10 | `c10_what_it_claims.py` | `C10` | J | anti-collapse, population limit, honest scope | 2:00 |

C04 came in at 0:47 against a 1:30 estimate, while C05's current owner-review
draft runs 0:45. The first four delivered scenes run 0:46, 2:44, 1:50 and
0:47; C05's duration remains provisional until the owner approves narration
and authorizes a final voice pass. The per-scene estimates are not tracking
anything and should not be treated as a delivery forecast.

**Estimated total ≈ 16:30.** `PLAN.md` §5 says "~9 min". That estimate is wrong in the same way Chapter B's was (8 min estimated, 17:50 built) — it counted plan items, not scenes. State the honest number now rather than discovering it at master-build time.

**`c02` keeps its number.** The prototype's content — the shape ladder — is exactly plan item C.2 and exactly handoff Scene B. The file gets a slug that names its job; its geometry moves to `common/` (§3). This answers "where does the cloud-geometry prototype belong" without a speculative rename.

### Colour assignment (fixed here, stable for the chapter)

No new hex values. `common/palette.py` already reserves everything needed.

| Role in Chapter C | Palette role |
|---|---|
| embedding cloud, samples, their fingerprint | `CLOUD` `#4FA8E8` |
| direction `u`, its line, guide lines, shadow dots, per-direction score `𝒯(u)`, score-vs-angle curve | `DIRECTION` `#5FCF80` — unused in Chapter B, semantically exact ("directions, projections, shadows") |
| the standard-Gaussian target and its curve | `TARGET` `#F0B429` |
| the gap, the failure shapes, a high score | `COLLAPSE` `#E8615A` |
| the direction-averaged score, the SIGReg value | `AVERAGE` `#9D6FE0` — the same purple that meant "average of many arrows" in Chapter B; it now means "average of many directions" |
| axes, ellipsoid wireframe, captions | `AXIS` / `GRID` / `MUTED` |

`MAGNITUDE` `#E2549C` stays unused. Yellow appears only on the target and on a genuinely active parameter — never on equations wholesale.

---

## 3. Where the `c02_covariance.py` prototype goes, and what changes

**Verdict: the technique is kept, the scene is not.** The prototype's file docstring is a correct engineering argument and its three load-bearing decisions must survive verbatim in behaviour:

- flat `Dot`s registered with `add_fixed_orientation_mobjects`, not 260 `Dot3D` spheres (Cairo draws a `Sphere` as a quad mesh; rebuilding per frame does not render);
- one `add_updater` moving a cloud built once, never `always_redraw` — `add_fixed_orientation_mobjects` registers the *instance*, and `always_redraw` silently drops the registration and lets the readout tumble with the camera;
- the ellipsoid rescaled from stored pristine `unit_points` each frame, never compounded — compounding drifts and cannot recover once an axis reaches `1e-3`.

**What changes:**

1. **It becomes `common/cloud.py::CloudRig`**, not a scene. Five scenes need a stable 3-D dot cloud whose geometry is driven by a tracker (C02, C03, C04, C07, C10). That clears the handoff §11 bar of "at least two Chapter C scenes need the same contract."
2. **The eigenvalue readout leaves Scene B.** `(λ₁, λ₂, λ₃)` is covariance vocabulary and Scene B is about shape, not rank arithmetic. Worse, showing eigenvalues while establishing the goal quietly implies the test *is* a covariance test — which SIGReg specifically is not (`data.ring_2d` exists as the counterexample to exactly that). The readout returns in C10 as a **muted secondary caption** naming which shape we are in, while the primary readout is the SIGReg score in `AVERAGE` purple.
3. **The ambient rotation is cut to one purposeful move per scene.** Handoff §8: "prefer one purposeful camera move over continuous ornamental rotation." The prototype's 3°/s spin runs for its full 20 seconds. Keep parallax where depth genuinely carries information (C02's ladder, C03's projection) and hold still where a shadow and a direction must stay readable.
4. **The morph direction reverses in C10.** The prototype walks ball → pancake → rod → point, which is the *definition* of collapse and belongs in C02. C10 walks rod → ball with the score falling, which is what the loss opposes.
5. **The caption `Transform(caption, self._cap(...))` pattern is a known trap** — it mutates `caption` while the variable name suggests otherwise (`ANIMATION_PLAYBOOK` "Local failure modes"). Rebuild with a stable caption instance updated in place.
6. **`SCALE = 1.15` and the `data.gaussian_3d(n=260)` count** carry over. `data.gaussian_3d` defaults to `n=220`; pick one and put it in `common/data.py`, not in a scene.

Everything else in the file — including the comments explaining *why* — should be preserved into `common/cloud.py`. Those comments are the record of two solved bugs.

### The other two new `common/` modules

Both meet the two-scene bar; neither is speculative.

**`common/project.py` — `CloudProjectionRig`.** Used by C03, C04, C05, C07, C10. One source of truth for the direction (handoff §11). Its state is a single unit-vector-valued object (a `ValueTracker` angle in the 2-D scenes, a `(θ, φ)` pair or explicit unit vector in 3-D), and it derives, all from that one state:

- the `DIRECTION` arrow in the cloud;
- the projection line through the origin;
- the dashed guide line from each cloud point to its foot;
- the scalar array `u^T z_i` as a NumPy array;
- the shadow dot positions;
- the score `𝒯(u^T Z)`;
- the score-vs-angle trace.

The API should be written against these five scenes' actual needs and nothing else.

**`common/score.py` — pure NumPy, no mobjects.** `epps_pulley(samples, lam, grid)` and `sigreg(Z, U, lam, knots)`. Every displayed number in Chapter C must come from these, and so must `facts.py`. Note that `b11_fingerprint_to_loss.py` currently computes Epps–Pulley inline (`EP_GRID = linspace(-8, 8, 4000)`, `EP_LAMBDA = 1.0`, `N * trapezoid(w * |φ̂ − φ₀|²)`). Extracting it must reproduce `EP_BIMODAL_SCORE` and `EP_GAUSSIAN_SCORE` bit-for-bit or Chapter B's rendered numbers change. Verify before switching `b11` over; if there is any doubt, leave `b11` alone and have `common/score.py` be the single definition Chapter C uses.

**One small `ThreePanelRig` API addition** (§7, decision 9): `mount(..., dots=None)` so C03 can hand the rig the shadow dots it already owns instead of the rig spawning a second set. Without it, C03 either creates ghost points or performs a fade-in/fade-out swap — both explicitly banned by handoff §8.

**Do not build:** a `SIGRegScene` base class, a generic direction-fan animation framework, a reusable quadrature widget, or a 3-D shadow abstraction that anticipates uses no scene has.

---

## 4. The scenes

Each entry gives: the causal beat, narration draft, persistent-object storyboard, reuse-vs-new, and claim flags. Narration density is classified per `NARRATION_SPEC.md` §22.

Spoken aliases, decided once: **"Cramer Wold"** spoken, `Cramér–Wold` displayed. **"u transpose z"**, **"z sub i"**, **"the letter M"** / **"the letter K"** only if the raw letters mispronounce in preview. Listen to every clip before animating final timing.

---

### C01 — From a number line to an embedding cloud
*(handoff Scene A · 0:47 · density: low)*

**Causal beat.**
Inherited: Chapter B's mechanism scores a scalar batch.
Experiment: run it on Gaussian and two-mode batches, then reveal those scalars as the one-coordinate output of a representation model.
Observation: widening the output layer from one neuron to two and then three makes every output a longer coordinate column and changes the batch from a line to a plane to a cloud.
Conclusion: the score must now act on the whole batch of vectors.
Handed on: what distribution should that collection have?

**Narration.**

> In the last chapter, we built the Epps-Pulley statistic, which compares a scalar batch with the standard Gaussian. A Gaussian-shaped batch scores low, while a batch with a different shape scores higher.
>
> Suppose those numbers come from an encoder. With one output coordinate, every input gives us one scalar, and the whole batch still lies on a line.
>
> After the batch passes through, those outputs form the same one-dimensional sample we scored before.
>
> Now, if we widen the output layer, each input gets a second coordinate. The line opens into a plane. Add a third, and the batch becomes a cloud.
>
> We'll use three dimensions because that's what we can see. In practice, D is often much larger.
>
> From here on, this cloud is Z. Suppose we want it to follow a standard Gaussian in D dimensions.

**Persistent objects.**

| | |
|---|---|
| Enters | Chapter B's Epps–Pulley formula with compact, computed Gaussian and two-mode score examples |
| Transforms | seven large individual digits cycle through a fully propagating network; the compact batch then appears; the centred output head and the same sample dots grow through line, plane, and cloud, followed by a continuous `D=4,6,8` head demonstration |
| Remains | the fifteen output-dot instances as the line becomes a plane and then a centred 3-D cloud |
| Exits | input cards, network, dimensionality label, and flat preview before the camera enters the 3-D cloud; only then does `Z` appear |

**Choreography note.** Preserve `_2017/nn/part1.py::NetworkMobject`'s explicit layers, behind-node connections, literal pixel/input mapping, and full-layer feed-forward rhythm. Computation continues beneath narration; do not leave a narration-free first pass. Use the low-opacity blue edge wave, not the old bright orange flash. Keep the output dots alive through line → plane → cloud.

**Reuse vs new.** Reuses `layout.RIG_LINE_CENTRE`/`RIG_LINE_WIDTH`, `data.gaussian_1d`, `data.gaussian_3d`, `ty.*`. New: the number-line→embedding-cloud choreography (scene-local, one-off — do not abstract it). New: `common/cloud.py` first use.

**Claim flags.**
- `QUALIFICATION` — `D=3` is explicitly displayed during the output-width progression and fades before the centred cloud shot.
- No mathematical claim is made in this scene. It is a change of object, not of argument.

---

### C02 — The shape is a property of the collection
*(handoff Scene B · ~2:44 ElevenLabs Archer · density: medium)*

**Causal beat.**
Inherited: C01 has adopted a standard Gaussian target for the embedding cloud.
Experiment 1: remove the spread along one axis, then another, then the last.
Observation 1: the batch rank falls `3→2→1→0`; rank zero is named as collapse
once in its own clean narration beat, without reopening Chapter A's
model-failure explanation.
Experiment 2: restore the target and motivate `N(0,I_D)` twice. LeJEPA's cited
downstream-risk result supplies the reason for this particular target, and the
future-video deferral immediately qualifies that claim. “For now” then leads
directly into zero mean, unit variance, and no preferred direction. The compact
direction arrow must remain inside the amber target while it leaves the screen
plane and sweeps through 3-D.
Training then asks how the blue batch can be made to match the amber target and
creates the need for a loss that measures that mismatch; both distributions and
the loss pulse on their spoken phrases. Try to build that loss by assigning one
independently sampled Gaussian partner to each embedding.
Observation 2: resampling changes every assignment while the blue cloud stays
fixed. As “infinitely many possible draws” is spoken, thirty rapidly
accumulating amber samples and their faint candidate lines replace the former
three-alternative illustration. For one fixed embedding, increasingly many
possible partners fill the target. Instead of listing every draw, the target
distribution calculates their expectation over a continuum independent of
batch size `N`. Its known mean and variance let that expectation be evaluated
exactly. The expanded square remains attached to the cloud: the blue
radius supplies `||z||`, the amber halo supplies the target moments, and a field
of red origin-directed arrows shows the pointwise minimum for the batch.
Conclusion: assigned partners cannot impose a property of the collection.
Handed on: measure the collection.

**Narration authority.** The implemented wording is generated in
`SCRIPT_chapterC.md`; do not copy the obsolete draft back into the scene. Its
spoken sequence is rank ladder → isolated collapse conclusion → theoretical
target motivation → immediate future-video qualification → “For now” and the
target geometry → need for a mismatch-measuring loss → one explicit pair → batch pairs and resampling →
one fixed embedding against infinitely many possible draws → exact expectation
from known moments → cloud-linked algebra → distributional conclusion. Logical
connectives are deliberate: each "so," "if," and "suppose" marks a dependency
rather than decorating a stage direction.

**Persistent objects.**

| | |
|---|---|
| Enters | the C01 cloud, unchanged, plus `ThreeDAxes` and a fixed-frame rank readout |
| Transforms | one shape tracker walks `(1,1,1) → (1,1,0) → (1,0,0) → (0,0,0)` while `rank(Z)` follows `3→2→1→0`; it then returns to `(1,1,1)`, gains the faint `TARGET` shell and a compact `DIRECTION` arrow that remains inside that shell while sweeping through genuine 3-D orientations; the batch, target, and `L_match(Z)` pulse in spoken order before the camera drops to a 2-D slice for the pairing beat; thirty candidate draws rapidly accumulate at the infinite-continuum beat; the algebra adds a blue radius, a 48-draw amber halo, and origin-directed arrows on the sampled batch points |
| Remains | the same 220 dot instances through the entire ladder — the ellipsoid rescales from pristine `unit_points` |
| Exits | the ellipsoid, the pairing arrows, the Gaussian partner dots. The cloud stays for C03. |

**Rhythm.** Handoff §9: introduce → settle → vary → settle → reveal. Each rung
of the ladder gets a settled endpoint with the small rank readout. The target
facts arrive on their spoken clauses while the green direction moves through
depth as well as the screen plane. The batch resample remains a discrete pulse,
while the continuum explanation deliberately uses a rapid accumulation of
candidate draws.

**Reuse vs new.** Reuses `common/cloud.py` (the extracted prototype), `data.degenerate_3d`, the `TARGET` ellipsoid. New: the 2-D pairing beat (partner dots, pull arrows, the averaged origin arrow, the one-line identity). The pairing beat is scene-local; it appears nowhere else.

**Claim flags.**
- `source_statement` — in the setup analyzed by LeJEPA, the isotropic Gaussian
  minimizes worst-case downstream prediction error. Cite that result; this
  scene does not prove it.
- `exact_derivation`, verified in `facts.py` — `E_{z*~N(0,I_D)} ‖z − z*‖² = ‖z‖² + D`, hence the gradient of the *expected* pairing objective at `z` is `2z`. This is a statement about the objective, not about training.
- `QUALIFICATION` — the expectation ranges over infinitely many possible target
  draws and is unrelated to the number `N` of blue embeddings. Enumerating all
  draws is impossible, but Monte Carlo approximation is possible. The exact
  simplification here uses the target's known first two moments and is not a
  capability unique to Gaussian distributions.
- **Hard boundary.** The narration must not say or imply that gradient descent on this objective collapses the cloud, or that any particular trajectory follows. Handoff Scene B: "Avoid claiming that a particular optimization trajectory is inevitable." Say what the expected pull is; stop there.
- The target explanation uses definitions only: `E[z*]=0` and
  `Cov(z*)=I_D`; for `D` unit-variance coordinates,
  `E||z*||²=D`. Do not promote the rotating-direction picture into C06's
  every-projection theorem; here it establishes isotropic geometry only.

---

### C03 — One projection gives a scalar batch
*(handoff Scene C · 1:50.27 final Archer delivery · density: low — this is the recognition payoff, and narration should stay out of its way)*

**Causal beat.**
Inherited: measure the collection.
Experiment: pick a unit direction; read off how far along it each vector sits.
Observation: those readings are an ordinary batch of numbers, and Chapter B's rig accepts them without modification.
Conclusion: one direction produces one score.
Handed on: does a small score along one direction say anything about the cloud?

**Narration authority.** The current 344-word narration is generated in
`SCRIPT_chapterC.md`. Its causal order is fixed: motivate the scalar/vector
type mismatch; choose a visibly normalized direction; project one positive
and one negative example; repeat for all `N`; identify the result as the scalar batch
the Epps--Pulley pipeline already accepts; run the characteristic-function
comparison; read the small score; then turn the actual 3-D direction twice and
show that the same finite cloud produces different shadows and scores.

**Persistent objects — this is the most choreographed transition in the chapter.**

| Phase | What happens |
|---|---|
| 1 | Cloud from C02 holds. “Epps--Pulley needs `{x_i}⊂R`” and “the model gives `{z_i}⊂R^D`” appear on their spoken clauses, then clear into the explicit `R^D -> R` bridge. The camera changes angle with the type contrast so the cloud reads as genuinely 3-D. |
| 2 | A `DIRECTION` arrow exactly one visible axis tick long grows from the origin while a thinner, lower-opacity line spans the cloud. `u, ||u||=1` appears on the unit-length clause, and normalization is motivated as preventing accidental rescaling. |
| 3 | One blue `z_i` is isolated and projected to `s_i=u^Tz_i=+1.93`. A second point on the opposite side is then projected with its own guide, and the displayed readout changes to `s_j=u^Tz_j=-1.53`. The positive/negative rule is therefore shown rather than merely narrated. |
| 4 | Forty-four representative `MUTED` guides establish repetition without turning the frame into a wire cage; all 220 dots descend into the one-dimensional shadow and the formula becomes `{u^Tz_i}_{i=1}^N⊂R`. |
| 5 | The same shadow instances flatten into screen space and settle onto `layout.RIG_LINE_CENTRE`; cloud and 3-D furniture are explicitly unregistered so no Cairo billboards bleed into the rig shot. |
| 6 | `rig.circle`, `rig.axes`, and titles fade in around those exact dots; `rig.mount(scene, dots=shadow_dots)` adopts them. `link=True` was dropped 2026-08-17 — the dashed centroid-to-curve connector rendered as a stray diagonal spanning both panels rather than a legible local relationship. |
| 7 | Before the sweep starts, the average arrow, its rider and the `t` readout grow/fade in from registered static seeds — `b03_the_rig.py::average_beat`'s pattern — and only then are the live `always_redraw` objects added (fixed 2026-08-17). The 220 arrows need no reveal of their own: at `t = 0` they all coincide, so the bundle reads as one line beneath the average. Then `rig.t` sweeps 0 → 6.5, `rate_func=linear`, and completes the full blue empirical curve before the comparison begins. Arrows wrap and the centroid moves; the average-position/curve-height correspondence is carried by that synchronized motion alone, not a drawn connector. |
| 8 | The `TARGET` standard-normal curve appears exactly on “standard-normal curve.” Only after both complete curves are visible does a separate red marker sweep 0 → 6.5 and fill the weighted gap behind itself; the formula clears before the computed `0.055` appears. |
| 9 | **The rig hands off to the 3-D experiment**, as two sequential beats (fixed 2026-08-17): the rig fades out in place while the score it computed crosses from beneath the curve panel to its labelled `score(u_1)=0.055` position; only then do the cloud, direction and shadow fade into the cleared frame. The earlier `scale(0.08).move_to(meter)` shrink was dropped — it dragged a tray of illegible miniature panels across the frame, and overlapping it with the 3-D reveal put `restored_line` diagonally across the still-large 2-D panels. Two purposeful camera moves then accompany real changes to `u_2` and `u_3`. Every projected point moves, and the displayed score recomputes to `0.046` and `0.872`. |

Phase 9 is a design commitment worth stating plainly: it is the honest visual
claim that the scalar pipeline produces one number attached to one direction.
The scene does not merely state that changing `u` matters; it turns the same
cloud twice, moves all 220 projected points, and shows three exact scores. The
rig is shown at full size, in its literal `layout` positions, exactly once.

**Which cloud.** The isotropic cloud from C01/C02, unchanged. Recommended over a structured cloud: identity continuity is worth more than an impressive first number, and the small score establishes the baseline that C04 then contradicts. (§7, decision 8.)

**Reuse vs new.** Heaviest reuse in the chapter: `ThreePanelRig` in full (`mount`, `t`, `arrows`, `centroid`, `trace`, `rider`, `readout` — not `link`, dropped 2026-08-17), `layout.RIG_*`, `wrap.ecf`, `wrap.gaussian_cf`, `common/score.py`. New: `CloudProjectionRig`'s first use; the phase-5 lift; the phase-9 contraction.

**Claim flags.**
- `OBSERVATION` only. The score being small here is *not* evidence the cloud is Gaussian, and the narration must not suggest it is. C04 exists precisely to close that door.
- Every displayed number — the projected values and `score(u)` — comes from the same NumPy array driving the dot positions. Handoff §11: never a hard-coded label beside a separately evaluated animation.

---

### C04 — One shadow can be innocent
*(handoff Scene D · implemented 2026-08-17, narration rewritten the same day on owner review · 156 words incl. on-screen · density: medium)*

**Causal beat.**
Inherited: one direction gives one number.
Experiment: give the cloud two well-separated clumps and turn `u` through a half turn.
Observation: along one direction the clumps separate and the score climbs; a quarter turn later they sit on top of one another and the shadow passes for a bell, while the cloud has not moved.
Conclusion: a small score along one direction is evidence about that direction.
Handed on: then check the coordinate directions?

**Narration authority.** The implemented 156 spoken words are generated in
`SCRIPT_chapterC.md`. The sweep is **monotone 0 → 180°**, which the earlier
draft below was not, and the narration follows it: start on the axis the clumps
separate along and read the large score, turn a quarter and watch the piles
slide through each other, keep turning until the hole reopens, then draw the
conclusion. Monotone matters for more than tidiness — the trace is written
left to right exactly once, with no doubling back over itself, and a half turn
is every distinct direction in the plane because `u` and `−u` give the same
shadow up to sign.

**The cloud.** `data.clumped_3d()` — `bimodal_1d` along x, the isotropic
cloud's own coordinates along y and z, every column at mean 0 and unit
variance. The unit variance is load-bearing: with every direction reading a
batch at the same scale, the alarming direction cannot be detecting a scale
mismatch, so the claim really is about shape. Scores: `17.095` at 0°, `0.046`
at 90°, both checked in `facts.py`.

**Persistent objects.**

| | |
|---|---|
| Enters | C03's exact last frame — same cloud, camera at `phi=76°, theta=12°`, `u_3` on its shadow, `score(u_3)=0.872` in the same corner |
| Transforms | C03's apparatus fades out first, then one camera move both flattens onto the turning plane (`phi=20°, theta=-90°`) and slides the world left via `frame_center` to clear the panels, while the same 220 dot instances morph into two clumps; then one angle tracker drives arrow, line, all 220 shadow feet, the live `score(u)` readout and the trace |
| Remains | cloud, arrow, meter, and the completed score-vs-angle trace with both settled scores marked (it is the scene's product) |
| Exits | the axis tips and the z axis, with the camera; the two-clump structure at the cut |

**The shadow is a dot plot, stacked along the line's own normal.** 220 feet
drawn straight onto the line pile into one bar and hide the only thing the
scene claims. `layout.stack_levels` is the project's dot-plot rule; stacking
along the normal rather than a fixed screen axis keeps the whole plot rigidly
attached to the direction, so it turns with it. That is what makes "the two
piles slide straight through each other" a thing you watch rather than a thing
you are told.

**The silent Gaussian reference (owner instruction, 2026-08-17).** A standard
normal is drawn top-left, in `TARGET`, on the words "and a Gaussian has no hole
in the middle", and then left alone for the rest of the scene. It is never
named, labelled or pointed at, and it fades out in the silence after beat 3,
once both judgements have been made against it. Leaving it up past that turns a
reference into furniture, and nothing in beats 4 or 5 is a shape judgement. The
scene asks for two shape judgements against a bell — two piles with a hole,
then a single hump — and had been asking the viewer to make them against a
remembered bell rather than a drawn one. Because
it is on screen, beat 3 no longer has to say "close enough to a bell" at all;
the words shrank as the picture did the work. It is deliberately **not** in the
panel column: the free space there sits directly above "score along each
direction", and a caption that close reads as labelling the curve above it.
Caught in a draft frame, which is why draft frames come before ElevenLabs.

**The ending is the band.** Beat 5 marks the stretch of the trace scoring
below `BAND_LEVEL = 0.5` — 50° to 140°, exactly half the half turn — and says
so. It is marked with **two dashed MUTED boundary lines, not a filled
rectangle**: the shaded block was rejected on looks, and the dashed form turns
out to be the more honest one anyway. A fill behind the curve reads as an area
*under* it, which is an integral and not the claim; it also dulled the trace it
sat behind. MUTED rather than DIRECTION because green verticals crossing a
green curve separate badly, and dashed MUTED is already this project's
annotation-guide convention (`CloudProjectionRig.guide_lines`). The scene's verdict is not that one direction happened to be innocent but
that half of them are, and that is a picture rather than a sentence. The two
settled scores are marked first ("Seventeen here, and almost zero here" is
deictic, so the marks *are* the sentence), the band second, and the cloud comes
back to full brightness on the closing words "the cloud behind it". `facts.py`
checks the fraction, and checks that the angle grid is uniform — a half turn's
node fraction only equals a direction fraction on a uniform grid.

**Continuity dividend, taken.** The alarming direction's shadow is the
**two-clump batch grammar from `b00` and `b11`** — `data.bimodal_1d`, the
chapter's running example, now revealed as a shadow of a structured cloud.

**One source of truth.** A single `ValueTracker(theta)`, and one tabulated
score curve read by the live meter (`np.interp`), the trace, and the settled
marks alike. Handoff §11: never a hard-coded label beside a separately
evaluated animation.

**Reuse vs new.** Reuses `CloudRig`, `CloudProjectionRig` (for the seam
snapshot only), `common/score.py`, `layout.stack_levels`, `ty.readout`. New:
`common/project.py::TurningProjection` — angle state, updater-driven geometry,
and the score table. The trace *panel* is scene-local: the numbers are what
C05 and C07 will reuse, the layout is not.

**Vertical treatment (§7 decision 6).** C04 plots its full range linearly,
`0 → 18`, with both settled scores labelled numerically. It can afford to,
because `17.095` against `0.046` only has to read as "huge versus almost
nothing". C05 turned out to be able to afford the same treatment over
`0 → 90` — see §7 decision 6, now closed.

**Claim flags.**
- `OBSERVATION` → `CLAIM`, and the claim is the weak one: one projection is insufficient. Do not overreach into "therefore we need all of them" yet; C05 has to earn that.
- Verified in `facts.py` — `score(x) = 17.095`, `score(y) = 0.046`, and both x and y coordinates at unit standard deviation.
- Verified in `facts.py` — half the half turn (50° to 140°) scores below `BAND_LEVEL = 0.5`, on a uniform angle grid, which is what makes the spoken "half of every direction in this plane" a checked number rather than an impression.

<details>
<summary>Superseded narration draft (kept as design history)</summary>

> <bookmark mark='clumps'/>Give the cloud some structure — two clumps, well separated.
>
> <bookmark mark='rotate'/>Turn the direction, and the shadow turns with it. Along one axis the clumps pull apart and the score climbs. <bookmark mark='innocent'/>A quarter turn later they sit on top of each other, and the shadow passes for a bell.
>
> The cloud never changed. So a small score along one direction is evidence about that direction, and nothing more.

</details>

<details>
<summary>Superseded delivered narration, 183 words (rewritten 2026-08-17 on owner review)</summary>

The owner's gripes: unclear and slightly redundant explanations, missing
conversational connectors, weak ending. Banned outright — "and it should",
"if we", "the cloud stays the same".

> Suppose the cloud has some structure. Two clumps, pulled well apart, and the same embeddings we have had all along.
>
> Now take the direction those clumps separate along. Every embedding still lands somewhere on the line, but the shadow comes out as two piles with a hole between them, and a standard Gaussian has no hole in the middle. So the score climbs, and it should.
>
> Turn the direction a quarter of the way round. The cloud is not moving, only the line we are reading it along. The two piles slide straight through each other, and what is left is a single hump, close enough to a bell that the score drops to almost nothing.
>
> Keep turning and the hole opens again. Every direction in this plane has its own score, and a half turn covers all of them.
>
> The cloud never changed. There is a wide band of directions where it passes, so a batch checked along any one of them would look fine. A small score is evidence about the direction we picked, and nothing about the cloud behind it.

</details>

---

### C05 — Both coordinates Gaussian, and every point on a line
*(handoff Scene E · **owner-review draft 2026-08-20, 0:45** · density: medium — one counterexample, one lesson)*

**Current authority — 2026-08-20 owner-review rework.** This scene keeps its
load-bearing inference and removes the repeated explanation around it: **two
coordinate-wise Gaussian checks do not establish that the whole
representation is Gaussian.** The cloud `Z=(X,X)` is visible from the first
frame as a diagonal line. One projection apparatus then survives the whole
experiment; no target curve, direction line, shadow batch, or score panel is
swapped for an independently created replacement.

| Beat | Visible argument | What the viewer should infer |
|---|---|---|
| 1 | The diagonal cloud is already visible while C04's limitation leads to the two coordinate axes. | Checking the horizontal and vertical directions is the natural shortcut after one direction failed. |
| 2 | Representative dashed guides drop points perpendicularly onto the actual x-axis. The literal feet then spread into a readable dot plot under one amber `N(0,1)` curve; `score(x)=0.244` appears. | “Score the x-coordinates” means project the cloud onto its horizontal axis, then apply the scalar score to those projected values. |
| 3 | The same direction line, arrow, shadow dots and amber curve rotate continuously onto the y-axis. `score(y)=0.244` joins the first result. | Because `y` copies `x`, the second coordinate produces the same scalar batch and the same low score. |
| 4 | The apparatus turns only 45° farther, toward `y-x`. The dot plot contracts to one literal point at the origin while `score(u)=81.785` appears; then the testing apparatus clears back to the bare line cloud. | The axes never compared the two coordinates. A mixed direction exposes the dependence, so testing must extend beyond the axes. |

The current draft narration is 133 spoken words and the low-quality render is
45.20 seconds. It uses three continuous spoken passages and bookmark-locks the
x projection, dot-plot stack, y turn, mixed turn, zero contraction and verdict
to the phrases that motivate them. The previous `x+y` wide-shadow example was
cut: it was mathematically correct but did not add a necessary inference once
the `y-x` collapse had exposed the missed dependence. The source and
`SCRIPT_chapterC.md` are the authority for this review draft. It has **not**
received an owner-authorized ElevenLabs/1080p delivery; the 60.97-second file
documents the superseded cut.

**Superseded 2026-08-18 production record.** The notes below describe the
previous strip-and-merge cut; they are retained for provenance and reusable
implementation lessons only. Where they conflict with the current rework,
the source and `SCRIPT_chapterC.md` win.

The four-step reveal survived intact. Nine things were decided during implementation:

1. **It is a `ThreeDScene` whose camera never moves,** locked at `phi=0, theta=-90°` — the orientation an ordinary 2-D `Scene` already has. That buys `CloudRig` and `TurningProjection` unchanged, both of which are written against a 3-D scene's fixed-orientation registry, on a scene that is honestly flat. C04 spent this chapter's one purposeful camera move; §8 does not give C05 another.
2. **`data.diagonal_2d` now standardizes `X`.** This is not tidying. `u^T Z = (u₁ + u₂) X` depends on the direction *only* through the scale `|u₁ + u₂|`, so an unstandardized `X` — this seed's raw draw has sample mean 0.043, sd 1.021 — puts the best-fitting scale slightly off 1 and moves the score's two minima **off the axes**, to 1° and 89°. The scene's closing claim would then be false of the picture it is read from. Standardizing pins the minima to the axes by construction. It also makes the ledger's word *exactly* ("both marginals are exactly standard normal") true of the 200 points on screen rather than of the population they came from.
3. **The two marginals are world-coordinate dot plots, not fixed-frame ones,** so the merge is a straight interpolation in the same coordinate system the cloud lives in and every dot lands exactly on the point it belongs to. The horizontal strip sits below the plane's region and the vertical strip to its left — the marginal-scatter layout — because a *diagonal* cloud reaches as far in `y` as its own `x` marginal reaches in `x`, so the strips have to sit outside the square rather than beside it. That in turn set `SCALE = 0.78`.
4. **The merge is 200 pairs converging,** each pair as one `AnimationGroup` inside a `LaggedStart` at `lag_ratio=0.0018`, so no dot is ever seen waiting for its partner. The arrived strip dots sit exactly on the `CloudRig`'s own dots, same radius and colour, so ownership changes hands invisibly and the instances that carry the updater are the ones every later beat projects.
5. **Two static scores, not one meter, in beats 1–2.** `score(x)` beside the horizontal strip, `score(y)` beside the vertical one, both reading `0.244`. A single shared meter could not hold both on screen at once, and the storyboard's deliberate hold wants exactly that. C04's live `score(u)` meter arrives later, when there is a direction to be live about, and its first reading is the same 0.244.
6. **C04's silent-Gaussian rule, applied twice.** A `TARGET` normal is stretched to each strip's own extent and laid over it — a fair overlay, since a dot plot's pile height is the density up to one constant. Never named, never labelled, and both fade in the silence after the hold, once both comparisons have been made.
7. **The score-vs-angle panel sits a unit further right than C04's** (screen `x = 3.55` rather than `2.60`). Draft frames showed that at C04's position the plane's `x` label, in the half-unit gap between the two panels, read as the *trace panel's* axis label. C05's world is narrower than C04's and can afford the shift.
8. **The shadow's dot plot is capped at 15 levels** (`TurningProjection.stack_max_level`, new). At 135° every value is zero, so an uncapped dot plot gives each of 200 samples its own level and builds a column straight off the top of the frame. Capping folds the excess into the top, and a point mass draws as a short dense knot at the pile's own established maximum height.
9. **The apparatus leaves on the closing line.** At a half turn the projection line lies exactly along the `x` axis and hides it, so lighting the two axes green would light up an axis nobody can see — and a scene whose verdict is about the whole *set* of directions should not end with one of them still picked out. Arrow, line and shadow fade; the completed trace is the record of the turn.
10. **The wide-diagonal claim now carries its own reference.** When the narration says that the 45° shadow is still bell-shaped but no longer standard, a compact amber `N(0,1)` curve appears in that shadow's rotating coordinates. Its narrower horizontal span makes the scale mismatch visible; it leaves before the anti-diagonal collapse, where a bell would compete with the point-mass picture.

**The superseded narration was 178 spoken words**, in seven blocks. It was
rewritten once on owner review — the first cut ran 126 words and 0:43, and the
note was that the intro and the explanations were confusing: *"What does check
the coordinates mean? this chapter doesn't make sense we just do stuff and
don't naturally explore."* Those defects motivated the later structural
rework recorded above.

1. **"Check the coordinates" was an instruction the viewer could not follow.** It was spoken over two dot strips, with no cloud and no vector on screen — so "coordinate" had no referent, and naming it would not have fixed that, because it is exactly the kind of word that feels understood while staying vague. The fix is visual and it is now the scene's first object: `z = (x, y)`, and the two slots physically leave it to become the two strips. The glyphs `x` and `y` are the same instances throughout — a slot of the embedding, then a strip's label, then an axis of the plane — so the merge in beat 3 reads as undoing the split rather than as a new trick.
2. **The scene never said that a coordinate IS a direction.** This is the deeper one. Without it, beats 1–3 (coordinates) and beats 5–7 (directions) are two unrelated activities, and the closing line lands on nothing, because the viewer was never told that the two things checked at the start were directions at all. The narration now makes it the spine: *"every embedding already comes with two directions we never had to choose: its own coordinates."* That single clause defines the term, states why the coordinates are the appealing thing to reach for — they feel canonical, like they are not a choice — and sets up the closing line, which now comes back to the same phrase: *"the two we never had to choose were both of them."*

The beat order was also changed so each beat answers the previous one rather than following it. C04 ends "a low score tells you about the direction you picked"; the move that follows is *use more than one*, and then *which ones* — not "check the coordinates" out of nowhere. And the reveal beat now spends its words on the part no picture can carry: the two `0.244`s stay on screen beside a cloud that is a line, so the contradiction is visible and the narration is free to explain *why a coordinate check could never have caught it* — a marginal is a statement about one slot on its own, and dependence lives between slots, where neither of them is looking. It follows C04's rules: every beat opens on a connector (*So / Now / Then / And / Keep*), none of the three banned phrases appears, and nothing is said that the animation already shows — "every sample landed on the diagonal" was cut and only its *reason* kept, because the merge is that sentence. Two lines carry content the picture cannot: "the same number exactly", which plants the secret in beat 1 and pays it off ten seconds later, and "the right shape, at the wrong scale", which forecloses the wrong reading that every off-axis projection is non-Gaussian. It ends on the two marked minima and the line **"And the two we checked were both of them."**

---

**Historical pre-rework plan — superseded.** The design below described the
former marginal-strip opening. It is retained for provenance only; do not use
it as implementation authority.

| Step | Screen | Sound |
|---|---|---|
| **0. setup** | Two dot strips: a horizontal one carrying the `x`-coordinates of 200 samples, a vertical one carrying the `y`-coordinates. No 2-D plane. No joint cloud. Each dot in the horizontal strip is index-linked to its partner in the vertical strip. | "Two coordinates, each measured on its own." |
| **1. horizontal shadow** | The horizontal strip runs through the `𝒯` meter. Score lands near zero, in `DIRECTION` green. | "The first scores near zero." |
| **2. vertical shadow** | The vertical strip runs through the same meter. Same result. | "So does the second. Both look like standard Gaussians." |
| — | **Deliberate hold.** `inspect(1.2)`, silent. Two near-zero scores sitting on screen. | — |
| **3. pull back** | `NumberPlane` fades in. Then, for each `i`, the horizontal dot and the vertical dot **merge into one 2-D dot** at `(x_i, y_i)` — `ReplacementTransform` per pair, in a fast `LaggedStart`. They land on the diagonal. | *silence through the merge*, then nothing for ~1.5 s |
| — | **Deliberate hold.** The line is on screen and unnamed. Handoff: "Let the viewer notice the line before stating the conclusion." | — |
| **4. rotate off-axis** | The `DIRECTION` arrow, which has been sitting on the horizontal axis since step 1, sweeps through a half turn. The shadow, the meter and the score-vs-angle trace follow. Two coordinate angles are marked on the trace — the only two places the score is small. | see below |

**Narration.**

> Two coordinates, each measured on its own. <bookmark mark='first'/>The first scores near zero. <bookmark mark='second'/>So does the second. Both look like standard Gaussians.
>
> <bookmark mark='lift'/>Now put each pair back together, at its own point in the plane.
>
> *(silence, ~2 s)*
>
> Every sample landed on the diagonal, because the second coordinate was a copy of the first. <bookmark mark='rotate'/>Turn the direction off the axes and the shadow stops being Gaussian. Along one diagonal it's spread too wide. <bookmark mark='collapse'/>Along the other, every point falls in the same place.
>
> So the two coordinates being Gaussian says nothing about how they move together. <bookmark mark='marks'/>Out of every direction there is, exactly two make this cloud look right.

**Why this works mathematically** (and must be verified in `facts.py`): for `Z = (X, X)`, `u^T Z = (u₁ + u₂) X`. On the coordinate axes that is `X ~ N(0,1)` and the score is at the sampling-noise floor. On the diagonal it is `√2·X ~ N(0,2)` — Gaussian but the wrong scale, so the score is large. On the **anti**-diagonal it is identically `0` — every point on top of every other, which is Chapter B's `data.collapsed_1d` picture exactly. The anti-diagonal is the dramatic beat and should land last.

**Persistent objects.**

| | |
|---|---|
| Enters | the two marginal strips (400 dots, index-paired), the `𝒯` meter carried in from C04 |
| Transforms | strips → 200 plane dots via per-pair merge; the direction arrow sweeps; the score-vs-angle trace draws |
| Remains | the plane dots, the arrow, the meter, the trace with its two marked minima |
| Exits | everything at the cut — C06 is a genuine reset to a different cloud |

**Reuse vs new.** Reuses `data.diagonal_2d` (already in the repo, documented for this exact purpose, `n=200`), `CloudProjectionRig`, the score-vs-angle trace, `common/score.py`. New: the marginal-strip pair and the merge choreography — scene-local, one-off.

**Claim flags.**
- `exact_derivation` — `Z = (X, X)` has both marginals exactly `N(0,1)` and covariance eigenvalues `(2, 0)`. Not an empirical accident; state it as construction.
- `CLAIM` — "a vector with Gaussian marginals need not be jointly Gaussian." This is the handoff §7 required counterexample and it must appear **before** Cramér–Wold is named. C06 must not run first.
- **Axis-range risk.** The anti-diagonal score is finite but large (`N · ∫ w |1 − e^{−t²/2}|² dt`, order 10¹–10² at `N = 200`) against a Gaussian batch's ~0.03. The score-vs-angle plot needs a decided vertical treatment. See §7, decision 6.

---

### C06 — Every direction, and the same target in each
*(handoff Scene F · ~1:30 · density: high — theorem qualification lives here)*

**Causal beat.**
Inherited: no finite set of chosen directions is safe.
Experiment: start from the cloud we actually want — independent standard Gaussian coordinates — and turn `u` anywhere at all.
Observation: the shadow keeps the same bell and the amber target curve never moves.
Conclusion (shown): if the cloud is `N(0, I_D)`, every unit projection is `N(0,1)`, so one target serves every direction.
Conclusion (cited): the converse. Cramér–Wold, with Chapter B's uniqueness theorem.
Handed on: "every direction" is a sphere, and a computer cannot visit a sphere.

**Narration.**

> Then the test has to be every direction at once.
>
> <bookmark mark='isotropic'/>Start from the cloud we actually want — coordinates that are independent standard Gaussians — and turn the direction anywhere you like. <bookmark mark='fixed'/>The shadow keeps the same bell, and the target curve never moves. So a single target serves every direction, which is what makes the scores comparable at all.
>
> <bookmark mark='theorem'/>The converse is a theorem, and we're citing it rather than proving it. If every one-dimensional projection of a distribution is a standard Gaussian, then the distribution itself is the standard Gaussian in D dimensions. That's Cramer Wold, together with the uniqueness result from Chapter B.

**Persistent objects.**

| | |
|---|---|
| Enters | the isotropic cloud (the C01/C02/C03 cloud, restored — same dot instances, ideally same seed), the `DIRECTION` arrow, the compact rig showing the empirical curve against the fixed amber target |
| Transforms | the direction sweeps continuously; the `CLOUD` curve wiggles inside sampling noise; the `TARGET` curve is drawn once and held rigid — the invariant is the point |
| Remains | the amber target curve, which will still be the target in C07, C08, C09 |
| Exits | the theorem card, after its hold |

**The theorem card.** Two lines, plainly separated:

```
 shown        Z ~ N(0, I_D)          ⟹  u^T Z ~ N(0,1)  for every unit u
 cited        u^T Z ~ N(0,1) ∀u      ⟹  Z ~ N(0, I_D)          Cramér–Wold
```

The cited line gets a visible marker — a small `MUTED` "theorem, not proved here" label, matching how `b08` handled Fourier uniqueness. `SOURCE_MAP.md` §6e: "This must never be narrated with 'therefore' or 'we have shown'." The narration above says "we're citing it rather than proving it" explicitly.

**Reuse vs new.** Reuses the C01 cloud, `CloudProjectionRig`, `layout.gaussian_frequency_curve` / the rig's target curve, `b08`'s theorem-card visual grammar. New: the theorem card's two-line split.

**Claim flags.**
- `theorem_statement` — Cramér–Wold. Cited. Never "therefore."
- `exact_derivation` — the forward direction. This one *is* elementary and the rotation demonstrates it; it may be narrated as a fact.
- Do not let the sweep imply the converse has been checked. The narration must own the asymmetry, and it does.

---

### C07 — `M` sampled directions
*(handoff Scene G · ~1:50 · density: medium)*

**Causal beat.**
Inherited: the test needs every direction.
Experiment: draw a direction the only unbiased way available — a Gaussian vector, divided by its length — and score its shadow. Then another. Then many.
Observation: the individual scores scatter; their average steadies as more are drawn.
Conclusion: replace the expectation over directions with an average over `M` sampled ones. `M` is introduced here and nowhere earlier.
Handed on: each of those scores is still an integral over every frequency.

**Narration.**

> Every direction is a whole sphere of them, and a computer can't visit a sphere. <bookmark mark='draw'/>It can draw one: take a Gaussian vector and divide by its length, and you land somewhere on the sphere with no direction favoured.
>
> <bookmark mark='first'/>Each one gives a shadow and a score. <bookmark mark='second'/>Here's another, and it disagrees with the first, because the two directions see different things.
>
> <bookmark mark='many'/>Draw M of them and average. <bookmark mark='M'/>More directions steady that average. They don't turn a finite batch into a proof.

**Choreography.** Translated from `_2017/nn/part3.py::ConstructGradientFromAllTrainingExamples` (show two → show all → average together → collapse into one vector) and paced like `CHAPTER_B_REVIEW_GUIDE.md` pattern 2 (fixed pulse per trial).

| Stage | Screen |
|---|---|
| 1 | One Gaussian vector appears *inside* the cloud, then snaps outward to unit length on a faint sphere. ~1.2 s, settled. |
| 2 | Its shadow and score `𝒯₁` in `DIRECTION` green. Settled. |
| 3 | A second direction, same rhythm, different score `𝒯₂`. Settled. |
| 4 | ~30 more at ~0.15 s each in a `LaggedStart` fan, each dropping its score into a growing right-hand column. |
| 5 | The column collapses into one `AVERAGE` purple number. |
| 6 | `M` is written for the first time, beside the column, as the count of rows. |

**Persistent objects.**

| | |
|---|---|
| Enters | the isotropic cloud from C06, the faint unit sphere, the score column |
| Transforms | direction arrows accumulate and dim as new ones arrive (bright = active, per handoff §12 "keep the active vector brighter while surrounding structure recedes") |
| Remains | the purple averaged score, the visible fan of directions, `M` |
| Exits | the individual score rows, absorbed into the average |

**Reuse vs new.** Reuses `CloudProjectionRig`, `common/score.py`, the `AVERAGE` colour convention from Chapter B. New: the direction-sampling animation and the score column. Both scene-local — do not build a framework for the fan.

**Claim flags.**
- `SOURCE_MAP.md` §8, verbatim: `u ~ N(0, I_D)`, then `u ← u/‖u‖`. Show it; it is one visual and one clause.
- `QUALIFICATION`, required — increasing `M` reduces Monte Carlo variation and does not make a finite batch a proof. Handoff §7 lists this explicitly.
- Do **not** state `1/√M` here. `SOURCE_MAP.md` §7 defers it to C10 as a limitation, not a derivation.
- Typical `M` is 32–1024 (`SOURCE_MAP.md` §8). Say it once if at all; it is engineering.

---

### C08 — `K` frequency knots
*(handoff Scene H · ~1:20 · density: medium)*

**Causal beat.**
Inherited: `M` scores, each of which is an integral.
Experiment: return to one scalar score — literally B11's weighted squared-gap area — and evaluate the integrand at finitely many frequencies instead.
Observation: at `K = 16` the finite sum already tracks a much denser reference.
Conclusion: replace each integral with `K` knots. `K` is introduced here and nowhere earlier.
Handed on: both approximations are in place; assemble.

**Narration.**

> One of those scores is still an integral over every frequency, and a computer can't visit those either. <bookmark mark='knots'/>Evaluate the integrand at K frequencies inside the window from Chapter B, and add up what you find.
>
> <bookmark mark='eight'/>Eight knots already follow the shape. <bookmark mark='sixteen'/>Sixteen tracks a far denser reference to within a hundredth of a percent, on this batch. The error falls like one over K squared, so there's not much left to gain.

**Persistent objects.**

| | |
|---|---|
| Enters | B11's weighted squared-gap picture, reconstructed — `gap_axes`, the `COLLAPSE` curve, the filled area, the amber `w_λ(t)` taper. This is a literal object return, and reconstructing it identically is the whole point of the scene's opening. |
| Transforms | `K = 8` knots drop onto the `t` axis as `TARGET` ticks with their sampled values; then `K = 16`; the finite sum's value ticks against the dense reference |
| Remains | `K`, and the discretized score expression |
| Exits | the gap axes at the cut |

**Boundaries.** Handoff Scene H: do not reopen the hard-bounds-versus-smooth-weights debate from Chapter B. The `[0.2, 4]` window and the Gaussian taper `w_λ(t) = e^{−t²/(2λ²)}` are settled inputs; the knots go inside them without comment. Trapezoidal weights `α_k` stay deferred (`SOURCE_MAP.md` §7) — the insight is finite evaluation, not quadrature mechanics.

**Reuse vs new.** Reuses `common/fingerprint.py::CharacteristicFunctionPlot`, `layout.frequency_axes` / `frequency_window`, `b11`'s gap-area geometry, `common/score.py`. New: the knot markers and the running finite sum.

**Claim flags.**
- **`K = 16` → 0.01% error vs `K = 2000`; `K = 8` → 0.04%; `O(1/K²)`.** `SOURCE_MAP.md` §8 records these as source facts. Handoff §7 states they "may be shown only with the exact experimental setup/source recorded in `SOURCE_MAP.md`." The current `SOURCE_MAP.md` entry records the numbers but **not** the batch, `λ`, or window they were measured on. Two acceptable resolutions, and one of them must happen before this scene renders: either (a) `facts.py` recomputes the error on the batch actually shown and the narration says "on this batch", or (b) the narration attributes the figure to the source and the on-screen demo shows only qualitative agreement. Draft above assumes (a). See §7, decision 5.

---

### C09 — Assembling SIGReg
*(handoff Scene I · ~1:30 · density: low — every symbol arrives beside its object)*

**Causal beat.**
Inherited: two finite approximations, both motivated.
Experiment: write down what has been happening.
Observation: each symbol already has a picture attached.
Conclusion: `SIGReg(Z) = (1/M) Σₘ 𝒯(u⁽ᵐ⁾ᵀ Z; λ)`.
Handed on: what does it do, and what does it promise?

**Narration.**

> Every piece of this is already on screen. <bookmark mark='project'/>The projection u transpose z turns the batch into numbers. <bookmark mark='score'/>𝒯 scores those numbers against the standard Gaussian, using K knots inside the weighted window. <bookmark mark='average'/>And the average over M directions is the whole regularizer.

**Build order — matched to `SOURCE_MAP.md` §8's verbatim form.**

| Step | Symbol | Arrives from |
|---|---|---|
| 1 | `u^{(m)T} z_i` | `TransformFromCopy` off the projection arrow and one shadow dot, still on screen from C07 |
| 2 | `𝒯( · ; λ)` wraps it | `TransformFromCopy` off the compact score meter |
| 3 | `(1/M) Σ_{m=1}^{M}` wraps that | the purple score column from C07 collapsing again |
| 4 | held | `SIGReg(Z) = (1/M) Σ_{m=1}^{M} 𝒯(u^{(m)T} Z; λ)` |

Optionally, `𝒯` expands once into its `K`-knot sum and collapses back — so the final line stays the source's one-line form while the viewer has seen what is inside it. `TransformMatchingTex` with the symbols isolated at construction (`ty.maths(..., isolate=[...])`).

**Persistent objects.**

| | |
|---|---|
| Enters | the C07 frame — cloud, direction fan, score column — held from the previous cut |
| Transforms | visible objects become formula terms; nothing new is created that has not been on screen |
| Remains | the assembled formula |
| Exits | the cloud and fan, dimmed under the formula, restored in C10 |

**Reuse vs new.** Reuses everything. New: nothing structural. `ANIMATION_PLAYBOOK` Pattern 7 covers the mechanics.

**Claim flags.**
- The formula must match `SOURCE_MAP.md` §8 exactly, including `λ`. `b11` shipped a defect of this exact shape (`𝒯` displayed without its `N` prefactor while being named the Epps–Pulley statistic). Check the rendered TeX character by character against §8.
- No new claim is made here. If a sentence in this scene asserts something, it is in the wrong scene.

---

### C10 — What the loss opposes, and what it promises
*(handoff Scene J · ~2:00 · density: high — this is the project's highest-risk scene)*

**Causal beat.**
Inherited: the assembled loss.
Experiment: score the shapes from C02.
Observation: the rod scores high, the round cloud low.
Conclusion (population): zero exactly when the cloud is `N(0, I_D)`.
Conclusion (finite): what we compute is an estimator, and the guarantee is about the global minimum.
Handed on: calibration.

**Narration.**

> <bookmark mark='shapes'/>Run it on the shapes from earlier. <bookmark mark='rod'/>The rod scores high, because almost every direction sees a distribution with hardly any spread in it. <bookmark mark='ball'/>The round cloud scores low. That's what this loss pushes against.
>
> <bookmark mark='chain'/>At the population level the statement is exact. The score is zero precisely when every projection is a standard Gaussian, and by Cramer Wold, that happens precisely when the cloud is the standard Gaussian in D dimensions.
>
> What we actually compute is an estimator of that. <bookmark mark='N'/>N samples leave a positive score even for a perfectly Gaussian batch. <bookmark mark='M'/>M directions leave sampling noise in the average, falling like one over the square root of M. <bookmark mark='K'/>K knots leave quadrature error.
>
> <bookmark mark='global'/>And the population result describes the global minimum. It says nothing about local minima, and nothing about whether gradient descent reaches the minimum at all.
>
> So what's left is calibration — for a given N, M and K, deciding how small the score has to be before a batch counts as Gaussian.

**Persistent objects.**

| | |
|---|---|
| Enters | the C02 cloud rig, restored, with the primary readout now the `AVERAGE` SIGReg score and the eigenvalue triple demoted to a `MUTED` caption |
| Transforms | one shape tracker walks rod → pancake → ball while the score falls; then the equivalence chain writes; then the three finite-parameter cards |
| Remains | the honest-scope statement as the last thing standing |
| Exits | everything at `clear_beat()` |

**The equivalence chain extends B11's, literally.** `b11` ends holding:

```
𝒯_pop = 0  ⟹  φ_X(t) = φ_0(t) ∀t  ⟹  X ~ N(0,1)
```

C10 writes the vector version in the same shape and same colours (`TARGET` implication arrows, `INK` terms), so it reads as the same sentence grown a dimension:

```
SIGReg_pop(Z) = 0  ⟺  u^T Z ~ N(0,1) ∀u  ⟺  Z ~ N(0, I_D)
```

That is `SOURCE_MAP.md` §6g verbatim.

**The single highest-risk moment in the project.** `PLAN.md` §5 marks it: "C.8 shows gradient descent opening a collapsed cloud. The source guarantees the global minimum only." Three concrete safeguards:

1. **The rod → ball morph is driven by a shape tracker, not framed as a training run.** No step counter, no epoch label, no loss-descending-over-time plot. The morph is a sweep through configurations, and the narration says "run it on the shapes from earlier" — a scoring pass, not an optimisation.
2. **The global-minimum sentence is spoken while the equivalence chain is on screen and nothing is moving.** Its own beat, with `inspect()` around it.
3. `facts.py` asserts the displayed scores against `common/score.py` on the exact shapes shown.

**Optional 8-second beat, cut first if runtime is tight:** `data.ring_2d` — a cloud with the same mean and covariance as a standard Gaussian that is plainly not Gaussian, and that SIGReg still rejects. It forecloses the "this is just a covariance penalty" reading. The data already exists. See §7, decision 7.

**Reuse vs new.** Reuses `common/cloud.py`, `common/score.py`, `b11`'s equivalence-chain typography. New: the three finite-parameter cards.

**Claim flags — the densest set in the chapter.**
- `theorem_statement` — the equivalence chain, `SOURCE_MAP.md` §6g.
- `source-stated limitation` — the `1/N` noise floor: "With finite `N`, even perfectly-Gaussian samples yield `SIGReg(Z) > 0` at order `1/N`" (§6f). `b09` already verified this empirically for the scalar case; C10 states it, does not re-verify.
- `stated, not derived` — `1/√M` (`SOURCE_MAP.md` §7).
- **`FORBIDDEN`** — any inference about convergence rate, optimization dynamics, uniqueness of parameters, or absence of local minima. Handoff §7, final bullet.
- The closing question is calibration, which follows from the three finite parameters just named. It is not a chapter announcement.

---

## 5. Transition contracts

Handoff §9 requires all five fields per boundary. Audio: every scene opens and closes with ~120 ms of held silence inside the first and last `voiceover` block so `ffmpeg -c copy` concatenation cannot clip a phoneme. `build.sh` performs a raw stream concat with no crossfade capability (`VISUAL_SYSTEM.md` §7), so a cut is a cut.

| Boundary | Last spoken | Last visible | First spoken | First visible | Persist / transform / disappear |
|---|---|---|---|---|---|
| **B11 → C01** | "…the same thing with a whole batch of vectors." | vector columns, amber `?`, `𝒯 ∈ ℝ` | "In the last chapter, we built the Epps-Pulley statistic…" | the Epps–Pulley equation | **Deliberate recap cut.** C01 compresses Chapter B to the equation it earned, then immediately reconnects it to encoder outputs. |
| **C01 → C02** | "Suppose we want it to follow a standard Gaussian in D dimensions." | centred 3-D cloud, `Z`, and the target label | "Suppose the cloud starts losing its spread." | the same cloud geometry | Cloud and axes persist in content; C02 begins manipulating the object C01 just named, then motivates why this target and a trainable loss are needed. |
| **C02 → C03** | "…the loss has to compare distributions rather than assign partners." | the round cloud, restored | "Choose a unit direction u." | the same cloud | Cloud persists. Pairing arrows and partner dots are gone before the cut. |
| **C03 → C04** *(built)* | "…but it cannot tell us whether the whole cloud does." | cloud at `phi=76°, theta=12°`, `u_3` arrow, its line, its 220 shadow feet, `score(u_3)=0.872` | "Now suppose the cloud has structure." | **the identical frame**, rebuilt from the same `CloudRig` and a `CloudProjectionRig` on `u=(0,1,0)` | Cloud persists. C03's arrow, line, shadow and score fade out on the first beat before the cloud changes, so the beat has one focal event; the rig itself was already gone (C03 phase 9). |
| **C04 → C05** *(built)* | "…It tells you nothing about the cloud behind it." | two-clump cloud, direction arrow, score-vs-angle trace | "One direction was not enough." | coordinate axes pulse, then the diagonal `y=x` cloud appears | **Genuine reset.** No testing apparatus persists, but "So" carries the argument across the cut: once one direction is insufficient, the coordinate axes are the natural next shortcut. |
| **C05 → C06** | "…test directions that mix the coordinates." | bare diagonal cloud on a plane, labelled `y=x` | "Then the test has to be every direction at once." | the isotropic cloud | Reset. "Then" carries the causal link; C05 leaves no direction, shadow, or target on screen, so C06 opens cleanly on the broader turn. |
| **C06 → C07** | "…together with the uniqueness result from Chapter B." | theorem card over the isotropic cloud | "Every direction is a whole sphere of them…" | the same cloud, card gone | Cloud persists; the theorem card exits during C06's own final beat, not at the cut. |
| **C07 → C08** | "They don't turn a finite batch into a proof." | cloud, direction fan, purple average | "One of those scores is still an integral…" | B11's gap axes and weighted area | Deliberate object return to Chapter B's picture. Hard cut. |
| **C08 → C09** | "…not much left to gain." | knots on the gap axes, `K` | "Every piece of this is already on screen." | the C07 frame restored | Hard cut back to the cloud and fan. Justified: C09 assembles from *visible* objects, so they must be visible. |
| **C09 → C10** | "…the average over M directions is the whole regularizer." | the SIGReg formula | "Run it on the shapes from earlier." | formula pinned small, C02's cloud rig entering | Formula persists, demoted to a corner. Cloud rig returns. |
| **C10 → end** | "…how small the score has to be before a batch counts as Gaussian." | the honest-scope statement | — | — | `clear_beat()`. |

---

## 6. Consolidated claim ledger

Every mathematical statement in Chapter C, with its status. This is the table `facts.py` and the narration audit check against.

| # | Claim | Scene | Status |
|---|---|---|---|
| 1 | `D = 3` on screen is a display choice; nothing depends on it | C01 | `QUALIFICATION` — say once |
| 2 | The displayed shape tracker has ranks `3→2→1→0`; rank zero is the collapsed endpoint | C02 | exact construction; motivation deferred to Chapter A |
| 2a | In LeJEPA's downstream-task setup, the isotropic Gaussian minimizes worst-case prediction error | C02 | `source_statement`, cited rather than proved |
| 3 | `E‖z − z*‖² = ‖z‖² + D` for `z* ~ N(0, I_D)`; expected pull is `2z`; the expectation is over a continuum independent of batch size, and the closed form uses known moments rather than a Gaussian-only trick | C02 | `exact_derivation`, verify in `facts.py` |
| 4 | Nothing about the optimization trajectory of the pairing loss | C02 | **FORBIDDEN** |
| 5 | `u^T z_i` for a unit `u` is an ordinary scalar batch | C03 | definition |
| 6 | A small `𝒯(u)` is evidence about `u` alone | C03, C04 | `CLAIM`, earned by C04 |
| 6a | On `data.clumped_3d()`, `score(x) = 17.095` and `score(y) = 0.046`, with both coordinates at unit variance | C04 | `exact_computation`, verified in `facts.py` |
| 6b | On `data.clumped_3d()`, half of every direction in the turning plane (50°–140°) scores below 0.5 | C04 | `exact_computation`, verified in `facts.py` |
| 7 | `Z = (X, X)` has both marginals exactly `N(0,1)`, covariance eigenvalues `(2, 0)` | C05 | `exact_derivation`, verified in `facts.py` — *exactly* is why `data.diagonal_2d` standardizes |
| 7a | On `data.diagonal_2d()`, `score(x) = score(y) = 0.244`, `10.284` at 45°, `81.785` at 135°; the directions scoring below 1.0 are exactly two arcs, one around each axis | C05 | `exact_computation`, verified in `facts.py` |
| 8 | Gaussian marginals do not imply joint Gaussianity | C05 | `CLAIM`, proved by construction |
| 9 | `Z ~ N(0, I_D) ⟹ u^T Z ~ N(0,1)` for every unit `u` | C06 | `exact_derivation`, demonstrated |
| 10 | Every one-dimensional projection standard Gaussian ⟹ joint is `N(0, I_D)` | C06 | **`theorem_statement`** — Cramér–Wold, cited, never "therefore" |
| 11 | `u ~ N(0, I_D)`, `u ← u/‖u‖` is uniform on the sphere | C07 | `SOURCE_MAP.md` §8 |
| 12 | Larger `M` reduces Monte Carlo variation, not finite-batch uncertainty | C07 | `QUALIFICATION`, required |
| 13 | `K = 16` → 0.01% vs `K = 2000`; `K = 8` → 0.04%; `O(1/K²)` | C08 | source fact — **provenance unresolved, see §7.5** |
| 14 | `SIGReg(Z) = (1/M) Σₘ 𝒯(u⁽ᵐ⁾ᵀ Z; λ)` | C09 | `SOURCE_MAP.md` §8, verbatim |
| 15 | Collapsed and low-rank clouds receive a high score | C10 | `empirical evidence, this run` — never "guarantee" |
| 16 | `SIGReg_pop = 0 ⟺ u^T Z ~ N(0,1) ∀u ⟺ Z ~ N(0, I_D)` | C10 | `theorem_statement`, `SOURCE_MAP.md` §6g |
| 17 | Finite `N` leaves a positive score at order `1/N` | C10 | source-stated limitation, §6f |
| 18 | Estimator variance `~1/√M` | C10 | stated, not derived (§7) |
| 19 | Nothing about convergence rate, local minima, dynamics, or parameter uniqueness | C10 | **FORBIDDEN**, `PLAN.md` §5's flagged highest risk |

---

## 7. Open decisions requiring the owner's sign-off

**All 11 decisions below were reviewed and approved 2026-08-11 — every recommended option was accepted as-is.** Kept in full for the reasoning; implementation should proceed per §8.

Each states the conflict, the recommendation, and the cost of getting it wrong.

**1. Scene count and the `PLAN.md` C.1 conflict.**
`PLAN.md` §5 lists Chapter C item 1 as "the cheating world model" — a loss meter hitting zero while an information meter drops to zero. The handoff's Scene A is "why vectors change the problem," and §4's protected arc contains no such beat. Ten scenes as laid out above absorbs C.1's *content* into C02 (the point-collapse rung) and C10 (what the loss opposes) rather than giving it its own opening scene.
**Recommendation:** adopt the handoff's ten scenes. Rationale: an opening scene about prediction losses would break the B11 seam, which is the strongest continuity the project has, and would introduce training machinery the viewer has never been shown.
**Cost if wrong:** the chapter opens on a cloud that no one has been told why they want.

**2. Where the "why regularize at all" motivation lives. — superseded
2026-08-14.**
The owner assigned the direct representation-collapse explanation to Chapter A.
C02 now uses the short rank ladder only, ending with one clause that names rank
zero as collapse. It does not show a constant network, prediction loss, or the
zero-information argument. The recovered time belongs to the Gaussian target,
the changing direction, and the pointwise expectation.

**3. Rebuild versus reuse of `c02_covariance.py`'s mesh-update code.**
**Recommendation:** rebuild as `common/cloud.py::CloudRig`, preserving the three technical decisions and their explanatory comments verbatim, and changing the five items in §3.
**Also unresolved:** was the prototype ever reviewed on a rendered frame? Its docstring calls 3-D "the second risky bet," and `RENDER_REVIEW.md` should be checked for a verdict before two scenes are built on it. If it has not been reviewed, do that first — a 480p draft of the ladder is cheap and it gates C02, C03, C04, C07 and C10.
**Cost if wrong:** five scenes built on unverified 3-D readability.

**4. Hard cut versus match cut at B11 → C01, and promoting `_vector_bridge`.**
`VISUAL_SYSTEM.md` §7 permits a match cut only when both scenes share one live rig; there is none here, so the honest choice is a hard cut whose first frame is near-identical. That requires both scenes to build the bridge from one definition.
**Recommendation:** promote `b11._vector_bridge()` to `common/`, swap `b11`'s call site (no render change), and have C01 call it. Verify the seam with `tools/still_frames.py` after either file changes.
**Cost if wrong:** the chapter's most important seam has two independently drifting constructions and nothing type-checks their agreement — the exact failure `common/data.py`'s comment about `ALIAS_T` was written to prevent.

**5. Provenance of the `K = 16` accuracy figure.**
Handoff §7 permits the claim only with the exact experimental setup recorded in `SOURCE_MAP.md`. §8 records the numbers but not the batch, `λ`, or window.
**Recommendation:** `facts.py` recomputes the relative error on the batch C08 actually displays, at `λ = 1` over `[0.2, 4]`, and the narration says "on this batch." Add the measured setup to `SOURCE_MAP.md` §8.
**Fallback:** attribute the figure to the source in narration and show only qualitative agreement.
**Cost if wrong:** a number on screen that `facts.py` cannot check — the class of defect that `SOURCE_MAP.md` §6a–6c exists to catch.

**6. Vertical treatment of the score-vs-angle plot in C05. — CLOSED 2026-08-18, built.**
The anti-diagonal projection of `Z = (X, X)` is identically zero, so its Epps–Pulley score is order 10¹–10² at `N = 200`, against ~0.03 on the coordinate axes. A linear axis makes the two near-zero minima indistinguishable from the axis line; a log axis introduces a reading the viewer has not been prepared for.
**Options:** (a) clip the axis and mark the excursion as off-scale; (b) plot on a compressed scale with the two minima annotated numerically; (c) reduce `N` so the dynamic range is smaller.
**Was recommended:** (a), with the two minima carrying explicit numeric labels.
**Resolved as: linear over the whole range, `0 → 90`, plus the numeric labels — the half of (a) that was actually load-bearing.** The clip is unnecessary, and the recommendation had the requirement backwards. C05 does not need the two minima *distinguished from* the axis line; it needs them **on** it, because "exactly two directions look right" is read as "the curve touches the floor exactly twice". Distinguishing them from the floor would have weakened the very claim the clip was meant to protect. What the clip was really guarding was the middle of the range, and that survives on its own: the 45° bump sits at `10.284`, which on a `0 → 90` axis of height 2.85 stands 0.33 world units clear of the axis — about six dot radii, plainly a bump and plainly not the floor. Two 0.244 marks name the minima.
Three preconditions made this work, and a future scene reusing the component should check them rather than assume the outcome: the dynamic range is 335:1 rather than the 10³ the note feared; the peak is a broad hump (35° of the half turn scores above 40) rather than a needle, so it reads as a region and not as a spike artefact; and `data.diagonal_2d` was changed to standardize `X`, without which the minima do not sit on the axes at all (see below).

**7. Does the `data.ring_2d` beat survive?**
It forecloses "SIGReg is just a covariance penalty," costs ~8 seconds in C10, and the data already exists.
**Recommendation:** storyboard it, implement it last, cut it first if C10 runs past 2:15.

**8. Which cloud C03 projects.**
**Recommendation:** the isotropic cloud carried from C01/C02 — identity continuity, and it establishes the small-score baseline that C04 contradicts.
**Alternative:** a mildly anisotropic cloud so the machine is visibly doing something.
**Cost if wrong:** minor; the risk is only that C03's payoff number is undramatic.

**9. The `ThreePanelRig.mount(dots=...)` API addition.**
C03 needs the rig to adopt shadow dots it already owns rather than spawning a second set. This is a small, additive, backward-compatible change to a Chapter B shared file.
**Recommendation:** approve. The alternative — mounting the rig and then removing the shadow dots at a matching frame — is the ghost-point pattern `common/rig.py`'s own `swap()` docstring warns about.
**Cost if wrong:** ghost dots at the chapter's most important transition.

**10. Runtime budget.**
~16:30 estimated against `PLAN.md`'s "~9 min". Chapter B ran 17:50 against an 8-minute estimate.
**Recommendation:** accept ~16:30 and update `PLAN.md` §5, or name a target now and decide which scenes absorb the cut. The compressible ones are C08 (`K` is engineering) and the C02 pairing beat; C05 and C06 are learner-journey moments 4 and 5 and should not be cut before those.

**11. Voice budget.** The ElevenLabs Creator account carries 127,467 characters/month; a Chapter B pass is ~20,510. Chapter C is comparable. Audio is cached per passage text plus service settings, so narration should be frozen at the draft-voice stage before an Archer pass — a late rewrite of every passage spends the budget twice.

---

## 8. Recommended implementation sequence

Once §7 is resolved. One scene at a time; render and review each before the next; do not build the chapter ahead of approval.

1. **Foundations, no scenes.** `common/score.py` (verified against `b11`'s numbers), `common/cloud.py` (extracted from the prototype), `_vector_bridge` promoted, `ThreePanelRig.mount(dots=)`. Validate with a still: `./render.sh <probe> -s -ql`.
2. **C03 first, not C01.** It is the hardest scene, it exercises `CloudProjectionRig` end to end, and it is the one whose failure would invalidate the architecture. Build it, render at `-qh`, review the phase-5 lift and phase-9 contraction frame by frame.
3. **C01, C02.** With `CloudRig` proven, these are choreography.
4. **Test the B11 → C01 → C02 → C03 seam** through the real `build.sh` concat path before going further.
5. **C04, C05.** Shared score-vs-angle component; decide §7.6 before writing either.
6. **C06.** Short, mostly typography and one sweep.
7. **C07, C08, C09.** The formula assembly is last of the three because it consumes their objects.
8. **C10.** Last, and reviewed against the claim ledger line by line before it is called finished.
9. **Generated script dump** (`tools/script_dump.py` → `SCRIPT_chapterC.md`), `tools/narration_audit.py`, `facts.py`, then the Archer pass, then the master.

---

### Files referenced

- `NEXT_MODEL_HANDOFF_chapterC.md`
- `PLAN.md`
- `SOURCE_MAP.md`
- `ANIMATION_PLAYBOOK_chapterB.md`
- `CHAPTER_B_REVIEW_GUIDE.md`
- `chapterC/c02_covariance.py`
- `chapterB/b11_fingerprint_to_loss.py`
- `chapterB/b00_the_problem.py`
- `common/{rig,wrap,layout,palette,type,data,beat,fingerprint,distribution}.py`
- `../../docs/{NARRATION_SPEC,VISUAL_SYSTEM,MANIM_CE_VS_MANIMGL,RENDER_REVIEW_SPEC}.md`
- `../3blue1brown_videos/_2024/transformers/{embedding,network_flow}.py`, `_2017/nn/part3.py`

**Two things deliberately not done in producing this draft:** no scene file was written or edited, and no Manim code appears above. The narration drafts are drafts — they have not been run through `tools/narration_audit.py`, which should happen before any of them reaches a `voiceover()` call.
