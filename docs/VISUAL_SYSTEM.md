# Visual system

Typography, colour, and layout for every explainer in this repo. Referenced by
[`EXPLAINER_PROCESS.md`](EXPLAINER_PROCESS.md) §8b and enforced when
[`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) §8.3 asks whether a scene
matches the project's established visual language.

Implemented in `projects/<name>/common/type.py` and `common/palette.py`. Scenes
import from there. **A scene that names a font, a colour, or a font size
directly is a defect**, the same way a hard-coded position is.

---

## 1. The rule that caused the rewrite

ManimGL's shipped default is `text.font: Consolas`. Consolas is a Windows
*monospace coding* font and is not present on macOS, so every `Text` in this
repo fell back to whatever Pango picked. That is the entire explanation for
"the text looks ugly and out of place": nothing was choosing the typeface.

```
$ python -c "from manimlib.config import manim_config; print(manim_config.text)"
{'font': 'Consolas', 'alignment': 'LEFT', 'font_size_for_unit_height': 144}

$ python -c "import manimpango; print('Consolas' in manimpango.list_fonts())"
False
```

**Never let a font default.** Under ManimGL, `custom_config.yml` set `text.font`
explicitly as a global backstop, and `common/type.py` set it again per-mobject
so a missing `custom_config.yml` could not silently change the look of a
render.

### Manim Community has no equivalent backstop

The project moved from ManimGL to Manim Community Edition; see the migration
handoff for the full port. The backstop described above is now the *only*
mechanism, not a belt-and-suspenders one: **CE has no global font setting at
all.** There is no `font` key in CE's `default.cfg` and no `config.font`
attribute — `manim.cfg` cannot set it the way `custom_config.yml` did. A
`manim.Text(...)` constructed without `font=` does exactly what a ManimGL
`Text` with a missing `custom_config.yml` did: it falls back to whatever Pango
picks, silently, with no error. This is the same defect that cost a whole
chapter's re-render once already, in a new engine.

The fix lives in `common/type.py`: the `Text` class defined there is a subclass
of `manim.Text` that defaults `font=FONT`, so every call site that imports
*this* `Text` — whether through `words()`/`title()`/`caption()`/etc., or by
constructing it directly — gets the right face even if it forgets to ask.
Scene files must import `Text` from `common.type`, not from `manim`; a bare
`from manim import *` shadowed by `from common.type import Text` afterward is
the pattern every current scene file uses. `tools/font_check.py` still catches
a missing install; nothing catches a scene that imports the wrong `Text`
except code review, so watch for it.

Manim Community's `Text` also renders **1.3623× larger than ManimGL's** at the
same `font_size` — a separate, unrelated defect from the missing font. See §3.

---

## 2. One typeface, two renderers

| Renderer | Face | Used for |
|---|---|---|
| `MathTex` | **Computer Modern**, via the default LaTeX template | mathematical expressions: $\varphi(t)$, $e^{itX}$, numerals inside a formula, axis tick numbers |
| `Text` | **Latin Modern Roman**, the OpenType successor to Computer Modern | every word of English: titles, panel captions, legends, annotations, units |

(Under ManimGL this table read `Tex` / `Text`. Manim Community splits ManimGL's
single `Tex` in two: CE's own `Tex` compiles in LaTeX *text* mode — it is the
old `TexText` — and `MathTex` is the one that compiles in math mode. Everything
this project calls mathematics is set in math mode, so every site that used to
say `Tex` now says `MathTex`; CE's `Tex` should not appear in a scene file.
`common/type.py`'s `maths()` is the one place that constructs it, exactly as
`words()` is the one place that constructs `Text`.)

The two faces are the same design. Latin Modern was commissioned specifically to
give Computer Modern a Unicode/OpenType form, and it is what a modern TeX
installation actually ships. So a caption and an equation in the same frame read
as one document instead of two design systems, and the `MathTex`/`Text`
boundary stops being a visual seam.

`MathTex` still owns mathematics and `Text` still owns English. That rule
survives the change — it is about *which renderer produces correct spacing and
italics*, not about which face. `MathTex(r"\text{mean} = +0.00")` is still
wrong, because LaTeX's `\text{}` sets an upright roman word inside a maths box
with maths spacing around it. (§3 below covers a further way `MathTex` and
`Text` diverge under CE that has nothing to do with LaTeX: their `font_size`
scales are not calibrated the same way.)

**Labelled numbers** — "mean = 0.00", "t = 1.35" — remain the one mixed case, and
still get a helper rather than a judgement call: `type.readout(label, tracker)`
baseline-aligns the word against the number. The faces now match, but the
baselines still do not: a `Text` x-height and a `DecimalNumber` digit sit at
different heights, and `VGroup.arrange()` centres rather than aligning.

### Why this replaced Helvetica Neue

Helvetica was chosen for defensible reasons, recorded here because they are the
reasons to check if the face is ever revisited: it was actually installed, a
neutral grotesque recedes behind the mathematics
([`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) §8.2), its even stroke weight
survives compression where Charter and Palatino do not, and it does not compete
with Computer Modern the way a geometric sans does.

