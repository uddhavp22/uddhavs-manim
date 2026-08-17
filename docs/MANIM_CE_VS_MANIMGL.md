# ManimCE and ManimGL — implementation and porting guide

This is the working reference for reading ManimGL/3Blue1Brown code and
rebuilding it in this repository's Manim Community Edition (ManimCE) codebase.
It explains both the visible API differences and the engine-level differences
that make a blind search-and-replace unreliable.

For ordinary scene-building and render commands, use
[`MANIM_GUIDE.md`](MANIM_GUIDE.md). For project typography, colour, spacing,
and motion rules, use [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md).

## 1. Scope and local source of truth

This workspace contains three distinct layers:

| Layer | Local path | Role |
|---|---|---|
| ManimCE | `../manim-ce/` | The engine this project runs; installed as the editable `manim` dependency |
| ManimGL | `../manim-up/` | A local ManimGL 1.7.2-era engine reference |
| 3Blue1Brown video code | `../3blue1brown_videos/` | Scenes plus 3b1b's project helper layer |

The target is the editable ManimCE checkout declared in `pyproject.toml`,
currently based on ManimCE 0.20.1. APIs can move, so for a questionable detail
search the local source rather than relying on memory or a tutorial written for
another release:

```sh
rg -n "class SomeName|def some_name" ../manim-ce/manim
rg -n "class SomeName|def some_name" ../manim-up/manimlib
rg -n "class SomeName|def some_name" ../3blue1brown_videos
```

The short rule is:

> Treat ManimGL code as a description of the visual behavior, not as source
> that should continue to look the same after the port.

## 2. These are two engines, not two import names

ManimCE began from the same lineage as ManimGL, so both have `Scene`,
`Mobject`, `VGroup`, `self.play`, `.animate`, updaters, and familiar geometry.
They have since developed independently.

| Concern | ManimCE in this repo | ManimGL |
|---|---|---|
| Package/import | `manim`; `from manim import *` | `manimgl` package, imported as `manimlib` |
| Default renderer | Cairo | OpenGL |
| Other renderer | Optional OpenGL via `--renderer opengl` | No Cairo path |
| Configuration | `manim.cfg` plus the global `config` object | `custom_config.yml` plus `manim_config` |
| Normal scene output | Writes a movie by default | Opens an interactive window; `-w` writes |
| Camera model | Depends on scene and renderer | A shader-backed `CameraFrame` is part of every scene |
| Interactive workflow | CE has OpenGL interaction, but it is not API-compatible with 3b1b's workflow | `InteractiveScene`, `embed`, `checkpoint_paste`, live camera control |
| Vector paths | Cairo `VMobject` uses cubic Bézier storage; CE OpenGL uses a different OpenGL mobject implementation | Shader-oriented quadratic path data |
| 3D style | `ThreeDScene` APIs, with renderer-dependent implementation | OpenGL camera, lights, depth testing, and shader uniforms throughout |

### CE OpenGL is not “ManimGL compatibility mode”

`--renderer opengl` changes ManimCE's renderer, but it does not turn its API
into ManimGL's. ManimCE uses a `ConvertToOpenGL` metaclass to substitute
OpenGL base classes for many mobjects. Switching renderer can therefore change
the actual class implementation and available methods, not merely the final
drawing backend.

This project targets ManimCE's default Cairo renderer. Do not add
`--renderer opengl` just to make a copied ManimGL method exist. That creates a
renderer-specific scene and can change geometry, layering, text, and output.

## 3. First identify where a symbol came from

An import such as this is not “all of ManimGL”:

```python
from manim_imports_ext import *
from _2024.transformers.helpers import *
```

`manim_imports_ext.py` re-exports `manimlib`, old TeX classes, Pi creatures,
custom drawings, backdrops, logos, and other 3b1b utilities. The second import
adds helpers written for one video series. A missing name may therefore be:

1. Python, NumPy, or another dependency;
2. a ManimGL engine API;
3. a 3b1b-wide helper from `manim_imports_ext` or `custom/`;
4. a helper local to that video's folder; or
5. a method defined earlier in the same scene class.

Find the definition before choosing a replacement. The correct port of a
custom helper is usually a small CE-native implementation of its behavior,
not a similarly named CE class.

### Example: `_2024/transformers/network_flow.py`

The currently referenced file contains all four relevant categories:

