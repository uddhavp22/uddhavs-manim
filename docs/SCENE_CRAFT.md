# Scene craft — choreographing a beat

How a beat is designed, animated, synchronised with its narration, and checked
before it is called done. This is the working companion to the four standards:

| Document | Owns |
|---|---|
| [`NARRATION_SPEC.md`](NARRATION_SPEC.md) | the words (binding) |
| [`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) | judging the finished MP4 (binding) |
| [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) | typography, colour roles, margins, easing, cut style |
| [`MANIM_GUIDE.md`](MANIM_GUIDE.md) | environment, render commands, CE API, voiceover plumbing |
| **this file** | how motion carries an argument, and the traps that break it silently |

Everything here was learned on rendered frames during Chapters B and C of the
SIGReg explainer and the LeNEPA segment. Where a rule came from an owner
review it says so; those are not up for re-litigation per scene.

---

## 1. The design unit is a beat, not an effect

Before coding a beat, write five lines:

```text
viewer before:
viewer after:
visible operation:
changes:
stays fixed:
```

Then an event sheet — one row per spoken phrase that has to land on a visual:

| Spoken phrase | Visual event | Why it moves | Must land exactly? |
|---|---|---|---|
| names the operation | operation begins | connects language to geometry | bookmark |
| explains the invariant | fixed object stays visible | prevents a false inference | no |
| states the result | final state holds | inspection time | usually no |

Every scene is one connected act of reasoning:

```text
problem → experiment → observation → conclusion → next question
```

At any moment a first-time viewer should be able to answer: what am I looking
at, what just changed, why did it change, what am I meant to infer. If the
answer depends entirely on narration, the visual argument is too weak. Useful
test at every review: **muted, would the changing relationship still be
visible?**

One dominant focal event per beat. Two simultaneous events are justified only
when their correspondence is the point (the line moving home while the same
samples wrap into a circle).

---

## 2. Composition and rhythm — owner preferences

These came out of scene-by-scene review and are binding across projects.

**Composition**

- Put the main experiment near the visual centre while it is introduced; move
  it aside only when a second idea genuinely needs the space.
- Use the full frame deliberately. Empty space is intentional, but unused space
  must not force the active diagram into a cramped corner. Check the complete
  1920×1080 frame, not a zoomed crop, and check the **most extreme** animated
  state (tallest stack, widest label, final tracker value), not the first.
- Samples never collide with a score box, equation, or annotation.
- Anything the narration calls an arrow keeps a readable arrowhead after its
  updater takes over; endpoint dots are markers, not replacements.
- Connectors need deliberate geometry — a mathematically correct anchor can
  still draw a crooked arrow. Keep a value/graph connector local to one panel;
  a dashed link spanning two panels reads as a stray diagonal (C03, removed).
- Remove arrows, captions, and helper marks once they have done their job.
  Persistent furniture must earn its place; fade it when the viewer no longer
  needs it for orientation. A reference curve drawn to judge a shape against
  (C04's silent Gaussian) leaves once both judgements have been made.
- No persistent scene titles. Label objects in place; chapter breaks only.
- Mark a region on a curve with two dashed `MUTED` boundary lines, not a fill.
  A fill behind a curve reads as an area under it, which is an integral and
  not the claim, and it dulls the trace.
- Avoid a text fade-out and fade-in in the same place at the same time; the
  overlap reads as ghosting. Fade one out, then the other in.
- Vectors show their numbers: signed decimals in brackets, never shaded cells.

**Rhythm**

```text
introduce → settle → vary → settle → reveal consequence
```

- A new example wants roughly a one-second visual beat with a settled endpoint.
  Vary examples in short settled pulses, not one long continuous morph; give
  each of three examples its own arrival.
- Continuous motion when continuity *is* the claim (a parameter sweep);
  discrete pulses when comparing separate trials.
- When narration says one sample moves, animate one sample and update the real
  dependent value. Do not remorph the whole batch.
- Do not stretch a small emphasis gesture — a lift, a pulse, a label write —
  across a whole sentence. It resolves promptly even when the idea needs longer.
- Do not stretch one `Transform` over a paragraph to avoid a static frame. A
  still frame is fine when it holds something inspectable.
- Spoken pauses should leave something new on screen to inspect.
- Repeated examples can speed up once the grammar is learned. Do not
  compensate for a wordy script by stretching every `Write`; tighten the words.

**Scene boundaries**

- The opening answers or tests the previous scene's closing question. It does
  not restate the previous conclusion and start again.
- The closing frame creates genuine demand for the next construction. A
  visible unknown or a declarative next step often does this with less fuss
  than a spoken question.
- Preserve an object across the cut only when its identity matters; otherwise
  clear decisively. Accidental leftovers are not continuity.
- Do not introduce future vocabulary as justification. Refer to needs the
  viewer already has (differentiability) until training or loss has been
  established on screen.
- Reserve a formal name and its symbol for the scene where naming is the
  payoff; before then use descriptive, visibly self-defining notation.

---

## 3. Choose the mechanism from the meaning

| Need | Prefer | Reason |
|---|---|---|
| one object changes state | `.animate`, `Transform`, `MoveToTarget` | keeps one visible identity |
| an object truly becomes another | `ReplacementTransform` | source leaves; target owns the next state |
| a source produces a second representation | `TransformFromCopy` | source stays while its descendant appears |
| equation terms persist across a rewrite | `TransformMatchingTex` | shared symbols keep identity |
| many properties depend on one scalar | `ValueTracker` + updaters | one source of truth |
| cheap geometry rebuilt per frame | `always_redraw` | concise |
| instance identity must persist | build once + `add_updater` | registration, z-order, references survive |
| several events start together | one `self.play(...)` / `AnimationGroup` | explicit concurrency |
| events in strict order | `Succession` | explicit sequencing |
| similar objects enter with overlap | `LaggedStart` or `common.anim.lagged_map` | controlled stagger |
| a moving point's history is the claim | `TracedPath` | history made persistent |

The mechanism should expose the relationship. A smoother effect is not a
clearer one.

### One tracker owns one parameter

If `t` drives arrows, centroid, readout, rider and partial curve, every one of
them reads the same `ValueTracker`. For a direction `u`: the arrow in the
cloud, every projected scalar, guide lines, the label and the score readout
all derive from one state. Independently animated copies drift, and the drift
is the sync error the viewer feels without being able to name.

`linear` when screen distance represents change in the parameter and speeds
must be comparable; `smooth` for a finite repositioning. No bounce, elastic or
overshoot, ever ([`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) §6).