The counter-argument that won: two faces meant every frame carried a seam
between the prose and the mathematics, and the project's reference look sets both
in the same family. The compression concern was real and is why the type scale in
§3 moved up rather than carrying over unchanged.

### Weight is not available in this face

Hierarchy runs on **size and colour only**. Not by preference — every heavier
Latin Modern face is broken in this pipeline:

| Face | Result |
|---|---|
| Latin Modern Roman (regular) | clean |
| Latin Modern Roman Demi | `2` returns a path **6.2× wide, 4.1× tall** |
| Latin Modern Roman, `weight=BOLD` | `b` returns a corrupt path |
| Latin Modern Roman, `weight=MEDIUM` | no-op — measured ink identical to `NORMAL` |

manimpango raises nothing for any of these. The corrupt glyph draws a stray
diagonal stroke across the frame, and its inflated bounding box then propagates
through `VGroup.arrange()` and `set_height()`, crushing every other row in the
group. One bad character, two failure modes, no traceback — the whole first
restyled frame rendered with a line through it and its layout collapsed.

`type.words()` still accepts `weight=MEDIUM` and deliberately ignores it, because
~30 call sites use it to mark which line is the active one. That distinction is
real; it is now carried by the size and colour chosen alongside it.

**`tools/font_check.py` is the regression check.** Run it whenever the typeface
changes. Nothing else in this repo can see this class of defect: `preflight.py`
checks names, `facts.py` checks numbers, `narration_audit.py` checks language.
None of them check whether the letters draw.

---

## 3. Type scale

ManimGL font size converts as **px at 1080p = font_size × 0.9375**
(`font_size_for_unit_height = 144`, frame height 8 units = 1080 px). That
conversion is ManimGL's; it does not carry over to Manim Community, and the
table below is unaffected only because `common/type.py` compensates for the
difference before it reaches CE — see the note immediately below the table.

### CE's `Text` does not mean the same `font_size` ManimGL's did

Measured directly, same face and string, `font_size` held fixed: CE's `Text`
renders **1.3623× larger** than ManimGL's at every size tested (24/36/48 gave
ratios 1.3632/1.3616/1.3623; four different strings at 32 gave
1.36235/1.36175/1.36263/1.36263). Stable to ~4 significant figures, so this is
a calibration constant, not per-string noise: ManimGL calibrates on
`font_size_for_unit_height = 144`, CE on `SCALE_FACTOR_PER_FONT_POINT = 1/960`,
and the two constants were never meant to produce the same output.

**`MathTex` is nearly unaffected** — measured at 1.031× against ManimGL's
`Tex`, and `DecimalNumber` at 1.018×, both imperceptible. So this is not simply
"CE text renders bigger"; it specifically changes the *ratio* between prose and
mathematics in the same frame, which is what §2 is about. Left uncorrected, a
caption and an equation sitting together stop reading as one document.

The fix is in `common/type.py`: its `Text` class divides every `font_size` by
the measured `1.3623` constant before handing it to `manim.Text`, so the tier
numbers in the table below still mean what they meant when they were set by
rendering `_fonttest.py` under ManimGL and reading the frame. `MathTex` and
`DecimalNumber` are left alone — correcting an already-imperceptible 1.03×
would be the fudge, not the fix. If the typeface or the scale is ever revisited,
re-run the measurement in `_fonttest.py` rather than trusting `1.3623` to still
be current; it is a property of the specific CE version and font, not a law.

| Role | `font_size` | px @1080p | Was | Notes |
|---|---|---|---|---|
| Scene title card | 46 | 43 | 46 | transient only |
| Statement on screen | 36 | 34 | 32 | the one sentence a beat is about |
| Body annotation | 31 | 29 | 28 | a full sentence on screen |
| Panel caption | 28 | 26 | 26 | pinned above a panel |
| Legend, annotation | 26 | 24 | 24 | |
| Axis tick label | 24 | 22.5 | 22 | **floor** |
| Readout (`t = 1.35`) | 32 | 30 | 30 | |

**Every prose tier moved up when the face changed.** Latin Modern's x-height is
roughly 0.43 em against Helvetica Neue's 0.52, so the old numbers rendered about
a sixth smaller than they measured. At 480p the small end stopped surviving:
`TICK` 22 and `CAPTION` 26 were both marginal in the draft. These values were set
by rendering `projects/sigreg_explainer/_fonttest.py` and reading it at 480p and
1080p — not by arithmetic.

