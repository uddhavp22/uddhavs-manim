# Chapter B rewrite and continuity plan

> **Status:** proposed structure for scene-by-scene review. This document does
> not authorize animation changes, file merges, or playback-order edits yet.
> It records the narrative backbone to protect while the script and framing are
> revised.

## The protected argument

Chapter B begins and ends with the same requirement: a differentiable scalar
score computed from samples.

```text
need one scalar loss
  → mean and variance miss shape
  → need a richer sample-based description
  → histograms preserve shape but have bad gradients
  → make each sample contribute smoothly
  → x becomes the unit direction e^(itx)
  → average the directions
  → one t gives one complex measurement
  → one measurement can be fooled
  → sweep t to obtain the characteristic-function curve
  → test what the curve notices and what it ignores
  → the full curve is complete by the uniqueness theorem
  → finite batches make some frequencies more useful than others
  → choose the standard-Gaussian characteristic function as the target
  → measure and accumulate squared gaps
  → obtain one differentiable scalar score
  → expose the remaining limitation: it only scores one-dimensional samples
```

Every scene should answer the question created by the previous scene. A scene
that merely adds a fact without changing the viewer's question does not belong
in the main line.

## Narrative rules for the rewrite

The recurring unit is:

```text
problem → experiment → observation → conclusion → next problem
```

- Questions are used only when the visible setup gives the viewer something
  they can reason about.
- The animation shows the experiment and observation. Narration supplies the
  cause, invariant, qualification, or conclusion.
- A result is not announced before its visual operation has been understood.
- The conclusion of one scene should do most of the work of opening the next.
- Openings do not recap the preceding scene unless a specific object must be
  restored after a hard cut.
- “Fingerprint” means a complete identifying description. The word earns its
  full force only after the uniqueness theorem.
- Examples remain examples. The uniqueness theorem is cited, not visually
  “proved” by showing several successful tests.

## Recommended conceptual order

```text
b00 → b01 → b02 → b03 → b04 → b05 → b06 → b07 → b08 → b09 → b10 → b11
```

This is now the canonical order in the filenames, `build.sh`, the generated
script, and `tools/script_dump.py`.

## Naming decision

There are two different moments that the current script partly conflates:

1. **Naming the constructed object.** Once the sweep exists, call it the
   characteristic function and give its empirical formula. The experimental
   scenes need a stable name and notation.
2. **Earning the fingerprint claim.** Only after `b08` may the narration say
   that the full curve identifies the distribution completely.

This reconciles “name the thing when it has been built” with “do not call it a
complete fingerprint before uniqueness.”

## Scene plans

### 1. `b00_the_problem` — why one score first needs a richer description

**Viewer before:** The task is to turn a sample batch into one training loss.

**Visible experiment:** Compare a bell-shaped batch with a two-clump batch
whose count, mean, and variance agree.

**Observation:** The summaries agree while the arrangement of mass does not.

**Conclusion:** Mean and variance cannot be the description from which the
final score is built. We first need a richer description of shape.

**Important clarification:** The two-batch example is not itself supposed to
produce the final scalar. Its job is to demonstrate why the score cannot be
built from a few summaries. This resolves the open note currently embedded in
the generated script.

**Keep:** The paired summary reveal and the visible contradiction.

**Rewrite/update:**

- Establish the final goal—one differentiable scalar—before or during the
  comparison, not after it.
- Replace the current “hole in a pipeline” explanation if it delays the simple
  causal point: summaries fail, so a richer description must come first.
- End by proposing the histogram as the obvious richer description.

**Exit question:** A histogram preserves visible shape. Can it also serve as a
training loss?

### 2. `b01_why_not_histograms` — shape without a useful gradient

**Viewer before:** Histograms look like a promising sample-based description.

**Visible experiment:** Move one sample continuously toward and across a bin
edge while its histogram count is tracked.

**Observation:** The count stays flat, then jumps.

**Conclusion:** Hard bins preserve shape but provide no useful local direction
for gradient descent.

**Keep:** The bin-edge counterexample.

**Rewrite/update:**

