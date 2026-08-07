# Rendered Explainer MP4 Review Specification

> **Status in this repo.** This is a **binding** specification, supplied by the
> project owner. It governs deliverable 10 of `EXPLAINER_PROCESS.md` and is the
> gate a chapter passes before it is called finished. The verification norms in
> `EXPLAINER_PROCESS.md` §8 (extract frames and look at them; a silent bug has
> no traceback) are the minimum; this document is the full standard.
>
> **Reviews are written down, not just performed.** Findings for a project live
> in `projects/<name>/RENDER_REVIEW.md`, one section per scene, in the §19
> output order. A scene with no entry there has not been reviewed.
>
> Companion: `NARRATION_SPEC.md` governs the spoken script (deliverables 7 and
> 9). This document governs what the finished file actually does.

This document governs the review of each rendered MP4 scene produced for a visual mathematical or technical explanation.

It complements the project’s source map, audience contract, concept graph, explanation path, scene graph, narration specification, and factual checks. Those documents describe what the scene is supposed to teach. This review determines whether the **rendered artifact actually teaches it**.

The reviewer must inspect the MP4 itself. Do not approve a scene merely because its code, plan, narration, or equations look correct.

A scene can be mathematically correct in source code and still fail because:

- the focal point is unclear;
- important text is unreadable;
- too many objects move at once;
- the visual and narration compete;
- an animation implies a false mathematical claim;
- the pacing leaves no time to understand a transition;
- the same point is repeated without adding understanding;
- the style feels tacky, gimmicky, derivative, or overly polished;
- persistent objects create clutter;
- a first-time viewer cannot tell what changed or why;
- an apparently minor rendering bug destroys the intended correspondence.

The final MP4 is the evidence.

---

# 1. Reviewer role

Act as an adversarial but constructive reviewer of a visual mathematical explanation.

Review the scene from four perspectives:

1. **First-time learner**  
   Does the scene teach someone who has the knowledge specified in the audience contract but does not yet understand the target concept?

2. **Mathematical reviewer**  
   Does the visual behavior support the exact claim being made, without suggesting a stronger or different result?

3. **Animation and visual-design reviewer**  
   Is attention controlled clearly? Does motion carry meaning? Is the composition restrained, coherent, legible, and free from gimmicks?

4. **Technical quality reviewer**  
   Does the final render contain clipping, timing errors, stale objects, unreadable labels, audio defects, visual artifacts, or resolution-dependent failures?

Do not merge these perspectives into a vague impression such as “looks good.”

Produce specific, timecoded evidence.

---

# 2. Required inputs

Use as many of the following as are available:

- the rendered MP4;
- the scene plan or scene graph;
- the explanation path;
- the audience contract;
- the final narration or transcript;
- the source map;
- the factual claims ledger;
- the preceding and following scenes;
- the target delivery resolution and frame rate;
- the animation source code;
- any automated narration or source-fidelity reports.

The MP4 is mandatory.

If some supporting input is missing, still review the MP4, but separate:

- what can be verified directly from the render;
- what depends on the missing plan, source, or transcript;
- what remains uncertain.

Do not infer that a planned event occurred merely because the plan says it should occur.

Do not infer that a mathematical claim is source-supported merely because it appears confidently in narration.

---

# 3. Non-negotiable review procedure

Do not review the video from a contact sheet alone.

Watch the complete MP4 several times in different modes.

## Pass 1 — Uninterrupted normal playback

Watch from beginning to end at normal speed with audio.

Do not pause.

Record:

- what you believe the scene is trying to teach;
- where your attention naturally goes;
- where you feel confused, rushed, bored, or visually overloaded;
- what conclusion you remember immediately afterward;
- whether the scene feels like one argument or a sequence of unrelated beats.

This pass measures the actual viewer experience.

Do not consult the plan until after recording this first impression when possible.

---

## Pass 2 — First-time learner reconstruction

Watch again with the audience contract in mind.

At each conceptual beat, answer:

- What objects does the viewer currently know?
- What new object or relation has just appeared?
- Why should the viewer care about this change?
- What should the viewer infer before the narration moves on?
- Could a qualified first-time viewer make that inference?
- Is a prerequisite being used before it is restored or taught?
- Does the scene expect knowledge that the audience contract did not grant?

