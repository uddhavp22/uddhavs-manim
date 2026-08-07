# SIGReg explainer — build plan (rev 7)

Governed by [`EXPLAINER_PROCESS.md`](../../EXPLAINER_PROCESS.md) (repo root).
This file is the **per-project instance** of that process's deliverables.

| Deliverable | Lives in | Governed by |
|---|---|---|
| 1 — source map | `SOURCE_MAP.md` | |
| 2 — audience contract | §2 below | |
| 3 — learner journey | §3 below | |
| 4 — concept graph | `concepts.yaml` | |
| 5 — explanation path | §5 below | |
| 6 — scene graph | §6 below | [`VISUAL_SYSTEM.md`](../../VISUAL_SYSTEM.md) |
| 7–9 — narration, diagnostics, revision | §7, [`SCRIPT_chapterB.md`](SCRIPT_chapterB.md), `tools/narration_audit.py`, `facts.py` | [`NARRATION_SPEC.md`](../../NARRATION_SPEC.md) |
| 10 — production | §8 below, [`RENDER_REVIEW.md`](RENDER_REVIEW.md) | [`RENDER_REVIEW_SPEC.md`](../../RENDER_REVIEW_SPEC.md) |

Rendering mechanics go to [`MANIM_GUIDE.md`](../../MANIM_GUIDE.md).

**Rev 7 (2026-08-07, Part 2 / Chapter C bridge).** Part 2 is not a second
introduction to characteristic functions. Its job is to turn the three-panel
construction from Part 1 into a **one-dimensional, sample-only,
differentiable Gaussianity score**. Chapter C then lifts that already-built
tool to an embedding cloud through projections. This follows the source
tutorial's construction: characteristic function → Epps–Pulley statistic →
random one-dimensional projections → SIGReg.

- The current `b08`–`b12` are rev-2 implementation, not the approved playback
  order below. Their source, claims ledger, and useful visual assets remain
  inputs; their scene boundaries and narration require a Part 2 revision.
- **Playback order is conceptual, not filename order:** establish completeness,
  then its finite-frequency limitation, then the Gaussian target,
  differentiability, and the scalar score. `build.sh` must carry that explicit
  order when the revision is implemented: `b09 → b08 → b11 → b10 → b12`.
- Chapter B ends with `𝒯` for a batch of **scalars**. It does not introduce
  projections `u`, their count `M`, or the finished SIGReg average. Those
  belong to Chapter C, where each has a visible reason to exist.

**Rev 6 (2026-08-06, session 3).** Two binding specifications arrived from the
project owner — [`NARRATION_SPEC.md`](../../NARRATION_SPEC.md) and
[`RENDER_REVIEW_SPEC.md`](../../RENDER_REVIEW_SPEC.md) — and Chapter B was
re-cut against both.

- **Every one of the 92 spoken passages was rewritten.** Rev 5's script passed
  the narration audit and still read as machine-written, because the loudest
  patterns in it had no budget describing their shape. Four now do; the
  findings and before/after are in [`RENDER_REVIEW.md`](RENDER_REVIEW.md) F7–F9.
  Headline: **12/12 scenes closed on a slogan; 0/12 now.**
- **The visual system was written down and implemented.** The prose had never
  had a typeface chosen for it — ManimGL's `text.font` default is `Consolas`,
  absent on macOS, so every `Text` fell back to an unspecified Pango family.
  See [`VISUAL_SYSTEM.md`](../../VISUAL_SYSTEM.md) and `RENDER_REVIEW.md` F1–F6.
- **`fingerprint` is no longer spoken before `b09` earns it** with the
  uniqueness theorem: 24 uses across 8 scenes → 5 across 3. This closes the
  rev-5 open question about metaphor count.

**Rev 5 (2026-08-06)** restructured rev 4 onto the Explanation Compiler process.
Rev 4 organised the plan around *changes in the viewer's mental model*, which
survives intact — it is now §3 and §5. Rev 5 added the audience contract, the
typed graph, the executable claims ledger, and three source-fidelity fixes that
re-reading the actual source turned up.