Display mathematics keeps its own tier, but for a different reason than before.
The old justification was compensation: Computer Modern at 32 did not read as the
same size as Helvetica at 32. That is now moot, since both channels are the same
face. What survives is that an equation the viewer has to *read* is a different
job from a caption, so `EQ` sits level with `BODY` and the two larger steps exist
for emphasis:

| Role | `font_size` | px @1080p | Was |
|---|---|---|---|
| Equation in the flow of a scene | `EQ` 31 | 29 | 34 |
| The one equation a beat is about | `EQ_DISPLAY` 48 | 45 | 48 |
| A result held alone on screen | `EQ_HERO` 64 | 60 | 64 |

**24 is the hard floor, for both tiers** (raised from 22 with the face change).
Anything smaller is unreadable on a phone after compression and fails
[`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) §5.7. `type.py` raises
`ValueError` rather than rendering it, because an unreadable label is a silent
failure: it renders without complaint and is only caught in review, after a
full-resolution render has been spent on it.

The deleted `chain_bar` was `font_size=16` (15 px) and then `set_width`-shrunk
below even that. It was illegible, permanently on screen, and carried no
information the scene needed — three separate §7.3/§8.2 failures in one
seven-word strip. Removed rather than enlarged.

---

## 4. Colour

Roles, not names. `common/palette.py` is the only place these hex values exist.

| Role | Hex | Meaning |
|---|---|---|
| `BG` | `#0C0E12` | background |
| `INK` | `#EDF0F4` | primary text |
| `MUTED` | `#8A93A0` | captions, de-emphasised context |
| `AXIS` | `#5A6472` | axis lines, ticks, tick labels |
| `GRID` | `#2A303A` | grid, panel furniture |
| `CLOUD` | `#4FA8E8` | the data: samples, the batch, its arrows, its fingerprint, real parts |
| `TARGET` | `#F0B429` | the Gaussian reference and its fingerprint |
| `COLLAPSE` | `#E8615A` | the gap, the error, imaginary parts, the failure case |
| `DIRECTION` | `#5FCF80` | directions, projections, shadows |
| `ACCENT` | `#EDF0F4` | the single "look here now" highlight, via weight and scale |

Three changes from the old palette, each with a reason:

**Background `#000000` → `#0C0E12`.** Pure black crushes: `GREY_D` furniture at
`#444444` disappeared entirely at 480p, and the panel axes in `b02` read as
absent rather than as quiet. A near-black with a slight cool cast keeps blacks
rich on an OLED phone while leaving room for furniture to sit *below* the data
without vanishing.

**Target `#FFFF00` → `#F0B429`.** Pure yellow is the brightest colour a display
can make; against near-black it vibrates, and thin yellow strokes smear under
chroma subsampling — which is why the `|φ(t)|` curve rendered olive and muddy
at `00:05:00` while its own label rendered bright. Amber holds its hue at 2 px
stroke, still reads as "reference", and stops competing with the white text for
the brightest thing in frame.

**`CLOUD` and `EMPIRICAL` merged.** `BLUE_C #58C4DD` and `BLUE_B #9CDCEB` were
two blues, one step apart, carrying two different meanings (the batch, and the
empirical fingerprint of the batch). At delivery size they were the same
colour. They *are* the same idea — the fingerprint belongs to the batch — so
they are now one role.

**Colour is never the sole carrier of meaning**
([`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) §12). The real and imaginary
curves are blue and red *and* labelled *real* and *imaginary* on the curve
itself, not only in a corner legend.

---

## 5. Layout

- **Safe margins.** Nothing within 0.45 units of any frame edge. The `t` axis
  label in `b02` was clipping the right edge; `layout.fit_in_frame` existed but
  was not applied to axis labels.
- **Vertical thirds.** A three-panel rig fills the middle band; the top band
  carries the title *or* the readout, never both plus a caption row.
- **One dominant focal event per beat**
  ([`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) §5.2).
- **Empty space is not a defect** (§8.2). Large empty regions are only a
  problem when they unbalance the frame — the old `b01` frames put the whole
  argument in the left half and left the right half black, which is imbalance,
  not restraint.
- **Arrows have arrowheads.** Six `Line`s through a circle's centre read as
  three diameters, not as six vectors that could cancel. Anything the narration
  calls an arrow is drawn with a tip.

---

## 6. Motion

- Default transition 0.6 s; a transformation the viewer must follow, 1.2 s.
- No bounce, elastic, or overshoot easing.
- No camera move without a reason stated in the scene plan.
- Emphasis is a change of weight, scale, or opacity — not a flash or a glow.
- A parameter sweep runs at a speed at which the viewer can read the readout;
  if the number is a blur, the sweep is decorative.