At the end, write the learner’s likely mental-state sequence.

Example:

```text
Before:
The complex exponential is only notation.

After beat 1:
It is a unit arrow at angle tx.

After beat 2:
A sample set produces many arrows.

After beat 3:
The average arrow records their net alignment.
```

Flag any beat where the mental state does not meaningfully change.

---

## Pass 3 — Muted playback

Watch the MP4 without audio.

Determine:

- whether the visual sequence has a readable causal structure;
- whether changing and invariant quantities are distinguishable;
- whether the viewer can identify the focal point;
- whether equations arise from visible operations;
- whether labels and transitions make relationships explicit;
- whether motion is mathematically meaningful or merely decorative;
- whether the visual accidentally tells a different story from the narration.

The video does not need to be fully self-explanatory when muted. However, the geometry and object transformations should remain coherent.

If the visual becomes an arbitrary slideshow without narration, the scene may be relying too heavily on speech.

---

## Pass 4 — Audio-only review

Listen without watching, or review the transcript independently.

Determine:

- whether the reasoning path remains coherent;
- whether visual referents are identifiable;
- whether narration relies on unexplained “this,” “that,” or “here”;
- whether it describes obvious motion instead of mathematical meaning;
- whether it announces attention without specifying what matters;
- whether it contains pauses where the visual presumably needs time;
- whether the narration overclaims what the visual establishes;
- whether the voice pacing is natural rather than uniformly compressed.

The audio need not duplicate the animation, but it should preserve the logic if the viewer briefly looks away.

---

## Pass 5 — Frame-by-frame and slow playback

Inspect:

- every cut;
- every equation reveal;
- every label appearance;
- every transformation between representations;
- the maximum-complexity frame;
- the smallest essential text;
- the beginning and end of every camera move;
- the exact frame where the narration names an object;
- every moment where multiple objects overlap;
- every extreme value of an animated parameter;
- every scene teardown.

Review at slow speed and pause at the worst cases, not only representative frames.

Generated geometry often fails at extremes while looking correct in the middle.

---

## Pass 6 — Plan and source comparison

Only after independently reviewing the render, compare it against:

- the scene purpose;
- intended learner-before and learner-after states;
- visual translation rules;
- proof status;
- source-supported claims;
- narration constraints;
- expected duration;
- declared invariants;
- known risks.

Verify that the MP4 delivers each planned realization.

Do not reward the scene for material that exists only in the plan.

---

## Pass 7 — Context review

When adjacent clips are available, watch:

- the previous scene;
- the current scene;
- the next scene;

as one continuous sequence.

Check:

- whether the opening repeats the previous conclusion;
- whether symbols or objects change style or position without explanation;
- whether the scene assumes a visual state that was not preserved;
- whether the ending creates a real need for the next scene;
- whether several clips restate the same insight;
- whether repeated title cards or recaps make the chapter feel episodic rather than continuous.

A clip may work alone but fail in sequence.

---

# 4. Reconstruct the scene before judging it

Before scoring, write a compact reconstruction:

```yaml
scene_intent:
  target_realization:
  viewer_before:
  viewer_after:
  central_visual_operation:
  mathematical_claim:
  proof_status:
  invariant:
  changing_quantity:
  necessary_representations:
  intended_next_question:
```

Then compare this reconstruction against the supplied plan.

If your reconstruction differs substantially from the plan, one of the following is likely true:

- the render does not communicate the planned idea;
- the plan is ambiguous;
- the narration and visual disagree;
- the reviewer has found a first-time-viewer confusion.

Do not silently resolve the discrepancy in the plan’s favor.

---

# 5. Clarity review

Clarity is the primary gate.

A scene is unclear when a qualified first-time viewer cannot reliably determine:

- what the objects represent;
- what operation is being performed;
- why the operation is being performed;
- what changed;
- what remained fixed;
- which visual feature corresponds to the mathematical claim;
- what conclusion should be retained.

## 5.1 Object identity

For every visible object, ask:

- What does this object represent?
- Was that meaning established before it appeared?
- Does its appearance remain stable?
- Is it confused with another object of similar shape or color?
- Does it change role without an explicit transition?
- Does it disappear and later return in a way that breaks continuity?

