# Natural Mathematical Narration Specification

> **Status in this repo.** This is a **binding** specification, supplied by the
> project owner. `EXPLAINER_PROCESS.md` §6 is a summary of it; **this file
> wins on any conflict about narration.** Deliverable 7 (draft narration) and
> deliverable 9 (revised narration) are written against §§1–30 here and audited
> against §31. `tools/narration_audit.py` mechanises the parts of §31 that can
> be counted — it is a *floor*, not the standard. A script can pass the audit
> and still fail this document, and when it does, this document is right.
>
> Companion: `RENDER_REVIEW_SPEC.md` governs the rendered MP4.
> Per-scene findings live in `projects/<name>/RENDER_REVIEW.md`.

This document governs the narration of visual mathematical and technical
explanations. Its purpose is to prevent narration that is technically correct
but recognizably machine-generated, overly polished, procedural, generic,
fragmented, or disconnected from the actual reasoning on screen.

This is not a request to imitate the wording, voice, mannerisms, or sentence
patterns of any particular educator.

The target is narration that sounds like a thoughtful mathematician or
scientist developing an idea naturally with the viewer:

- precise without sounding formal for its own sake;
- intuitive without replacing reasoning with metaphor;
- conversational without becoming casual filler;
- visual without merely describing animation;
- proof-like without reading like a textbook proof;
- economical without becoming a sequence of clipped fragments;
- confident without pretending every result is obvious;
- curious without manufacturing surprise.

Natural narration must be designed from the mathematical reasoning and scene
structure. It cannot be repaired reliably by replacing a few phrases during the
final editing pass.

---

# 1. The narration's job

Narration should perform one or more of the following functions:

1. establish a mathematical problem;
2. direct attention to a specific visual relationship;
3. state an observation;
4. explain why an operation is being performed;
5. connect a visual construction to notation;
6. justify a mathematical step;
7. distinguish what changes from what remains fixed;
8. connect the current idea to an earlier one;
9. identify the limits of an argument;
10. compress several observations into a reusable concept;
11. prepare a question that the next scene genuinely answers.

Every substantive sentence should have an identifiable function.

A sentence should normally be removed when it only:

- announces that an explanation is beginning;
- announces that the topic is important;
- promises that something will make sense later;
- tells the viewer that an idea is surprising;
- summarizes a point that was already stated clearly;
- labels a transition without advancing the reasoning;
- adds verbal energy without adding mathematical meaning.

Weak:

> Now that we have established the basic intuition, we can move on to the
> mathematical formulation.

This sentence only announces the organization of the explanation.

Stronger:

> The average arrow is already the quantity we need. Complex notation gives it
> a compact name.

The second sentence advances the argument.

---

# 2. Narrate the reasoning, not the lesson plan

Do not tell the viewer that they are being taught. Avoid repeatedly describing
the structure of the explanation:

- "First, we need to understand…"
- "Before we can continue…"
- "The next thing we need to do…"
- "Now that we understand…"
- "We will return to this later."
- "Let us begin with the intuition."
- "We can now introduce the formal definition."
- "This will become important shortly."

Occasional structural guidance is acceptable when the explanation genuinely
changes direction, but most transitions should emerge from the mathematical
need.

Weak:

> Before defining the characteristic function, we first need to understand
> complex exponentials.

Stronger:

> The expression $e^{itx}$ is a unit arrow whose angle is $tx$.

The stronger version begins with the mathematical object itself.

Weak:

> Now that we know what the arrows represent, let us average them.

Stronger:

> Each sample has supplied one direction. Their average records whether those
> directions reinforce or cancel.

This does not announce a new section. It explains why averaging follows.

---

# 3. Do not use "human-sounding" filler

Do not attempt to sound human by adding:

- casual asides;
- fake uncertainty;
- verbal hesitations;
- rhetorical filler;
- slang;
- unnecessary jokes;
- arbitrary personal opinions;
- repeated phrases such as "you know" or "basically."

