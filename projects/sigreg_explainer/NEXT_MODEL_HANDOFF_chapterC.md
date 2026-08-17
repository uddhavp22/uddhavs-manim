# Chapter C production handoff

This is the canonical handoff for continuing the SIGReg explainer after
Chapter B. It collects the durable lessons from the Chapter B review cycle and
turns them into a script, storyboard, animation, and implementation contract
for Chapter C.

The goal is not to imitate the surface of a 3Blue1Brown video. The goal is to
adopt the underlying discipline: create a need for each idea, let the viewer
reason from a concrete visual, preserve object identity, and make every spoken
sentence arrive with the visual evidence that supports it.

## Current production status — 2026-08-16

This section supersedes the stale implementation-state wording in §2 below.
The protected idea arc and style contract remain binding.

- C01–C03 are implemented after the 2026-08-12 owner-directed motion and
  redundancy pass. The narration assumes the viewer knows vectors and
  projection; it does not teach coordinates again.
- C01 now opens on the Epps–Pulley equation Chapter B established, followed by
  two compact, genuinely computed examples: a Gaussian-shaped batch scores
  `0.063`, while a two-mode batch scores `3.581`. It then runs seven large
  individual 5×7 digits at a readable pace through a `35 → 8 → 6 → 8` network
  ported from the visual grammar of 3Blue1Brown's 2017 neural-network scenes;
  the compact fifteen-image batch appears only after that loop. Literal pixels correspond to the 35 input
  neurons, every layer changes activation, and a restrained blue wave crosses
  each complete edge group under continuing narration. The output head begins
  with one centred neuron, grows smoothly through `D=2` and `D=3`, then
  continues through `D=4,6,8` without an abrupt return cut. The geometry stays
  explicitly marked as the visible `D=3` preview while the wider heads establish
  practical scale. There is no matrix panel and no early `Z`: the diagram clears
  into the centred 3-D cloud, and only then is the cloud named `Z`. Narration
  calls the result only **the score**; `T` is not spoken because it is too easily
  confused with frequency `t`. The narration now says “a neural network
  produces those numbers” instead of asking ElevenLabs to pronounce “encoder”;
  the final voice was regenerated after the earlier pronunciation proved
  unreliable. The scene ends by simply adopting the standard Gaussian in `D`
  dimensions as the desired target, not by posing a question.
- C02's narration is 476 spoken words after the 2026-08-16 owner critique and
  is now a concrete visual argument,
  not a caption-led summary. It starts on C01's exact fifteen points, completes
  the cloud under narration, and walks ball → sheet → line → point with a
  compact `rank(Z)=3→2→1→0` readout. Representation collapse is named once in a
  separate clean narration beat at rank zero; the previous input-card/network
  detour was removed because Chapter A owns the full model-failure explanation.
  The scene now motivates the target
  twice: it cites LeJEPA's downstream-risk result, then unpacks
  `z*~N(0,I_D)` as zero mean and identity covariance while one compact green
  direction remains inside the amber target and sweeps through genuine 3-D
  orientations as unit variance is spoken. The connective wording
  makes the consequence explicit: if the direction turns and the target stays
  unchanged, then no direction is preferred. The future-video sentence now
  immediately follows and qualifies the LeJEPA downstream-task claim; “For
  now” then leads directly into mean zero and unit variance. Before any
  squared-distance pair appears, the narration asks how to make the blue batch
  match the amber target and creates a loss that measures that mismatch; the
  blue batch, amber target, and `L_match(Z)` pulse in sync.
  The failed pointwise objective is built from one example before it is
  repeated: the blue `z_i` is isolated when named, its sampled amber
  `z_i^star` appears on the next spoken clause, and the squared-distance arrow
  waits for “pair.” Only then do thirteen faint additional pairs appear.
  Resampling changes only the amber points and arrows. When the narration first
  says there are infinitely many possible draws, thirty amber candidates and
  faint lines rapidly accumulate instead of showing only three alternatives.
  The expectation beat explicitly replaces listing every possible draw with
  calculating an expectation under the target, states that the possible draws
  form an infinite continuum independent of batch size `N`, fixes one
  embedding, and visibly accumulates 48 possible Gaussian partners around it.
  The known target moments make the expectation
  analytically evaluable; the narration does not falsely call this a
  Gaussian-only capability or claim Monte Carlo approximation is impossible.
  Those arrows contract to one origin-directed average before the algebra is
  built in a separate lower panel. The square is expanded explicitly; the
  cross term vanishes because `E[z*]=0`, and `E||z*||²=D` follows from `D`
  unit-variance coordinates before the simplified identity and pointwise
  minimum appear. The algebra remains tied to the cloud with a blue radius,
  pulses on the amber target draws and origin, and a final field of red arrows
  showing the independently origin-directed pointwise minima. There are no
  decorative top captions or equation/arrow overlaps. The final conclusion
  calls this the wrong loss because every embedding is pulled toward zero,
  then distinguishes that pointwise collapse from matching the batch
  distribution.