Flag decorative or unexplained objects.

---

## 5.2 Focal point

At every moment, identify the intended focal point.

Then identify the actual focal point created by:

- motion;
- brightness;
- color;
- scale;
- central placement;
- text appearance;
- camera movement;
- audio emphasis.

If these disagree, the viewer’s attention is being misdirected.

Prefer one dominant focal event per beat.

Two simultaneous changes are acceptable only when their correspondence is the point.

Three or more simultaneous changes require strong justification and explicit guidance.

---

## 5.3 Changing quantities and invariants

For each animation, name:

- what changes;
- what remains fixed;
- why that distinction matters.

The render should make both visible.

Example:

```text
Changes:
frequency t and each arrow’s phase.

Remains fixed:
the sample values on the number line.
```

Flag scenes where the viewer may believe the data, coordinate system, probability distribution, or reference object is changing when it is not.

---

## 5.4 Visual causality

A visual transition should communicate why one state leads to the next.

Flag teleportation:

- an equation appears with no construction;
- a point becomes a curve without tracing the correspondence;
- a high-dimensional object becomes a shadow with no visible projection;
- a sum appears without showing what is being added;
- a label changes while the object remains ambiguous;
- an old representation disappears before the new representation inherits its meaning.

Prefer morphs, traced links, persistent anchors, or brief overlap when they preserve identity.

Do not use transformation effects solely because they look smooth.

---

## 5.5 Multiple representations

When multiple panels or forms are visible, verify that the translation between them is explicit.

For every pair, state the rule:

```text
sample x
→ angle tx

angle tx
→ unit arrow e^(itx)

individual arrows
→ average arrow

average arrow coordinates
→ real and imaginary values of φ(t)
```

Flag a panel if:

- its input is unclear;
- its output is unclear;
- the timing does not reveal correspondence;
- it duplicates another panel;
- the viewer is told to watch everything at once;
- a visual link exists only in narration and not on screen;
- it displays a reduced quantity while the narration speaks about the full object.

---

## 5.6 Equation legibility and timing

For every equation:

- Is it large enough at the target delivery size?
- Is it visible long enough to parse?
- Is it placed near the relevant object without covering it?
- Were its symbols introduced?
- Does each operation correspond to something visible?
- Does the equation appear before, during, or after its construction?
- Is the reveal timed to the narration?
- Does highlighting direct attention to the relevant term?
- Is an essential condition hidden in small text?
- Is the notation consistent with earlier scenes?

An equation should normally arrive when the viewer already understands the operation it compresses.

Flag formula dumps and decorative equations.

---

## 5.7 Readability at actual size

Inspect the MP4 at:

- the encoded resolution;
- the expected playback size;
- full-screen;
- a typical embedded-player size.

Do not approve text because it is readable in a zoomed crop.

Check:

- minimum text size;
- line thickness;
- superscripts and subscripts;
- decimal points;
- minus signs;
- Greek letters;
- low-contrast grid lines;
- labels over shaded regions;
- labels at frame edges;
- color distinctions after video compression;
- formula clarity during motion.

If the scene is a low-resolution draft, mark resolution-dependent findings and repeat the check on the final render.

---

## 5.8 First-time-viewer ambiguity test

List every plausible wrong interpretation.

Examples:

- the horizontal component is the whole complex value;
- increasing frequency always decreases magnitude;
- the animation proves convergence;
- random projections guarantee optimization success;
- the distribution itself moves when only a probe parameter changes;
- color indicates mathematical sign when it only indicates category;
- a sample average and population expectation are identical objects.

For every plausible misunderstanding, state:

- the timecode;
- what causes it;
- whether narration, animation, or both need revision;
- the smallest change that would prevent it.

---

# 6. Explanatory-value review

Every visual event must perform explanatory work.

## 6.1 Pen-and-paper survival test

Ask whether the conceptual beat could be reconstructed with a few drawings.

Then ask what the animation adds:

- continuity;
- dependence on a parameter;
- preservation of identity;
- accumulation;
- comparison;
- projection;
- cancellation;
- limiting behavior;
- a hidden invariant becoming visible.

If animation adds only polish, mark it as decorative.

Decorative animation is not always forbidden, but it must not consume attention, runtime, or stylistic weight needed by the argument.

