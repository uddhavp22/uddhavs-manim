# Chapter B animation reimplementation playbook

Working reference for redesigning Chapter B under Manim Community Edition
0.20.1. This is deliberately narrower than `docs/MANIM_GUIDE.md`: it focuses on
animation structure, continuity, and iteration for this chapter.

Last checked against the official Manim CE 0.20.1 documentation on 2026-08-08.

## First: where script changes belong

`SCRIPT_chapterB.md` is generated output. It is useful for reading the whole
chapter, but it is not render input and the next dump will overwrite edits to
it. The spoken source of truth is each scene's `self.voiceover(text=...)`
block.

For a broad rewrite:

1. Draft in a separate working document if that is more comfortable.
2. Move approved passages into the scene files, either directly or through
   `tools/renarrate.py`.
3. Regenerate the readable master:

   ```bash
   .venv/bin/python tools/script_dump.py \
       projects/sigreg_explainer/chapterB \
       -o projects/sigreg_explainer/SCRIPT_chapterB.md
   ```

4. Treat that regenerated file as the review copy.

Framing should settle before detailed choreography. A changed sentence often
changes which object must be visible, which event needs a bookmark, and how
long the animation has to breathe.

## The design unit is a beat, not an effect

Before coding a beat, write five lines:

```text
viewer before:
viewer after:
visible operation:
changes:
stays fixed:
```

Then add an event sheet:

| Spoken phrase | Visual event | Why it moves | Must land exactly? |
|---|---|---|---|
| names the operation | operation begins | connects language to geometry | bookmark |
| explains the invariant | fixed object remains visible | prevents a false inference | no |
| states the result | final state holds | gives inspection time | usually no |

This catches the common failure where the code is polished but the viewer
cannot tell what changed. One dominant focal event per beat remains the default.
Two simultaneous events are justified when their correspondence is the point,
as in the line moving home while the same samples wrap into a circle.

## Choose the mechanism from the meaning

| Need | Prefer | Reason |
|---|---|---|
| one object changes state | `.animate`, `Transform`, or `MoveToTarget` | keeps one visible identity |
| an object truly becomes another | `ReplacementTransform` | source leaves; target owns the next state |
| a source produces a second representation | `TransformFromCopy` | source stays while its visual descendant appears |
| equation terms persist across a rewrite | `TransformMatchingTex` | shared symbols keep their identity |
| many properties depend on one scalar | `ValueTracker` plus updater | one source of truth |
| cheap geometry can be rebuilt per frame | `always_redraw` | concise and reliable |
| instance identity must persist | build once plus `add_updater` | fixed registration, z-order, and references survive |
| several events start together | one `self.play(...)` or `AnimationGroup` | explicit concurrency |
| events happen in order | `Succession` | explicit sequencing |
| similar objects enter with overlap | `LaggedStart` or local `lagged_map` | controlled stagger |
| a moving point's history is the claim | `TracedPath` | makes temporal history persistent |

The mechanism should expose the mathematical relationship. A smoother effect
is not automatically a clearer one.

## Pattern 1: one tracker owns one mathematical parameter

If `t` changes the arrows, centroid, readout, rider, and partial curve, every
one of those should read the same `ValueTracker`. Do not animate five derived
objects separately and hope they finish together.

```python
rig = ThreePanelRig(samples)
rig.mount(self, link=True)

with self.voiceover(
    text="Raise the frequency. The samples stay fixed while their phases change."
) as tracker:
    self.across(
        tracker,
        rig.t.animate.set_value(4.0),
        floor=4.0,
        rate_func=linear,
    )
```

Use `linear` when screen distance represents change in the parameter and the
viewer should compare speeds. Use `smooth` for a finite repositioning where
gentle starts and stops aid tracking. This project does not use bounce,
elastic, or overshoot easing.

## Pattern 2: `always_redraw` for cheap derived geometry

`always_redraw(factory)` calls the factory every frame and returns a new shape
through the same wrapper. It is ideal for a dot, arrow, short line, or partial
curve derived from trackers.