- C03 is now a 358-word pedagogical construction rather than a notation-first
  summary. It opens by visibly contrasting the scalar batch Epps--Pulley needs
  with the vector batch the model supplies, then shows the required
  `R^D -> R` bridge. The displayed direction arrow is exactly one visible axis
  unit long and carries `||u||=1`; a thinner line, rather than a stretched
  arrow, spans the cloud. Narration
  explains that normalization prevents the choice of direction from also
  rescaling the projected numbers. One isolated embedding is dropped
  perpendicularly first, its signed coordinate `u^T z_i = +1.93` is read. A
  point on the opposite side is then projected to `u^T z_j = -1.53`, so the
  sign explanation has a visible example. Only then are the same operation and 44 representative guide lines extended
  to the full 220-point batch. The projected dots preserve object identity as
  they become the scalar batch and enter the full Epps--Pulley mechanism. A
  visible `t` readout completes the empirical characteristic function before
  the standard-normal curve appears on its spoken clause. A separate moving
  instantaneous-gap marker then sweeps the completed curves, progressively filling the
  weighted discrepancy, and computed result `0.055` appear on their narrated
  clauses. The discrepancy clears before the score appears. The rig then
  contracts into the restored 3-D experiment: two camera moves accompany real
  changes in direction, every shadow point moves, and the exact displayed
  scores change from `score(u_1)=0.055` to `score(u_2)=0.046` and
  `score(u_3)=0.872`. Those numbers remain visual examples rather than a spoken
  roll-call, and the ending now contrasts evidence about one shadow with a
  conclusion about the whole cloud.
  Fixed-orientation cloud objects and fixed-frame rig objects must be
  explicitly unregistered during ownership changes or they bleed through the
  composition under Cairo.
- `SCRIPT_chapterC.md` is now generated from C01–C03. Continue regenerating it
  after narration changes; do not edit it by hand.
- C01 and C02 have authorized final ElevenLabs/1920×1080/60 deliveries. C02's
  former final was superseded by the 2026-08-16 owner-directed rewrite, and the
  rewritten scene was rerendered with Archer after owner approval. C03's
  owner-authorized final ElevenLabs/1080p pass is complete.
- C01's delivered ElevenLabs file is
  `media/videos/sigreg_explainer/chapterC/c01_vectors/1080p60/C01.mp4`
  (46.22 s, H.264 1920×1080 at 60 fps, AAC 48 kHz stereo).
- C02's delivered ElevenLabs file is
  `media/videos/c02_the_shape_is_the_goal/1080p60/C02.mp4`
  (163.87 s, H.264 1920×1080 at 60 fps, AAC 48 kHz stereo, Archer voice).
- C03's delivered ElevenLabs file is
  `media/videos/c03_one_shadow/1080p60/C03.mp4`
  (112.77 s, H.264 1920×1080 at 60 fps, AAC 48 kHz stereo, Archer voice).
- Validation: the current files pass `py_compile`; `preflight` reports no
  undefined names; narration audit passes every budget (974 spoken words total,
  C01 140, C02 476, and C03 358); ffmpeg's `-45 dB`/2.2 s silence scan reports no
  qualifying dead air; complete ffmpeg
  decodes pass;
  and `facts.py` passes 24/24. The last fresh Pyright CLI run reported 0 errors and only the three
  intentional Manim wildcard-import warnings; Pyright was not installed in the
  final render shell, so do not represent that earlier run as post-render.
- Serena/editor language-server results may remain stale until the editor's
  language server is restarted. Use a fresh Pyright CLI run as the authority.
- The primary source tutorial was re-read on 2026-08-15 for C02's target and
  pointwise-expectation claims, and on 2026-08-12 especially for §§4–5.
  Its reduction order is binding: one-dimensional `𝒯` → projections `uᵀZ` →
  every direction / Cramér–Wold → `M` sampled directions, with quadrature `K`
  introduced only when computation requires it. Do not pull C06–C08's results
  into C01–C03.
- Next implementation work begins at C04. Do not reopen C01–C03 unless a new
  rendered observation identifies a regression.

Relevant 3Blue1Brown source patterns were consulted in the local source tree,
with C01 now specifically grounded in `_2017/nn/part1.py::NetworkMobject`,
`MoreHonestMNistNetworkPreview`, `NetworkScene.feed_forward`,
`_2017/nn/part2.py::PreviewLearning.activate_network`, and `PixelsFromVect`.
The adopted ideas are literal pixel-to-input correspondence, connections
behind neurons, activation encoded by neuron fill, complete edge-group
propagation, and persistent output geometry. Syntax remains local Manim CE per
`MANIM_CE_VS_MANIMGL.md`.