| Name | Actual provenance | Porting consequence |
|---|---|---|
| `InteractiveScene`, `ShowCreation`, `self.frame` | ManimGL | Translate or redesign with CE scene/camera APIs |
| `set_floor_plane`, `deactivate_depth_test`, `set_shading` | ManimGL renderer behavior | Rebuild the 3D look; there is no safe name-only port to Cairo |
| `EmbeddingArray`, `NumericEmbedding` | `_2024/transformers/helpers.py` | Port only if the target scene truly needs this visual primitive |
| `break_into_tokens`, `get_piece_rectangles` | `_2024/transformers/embedding.py` | Reimplement as project helpers; they also bring tokenizer assumptions |
| `progress_through_attention_block` and related methods | The scene class itself | Preserve the narrative/visual behavior, then translate its internals |

Import replacement is therefore only the first few percent of this port.

## 4. Engine architecture that affects scene code

### 4.1 Scene lifecycle

Both engines build a scene around `construct()`. ManimCE's documented render
lifecycle is:

```text
setup() → construct() → tear_down()
```

Use `setup()` for initialization that must happen before every render. Avoid a
custom scene `__init__` unless there is a compelling engine-level reason.

ManimCE keeps output state under `scene.renderer`; for example, the file writer
is `scene.renderer.file_writer`. ManimGL commonly exposes equivalent state
directly as `scene.file_writer` and uses `scene.skip_animations` in places
where CE code may need `scene.renderer.skip_animations`.

### 4.2 Camera ownership

In ManimGL, every `Scene` creates a camera frame and exposes it as
`self.frame`. The frame is an animatable mobject with orientation, position,
and height:

```python
self.play(self.frame.animate.reorient(-30, 70, 0, center, height))
```

In ManimCE, choose the scene type that expresses the intended camera behavior:

- `Scene`: fixed 2D camera;
- `MovingCameraScene`: 2D camera with `self.camera.frame`;
- `ThreeDScene`: 3D orientation through `set_camera_orientation`,
  `move_camera`, and ambient-rotation methods.

Do not mechanically change `self.frame` to `self.camera.frame` inside a normal
CE `Scene`; the default Cairo camera does not provide the moving-frame contract.

### 4.3 Mobject data and vector paths

The public transformation methods look similar, but the internal data models
are not portable:

- ManimGL `Mobject` stores GPU-oriented structured arrays and shader uniforms.
- ManimCE's Cairo `Mobject`/`VMobject` stores CPU-side points and style arrays
  for Cairo rendering.
- ManimCE OpenGL uses separate `OpenGLMobject` and `OpenGLVMobject`
  implementations.
- Cairo paths use four points per cubic Bézier curve; the OpenGL
  implementations use different quadratic-oriented representations.

Code that calls public methods such as `set_points_as_corners`,
`add_points_as_corners`, `point_from_proportion`, `apply_function`, or
`set_stroke` is a reasonable port candidate. Code that slices `.points`, edits
`.data`, changes `.uniforms`, replaces shaders, or assumes a fixed number of
control points must be rewritten against a public ManimCE API.

### 4.4 Object identity and families

A mobject is a tree: the object itself plus its `submobjects`. Animations,
camera registration, draw ordering, and updater recursion often operate on the
whole family.

`always_redraw(factory)` in both local engines keeps the outer wrapper object
and updates it with `wrapper.become(factory())`. The newly built object's
children can replace the wrapper's prior children every frame. This matters
when an API registers individual family members by identity, as Cairo's
fixed-orientation/fixed-in-frame camera bookkeeping does.

Consequences:

- Do not put a changing `always_redraw` family through
  `add_fixed_in_frame_mobjects` and assume every future child is registered.
- For a fixed overlay, build it once and update values or positions on the same
  instances.
- Before fading an `always_redraw` object, clear or freeze its updater; otherwise
  its next rebuild can restore opacity while `FadeOut` is trying to change it.

The project helpers `ActScene.freeze`, `clear_beat`, and `clear_overlay` already
handle the last case.

### 4.5 Source-tree map

When behavior is ambiguous, these are the implementation entry points in the
two sibling engine checkouts:

| Concern | ManimCE | ManimGL |
|---|---|---|
| Scene lifecycle | `manim/scene/scene.py` | `manimlib/scene/scene.py` |
| Moving/interactive scene | `manim/scene/moving_camera_scene.py`, OpenGL interaction in `scene.py` | `manimlib/scene/interactive_scene.py`, `scene_embed.py` |
| 3D scene API | `manim/scene/three_d_scene.py` | `manimlib/scene/scene.py` (`ThreeDScene`) |
| Base mobject | `manim/mobject/mobject.py` | `manimlib/mobject/mobject.py` |
| Vector paths | `manim/mobject/types/vectorized_mobject.py` and `mobject/opengl/opengl_vectorized_mobject.py` | `manimlib/mobject/types/vectorized_mobject.py` |
| Animations | `manim/animation/` | `manimlib/animation/` |
| Camera/rendering | `manim/camera/`, `manim/renderer/` | `manimlib/camera/`, `renderer.py`, `shader_wrapper.py` |
| Text and TeX | `manim/mobject/text/` | `manimlib/mobject/svg/text_mobject.py`, `tex_mobject.py` |
| Coordinates | `manim/mobject/graphing/coordinate_systems.py` | `manimlib/mobject/coordinate_systems.py` |
| Configuration | `manim/_config/` | `manimlib/config.py`, `default_config.yml` |
| CLI/scene loading | `manim/cli/`, `manim/utils/module_ops.py` | `manimlib/__main__.py`, `extract_scene.py` |

## 5. API translation reference

This table is a starting point, not a promise of identical pixels.

| ManimGL source | ManimCE target | Notes |
|---|---|---|
| `from manimlib import *` | `from manim import *` | Then add explicit project/common imports |
| `from manim_imports_ext import *` | No single replacement | Inventory every custom name first |
| `InteractiveScene` | `Scene`, `MovingCameraScene`, or `ThreeDScene` | Choose by rendered behavior, not by name |
| `ShowCreation(mob)` | `Create(mob)` | Common direct rename |
| `ShowCreationThenDestruction(path)` | `ShowPassingFlash(path)` | Check timing and remover behavior |
| `VFadeIn`, `VFadeInThenOut` | No direct CE class | Use `FadeIn`/`FadeOut`, `Succession`, or a small purpose-built animation after checking updater/remover behavior |
| `axes.get_graph(f)` | `axes.plot(f)` | Translate range/config arguments too |
| `axes.add_coordinate_labels()` | `axes.add_coordinates()` | Label styling differs |
| `Axes(width=..., height=...)` | `Axes(x_length=..., y_length=...)` | Ranges still need review |
| `NumberLine(width=...)` | `NumberLine(length=...)` | Constructor rename |
| `Tex(r"x^2")` | `MathTex(r"x^2")` | ManimGL `Tex` is math-first; CE `Tex` is text mode |
| `TexText("words")` | `Tex("words")` or project `Text` | Prefer project `Text` for ordinary prose |
| `Tex(..., isolate=[...], t2c={...})` | `MathTex(..., substrings_to_isolate=[...], tex_to_color_map={...})` | Subobject splitting is not identical |
| `tex[r"\alpha"]` | `tex.get_part_by_tex(...)` after isolation | In this project, use `common.type.maths(..., isolate=...)` |
| `TransformMatchingStrings(a, b)` | `TransformMatchingTex(a, b)` | Verify how both equations are split |
| `mob.get_width()` / `get_height()` | `mob.width` / `mob.height` | CE compatibility methods may exist; properties are preferred here |
| `mob.set_width(v)` | `mob.scale_to_fit_width(v)` | Use `stretch_to_fit_width` only when distortion is intended |
| `mob.set_height(v, stretch=True)` | `mob.stretch_to_fit_height(v)` | Be explicit about distortion |
| `mob.set_max_width(v)` | Scale conditionally when `mob.width > v` | `scale_to_fit_width` always resizes, so preserve the “maximum” condition |
| `mob.get_shape()` | `(mob.width, mob.height)` | Add depth explicitly if the source used a 3D shape tuple |
| `FRAME_WIDTH`, `FRAME_HEIGHT` | `config.frame_width`, `config.frame_height` | CE frame dimensions are runtime config |
| `DEG` | `DEGREES` | Both multiply radians; use the local spelling |
| `FadeIn(mob, UP)` | `FadeIn(mob, shift=UP)` | CE treats positional mobjects variadically |
| `FadeOut(mob, DOWN)` | `FadeOut(mob, shift=DOWN)` | Make animation options keywords |
| `LaggedStartMap(AnimationClass, group)` | `common.anim.lagged_map(AnimationClass, group)` | CE's argument creation semantics differ; use the project wrapper |
| `mob.fix_in_frame()` | `scene.add_fixed_in_frame_mobjects(mob)` | Required for the default Cairo renderer |
| `self.frame.reorient(theta, phi, ...)` | `set_camera_orientation(phi=..., theta=...)` / `move_camera(...)` | CE uses explicit named angles; review angle order and units |
| `self.frame.add_ambient_rotation(rate)` | `begin_ambient_camera_rotation(rate=...)` | On a `ThreeDScene` |
| `DotCloud(...)` | Usually a `VGroup` of `Dot`s in this repo | CE exports an OpenGL `DotCloud`, but it is not a Cairo `VMobject` |
| `Cube(...).set_shape(w, h, d)` | `Prism(dimensions=[w, h, d], ...)` | Rebuild style rather than carrying shader kwargs |
| `mob.set_backstroke(color, width)` | `mob.set_background_stroke(color=color, width=width)` | Useful for readable text over geometry |
| `mob.clear_updaters(recurse=True)` | `mob.clear_updaters(recursive=True)` | Keyword differs |
| `manimgl file.py Scene -w` | `./render.sh file.py Scene -ql` | This repo always renders through its wrapper |