### `always_redraw` versus build-once

`always_redraw` is right for a dot, arrow, short line or partial curve derived
from trackers. Keep the factory cheap: precompute tables, never construct
`MathTex`/`Text` or a large sampled graph per frame, always go through
`axes.c2p`. `ThreePanelRig._refresh()` is the reference: the curve is computed
once and the visible prefix rebuilt from the stored table.

Build once and mutate with `add_updater` when instance identity matters:
fixed-in-frame or fixed-orientation objects in a `ThreeDScene`, objects other
references hold, geometry whose draw order must not change, or anything a
Transform-family animation will later target. Preserve a wrapper with
`mob.become(...)` inside the updater when the geometry genuinely needs
rebuilding. Never let an updater and a direct `Transform` control the same
mobject in one `play`.

### Hand static seeds to live objects explicitly

Ghosts come from an introductory static copy and its live replacement both
surviving. Treat the handoff as ownership transfer: animate the seed in, then
at a frame where both factories agree, `live.update(0)`, `self.add(live)`,
`self.remove(seed)`. Cross-fade only briefly and never leave both at full
opacity. `b03_the_rig.py::average_beat` is the reference implementation.

Same rule when a scalar batch enters the rig: `ThreePanelRig.mount(dots=...)`
adopts the dots the scene already owns rather than spawning a second set.

### Concurrency on one timeline