## 1. Read these before changing Chapter C

These documents are binding unless the user explicitly overrides them:

- [`PLAN.md`](PLAN.md) — mathematical and chapter-level plan.
- [`SOURCE_MAP.md`](SOURCE_MAP.md) — claim boundaries and source discipline.
- [`ANIMATION_PLAYBOOK_chapterB.md`](ANIMATION_PLAYBOOK_chapterB.md) — proven
  Manim patterns and Chapter B visual language.
- [`CHAPTER_B_REVIEW_GUIDE.md`](CHAPTER_B_REVIEW_GUIDE.md) — review criteria
  learned during the scene-by-scene pass.
- [`../../docs/NARRATION_SPEC.md`](../../docs/NARRATION_SPEC.md) — narration,
  bookmarks, pauses, and anti-redundancy rules.
- [`../../docs/RENDER_REVIEW_SPEC.md`](../../docs/RENDER_REVIEW_SPEC.md) — render
  and audiovisual verification.
- [`../../docs/VISUAL_SYSTEM.md`](../../docs/VISUAL_SYSTEM.md) — typography,
  palette, spacing, and reusable visual conventions.
- [`../../docs/MANIM_CE_VS_MANIMGL.md`](../../docs/MANIM_CE_VS_MANIMGL.md) —
  translation guide for local 3Blue1Brown ManimGL references.

`SCRIPT_chapterB.md` is generated from the actual `voiceover()` calls. It is a
reference, not an editable source. Chapter C should eventually have the same
generated-script workflow.

## 2. Current state and immediate rule

Chapter C is not yet a finished production sequence. The only existing scene,
[`chapterC/c02_covariance.py`](chapterC/c02_covariance.py), is a visual
prototype: a 3-D point cloud changing between ball, pancake, rod, and point
configurations with an eigenvalue readout. Treat its useful geometry and
camera techniques as raw material, not as an approved script or scene order.

Do not polish that prototype in isolation. First approve the Chapter C causal
arc and scene boundaries. Then decide whether it remains `c02`, moves, splits,
or is replaced. Do not rename Chapter C files speculatively.

## 3. What Chapter B hands to Chapter C

The viewer already knows:

- a scalar batch of samples can be mapped to unit directions with
  `x_i -> exp(i t x_i)`;
- averaging those directions gives the empirical characteristic function;
- one frequency can be fooled, while the whole characteristic function is
  unique at the population level;
- a standard Gaussian has a known target characteristic function;
- squared fingerprint discrepancies can be accumulated and smoothly weighted
  into the Epps–Pulley statistic;
- an empirical Gaussian batch normally has a small positive score because of
  finite-sample variation.

Chapter C must reuse this knowledge instead of reteaching it. A brief visual
recall is useful; another explanation of wrapping, Euler's formula, histogram
gradients, or the Gaussian characteristic function is not.

The visual continuity should be literal:

```text
vector cloud -> one projected shadow -> familiar scalar samples
             -> familiar wrapping rig -> one scalar score
```

The Chapter B rig should look and behave like the same object when it returns.
Reusing its colors, scale, notation, and motion is more valuable than building
a novel version.

## 4. Protected Chapter C idea arc

This is the backbone to protect while writing scenes:

```text
We now have a smooth Gaussianity score for scalar samples.
        ↓
A learned representation gives one vector per sample.
        ↓
Matching or assigning a target to each vector is the wrong kind of goal;
Gaussianity is a property of the whole cloud.
        ↓
Take one direction u and project the cloud onto it: u^T z_i.
        ↓
Those projections are ordinary scalar samples, so Chapter B's score applies.
        ↓
But one projection can hide structure.
        ↓
Even checking the coordinate axes can fail:
Z = (X, X) has Gaussian coordinates but lies on a line.
        ↓
We need to inspect every direction.
        ↓
Cramér–Wold supplies the population-level reason:
all one-dimensional projections determine the joint distribution.
        ↓
For an isotropic Gaussian, every unit-direction projection is N(0,1).
        ↓
In practice, sample M directions and average their scalar scores.
        ↓
Approximate each scalar frequency integral with K knots.
        ↓
Assemble the SIGReg loss from operations the viewer has already seen.
        ↓
Show what it opposes: collapse and low-rank geometry receive a penalty.
        ↓
State the population-limit payoff and the finite-computation limits honestly.
```