### Methods with the same name can still differ

The dangerous ports are calls that do not raise:

- Text at the same `font_size` is not physically the same size. This project
  measured CE `Text` at about 1.3623 times ManimGL's height and compensates in
  `projects/sigreg_explainer/common/type.py`.
- Constructor keywords may target different style channels. Inspect the local
  signature when color, opacity, tip size, or stroke width looks wrong.
- `.animate.rotate(PI)` interpolates the object's states; it does not guarantee
  the visible circular path that `Rotate(mob, PI)` expresses.
- Matching transforms depend on each engine's submobject splitting, especially
  for TeX.

## 6. Text and TeX require a semantic port

Use three separate ideas in ManimCE:

| Content | ManimCE class in this project |
|---|---|
| Ordinary English | `common.type.Text` or `common.type.words()` |
| Mathematical notation | `MathTex` or `common.type.maths()` |
| LaTeX text-mode content | `Tex` (rare in scene files here) |

ManimGL's `Tex` compiles math-oriented input, while its `TexText` removes the
math environment. ManimCE reverses the practical naming expectation:
`MathTex` is math mode and `Tex` is normal text mode. A blind `Tex` → `Tex`
port can therefore compile differently or fail.

ManimGL's labelled-SVG/string selector system also permits expressions such as
`tex["x"]`. In ManimCE, isolate the relevant substring at construction and
then use `get_part_by_tex` or `set_color_by_tex`. Always check the number and
shape of submobjects before a matching transform.

Project rule: scene files should use the helpers in `common/type.py` so font,
minimum size, math/prose separation, and CE size calibration stay consistent.

## 7. Animations and updaters

### What normally carries over

The following concepts are shared and are good anchors for a rewrite:

- `self.play(...)`, `self.wait(...)`, and rate functions;
- `.animate` for ordinary state interpolation;
- `ValueTracker` plus `always_redraw` or a stable-instance updater;
- `Transform`, `ReplacementTransform`, `MoveToTarget`, `Restore`;
- `AnimationGroup`, `LaggedStart`, and `Succession`;
- mobject updaters accepting `(mobject)` or `(mobject, dt)`.

### What needs deliberate translation

Animation constructors do not share one universal positional signature. One
common 3b1b idiom is:

```python
FadeIn(label, UP)
```

ManimGL reads `UP` as the shift vector. ManimCE's `FadeIn` accepts multiple
mobjects positionally, so the CE spelling is:

```python
FadeIn(label, shift=UP)
```

`LaggedStartMap` is another semantic difference. ManimGL calls the animation
factory once per direct child. The local ManimCE implementation expands the
result of `arg_creator(child)` into positional arguments; its identity default
can therefore unpack a compound child. Use `common.anim.lagged_map`, which
wraps each child in a one-item tuple.

### Stable instance versus rebuild-every-frame

Use `always_redraw` for simple 2D derived geometry where replacing the family
is harmless. Prefer building once and attaching an updater when:

- the object has fixed-frame or fixed-orientation camera registration;
- other code holds references to its children;
- recreating it is expensive (large text, surfaces, or point sets);
- its identity controls layering or later transforms.

## 8. Geometry, groups, and layout