Naturalness comes from the movement of thought, not from simulated
imperfections.

Weak:

> So, yeah, this is basically kind of like wrapping the line around a circle.

Stronger:

> Multiplying $x$ by $t$ turns its position on the line into an angle on the
> circle.

Do not deliberately insert grammatical mistakes, false starts, or filler words
to evade detection as machine-written text.

---

# 4. Begin with mathematical substance

Prefer openings that immediately create:

- an object;
- a situation;
- a visible discrepancy;
- a problem;
- a concrete example;
- a meaningful question.

Avoid abstract framing openings.

Weak:

> We begin with samples, not a formula.

Weak:

> At its core, this is a story about how distributions can be represented.

Weak:

> To understand characteristic functions, we first need to step back.

Stronger:

> These two distributions have the same mean and variance, although their mass
> is arranged very differently.

Stronger:

> Place a sample $x$ on the number line. At frequency $t$, it determines the
> angle $tx$.

Stronger:

> A matrix usually turns a vector away from the line it started on. A few
> directions behave differently.

The opening should put something in the viewer's mind that the next sentence
can act upon.

---

# 5. Avoid generic LLM framing patterns

The following patterns are not absolutely forbidden, but their repeated use is
a major failure.

## "We start with X, not Y"

Examples:

- "We start with samples, not a formula."
- "We have a picture, not a proof."
- "We need a direction, not just a number."

This pattern often sounds polished while saying very little. Use it only when
the contrast is mathematically essential. Prefer describing the actual
situation.

Instead of:

> We start with samples, not a formula.

Use:

> Suppose these points are measurements collected from an experiment.

---

## "It is not X; it is Y"

Examples:

- "This is not merely a trick; it is a new language."
- "The curve is not just a summary; it is a fingerprint."
- "This is not an approximation; it is a geometric interpretation."

Models overuse this construction because it creates immediate rhetorical
emphasis. Use contrast when correcting a genuine misconception, not as a
default sentence generator.

Weak:

> This is not just an average. It is a frequency probe.

Stronger:

> The average depends on $t$, so changing $t$ asks a different alignment
> question of the same samples.

---

## "Here is the key idea"

Related phrases include:

- "Here is the trick."
- "Here is the central insight."
- "The key thing to notice is…"
- "This is where things become interesting."
- "The magic happens when…"

Replace importance labels with the observation itself.

Weak:

> The key insight is that the arrows cancel.

Stronger:

> When the arrows point in different directions, their sum becomes shorter.

---

## "Let's…"

Examples:

- "Let's begin."
- "Let's make this concrete."
- "Let's take a closer look."
- "Let's see what happens."
- "Let's step back."
- "Let's build some intuition."

Occasional use is natural. Repeated use makes the speaker sound like a generic
tutor. Prefer direct narration:

> Set $t=0$. Every arrow points to the right.

rather than:

> Let's set $t=0$ and see what happens.

---

## Artificial importance language

Avoid unearned uses of:

- important; crucial; profound; powerful; remarkable;
- elegant; beautiful; magical; surprising; fascinating;
- fundamental; deep.

Do not tell the viewer how to feel about a result.

Weak:

> This beautiful and powerful result tells us something profound.

Stronger:

> Knowing the characteristic function for every $t$ determines the distribution
> uniquely.

The result itself should establish its importance.

---

# 6. Avoid procedural command chains

Generated explanations often become sequences of commands:

> Take the number line.
> Wrap it around a circle.
> Draw an arrow.
> Average the arrows.
> Plot the result.
> Increase the frequency.
> Watch what happens.

This can be clear, but it sounds mechanical because the reasoning between
operations has disappeared.

Every nontrivial operation should be motivated by one of the following:

- a question;
- a limitation in the current representation;
- a quantity we want to measure;
- an observation from the previous scene;
- a mathematical relationship.