Each beat must answer the question created by the beat immediately before it.
Do not present a chain of definitions that only becomes motivated later.

## 5. Recommended scene architecture

The exact numbering can change after storyboard review. The conceptual order
should remain stable.

### Scene A — Why vectors change the problem

Recall the scalar input `x_1, ..., x_N`, then transform each scalar into a
vector `z_i`. Use a compact morph inspired by the transformer embedding scenes:
the same sample objects acquire components and fan into a cloud.

The point is simple: Chapter B accepts one number per sample; the model now
hands us a vector per sample. Give this transition room to land.

### Scene B — The target belongs to the cloud

Show point, line, pancake, and roughly spherical clouds. If a Gaussian target
point is assigned independently to every embedding, the pairing is arbitrary
and can pull points in misleading ways. The desired geometry is a property of
the collection, not an identity assigned to an individual point.

Avoid claiming that a particular optimization trajectory is inevitable. This
scene motivates a distributional test; it does not prove training behavior.

### Scene C — Reuse the scalar score on one shadow

Introduce a unit direction `u`. Project every `z_i` to `u^T z_i`. Preserve
identity with guide lines or concurrent motion so the viewer sees each dot
become its own scalar shadow. Then hand those shadows to the familiar Chapter
B rig.

This is the key continuity payoff. Keep narration light and let recognition do
the work.

### Scene D — One shadow can be fooled

Rotate `u` around a structured cloud. Some directions reveal separation or
collapse; another can make the projection look innocuous. The direction must
visibly control the shadow through one shared tracker.

### Scene E — Coordinate checks still miss dependence

Use `Z = (X, X)`. Both coordinate projections are Gaussian, yet the points lie
on a diagonal line. Reveal this in the order:

1. inspect the horizontal shadow;
2. inspect the vertical shadow;
3. pull back to the full cloud;
4. rotate to a diagonal direction that exposes the dependence.

Let the viewer notice the line before stating the conclusion.

### Scene F — Every direction determines the cloud

Now name the need: inspect all directions. Cite the Cramér–Wold theorem without
pretending to prove it. For a standard multivariate Gaussian, every unit
direction gives a standard one-dimensional Gaussian. Therefore the Chapter B
score has the same target in every direction.

### Scene G — Replace all directions with sampled directions

The sphere of directions is conceptually continuous. Computation samples `M`
unit vectors, usually by normalizing Gaussian vectors. Show a few directions
first, then a rhythmic fan of many directions, then average their scalar
scores. Introduce `M` only at this moment.

### Scene H — Replace each integral with frequency knots

Return to one familiar scalar score. Replace the continuous frequency sweep by
`K` sampled knots. Show a modest number such as `K=16` tracking the continuous
result closely before mentioning the denser reference. Introduce `K` only when
the integral becomes a computation.

Do not reopen the Chapter B debate over hard bounds versus smooth weights. Use
the approved scalar statistic as a component and focus on its discretization.

### Scene I — Assemble SIGReg

Build the formula in the same order as the visible operations:

```text
project -> scalar Gaussianity score -> repeat over directions -> average
```

Every symbol should arrive beside the object or operation it denotes. The
formula is the compression of a process the viewer already understands, not a
new object dropped onto the screen.

### Scene J — What the loss can and cannot claim

Use the covariance/eigenvalue prototype as evidence that collapsed and
low-rank clouds are penalized. A progression such as `(1,0,0) -> (1,1,1)` may
illustrate a desired direction of change, but never narrate it as a guarantee
of gradient-descent convergence or absence of local minima.

In the population/all-directions limit, zero Epps–Pulley score on every
projection plus Cramér–Wold implies `Z ~ N(0, I_D)`. With finite `N`, `M`, and
`K`, the implementation is an estimator. End with that honest distinction and
the next concrete question, not with a generic chapter announcement.

## 6. How the user wants ideas framed

### Use a causal thought process

The preferred structure is:

```text
problem -> experiment -> observation -> conclusion -> next need
```

Useful connective language includes “if,” “then,” “now,” “suppose,” “notice,”
and “so.” Use them to express real logic, not as decorations on every sentence.
If a sentence begins with “so,” it should actually land a consequence.

Strong pattern:

> If we look only along this direction, the cloud becomes an ordinary batch of
> numbers. Then the score from Chapter B applies without changing it.

Weak pattern:

> The left panel shows the cloud. The line moves. The right panel shows the
> score.

The latter merely describes visible actions.

### Create desire before notation

Introduce an object in this order:

1. show the concrete problem;
2. let a natural attempt fail;
3. isolate the missing capability;
4. show the construction visually;
5. name and formalize it.

Do not announce “Cramér–Wold,” `M`, `K`, or the full SIGReg expression before
the viewer wants the idea each name compresses.