`VGroup` is for vector mobjects. `Group` can hold mixed mobject types such as
images, surfaces, and vector objects. If CE says that a value cannot be added
to a `VGroup`, changing to `Group` may be correct; forcing a renderer-specific
object into `VGroup` is not.

The local ManimCE version accepts iterables in `VGroup`, including generators,
but explicit starred construction is clearer when porting:

```python
dots = VGroup(*(Dot(point) for point in points))
```

It makes “one generated object per child” visible and works across more Manim
versions.

Use coordinate-system methods for data geometry:

```python
axes = Axes(...)
curve = axes.plot(f, x_range=(low, high))
point = axes.c2p(x, f(x))
```

Do not place graph annotations with raw scene coordinates copied from the
source. Port the coordinate transform and then tune layout against this
project's configured frame.

For frame-aware positioning, use `config.frame_width` and
`config.frame_height`, then pass uncertain-width annotations through
`common.layout.fit_in_frame`.

## 9. 3D, lighting, depth, and shaders

This is where a behavioral rewrite is most often necessary.

ManimGL scene code can directly manipulate:

- the frame's Euler axes and orientation;
- a camera light source;
- depth testing on individual objects;
- shader shading, gloss, shadow, reflectiveness, and flat strokes;
- OpenGL point clouds and surfaces.

Some similarly named methods exist only on ManimCE's OpenGL classes. They are
not available on the default Cairo mobject implementation and should not be
used as a reason to switch the whole project renderer.

For a CE/Cairo rewrite:

1. Start with `ThreeDScene` and `set_camera_orientation`.
2. Rebuild solids using CE classes such as `Prism`, `Cube`, `Surface`, and
   `ThreeDAxes`.
3. Express the intended appearance with `fill_color`, `fill_opacity`,
   `stroke_width`, and `shade_in_3d` where supported.
4. Use `set_z_index` or addition order for 2D overlays; do not port depth-test
   toggles into unrelated 2D code.
5. Register captions with `add_fixed_in_frame_mobjects` and billboarded world
   labels with `add_fixed_orientation_mobjects`.
6. Replace high-performance ManimGL point clouds with a practical CE/Cairo
   representation, usually a stable `VGroup` of `Dot`s at the counts used in
   this explainer.

`set_floor_plane("xz")` is specifically a ManimGL camera-frame convention. In
CE, choose the axes, object coordinates, and camera orientation explicitly.

## 10. Configuration, commands, and assets

Do not port `custom_config.yml` keys into scene code. This project centralizes
the CE equivalents in `manim.cfg` and its wrappers.

| Task | ManimGL | This ManimCE project |
|---|---|---|
| Main config | `custom_config.yml` | `manim.cfg` |
| Render | `manimgl file.py Scene -w` | `./render.sh file.py Scene -ql` |
| Final quality | Camera/config flags | `./render.sh file.py Scene` (1080p60 project default) |
| Still | Commonly `-s` plus a write/open choice | `./render.sh file.py Scene -s` |
| Frame dimensions | `FRAME_WIDTH`, `FRAME_HEIGHT` | `config.frame_width`, `config.frame_height` |
| Assets | YAML directory tree | `assets_dir = ./sounds` plus explicit project paths |
| Global text font | `custom_config.yml` supports `text.font` | No CE `manim.cfg` font key; use `common/type.py` |

Always use `render.sh`. It selects the virtual environment, restores the TeX
path and `PYTHONPATH`, changes to the repository root so `manim.cfg` is found,
and keeps outputs under the intended `media/` tree.

## 11. Recommended refactoring workflow

### Step 1 — Record the behavior to preserve

Write down:

- what objects are visible;
- which data or equations determine them;
- what changes during each beat;
- the camera move and focal point;
- which visual details are essential versus merely 3b1b styling.

This becomes the port's contract. “The new source resembles the old source” is
not a useful contract.

### Step 2 — Perform a provenance pass

For every non-obvious class, function, method, and constructor keyword, locate
its definition. Separate engine APIs from 3b1b helpers and scene-local code.

Useful searches for a copied file:

```sh
rg -n "manim_imports_ext|from _[0-9]{4}|from custom" source.py
rg -n "class Name|def name" ../3blue1brown_videos ../manim-up/manimlib
rg -n "class Candidate|def candidate" ../manim-ce/manim
```

### Step 3 — Port math and data before mobjects