Weak:

> Draw each point as an arrow and average them.

Stronger:

> Each sample has become a direction. Averaging those directions reveals
> whether the phases reinforce one another or cancel.

Weak:

> Plot the endpoint against $t$.

Stronger:

> Repeating the same average at every frequency produces a function of $t$.

The operation is still clear, but it follows from a reason.

---

# 7. Use visual language precisely

Narration should direct the viewer's attention, but it should not merely
describe every visible movement.

Avoid narrating obvious animation:

> The blue dot moves to the right.
> The circle grows larger.
> The arrow changes color.
> The equation appears at the top.

Describe what the movement means.

Weak:

> The arrows begin to rotate around the circle.

Stronger:

> Increasing $t$ changes every angle from $t x_j$ to a larger multiple of the
> same sample value.

Weak:

> The average arrow becomes smaller.

Stronger:

> These directions now oppose one another, so part of the vector sum cancels.

The visual and narration should complement each other:

- animation shows movement and geometry;
- narration identifies the relationship, invariant, cause, or implication.

Do not make both channels communicate identical low-level information.

---

# 8. Specify what the viewer should notice

Avoid empty attention commands:

- "Notice what happens."
- "Watch carefully."
- "Look at this."
- "Keep an eye on the right."
- "Watch all three panels."
- "Pay attention here."

An attention command must identify the relationship that matters.

Weak:

> Watch what happens as $t$ increases.

Stronger:

> The samples remain fixed. Only their angles change, and samples farther from
> zero rotate more quickly.

Weak:

> Watch all three panels at once.

Stronger:

> Follow one sample from its fixed position on the line, through the angle
> $tx$, to its arrow on the circle.

The viewer should never have to guess which part of a busy animation carries
the argument.

---

# 9. Distinguish observation, interpretation, and conclusion

Do not compress several epistemic steps into one confident sentence.

Separate:

1. what is visibly happening;
2. how it should be interpreted;
3. what mathematical conclusion follows.

Example:

> At this frequency, the arrows are spread around the circle. Their horizontal
> and vertical components cancel almost completely. The average therefore lies
> close to the origin.

This is clearer than:

> The high frequency destroys the signal.

The latter skips the visual observation and introduces an interpretation that
may be too strong.

Use language appropriate to the strength of the reasoning.

## For direct observations

- "The arrows are spread around the circle."
- "The transformed square has twice the original area."
- "This vector stays on the same line."

## For derived claims

- "So the average is close to zero."
- "Therefore the area scale factor is two."
- "This direction is preserved by the transformation."

## For visual intuition

- "This suggests…"
- "The picture makes it plausible that…"
- "Geometrically, we should expect…"

## For cited theorems

- "A theorem guarantees…"
- "The uniqueness theorem states…"
- "Proving this requires…"

Do not use "therefore" when the preceding visual only makes the claim
plausible.

---

# 10. Make equations arrive from the scene

An equation should not interrupt the visual argument as a separate formal
layer. Before displaying an equation, establish what its pieces already mean.

Weak:

> The characteristic function is defined as
> $$\varphi_X(t)=\mathbb{E}\left[e^{itX}\right].$$

This may be acceptable for an expert audience, but it is not a visual
derivation.

Stronger sequence:

1. A sample $x$ determines the angle $tx$.
2. The unit arrow at that angle is $e^{itx}$.
3. Average the arrows over the sample set.
4. Replace the finite average with a population expectation.
5. Name the resulting function.

The narration might say:

> A sample $x$ contributes the unit arrow $e^{itx}$. Averaging over the
> distribution gives
> $$\varphi_X(t)=\mathbb{E}\left[e^{itX}\right].$$

The equation now compresses an operation the viewer already understands.

---

# 11. Do not explain every symbol mechanically

Avoid narration that sounds like documentation:

> Here, $\varphi$ denotes the characteristic function, $X$ denotes the random
> variable, $t$ denotes frequency, $i$ denotes the imaginary unit, and
> $\mathbb{E}$ denotes expectation.

Define symbols when they become relevant, preferably through their role.

Stronger:

> The input $t$ controls the wrapping frequency. For that frequency,
> $\varphi_X(t)$ is the average arrow produced by the distribution of $X$.

The imaginary unit may need no separate definition if the audience contract
assumes complex numbers. If it is marked `REFRESH`, restore only the necessary
picture.

---

# 12. Do not overexplain assumed prerequisites

Natural narration respects the viewer's competence. If vectors are assumed, do
not say:

> A vector is an object with magnitude and direction.

If expectation is assumed, do not provide a foundational definition. Use
assumed concepts directly.

If a concept is marked `REFRESH`, restore only the part needed for the current
argument. Example:

> Recall that $e^{i\theta}$ is a unit arrow at angle $\theta$.

Then continue. Do not expand into Euler's identity, the power series, or the
full complex plane unless the video actually needs them.

Unnecessary prerequisite explanations make narration feel generic because the
model is writing for an imaginary lowest-common-denominator audience rather
than the specified viewer.

---

# 13. Vary sentence structure without forcing variety

Generated narration often repeats one syntax pattern. Common repeated patterns
include:

## Imperative pattern

> Take the samples. Wrap the line. Draw the arrows. Average them.

## Contrast pattern

> It is not X. It is Y.
> We do not need A. We need B.

## Question-answer pattern

> What happens next? The arrows cancel.
> Why does this matter? It gives us a curve.

## Three-beat pattern

> It rotates. It cancels. It shrinks.

## Repeated "Now"

> Now increase $t$. Now average the arrows. Now plot the result.

Do not solve this by mechanically alternating sentence lengths. Instead, let
logical relationships determine syntax.

Use:

- short sentences for a decisive observation;
- longer sentences when connecting cause and consequence;
- questions when the viewer has enough information to genuinely consider them;
- equations where prose would be less precise;
- pauses where the visual needs time.

Example with varied but natural rhythm:

> At $t=0$, every arrow points to the right, so their average is exactly $1$.
> As $t$ increases, the samples themselves do not move; only the phases change.
> Values farther from zero accumulate angle more quickly, and the arrows begin
> to separate.

The sentence variation follows the reasoning.

---

# 14. Avoid excessive rhetorical questions

Rhetorical questions are useful when they create a real inference.

Weak:

> What do we do next? We average the arrows.

Weak:

> Why is this useful? Because it captures the distribution.

Weak:

> What happens when $t$ increases? The arrows rotate faster.

These questions are answered before the viewer has time or information to
think.

Stronger:

> At $t=0$, every distribution produces the same average arrow. Which part of
> the distribution becomes visible once the frequency moves away from zero?

This question introduces a genuine problem.

Use questions when:

- the preceding scene creates uncertainty;
- multiple outcomes seem plausible;
- the viewer can make a prediction;
- the question motivates a new construction.

Do not end every section with a question merely to create engagement.

---

# 15. Avoid artificial suspense

Do not delay an ordinary fact with dramatic phrasing.

Avoid:

- "And then something remarkable happens."
- "But the real surprise comes next."
- "This is where the magic begins."
- "What happens next changes everything."
- "The answer is more profound than it first appears."

Mathematical suspense should come from:

- a contradiction;
- a failed approach;
- an unexpected invariant;
- an edge case;
- two representations suddenly agreeing;
- a result that resolves an established problem.

The narration should not announce surprise before the viewer has experienced
it.

---

# 16. Do not overuse delayed naming

Constructing an object before naming it can be effective, but it must not
become a repetitive gimmick.

Weak recurring pattern:

> This object has a name. It is called the determinant.
> This curve has a name. It is called the characteristic function.
> This direction has a name. It is called an eigenvector.

This becomes predictable and theatrical.