### Concrete first, notation last

Prefer:

```text
one cloud -> one shadow -> several shadows -> all directions -> notation
```

Avoid beginning with an expectation over directions and explaining its pieces
afterward.

### Ask only genuine questions

A question is useful when the visual lets the viewer predict or test its
answer. Do not end every scene with a rhetorical question, and do not use fake
suspense for a fact the narration immediately reveals.

### Do not narrate stage directions

Do not say “the left panel,” “the dots move up,” “the dotted line shows,” or
read labels that are already obvious. Narration should explain why an action
matters, what pattern to notice, or what follows mathematically.

Deictic words such as “this,” “here,” “now,” and “that direction” are allowed
only when the corresponding object is already present or begins changing on
that word.

### Avoid negative parallelism and canned contrast

The user dislikes constructions such as:

- “not X, but Y”;
- “this is a numerical choice, not a theorem”;
- “one thing stays, another changes” as generic filler;
- “the remaining step”;
- “the useful middle ground”;
- “constraint one / constraint two” as a pedagogical voice;
- “as you can see”;
- “we simply” when the step is not simple.

State the positive idea directly. If contrast is mathematically essential,
make it specific and earn it with the visual.

### Keep the voice human and economical

Use contractions and varied sentence lengths. Alternate exploratory sentences
with short landing sentences. Avoid dense prose written to resemble a paper,
and avoid repetitive scaffolding such as “This gives us...” at every beat.

The viewer should feel invited to reason, not managed through a checklist.

### Do not overclaim the scalar

At the beginning, frame the scalar as a score against a chosen target
distribution. The entire population characteristic function uniquely
determines a distribution; a single scalar generally does not identify every
arbitrary distribution. The special claim is:

```text
population score = 0
-> every tested characteristic-function discrepancy is 0
-> all projections match the Gaussian target
-> by Cramér–Wold, the joint distribution is N(0, I_D)
```

Finite empirical scores require calibration against sampling variation.

## 7. Mathematical claim ledger for Chapter C

Keep these distinctions explicit in code comments and narration drafts:

- Population characteristic function:
  `phi_X(t) = E[exp(i t X)]`.
- Empirical characteristic function:
  `hat(phi)_N(t) = (1/N) sum_j exp(i t x_j)`.
- For finite Gaussian samples, the empirical Epps–Pulley statistic is usually
  positive. “Near zero” means consistent with ordinary sampling variation,
  not an exact proof that the batch was generated by a Gaussian.
- A vector with Gaussian marginals need not be jointly Gaussian. `Z=(X,X)` is
  the required counterexample.
- Cramér–Wold says the collection of all one-dimensional projections determines
  a probability distribution. Cite it; do not claim it was proved onscreen.
- If `Z ~ N(0,I_D)`, every unit projection `u^T Z ~ N(0,1)`.
- Conversely, if every unit projection has the standard Gaussian law, then the
  joint law is `N(0,I_D)` in the population limit.
- Sampling `M` directions approximates the directional expectation. Increasing
  `M` reduces Monte Carlo variation; it does not turn a finite batch into a
  proof.
- Sampling `K` frequency knots approximates the scalar integral.
- The `K=16` versus dense-reference accuracy claim may be shown only with the
  exact experimental setup/source recorded in `SOURCE_MAP.md`.
- SIGReg's zero-at-population result describes global optima. Do not infer
  convergence rate, optimization dynamics, uniqueness of parameter values, or
  absence of local minima.

When a scene uses a theorem, mark it as a cited result. When it shows an
experiment, call it evidence or an example rather than a proof.

## 8. Visual grammar to preserve

### Stable meanings

Use the project palette, but preserve these semantic roles across scenes:

- sample/cloud data: blue;
- contrasting or non-Gaussian data: coral/red;
- average/result vector: purple;
- target, parameter, or active emphasis: yellow only when genuinely active;
- axes, inactive labels, and structural furniture: gray/white.

Do not color every equation or sentence yellow. Color should answer “what is
active?” rather than decorate the frame.

If Chapter C needs new colors for projection direction or per-direction score,
assign them once in the storyboard and keep them stable.

### Preserve object identity

When a cloud becomes a shadow, each point should visibly remain the same point.
Use concurrent transforms, guide lines, or temporary trails. Avoid fading one
set out and independently creating another set that only happens to have the
same count.

When a scalar batch enters the Chapter B rig, reuse or transform the projected
dots; do not spawn duplicates that create ghost points.

### Center the active idea, not the bounding boxes

Check the rendered visual center, including labels and tall dot stacks. Do not
leave a large unused lower region while active objects crowd the middle. Keep
titles and equations clear of data, and leave enough clearance for the most
extreme animated state, not just the first frame.