- Let the moving sample and changing count be the central event; bin-width and
  offset sensitivity are secondary and can be shortened if they delay it.
- Show the actual sample and corresponding bar together. A standalone step
  graph is weaker if the viewer cannot see which sample causes the jump.
- Avoid overstating the conclusion: histograms are not “bad descriptions”; they
  are bad for this differentiable-loss requirement.

**Exit question:** Can every sample contribute something that changes smoothly
when the sample moves?

### 3. `b02_arrows` — a smooth contribution represented by a direction

**Viewer before:** Each sample needs a smooth contribution that can reinforce
or cancel with other samples.

**Visible experiment:** Introduce a unit arrow, its angle, its horizontal and
vertical components, and an average of several arrows.

**Observation:** Nearby directions reinforce; spread directions cancel.

**Conclusion:** A unit direction is a smooth, averageable contribution.

**Keep:** Unit-arrow components and the average moving inward as directions
spread.

**Rewrite/update:**

- Introduce `e^{i\theta}` only as compact notation for the already-visible unit
  direction.
- Avoid becoming a general complex-number lesson. Only angle, components, and
  averaging are prerequisites for the next construction.
- Make the average a point or arrow whose identity persists through the beat.

**Exit question:** What angle should a sample value `x` produce?

### 4. `b03_the_rig` — one sample becomes a direction; one setting becomes a curve

**Viewer before:** A unit direction is smooth and averageable, but no rule yet
connects it to sample values.

**Visible experiment:** Use `\theta=tx`, wrap the number line, average the
arrows, then vary `t` while the samples remain fixed.

**Observation:** One `t` gives one complex average. Sweeping `t` makes that
average trace a curve. Its real and imaginary coordinates record how far right
and up the average arrow points.

**Conclusion:** The same fixed batch can answer a continuous family of smooth
questions indexed by `t`.

**Keep:** The center-panel wrap, concurrent line handoff, average arrow, sweep,
and real/imaginary correspondence.

**Rewrite/update:**

- Protect the invariant: samples never move during the `t` sweep.
- Give each representation change an explicit handoff:
  `x → tx → e^{itx} → average arrow → curve value`.
- Do not ask the viewer to watch all three panels without naming the link.
- Decide during scene review whether symmetry remains here or moves into the
  experimental block. It belongs after real/imaginary parts are understood,
  but not necessarily inside this already-long construction scene.

**Exit question:** We have built a whole function. What exactly is it, and what
does its formula say we computed?

### 5. `b04_the_definition` — name the constructed function, without overclaiming it

**Viewer before:** The mechanism and curve are understood visually but do not
yet have stable notation.

**Visible operation:** Compress the already-visible sequence “wrap, add, divide
by `N`” into

```text
φ̂_N(t) = (1/N) Σ_j e^(itx_j).
```

**Observation:** Every symbol refers to an operation the viewer has already
seen.

**Conclusion:** This empirical curve is the characteristic function of the
batch.

**Keep:** Naming only after construction and the empirical formula.

**Rewrite/update:**

- Make the formula inherit its terms from the rig rather than appearing under
  a fresh copy of the apparatus.
- Do not call the curve a complete fingerprint yet.
- Strong consolidation candidate: fold this short scene into the end of `b03`,
  or place it before `b03` changes to a symmetric test batch so an exact visual
  seam is possible. The current `b03` ends on `MIRRORED`, while `b04` opens on
  the original bimodal batch; that is not a valid match cut.

**Exit question:** Before using this function as a score, what does it notice,
what stays invariant, and how can it fail?

### 6. `b05_worked_examples` — experimental stress tests on one apparatus

**Viewer before:** The characteristic function has a visual meaning and a
formula, but its behavior is still unfamiliar.

**Visible experiments:**

- collapsed/constant batch → magnitude remains one;
- symmetric two-point batch → imaginary parts cancel and `φ(t)=cos t`;
- translated batch → phase changes while magnitude is preserved.

**Observation:** Collapse, symmetry, and translation leave different, visible
signatures in the curve.

**Conclusion:** The curve contains much more structure than mean and variance,
but individual properties and examples do not yet establish completeness.

