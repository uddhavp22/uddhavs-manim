# C06 revision design — "one continuous proof"

Working document for the 2026-08-24 revision of
`chapterC/c06_every_direction.py`, written against owner review of the
182 s ElevenLabs render. Delete once the revision has shipped and been
signed off.

## 0. The structural verdict

The scene currently runs the *same* construction twice — graph → ray → sweep
→ field, once for Z at 0:57–1:25 and again implicitly when the two fields
morph at 2:00–2:30 — and the second run is decorative rather than
inferential. That duplication is the seam the owner is feeling. The fix is
not to smooth transitions. It is to **let the frequency field be built
exactly once, at the moment it carries logical weight**, and to make the
1-D radial slice the object that is compared, deformed, and quantified over.

Resulting spine, one pass, no backtracking:

```
turn u  →  target: every projection is N(0,1)
        →  ONE shadow's CF = a radial slice φ_Z(tu)           [derivation]
        →  two clouds, same mean & covariance, DIFFERENT slices  [the stake]
        →  deform until the slices agree                       [the attempt]
        →  every u ⇒ every slice ⇒ the whole CF                [the quantifier;
                                                                field built HERE, once]
        →  Chapter B uniqueness ⇒ same distribution            [the citation]
        →  that implication is Cramér–Wold                     [the name]
        →  specialise to Z                                     [the payoff]
```

Edits land in `chapterC/c06_every_direction.py`, with supporting changes in
`common/data.py` and `facts.py`.

## 1. Radial slice is primary; the two-field morph is discarded

**Decision: the field appears once, after the slices agree, as the
accumulation of slices.**

1. **The field cannot show sign; the slice can.** `_field_alpha` takes
   `np.abs(...)`. The ring's characteristic function is `J₀(√2‖ξ‖)`, which
   goes negative; drawn as brightness its negative lobes render *bright*.
   The single most informative fact about the rival — its CF crosses zero
   where the Gaussian's never does — is destroyed by the field encoding and
   is trivially visible on a 1-D curve.
2. **The slice is the object the derivation produced.** `φ_{u⊤Z}(t)` *is*
   the 1-D graph. Comparing it means the comparison beat consumes the
   derivation beat's output instead of starting from a new object.
3. **The field is the conclusion of the covering argument, not a premise.**
   "All projections recover the whole CF" is precisely "sweeping u fills the
   plane with rays". If the field already exists before that sentence, the
   sentence has nothing to do.
4. **It gives brightness a reason to exist.** Deferred to the covering step,
   the motivation is forced: you cannot draw a curve on a thousand rays, so
   the value has to go onto the ray itself.

| Existing | Verdict |
|---|---|
| `RING_PROFILE` | kept, re-purposed to feed a 1-D curve, not a field texture |
| `GAUSSIAN_PROFILE`, `_field_lookup`, `_field_alpha`, `_field_image`, `FIELD_*` | kept unchanged, called once, for one MAGNITUDE field |
| `morph_rival_field` | discarded |
| `rival_field` ImageMobject in RIVAL | discarded |
| `ray`, `ray_opacities`, `update_ray` | kept, re-homed from beat 3 to beat 7 |
| `trail_rays`, `reveal_trail` | kept, re-homed from beat 3 to beat 7 |
| `EXAMPLE_TS` three example points | discarded — a separate mini-demonstration; beat 7's legend supersedes it |
| `pick` example-point ξ readout | discarded — redundant with beat 7's covering argument |
| `move_rival_points` / `morph` tracker | modified: becomes an exact-mixture wave (§3) |

New scene-wide invariant, worth a comment in the file: *brightness only ever
encodes a non-negative characteristic function; this scene never draws a
signed field.* With the ring field gone this now holds, and retro-justifies
`_field_alpha`'s `abs()`.

## 2. Revised beat sheet

Narration is the spoken text verbatim. Bookmarks fire the reveal **before**
the phrase that names the thing.

### Beat 1 — Turn u (≈13 s; replaces 329–365)