### 3-D readability

For clouds:

- use modest ambient camera motion only when parallax adds information;
- keep projected shadows and current direction readable from the chosen angle;
- use billboarded or fixed-orientation dots carefully;
- do not allow depth sorting to make important points flicker;
- prefer one purposeful camera move over continuous ornamental rotation.

The existing covariance prototype's build-once mesh update is preferable to
reconstructing hundreds of spheres every frame.

### Typography and notation

Use project font helpers and Computer Modern conventions. Keep mathematical
symbols in `MathTex`; use prose text helpers for words. Do not mix font systems
casually.

Every curve must be identified precisely. Distinguish:

- `Re phi`;
- `Im phi`;
- the complex point `phi`;
- magnitude `|phi|`;
- Gaussian target;
- squared gap;
- direction-averaged score.

Avoid a generic label such as “the curve” when more than one of these is
present.

## 9. Rhythm, pacing, and scene transitions

The reliable beat is:

```text
introduce -> settle -> vary -> settle -> reveal the conclusion
```

The user repeatedly preferred rhythmic examples over long simultaneous
reveals. Show one or two examples with room to register them, then accelerate
the repeated pattern. A pause should leave an inspectable state, not an empty
frame.

Basic arrivals generally need about 0.5–1.0 seconds; a major conceptual morph
may need longer. Repeated examples can become faster once the grammar is
learned. Do not compensate for a wordy script by stretching every `Write`.
Tighten the language first.

### Transition contract

For every neighboring pair of scenes, write down:

1. the final spoken idea of scene A;
2. the final visible objects of scene A;
3. the first spoken idea of scene B;
4. the first visible objects of scene B;
5. which objects persist, transform, or disappear.

The next scene should continue the thought conversationally. It should not
restate the previous conclusion and then begin again. Cross-scene audio needs
short handles so concatenation never clips the first or last phoneme. Fades
should be quick when object identity continues and slower only when a genuine
reset is needed.

Do not render the master as a new monolithic animation if the build system is
defined to concatenate approved scene masters. Scene-level audiovisual sync
must survive the exact assembly path used for the final chapter.

## 10. Narration and animation synchronization

Chapter B repeatedly exposed a specific failure: correct words and correct
animations can still feel wrong when they are offset by half a beat.

Rules:

- Place a bookmark immediately before the noun or verb that triggers a visual.
- Start the animation on that bookmark, not after the sentence finishes.
- If narration says “this direction rotates,” rotation begins on “rotates.”
- If narration names a result, the result should be visible or completing its
  reveal on that phrase.
- Do not let a long `Write` trail behind the spoken sentence.
- Use one tracker as the source of truth for direction, projection, displayed
  value, curve marker, and score whenever they represent the same parameter.
- Continuous parameter sweeps may span narration; `Write`, `Indicate`, and
  `Circumscribe` should usually be short cue-bound actions.
- Add deliberate still frames before a dense explanation and after a payoff.
- Inspect the rendered MP4 with audio. Source timestamps alone are not proof
  of sync.

For ElevenLabs or any TTS voice, preview mathematical pronunciation before a
full render. Spoken text should be TTS-safe:

- say “sine,” “cosine,” and “the integral” in natural prose rather than asking
  the voice to infer pronunciation from raw LaTeX;
- say “x sub i” and distinguish an index from the imaginary unit when needed;
- separate ambiguous clauses with punctuation or a short bookmark pause;
- do not read every symbol already visible onscreen.

If a word remains mispronounced, use the project's pronunciation mechanism or
a narrowly written spoken alias while leaving the displayed mathematics
unchanged. Always listen to the generated clip.

## 11. Manim implementation patterns

### Prefer project infrastructure

Use the existing scene, typography, palette, layout, voiceover, and timing
helpers before adding new abstractions. Search the project with `rg` before
inventing a helper.

Expected patterns include:

- `ActScene`/project voiceover wrappers and bookmarks;
- project `Text` and palette helpers;
- `ValueTracker` plus derived geometry for a single changing parameter;
- `TransformMatchingTex` when a formula is genuinely being reorganized;
- `ReplacementTransform` when an object changes role but preserves identity;
- cleanup/freeze helpers for updater-driven objects before removal or scene
  handoff.

### One source of truth

For a direction `u`, derive from one tracker or one vector state:

- the arrow in the cloud;
- every projected scalar;
- guide lines;
- any direction label;
- the scalar-score readout.

Do not animate these independently. Independent animations drift and create
the sync errors seen during Chapter B.

### Use updaters selectively

`always_redraw` is appropriate for cheap, genuinely derived geometry such as a
projection line or moving marker. It is a poor choice for hundreds of 3-D
objects or complex TeX. Build expensive geometry once and update its points or
style.