---

## 0. The gate: the pen-and-paper test

Before any scene is coded, its idea must be reconstructible with a few drawings
and no polish. If a beat cannot survive that test, animating it is decoration.

**Every visual action must correspond to a necessary mathematical realization.**
If the viewer would understand the same amount with the animation removed, the
animation is not doing work.

This is the local form of the process's core principle: the explanation behaves
like a visual argument, and the formula arises from the visible operation.

---

## 1. The irreducible core

> **SIGReg checks whether every one-dimensional shadow of an embedding cloud
> has the Fourier fingerprint of a standard Gaussian.**

Everything else exists to make that sentence computable:

```
embedding cloud -> random 1-D shadows -> characteristic-function fingerprints
                -> distance from the Gaussian fingerprint -> a differentiable loss
```

The video should feel like **one continuous investigation**, not a tour:

> We need to tell whether a cloud has collapsed. We only have samples. How can
> samples describe a distribution? Wrap them round a circle and average. How do
> we compare whole fingerprints? Measure the gap across frequencies. How do we
> handle hundreds of dimensions? Look at shadows. How many shadows and
> frequencies can we afford? Sample a few of each.

```
losses can be cheated -> we must constrain a DISTRIBUTION
  -> characteristic functions fingerprint distributions
  -> shadows fingerprint clouds
  -> SIGReg makes this differentiable and practical
```

---

## 2. Audience contract  *(Deliverable 2)*

**Intended viewer.** Comfortable with undergraduate mathematics — vectors,
averages, basic probability, and what a derivative is for. Has met complex
numbers but does not think in them daily. Has *not* internalised Fourier
analysis, and does not need to.

In plain language: *the video assumes vectors, averages and basic probability;
briefly restores the picture of a complex exponential as a rotating unit arrow;
teaches characteristic functions themselves from scratch; and cites, without
proving, the Fourier uniqueness theorem.*

| | Concepts |
|---|---|
| **ASSUME** | expectation as a weighted average; unit vectors and projection; covariance and eigenvalues; that gradient descent needs derivatives |
| **REFRESH** | complex number as an arrow; `e^{iθ}` as the unit arrow at angle `θ` (`b01`, and *only* by that property) |
| **TEACH** | phase `t·x`; wrapping; the empirical CF; the three-panel rig; `Re`/`Im`; `φ(0)=1`; frequency selection; differentiability; the Gaussian fingerprint; the squared-gap loss |
| **DEFER** | the CF as a Fourier transform of a density; the inversion formula; contour integration; `λ` tuning; quadrature weights `α_k` |

`fourier_transform` is DEFER by explicit decision, not oversight — introducing
it first is the standard way this topic gets explained badly (§4).

---

## 3. Learner journey  *(Deliverable 3)*

The five moments that carry the weight. Slow down here; move briskly elsewhere.

1. **Perfect prediction can mean zero understanding.** The loss meter reads
   *perfect* while the cloud becomes one dot. The contradiction is the hook.
   *Before:* a low loss means the model learned something. *After:* a loss can
   be satisfied by a degenerate encoder.
2. **Matching Gaussian points ≠ matching a Gaussian distribution.** The naive
   fix provably pulls to the origin: `E‖z−z*‖² = ‖z‖² + D`, so `∇_z = 2z`.
   Gaussianity is a property of the **collection**, not of a point.
   *Proof status:* `exact_derivation`, verified in `facts.py`.
3. **A characteristic function is an average rotating arrow.** Not "the Fourier
   transform of a measure" — correct and useless as a first mental object.
   *Before:* `e^{itx}` is arbitrary complex notation. *After:* it is a direction
   whose angle depends on `x` and `t`. The three-panel rig lives here.
4. **Every shadow determines the cloud.** `Z = [X, X]` passes both axis-wise
   tests and is rank one. Then Cramér–Wold. *Proof status:* the counterexample
   is `exact_derivation`; Cramér–Wold is `theorem_statement`.
