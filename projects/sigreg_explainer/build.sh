#!/usr/bin/env bash
# Render every scene of a chapter and concatenate them in order.
#
#   ./build.sh chapterB          draft (480p15) — the default while iterating
#   ./build.sh chapterB1         just Part 1 of chapter B
#   ./build.sh chapterB1 -ql --voice eleven --force
#   ./build.sh chapterB -qh      final 1080p60
#   ./build.sh all               every chapter, one master per chapter
#
# Scene class is derived from the filename: b03_three_panels.py -> B03.
# Output: media/masters/sigreg_explainer/<target>_master.mp4
#
# Note that draft is now 480p at *15* fps, not 30: Manim Community's -ql couples
# frame rate to resolution. Timing still reads correctly, but do not judge
# motion smoothness from a draft.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../.." && pwd)"
CHAPTER="${1:-chapterB}"
shift || true
QUALITY="-ql"
VOICE="draft"
FORCE=0

# Ceiling on a single scene render, in seconds. See the watchdog in build_one:
# manim does not reliably exit after a scene raises, and without this one bad
# scene hangs a whole chapter build forever. Generous by default because a
# 1080p60 scene is legitimately slow; override for a quick draft pass with
# SIGREG_RENDER_TIMEOUT=300 ./build.sh chapterB1
RENDER_TIMEOUT="${SIGREG_RENDER_TIMEOUT:-1800}"

# Keep the historical positional quality flag working, while accepting the
# build settings in either order: `chapterB1 -ql --voice eleven`.
#
# -l and --hd are the manimgl spellings. They are still accepted and translated
# rather than rejected, because they appear throughout PLAN.md, RENDER_REVIEW.md
# and this repo's shell history; silently failing an old invocation would be a
# worse outcome than carrying two spellings.
while [[ $# -gt 0 ]]; do
  case "$1" in
    --voice)
      [[ $# -ge 2 ]] || { echo "error: --voice needs draft or eleven" >&2; exit 2; }
      VOICE="$2"; shift 2 ;;
    --force) FORCE=1; shift ;;
    -ql|-qm|-qh|-qp|-qk) QUALITY="$1"; shift ;;
    -l)    QUALITY="-ql"; shift ;;
    --hd)  QUALITY="-qh"; shift ;;
    *) echo "error: unknown build option: $1" >&2; exit 2 ;;
  esac
done

case "$VOICE" in
  draft|eleven) ;;
  *) echo "error: --voice must be draft or eleven (got $VOICE)" >&2; exit 2 ;;
esac
export SIGREG_VOICE="$VOICE"

# A quality/voice pair alone is not a render identity.  These files control
# Manim's output and voiceover behaviour but do not necessarily become newer
# than an existing clip after a checkout.  Hash their contents, including all
# local voiceover service code, so a corrected configuration cannot silently
# reuse an older video with the old behaviour baked in.
build_inputs_hash() {
  {
    shasum -a 256 "$REPO_ROOT/manim.cfg" "$REPO_ROOT/render.sh"
    find "$REPO_ROOT/voiceover" -type f -name '*.py' -print0 \
      | sort -z | xargs -0 shasum -a 256
  } | shasum -a 256 | awk '{print $1}'
}
BUILD_INPUTS_HASH="$(build_inputs_hash)"

# --- part maps ---------------------------------------------------------------
# A chapter can be published as separate parts. A part names the directory its
# scenes live in and the scenes themselves, in playback order; nothing moves on
# disk, so per-scene render paths still key off the *directory*.
#
# The order is explicit rather than a glob because Chapter B follows the
# learner's questions, not filename order: the obvious histogram attempt fails
# immediately after the opening problem; the characteristic function is named
# immediately after its construction; and the later scenes stress-test that
# named object before asking what the complete curve guarantees.
part_dir() {
  case "$1" in
    chapterB1|chapterB2) echo "chapterB" ;;
    *)                   echo "$1" ;;
  esac
}