Names can enter naturally:

> This area scale factor is the determinant of the transformation.

Or, for an expert audience:

> The determinant measures the signed area scale factor.

Choose timing based on the audience and scene, not a universal rule.

---

# 17. Avoid metaphor churn

A metaphor creates obligations. If the characteristic function is called a
"frequency probe," specify:

- what is being probed;
- what the frequency controls;
- what the output records;
- where the metaphor stops being literal.

Do not call the same object a fingerprint, a probe, a lens, a shadow, a
language, a map, and a machine within a short span. This makes narration sound
generated because the model repeatedly searches for fresh imagery.

Prefer one visual model grounded directly in the mathematics. For
characteristic functions, "average rotating arrow" may be more useful than any
metaphor because it describes the actual construction.

If "fingerprint" is used, reserve it for the uniqueness theorem and qualify it:

> Since the full characteristic function determines the distribution, it acts
> like a mathematical fingerprint.

The theorem justifies the metaphor.

---

# 18. Avoid slogan-like conclusions

LLM narration often ends sections with polished summary statements:

- "And that is the hidden geometry behind the formula."
- "The curve remembers what the samples forget."
- "A cloud of numbers has become a geometric signature."
- "The abstraction is simply the picture in disguise."

These sentences can sound impressive but may add no understanding.

A conclusion should do one of the following:

- state the result precisely;
- connect it to the next problem;
- compress the established mental model;
- identify a limitation;
- explain why the result matters for the larger method.

Stronger:

> For every $t$, the characteristic function records the average phase
> $e^{itX}$. The next question is why SIGReg compares these averages rather
> than comparing samples directly.

This both summarizes and advances.

**Do not require every scene to end with a quotable line.**

---

# 19. Maintain local continuity

Each paragraph should grow from the preceding one. A transition is strong when
the previous idea creates the need for the next.

Example:

> One frequency gives one complex number. That cannot describe an entire
> distribution, so vary $t$.

The next operation follows from a limitation in the current result.

Weak:

> Now let us turn to the role of frequency.

The transition could appear anywhere.

Before finalizing narration, test every paragraph boundary:

1. What fact or limitation from the previous paragraph motivates this one?
2. Could this paragraph be moved elsewhere without changing the logic?
3. Does the first sentence connect to what the viewer is currently seeing?
4. Does the paragraph introduce a new object before establishing why it is
   needed?

If a paragraph can be moved almost anywhere, it may be generic exposition
rather than part of a reasoning path.

---

# 20. Maintain global continuity

The full narration should have a recognizable mathematical arc. A common arc
is:

```text
specific problem
  → failed or insufficient description
    → visual construction
      → observation
        → mathematical formulation
          → parameter exploration
            → edge case
              → general claim
                → proof boundary
                  → application
```

This is not a required template. The important condition is that every section
changes the viewer's understanding and contributes to the target question.

Avoid introductions that promise several ideas and conclusions that merely
repeat them. Do not include a recap after every small step. Recaps should
compress several steps into a reusable mental model.

---

# 21. Use repetition deliberately

Some repetition is necessary for learning. Good repetition changes
representation or level:

1. show an average arrow;
2. express it as a finite sum;
3. generalize it to expectation;
4. interpret its real and imaginary parts.

Bad repetition restates the same sentence:

> The arrows cancel.
> Their directions cancel one another.
> This cancellation makes the average smaller.

Combine these unless the visual needs time.

Repeated terminology can provide continuity. Repeated rhetorical framing
usually creates an LLM cadence.

---

# 22. Match narration density to the visual

Do not speak continuously merely because the scene has a fixed duration.

Allow pauses when:

- a transformation needs to be watched;
- several visual correspondences appear;
- the viewer should make a prediction;
- an equation has just been assembled;
- an edge case needs time to register.

Do not narrate over every animation beat. Conversely, do not leave a visually
ambiguous operation unexplained.