```python
t = ValueTracker(0.0)
rider = always_redraw(
    lambda: Dot(
        axes.c2p(t.get_value(), f(t.get_value())),
        radius=0.08,
    ).set_fill(AVERAGE, 1)
)

self.add(rider)
self.play(t.animate.set_value(4.0), run_time=4.0, rate_func=linear)
```

Keep the factory cheap:

- precompute sample-independent grids and tables;
- do not construct `MathTex`, `Text`, or a large sampled graph every frame;
- use `axes.c2p(...)`, never raw screen coordinates for data geometry;
- clear updaters before fading or removing dynamic objects.

`ThreePanelRig._refresh()` and `_curve()` already follow the right pattern:
the empirical curve is computed once, then the visible prefix is rebuilt from
the stored table.

## Pattern 3: build once when object identity matters

An updater can mutate a persistent instance instead of replacing it every
frame. Prefer this for fixed-in-frame/fixed-orientation objects, objects held
by other references, or geometry whose draw order must not change.

```python
rider = Dot(radius=0.08).set_fill(AVERAGE, 1)
rider.add_updater(
    lambda mob: mob.move_to(
        axes.c2p(t.get_value(), f(t.get_value()))
    ),
    call_updater=True,
)
self.add(rider)

self.play(t.animate.set_value(4.0), run_time=4.0, rate_func=linear)
rider.clear_updaters()
```

For geometry that genuinely needs rebuilding, preserve the wrapper instance
with `become`:

```python
curve = VMobject()
curve.add_updater(
    lambda mob: mob.become(build_partial_curve(t.get_value())),
    call_updater=True,
)
```

Manim normally suspends the main mobject's updater while directly animating
that same mobject. Avoid asking an updater and a `Transform` to control the
same object in the same `play`; animate the tracker or suspend/clear the updater
first.

## Pattern 4: hand off static objects to live objects explicitly

Ghosts appear when an introductory static copy and its live updater-backed
replacement both survive. Treat the handoff as ownership transfer.

```python
seed = build_at_initial_state()
live = always_redraw(build_from_trackers)

self.add(seed)
# Animate the introduction while `seed` is the owner.

# At a frame where both factories produce the same visible state:
live.update(0)
self.add(live)
self.remove(seed)
```

If the handoff must be visible, cross-fade briefly, but never leave both copies
at full opacity. Afterward, store and later remove the live object, not the
obsolete seed. The `b03` wrap and `ThreePanelRig.mounted_dots` are the chapter's
main examples of this rule.

## Pattern 5: choreograph concurrency on one timeline

Use one `play` when events describe the same operation. `squish_rate_func`
places short sub-events on a shared normalized timeline without nesting a
pile of waits.

```python
self.play(
    rig.kappa.animate.set_value(1.0),
    rig.line.animate.move_to(layout.RIG_LINE_CENTRE),
    FadeOut(
        seed_dots,
        rate_func=squish_rate_func(smooth, 0.00, 0.15),
    ),
    FadeIn(
        home_dots,
        shift=0.1 * UP,
        rate_func=squish_rate_func(smooth, 0.78, 1.00),
    ),
    run_time=3.2,
)
```

Use the composition classes deliberately:

```python
# together
AnimationGroup(anim_a, anim_b, lag_ratio=0)

# partly overlapping
LaggedStart(anim_a, anim_b, anim_c, lag_ratio=0.18)

# strictly ordered
Succession(anim_a, anim_b, anim_c)
```

An `AnimationGroup` or `LaggedStart` `run_time` rescales the child timings to
fit the whole group. Verify the resulting rhythm in the MP4; do not infer it
from the child durations alone.

For a collection of compound mobjects in this repo, use
`common.anim.lagged_map`, not `LaggedStartMap` directly. CE's default argument
unpacking can bind an arrow tip or text glyph as an animation argument.

## Pattern 6: preserve causal identity with the right transform

The transform classes differ in scene ownership:

- `Transform(source, target)` mutates `source`; `target` is only the shape it
  aims at.
- `ReplacementTransform(source, target)` removes the source and leaves the
  target in the scene.