**Keep:** One persistent rig and explicit batch swaps.

**Rewrite/update:**

- Treat every example as a question asked of the same machine, not a catalogue
  of facts.
- If runtime becomes crowded, the exact two-point/cosine example is the first
  item to test for removal: it is mathematically clean, but it is not a required
  link in the protected backbone.
- If symmetry moves out of `b03`, place it here before translation.
- Consider folding `b06` into this experimental scene only after narration is
  settled; conceptually it is another invariant test on the same rig.

**Exit question:** Is there any frequency at which all distributions must
agree?

### 7. `b06_the_anchor` — agreement at one frequency proves nothing

**Viewer before:** Different batches produce informative differences across
the curve.

**Visible experiment:** Set `t=0`; every sample maps to angle zero and every
arrow lands at one.

**Observation:** `φ(0)=1` for every distribution.

**Conclusion:** Agreement at one frequency can be completely uninformative.

**Keep:** The exact three-step visual argument `t=0 → tx=0 → e^{i0}=1`.

**Rewrite/update:**

- Frame this as the first decisive failure of a one-frequency test, not as an
  isolated property card.
- End on the stronger question: zero is forced, but can a nonzero frequency
  also make a spread-out batch look collapsed?

**Exit question:** Can a carefully chosen nonzero frequency be fooled too?

### 8. `b07_one_speed_fails` — a nonzero frequency can alias

**Viewer before:** Agreement at `t=0` is useless, but perhaps one well-chosen
nonzero frequency is enough.

**Visible experiment:** Show a visibly spread batch whose values are spaced by
the wrapping period, so all arrows align at one nonzero `t`; then nudge `t`.

**Observation:** The same batch looks collapsed at one frequency and spread at
nearby frequencies.

**Conclusion:** No single measurement carries the whole distribution.

**Keep:** The simultaneous contradiction—spread-out samples and
`|φ(t)|=1`—followed by the frequency nudge.

**Rewrite/update:**

- The final finite probes should visibly suggest densifying into a whole curve.
- End directly on the question uniqueness answers; do not insert another fact
  scene between aliasing and the theorem.

**Exit question:** Could two genuinely different distributions agree across
the entire curve?

### 9. `b08_uniqueness` — the full curve earns “fingerprint”

**Viewer before:** Any finite collection of isolated measurements feels
potentially vulnerable.

**Visible operation:** Expand from one point, to several sampled points, to a
continuous curve.

**Theorem statement:** If two characteristic functions agree for every `t`,
the distributions agree.

**Conclusion:** The full characteristic function is a complete fingerprint of
a one-dimensional distribution.

**Keep:** The explicit qualification that the theorem is cited, not proved.

**Rewrite/update:**

- Remove the current backward reference “that is why the reliable range
  mattered”; the frequency-range experiment now follows this scene.
- Make the boundary between visual motivation and theorem statement explicit:
  the densifying points motivate the question but do not prove the theorem.
- Make clear that uniqueness concerns the full complex-valued characteristic
  function—both real and imaginary components—not only whichever component a
  later experiment chooses to plot.
- This is the first scene where “fingerprint” may carry the full completeness
  claim.

**Exit question:** A computer and a finite batch cannot evaluate an ideal
continuous curve perfectly. Which frequencies give useful information in
practice?

### 10. `b09_which_frequencies` — completeness meets finite data

**Viewer before:** The complete curve identifies the distribution in theory.

**Visible experiment:** Return to the original bell-shaped and two-clump
batches. Sweep from low to high `t`, then compare repeated finite Gaussian
draws.

**Observations:**

- very low frequencies barely separate these matched-summary batches;
- intermediate frequencies expose the shape difference;
- at high frequencies, finite-sample fluctuation dominates the small
  population signal.

**Conclusion:** Practical scoring must emphasize a useful frequency region and
suppress the noisy tail; the particular bandwidth remains a choice.

**Keep:** The low → informative → noisy experimental progression and the
finite-sample qualification.

**Rewrite/update:**

- This scene follows uniqueness, so its opening should contrast the ideal full
  curve with what finite computation can actually estimate.