> `<bookmark mark='turn'/>`Keep turning the direction u. `<bookmark
> mark='fill'/>`Every angle gives another shadow of the same cloud, and a
> full turn of u produces the whole family of them. `<bookmark
> mark='ask'/>`One direction was enough to catch this cloud lying on a line.
> Does the whole family pin the cloud down completely?

Screen unchanged: plane, line cloud, `y=x` label, active `u` arrow/line fade
in on `turn`; on `fill` a 0.4 s hold, then `angle → shadow_angles[0] + TAU`
with wheel ring, spokes and eight `shadow_plots` lagging in.

"every direction has had its turn" removed here as well as later (§4.5). The
closing question is new and is what makes the rest of the scene one argument
rather than a tour.

### Beat 2 — The target (≈21 s; replaces 412–475)

> `<bookmark mark='gaussian'/>`Suppose the cloud itself is standard
> Gaussian. `<bookmark mark='spread'/>`Its spread is the identity in every
> direction, so projecting onto any unit direction leaves the variance
> exactly one. `<bookmark mark='hold'/>`The direction can swing anywhere it
> likes and that number stays where it is, `<bookmark mark='turn'/>`so every
> unit direction produces the same standard Gaussian shape — which is the
> target each of these shadows has to match.

Mechanics unchanged. Two edits: the `reason` bookmark is deleted (the flick
loop budgets against `turn`), and the finite-batch sentence is gone.

**Supporting change.** `_standardized_isotropic_points` should **whiten**
rather than standardise per-coordinate (subtract mean, then multiply by
`Σ^{-1/2}`). Then the live `Var[u⊤Z]` readout is exactly `1.00` for every u,
which is what the narration now asserts without the finite-batch escape
clause. Re-run `facts.py`'s seed-76 projection check afterwards.

### Beat 3 — One shadow's CF is a radial slice (≈32 s; replaces 489–563 and 565–633; discards 635–677)

> `<bookmark mark='one'/>`Take the shadow along a single direction on its
> own. It is an ordinary batch of numbers, so it has a characteristic
> function. Writing that function out connects it directly to the cloud's
> own. `<bookmark mark='define'/>`By definition it averages a unit arrow
> whose angle is t times the projected value. `<bookmark
> mark='regroup'/>`The projected value is a dot product, so that angle is
> the point z dotted with t u. `<bookmark mark='identity'/>`Averaged over
> the cloud, that is the cloud's own characteristic function at the single
> point t u. `<bookmark mark='meaning'/>`So u fixes a ray out from the
> origin of frequency space, raising t slides the point t u along it,
> `<bookmark mark='trace'/>`and the shadow's curve is what the cloud's
> characteristic function does along that ray.

- `one`: snap `angle` to one of the eight `shadow_angles` (the upper-left
  one, ~135°, so the ray stays clear of the right-hand CF panel). **Keep
  that single `shadow_plot` visible**; fade the other seven and the cloud
  dots. `converse_axes` + `converse_curve` + `converse_panel_label` +
  `converse_eq[0]` create at `RIG_CF_CENTRE`. This is what satisfies the
  owner's "start from an already-visible direction".
- `define` → `converse_eq[1]`; `regroup` → `converse_eq[2]`; `identity` →
  `Indicate(converse_eq[2])`.
- `meaning`: the sample-space plane fades out and a frequency-space frame
  fades in — `ξ₁`/`ξ₂` axis labels on the wheel's own axes plus
  `freq_tag = ty.caption("frequency space")`. A dashed `DIRECTION`-dim guide
  line runs origin → `SPOKE_RADIUS·u`.
- `meaning`/`trace`: the `t_val` sweep. `graph_tracer` runs along the curve;
  `freq_tracer` runs along the guide line at `t·t_scale_wheel·u`. **Both
  tracers are `INK`; neither carries a value or a brightness** — this beat
  establishes *which point* `ξ = tu` is, not what its value looks like.

`update_freq_tracer`'s brightness lines are removed; it becomes a plain
`INK` dot. `ray`/`ray_opacities`/`update_ray` are **not** used here.

