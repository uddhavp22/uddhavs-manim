# Plugin adoption

Research from the ManimGL → Manim Community migration, evaluating the 12
third-party packages considered for the SIGReg explainer. Checked against
actual PyPI JSON metadata (`curl https://pypi.org/pypi/<name>/json`), not just
package descriptions — several have version pins that conflict with this
repo's `manim>=0.20.1` and wouldn't be obvious from the package page alone.

## Adopted

- **`manim-vision`** (installed, `pyproject.toml`) — watches `add`/`play`/
  `remove`, converts tracked `VMobject`s to Shapely geometry, and reports
  meaningful overlaps as a collision timeline. Automates the exact class of
  defect [`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) and
  [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) §5 check by eye today (e.g. the
  documented "t axis label clipping the right edge" bug).

  Wired into `common/beat.py`'s `ActScene` — `setup()`/`tear_down()` are
  Manim's own scene lifecycle hooks (`Scene.render()` calls
  `setup() -> construct() -> tear_down()`), so every scene gets monitored
  automatically with no per-file boilerplate. **Off by default**: it only
  attaches when `SIGREG_VISION=1` is set, e.g.
  `SIGREG_VISION=1 ./render.sh <scene> -ql`. It stays off for normal and
  final-pass renders on purpose — it runs a background collision-check
  executor alongside the real render, it is beta software (`Development
  Status :: 4 - Beta` on PyPI) whose geometry engine has not been exercised
  against every mobject type this project uses (a couple of `MathTex` glyph
  paths threw `shapely` `TopologyException` warnings on the first real run
  against `b03` — logged and skipped, not fatal, but a real gap), and a
  diagnostic tool must never be able to jeopardize a paid ElevenLabs render.
  Both `monitor()` and `shutdown()` calls are wrapped in `except Exception`
  for the same reason.

  Reports land in `media/manim_vision/<Scene>_*.{json,jsonl,txt}` — see the
  package's own README for the format. A first run against `B03` returned
  233 collision events across 28 groups; these have not yet been triaged for
  which are real layout defects versus expected transient overlap during a
  sweep (e.g. arrow tips passing near each other), which is the next step
  before this becomes a standing render-review gate rather than an
  available tool.

## Needs a decision — compatible, on-topic, not yet installed

- **`statanim`** (`manim>=0.18.0` ✓, adds `scipy`) — pre-built Normal/
  Binomial/Poisson distributions, regression, hypothesis testing, probability
  trees. Directly on-topic: this project's subject is characteristic
  functions and Gaussian fingerprints. Add with `uv add statanim` if picked
  up; no code currently depends on it.

## Needs an explicit decision — not a quick add

- **`manim-voiceover-plus`** (`manim>=0.19,<1.0` ✓) — a maintained fork of
  upstream `manim_voiceover` with current ElevenLabs support. Direct
  competitor to this repo's hand-rolled `voiceover/` package, which has been
  ported through two engine migrations and carries real custom work
  (background-music ducking with measured dB numbers, macOS `say` fallback,
  subcaption wrapping — see [`MANIM_GUIDE.md`](MANIM_GUIDE.md) §8). Adopting
  it means verifying every one of those exists upstream or gets re-ported,
  and it pulls `sox`/`mutagen` back in — dependencies `voiceover/audio.py`'s
  docstring explains were deliberately dropped for `pydub`+`ffmpeg`. Its
  `transcribe` extra also pins `openai-whisper<20230315` /
  `stable-ts<3.0,>=2.6.2`, which may reopen the numpy resolver fight
  `pyproject.toml` documents.
  **Status: awaiting a decision from the user on whether it's worth displacing
  the hand-rolled package.**

## On standby — not currently relevant, kept for later

Not adopted because nothing in the current explainer needs them, not because
they're broken. Revisit if the project's output format changes.

- **`manim-videos`** — embeds external video clips inside a scene. Nothing in
  chapters B or C currently composites in outside footage; every visual is
  generated. Would matter if a future chapter wants to cut to a recorded
  demo, screen capture, or real-world clip alongside the animation.

Has no hard compatibility blocker recorded against `manim>=0.20.1` — that
check should be re-run against current PyPI metadata before installing, since
this doc reflects an August 2026 snapshot.

## Hard compatibility blockers — do not attempt without re-checking first

- **`manim-physics`** — requires `manim<0.19.0`. We're on `0.20.1`. Will not
  install alongside the current engine, full stop. Author also states
  limited ongoing maintenance.
- **`manim-euclid`** — requires Python `>=3.13`. This venv is pinned to 3.12
  (see `pyproject.toml`'s `requires-python`). "Experimental" status, one
  contributor.
- **`chanim`** (`raghavg123/chanim`, mirrored at `kilacoda/chanim`) — chemistry
  drawing extension (chemfig LaTeX bonds/rings). Archived by its author
  2026-01-12 ("stopped working on Manim a couple years ago... faulty code").
  Spike-tested 2026-08-10: `uv add chanim` resolves and installs cleanly
  (`requires-dist` is just `manim`, unpinned), but it registers itself via
  manim CE's `manim.plugins` entry point, which `manim/plugins/__init__.py`
  loads *unconditionally* on every `manim` invocation — not only when a scene
  imports it. Its `chem_objects.py` references `TexSymbol`, an attribute this
  version of manim CE doesn't have, so the entry point load throws
  `NameError` at import time and **`manim --version` itself fails** with the
  package merely installed. Confirmed broken, reverted (`uv remove chanim`),
  confirmed `manim --version` works again. Do not reinstall without patching
  `chem_objects.py`'s `TexSymbol` reference or removing/renaming its
  `manim.plugins` entry point first — either fix would need to happen in a
  fork, since upstream is archived.

## Stale, unverified against CE 0.20 — spike-test before relying on

- **`manim-ml`** — last released April 2023, before this migration's own
  discovered API breaks (`Tex`/`MathTex` split, `LaggedStartMap`). No manim
  version pin in its PyPI metadata at all. If chapter C ever wants
  neural-net diagrams (plausible — B11 ends on "representations are vectors,
  in hundreds of dimensions"), render one of its example scenes first, don't
  assume it works.
- **`manim-svg-animations`** — last released March 2023, targets Python
  `<3.12` (we're on 3.12, likely broken), and its output is interactive
  HTML/JS, not the MP4s this project delivers.
- **`manim-extras`** — one release, 2022, abandoned, unclear differentiation.

## Not actually manim libraries — flag before assuming otherwise

- **`manim-mcp`** — not importable into a scene at all. It's a standalone
  LLM-agent CLI/MCP-server that generates *and executes* manim code from
  natural-language prompts, and it depends on **`manimgl`** — the engine this
  project just migrated away from. Stores LLM API keys, uploads renders to
  S3/MinIO. Different tool, different workflow, out of scope.
- **`manim-claude`** — not a dependency for this repo either. It's a Claude
  Code *skill* package that installs reference files into the Claude Code
  setup itself, not into `uddhavs-manim`. Brand-new, single-maintainer,
  first release. Needs explicit confirmation before running its installer —
  it modifies the agent's own environment, not this project.