5. **The anti-collapse proof is nearly trivial by the end.** Payoff, not lemma.

---

## 4. What to deliberately avoid

- Animating the finished SIGReg formula term-by-term before the pipeline is understood.
- Introducing `N, D, M, K, t, λ, λ_reg` in one scene. Each symbol appears only
  when needed — **`M` does not exist until Chapter C.6**.
- Calling the CF "the Fourier transform of a density" as the introduction.
- Asserting isotropy prevents collapse without showing covariance eigenvalues.
- Colour-coded labels as a substitute for deriving why an operation is there.
- Equal time per section. Quadrature is engineering; CFs and Cramér–Wold are the video.
- **3b1b mannerisms.** No "pause and ponder", no "isn't it beautiful". Borrow
  the structure, not the voice.

**Licensed analogies — exactly two.** *Arrows agreeing vs cancelling*, and
*shadows*. Both are licensed because the metaphor is literally what the maths
does. `fingerprint` is a third and is grandfathered in as naming (see §7).

### Notation fixed here

| Symbol | Meaning |
|---|---|
| `𝒯` | the Epps–Pulley statistic |
| `K` | number of frequency knots |
| `M` | number of random projections (Chapter C only) |
| `t` | frequency — **never** a time index |

---

## 5. Explanation path  *(Deliverable 5)*

Three chapters, each independently watchable.

### Chapter A — How distributions answer questions  (~4 min) — **unbuilt**
1. A machine producing numbers; the distribution is *how often*, not *what*.
2. Probability as mass placed on values; density as the continuous limit.
3. Expectation as a **weighted average** — a balance point.
4. **Expectation as a distribution-querying machine.** `g(x) = x²` on a line.
5. Moments give partial information — none reveal everything.

*Core realization: a distribution can be understood through how it averages functions.*

Chapter B currently marks these ASSUME. If A is built, B's contract tightens.

### Chapter B — Characteristic functions  (~8 min planned / **17:25 built**) ← the heart

The problem, stated first: *we have samples, not a formula. What family of
questions preserves all the information?*

1. Complex numbers as arrows; `e^{iθ}` = unit arrow at angle θ.
2. `x ↦ e^{itx}` — wrap the number line round the circle. `Δθ = t·Δx`.
3. Average the arrows → the centroid. Aligned → long; spread → cancels.
4. **Sweep `t`. The three-panel rig.**
5. Real and imaginary parts: *how far right* and *how far up*, on average.
6. **Worked examples**, each teaching one thing, all exact:
   constant → `|φ|=1`; two-point → `φ(t)=cos t` exactly; shift → phase only.
7. `φ(0) = 1` always. A fixed anchor for every graph that follows.
8. **Completeness before approximation.** The full characteristic function
   determines the scalar distribution (Fourier uniqueness, cited not proved).
   The viewer can now say why a whole curve, rather than one frequency, was
   built in Part 1.
9. **The finite-frequency problem.** A computer and a finite batch cannot use
   every `t`: low frequencies miss the toy batches' shape difference, while
   high frequencies are dominated by empirical-CF noise. This motivates a
   smooth bandwidth weight without pretending `λ` is uniquely determined.
10. **The target we want.** For a standard normal scalar,
    `φ₀(t)=e^{−t²/2}`. Show its smooth decay against the toy batches. The ODE
    derivation is optional appendix material; the target curve is load-bearing.
11. **Why this can train, unlike a histogram.** Moving a wrapped sample changes
    `e^{itx}` smoothly, whereas a bin count is locally constant. This earns the
    word “loss” before a loss is written.
12. **Close the one-dimensional construction.** At each frequency, square the
    gap `|φ̂_N(t)−φ₀(t)|²`; accumulate the visibly constructed gap across the
    weighted frequency range; introduce the `N` prefactor and name the result
    `𝒯`, the Epps–Pulley statistic. End on its limitation: it scores scalars,
    while an embedding is a cloud of vectors.

