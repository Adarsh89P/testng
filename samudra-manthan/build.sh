#!/bin/sh
# Rebuild the film: sh build.sh   (needs ffmpeg 7+ on PATH, and the Lemo-Opuscar library with `setup.sh deps` done)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${LIB:-/root/lemo-opuscar}
export LIB
cd "$LIB"
mkdir -p "$HERE/out"
node core/render/events.mjs "$HERE"
"$LIB/.venv/bin/python" "$HERE/mix.py"
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/samudra-manthan.mp4" 24 2