Use one `play` when events describe the same operation, with
`squish_rate_func(smooth, a, b)` to place short sub-events on the shared
timeline. An `AnimationGroup` or `LaggedStart` `run_time` rescales its
children; verify the resulting rhythm in the MP4, never from the child
durations.

### Transforms and paths

`Transform(a, b)` mutates `a`; `b` is only a target shape — so after it, keep
referring to `a`. The caption pattern `Transform(caption, new_caption)` bit
Chapter C exactly this way. `.animate.rotate(PI)` interpolates endpoints, not
the rotation; use `Rotate(...)` or `path_arc=` when the path is the lesson.
`TransformFromCopy(sample_dot, landing)` is the honest way to say "this sample
produces this point" without destroying the source representation. Use it
selectively; copying every item at once is noise.

### Equations inherit meaning from the picture

Compile once with the meaningful terms isolated (`ty.maths(..., isolate=[...])`
or `substrings_to_isolate`), reveal only after the corresponding visible
operation exists, and let `TransformFromCopy` off the visible arrow, gap or
area give birth to the term it denotes. Every displayed number comes from the
same NumPy state that drives the geometry (`common/score.py`, `facts.py`),
never a label typed beside a separately evaluated animation.

### Focus with state, not decoration

Chapter B is a two-dimensional argument and rarely needs camera motion; a
camera move is justified only when it reveals a relation that cannot be framed
otherwise, and one purposeful move per scene is the budget. Prefer dimming
inactive groups, briefly enlarging the active one, moving a label next to its
referent, a short dashed link between corresponding points, or keeping the
invariant visible while the active object moves. Restore with
`save_state()`/`Restore` rather than building a second copy. Pin layers with
`set_z_index`; do not rely on incidental `add()` order once updaters rebuild
things.

### Narration owns duration, without blank frames

One `voiceover` block per conceptual beat. `across(tracker, anim, floor=...)`
lets the voice set the length with a minimum; `inspect(s)` only after a state
change worth examining. Use a bookmark when an event must land on a word.
The context manager waits out unused audio after the code inside finishes, so
**do not fade the last visible object while narration remains** — that
remainder becomes narrated black video.

Scene boundaries are raw stream concatenation with no crossfade. `clear_beat()`
for an honest hard cut; `clear_overlay(...)` only for a match cut where the
next scene reconstructs the identical rig state from the same shared
constants. Compare the outgoing last frame with the incoming first frame after
either scene changes (`tools/still_frames.py`).

---

## 4. Narration and animation together

The spec governs the words. These are the rules for how words and motion meet;
Chapter B's most common defect was correct words and correct animation offset
by half a beat.

- Place a bookmark immediately before the noun or verb that triggers a visual,
  and start the animation on it, not after the sentence.
- Never speak a thing before it is on screen. A deictic — "this", "here",
  "that direction" — is allowed only when the object is already present or
  begins changing on that word; otherwise name the object.
- Blocking is silent. Do not narrate that a line rises or a panel moves; spend
  the voice on the relationship the blocking makes visible.
- Every beat opens on a connector that expresses real logic — "Now suppose",
  "Take the direction", "Then the shadow", "So pick one" — not on a
  construction. "So" lands a consequence; "if … then" ties a variation to what
  it changes. These are the conversational connectors the owner asked for, not
  filler to strip.
- Do not restate what the animation shows. "The cloud stays the same" was cut
  on owner review because the animation is that sentence.
- Do not move a parameter to demonstrate a dependent object before that object
  has been introduced.
- Create desire before notation: concrete problem → natural attempt fails →
  missing capability isolated → construction shown → name and formalise.
  `M`, `K`, "Cramér–Wold", and a finished formula arrive only when the viewer
  wants the thing each compresses.
- Do not cite an earlier chapter by name as an explanation; it reads as a
  redundant re-explanation.
- Continuous sweeps may span narration; `Write`, `Indicate`, `Circumscribe`
  are short cue-bound actions. Add a deliberate still before a dense
  explanation and after a payoff.
