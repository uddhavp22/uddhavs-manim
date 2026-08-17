# uddhavs-manim

Explainer animations built on [Manim Community Edition](https://www.manim.community/) — chiefly the **SIGReg explainer** in `projects/sigreg_explainer/`.

## Layout

```
uddhavs-manim/          this repo — the deliverable
├── projects/
│   └── sigreg_explainer/
│       ├── chapterB/, chapterC/     one file per beat
│       ├── common/                  reusable primitives: palette, layout, type, rig, wrap, beat, data
│       └── build.sh                 renders a chapter and concatenates it into a master
├── voiceover/           narration: TTS, word-level bookmark timing, subcaptions, music-bed ducking
├── tools/                preflight checks, font checks, still frames
├── docs/                 VISUAL_SYSTEM, NARRATION_SPEC, EXPLAINER_PROCESS, RENDER_REVIEW_SPEC
├── render.sh              render entrypoint — use this, not `manim` directly
├── manim.cfg             background color, resolution, media/assets dirs
└── pyproject.toml
```

This repo is a **standalone project that depends on Manim CE**, not a fork of it. The engine lives in a sibling clone:

```
Uddhavs manim/
├── manim-ce/        clone of ManimCommunity/manim — the engine
└── uddhavs-manim/   this repo
```

`pyproject.toml` sources `manim` from `../manim-ce` as an editable path dependency, so the engine can be read (and, if ever needed, patched) alongside the project rather than pinned to a PyPI release.

## Setup

Requires Python 3.12, and a sibling `manim-ce/` checkout next to this repo (see layout above).

```bash
brew install pkg-config cairo pango   # pycairo build deps
uv venv --python 3.12 .venv
uv pip install -e ../manim-ce
uv pip install -e .                    # this repo's own dependencies (see pyproject.toml)
```

Also needed on the system, not managed by the venv:
- **TinyTeX** at `~/Library/TinyTeX/bin/universal-darwin` — `render.sh` puts it on `PATH`.
- **ffmpeg**.
- The **Latin Modern Roman** OpenType font, installed from the TinyTeX tree:
  ```bash
  cp ~/Library/TinyTeX/texmf-dist/fonts/opentype/public/lm/lmroman10-regular.otf ~/Library/Fonts/
  ```
  Verify with `./render.sh tools/font_check.py FontCheck -s -ql` (see `docs/VISUAL_SYSTEM.md` §2 for why only the Regular weight is used).

Secrets: copy `.env.example` to `.env` and fill in `ELEVEN_API_KEY` if you plan to render with `--voice eleven` / `SIGREG_VOICE=eleven`. The default draft voice is the offline macOS `say` binary — every render works with no key set and no network access.

## Rendering

Always render through `./render.sh` (or `build.sh`), not `manim` directly — they resolve `manim.cfg` and every output path against the repo root, which a bare `manim` invocation from another working directory silently gets wrong.

```bash
./render.sh projects/demo/scene.py DemoExplainer -ql   # one scene, draft quality
./render.sh projects/demo/scene.py DemoExplainer       # 1080p60
./render.sh projects/demo/scene.py DemoExplainer -p    # ...and open the result
```

Draft (`-ql`) is 480p at 15fps — good for iterating on layout and timing, not for judging motion smoothness.

To build a whole chapter into one master file:

```bash
cd projects/sigreg_explainer
./build.sh chapterB1          # just Part 1 of chapter B, draft quality
./build.sh chapterB -qh       # every scene in chapter B, 1080p60
./build.sh all                # every chapter
```

Output: `media/masters/sigreg_explainer/<target>_master.mp4`.

`SIGREG_VOICE` (or `--voice`) defaults to `draft` (offline `say`, no API spend). Whisper transcription for word-level bookmark timing runs on first render of each narration line and caches under `media/voiceovers/` — later renders are much faster. Dropping `transcription_model=` from a scene's speech-service construction falls back to linear bookmark timing, useful for iterating on geometry before spending time on exact word placement.

## Docs

Read the relevant doc in `docs/` before adding a new visual pattern:

- `VISUAL_SYSTEM.md` — typography, color, layout rules
- [`MANIM_CE_VS_MANIMGL.md`](docs/MANIM_CE_VS_MANIMGL.md) — engine differences and how to refactor ManimGL/3b1b code into this ManimCE project
- `NARRATION_SPEC.md` — voiceover conventions
- `EXPLAINER_PROCESS.md` — how a chapter gets made, beat by beat
- `RENDER_REVIEW_SPEC.md` — what a finished render is checked against

`media/` is fully gitignored — everything under it (renders, caches, the TTS cache) is reproducible from source.