- `TransformFromCopy(source, target)` leaves the source and transforms a copy
  into the target.
- `Scene.replace(old, new)` performs a non-animated swap while preserving draw
  order.

For Chapter B, `TransformFromCopy` is especially useful for explicit mappings:

```python
landing = Dot(circle_point).set_fill(CLOUD, 1)
self.play(TransformFromCopy(sample_dot, landing), run_time=1.2)
```

That says “this sample produces this landing point” without destroying the
number-line representation. Use it selectively; copying every item at once
creates visual noise.

When a path carries meaning, specify it. `.animate` interpolates endpoints;
`.animate.rotate(PI)` does not show the actual rotation through angle `PI`.

```python
self.play(Rotate(arrow, angle=PI, about_point=arrow.get_start()))
self.play(dot.animate(path_arc=PI / 3).move_to(target_point))
```

## Pattern 7: make equations inherit meaning from the picture

Compile equations once, isolate meaningful terms, and reveal them only after
the corresponding visible operation exists.

```python
empirical = MathTex(
    R"\hat\varphi_N(t)",
    "=",
    R"\frac{1}{N}",
    R"\sum_{j=1}^{N}",
    R"e^{itx_j}",
    font_size=ty.EQ_DISPLAY,
)
```

For an algebraic rewrite:

```python
next_line = MathTex(
    R"\hat\varphi_N(t)", "=", R"C(t)", "+", "i", R"S(t)",
    font_size=ty.EQ_DISPLAY,
)
self.play(TransformMatchingTex(empirical, next_line), run_time=1.4)
```

Split `MathTex` into stable semantic units or use
`substrings_to_isolate`; matching works from the TeX strings of the
submobjects. Use `TransformFromCopy` when a visible arrow, gap, or area should
give birth to one equation term.

English belongs in `common.type.Text`/`ty.*`; mathematics belongs in
`MathTex`/`ty.maths`. Use `ty.line(...)` for mixed prose and mathematics so
unsupported Unicode glyphs do not silently fall back to another font.

## Pattern 8: focus with state, not decoration

Chapter B is a two-dimensional argument and rarely needs camera motion. A
camera move is justified only when it reveals a relation that cannot be framed
clearly otherwise. Prefer:

- dimming inactive panels;
- temporarily enlarging the active group;
- moving a label next to its referent;
- a short dashed link between corresponding points;
- keeping an invariant object visible while the active object moves.

```python
self.play(
    inactive.animate.set_opacity(0.25),
    active.animate.scale(1.08),
    run_time=0.6,
)
```

Restore state afterward rather than building a second copy. `save_state()` and
`Restore(mob)` are useful when several style/position properties change
together.

Use `set_z_index` for stable layers:

```python
shade.set_z_index(-2)
axes.set_z_index(-1)
curve.set_z_index(1)
label.set_z_index(2)
```

Do not rely on incidental `add()` order once objects are introduced by several
animations or rebuilt by updaters.

## Pattern 9: show history only when history is information

`TracedPath(point.get_center)` is useful when the path taken is itself the
claim. It should not replace a known function graph merely because it is easy.
For the characteristic-function panels, the existing precomputed-table and
visible-prefix approach is better: it is deterministic, can be reset on batch
swaps, and cannot retain an obsolete trail.

If a trace is used, decide whether it should persist or dissipate, and remove
or clear it when the state changes.

## Pattern 10: let narration own duration without creating blank frames

One voiceover block should normally correspond to one conceptual beat.

```python
with self.voiceover(
    text="The samples stay fixed. Only the wrapping frequency changes."
) as tracker:
    self.across(
        tracker,
        rig.t.animate.set_value(3.0),
        floor=3.0,
        rate_func=linear,
    )
```

Use a bookmark when an event must land on a word:

```python
with self.voiceover(
    text="The vertical pieces <bookmark mark='cancel'/>cancel in pairs."
) as tracker:
    self.wait_until_bookmark("cancel")
    self.across(tracker, FadeOut(vertical_parts), floor=0.8)
```