**Fixes a live defect.** The current script says "frequency space" while
nothing on screen is labelled as such until much later. Moving `freq_tag`
here repairs a real violation of never-name-before-it-is-on-screen.

### Beat 4 — A second cloud with the same first two moments (≈18 s; replaces 745–831 and 851–857)

> `<bookmark mark='second'/>`Now take a second cloud. Start from the same
> points, and push them outward until they sit on a ring rather than piling
> up in the middle. `<bookmark mark='moments'/>`Its mean is still zero, and
> its covariance is still the identity, so nothing built from those two
> numbers can tell the clouds apart. `<bookmark mark='differ'/>`They are
> plainly not the same distribution.

Three columns, held for beats 4–6:

| | x | contents |
|---|---|---|
| left | ≈ −4.9 | cloud **X** (the Gaussian), radius ≈1.2, centre y ≈ +0.5 |
| centre | 0 | `converse_axes` + `converse_curve`, moved from `RIG_CF_CENTRE` |
| right | ≈ +4.9 | cloud **Y** (the ring), same size and y |

Captions above each cloud (`ty.caption`, `MAGNITUDE` / `RIVAL`), in-place
`X` / `Y` maths labels beside each, and beneath each a two-line MUTED
`ty.BODY` block in **C02's moment grammar**
(`chapterC/c02_the_shape_is_the_goal.py` lines 123–136):

```
E[X] = 0                E[Y] = 0
Cov(X) = I              Cov(Y) = I
```

Sequence: `cloud.freeze()`; the frozen `cloud.dots` scale and slide left
(safe once frozen — the hazard already documented in the existing file).
`second`: the dot group is copied to the right panel by a `LaggedStart` of
`TransformFromCopy`s, then the copies migrate outward onto ring positions
using the §3 wave updater run at `mix: 1 → 0`. `moments`: both blocks fade
in together. `differ`: a simultaneous `Indicate` of both blocks.

**Why Y is a copy of X's points.** The owner asks for "the same visual
grammar the Gaussian cloud was built with". The Gaussian cloud in this scene
was never built from nothing — it *morphed from C05's line* via
`cloud.animate_base_points`. The faithful reading of "same grammar" is
therefore *a continuous migration of persisting dot instances*, not a
`FadeIn` of a fresh sample. Building Y from X's own points satisfies that,
makes the shared moments a property of the construction the viewer watched,
and makes beat 6's endpoint literally X's configuration again.

Whiten the ring sample too, so `Cov(Y) = I` is exactly true of the pictured
points.

### Beat 5 — The two slices differ (≈23 s; replaces 838–842)

> `<bookmark mark='project'/>`Project both clouds onto the same direction.
> `<bookmark mark='shadows'/>`The Gaussian's shadow is one hump; the ring's
> is two, pushed out to either side — and those two batches still have the
> same mean and the same variance, which is exactly where Chapter B started.
> `<bookmark mark='curves'/>`Their characteristic functions do not agree at
> all. The ring's dips below zero where the Gaussian's is still falling
> smoothly, `<bookmark mark='gap'/>`so a single direction already separates
> two clouds that the moments could not.

- `project`: one `DIRECTION` arrow through each cloud at the same fixed `u`.
  u does **not** turn during beats 4–6 — a single slice is the unit of
  comparison.
- `shadows`: a live mini dot-plot tangent to the outer edge of each cloud,
  driven by that cloud's current points. Reuses the wheel's shadow grammar
  verbatim — `layout.stack_levels`, `MINI_X_SCALE`, `MINI_STACK_STEP`,
  `MINI_DOT_RADIUS`. New: the updater reads each comparison cloud rather
  than `cloud.current_points()`.
- `curves`: the centre axes already carries the `MAGNITUDE` Gaussian curve
  (`converse_curve`, the same mobject the derivation produced). A second
  `RIVAL`-coloured curve draws in: `J₀(√2 t)`, from `RING_PROFILE`. Axes
  `y_range` must widen to `(-0.55, 1.15)` — `J₀` bottoms at ≈ −0.40. Build
  `converse_axes` with that range from the start so it is one object
  throughout.