*Core realization: a characteristic function yields a complete,
sample-computable, differentiable **one-dimensional Gaussianity score**.*

Ends on the question that opens C: *`𝒯` can score one line of numbers. Which
lines of a vector cloud must look Gaussian for the whole cloud to be Gaussian?*

### Chapter C — SIGReg  (~9 min) — **unbuilt except `c02`**
1. **The cheating world model.** Loss meter hits zero; an information meter
   drops to zero at the same instant. No SIGReg formula yet.
2. **The distribution goal and tempting wrong fix.** Point, line, pancake,
   sphere; then random-target matching pulls every point to the origin. The
   target is a property of the collection, not an assigned partner per point.
3. **Bring back `𝒯` on one shadow.** A unit direction `u` turns the cloud into
   scalars `uᵀz`; Chapter B's score applies without a new statistic.
4. **One shadow is not enough.** `Z=[X,X]` can look Gaussian on coordinate axes
   while living on a line. This failure creates the need for every direction.
5. **All shadows determine the cloud.** State Cramér–Wold, cited not proved:
   Gaussian projections in every unit direction imply `N(0,I_D)`.
6. **Make “all” computable.** Sample `M` unit directions; only now introduce
   `M` and average the already-understood scalar scores.
7. **Make each scalar score computable.** Replace its weighted frequency
   integral by `K` knots. Show `K=16` versus `K=2000` (0.01% error), but defer
   trapezoidal weights `α_k`; the insight is finite evaluation, not mechanics.
8. **The SIGReg formula, assembled from visible operations.** Average over
   directions, each containing its discretized `𝒯`; then watch the loss oppose
   collapse. Eigenvalues `(1,0,0) → (1,1,1)` are evidence of this run, not a
   convergence guarantee.
9. **The proof as payoff.** In the population/all-direction limit, the
   Epps–Pulley and Cramér–Wold implications give `Z∼N(0,I_D)`.
10. **Limits and honest scope.** finite `N`, finite `M`, finite `K`, bandwidth
    choice, global optima versus optimization dynamics, and what SIGReg does
    not guarantee.

> ⚠ **Highest-risk false inference in the project** (`concepts.yaml`, status
> OPEN). C.8 shows gradient descent opening a collapsed cloud. The source
> guarantees the **global minimum only** — "not local minima or convergence
> rates". C.9 must say this out loud or the animation implies a guarantee the
> mathematics does not provide.

### Part 2 → Chapter C continuity contract

| At the end of Part 2, the learner knows | Therefore Chapter C may do | Chapter C must not redo |
|---|---|---|
| `𝒯` scores whether one scalar batch resembles `N(0,1)` from samples, using a weighted CF gap | Project a cloud onto one line and reuse `𝒯` immediately | Re-explain wrapping, `φ̂_N`, the Gaussian target, or why the weight exists |
| One frequency is insufficient and infinitely many cannot be evaluated exactly | Introduce `K` only when turning the known integral into a finite computation | Present quadrature as a new reason to care about characteristic functions |
| The full scalar CF determines a scalar distribution | Make “every direction” necessary with `Z=[X,X]`, then cite Cramér–Wold | Claim coordinate-wise Gaussianity is enough |
| The statistic is differentiable in scalar samples | Show gradients through `uᵀz` and the assembled loss | Re-litigate histograms except for one visual contrast |

---

## 6. Scene graph  *(Deliverable 6)*

### The persistent visual language

Typography, colour, and layout are **not decided here** — they live in
[`VISUAL_SYSTEM.md`](../../VISUAL_SYSTEM.md) and are implemented in
`common/type.py` and `common/palette.py`. A scene that names a font, a hex
colour, or a font size directly is a defect. This section covers only the
objects specific to this explainer.

Four objects, reused throughout. Nothing else gets invented mid-video.

| Object | Meaning | Colour role |
|---|---|---|
| **Embedding cloud** | the multivariate representation distribution | `CLOUD` |
| **Projection line** | one Cramér–Wold direction `u` | `DIRECTION` |
| **Unit circle** | the characteristic-function construction | `AXIS` furniture |
| **Frequency graph** | Gaussianity discrepancy across `t` | `CLOUD` vs `TARGET`, gap in `COLLAPSE` |