- If the experiment plots only the real component, say so. It is evidence about
  where these particular batches separate, not a replacement for the full
  complex fingerprint used by the theorem and final loss.
- Do not reveal `e^{-t^2/2}` as a labeled formula here. The Gaussian population
  curve may appear as a reference, but `b10` owns the formula reveal.
- Keep “useful range” distinct from the smooth weight and its tunable
  bandwidth.

**Exit question:** Within the useful range, what curve should a standard
Gaussian produce?

### 11. `b10_gaussian_fingerprint` — choose the target curve

**Viewer before:** The characteristic function is complete, and a finite score
needs a practical frequency emphasis. The desired distribution is the standard
Gaussian.

**Visible prediction:** Symmetry predicts a zero imaginary part; the universal
anchor predicts that the curve begins at one.

**Known result:**

```text
φ₀(t) = e^(-t²/2).
```

**Conclusion:** The standard Gaussian supplies one target complex value at
every frequency.

**Keep:** The anchor and symmetry connections, target curve, and direct bridge
to pointwise disagreement.

**Rewrite/update:**

- Do not imply that “real and starts at one” derives or uniquely determines the
  formula; many functions have both properties. Those observations let the
  viewer anticipate features of the known Gaussian characteristic function.
- Keep the derivation omitted unless the chapter's scope changes.
- Remove the isolated title-card opening. It currently fades the only visible
  object before its voiceover block finishes, matching the known narrated-black
  gap at the `b08 → b10` region.
- Prefer a direct visual handoff from `b09`'s axes and frequency window to the
  Gaussian target curve.

**Exit question:** How do we turn the batch-to-target disagreement at every
frequency into one number?

### 12. `b11_fingerprint_to_loss` — return to the scalar goal

**Viewer before:** At every frequency, the batch and Gaussian give two complex
points.

**Visible construction:**

1. Draw the pointwise complex gap.
2. Square its length.
3. Sweep `t` and trace the squared gap.
4. Accumulate the gap across frequencies.
5. Introduce the smooth weight and `N` factor as the published statistic's
   refinements.

**Observation:** The Gaussian batch accumulates a small finite-sample baseline;
the two-clump batch accumulates much more.

**Conclusion:** The Epps–Pulley statistic is the differentiable scalar score
requested at the beginning.

**Keep:** Visual gap → squared gap → accumulated area → formula, in that order.

**Rewrite/update:**

- Explicitly close the histogram loop: moving a sample moves `e^{itx}` and the
  accumulated score smoothly.
- Do not let the full weighted formula appear before the weight has a visual or
  verbal role.
- End on the limitation, not a victory slogan: this scores scalar batches,
  while learned representations are vectors.

**Exit question:** Which one-dimensional views of a high-dimensional cloud must
look Gaussian? This is Chapter C's opening problem.

## Boundary and transition contract

A transition has three layers:

1. the outgoing conclusion;
2. the incoming question;
3. the visual state across the cut.

Narrative continuity does not require every boundary to be a visual match cut.
A hard cut is correct when the apparatus or data changes. What must disappear
is the feeling that each file restarts the lesson.