- Pronunciation is part of delivery. Say "sine", "the integral", "u transpose
  z", "z sub i"; prefer "equal spacing" over hoping the voice reads "even"
  correctly; listen to every generated clip before animating final timing.
  Audio is cached on passage text plus service settings, so freeze narration
  at the draft-voice stage before an ElevenLabs pass.
- ElevenLabs is the timing authority. Draft voice is for geometry; any beat
  whose choreography depends on phrase timing is rechecked against the
  rebuilt ElevenLabs master.

---

## 5. Manim CE traps that render without an error

[`MANIM_GUIDE.md`](MANIM_GUIDE.md) §5 has the engine-level list (`LaggedStartMap`
mis-binding, `Dot(color=)`, `Text` import, `tipa`, caching). These are the
production ones on top of it. Every one was found on a frame, not in a
traceback.

**Updaters and identity**

1. `FadeIn`/`FadeOut` on an `always_redraw` mobject is a no-op — the updater
   resets the opacity every frame and the object pops. Animate a static seed,
   then swap in the live object (§3).
2. `FadeOut` on a `Group` sets one opacity across the family, so a member
   already at zero opacity is forced visible and fades from there. Remove such
   mobjects from the scene instead of parking them invisible.
3. An updater that survives into a fade or teardown resets opacity every
   frame. `clear_updaters(recursive=True)`, then fade, then remove — and it
   bites on partial teardown too (`b11` left two live dots redrawing for 40 s).
4. A static seed and its `always_redraw` successor both left visible is the
   ghost-dot pattern. Store and remove the live object, not the obsolete seed.
5. An `add_updater` that only moves points is safe with opacity animations,
   unlike `always_redraw`; that is why `TurningProjection` builds geometry once.

**3-D scenes**

6. A frame-coordinate mobject added in a `ThreeDScene` without
   `add_fixed_in_frame_mobjects` is projected through the 3-D camera — a
   correct seed arrow draws as a skewed diagonal. Register seeds and their
   children the way the live rig is registered, or build them after the rig
   is flat. Fixed-orientation cloud objects and fixed-frame rig objects must
   be unregistered during ownership changes or they bleed through the next
   composition under Cairo.
7. `DecimalNumber.set_value` discards its glyphs and builds new ones, which
   are unregistered; the 3-D camera then projects the digits away from their
   label. A live `DecimalNumber` in a `ThreeDScene` calls
   `self.camera.add_fixed_in_frame_mobjects(mob)` inside its own updater (the
   camera method, not the scene method, which would re-`add` every frame).
8. The same glyph rebuild means a `DecimalNumber` whose updater changes the
   digits must be settled with `update(0)` before it is the target of a
   Transform-family animation, or the point counts mismatch and the reveal
   dies with a numpy broadcast error.
9. `set_camera_orientation(frame_center=c)` moves world content by `−2c` and
   fixed-frame content by `−c`. Derive positions from the screen layout
   through a helper (`_framed` in C05) rather than copying another scene's
   constants as if they were screen positions.
10. `ThreeDAxes` does not put its zero at the world origin; each axis is
    centred on its own bounding box, so `c2p(0,0,0)` sits about a sixth of a
    tick off. Fix with
    `for axis in axes.axes: axis.shift(-axis.number_to_point(0))`.

**Drawing**

11. `set_opacity` on a plotted curve raises its fill with its stroke and floods
    the area under it. Reveal with `set_stroke(opacity=...)` and pin
    `set_fill(opacity=0)`.
12. A bar or stack taller than the frame is simply not in the render, and
    clipped text raises nothing (`fit_in_frame` guards horizontally only).
    Check the worst case of generated geometry, and cap dot-plot stacks
    (`TurningProjection.stack_max_level`) where a projection can send every
    sample to one value.
13. An angle drawn from a raw `ValueTracker` wraps past 2π into a near-closed
    ring.
14. Labels at the far edge of an `Axes` land inside whatever is shaded there.
15. Colour read off a 480p draft is unreliable; crop and zoom before judging.

**Process**

16. A crashed render can hang instead of exiting (a stuck transcription
    worker at interpreter shutdown), so `render.sh … | tail` shows nothing.
    Redirect to a file and read it.