One transition, revealed progressively:
`cloud -> shadow -> wrapped arrows -> average arrow -> loss`

### The three-panel rig (the central visual)

```
┌─ numbers on a line ─┐  ┌─ arrows on the circle ─┐  ┌─ phi(t) vs t ─┐
│  •  • •      •      │  │      ↖ ↑ ↘ →          │  │      ╭────     │
└─────────────────────┘  └───────────────────────┘  └────────────────┘
                                    ▲
                              frequency t
```

**Translation rule** — written out, because "watch all three panels" is exactly
what the process forbids:

```
sample x on the number line
  → angle t·x
    → arrow e^{itx}
      → average arrow
        → the HORIZONTAL POSITION of that average IS the height of the curve
```

The dashed link line draws that last step rather than asserting it. The viewer
should be able to *predict* what the next panel does before it does it.

**Invariant across the sweep:** panel 1 never moves. The data is not changing;
only the wrapping speed is.

### File naming — the number IS the plan item

`<chapter-letter><item-number>[suffix]_<slug>.py`; scene class is the prefix
uppercased (`b06a_one_speed_fails.py` → `B06A`). `build.sh` globs and sorts on
filename, so the number alone fixes running order.

- **`b00`** — un-numbered lead-in stating the problem.
- **`b06a`** — a letter suffix marks an addition not in the numbered list.
- A scene spanning several items is named for its first (`b02` covers 2–4).
- Gaps are unbuilt scenes, not missing files.

---

## 7. Diagnostics and revision  *(Deliverables 7–9)*

### Executable, not asserted

| Tool | Checks | Status |
|---|---|---|
| `facts.py` | every number spoken on screen | **19/19 pass** |
| `tools/narration_audit.py` | language patterns, per 1k words | **all budgets pass** |

Both exit non-zero on failure. A stale number is a build failure, not a
confident line of narration that happens to be wrong.

### Source-fidelity fixes, 2026-08-06

The source was re-fetched to run the fidelity diagnostic. Three defects in
already-rendered scenes:

1. **`b12` displayed `𝒯` without the `N` prefactor** while calling it the
   Epps–Pulley statistic. The source has `𝒯 = N∫w(t)|φ_N−φ₀|²dt`. As a *loss*
   the prefactor does not move the argmin — but the named statistic has it.
   **Fixed**; `N` now on screen and glossed.
2. **`b12` showed `w_λ(t)` over an animation that never constructed it.** The
   swept area is unweighted. Visual-symbolic correspondence broken. **Fixed** by
   building the formula in two steps — the unweighted integral the picture
   actually computed, then the weight and `N` as named refinements, with the
   measured reassurance that the verdict moves only 56.4× → 57.3×.
3. **`b08` claimed the weighting "is not a tuning knob".** The source explicitly
   calls `λ` a *bandwidth parameter*, so it plainly is one. **Fixed** — what
   finite `N` forces is the *existence* of high-frequency suppression, not any
   particular `λ`. Also separated the smooth weight `w(t)` from the `[0.2, 4]`
   truncation, which the scene had conflated.

### Narration fixes from the audit

4. **`b02` said "Watch all three panels at once"** — the process's own negative
   example, verbatim. **Fixed** to name the invariant and the dependency.
5. **`b05` had a run of five consecutive short sentences.** **Fixed**; longest
   run now 3.

### Standing findings, not yet acted on

- **Metaphor count is 2, over the process's cap of ~1.** `fingerprint` (24 uses,
  8 scenes) and `arrow` (39 uses, 11 scenes). Judgement: `arrow` is not a
  metaphor — a complex number *is* an arrow here, which is the whole point — so
  the real count is one metaphor plus one representation. Recorded rather than
  fixed. Revisit if a third appears.
