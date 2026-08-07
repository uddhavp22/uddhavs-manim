# uddhavs-manim — working reference

Reference notes for building explainer videos in this repo. Written primarily
for Claude to read at the start of a video-building task, but it doubles as the
human-facing setup record.

This repo builds on **Manim Community Edition** (CE), consumed as an editable
dependency from a sibling clone at `../manim-ce`. It is the successor to an
earlier version of this project built on **ManimGL** (3b1b/manim); the two
engines share a name and a design lineage but diverge in API in ways that will
silently misbehave rather than raise. See
[ManimGL → Manim Community, if you're translating old code](#3-manimgl--manim-community-if-youre-translating-old-code).

**This file covers mechanics only.** What to build and how it is judged:

| | |
|---|---|
| [`EXPLAINER_PROCESS.md`](EXPLAINER_PROCESS.md) | the process, its ten deliverables, and precedence |
| [`NARRATION_SPEC.md`](NARRATION_SPEC.md) | **binding** — how the script is written and audited |
| [`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) | **binding** — how a finished MP4 is reviewed |
| [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) | typography, colour, layout, motion |

---

## 1. Environment

| Piece | Where / version | Notes |
|---|---|---|
| Python | `.venv/` — 3.12 | `uv venv --python 3.12 .venv` |
| Manim CE | `../manim-ce`, editable install (`v0.20.1`) | `uv pip install -e ../manim-ce` — engine edits, if ever needed, take effect immediately |
| ffmpeg | Homebrew | |
| LaTeX | TinyTeX → `~/Library/TinyTeX` | Installed without sudo |
| stable-ts | `>=2.19` (imports as `stable_whisper`, **not** `stable_whisper` the PyPI name — the distribution is `stable-ts`) | Whisper word timings for bookmarks, §8 |

**numpy is pinned `<2.5`.** `stable-ts` → `openai-whisper` → `numba`, and no
`numba` release supports numpy 2.5 yet; the resolver's only escape route is
`numba==0.53.1`, which requires Python `<3.10` and fails to build here. Lifting
the pin without checking numba's compatibility first produces a long, confusing
build failure rather than an obvious one. Both pins are recorded with this
reasoning in `pyproject.toml`.

`openai` is deliberately **not** a dependency — the ElevenLabs and OpenAI
voiceover services call their REST endpoints through stdlib `urllib`, not an
SDK.

**PATH:** TinyTeX is not on `PATH` for non-login shells, so `render.sh` and
`build.sh` export it explicitly:

```sh
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
```

If LaTeX fails with "command not found", that export is the first thing to
check.

### TeX packages installed

The default TeX template pulls in a long preamble. These were installed on top
of the TinyTeX base:

```
dvisvgm standalone preview babel-english amsmath amsfonts doublestroke
setspace tipa relsize jknapltx fundus-calligra calligra-type1 wasysym wasy
wasy-type1 ragged2e everysel physics xcolor microtype psnfss fontaxes
cm-super type1cm rsfs
```

If a new scene fails with `LaTeX Error: File 'foo.sty' not found` or
`Metric (TFM) file not found`:

```sh
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
tlmgr search --global --file "/foo.sty"   # find the owning package
tlmgr install <package>
```

The package name usually differs from the `.sty` name — `ragged2e.sty` lives in
`ragged2e`, `calligra.sty` in `fundus-calligra`, `mathrsfs.sty` in `jknapltx`.
Always search rather than guessing.

### Recreating from scratch

```sh
brew install pkg-config cairo pango       # pycairo build deps
uv venv --python 3.12 .venv
uv pip install -e ../manim-ce
uv pip install -e .                       # this repo's own deps, see pyproject.toml
sh <(curl -fsSL https://yihui.org/tinytex/install-bin-unix.sh)
tlmgr install <the list above>
cp ~/Library/TinyTeX/texmf-dist/fonts/opentype/public/lm/lmroman10-regular.otf ~/Library/Fonts/
```

---

## 2. Layout and commands

```
projects/<topic>/scene.py             source for one video
projects/sigreg_explainer/common/     reusable primitives: palette, layout, type, rig, wrap, beat, data, anim
media/videos/<module>/<quality>/      renders (gitignored)
media/voiceovers/                     generated narration + cache.json (gitignored)
media/masters/<project>/              build.sh's concatenated chapter output (gitignored)
voiceover/                            narration package — see §8
manim.cfg                             tracked config (background, resolution, media/asset dirs)
render.sh                             wrapper: venv + TeX PATH + PYTHONPATH + `manim render`
build.sh                              renders a chapter and concatenates it — see §6
MANIM_GUIDE.md                        this file
```

`render.sh` passes everything through to `manim render`:

```sh
./render.sh projects/demo/scene.py DemoExplainer -ql   # draft mp4, 480p15 — use while iterating
./render.sh projects/demo/scene.py DemoExplainer       # final mp4, 1080p60 (manim.cfg's default)
./render.sh projects/demo/scene.py DemoExplainer -p    # ...and open it when done
./render.sh projects/demo/scene.py DemoExplainer -s    # last frame → png
./render.sh projects/demo/scene.py DemoExplainer -t    # transparent background (webm/mov)
./render.sh projects/demo/scene.py -a                  # every scene in the file
./render.sh projects/demo/scene.py Demo -n 3            # skip to animation #3
```

Useful flags: `-ql` 480p15 · `-qm` 720p30 · `-qh` 1080p60 · `-qp` 1440p60 ·
`-qk` 2160p60 · `-i`/`--format gif` · `-p` open when done · `--fps N` ·
`-n START,END` · `--renderer opengl` for the interactive/live-embed renderer.

**Always iterate with `-ql`.** It is several times faster and reveals every
layout and timing problem. It is also **15 fps, not 30** — CE couples frame
rate to the quality tier — so draft timing reads correctly but motion
smoothness must be judged at `-qh` or above.

**Writing is the default; there is no `-w`.** This is the single biggest
day-to-day difference from ManimGL. `manim render file.py Scene` writes an mp4
immediately; nothing opens a blocking preview window unless `-p` (cairo) or
`--renderer opengl` (interactive) is passed. `-s` alone is enough for a still
frame — no second flag needed the way ManimGL required `-s -w` together.

### `manim.cfg`

Tracked (unlike ManimGL's gitignored `custom_config.yml`), at the repo root.
Sets: `background_color = #0C0E12` (upstream default is black), `pixel_width`/
`pixel_height`/`frame_rate` for the `-qh` tier (1920×1080@60), `media_dir =
./media`, `assets_dir = ./sounds` (so `add_background_music("music/bed.mp3")`
resolves), `write_to_movie = True`, `verbosity = WARNING`,
`notify_outdated_version = False`.

manim reads this from the **current working directory**, which is why
`render.sh` and `build.sh` always `cd` to the repo root first before invoking
the CLI — running from elsewhere silently loses the whole file: wrong
background, wrong resolution, output scattered into a stray `media/` folder
relative to wherever it ran.

**CE has no global font setting**, unlike ManimGL's `custom_config.yml` →
`text.font`. There is no `font` key anywhere `manim.cfg` could set it, and no
`config.font` attribute. `common/type.py`'s `Text` class is the actual backstop
now — see [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) §1.

---

## 3. ManimGL → Manim Community, if you're translating old code

Most manim material online, and everything under `manim-up/` (the old ManimGL
version of this project, kept as a read-only reference for diffing), is written
against one engine or the other. **When unsure, grep `manim-ce/manim/` rather
than recalling from general manim knowledge** — CE's own source is the ground
truth for this repo, not memory of either API.

| Manim Community (here) | ManimGL |
|---|---|
| `Create(mob)` | `ShowCreation(mob)` |
| `axes.plot(f)` | `axes.get_graph(f)` |
| `MathTex(...)` (math mode) | `Tex(...)` |
| `Tex(...)` (**text** mode — do not use for maths) | `TexText(...)` |
| `axes.add_coordinates()` | `axes.add_coordinate_labels()` |
| `Axes(x_length=, y_length=)` | `Axes(width=, height=)` |
| `NumberLine(length=)` | `NumberLine(width=)` |
| `Arrow(stroke_width=, tip_length=)` | `Arrow(thickness=, tip_width_ratio=)` |
| `mob.width` / `mob.height` (properties) | `mob.get_width()` / `mob.get_height()` |
| `mob.scale_to_fit_width(v)` | `mob.set_width(v)` |
| `mob.stretch_to_fit_height(v)` | `mob.set_height(v, stretch=True)` |
| `mob.clear_updaters(recursive=True)` | `mob.clear_updaters(recurse=True)` |
| `MathTex(..., tex_to_color_map={})` | `Tex(..., t2c={})` |
| `MathTex(..., substrings_to_isolate=[...])` + `set_color_by_tex` | `tex["\\substring"]` string indexing |
| `TransformMatchingTex` | `TransformMatchingStrings` |
| `self.set_camera_orientation(phi=, theta=)` (degrees via `DEGREES`) | `self.frame.reorient(theta, phi, gamma)` |
| `self.begin_ambient_camera_rotation(rate=)` | `self.frame.add_ambient_rotation(rate)` |
| no equivalent — `VGroup` of `Dot` + `add_fixed_orientation_mobjects` | `DotCloud` |
| `scene.add_fixed_in_frame_mobjects(mob)` | `mob.fix_in_frame()` |
| `scene.renderer.skip_animations` | `scene.skip_animations` |
| `scene.renderer.file_writer` | `scene.file_writer` |
| `config.frame_rate` | `self.camera.fps` |
| `manim.logger` | `manimlib.logger.log` |
| `config.frame_width` (14.222, same value) | `FRAME_WIDTH` |
| `DEGREES` | `DEG` |
| `manim render file.py Scene -qh` (writing is default) | `manimgl file.py Scene -w` |
| `-ql` (854×480 **@15fps**, note the fps drop from ManimGL's -l) | `-l` (480p@30) |

Other divergences worth knowing:

- `config` has no `font` attribute and CE's `default.cfg` has no `font` key —
  see §2's `manim.cfg` note and [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) §1.
- **CE's `Text` renders 1.3623× larger than ManimGL's `Text` at the same
  `font_size`.** `MathTex`/`DecimalNumber` are nearly unaffected (1.03×,
  1.02×). `common/type.py`'s `Text` class corrects for this — see
  [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) §3. This is the dangerous kind of
  divergence: a name that exists in both engines, behaves differently, and
  raises nothing. Assume there are more; prefer measuring over trusting a name.
- `LaggedStartMap` is a trap — see §5.
- `VGroup` for vector mobjects, `Group` for mixed/image/surface mobjects, same
  as ManimGL. Putting an `ImageMobject` in a `VGroup` still fails.
- Angles are radians in both engines; `DEGREES` (CE) / `DEG` (ManimGL) convert.

---

## 4. Patterns that carry most scenes

### Structure: one method per beat of the script

```python
class Topic(Scene):
    def construct(self):
        self.intro()
        self.main_idea()
        self.payoff()
```

A note like "redo the middle section" then touches exactly one method, and
`-n` can skip straight to it.

### The `.animate` builder

```python
self.play(mob.animate.shift(UP).set_color(RED), run_time=2)
```

Interpolates start → end state. It does **not** replay the method's internal
motion, so `mob.animate.rotate(PI)` takes the straight-line path through the
center. Use `Rotate(mob, PI)` when the path matters.

### ValueTracker + always_redraw

The standard way to drive continuous motion from one number:

```python
t = ValueTracker(0)
dot = always_redraw(lambda: Dot(axes.c2p(t.get_value(), f(t.get_value()))))
self.add(dot)
self.play(t.animate.set_value(3), run_time=4)
```

`always_redraw` re-runs the lambda every frame. Anything it returns must be
constructed fresh inside the lambda — this matters even more under CE than it
did under ManimGL, because CE's `add_fixed_in_frame_mobjects` and
`add_fixed_orientation_mobjects` register a mobject **by instance**, and
`always_redraw` hands back a new instance every frame, silently dropping the
registration (see the 3-D note below).

### Morphing equations

```python
a = MathTex(R"a^2 + b^2 = c^2", substrings_to_isolate=["a^2", "b^2", "c^2"])
b = MathTex(R"a^2 = c^2 - b^2", substrings_to_isolate=["a^2", "b^2", "c^2"])
self.play(TransformMatchingTex(a, b, run_time=1.5))
```

This is the single highest-value animation for math explainers — shared
symbols slide to their new positions instead of cross-fading.
`substrings_to_isolate` controls what counts as a matchable unit, and is also
required before `set_color_by_tex` can colour part of a formula — without it a
`MathTex` is one submobject, and `set_color_by_tex` recolours the whole thing
silently rather than raising.

### Graphs

```python
axes = Axes(x_range=(-1, 4, 1), y_range=(-1, 5, 1), x_length=9, y_length=5.5)
axes.add_coordinates(font_size=20)
graph = axes.plot(lambda x: 0.4 * x**2, x_range=(-0.8, 3.4)).set_color(BLUE)
```

`axes.c2p(x, y)` maps data coords → screen point; `axes.p2c` is the inverse.
**Never position things against a graph with raw screen coordinates** — always
go through `c2p`.

### 3D

```python
class Spatial(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        surface = Surface(lambda u, v: [u, v, u * v], u_range=(-2, 2), v_range=(-2, 2))
        self.set_camera_orientation(phi=70 * DEGREES, theta=-32 * DEGREES)
        self.begin_ambient_camera_rotation(rate=3 * DEGREES)
```

Two-D overlays in a `ThreeDScene` (captions, readouts) need
`self.add_fixed_in_frame_mobjects(mob)`, or they tumble with the camera.
Off-plane point clouds need `self.add_fixed_orientation_mobjects(mob)` so the
camera billboards them instead of rotating them edge-on.

**Both of those register by instance, not by reference to "whatever this
variable currently points to."** Wrapping a fixed mobject in `always_redraw`
means every frame's fresh instance is unregistered and silently falls back to
world-space behaviour. `chapterC/c02_covariance.py` hit exactly this —
`DotCloud` (ManimGL-only, no CE equivalent) had to become a `VGroup` of flat
`Dot`s registered once, and every `always_redraw` in that scene was converted
to a build-once-plus-updater for the same reason.

### Text and layout

```python
VGroup(a, b, c).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
mob.to_edge(UP)  .to_corner(UR)  .next_to(other, RIGHT, buff=0.3)  .move_to(ORIGIN)
```

Frame is 8 units tall and ~14.22 wide (`config.frame_height`,
`config.frame_width`), origin at center. `UP/DOWN/LEFT/RIGHT/IN/OUT`,
`UL/UR/DL/DR` are unit vectors.

### Audio

`self.add_sound("name.wav", time_offset=0, gain=None)` — files resolve against
`assets_dir` (`./sounds` here, set in `manim.cfg`). Absolute paths also work.

For narration, don't hand-sync against this — use the `voiceover` package
(§8), which fits `run_time` to the audio automatically.

---

## 5. Gotchas hit in practice

- **`LaggedStartMap` silently mis-binds compound mobjects.** CE's version
  builds each animation as `animation_class(*arg_creator(submob))`, and the
  default `arg_creator` is the identity — `Mobject.__iter__` yields the
  mobject itself *followed by its children*, so a two-part mobject like an
  `Arrow` (shaft + tip) unpacks into two positional arguments:
  `LaggedStartMap(GrowArrow, arrows)` calls `GrowArrow(arrow, tip)`, and the
  tip lands in `GrowArrow`'s second parameter, `point_color`. Nothing raises at
  construction — it raises in `begin()`, animations later, as `AttributeError:
  ArrowTriangleFilledTip object has no attribute 'hex'`, because the tip is
  being parsed as a colour. The same unpacking silently mis-binds
  `Indicate(mob, scale_factor, color)` and `Create(mob, lag_ratio,
  introducer)`; it happens to be harmless for `FadeIn(*mobjects)` only because
  that call is variadic, and even then it animates a `Text`'s individual
  glyphs rather than the `Text` as a whole. **Use `common/anim.py`'s
  `lagged_map(animation_class, group, **kwargs)` instead of `LaggedStartMap`
  directly** — it passes an explicit `arg_creator` that wraps each submobject
  in a 1-tuple, restoring "one animation per direct submobject" regardless of
  what that submobject is made of.
- **`Dot(color=X)` is silently ignored**, same as ManimGL. `Dot.__init__`
  declares `fill_color` explicitly, so a `color=` kwarg lands in `**kwargs` and
  loses to the default — the dot renders white with no error. Use
  `fill_color=` or `.set_fill(X, 1)`. Worth checking for any mobject whose
  `__init__` names `fill_color`/`stroke_color` explicitly rather than taking
  `color`.
- **CE's `Text` renders larger than the same `font_size` meant under ManimGL**
  — see §3 and [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) §3. Always import `Text`
  from `common.type`, never straight from `manim`, in a scene file.
- **`Tex` in a scene file is very likely a bug, not a choice.** CE's `Tex`
  compiles in LaTeX text mode; every mathematical expression in this project
  wants `MathTex`. `Tex(r'\varphi_0(t)=e^{-t^2/2}')` raises "Missing $
  inserted" immediately, so this one at least fails loudly.
- **`add_fixed_in_frame_mobjects` / `add_fixed_orientation_mobjects` register
  by instance** — see the 3-D note in §4. `always_redraw` breaks the
  registration silently.
- **Manim exits 1 on an exception inside `construct()`,** unlike ManimGL's exit
  0. `build.sh`'s freshness guard depends on this, and also does its own
  mtime-before/mtime-after check as a second line of defence, because a script
  crashing after partially writing output is still possible.
- **manim resolves `manim.cfg` and every output path against the current
  working directory.** Running it from anywhere but the repo root silently
  loses the config. Always go through `render.sh` / `build.sh`.
- **LaTeX results are cached on disk.** A fixed `.sty` install won't retry a
  previously failed string until the cache is cleared: `--flush_cache`, or
  delete the relevant files under `media/Tex`.
- **`\;` immediately before `\text{...}` fails** with the default template:
  `Argument of \text@ has an extra }`. The culprit is **`tipa`** in the default
  preamble, which redefines `\;` in text mode for IPA diacritics. Use `\quad`,
  `\ `, or `\,` instead. When a `MathTex` string fails mysteriously, bisect the
  *preamble*, not just the string.

---

## 6. Workflow for turning a script into a video

1. **Read the script and break it into beats** — one idea per beat, each
   becoming a method on the `Scene`.
2. **Decide what actually moves.** The animation should carry the explanation,
   not decorate it. If a beat is just narration, it probably wants one still
   frame held for its duration, not motion for motion's sake.
3. **Write `projects/<topic>/scene.py`.** Start from `projects/demo/scene.py`.
4. **Draft render at `-ql`**, then extract frames to actually look at the
   output:
   ```sh
   ffmpeg -ss 8 -i media/videos/<topic>/480p15/<Scene>.mp4 -frames:v 1 /tmp/f.png
   ```
   Rendering without errors is not the same as looking right — check the
   frames. Do not judge motion smoothness or colour from a `-ql` render — see
   §2.
5. **Iterate on timing.** `run_time` per `play`, `self.wait(n)` between beats.
   Default `run_time` is 1.0s, default `wait` is 1.0s — both are usually too
   fast for a viewer reading new notation.
6. **Final render at `-qh`** (1080p60, `manim.cfg`'s default — no flag needed)
   once settled.
7. **Once a scene renders clean, run `build.sh` for its chapter** to exercise
   the concatenation path, not just the individual scene.

### Timing rules of thumb

- New equation appearing: `Write`, `run_time=1.5–2`, then `wait(1.5)`.
- Algebra step (`TransformMatchingTex`): `run_time=1.5`, then `wait(1)`.
- Continuous sweep (ValueTracker): `run_time=4–6` — slower than feels right
  while writing it.
- Between beats: `wait(0.5)` after a `FadeOut` before the next thing starts.

### Rate functions

`smooth` (default), `linear`, `rush_into`, `rush_from`, `there_and_back`,
`there_and_back_with_pause`, `wiggle`, `double_smooth`, `slow_into`,
`exponential_decay`.

---

## 7. Colors

> For a *project*, do not pick from this palette directly — import a role from
> the project's `common/palette.py`. The rules and the reasoning are in
> [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) §4. What follows is what Manim
> Community offers underneath.

CE ships the same 3b1b-derived palette ManimGL did, each with `_A` (lightest)
→ `_E` (darkest) variants: `BLUE TEAL GREEN YELLOW GOLD RED MAROON PURPLE
GREY`, plus `WHITE BLACK ORANGE PINK LIGHT_PINK GREY_BROWN DARK_BROWN
LIGHT_BROWN PURE_RED PURE_GREEN PURE_BLUE`.

The bare names (`BLUE`) are the `_C` variants. On black, `_B`/`_C` read best;
`_D`/`_E` get muddy. Colours are `ManimColor` instances now (`manim.utils.
color.core`), not raw hex strings, but every named constant still parses
anywhere a colour is accepted.

---

## 8. Voiceover

`voiceover/` is a port of [manim-voiceover][mv] (originally Manim Community's
own narration plugin) onto this repo's `Scene`. Narration lives in the scene
next to the animation, and the audio drives the timing rather than the other
way around. (The port history runs backwards from what you'd expect: the
package was written for CE, ported onto ManimGL for the earlier version of
this project, and has now been ported back for this one — see §8's closing
note on `manim_voiceover` proper if starting a project from scratch.)

[mv]: https://github.com/ManimCommunity/manim-voiceover

```python
from manim import *
from voiceover import VoiceoverScene
from voiceover.services.say import SayService

class Demo(VoiceoverScene):
    def construct(self):
        self.set_speech_service(SayService(voice="Samantha"))

        graph = ...
        with self.voiceover(text="Here the curve bends away.") as tracker:
            self.play(Create(graph), run_time=tracker.duration)
```

`tracker.duration` is the length of the generated clip, so the animation is
stretched to cover the sentence exactly. On leaving the `with` block the scene
waits out any narration the animations did not fill — a beat can never run
ahead of its own audio.

Working example: `projects/voiceover_demo/scene.py`.

### Bookmarks

To hit a specific word rather than a whole sentence:

```python
with self.voiceover(
    text="First we <bookmark mark='spin'/>rotate, then we <bookmark mark='grow'/>scale."
):
    self.wait_until_bookmark("spin")
    self.play(Rotate(square, PI / 2))
    self.wait_until_bookmark("grow")
    self.play(square.animate.scale(1.6))
```

Pass `transcription_model="base"` to any service to get exact placement — it
runs Whisper over the generated audio and maps every word to its real
timestamp. Without it, bookmarks are interpolated linearly across the clip,
assuming speech advances through the text at a constant rate. `common/beat.py`
sets `transcription_model="base"` in the shared speech-service construction
every `sigreg_explainer` scene inherits, so this is on by default there;
dropping it is a legitimate way to iterate quickly on geometry before spending
time on exact word-level landing.

**How much that matters, measured on this machine** (`say`, Samantha at 170wpm,
drift between the linear estimate and Whisper's ground truth):

| Line | Bookmark | Drift |
|---|---|---|
| 2.9 s, one clause | early / late | 2 ms / 33 ms — 0–2 frames |
| 11.1 s, four clauses | early / late | 142 ms / 334 ms — 8–20 frames |

So linear is fine for a short sentence and visibly wrong for a long one, and
the error grows the further into the line the bookmark sits.

(Upstream `manim_voiceover` *requires* Whisper for bookmarks and raises
otherwise. This port falls back to linear timing instead, so bookmarks still
work without it.)

### Services

| Service | Import from `voiceover.services.` | Needs | Status |
|---|---|---|---|
| `SayService` | `say` | nothing — macOS built-in | verified |
| `ElevenLabsService` | `elevenlabs` | `ELEVEN_API_KEY` | verified |
| `GTTSService` | `gtts` | network | verified |
| `OpenAIService` | `openai` | `OPENAI_API_KEY` | untested |
| `RecorderService` | `recorder` | a microphone | untested |

### ElevenLabs specifics

Learned the hard way, all of it invisible from the status codes alone:

- **The API key is scoped.** A new key may carry none of the permissions you
  need. `voices_read` is required to look a voice up by name; `text_to_speech`
  to generate at all. Grant them at elevenlabs.io → Profile → API Keys. Passing
  `voice_id=` instead of `voice_name=` skips the lookup and needs no read
  scope.
- **Free tier cannot use Voice *Library* voices via the API** — it returns 402.
  The ~21 default voices (Alice, Daniel, George, Sarah, Brian…) do work on the
  free tier. "Rachel", the ID in most older tutorials, is now a library voice
  and will fail.
- **Stock voices are named `"Alice - Clear, Engaging Educator"`**, not
  `"Alice"`, so exact-matching a first name finds nothing. `_resolve_voice_id`
  matches on the part before the dash, case-insensitively, so
  `voice_name="Alice"` works.
- Free tier is 10k characters/month. A 10-minute video is roughly 9k, so one
  video per month before it bills. Audio is cached, so re-rendering is free —
  only *edited* lines re-spend.

Keys are read from the environment or a `.env` file at the repo root (which is
gitignored — see `.env.example` for the template).

```sh
echo 'ELEVEN_API_KEY=sk_...' >> .env
```

**Draft with `SayService`, then swap the one line.** Every service produces the
same cache format, so switching voice at the end changes nothing but timing.

`say` is fine for laying out timings but sounds robotic — its compact voices
are not usable in a finished video. Either download the Enhanced/Premium
variants (System Settings → Accessibility → Spoken Content → Manage Voices,
then `SayService(voice="Ava (Premium)")`), or move to ElevenLabs for the final
pass.

### Smoke-testing a service

```sh
PYTHONPATH=. .venv/bin/python -m voiceover.check say --voice Samantha
PYTHONPATH=. .venv/bin/python -m voiceover.check elevenlabs --voice-name Adam
PYTHONPATH=. .venv/bin/python -m voiceover.check say --transcribe base
```

Generates one clip, prints its duration and resolved bookmark times, and plays
it back — cheaper than rendering a scene to find out a key is wrong.

`RecorderService` records your own voice through ffmpeg's avfoundation input,
one block at a time, with playback and redo between takes.

### Caching

Audio is generated once and cached in `media/voiceovers/`, keyed on the text,
the service config, and `global_speed`. Editing a line regenerates only that
line. Bookmarks are stripped from the cache key, so moving a bookmark never
re-bills an API call or forces a re-record.

`global_speed=1.15` on any service re-times every clip through ffmpeg's
`atempo` without changing pitch — the cheapest fix for narration that drags.

### Subcaptions

CE writes subcaptions natively — `Scene.add_subcaption(text, duration, offset)`
is a first-class part of its file writer, and it serialises the `.srt` for
free. `add_wrapped_subcaption` (on `VoiceoverScene`) splits a sentence into
~70-character chunks and calls `add_subcaption` once per chunk, with offsets
accumulating from zero within the current voiceover (CE stamps
`self.time + offset` internally). `set_speech_service(..., create_subcaption=
False)` turns it off. There is no `voiceover/subcaption.py` any more — the
hand-rolled ManimGL-era SRT writer this used to be was deleted, since CE does
the job itself.

### Background music

```python
self.add_background_music("rubinetti/stepwise.mp3", gain=-22, duck=-8)
```

Lays a bed under the whole scene and **ducks it automatically while anyone is
speaking**. The scene already records every voiceover's start and end, so the
attenuation windows are exact — no sidechain compressor guessing where the
speech is, and no gain automation drawn by hand. Files resolve against
`assets_dir` (`./sounds`, set in `manim.cfg`) or from any absolute path.

| Arg | Default | What it does |
|---|---|---|
| `gain` | `-22` dB | Resting level. Music mastered for listening is *far* too loud as a bed. |
| `duck` | `-8` dB | Extra attenuation while narration plays. |
| `ramp_ms` | `400` | Glide in/out of a duck. Shorter pumps, longer collides with the sentence. |
| `fade_in` / `fade_out` | `1.5` / `3.0` s | At the ends of the bed. |
| `loop` | `True` | Repeat if the track is shorter than the scene. |
| `start` / `end` | whole scene | Restrict the bed to one stretch. |

Verified on a constant-level tone: resting `-37.1` dB, ducked `-45.1` dB,
against `-37.1` / `-45.1` predicted, with the ramp gliding
`-41.2 → -43.6 → -45.1` over the 400 ms before speech.

To let a moment breathe, just stop narrating — the bed un-ducks on its own:

```python
with self.music_break(4.0):
    self.play(Rotate(shape, TAU), run_time=4)
```

`music_break` is only sugar for "hold this long"; it waits out any remainder if
the animations inside come up short. The music swell is a consequence of there
being no voiceover, not of the helper.

Call `add_background_music` anywhere in `construct` — the mix is assembled in
`tear_down`, which CE calls before `renderer.scene_finished`, once the scene's
real length and every narration span are known.

### Choosing a track

Drop candidates in `sounds/music/` and hear each one the way it will actually
be heard — ducked under speech:

```sh
PYTHONPATH=. .venv/bin/python -m voiceover.audition music
PYTHONPATH=. .venv/bin/python -m voiceover.audition music --pause --gain -26
```

A track that sounds lovely alone often fights the voice; anything with melodic
movement in the vocal range does. Judging a bed in isolation is the mistake.

Note that `sounds/music/foo.mp3` must be referenced as `"music/foo.mp3"` —
names resolve relative to `assets_dir`, not by basename. The audition prints
the correct string for whichever track you pick.

### Where to get music

- **[Pixabay Music](https://pixabay.com)** — CC0-style, commercial OK, no
  attribution. Best free default.
- **YouTube Audio Library** — in YouTube Studio, guaranteed safe on YouTube.
- **[Musopen](https://musopen.org)** — public-domain *recordings* of PD
  classical (Satie, Chopin, Debussy). Their [FAQ](https://musopen.org/faq/)
  notes user uploads are unvetted, so confirm per track: a PD composition does
  not make an arbitrary recording PD.
- **Epidemic Sound / Artlist** — ~$15/mo, and the licence includes Content ID
  clearance, which is the real reason to pay.

Whatever the source, search the track title plus "Content ID" before
committing. False claims on CC0 and public-domain recordings are common.

### Gotchas

- **`render.sh` exports `PYTHONPATH=$REPO_ROOT`** so `from voiceover import
  ...` resolves. manim loads scene files through `spec_from_file_location`,
  which does not put the repo root on `sys.path`. Running `manim` directly
  without that export fails with `ModuleNotFoundError: voiceover`.
- **Iterate with `-ql`, but the audio is generated at full quality
  regardless.** The first render of a scene pays the TTS (and, with
  `transcription_model` set, Whisper) cost; later ones hit the cache in
  `media/voiceovers/`.
- **`-s` (still frame) skips every animation**, so no audio is produced.
- `scene.renderer.skip_animations` is the CE spelling of ManimGL's
  `scene.skip_animations`; `voiceover/scene.py` checks it directly rather than
  through a compatibility shim.

---

## 9. Relationship to `manim_voiceover` upstream

If starting a *new* project from scratch rather than continuing this one, the
straight-line choice is the real [`manim_voiceover`][mv] package from PyPI,
which this repo's `voiceover/` package was originally derived from before being
ported onto ManimGL and back. This repo's version diverges deliberately in a
few places worth knowing if diffing against upstream: it falls back to linear
bookmark timing instead of requiring Whisper, it adds background-music ducking
tied to recorded narration spans, and its caching keys are structured around
this project's own `common/beat.py` speech-service setup.
