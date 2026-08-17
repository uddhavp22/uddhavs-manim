# Chapter B review guide

This is the short, practical companion to
[`RENDER_REVIEW_SPEC.md`](../../docs/RENDER_REVIEW_SPEC.md). It records the
qualities we are actively judging while Chapter B is rebuilt scene by scene.
The MP4 is the evidence; clean source code is not a substitute for watching it.

## The central test

Every scene should feel like one connected act of reasoning:

```text
problem → experiment → observation → conclusion → next question
```

At any moment, a first-time viewer should be able to answer:

1. What am I looking at?
2. What just changed?
3. Why did it change?
4. What am I meant to infer from that change?

If the answer depends entirely on narration, the visual argument is too weak.

## General preferences distilled from scene review

- Put the main experiment near the visual centre while it is being introduced.
- Move it aside only when a second idea genuinely needs the space.
- Use the full frame deliberately. Large unused margins should not leave the
  active diagram cramped elsewhere, and every extreme example must clear the
  score, labels, and equations.
- Connectors must have deliberate geometry. A mathematically correct anchor can
  still produce an arrow that looks crooked.
- Any object called an arrow must retain a readable arrowhead after its live
  updater takes over. Endpoint dots are subordinate markers, not replacements
  for the arrow silhouette.
- Let examples establish a rule before presenting requirements for that rule.
- Motivate a representation by the question it answers before naming it. A
  histogram belongs because it retains shape; the name alone is not a reason.
- Vary examples in short, settled pulses instead of one long continuous morph.
- When narration says one sample moves, animate one sample and update the real
  dependent value. Do not remorph the whole batch.
- The animation must instantiate the spoken claim. Do not move a sample while
  asking what it should contribute unless its contribution is also changing.
- Remove arrows, captions, and helper marks after they have done their job.
- Avoid simultaneous text fade-outs and fade-ins in the same location; their
  overlap reads as ghosting.
- Use empty space to protect the focal object. Samples must never collide with
  a score box, equation, or annotation.
- End by creating the question the next scene answers, not with a generic
  slogan or recap.
- Do not force that handoff into a spoken question every time. A visible
  unknown or a declarative next step often carries curiosity with less fuss.
- Do not introduce future vocabulary as justification. Refer to needs the
  viewer already knows—such as differentiability—until training, loss, or
  optimization has actually been established.
- State local mathematical behavior precisely: for hard histogram counts the
  derivative is zero between bin edges and undefined at an edge.
- Treat a scene boundary as a handoff. The previous closing unknown should
  become the next opening object or experiment, with a short breath when the
  viewer needs to reset.

## Animation review

Look for these on normal playback and again frame by frame:

- **Causal motion:** a changing object visibly drives its dependent objects.
- **Object identity:** the same mathematical object should transform rather
  than disappear and reappear without reason.
- **Endpoint frames:** every important transformation settles long enough to
  read before the next one begins.
- **One focal change:** if several things move, they should express one event.
- **Clean paths:** no accidental diagonal drift, crossing dot trajectories,
  sudden snaps, or updater-created jitter.
- **Exact extremes:** inspect the tallest stack, largest label, final tracker
  value, and the frame immediately before and after a discontinuity.
- **Clean teardown:** no ghost dots, stale arrows, live updaters fighting a
  fade, or one-frame flashes at the cut.

Useful question: if the audio were muted, would the changing relationship
still be visible?

## Style and composition

- One dominant visual idea per frame.
- Computer Modern typography through `common/type.py`; no ad hoc font family.
- Text remains at or above the project size floor.
- Colour has meaning: blue is the sample/batch, red is the contrasting or
  failure state, amber is the current target, question, or measurement.
- Labels describe an object or relation. They do not restate narration.
- Empty space is intentional, but unused space should not force the active
  diagram into a cramped corner.
- Persistent furniture must earn its place. Fade it once the viewer no longer
  needs it for orientation.
- Check the complete 1920×1080 frame, not a zoomed crop.

## Rhythm

Good rhythm alternates motion and inspection:

```text
introduce → settle → vary → settle → reveal consequence
```

