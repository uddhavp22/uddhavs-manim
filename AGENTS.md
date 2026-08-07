# Repository Instructions

This is a Manim Community educational-animation project.

## Before editing

Read the closest relevant doc in `docs/` (VISUAL_SYSTEM.md, NARRATION_SPEC.md,
EXPLAINER_PROCESS.md, RENDER_REVIEW_SPEC.md) and inspect existing components
before creating new abstractions.

## Architecture

Reusable visual primitives belong in the project's `common/` package
(e.g. `projects/sigreg_explainer/common/`: palette, layout, type, rig, wrap,
beat, data).

Scene files should primarily describe:
- which visual objects participate
- layout
- animation sequencing
- scene-specific state

Do not duplicate reusable construction logic across scenes.

## Visual consistency

Follow the existing semantic colors, typography, spacing, and animation
conventions defined in `common/` and `docs/VISUAL_SYSTEM.md`.

Search existing scenes and `common/` before introducing a new visual pattern.

## Validation

Always render through `./render.sh` from the repo root — it handles the venv,
the TeX PATH, and manim.cfg resolution.

For scene changes:
1. run the relevant Python checks (`tools/preflight.py` where applicable)
2. render the affected scene at low quality: `./render.sh <file.py> <Scene> -ql`
3. inspect failures and repair them before finishing

For refactors:
- preserve existing behavior
- avoid unrelated cleanup
- report every affected file

## Completion report

Keep the final response concise:

- Files changed
- What changed
- Validation performed
- Any remaining concern

Do not paste large code snippets when the changes are already present in the
working tree.