- **`b00` and `b08` still show cadence runs of 4.** Below the run-of-5 threshold
  that triggered the `b05` rewrite. Left alone.
- **Repeated openers**: "it is…" ×14, "that is…" ×12. Diffuse across 3.5k words;
  a systemic rewrite would cost more than it buys.

---

## 8. Production  *(Deliverable 10)*

### Chapter B status: complete — 10 scenes, all narrated

Part 1 was re-cut at rev 4 and is now six scenes rather than eight. Two scene
files were **folded into their neighbours and deleted**, because each was one
half of an investigation the master was cutting in two — the rendered chapter
faded a live three-panel rig to background and rebuilt an almost identical one
a second later at both seams:

- `b05_real_and_imaginary` → the second half of **`b02`**. The curve is built,
  and then the same rig, the same batch and the same sweep are used to notice
  that the curve was only one of the average arrow's two coordinates.
- `b06b_what_magnitude_ignores` → the third beat of **`b06`**. Same rig, third
  question.

`b07` was rewritten rather than trimmed. It used to prove `phi(0) = 1` on three
batches nobody had met and stop there; it now proves the same thing and then
runs **`b00`'s two toy batches** through the rig, so the question the chapter
opens with is the question its last Part 1 scene answers. See
[`RENDER_REVIEW.md`](RENDER_REVIEW.md) rev 4.

| file | plan item | rev 3 | rev 4 |
|---|---|---|---|
| `b00_the_problem` | lead-in | 0:33 | 1:11 |
| `b01_arrows` | 1 | 1:28 | 1:24 |
| `b02_the_rig` | 2–5 | 1:19 + 1:21 | 2:41 |
| `b06_worked_examples` | 6 | 0:48 + 0:53 | 1:20 |
| `b06a_one_speed_fails` | aliasing | 0:55 | 0:55 |
| `b07_the_anchor` | 7 | 0:53 | 1:30 |
| `b08_which_frequencies` | 8 | 2:08 |
| `b09_uniqueness` | 9 | 1:31 |
| `b10_why_not_histograms` | 10 | 1:48 |
| `b11_gaussian_fingerprint` | 11 | 2:59 |
| `b12_fingerprint_to_loss` | 12 | 2:43 |

**Master runs ~17:50 at 480p draft, against the ~8 min estimate in §5.** The
estimate was wrong, not the pacing: it predates the beats and assumed each plan
item was a beat rather than a scene. No dead air — silence detection at −45 dB
over 2.5 s finds nothing, because `VoiceoverScene` makes audio drive timing.

If runtime has to come down: **`b11` at 2:59 is the outlier** and §5 calls the
ODE derivation an appendix. Stages B and C are the cuttable ones. `b08` and
`b12` are moments 3 and 5 of §3 and should not be cut before `b11` is.

**Still 480p.** Final pass is `./build.sh chapterB --hd`.

### Narration pipeline

On the repo's `voiceover/` port of manim-voiceover: narration lives beside the
animation and `tracker.duration` makes the *audio drive the timing*, so a beat
cannot run ahead of its own speech. This structurally eliminates the rev-3
defect where 13.0 s and 14.7 s of dead air sat on the two most important
animations.

- Service: `ElevenLabsService(voice_id="Fahco4VZzobUeiPqni1S",
  voice_settings={"stability": 0.65, "similarity_boost": 0.75},
  transcription_model="base")` selects Archer - Conversational.
  Verified working. Key in a gitignored `.env` — never print or commit it.
- `transcription_model="base"` runs Whisper for true word timings. Measured
  drift without it on an 11 s line: 142–334 ms (8–20 frames).
- `SIGREG_VOICE=draft` selects macOS `say`; `SIGREG_VOICE=eleven` selects Archer.
  `build.sh --voice eleven` supplies it for Part 1. The Creator account has 127,467
  characters/month; audio is cached, so only edited passages re-spend.
- Bookmarks (`<bookmark mark='x'/>` + `wait_until_bookmark`) tie a specific word
  to a specific visual — essential for the rig.

---