Before transforming or removing updater-driven objects, freeze them into their
current geometry. Otherwise arrows lose tips, dots linger, colors flash, and
objects snap back to stale states.

### Animate a handoff, then enable live motion

For a cloud-to-shadow transition:

1. construct stable cloud points;
2. construct each target projection position;
3. animate the points and guide lines concurrently;
4. settle on the scalar line;
5. only then enable the tracker-driven rotation/projection updater.

This avoids the abrupt resets and duplicate-point ghosts that had to be fixed
repeatedly in Chapter B.

### Keep code proportional

Do not build a framework for a one-off movement. Extract a reusable rig only
when at least two Chapter C scenes need the same cloud/projection/score
contract. A likely useful abstraction is a small `CloudProjectionRig` with
stable access to cloud points, direction, scalar shadows, and guide lines; its
API should follow actual storyboard needs rather than anticipated ones.

### Verify numerical displays

Any displayed projection, eigenvalue, characteristic-function value, gap, or
loss must come from the same computation driving the geometry. Never hard-code
a label beside a separately evaluated animation. Check values at the visible
endpoints and several intermediate frames.

## 12. Local 3Blue1Brown references

These files are ManimGL references. Study their choreography and pedagogy, then
translate the pattern to Manim Community using
[`MANIM_CE_VS_MANIMGL.md`](../../docs/MANIM_CE_VS_MANIMGL.md). Do not paste
ManimGL syntax into this project.

Paths below are relative to the `uddhavs-manim/` repository root.

### Neural-network series — concrete example before abstraction

- `../3blue1brown_videos/_2017/nn/part1.py`
  - `PreviewMNistNetwork`
  - `IntroduceEachLayer`
  - `BreakUpMacroPatterns`
  - `IntroduceWeights`
  - `MotivateSquishing`
  - `IntroduceSigmoid`
  - `IntroduceWeightMatrix`
- `../3blue1brown_videos/_2017/nn/part2.py`
  - study the movement from one training example to cost over many examples;
    keep the concrete case alive while notation expands.
- `../3blue1brown_videos/_2017/nn/part3.py`
  - `InterpretGradientComponents`
  - `ShowAveragingCost`
  - `ConstructGradientFromAllTrainingExamples`
  - `SimplestNetworkExample`

Borrow these habits:

- isolate one neuron/example/component before showing the full system;
- vary inputs rhythmically after the visual grammar is understood;
- transform familiar objects into formula terms;
- create the need for a nonlinear or aggregate operation before naming it;
- use focus and dimming to control attention instead of adding labels.

### Transformer/deep-learning series — vectors, embeddings, and flow

- `../3blue1brown_videos/_2024/transformers/embedding.py`
  - `IntroduceEmbeddingMatrix`
  - `Word2VecScene`
  - `ThreeDSpaceExample`
  - `HighDimensionalSpaceCompanion`
  - `LearningEmbeddings`
  - `DotProducts`
  - `DotProductWithPluralDirection`
  - `SimpleSpaceExample`
  - `ManyIdeasManyDirections`
- `../3blue1brown_videos/_2024/transformers/network_flow.py`
  - especially `HighLevelNetworkFlow.show_initial_text_embedding` for
    token-to-vector identity, concurrent motion, and progressive system build.
- `../3blue1brown_videos/_2024/transformers/attention.py`
  - study one-query-at-a-time focus, routing, and selective dimming.
- `../3blue1brown_videos/_2024/transformers/mlp.py`
  - `BasicMLPWalkThrough`
  - `MatricesVsIntuition`
  - `StackOfVectors`
  - `ShowAngleRange`
  - `AlmostOrthogonal`
- `../3blue1brown_videos/_2024/transformers/ml_basics.py`
  - `PremiseOfML`
  - `CostFunction`
- `../3blue1brown_videos/_2024/transformers/generation.py`
  - use as a rhythm reference for repeated inputs and outputs.
- `../3blue1brown_videos/_2024/transformers/almost_orthogonal.py`
  - use for intuition about many directions in high-dimensional space.
- `../3blue1brown_videos/_2024/transformers/helpers.py`
  - inspect supporting patterns, but use local project helpers in production.

Borrow these habits for Chapter C:

- transform scalar samples into vectors without losing their identities;
- make dot products and projections spatial before writing `u^T z`;
- show one direction, then several, then the higher-dimensional generalization;
- keep the active vector brighter while surrounding structure recedes;
- use repeated examples as a visual rhythm, not a wall of simultaneous data.

### Fourier and gradient references — parameter sweeps and causality