Use `reserve=` when a second event still has to happen inside the block. Use
`inspect()` only after a meaningful state change that the viewer can examine.

Do not fade the last visible object while narration remains. The context
manager waits out unused audio after the code inside it finishes; if the last
object has already faded, that remainder becomes narrated black video. A title
card should either remain until the block ends or hand directly to the first
substantive object before it disappears.

## Pattern 11: make scene boundaries explicit

The chapter master is a raw stream concatenation; it has no crossfades.

- Use `clear_beat()` for an honest hard cut.
- Use `clear_overlay(...)` only for a real match cut where the next scene
  reconstructs the exact same rig state.
- Record each scene's entry and exit state in its plan.
- Compare the outgoing last frame with the incoming first frame after either
  scene changes.

Do not fake continuity across different data, axes, colors, tracker values, or
panel geometry. A visible cut is clearer than an almost-matching apparatus.

## Chapter B mechanism map

This is a starting map, not a locked storyboard. Re-derive it after the script
and framing change.

| Scene | Load-bearing visible operation | Likely mechanism |
|---|---|---|
| `b00` | unlike batches produce the same summaries | shared layout factories; staged metric reveals; hold both batches as invariants |
| `b01` | one moving sample leaves counts flat, then makes them jump | one sample-position tracker; histogram derived from it; emphasize discontinuity without fake smooth interpolation |
| `b02` | unit-arrow components add and cancel | `Rotate`; component lines; `TransformFromCopy`; persistent average arrow |
| `b03` | number line wraps while moving into the three-panel rig | `kappa`, `rigid`, and `t` trackers; explicit static/live handoff; concurrent choreography |
| `b04` | the already-seen operations compress into the empirical-CF formula | copy visual parts into isolated equation terms; no fresh apparatus |
| `b05` | different batches stress-test one persistent rig | `ThreePanelRig.swap`; precomputed tables; reset `t`; keep panel geometry fixed |
| `b06` | `t=0` forces every arrow to one | short tracker move to zero; persistent anchor; restrained hold |
| `b07` | a spread-out batch aliases at one frequency | one frequency tracker; exact aligned state plus a small nudge; keep sample positions fixed |
| `b08` | one measurement becomes a complete curve, then a cited theorem | identity-preserving expansion from point to curve; clearly separate visual evidence from theorem statement |
| `b09` | low-frequency similarity gives way to separation, then noise | precomputed curves; temporary focus regions; avoid animating all trials as equal focal objects |
| `b10` | the Gaussian target becomes a visible reference curve | equation and curve built as one object-relation; direct title-to-content handoff; no narrated black gap |
| `b11` | pointwise complex gap sweeps into a squared-gap curve and area | one `t` tracker; linked endpoints; derived gap; visible-prefix curve; staged `TransformMatchingTex` |

The unresolved note currently embedded in `b00` is pedagogical, not a Manim
problem. Resolve why that example earns its runtime before investing in new
animation plumbing for it.

## Local failure modes to guard against

- A static seed and an `always_redraw` successor both remain visible.
- An updater recreates expensive text or hundreds of curve points every frame.
- The same mobject is controlled by both an updater and a direct transform.
- `.animate.rotate(...)` is used when the rotational path is the lesson.
- A `Transform` is followed using the target variable even though the source
  remained the scene-owned object.
- `LaggedStartMap` is used directly on arrows or text instead of
  `common.anim.lagged_map`.
- Dot styling changes between Manim variants are assumed from memory. In the
  installed CE 0.20.1, both `Dot(color=...)` and `Dot(fill_color=...)` set the
  fill; this project generally uses `.set_fill(..., 1)` to make opacity
  explicit.
- A scene imports `Text` from Manim instead of `common.type`.
- Raw coordinates are used for marks attached to axes instead of `c2p`.
- An updater survives into a fade or teardown and resets opacity every frame.
- An on-screen Unicode math glyph bypasses `MathTex` and silently falls back.
- Several unrelated panels animate simultaneously.
- A title card fades before its voiceover block finishes.
- A scene-level render works, but the boundary fails in the concatenated
  master.

