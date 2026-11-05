#!/bin/sh
# Rebuild: sh build.sh  (ffmpeg 7+ on PATH; Lemo-Opuscar library installed). Audio = the shadow-puppet film's mix (same voice-over and timing).
set -e
HERE=$(cd "$(dirname "$0")" && pwd); LIB=${LIB:-/root/lemo-opuscar}; export LIB; cd "$LIB"; mkdir -p "$HERE/out"
[ -f "$HERE/out/mix.wav" ] || cp "$HERE/../markandeya/out/mix.wav" "$HERE/out/mix.wav"
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/markandeya-oil.mp4" 24 0
