#!/usr/bin/env bash
# Render a manim scene without having to remember the venv path or the
# TinyTeX PATH export.
#
#   ./render.sh <file.py> [SceneName ...] [manim flags]
#
# Examples:
#   ./render.sh projects/demo/scene.py Demo             # write mp4 at 1080p60
#   ./render.sh projects/demo/scene.py Demo -ql         # write mp4 at 480p15
#   ./render.sh projects/demo/scene.py Demo -p          # ...and open it
#   ./render.sh projects/demo/scene.py Demo -s          # save last frame as png
#   ./render.sh projects/demo/scene.py -a               # every scene in file
#
# Any flag `manim render` accepts is passed straight through. Note that writing
# is the default in Manim Community -- there is no -w, and -p only controls
# whether the result is opened afterwards.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# manim resolves BOTH manim.cfg and every output directory relative to the
# current working directory. Running from anywhere else silently loses the
# config (wrong background, wrong frame rate) and scatters renders into stray
# media/ folders. So: make every path argument absolute, then always run from
# the repo root.
args=()
for a in "$@"; do
  if [[ "$a" != -* && -e "$a" ]]; then
    args+=("$(cd "$(dirname "$a")" && pwd)/$(basename "$a")")
  else
    args+=("$a")
  fi
done
set -- "${args[@]}"
cd "$REPO_ROOT"

# LaTeX lives in TinyTeX, which is not on PATH for non-login shells.
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"

# manim loads scene files via spec_from_file_location, which does not put the
# repo root on sys.path. Without this, `from voiceover import VoiceoverScene`
# fails even though the package sits right next to the scene.
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

MANIM="$REPO_ROOT/.venv/bin/manim"
if [[ ! -x "$MANIM" ]]; then
  echo "error: $MANIM not found. Set the venv up with:" >&2
  echo "    uv venv --python 3.12 .venv" >&2
  echo "    uv pip install --python .venv/bin/python -e ../manim-ce" >&2
  exit 1
fi

exec "$MANIM" render "$@"