---

## 6.2 Visual argument test

For each major claim, complete:

```text
The viewer sees ________.
This corresponds mathematically to ________.
Therefore the scene supports the claim that ________.
```

If the middle line cannot be completed precisely, the visual may be an analogy rather than an argument.

That is acceptable only if the proof status is labeled honestly.

---

## 6.3 Motivation test

For every unusual operation, ask:

- What problem has been established?
- Why does this operation address it?
- Could the operation feel arbitrary to a first-time viewer?
- Does the previous beat create the need for it?
- Is the motivation visible or merely asserted?

Flag scenes that perform a clever construction before the viewer feels the need for it.

---

## 6.4 Proof-status test

Classify each central result:

- exact derivation;
- full proof;
- proof sketch;
- theorem statement;
- intuition only;
- analogy;
- empirical demonstration.

Then inspect whether the MP4’s visual confidence matches that status.

Animation can falsely imply proof through:

- universal-looking parameter sweeps;
- one successful optimization trajectory;
- perfectly smooth convergence;
- examples without counterexamples;
- camera emphasis on a conclusion;
- phrases such as “therefore” or “this guarantees.”

Any mismatch is a blocker.

---

## 6.5 Edge-case and extreme-frame test

Inspect cases most likely to break the claim or the visual:

- zero;
- negative values;
- symmetric inputs;
- degenerate distributions;
- repeated points;
- high-frequency oscillations;
- realignment after cancellation;
- parameter endpoints;
- zero-length arrows or vectors;
- off-screen objects;
- maximum bar height;
- maximum label width;
- empty sets;
- near-overlapping curves.

Do not approve a parameter animation after viewing only its middle range.

---

# 7. Redundancy review

Redundancy is not merely repeated words.

A scene is redundant when time, motion, text, or representation is used without producing a new inference.

## 7.1 Conceptual repetition

Flag when the same learner-state transition occurs more than once.

Examples:

- explaining twice that complex numbers can be arrows;
- showing cancellation in several examples without adding a new case;
- restating that every distribution satisfies \(\varphi(0)=1\);
- repeating a previous scene’s conclusion as a new opening.

Repetition is justified when it changes level:

```text
visual observation
→ finite-sample equation
→ population equation
→ edge case
```

It is not justified when it simply restates the same idea.

---

## 7.2 Channel redundancy

Compare narration, text, and animation.

Flag when all three say exactly the same low-level thing.

Example:

- arrow visibly moves upward;
- label says “arrow moves upward”;
- narration says “the arrow moves upward.”

At least one channel should carry a relationship or implication.

Useful division:

- animation shows motion;
- on-screen text preserves notation or a conclusion;
- narration explains cause, invariant, or meaning.

---

## 7.3 Panel redundancy

For each panel, ask:

- What unique information does it provide?
- Is that information necessary at this moment?
- Could the panel appear only when relevant?
- Does it remain on screen after its role is finished?
- Is it competing with the active panel?

A persistent visual language is useful, but persistence must not become permanent clutter.

---

## 7.4 Motion redundancy

Flag:

- repeated wiggles or pulses;
- objects moving to locations they could already occupy;
- camera pans that reveal nothing;
- multiple easing stages for a simple transition;
- repeated emphasis animations;
- labels entering and exiting without need;
- decorative rotations;
- long transforms whose correspondence is already obvious.

Ask whether cutting the motion changes understanding.

---

## 7.5 Runtime compression test

Identify every interval that can be shortened without reducing:

- comprehension;
- inference time;
- equation-reading time;
- emotional contrast;
- necessary pause;
- narration naturalness.

Do not equate constant motion with good pacing.

Do not remove pauses needed for a viewer to inspect a visual relation.

Classify each cut suggestion:

- safe cut;
- likely cut;
- risky cut;
- do not cut.

---

# 8. Taste and tackiness review

“Tacky” is not a synonym for colorful or animated.

A scene feels tacky when stylistic choices draw attention to the production rather than the idea, or when emphasis is disproportionate to the mathematical event.

## 8.1 Common tackiness signals

Flag when unjustified:

- glows;
- neon outlines;
- particle effects;
- dramatic zooms;
- bounce or elastic easing;
- repeated overshoot;
- cinematic title reveals;
- lens-flare-like effects;
- excessive gradients;
- flashing colors;
- confetti-like motion;
- sound effects for ordinary algebra;
- meme-like reactions;
- exaggerated suspense;
- too many accent colors;
- every object receiving an entrance animation;
- text arriving word by word without pedagogical purpose;
- faux-handwritten emphasis added as decoration;
- constant camera motion;
- 3Blue1Brown mannerisms copied without need.

Do not ban an effect by name.

Ask:

- What does it direct attention to?
- What mathematical relation does it encode?
- Is the intensity proportional to the importance of the event?
- Would a quieter treatment communicate more clearly?
- Does the effect remain tasteful when repeated across a chapter?

---

## 8.2 Visual restraint

A strong scene typically has:

- a stable background;
- a small, consistent palette;
- one primary accent at a time;
- limited font and label styles;
- motion concentrated around the active relationship;
- persistent semantic color assignments;
- sufficient empty space;
- no unnecessary borders or panels;
- no visual element whose main role is “making the screen look full.”

Flag unused visual territory only when it harms balance. Empty space is not a defect.

---

## 8.3 Style consistency

Compare against the project’s established visual language.

Check:

- object colors;
- line weights;
- arrowheads;
- typeface and font sizes;
- equation style;
- panel margins;
- axis appearance;
- camera behavior;
- transition style;
- use of labels;
- semantic meaning of color;
- amount of motion.

A new style is allowed when a new semantic category requires it.

Do not invent a new visual motif for every scene.

---

## 8.4 Earned emphasis

List every moment of strong emphasis:

- bright color;
- sudden scale change;
- full-screen equation;
- camera zoom;
- long pause;
- isolated object;
- musical or vocal emphasis.

For each, ask whether the conceptual importance earns it.

If every beat is emphasized, nothing is emphasized.

---

# 9. Cognitive-load review

## 9.1 Simultaneous novelty

Count how many of the following are new in each beat:

- object;
- symbol;
- color meaning;
- coordinate system;
- panel;
- parameter;
- equation;
- motion rule;
- theorem;
- narration term;
- visual metaphor.

Flag beats that introduce several central items at once.

A dense scene may be acceptable for an expert audience, but the burden must match the audience contract.

---

## 9.2 Split attention

Flag when the viewer must repeatedly look between distant areas to assemble one relationship.

Ask whether:

- corresponding objects can be closer;
- a temporary link line can connect them;
- one panel can be enlarged while others dim;
- labels can move nearer the relevant marks;
- the equation can be built beside the visual source;
- simultaneous animation can become sequential.

Do not solve all split-attention problems with arrows and labels; excessive connectors create clutter.

---

## 9.3 Transient information

Animation disappears.

Check whether important intermediate states remain visible long enough to compare.

Flag when:

- an old state vanishes before the new state can be interpreted;
- a parameter value changes before the viewer reads it;
- an equation is transformed too quickly;
- a conclusion appears briefly and is immediately replaced;
- a long narration refers to an object that has already left the screen.

Use persistent anchors, ghosts, traces, or pauses only when comparison requires them.

---

## 9.4 Narration–visual competition

Flag moments when:

- narration introduces one idea while the animation demonstrates another;
- an equation must be read while the voice explains a separate concept;
- several labels appear during a dense verbal sentence;
- the viewer is asked to inspect a curve while listening to a proof qualification;
- animation continues through a sentence whose precision requires concentration.

The visual and narration should either reinforce one idea or deliberately divide labor without competing.

---

# 10. Pacing and synchronization review

## 10.1 Event timing

For every narrated reference, verify that the object:

- already exists;
- is visible;
- is not covered;
- remains present long enough;
- changes at the expected word or phrase.

Record timing mismatches in milliseconds or frames when possible.

Examples:

- narration says “horizontal component” before it is drawn;
- an equation appears after its explanation;
- a highlight ends before the relevant phrase;
- the next animation begins before the current sentence resolves;
- a bookmark causes an abrupt or unnatural pause.

---

## 10.2 Comprehension pauses

A pause is useful when the viewer needs to:

- compare two states;
- read an equation;
- predict an outcome;
- recognize cancellation;
- inspect an edge case;
- absorb a conclusion.

