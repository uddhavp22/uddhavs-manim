#!/usr/bin/env bash
# Manim Sideview (the VS Code extension)'s `manim-sideview.defaultManimPath`
# target.
#
# Sideview spawns this directly via Node's child_process.spawn with
# shell: false and cwd set to whatever directory holds the .py file being
# previewed -- it does not go through render.sh, and it must not: render.sh
# force-cds to the repo root, which would make it load the repo-root
# manim.cfg instead of the one Sideview already parsed from the scene's own
# directory to predict the output path, breaking its "find the rendered
# file" logic. This wrapper preserves whatever cwd Sideview passed in.
#
# It still needs the same PATH fix render.sh applies: TinyTeX (LaTeX, needed
# for any MathTex) is exported only in ~/.zshrc, an interactive-shell file
# that a GUI-launched VS Code does not reliably source before spawning
# extensions' child processes.
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$REPO_ROOT/.venv/bin/manim" "$@"