For every scene, classify narration density:

- `low`: the visual carries most of the reasoning;
- `medium`: narration and visual share the argument;
- `high`: the idea depends on verbal precision or proof qualification.

Narration should become denser around assumptions, logical implications, proof
boundaries, subtle distinctions, and limitations. It can become lighter around
visible motion, repeated examples, and transformations already understood.

---

# 23. Write complete prose before subtitle segmentation

Do not draft directly in SRT-style fragments.

Bad drafting process:

```text
We have samples, not a formula.
So here is the move that makes them measurable.
```

This encourages clipped cadence and unnatural line-level conclusions.

First write coherent paragraphs meant to be spoken aloud. Only after narration
is final should it be divided according to breath, timing, visual events,
subtitle readability, and clause boundaries.

Subtitle line breaks must not influence the syntax of the original narration.

---

# 24. Use mathematical language naturally

Avoid unnecessary formalism:

> It can therefore be observed that the magnitude decreases.

Prefer:

> The average becomes shorter.

But do not oversimplify precise distinctions:

- scalar versus vector;
- real part versus magnitude;
- empirical average versus expectation;
- intuition versus proof;
- typical behavior versus guaranteed behavior.

Natural language should remain mathematically responsible.

Prefer active constructions:

> The transformation doubles area.

over:

> The area is caused to be doubled by the transformation.