A pause is dead air when nothing new can be inspected and no tension is being held.

Do not judge silence only by duration. Judge whether the frame supports active thought.

---

## 10.3 Voice pacing

Check:

- speech rate;
- phrase boundaries;
- breath placement;
- emphasis;
- monotony;
- unnatural acceleration;
- overlong pauses caused by bookmarks;
- words cut by transitions;
- equation reading;
- pronunciation of symbols and names.

The voice should not sound as if it is racing to keep up with animation or waiting for animation to finish.

---

## 10.4 Scene opening and closing

The opening should rapidly establish:

- continuity from the previous scene;
- the active object;
- the current question.

Avoid restarting the chapter in every clip.

The closing should:

- leave the final realization visible;
- avoid a slogan-like summary;
- create a genuine next question when appropriate;
- avoid clearing the frame before the idea lands;
- avoid holding a crowded final state too long.

---

# 11. Mathematical–visual consistency review

For every mathematical object, verify that its visual encoding is faithful.

Examples:

- complex value: both real and imaginary components are preserved when required;
- vector magnitude: not confused with horizontal coordinate;
- expectation: not visually confused with a single sample;
- projection: direction and normalization are correct;
- covariance eigenvalues: scale and orientation correspond to the cloud;
- distribution: not represented as a finite sample without qualification;
- integral: area depiction matches weighting and bounds;
- optimization: one trajectory is not narrated as a guarantee;
- asymptotic behavior: not shown as monotonic if oscillation is possible;
- theorem: examples are not presented as proof.

Flag every place where a visual simplification removes information later required by the conclusion.

---

# 12. Accessibility and robustness review

Check:

- essential distinctions do not rely on color alone;
- contrast remains sufficient under compression;
- labels accompany color-coded curves;
- red/green are not the sole opposing categories;
- thin lines survive at delivery size;
- narration names essential visual distinctions;
- rapid flicker is absent;
- text is not placed at unsafe frame edges;
- subtitles, if present, do not cover equations;
- symbols are pronounced clearly;
- the scene remains understandable on a small screen.

Optional but useful:

- inspect in grayscale;
- inspect with simulated color-vision deficiency;
- inspect at reduced playback size;
- inspect one compressed re-encode.

---

# 13. Technical render integrity

Inspect for silent failures.

## Geometry and layout

- clipped text;
- off-screen labels;
- objects beyond safe margins;
- formulas covering marks;
- axis labels inside shaded regions;
- line or bar heights exceeding the frame;
- inconsistent scaling;
- excessive empty margins caused by bad camera framing;
- elements becoming too small after a zoom-out;
- 2-D overlays drifting in 3-D scenes;
- labels detached from moving objects.

## Animation state

- stale `always_redraw` objects;
- updaters continuing after teardown;
- duplicate objects left after transforms;
- ghost elements;
- objects snapping at the final frame;
- trackers wrapping incorrectly;
- transforms leaving both source and target;
- partial fades;
- lingering dots, lines, or labels;
- unexpected z-order changes;
- camera interpolation jumps.

## Video

- frame drops;
- duplicate frames;
- tearing;
- aliasing;
- severe compression;
- inconsistent frame rate;
- black frames;
- abrupt cuts;
- wrong aspect ratio;
- letterboxing;
- broken transparency;
- incorrect duration.

## Audio

- clipping;
- distortion;
- background noise;
- inconsistent loudness;
- abrupt edits;
- truncated words;
- long accidental silence;
- room-tone changes;
- voice changes across clips;
- desynchronization;
- excessive timing drift;
- poor pronunciation;
- audio ending before or after the visual.

## Export

Verify:

- target resolution;
- target frame rate;
- audio sample rate;
- channel configuration;
- correct scene version;
- no draft watermark or low-resolution assets;
- final font rendering;
- correct color space where relevant.

---

# 14. Review against the plan

For each declared scene requirement, mark:

- `DELIVERED`;
- `PARTIALLY DELIVERED`;
- `NOT DELIVERED`;
- `CONTRADICTED BY RENDER`;
- `NOT VERIFIABLE`.

Required comparison fields:

```yaml
plan_compliance:
  target_realization:
  learner_before_to_after:
  visual_translation_rules:
  invariant:
  changing_quantity:
  equation_reveal:
  proof_status:
  misconception_prevention:
  duration:
  transition_to_next_scene:
```

Do not use the plan as a reason to excuse an unclear render.

The viewer does not see the plan.

---

# 15. Scoring

Score the MP4 out of 100.

## Explanatory clarity — 20

- object meanings;
- operation clarity;
- focal control;
- first-time-viewer comprehension;
- absence of plausible false interpretations.

## Visual reasoning — 15

- animation performs mathematical work;
- visible operations correspond to equations;
- causal transformations are clear;
- proof status is respected.

## Narration–visual coordination — 15

- timing;
- division of labor;
- precise attention guidance;
- no channel conflict;
- clear visual referents.

## Mathematical and source fidelity — 15

- claims are correct;
- conditions are preserved;
- representations retain necessary information;
- examples do not overclaim;
- theorem boundaries are honest.

## Cognitive load and representation management — 10

- controlled novelty;
- readable multi-panel structure;
- explicit translations;
- limited split attention;
- sufficient persistence.

## Pacing and non-redundancy — 10

- no conceptual repetition;
- no unnecessary motion;
- sufficient inference time;
- efficient scene opening and closing.

## Visual taste and consistency — 10

- restrained emphasis;
- coherent palette;
- consistent visual language;
- absence of gimmicks;
- production choices serve the idea.

## Technical integrity and accessibility — 5

- no clipping or artifacts;
- readable at delivery size;
- audio quality;
- robust color and labeling.

Report category scores with evidence.

Do not provide only a total.

---

# 16. Automatic blockers

The scene cannot be approved while any of these remain:

- a mathematical error;
- a source-fidelity error affecting the central claim;
- an animation implying a stronger theorem or guarantee than supported;
- an essential equation or label unreadable at delivery size;
- a missing representation component required by the conclusion;
- a narration–visual contradiction;
- a first-time viewer cannot identify the main operation;
- a high-severity false inference remains plausible;
- an essential object is clipped or hidden;
- audio is unintelligible or materially out of sync;
- a rendering artifact changes the mathematical meaning;
- the scene’s learner-after state is not achieved;
- the clip is the wrong version, resolution, or duration.

A high numeric score cannot override a blocker.

---

# 17. Severity levels

Use:

## BLOCKER

The scene is mathematically wrong, materially misleading, unintelligible, technically broken, or fails its core teaching goal.

## HIGH

A large fraction of first-time viewers are likely to misunderstand, miss, or falsely generalize the main point.

## MEDIUM

The scene remains usable, but clarity, pacing, legibility, style, or continuity is significantly weaker than intended.

## LOW

A local polish issue with limited effect on understanding.

## NOTE

A defensible choice, tradeoff, or future improvement that does not require revision.

---

# 18. Required timecoded findings format

For every substantive finding, provide:

| Time | Category | Severity | Evidence | Viewer consequence | Recommended fix |
|---|---|---|---|---|---|

Do not write:

> The scene is a little cluttered.

Write:

> **00:38.2–00:43.6 — Split attention — HIGH.** The real and imaginary curves begin drawing while the formula appears beneath the center panel and the frequency value continues changing above it. The viewer must read three new mappings simultaneously. Freeze \(t\), build the formula first, then resume the sweep with the formula dimmed.

Use exact time ranges whenever possible.

---

# 19. Required review output

Produce the report in this order.

## 1. Verdict

One of:

- `APPROVE`;
- `APPROVE WITH MINOR CHANGES`;
- `REVISE`;
- `REBUILD`.

Include one sentence explaining why.

---

## 2. Reconstructed teaching goal

State what the MP4 actually appears to teach before consulting or quoting the plan.

---

## 3. First-time-viewer experience

Describe:

- the likely mental-state progression;
- the strongest moment;
- the first point of confusion;
- the most likely false inference;
- what the viewer is likely to remember.

---

## 4. Blockers

List blockers first.

If none, say explicitly:

> No automatic blockers found.

---

## 5. Timecoded findings

Use the required table.

Separate:

- clarity;
- mathematical meaning;
- pacing;
- redundancy;
- taste;
- technical defects.

---

## 6. Plan-compliance table

Mark each planned requirement.

---

