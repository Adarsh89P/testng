#!/bin/sh
# Rebuild: sh build.sh  (ffmpeg 7+ on PATH; Lemo-Opuscar library installed). Oil painting, mrityunjaya short v2.
set -e
HERE=$(cd "$(dirname "$0")" && pwd); LIB=${LIB:-/root/lemo-opuscar}; export LIB; cd "$LIB"; mkdir -p "$HERE/out"
"$LIB/.venv/bin/python" "$HERE/mix.py"
node core/render/video.mjs "$HERE" --fps 24 --workers 4 --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/mrityunjaya.mp4" 24 0