## 9. Corrections to the pasted prose (blog is right)

- Integration range is **`[0.2, 4]`, one-sided** — not `[−5,5]`. The integrand is
  even, so a symmetric grid spends half its knots on a mirror image.
- **`K = 16`** knots → 0.01% error vs `K=2000`; `K=8` → 0.04%; `O(1/K²)`.
- The blog derives `e^{−t²/2}` by **contour integration**; we use the ODE route
  (`p′ = −xp` ⇒ `φ′ = −tφ`). Declared divergence, `SOURCE_MAP.md` §6d.
- The `[0.2, 4]` mass fraction is **batch-dependent** (99.63%–99.98% measured
  across four batches). Rev 4 recorded 99.78% as though it were a constant and
  `b08` spoke it; both now state the bound instead.

---

## 10. Bugs found (all silent — none raised an error)

### From the rev-6 restyle, 2026-08-06 session 3

- **`text.font` defaulted to `Consolas`, which is not installed.** Every `Text`
  in the chapter rendered in an unspecified Pango fallback for the entire life
  of the project. No warning; manimpango falls back silently. Fixed in
  `custom_config.yml` *and* passed explicitly in `common/type.py`, because one
  of those alone is a machine-local fix. → `VISUAL_SYSTEM.md` §1.
- **`build.sh` reported success on a scene that crashed.** manimgl exits 0 after
  an exception inside `construct()`, and the build only tested that the output
  file *existed* — which it did, from the previous render. The master was
  rebuilt from stale clips and its duration was unchanged, which is the only
  reason it was noticed. Now compares mtime against a timestamp taken *before*
  the render. This is the same shape as the session-2 bug where a wait loop
  tested for a path instead of a completion signal.
- **`NameError` inside a beat method surfaced twenty minutes into a build**,
  after four scenes of text-to-speech had been spent. pyflakes cannot help —
  `from manimlib import *` makes every mobject class "possibly undefined", so
  real findings drown. `tools/preflight.py` resolves the star import for real
  and now gates the build.
- **`ty.line()` needed an explicit baseline alignment.** `VGroup.arrange()`
  centres, and Helvetica x-height sits nowhere near Computer Modern digit
  height, so a word and its number rendered visibly off each other's baseline.

### Earlier

- `\;` before `\text{}` fails under the default TeX template. Cause is **`tipa`**.
- `render.sh` from any cwd but the repo root silently lost `custom_config.yml`.
- `TransformMatchingStrings(x.copy(), y)` leaves both copies on screen.
- `next_to(eq, RIGHT)` annotations run off frame → `layout.fit_in_frame()`.
- A stage header left on screen collided with the result moved into its slot.
- `Dot(color=)` is silently ignored — use `fill_color=`.
- 2-D overlays in a `ThreeDScene` need `.fix_in_frame()`.

From building items 1, 5, 7–10, 12 — all found by extracting frames and looking:

- **`FadeOut` cannot remove an `always_redraw` mobject.** Known for
  `clear_beat`, but it bites on *partial* teardown too: `b12` faded its left
  panel and left two live dots redrawing for 40 s with no panel around them.
  `clear_updaters(recursive=True)`, then `FadeOut`, then `remove`.
- **A bar taller than the frame is simply not in the render.** `b10` used one
  screen-height-per-count at every bin width; at width 1.5 the tallest bar was
  7.2 units on an 8-unit frame. Generated geometry needs its *worst* case
  checked, not its typical one.
- **Clipped text raises nothing.** `b11`'s closing aside fell off the bottom.
  `fit_in_frame` guards horizontally only.
- **An angle drawn from a raw `ValueTracker` wraps past 2π.** `b01`'s arc became
  a near-closed ring over the components.
- Labels at the far edge of an `Axes` land *inside* whatever is shaded there
  when the region is a few pixels wide (`b08`'s "too low" over the window).
- Reading colour off a 480p draft is unreliable — `b02`'s `Tex` substring
  colouring looked white at 480p and was correct at full crop. Zoom first.