## 7. Redundancy and cut report

Identify:

- repeated ideas;
- unnecessary persistent elements;
- safe cuts;
- risky cuts;
- moments that need more time rather than less.

---

## 8. Visual-taste report

List:

- tacky or gimmicky effects;
- overemphasis;
- inconsistent styling;
- unearned camera movement;
- clutter;
- any element that looks impressive but does not teach.

Also list tasteful choices worth preserving.

---

## 9. Clarity stress test

Answer:

- What changes?
- What stays fixed?
- What is the viewer supposed to infer?
- Which equation corresponds to the visual operation?
- What could be misunderstood?
- Does the scene establish or merely assert the conclusion?

If any answer is unclear, the scene needs revision.

---

## 10. Scorecard

Report all eight category scores.

---

## 11. Required changes

Give a prioritized checklist.

Use exact actions:

- delete;
- shorten;
- hold;
- dim;
- enlarge;
- relabel;
- move;
- reorder;
- split;
- merge;
- redraw;
- change narration;
- add a link line;
- replace the example;
- qualify the claim.

Avoid vague recommendations such as “make it clearer.”

---

## 12. Optional polish

Keep separate from required fixes.

---

## 13. Revised scene outline

When the verdict is `REVISE` or `REBUILD`, provide a corrected beat-by-beat outline.

Do not rewrite the entire project plan unless requested.

---

# 20. Reviewer behavior constraints

Do not:

- praise the scene before identifying whether it works;
- accept the plan’s explanation of what the viewer “should” understand;
- treat smooth animation as evidence of good explanation;
- assume that more motion is better;
- recommend flashy effects to solve an attention problem;
- demand constant novelty;
- penalize quiet or simple scenes for lacking spectacle;
- rewrite the narration when the real problem is visual;
- propose visual changes for a mathematical problem that requires changing the reasoning;
- use “tacky” as an unexplained judgment;
- approve unreadable material because it is visible when zoomed;
- rely only on automated scene detection or contact sheets;
- report only style issues while missing mathematical implications;
- say “everything looks good” without timecoded evidence;
- invent source claims or intended meanings.

Do:

- preserve strong choices;
- distinguish local defects from systemic ones;
- prefer the smallest repair that restores the reasoning;
- recommend a rebuild when local edits cannot fix the conceptual structure;
- evaluate the final delivery render again after revision.

---

# 21. Final acceptance checklist

A scene is ready only when all are true:

- [ ] The target realization is identifiable from the MP4.
- [ ] The learner-before state can plausibly become the learner-after state.
- [ ] Every essential object has a stable, understood meaning.
- [ ] The viewer knows what changes and what remains fixed.
- [ ] Each major visual action corresponds to mathematical reasoning.
- [ ] Multiple representations have explicit translation rules.
- [ ] Equations arrive from visible operations.
- [ ] No visual implies a stronger result than the source supports.
- [ ] No high-severity false inference remains plausible.
- [ ] Narration and animation are synchronized.
- [ ] The viewer has time to inspect essential changes.
- [ ] No concept is repeated without adding depth.
- [ ] Every persistent panel or label still has a role.
- [ ] Strong emphasis is earned.
- [ ] The visual style is restrained and consistent.
- [ ] Essential text and curves are readable at target size.
- [ ] Color is not the only carrier of essential meaning.
- [ ] Extreme parameter values have been inspected.
- [ ] Scene teardown leaves no stale objects.
- [ ] Audio is clear, consistent, and correctly timed.
- [ ] The final encoded file has the intended resolution, frame rate, and duration.
- [ ] The report contains no unresolved blocker.
- [ ] The revised render has been reviewed again, not approved from code changes alone.

---

# 22. Initial instruction when an MP4 is supplied

Begin approximately as follows:

> I will review the finished render rather than trusting the plan or source code. I will first watch it uninterrupted as a new viewer, then inspect it muted, audio-only, frame by frame, and against the scene plan. I will report timecoded clarity, mathematical, pacing, redundancy, taste, synchronization, accessibility, and technical findings. I will separate blockers from optional polish.

Then perform the review.

Do not begin by summarizing the plan.

Do not approve the scene before watching the full MP4.

Do not treat the review as a general discussion. Produce an actionable QA report.