| Boundary | Logical handoff | Recommended visual treatment |
|---|---|---|
| `b00 → b01` | summaries fail → try a histogram | strongest match-cut candidate: leave the clumped batch selected and grow bins from the exact same dots; both scenes already use `data.bimodal_1d(40)` |
| `b01 → b02` | bins jump → seek a smooth contribution | honest hard cut; isolate the moving sample at the end of `b01`, then open `b02` directly on a movable point/direction—no title card |
| `b02 → b03` | directions can average → sample values must supply angles | hard cut with a direct answer: `b03` opens on the number line and immediately maps position to angle |
| `b03 → b04` | whole curve constructed → compress it into a name/formula | either merge `b04` into `b03`, or end `b03` before the symmetry batch swap and reproduce the exact rig state; the current states do not match |
| `b04 → b05` | named machine → test it | hard cut earned by the batch change; mount the familiar rig without reintroducing its panels |
| `b05 → b06` | examples show varied behavior → ask what never varies | hard cut or explicit in-rig batch swap; avoid a new section card |
| `b06 → b07` | all curves agree at zero → can a nonzero setting also mislead? | conceptual match: keep the aligned-arrow state, then reveal that `b07` aligns a spread batch at nonzero `t` |
| `b07 → b08` | finite probes can fail → what about the full curve? | strong continuity seam: sampled probe points densify into the complete curve; merge the last beat/first beat if exact geometry is otherwise awkward |
| `b08 → b09` | full curve is complete → finite data cannot use it ideally | preserve curve axes if practical; replace ideal equality with empirical curves and a finite sweep |
| `b09 → b10` | useful band identified → choose the Gaussian value inside it | strongest later match cut: retain the same axes/window and reveal the target curve; requires unifying `b09`'s `big_axes()` and `b10`'s `layout.cf_axes()` geometry |
| `b10 → b11` | target at every `t` → measure pointwise gaps | direct content handoff: select one `t` on the target curve and expand that pair of points into `b11`'s complex-plane gap view |
| `b11 → Chapter C` | scalar score complete → representations are vectors | leave the scalar limitation visible; Chapter C should begin by projecting a cloud to a line and reusing this exact score, not by reteaching it |

### Transition implementation rule

Do not choose `clear_overlay()` merely because two neighboring scenes both
contain axes or a rig. A visual match cut is valid only when data, geometry,
colors, trackers, and visible overlays agree exactly. Otherwise use
`clear_beat()` and preserve continuity through the question/answer structure.

Potential scene merges are decisions to make after the script pass:

- `b03 + b04`: construction and naming are one continuous realization.
- `b05 + b06`: the universal anchor can be one more experiment on the same
  rig.
- the end of `b07` + opening of `b08`: finite probes becoming the complete
  curve is one continuous visual claim.

Do not merge solely to avoid a cut. Merge only when the two files are one
question on one apparatus.

## Script update sequence

The user will review one scene at a time. For each scene:

1. Agree on `viewer before`, `viewer after`, and the exit question.
2. Decide which existing claims and examples remain.
3. Rewrite the spoken passages in a working draft.
4. Move approved narration into the scene's `self.voiceover(...)` blocks.
5. Regenerate `SCRIPT_chapterB.md`; never treat hand edits there as final.
6. Read the outgoing scene and incoming scene together before proceeding.

After all scene scripts are approved:

1. update `build.sh` playback order;
2. update `tools/script_dump.py` playback order;
3. synchronize `PLAN.md`, `concepts.yaml`, `SOURCE_MAP.md`, and affected scene
   docstrings with the approved argument;
4. decide the three consolidation candidates above;
5. write beat-level animation plans against the final narration;
6. only then begin animation repair and reimplementation;
7. review every rebuilt boundary in the concatenated master, not only in
   isolated scene renders.

Two known metadata mismatches must be resolved during that synchronization:

- `concepts.yaml` currently labels the Gaussian characteristic function as an
  `exact_derivation`, and `SOURCE_MAP.md` says the video uses the ODE derivation.
  The present `b10` and this proposed arc omit the derivation. If that remains
  the decision, the proof-status records must say that the formula is stated as
  a known result rather than derived in the chapter.
- `concepts.yaml` currently links aliasing directly to the practical integration
  range. In the revised argument, aliasing motivates the need for the whole
  curve and the uniqueness question; low-frequency blindness and finite-sample
  noise motivate the practical weighting/range.

## Questions intentionally deferred to scene review

- Does `b00` need both constraint callouts, or can the differentiability
  requirement land more cleanly through the histogram failure?
- Does the exact two-point `φ(t)=cos t` example earn its runtime?
- Should symmetry remain in `b03` or move into `b05`?
- Should `b04` remain a separate file after the definition is rewritten?
- Should `b06` remain separate or become the final invariant experiment in
  `b05`?
- How much of the `1/N` high-frequency noise-floor calculation belongs in the
  main narration rather than on screen or in an appendix?
- Can `b09`, `b10`, and `b11` share one axes geometry strongly enough to support
  real continuity seams?

These choices can shorten or merge scenes, but none changes the protected
argument at the top of this document.