Extract pure Python/NumPy calculations from rendering code. Verify values and
array shapes independently. Avoid carrying video-specific dependencies such as
tokenizers or model libraries unless the target scene actually needs live
model data.

### Step 4 — Rebuild one static endpoint

Create the target CE scene with its final static geometry. Translate text,
coordinates, groups, and camera framing before adding animations. A still
frame makes scale and layout errors cheaper to diagnose.

### Step 5 — Add state and motion

Introduce `ValueTracker`, updaters, transforms, and camera motion one behavior
at a time. Make animation options keyword arguments. Replace GL-only shader
effects with CE-native visual cues.

### Step 6 — Extract only genuinely reusable pieces

If the port creates a reusable visual primitive, place it in the project's
`common/` package. Scene files should retain participation, layout, and
sequencing; construction logic shared across scenes belongs in `common/`.

Do not copy a large 3b1b helper module to obtain one class. Port the smallest
coherent behavior and remove unused dependencies.

### Step 7 — Validate in layers

Start with the relevant Python/preflight check, then render a still and a full
low-quality scene:

```sh
./render.sh path/to/scene.py SceneName -s -ql
./render.sh path/to/scene.py SceneName -ql
```

Inspect the output. A clean render only proves that the API calls executed; it
does not prove that font sizes, matching transforms, layering, camera angles,
or updater identities survived the port.

For actual scene work, follow the validation commands in `AGENTS.md`: run the
relevant Python preflight check, render the affected scene at `-ql`, and inspect
the result before a final-quality render.

## 12. Small before/after example

ManimGL:

```python
from manim_imports_ext import *

class Source(InteractiveScene):
    def construct(self):
        frame = self.frame
        curve = VMobject().set_points_as_corners([LEFT, UP, RIGHT])
        label = TexText("Signal")
        self.play(
            ShowCreation(curve),
            FadeIn(label, UP),
            frame.animate.set_height(6),
        )
```

ManimCE, preserving the behavior rather than the structure:

```python
from manim import *

from projects.sigreg_explainer.common import type as ty


class Target(MovingCameraScene):
    def construct(self):
        curve = VMobject().set_points_as_corners([LEFT, UP, RIGHT])
        label = ty.words("Signal")
        self.play(
            Create(curve),
            FadeIn(label, shift=UP),
            self.camera.frame.animate.scale_to_fit_height(6),
        )
```

Even this small port required decisions about the scene type, text system,
animation constructor, creation animation, and camera ownership.

## 13. Common failure signatures

| Symptom | Likely cause | First check |
|---|---|---|
| `NameError` after replacing the import | Name came from `manim_imports_ext`, `custom/`, or a video helper | Find its definition in `3blue1brown_videos/` |
| Object exists but looks wrong | Same name, different constructor/style semantics | Inspect both local class signatures |
| Math fails to compile after `Tex` port | ManimGL math-mode `Tex` became CE text-mode `Tex` | Use `MathTex` / `common.type.maths` |
| Formula coloring affects too much or nothing | CE substring was not isolated | Pass `substrings_to_isolate` at construction |
| Camera attribute is missing | A ManimGL universal frame was ported into CE `Scene` | Choose `MovingCameraScene` or `ThreeDScene` |
| Depth/shading method is missing | Copied method is OpenGL-specific | Rebuild the appearance for CE/Cairo |
| Fade direction behaves as another object | Positional ManimGL shift used with variadic CE fade | Use `shift=` |
| `LaggedStartMap` fails inside `begin()` | Compound child was expanded into animation arguments | Use `common.anim.lagged_map` |
| Fixed 3D label starts rotating after an update | `always_redraw` replaced registered family members | Keep stable instances and update them in place |
| Fade does not remove a live object | Its updater rebuilds style every frame | Freeze/clear updaters before fading |
| Port renders but framing differs | GL constants/config or font scale carried over | Use CE `config` and project type/layout helpers |

## 14. Licensing note for copied video code

The ManimCE and ManimGL engine repositories are MIT-licensed, but the
`3blue1brown_videos` repository states that its video source is licensed under
CC BY-NC-SA 4.0. Refactoring code does not by itself remove attribution,
non-commercial, or share-alike obligations. Before directly copying a scene or
helper, check that repository's `README.md` and license, record the source, and
decide whether reimplementing the underlying idea is more appropriate for the
intended use.

This is a project warning, not legal advice.