- `gap`: a short `COLLAPSE`-coloured vertical rule at the t where the curves
  are furthest apart, or an `Indicate` on the ring curve's negative lobe.

The Chapter B callback is load-bearing: the ring's projection is a
two-humped batch with mean 0 and variance 1 — literally the counterexample
`b00_the_problem` opens on. Saying so costs three seconds and converts this
beat from a new example into the chapter's own thread.

### Beat 6 — Deform until they agree (≈16 s; replaces 864–893)

> `<bookmark mark='push'/>`Now move the ring's points back, a few at a time,
> into the positions the Gaussian's points occupy. `<bookmark
> mark='follow'/>`The shadow closes up into a single hump, and its
> characteristic function climbs toward the other one. `<bookmark
> mark='meet'/>`The two curves only lie on top of each other at the moment
> the two clouds do.

`mix: 0 → 1` over ~11 s, `rate_func=linear`. Three things move off one
tracker: Y's dots (wave migration), Y's live shadow dot-plot (two humps
merging into one bell — the strongest single image in the section), and the
`RIVAL` curve rising to coincide with the `MAGNITUDE` one. At `mix = 1` Y's
dots sit exactly on X's frozen configuration, translated; a brief `Indicate`
on the coincident curves.

The `morph` `ValueTracker` and the staggered-delay idea survive;
`move_rival_points` is rewritten per §3; `morph_rival_field` is deleted and
replaced by a one-line curve updater re-pointing the `RIVAL` VMobject from
the blended profile.

### Beat 7 — Every direction, and the field (≈27 s; re-homes 680–740)

> `<bookmark mark='one_dir'/>`That was one direction. Its curve says what
> the characteristic function does along a single ray, and the rest of the
> plane is still blank. `<bookmark mark='encode'/>`Drawing the curve's
> height as brightness at the point t u instead puts the same information on
> the ray itself, `<bookmark mark='lit'/>`so the whole curve becomes a line
> of light, bright at the origin and fading out where the curve falls.
> `<bookmark mark='sweep'/>`Turning u carries the ray around with it,
> `<bookmark mark='fill'/>`and since every point of frequency space sits at
> some distance along some direction, the sweep leaves nothing uncovered.

- `one_dir`: clouds, captions, X/Y labels, moment blocks and both shadow
  plots fade out. The axes + curve travel **back** to `RIG_CF_CENTRE` — the
  apparatus returns to its beat-3 configuration, which is the visual
  statement that this is the same argument continuing. Wheel ring, spokes,
  `u` arrow and `freq_tag` come back up at origin.
- `encode` — **the explicit height→brightness explanation.** One legend row
  under the axes:

  `ty.caption("height")` — `ty.maths("=")` — `ty.maths(R"\varphi_X(tu)",
  color=MAGNITUDE)` — `ty.maths("=")` — `ty.caption("brightness")`

  `ty.LABEL`/`CAPTION` scale, MUTED words, maths in `MAGNITUDE`. It says the
  correspondence *is* the equation, so it introduces no new visual
  vocabulary. Exits with the axes.
- `lit`: `ray` lights from origin outward over ~1.2 s, segment opacities
  from `ray_opacities`; the graph curve fades as the ray reaches full
  length. `update_ray` is driven by a reveal tracker instead of `t_val`.
- `sweep`/`fill`: `angle → +TAU` with `trail_rays` + `reveal_trail` exactly
  as written today, then `_field_image(GAUSSIAN_PROFILE, MAGNITUDE)` fades
  in and the fan fades out.

~95% of the existing 680–740 is reused verbatim, re-sequenced and given a
different narrative job.

### Beat 8 — Uniqueness, then the name (≈22 s; replaces 894–899 and 918–972)

> `<bookmark mark='if'/>`So if two clouds cast the same shadow in every
> direction, every one of those rays carries the same values for both of
> them, and their characteristic functions agree at every point of the
> plane. `<bookmark mark='unique'/>`Chapter B's uniqueness result finishes
> it: distributions with the same characteristic function everywhere are the
> same distribution. `<bookmark mark='statement'/>`Written out, that is the
> implication — matching every one-dimensional projection forces the joint
> distributions to match. `<bookmark mark='name'/>`It is called the
> Cramér–Wold theorem.

- `if`: field on screen, one gentle pulse of the whole disc. Shrink the
  field to ~0.8 to clear the top and bottom text bands.
- `unique`: `uniqueness_recall` (`φ_X = φ_Y ⟹ X =ᵈ Y`) fades in at the
  bottom edge, unchanged.
- `statement`: `cw_statement` + `quantifier_box` at the top edge,
  `Indicate(quantifier_box)`.
- `name`: `cw_label` fades in **centred** under `cw_statement`.

**The off-centre label, fixed two ways.** `aligned_edge=RIGHT` is dropped:
`.next_to(cw_statement, DOWN, buff=0.38)` then `layout.fit_in_frame`. And
the name gets its own short sentence so the bookmark sits at a sentence
boundary — the label fades in during "It is called the…" and the words
"Cramér–Wold" land ~0.9 s later with the label already settled. Nothing
about the theorem exists on screen before `statement`.

"an extension of uniqueness" is gone. The chain is spoken in order: same
shadows → same values on every ray → same CF everywhere → Chapter B's
uniqueness → same distribution → that implication has a name.

"one direction, one distance along it", "one direction at a time", "every
direction has had its turn", "every ray, every point" are all deleted.

### Beat 9 — Specialise and close (≈25 s; replaces 973–1116, discards 1006–1051)

> `<bookmark mark='specialize'/>`For the target being matched, every one of
> those shadows is the same curve — e to the minus t squared over two.
> `<bookmark mark='field'/>`Read out along every ray, that single curve
> fills the plane with e to the minus the squared distance from the origin,
> over two. `<bookmark mark='resolve'/>`Only one cloud has that
> characteristic function: `<bookmark mark='conclude'/>`Z itself, standard
> Gaussian in every dimension. `<bookmark mark='payoff'/>`So the theorem
> buys this: a distribution in D dimensions can be pinned down without ever
> looking at it in D dimensions. A family of one-dimensional shadows is
> enough.

Keep the existing two-step clears — they fix real overlap bugs. `specialize`:
clear `cw_statement`/`cw_label`, then `specialize_eq` at the top edge.
`field`: `field_label` (`φ_Z(ξ) = e^{-‖ξ‖²/2}`). `resolve`/`conclude`: clear
the frequency-space frame, restore the wheel, spokes, `shadow_baselines`,
`shadow_dot_groups`, `target_curves` and the cloud at origin, and fade in
`conclusion` (`Z ~ N(0, I_D)`). That is the state C07 inherits.

Discarded: the `pick` beat (`example_line`, `example_dot`, `example_label`,
`t = ‖ξ‖, u = ξ/‖ξ‖`, the numeric readout). It re-teaches the polar reading
of ξ that beat 7's covering argument has just made structurally. Cutting it
removes ~12 s and one whole mini-demonstration.

Restoring the cloud requires it to travel back from the left panel; it is
frozen, so this is a plain `.animate.scale().shift()`, and the
`shadow_dot_groups` updaters must be re-frozen after the move exactly as the
current code does.

## 3. The mechanism that makes beats 4 and 6 exact

Both the construction (beat 4) and the deformation (beat 6) run one updater
off one tracker `mix ∈ [0,1]`:

- point *j* has a transfer time `τ_j` spread evenly over `[0, 1−w]` with a
  small window `w ≈ 0.05`, shuffled;
- at `mix = s`, points with `τ_j + w ≤ s` are exactly at their Gaussian
  positions, points with `τ_j > s` are exactly on the ring, and ≤5% are in
  flight;
- the displayed cloud is therefore a sample from the **mixture**
  `(1−s)·Ring + s·N(0, I)`.

Because the characteristic function is linear in the distribution, that
mixture's CF is *exactly*

```
(1−s)·J₀(√2‖ξ‖) + s·e^{−‖ξ‖²/2}
```

which is precisely the blend the existing `morph_rival_field` already
computes — but now it is the truth at every frame rather than an
interpolation that is only correct at the endpoints. Two consequences fall
out free:

- the mixture has mean 0 and covariance I for **every** s, so "the coarse
  statistics agree" is true throughout the deformation, not just at its ends;
- the current staggered slide (`point_delays`,
  `np.linspace(0.0, 0.18, ...)`) produces a shrinking annulus, which is
  *not* a mixture and whose CF is not the blend. Replacing it with the wave
  is both more honest and a better read: points visibly *leave the ring and
  arrive in the middle*, one group at a time.

Curves and fields in this scene remain **population** objects; points remain
a finite sample. That is the same contract the rest of the chapter runs on.
Do not switch the curves to empirical CFs — Monte-Carlo wiggle of ~0.07 at
n=220 would leave the two curves visibly not coinciding at the end,
destroying beat 6's payoff.

**Add to `facts.py`:** `mixture_keeps_moments_and_blends_cfs` — for several
s, the mixture's mean is 0, its covariance is I, and its CF equals the blend
to machine precision. That is the claim the entire comparison section rests
on, and nothing currently checks it.

## 4. Where the owner's instructions conflict, and the recommendation

**1. "Explain height→brightness at the tracer sweep" vs. "one continuous
proof".** Putting brightness at the beat-3 sweep forces the field to be built
there, which is what creates the duplicate construction. *Resolution:* split
the correspondence into two statements doing different jobs — beat 3
establishes *which point* `ξ = tu` is (parameter correspondence, tracers, no
value), beat 7 establishes *how its value is drawn* (the legend,
brightness). Neither repeats the other, and brightness acquires a reason.
A deliberate deviation from the literal instruction that serves its stated
purpose better.

**2. "Build the ring with the same grammar the Gaussian cloud was built
with".** The Gaussian cloud was never built from points — it was morphed
from C05's line. *Resolution:* read "same grammar" as "persisting dot
instances migrating continuously", and build Y from X's own points. Flagged
because it is a reinterpretation, not a literal execution.

**3. The proof step contains a logical gap.** "Deform the second
distribution until the slices agree everywhere; at that point φ_X = φ_Y ∀ξ
follows visually, and uniqueness finishes it." If Y is deformed until it *is*
X, uniqueness has nothing left to do — identity is already visible. The
animation cannot demonstrate "agreement forces identity"; it demonstrates it
along **one** one-parameter family. *Resolution:* narrate the deformation as
an attempt whose result is an *observation* ("the two curves only lie on top
of each other at the moment the two clouds do"), and let beat 8 do the
general work with an explicit conditional ("So **if** two clouds cast the
same shadow in every direction, then…"). This is exactly the chain the owner
themselves specified, and it keeps proof-strength honest per NARRATION_SPEC
§9/§25.

**4. Both clouds are isotropic, so one radial slice already determines the
whole field.** The u-sweep in beat 7 is therefore a *quantifier* step, not a
discovery step. *Resolution:* leave this unstated but make beat 7's opening
sentence carry the limitation explicitly ("That was one direction… the rest
of the plane is still blank") and keep the covering claim strictly
conditional. A spoken isotropy caveat costs ~5 s and invites the viewer to
wonder whether one direction sufficed — the opposite of C04's lesson.
*Rejected alternative:* replace the ring with a four-clump cloud (`Cov = I`,
CF `cos ξ₁ cos ξ₂`, genuinely direction-dependent slices). It would make the
sweep do discovery work, but it discards `RING_PROFILE` and the whole
radial-lookup field machinery, breaks `data.ring_2d`'s documented role as
the project's same-moments counterexample, and turns the counterexample into
a set of atoms.

**5. Scope of the slogan cut.** "every direction has had its turn" is listed
as post-Cramér–Wold slogan but also occurs in the **opening** beat. Remove
both — same construction, same objection.

**6. "No persistent scene titles" vs. the Cramér–Wold label.** The label is
an in-place label on a visible equation and exits with it in beat 9.
Compliant as designed; do not promote it to a top-of-frame title.

**7. `converse_axes` y-range.** Reusing one axes object across beats 3–7 —
which is what gives the scene its continuity — requires
`y_range=(-0.55, 1.15)` from the start so `J₀` fits later. This slightly
changes the beat-3 framing versus `(-0.1, 1.15)`. Accept it; the alternative
is two axes objects and a cut.

## 5. Runtime budget

Baseline: ~604 spoken words in 182 s ⇒ ~3.3 words/s including `inspect`
holds.

| Beat | Words | Seconds | vs. today |
|---|---|---|---|
| 1 Turn u | 44 | 13 | −2 |
| 2 The target | 68 | 21 | −8 (finite-batch line cut) |
| 3 Slice derivation + t-sweep | 105 | 32 | −38 (example points cut, sweep moved out) |
| 4 Second cloud + moments | 58 | 18 | new |
| 5 Two shadows, two curves | 75 | 23 | new |
| 6 Deform until they agree | 52 | 16 | −6 |
| 7 Every direction → the field | 87 | 27 | +27 (re-homed) |
| 8 Uniqueness → Cramér–Wold | 74 | 22 | −16 |
| 9 Specialise + close | 81 | 25 | −22 (`pick` cut) |
| **Total** | **644** | **≈197** | +15 s over 182 |

Plus ~4 s of new `inspect` holds around the beat-4 construction ⇒ **≈201 s**.
If it overruns in the draft pass, trim in this order: beat 5's "which is
exactly where Chapter B started" (−3 s), beat 9's second payoff sentence
(−4 s), beat 1's closing question (−4 s, but this one is doing structural
work — cut last).

**Voice flags.** "Gaussian" occurs **6** times in the revised script against
5 today — net +1. "covariance" occurs **1** time against 1 today — net 0.
Both words are currently mispronounced by the ElevenLabs voice; a
pronunciation fix is being pursued separately and does not gate this work.

## 6. Implementation sequence

Each step should render green at `-ql` before the next. Steps 1–3 are
independent of the big restructure and de-risk it.

1. **Data & facts.** Whiten `_standardized_isotropic_points`; whiten the
   ring sample; re-run the seed-76 projection check; add
   `mixture_keeps_moments_and_blends_cfs` to `facts.py`. No animation change.
2. **Beats 1–2 text-only.** Delete the finite-batch clause and the `reason`
   bookmark; re-target the flick loop at `turn`; delete "every direction has
   had its turn" from beat 1. Verify the variance readout reads a flat 1.00.
3. **Beat 3.** New narration; keep one `shadow_plot`; widen `converse_axes`
   y-range; strip brightness from `update_freq_tracer`; move `freq_tag` +
   ξ₁/ξ₂ here and swap the sample-space plane for a frequency-space frame;
   delete the `EXAMPLE_TS` block. Lift `ray`/`trail_rays`/field construction
   out of this beat and park the code.
4. **Beat 7.** Re-home the parked sweep machinery: legend row, ray reveal,
   `angle → +TAU` trail, field fade-in. At this point the scene should run
   end-to-end with beats 4–6 absent — beat 3 → 7 → 8 → 9. Verify the whole
   spine reads before adding the comparison.
5. **Beat 4.** Three-column layout, mixture wave updater, moment blocks in
   C02's grammar, X/Y labels. Delete `rival_field`, `morph_rival_field`,
   `move_rival_points`, `same_distribution_caption`.
6. **Beat 5.** Two live shadow dot-plots; the `RIVAL` `J₀` curve on the
   shared axes.
7. **Beat 6.** Drive the wave, the shadows and the rival curve off the one
   `mix` tracker.
8. **Beats 8–9.** Restage `cw_label` (centred, `name` at its own sentence);
   delete the `pick` block; verify the closing restore of the wheel/shadow
   plots after the cloud's return trip, re-freezing `shadow_dot_groups`.
9. **Full `-qh` pass with `SIGREG_VOICE=eleven`**, then review the frame
   sequence for beat 4→5 and beat 6→7 (the two densest transitions) rather
   than stills.