## Reimplementation loop

Work one conceptual beat at a time:

1. Update narration in the scene source and regenerate `SCRIPT_chapterB.md`.
2. Write the beat sheet: before, after, operation, change, invariant.
3. Reuse or extend `common/` before introducing scene-local duplication.
4. Run static checks:

   ```bash
   .venv/bin/python tools/preflight.py \
       projects/sigreg_explainer/chapterB \
       projects/sigreg_explainer/common

   .venv/bin/python tools/narration_audit.py \
       projects/sigreg_explainer/chapterB
   ```

5. Render the affected scene in draft voice at low quality:

   ```bash
   ./render.sh \
       projects/sigreg_explainer/chapterB/b03_the_rig.py B03 -ql
   ```

6. Watch the MP4 normally, muted, and at the worst transition frame. Rendering
   without errors is not visual verification.
7. Optionally run collision diagnostics on a draft:

   ```bash
   SIGREG_VISION=1 ./render.sh \
       projects/sigreg_explainer/chapterB/b03_the_rig.py B03 -ql
   ```

   Treat the report as evidence to triage, not an automatic failure gate.
8. Render important motion at `-qh`; `-ql` is 15 fps and is not a motion-
   smoothness reference.
9. Rebuild the real chapter master after scene boundaries or shared inputs
   change:

   ```bash
   projects/sigreg_explainer/build.sh chapterB -qh --voice eleven --force
   ```

10. Inspect the master and run output-level checks:

    ```bash
    .venv/bin/python tools/dead_air.py --min 1.5 \
        media/masters/sigreg_explainer/chapterB_master.mp4

    .venv/bin/python tools/still_frames.py --min 2.5 \
        media/masters/sigreg_explainer/chapterB_master.mp4
    ```

ElevenLabs is the final timing authority. Draft voice is for geometry and
iteration; any beat whose choreography depends on phrase timing must be checked
again against the rebuilt ElevenLabs master.

## Official Manim references used

- [Animation composition: `AnimationGroup`, `LaggedStart`, and `Succession`](https://docs.manim.community/en/stable/reference/manim.animation.composition.html)
- [`AnimationGroup` timing and `lag_ratio`](https://docs.manim.community/en/stable/reference/manim.animation.composition.AnimationGroup.html)
- [`ValueTracker`](https://docs.manim.community/en/stable/reference/manim.mobject.value_tracker.ValueTracker.html)
- [`always_redraw` and updater utilities](https://docs.manim.community/en/stable/reference/manim.animation.updaters.mobject_update_utils.html)
- [`Transform`, including `path_arc`](https://docs.manim.community/en/stable/reference/manim.animation.transform.Transform.html)
- [`ReplacementTransform`](https://docs.manim.community/en/stable/reference/manim.animation.transform.ReplacementTransform.html)
- [`TransformFromCopy`](https://docs.manim.community/en/stable/reference/manim.animation.transform.TransformFromCopy.html)
- [`TransformMatchingTex`](https://docs.manim.community/en/stable/reference/manim.animation.transform_matching_parts.TransformMatchingTex.html)
- [`TracedPath`](https://docs.manim.community/en/stable/reference/manim.animation.changing.TracedPath.html)
- [`Mobject.animate`, updater, state, and z-index behavior](https://docs.manim.community/en/stable/reference/manim.mobject.mobject.Mobject.html)
- [`Scene` ownership, replacement, waits, and lifecycle](https://docs.manim.community/en/stable/reference/manim.scene.scene.Scene.html)
- [Manim's render-loop and updater lifecycle](https://docs.manim.community/en/stable/guides/deep_dive.html)
- [Configuration, caching, quality, and section flags](https://docs.manim.community/en/stable/guides/configuration.html)

The official deep-dive warns that its detailed renderer walkthrough began at
Manim 0.16.0. The lifecycle points used here were cross-checked against the
current 0.20.1 reference pages and this repo's editable `../manim-ce` source;
repo-specific behavior remains governed by `docs/MANIM_GUIDE.md` and the
project's `common/` package.