part_scenes() {
  case "$1" in
    chapterB1) echo "b00 b01 b02 b03 b04 b05 b06 b07" ;;
    # Part 2 is deliberately ordered as an argument, not by filename.  First
    # establish what a complete curve means; then decide which part of that
    # curve is trustworthy; only then introduce the Gaussian target and the
    # smooth loss built from it.
    chapterB2) echo "b08 b09 b10 b11" ;;
    chapterB)  echo "b00 b01 b02 b03 b04 b05 b06 b07 b08 b09 b10 b11" ;;
    *)         echo "" ;;   # whole directory, in filename order
  esac
}

build_one() {
  local chapter="$1" quality="$2"
  shopt -s nullglob
  local dir order scenes=()
  dir="$(part_dir "$chapter")"
  order="$(part_scenes "$chapter")"

  if [[ -n "$order" ]]; then
    local stem match
    for stem in $order; do
      match=("$HERE/$dir/${stem}_"*.py)
      # Exactly one, or the part is lying about what it contains. A silently
      # dropped scene is the failure mode that matters here: the master would
      # still build, just missing a minute of the argument.
      if [[ ${#match[@]} -ne 1 ]]; then
        echo "error: part '$chapter' names scene '$stem', which matches" >&2
        echo "       ${#match[@]} files in $dir (expected exactly 1)" >&2
        exit 1
      fi
      scenes+=("${match[0]}")
    done
  else
    scenes=("$HERE/$dir"/[abc][0-9][0-9]*_*.py)
  fi

  if [[ ${#scenes[@]} -eq 0 ]]; then
    echo "  (no scenes in $chapter, skipping)"
    return 0
  fi

  # Preflight before spending anything. A NameError inside a beat method only
  # raises when that beat runs, which in this chapter meant twenty minutes and
  # a full chapter's text-to-speech before the failure surfaced.
  PYTHONPATH="$HERE:$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}" \
    "$REPO_ROOT/.venv/bin/python" "$REPO_ROOT/tools/preflight.py" \
    "$HERE/$dir" "$HERE/common" || exit 1

  local outputs=()
  for src in "${scenes[@]}"; do
    local base scene
    base="$(basename "$src" .py)"
    scene="$(echo "${base%%_*}" | tr '[:lower:]' '[:upper:]')"
    echo "==> $base :: $scene"

    # Manim Community owns the output path and composes it from config as
    # media/videos/{module_name}/{quality}/{Scene}.mp4. Ask the engine where it
    # intends to write rather than reconstructing that here -- the {quality}
    # segment is a resolution-and-framerate stamp that moves with the -q flag
    # and with manim.cfg, and a wrong guess would not fail loudly, it would
    # quietly defeat the staleness check below.
    #
    # Run it from the repo root, as render.sh does: manim reads manim.cfg from
    # the working directory and resolves media_dir against it, so asking from
    # anywhere else would answer for a different config than the render uses.
    local out
    out="$(cd "$REPO_ROOT" && PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}" \
      "$REPO_ROOT/.venv/bin/python" "$REPO_ROOT/tools/output_path.py" \
      "$src" "$scene" "$quality")" || exit 1
    local keyfile="${out}.buildkey"
    local build_key="quality=${quality};voice=${VOICE};inputs_sha256=${BUILD_INPUTS_HASH}"
    local rebuild="$FORCE"
    local dep
    if [[ "$rebuild" -eq 0 ]]; then
      if [[ ! -f "$out" || ! -f "$keyfile" || "$(<"$keyfile")" != "$build_key" ]]; then
        rebuild=1
      else
        for dep in "$src" "$HERE"/common/*.py "$HERE/facts.py"; do
          if [[ "$dep" -nt "$out" ]]; then rebuild=1; break; fi
        done
      fi
    fi

    if [[ "$rebuild" -eq 0 ]]; then
      echo "    (up to date)"
      outputs+=("$out")
      continue
    fi

    # Record the mtime BEFORE rendering. Testing that the output file exists is
    # not a test that this render produced it: manim exits 0 after an exception
    # inside construct(), so a scene that crashed left the previous render on
    # disk and the master was silently rebuilt from stale clips. The file must
    # be newer than the attempt, not merely present. (Manim Community exits 1 on
    # a construct() exception where manimgl exited 0, so `set -e` would now
    # catch most of these -- the check stays because it also catches the case
    # where the render succeeds but writes somewhere other than expected.)
    local before=0
    [[ -f "$out" ]] && before="$(stat -f %m "$out")"

    # No -w: writing is the default in Manim Community. -v WARNING replaces the
    # old -q; manim.cfg already sets it, but a chapter build should not depend
    # on that staying true.
    #
    # Run under a watchdog. When a scene raises, manim prints the traceback and
    # then does *not* exit -- the process sits at 0% CPU indefinitely, because
    # stable-ts/torch leaves a non-daemon thread behind (the "leaked semaphore"
    # warning at the end of a clean run is the same machinery). It cost two
    # separate sessions a misdiagnosis: both read the silence as a slow render
    # and waited on a process that had already failed. A successful render exits
    # normally, so in practice this only fires on the failure path -- but
    # without it a single bad scene blocks a chapter build forever, which is a
    # worse failure than stopping. macOS ships no timeout(1), hence doing it by
    # hand.
    "$REPO_ROOT/render.sh" "$src" "$scene" "$quality" -v WARNING &
    local render_pid=$!
    ( sleep "$RENDER_TIMEOUT"
      kill -0 "$render_pid" 2>/dev/null && kill "$render_pid" 2>/dev/null ) &
    local watchdog_pid=$!

    local rc=0
    wait "$render_pid" || rc=$?
    kill "$watchdog_pid" 2>/dev/null || true
    wait "$watchdog_pid" 2>/dev/null || true

    if [[ $rc -ne 0 ]]; then
      echo "error: $scene render exited $rc" >&2
      if [[ $rc -eq 143 ]]; then
        echo "       (143 = SIGTERM: killed by the ${RENDER_TIMEOUT}s watchdog." >&2
        echo "        Either the scene is genuinely slower than that, or it" >&2
        echo "        raised and hung. Scroll up for a traceback.)" >&2
      fi
      exit 1
    fi

    if [[ ! -f "$out" ]]; then
      echo "error: $scene produced no output at $out" >&2
      exit 1
    fi
    local after; after="$(stat -f %m "$out")"
    if [[ "$after" -le "$before" ]]; then
      echo "error: $scene did not rebuild -- $out is unchanged from before the" >&2
      echo "       render, so construct() almost certainly raised. Scroll up." >&2
      exit 1
    fi
    printf '%s\n' "$build_key" > "$keyfile"

    outputs+=("$out")
  done

  # Discover the rate only after rendering. An ElevenLabs pass changes it from
  # 22050 to 44100, so looking at an old clip before the loop would generate
  # mismatched padding in the very pass this script is meant to protect.
  local RATE=""
  local out r
  for out in "${outputs[@]}"; do
    r="$(ffprobe -v error -select_streams a -show_entries stream=sample_rate \
         -of csv=p=0 "$out" 2>/dev/null | head -1)"
    if [[ -n "$r" ]]; then RATE="$r"; break; fi
  done
  RATE="${RATE:-22050}"

    # A scene with no narration has no audio stream at all. The concat demuxer
    # with -c copy cannot span mismatched stream layouts: it silently ends the
    # audio track at the first such file, so the master loses every second of
    # narration after it. Note that silence-detection will NOT catch this --
    # a missing stream is not silence. Pad with real silence instead.
  local list; list="$(mktemp)"
  local concat_outputs=()
  local concat_temps=()
  for out in "${outputs[@]}"; do
    # Do not use `ffprobe | grep -q` here. With pipefail enabled, grep may
    # close after its match and leave ffprobe with SIGPIPE, falsely classifying
    # a narrated scene as silent.
    local audio_type
    audio_type="$(ffprobe -v error -select_streams a \
      -show_entries stream=codec_type -of csv=p=0 "$out")"
    local dur
    dur="$(ffprobe -v error -select_streams v:0 -show_entries stream=duration \
           -of csv=p=0 "$out")"
    local normalized
    normalized="$(mktemp -t sigreg-concat)"
    concat_temps+=("$normalized")
    if [[ "$audio_type" != "audio" ]]; then
      # The silent track MUST match the sample rate of the narrated scenes.
      # Concat -c copy computes timestamps from the first stream's rate, so
      # padding at 44100 against manim's 22050 reports exactly double the
      # duration. Rate is discovered, not assumed. -t rather than -shortest,
      # which is unreliable alongside -c:v copy.
      echo "    (no narration in $(basename "$out") — padding with silence at ${RATE} Hz)"
      ffmpeg -v error -y -i "$out" \
             -f lavfi -t "$dur" \
             -i "anullsrc=channel_layout=stereo:sample_rate=${RATE}" \
             -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -ar "${RATE}" \
             -ac 2 -f mp4 "$normalized"
    else
      # Manim stops the audio stream at the final spoken cue while the video
      # commonly continues through an inspect/fade beat. The concat demuxer
      # represents that missing tail by stretching one AAC packet. Some
      # players then switch the next scene's audio on abruptly or clip its
      # opening syllable. Give every clip a real, continuous audio timeline
      # exactly as long as its video before stitching.
      ffmpeg -v error -y -i "$out" -map 0:v:0 -map 0:a:0 \
             -c:v copy -af apad -t "$dur" -c:a aac -ar "${RATE}" -ac 2 \
             -f mp4 "$normalized"
    fi
    concat_outputs+=("$normalized")
  done

  # The concat demuxer with stream copy does not reject mismatched audio
  # parameters; it simply stops the master audio at the first mismatch. Refuse
  # to create that silently corrupt master and name every offending clip.
  local audio_signature="" signature
  for out in "${concat_outputs[@]}"; do
    signature="$(ffprobe -v error -select_streams a:0 \
      -show_entries stream=codec_name,sample_rate,channels -of csv=p=0 "$out")"
    if [[ -z "$audio_signature" ]]; then
      audio_signature="$signature"
    elif [[ "$signature" != "$audio_signature" ]]; then
      echo "error: cannot concatenate mixed audio formats:" >&2
      echo "       expected $audio_signature" >&2
      echo "       got      $signature  $out" >&2
      rm -f "$list"; exit 1
    fi
  done
  for out in "${concat_outputs[@]}"; do
    printf "file '%s'\n" "$out" >> "$list"
  done

  # Masters live under media/ alongside the per-scene renders now that manim
  # owns that tree; media/ is gitignored in full, and a master is a build
  # artefact like any other. mkdir because nothing else creates this level.
  local master_dir="$REPO_ROOT/media/masters/sigreg_explainer"
  mkdir -p "$master_dir"
  local master="$master_dir/${chapter}_master.mp4"
  # Video remains a stream-copy stitch of the rendered MP4s. Audio is decoded
  # across the whole list and encoded once, removing per-file AAC priming and
  # edit-list discontinuities without touching a rendered frame. Mux the two
  # finished streams as a separate last step: asking one ffmpeg process to copy
  # H.264 while encoding AAC shifts the video globally by one AAC frame.
  local master_video master_audio
  master_video="$(mktemp -t sigreg-master-video)"
  master_audio="$(mktemp -t sigreg-master-audio)"
  ffmpeg -v error -y -f concat -safe 0 -i "$list" \
         -map 0:v:0 -an -c:v copy -f mp4 "$master_video"
  ffmpeg -v error -y -f concat -safe 0 -i "$list" \
         -map 0:a:0 -vn -c:a aac -ar "${RATE}" -ac 2 \
         -f mp4 "$master_audio"
  ffmpeg -v error -y -i "$master_video" -i "$master_audio" \
         -map 0:v:0 -map 1:a:0 -c copy "$master"
  rm -f "$list"
  rm -f "$master_video" "$master_audio"
  for out in "${concat_temps[@]}"; do rm -f "$out"; done
  echo "master: $master  ($(ffprobe -v error -show_entries format=duration \
      -of csv=p=0 "$master")s)"

  # Dead air. A scene can hold an empty frame for seconds with narration over
  # it and pass every other check in this repo -- b00 did exactly that, and the
  # only symptom was that the video "dragged". Reported, not fatal: the master
  # is already built and worth looking at, and the judgement about whether a
  # given gap is deliberate belongs to the review.
  echo "--- dead air ---"
  python3 "$REPO_ROOT/tools/dead_air.py" --min 1.5 "$master" || true
}

if [[ "$CHAPTER" == "all" ]]; then
  for c in chapterA chapterB chapterC; do
    [[ -d "$HERE/$c" ]] && { echo "--- $c ---"; build_one "$c" "$QUALITY"; }
  done
else
  build_one "$CHAPTER" "$QUALITY"
fi
