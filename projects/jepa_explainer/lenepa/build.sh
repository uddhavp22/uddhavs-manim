#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SOURCE="$ROOT/projects/jepa_explainer/lenepa/scenes.py"
VOICE="eleven"
QUALITY="h"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --voice) VOICE="$2"; shift 2 ;;
    --quality) QUALITY="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

case "$VOICE" in
  eleven|draft|timing) ;;
  *) echo "voice must be eleven, draft, or timing" >&2; exit 2 ;;
esac
case "$QUALITY" in
  l|m|h|p|k) ;;
  *) echo "quality must be l, m, h, p, or k" >&2; exit 2 ;;
esac

SCENES=(
  LeNEPA01Tokens
  LeNEPA02Predict
  LeNEPA03PredictionLoss
  LeNEPA04TemporalSIGReg
  LeNEPA05Objective
  LeNEPA06Protocol
  LeNEPA07Results
  LeNEPA08Landing
)

cd "$ROOT"
.venv/bin/python tools/preflight.py projects/jepa_explainer/lenepa
.venv/bin/python projects/jepa_explainer/lenepa/facts.py
.venv/bin/python tools/narration_audit.py projects/jepa_explainer/lenepa/scenes.py

for scene in "${SCENES[@]}"; do
  LENEPA_VOICE="$VOICE" ./render.sh "$SOURCE" "$scene" "-q$QUALITY"
done

list_file="$ROOT/media/lenepa-${VOICE}-${QUALITY}-concat.txt"
: > "$list_file"
for scene in "${SCENES[@]}"; do
  path="$(.venv/bin/python tools/output_path.py "$SOURCE" "$scene" "-q$QUALITY")"
  printf "file '%s'\n" "$path" >> "$list_file"
done

output_dir="$ROOT/media/videos/jepa_explainer/lenepa"
mkdir -p "$output_dir"
output="$output_dir/LeNEPA_segment_${VOICE}_q${QUALITY}.mp4"
raw_output="$output_dir/.LeNEPA_segment_${VOICE}_q${QUALITY}_raw.mp4"
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i "$list_file" -c copy "$raw_output"

# Manim ends each scene's AAC stream at its last spoken cue, while the video
# continues through the closing inspection/fade.  Pad the master to the exact
# video duration so players do not see a short audio stream at the final cut.
video_duration="$(ffprobe -v error -select_streams v:0 \
  -show_entries stream=duration -of csv=p=0 "$raw_output")"
ffmpeg -hide_banner -loglevel error -y -i "$raw_output" \
  -map 0:v:0 -map 0:a:0 -c:v copy -af apad -t "$video_duration" \
  -c:a aac -ar 48000 -ac 2 "$output"
rm -f "$raw_output"

echo "$output"