- `../3blue1brown_videos/_2018/fourier.py`
  - study continuous tracker-driven wrapping, sweep traces, and how one moving
    parameter controls several synchronized representations.
- `../3blue1brown_videos/_2017/gradient.py`
  - study how local changes and gradients are made causal rather than merely
    decorative.

The production standard is behavioral inspiration: object continuity,
attention control, pacing, and idea order. Copying a complicated 3Blue1Brown
scene wholesale usually creates redundant code and mismatched visual grammar.

## 13. ManimGL-to-CE translation checklist

Before adapting a local 3Blue1Brown pattern:

1. identify the pedagogical behavior, not the class name;
2. find the CE equivalent in the project or Manim documentation;
3. replace GL-specific camera, updater, shader, and text APIs;
4. preserve local typography and palette;
5. verify updater cleanup and z-order explicitly;
6. render the exact motion at review quality;
7. compare the result frame-by-frame, not source-by-source.

If the source uses a custom shader or interactive camera feature, reproduce the
minimum visual behavior needed for the explanation. Do not import the entire
GL mechanism.

## 14. Production workflow for each Chapter C scene

1. **Write the pedagogical beat.** State the question inherited from the prior
   scene, the experiment, the observation, and the conclusion.
2. **Draft narration.** Remove panel descriptions, equation recitation,
   repetitive conclusions, fake questions, and negative parallelism.
3. **Storyboard persistent objects.** Record what enters, transforms, remains,
   and exits.
4. **Write the transition contract.** Include audio handles and the exact first
   and last frames.
5. **Implement the smallest working visual.** Reuse project helpers and one
   source of truth for linked motion.
6. **Generate voice audio.** Listen for pronunciation and revise spoken aliases
   before animating final timing.
7. **Sync by bookmarks.** Align actions to semantic words rather than guessed
   durations.
8. **Render the individual scene at review quality.** Low-resolution drafts
   are useful for iteration but do not replace visual review of the actual
   deliverable.
9. **Inspect frames and audio.** Check overlaps, centering, arrow silhouettes,
   dot size, color stability, and numerical agreement.
10. **Test the scene transition.** Concatenate adjacent approved scene files by
    the real master-build path and listen for clipped or crowded audio.
11. **Regenerate the script dump.** Confirm the generated script matches what
    the render actually says.

Do not build the full chapter before the script and idea order are approved.
Do not call a scene finished based only on a successful render.

## 15. Review checklist

### Story and narration

- Does the opening continue the preceding thought?
- Is the reason for the scene clear before notation appears?
- Does narration add meaning beyond visible motion?
- Are “if,” “then,” “now,” and “so” expressing real causal links?
- Is every question genuinely answerable from the visual?
- Are theorem statements and empirical observations distinguished?
- Is the spoken language natural and concise?
- Have TTS pronunciations been listened to, especially mathematical terms?

### Visuals

- Is the active idea centered with adequate clearance at every extreme state?
- Do points remain attached to the correct line, plane, or projection?
- Does object identity survive transformations?
- Are dots and arrow tips proportionate rather than oversized?
- Is purple reserved for the aggregate/result where that convention applies?
- Is yellow used for active emphasis rather than all text?
- Are full complex values, components, magnitudes, targets, and gaps visually
  distinct?
- Are labels useful, sparse, and non-overlapping?

### Motion and sync

- Does each action begin on the word that motivates it?
- Are parameter-linked elements driven by one source of truth?
- Are repeated examples rhythmic rather than sluggish?
- Is there breathing room after important observations?
- Are updaters frozen or removed cleanly before transforms?
- Do any objects flash, reset, duplicate, lose arrowheads, or change color?
- Does the first word of the scene and last word of the prior scene survive
  final concatenation?

### Mathematics

- Is the population/empirical distinction correct?
- Is one projection clearly insufficient?
- Is the Gaussian-marginal counterexample shown before Cramér–Wold?
- Are `M` and `K` introduced only when their approximations become necessary?
- Are numerical labels computed from the same state as the geometry?
- Are global-minimum claims kept separate from optimization claims?
- Are finite-sample limitations stated without undermining the construction?

## 16. First task for the next model

Before editing `c02_covariance.py`, produce a short Chapter C script/storyboard
using Sections 4 and 5. The first review should decide:

- how Chapter B's final scalar samples transform into vectors;
- where the cloud-geometry prototype belongs;
- the exact `Z=(X,X)` counterexample choreography;
- how the Chapter B rig returns after projection;
- where Cramér–Wold is named;
- how `M`, `K`, and the final SIGReg formula are revealed;
- how the chapter ends without overclaiming training behavior.

Once that arc is approved, implement scenes one at a time, render them
individually, and review each transition alongside the scene itself.