- A new example usually wants about a one-second visual beat, with a short
  settled endpoint.
- Do not stretch one `Transform` over a whole paragraph merely to avoid a
  static frame.
- Do not rush three examples through one unbroken morph. Give each a distinct
  arrival.
- Spoken pauses should leave something new to inspect.
- Continuous motion is appropriate when continuity is the claim. Discrete
  pulses are appropriate when comparing separate trials.
- Use `tracker.get_remaining_duration()` so the delivery voice controls the
  beat, but divide that time intentionally rather than assigning all of it to
  the last animation.
- Use narration bookmarks when a particular phrase names a particular visual
  event. Whole-passage timing is not enough for a lift, projection, component,
  or formula that needs to arrive on a word.

## Language and pedagogy

- Prefer questions the viewer can reason about from the current frame.
- Introduce a condition as the answer to a practical need, not as “constraint
  one” and “constraint two.”
- Prefer “try,” “suppose,” “move,” and “what changes?” when the animation
  actually performs that experiment.
- Use connective experiment language across consecutive beats: “Suppose we…”
  establishes the setup, and “Then, if we…” makes the variation feel causal
  rather than like a new disconnected fact.
- State observations after they become visible.
- Avoid “as you can see,” “clearly,” “here is,” slogan endings, and decorative
  metaphors before the mathematics earns them.
- Narration should explain the implication of motion, not merely describe the
  motion itself.
- Blocking is usually silent. Do not narrate that a line rises, a panel moves,
  or a label changes when the viewer can already see it; use the voice for the
  mathematical relationship that the blocking makes visible.
- Do not stretch a small emphasis gesture across a full sentence. A lift,
  pulse, label write, or object handoff should resolve promptly even when the
  underlying idea needs longer to explain.
- When notation is spoken, write the narration so the voice says each symbol
  unambiguously. Pronunciation is part of the final delivery, not cleanup for
  later.
- Test capitalization and punctuation before adding spoken scaffolding around
  notation. For ambiguous words, prefer an unambiguous phrase such as “equal
  spacing” over hoping the voice chooses the intended pronunciation of “even.”
- Before introducing compact notation, make clear what object it represents
  and why that representation answers the current question.
- Reserve a formal name and its conventional symbol for the scene where that
  naming is the payoff. Before then, use descriptive or visibly self-defining
  notation rather than spending the vocabulary early.
- Do not move a parameter to demonstrate a dependent colour, curve, or
  component before that dependent object has been introduced.
- Keep screen text compressed: notation, values, and relationships belong on
  screen; the reasoning belongs in the voice.

## Transitions between scenes

Review the previous, current, and next clips in sequence.

- The opening should answer or test the previous scene’s final question.
- Preserve a visual object across the cut only when its identity matters.
- Otherwise clear the scene decisively; accidental leftovers are not
  continuity.
- The closing frame should create genuine demand for the next construction.
- Avoid repeating the previous conclusion before beginning the next idea.

## 3Blue1Brown patterns worth borrowing

These are small structural patterns from the local
`3blue1brown_videos/_2024` source. That repository uses ManimGL; the examples
below show the equivalent Manim Community shape used in this project.

### 1. Put the unknown on screen before explaining the machinery

Source: `_2024/transformers/network_flow.py`, around lines 175–207. The scene
first writes `???`, draws attention to the missing token, waits, and only then
turns the existing text into model inputs.

```python
question = ty.words("???", size=ty.STATEMENT, color=TARGET)

self.play(LaggedStart(
    FadeIn(context_box),
    Create(arrow),          # ManimGL uses ShowCreation
    Write(question),
    lag_ratio=0.3,
))
self.inspect(0.8)
```

The lesson is not the question marks. It is the order: establish a concrete
unknown, let the viewer hold it, then introduce the mechanism that resolves it.

### 2. Give repeated examples a fixed pulse

Source: `_2024/transformers/old_auto_regression.py`, around lines 558–571. A
set of dials is randomized five times, with each trial receiving one second.