Prefer concrete nouns ("average arrow", not "resulting representational
quantity").

Prefer verbs that describe the operation: rotates, stretches, projects,
cancels, accumulates, preserves, aligns, separates, converges, oscillates.

---

# 25. Preserve uncertainty and conditions

Do not make a sentence cleaner by deleting necessary qualifications.

Weak:

> At high frequencies, the average goes to zero.

This may require assumptions and refers to an asymptotic result, not
necessarily an empirical finite-sample curve.

Stronger:

> For many continuous distributions, the population characteristic function
> becomes small at sufficiently high frequencies. A finite empirical average
> can continue to oscillate and realign.

Natural narration does not mean absolute confidence. Use conditions without
burying the idea under legalistic phrasing.

---

# 26. Avoid invisible referents

Do not repeatedly use *this*, *that*, *it*, *these*, *the result*, *the
object*, when several possible referents are visible.

Weak:

> This becomes smaller as it changes.

Stronger:

> The average arrow becomes shorter as the individual directions separate.

Precise referents improve both comprehension and naturalness.

---

# 27. Do not abuse "simple" and "just"

Avoid phrases such as:

- "simply average them";
- "just rotate the vector";
- "all we have to do is…";
- "it is easy to see…";
- "obviously…";
- "clearly…"

These phrases often hide the exact step a learner needs. Use "just" only when
removing a genuine misconception or emphasizing that no extra operation is
involved.

Weak:

> The characteristic function is simply the expectation of a complex
> exponential.

Stronger:

> For each frequency, convert $X$ into the unit arrow $e^{itX}$, then average
> that arrow over the distribution.

---

# 28. Do not manufacture intimacy

Avoid repeatedly addressing the viewer with:

- "you can see";
- "you might think";
- "you may remember";
- "you probably noticed";
- "as you can imagine."

These phrases assume a mental response that may not have occurred. Prefer
stating the observation.

Weak:

> You can see that the arrows cancel.

Stronger:

> The arrows point in opposing directions, so their components cancel.

Direct address is useful for genuine invitations:

> Pause here and predict whether the average will grow or shrink.

Use it sparingly.

---

# 29. Narration should survive without the animation — but improve with it

The viewer should not become completely lost if they briefly look away.
However, narration should not duplicate the entire visual in exhaustive detail.

A useful test:

- Audio alone should preserve the reasoning path.
- Visuals should make the reasoning easier to perceive and remember.
- Neither channel should be wholly redundant.
- Neither channel should contain an essential unsupported leap.

If the narration says "this point" or "that arrow," ensure the referent remains
clear from context.

---

# 30. Drafting procedure

Use the following process for each scene.

## Step 1: State the narration objective

> Make the viewer understand that $e^{itx}$ is a unit arrow, not an arbitrary
> symbolic trick.

## Step 2: List the necessary claims

- $tx$ is an angle.
- $e^{itx}$ has coordinates $(\cos tx, \sin tx)$.
- Its magnitude is one.

## Step 3: List what the animation already communicates

- the arrow rotates;
- its length remains fixed;
- changing $x$ changes the angle.

## Step 4: Write only what the narration must add

> The exponential records a direction: $tx$ sets the angle, while the arrow's
> length stays one.

## Step 5: Connect to the next scene

> Every sample now contributes one direction. Their average will tell us
> whether those directions agree.

## Step 6: Read aloud

Check:

- Does it sound like a sentence someone would naturally say?
- Are there too many clauses?
- Is emphasis being announced rather than earned?
- Does any phrase exist only to sound polished?
- Is the mathematical referent clear?
- Does the last sentence create the next need?

---

# 31. Narration audit

After completing the draft, run a dedicated audit. **Do not revise while
performing the initial audit.** First identify patterns across the entire
script.

> In this repo, `tools/narration_audit.py` performs the countable parts of
> A–E and H automatically. F, G, I, J are judgement work and must be written
> out by hand.

## A. Transition audit

Count and list every occurrence of: *now, next, here, let us, let's, before,
instead, rather, finally, first, second, in other words, at this point.*

Questions:

- Are several paragraphs opened with the same transition?
- Does the transition advance reasoning or merely announce structure?
- Could the mathematical relationship replace the signpost?

## B. Contrast audit

Identify: *not X but Y; X rather than Y; this is not merely X; we do not need
X; instead of X; the point is not X.*

For each occurrence, ask:

- Is a real misconception being corrected?
- Is the contrast necessary?
- Is this construction repeated nearby?
- Could a direct positive statement be clearer?

## C. Imperative audit

List commands: *take, draw, imagine, place, rotate, watch, look, notice,
consider, suppose, think.*

Commands are not inherently bad. Flag scenes with long runs of commands lacking
explanation.

## D. Importance-language audit

List: *important, crucial, key, surprising, powerful, elegant, profound,
beautiful, remarkable, fundamental.*

Require evidence that each word is earned. Delete most of them.

## E. Cadence audit

Record approximate sentence structure: short declarative, long explanatory,
imperative, rhetorical question, equation introduction, conclusion, fragment.

Flag:

- three or more consecutive sentences with nearly identical structure;
- repeated paragraph lengths;
- repeated question-answer pairs;
- **repeated slogan endings**;
- excessive fragments;
- subtitle-like prose.

## F. Function audit

Assign every sentence one or more labels: `PROBLEM`, `ATTENTION`,
`OBSERVATION`, `MOTIVATION`, `JUSTIFICATION`, `VISUAL_TO_SYMBOL`, `CLAIM`,
`QUALIFICATION`, `TRANSITION`, `RECAP`, `APPLICATION`.

Flag sentences with no clear function. Flag sections containing many
`TRANSITION` or `RECAP` sentences but few `OBSERVATION`, `JUSTIFICATION`, or
`CLAIM` sentences.

## G. Visual grounding audit

For every substantive visual reference, ask:

- What object is visible?
- Which property matters?
- What changes?
- What remains fixed?
- Is the narration naming the relationship or only the motion?
- Is the relevant object still on screen when referenced?

## H. Proof-language audit

List every occurrence of: *therefore, hence, so, proves, shows, implies,
guarantees, must, exactly, always, never.*

Check whether the preceding reasoning supports that strength.

## I. Metaphor audit

List every metaphor. For each:

- What maps to what?
- Is the mapping explained?
- Does it remain valid?
- Does another metaphor compete with it?
- Is the metaphor doing work that the mathematics should do?

## J. Compression audit

Identify places where:

- three sentences can become one;
- a sentence repeats the animation;
- a recap restates the previous paragraph;
- an adjective announces significance;
- a transition can be replaced by a reason;
- an analogy repeats an already clear geometric model.

Compression should remove redundancy, not reasoning.

---

# 32. Scoring the narration

Score narration separately from mathematical and pedagogical correctness.

| Category | Points | Evaluate |
|---|---|---|
| Spoken naturalness | 10 | sentences sound natural aloud; voice feels continuous rather than assembled; direct address used sparingly; wording specific to the actual mathematics; avoids generic educational phrasing |
| Reasoning continuity | 10 | each paragraph grows from the previous; operations motivated; transitions arise from mathematical needs; conclusions follow from stated observations |
| Cadence and variation | 10 | sentence-pattern variation; use of pauses; balance of short and connected sentences; avoids repetitive imperatives and rhetorical questions |
| Economy | 10 | every sentence has a function; explanations not repeated; visual information not unnecessarily narrated; transitions and recaps not excessive |
| Visual coordination | 10 | attention guidance precise; narration explains relationships rather than obvious motion; equations arrive at the right visual moment; multiple representations connected explicitly |

**Total narration score: 50 points.**

Any of the following blocks finalization regardless of score:

- severe cadence repetition across the full script;
- repeated generic LLM framing;
- narration written as subtitle fragments;
- procedural instructions without reasoning;
- a metaphor replacing mathematical justification;
- proof language stronger than the argument;
- narration that contradicts the visual representation.

---

# 33. Revision procedure

Revise in this order:

1. remove mathematically misleading language;
2. repair proof-strength mismatches;
3. restore missing reasoning between operations;
4. clarify visual referents and attention;
5. replace generic transitions with mathematical causes;
6. remove unnecessary prerequisite explanation;
7. break repetitive syntax patterns;
8. delete unearned importance language;
9. reduce metaphor churn;
10. compress repeated observations;
11. read the full passage aloud again.

**Do not revise by replacing every flagged phrase with a synonym.**

Weak:

> Here is the key idea.

Bad superficial revision:

> The central insight is this.

Better revision: state the idea directly.

Do not solve repeated "Now" openings by mechanically replacing them with
*next*, *then*, *at this stage*, or *subsequently*. Repair the reasoning
connection instead.

---

# 34. Required output after narration generation

After drafting narration, provide:

**Narration draft** — complete spoken prose, organized by scene. Do not segment
into subtitles.

**Narration audit** — transition count; contrast-pattern count; imperative
clusters; repeated syntax patterns; empty attention commands; teaching-process
narration; importance-language occurrences; metaphors used; slogan-like
conclusions; sentences with unclear function.

**Highest-priority findings** — separate systemic problems (affecting the voice
of the whole script) from local problems (one sentence or scene).

**Revised narration** — targeted revisions.

**Before-and-after examples** — for each major systemic issue, at least one
concrete revision, explaining what changed structurally.

**Final narration score** — the five categories reported separately.

Do not claim the narration is natural merely because banned phrases were
removed.

---

# 35. Final standard

The narration is ready only when:

- the speaker sounds focused on the mathematics rather than on performing
  explanation;
- each operation has a reason;
- each equation compresses something the viewer already understands;
- visual attention is guided precisely;
- proof strength is represented honestly;
- assumed knowledge is respected;
- the cadence does not repeat a recognizable template;
- metaphors are limited and justified;
- transitions emerge from the argument;
- the script reads as continuous spoken thought rather than assembled
  educational copy;
- removing any sentence would either lose reasoning, precision, orientation, or
  necessary pacing.

The final goal is not narration that merely avoids obvious machine-generated
phrases. The goal is narration whose language feels necessary because it grows
directly from the mathematical objects, visual changes, and reasoning of the
explanation.