17. Rendering without errors is not verification. Extract frames, watch the
    MP4 with audio, and view frame sequences rather than isolated stills —
    stills miss overlaps and pacing.

---

## 6. The loop for one beat

1. Update narration in the scene source; regenerate the chapter's
   `SCRIPT_*.md` with `tools/script_dump.py`. The generated file is the review
   copy, never the edit surface.
2. Write the five-line beat sheet and the event sheet (§1).
3. Reuse or extend `common/` before adding scene-local construction. Extract a
   reusable rig only when a second scene needs the same contract.
4. Static checks: `tools/preflight.py`, `tools/narration_audit.py`, `facts.py`.
5. Draft render, draft voice, `-ql`. Watch it normally, muted, and at the worst
   transition frame. `SIGREG_VISION=1` adds collision diagnostics to triage.
6. Render important motion at `-qh`; `-ql` is 15 fps and not a smoothness
   reference.
7. Rebuild the chapter master after boundaries or shared inputs change; run
   `tools/dead_air.py` and `tools/still_frames.py` on it; check each seam.
8. Write the scene's entry in `projects/<name>/RENDER_REVIEW.md` per
   [`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) §19. A scene with no entry
   has not been reviewed.

Quick pass before the full review — on normal playback and again frame by
frame: causal motion (a changing object visibly drives its dependents), object
identity (transform, never vanish-and-reappear), settled endpoints, one focal
change, clean paths (no diagonal drift, crossing trajectories, snaps, jitter),
exact extremes, clean teardown (no ghost dots, stale arrows, one-frame flashes
at the cut).

---

## 7. 3Blue1Brown patterns worth borrowing

The local `3blue1brown_videos/` tree is ManimGL; translate through
[`MANIM_CE_VS_MANIMGL.md`](MANIM_CE_VS_MANIMGL.md) and never paste GL syntax.
The standard is behavioural — object continuity, attention control, pacing,
idea order — not surface. Copying a scene wholesale produces redundant code and
mismatched visual grammar.

| Habit | Where to see it |
|---|---|
| Put the unknown on screen (`???`), let the viewer hold it, then introduce the mechanism | `_2024/transformers/network_flow.py` ~175–207 |
| Give repeated trials a fixed pulse (dials randomised five times, one second each) | `_2024/transformers/old_auto_regression.py` ~558–571 |
| Stagger many related arrivals with `LaggedStart` + `Succession`, then remove them | `old_auto_regression.py` ~501–521 |
| One tracker drives wrapping, arrows, centre of mass, graph point and traced curve; one carrier transforms into its wrapped state, no source copy left behind | `_2018/fourier.py` `wrap_around_circle`, `change_frequency` |
| Keep a value/graph connector local to one panel | `_2018/fourier.py::get_graph_v_line` |
| Isolate one neuron/example before the full system; literal pixel-to-input correspondence; connections behind neurons; complete edge-group propagation | `_2017/nn/part1.py` `NetworkMobject`, `PreviewMNistNetwork`, `IntroduceEachLayer` |
| Show two → show all → average → collapse into one vector | `_2017/nn/part3.py::ConstructGradientFromAllTrainingExamples` |
| Token-to-vector identity, concurrent motion, progressive system build | `_2024/transformers/network_flow.py::HighLevelNetworkFlow` |
| Focus on one vector before revealing the same operation in parallel; one query at a time with selective dimming | `_2024/transformers/mlp.py::BasicMLPWalkThrough`, `attention.py` |
| Make a dot product spatial before writing it; one direction, then several, then the high-dimensional generalisation | `_2024/transformers/embedding.py` `DotProducts`, `ManyIdeasManyDirections` |
| Local changes and gradients made causal rather than decorative | `_2017/gradient.py` |

Manim GL → CE reminders when reading them: `ShowCreation` → `Create`; `Tex` for
maths → `ty.maths`; `TexText` → `ty.words`; `DEG` → `DEGREES`;
`self.frame.reorient(...)` has no blind translation; `set_anim_args` → pass
timing to `self.play`.