```python
for samples_a, samples_b in examples:
    self.play(
        Transform(top_dots, dots_for(samples_a)),
        Transform(bottom_dots, dots_for(samples_b)),
        ChangeDecimalToValue(score, pair_score(samples_a, samples_b)),
        run_time=0.8,
        rate_func=smooth,
    )
    self.wait(0.2)
```

The repeated duration creates rhythm and makes each state feel like a separate
trial. Sort or otherwise pair dot identities before transforming so the paths
do not become visual noise.

### 3. Stagger many related arrivals, then remove them

Source: `_2024/transformers/old_auto_regression.py`, around lines 501–521.
Many facts enter with `LaggedStart`, each using a `Succession` to appear and
flow inward.

```python
self.play(LaggedStart(*(
    Succession(
        FadeIn(item),
        item.animate.move_to(destination).set_opacity(0),
    )
    for item in items
), lag_ratio=0.05, run_time=5))
self.remove(*items)
```

This is useful when many objects express one repeated process. It is not a
license to stagger unrelated decorations.

### 4. Attach all dependent geometry to one state variable

For continuous mathematical motion, use a `ValueTracker` and derive every
dependent object from it:

```python
x = ValueTracker(0.7)
dot = always_redraw(lambda: Dot(number_line.n2p(x.get_value())))
readout = always_redraw(lambda: ty.readout("s", score_at(x.get_value())))

self.play(x.animate.set_value(1.3), run_time=3, rate_func=linear)
```

In this repo, freeze live objects before fading them. An `always_redraw`
mobject can otherwise rebuild itself every frame and fight the fade.

### 5. Fourier-style wrapping and center-of-mass plots

Source: `_2018/fourier.py`, especially `wrap_around_circle()`,
`introduce_frequency_plot()`, and `change_frequency()`.

- Transform one carrier into its wrapped state. Do not leave a source copy and
  a live destination copy visible over one another.
- Let one frequency tracker drive the wrapping, arrows, center of mass, graph
  point, and traced curve.
- Keep the individual contributions one colour and the center-of-mass marker a
  dedicated colour; never recolour the whole group to emphasize the average.
- Name the plotted coordinate before drawing its curve. In B03, the blue curve
  is specifically the horizontal coordinate of the purple average, not a
  generic measure of its location.
- Prefer a continuous forward sweep. If a return to zero is mathematically
  needed, narrate it and give it its own visible beat instead of hiding a fast
  reset inside the next claim.

## ManimGL-to-CE reminders

Do not paste local 3Blue1Brown code unchanged:

| ManimGL source | This project, Manim CE |
|---|---|
| `ShowCreation(mob)` | `Create(mob)` |
| `Tex(...)` for maths | `MathTex(...)` or `ty.maths(...)` |
| `TexText(...)` | `Text(...)` or `ty.words(...)` |
| `DEG` | `DEGREES` |
| `self.frame.reorient(...)` | CE camera methods; do not translate blindly |
| `set_anim_args(...)` | pass timing arguments to `self.play(...)` |

See [`MANIM_CE_VS_MANIMGL.md`](../../docs/MANIM_CE_VS_MANIMGL.md) before
adapting a full pattern.

## Scene review note template

```text
Scene:
Artifact and resolution:

First uninterrupted impression:
What the viewer learns:

Animation:
- [timestamp] finding → viewer consequence

Style/layout:
- [timestamp] finding → viewer consequence

Rhythm/audio:
- [timestamp] finding → viewer consequence

Language/pedagogy:
- [timestamp] finding → viewer consequence

Transition in/out:
- previous → current:
- current → next:

Verdict: approve / revise / blocker
Highest-value next change:
```

## B01 review targets

When reviewing `B01.mp4`, check specifically that:

- the histogram grows from the samples rather than appearing as an unrelated
  chart;
- the three bin configurations read as separate, settled trials;
- the highlighted sample and the two amber counts are immediately legible;
- both counts remain unchanged before the edge;
- the counts and bar heights jump on the same frame as the crossing;
- the derivative statement appears only after the jump is observed;
- the final isolated sample remains fixed while `x_i \mapsto ?` asks what its
  smooth contribution should be, creating the need for B02.
