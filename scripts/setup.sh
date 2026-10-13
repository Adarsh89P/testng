#!/usr/bin/env bash
# One-shot setup for the YoutubeAutomation2 video pipeline (Hinglish channel).
# Safe to re-run: skips anything already present.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FONTS="$ROOT/assets/fonts"; MODELS="$ROOT/assets/models"
mkdir -p "$FONTS" "$MODELS"

echo "== system packages (ffmpeg, Devanagari fonts, imagemagick)"
if ! command -v ffmpeg >/dev/null || ! fc-list | grep -qi devanagari; then
  apt-get update -q && apt-get install -y -q ffmpeg imagemagick fonts-noto-core fonts-noto-extra fonts-noto-ui-core fonts-noto-color-emoji
fi

echo "== python packages"
pip3 install --break-system-packages -q -r "$ROOT/requirements.txt"

echo "== fonts (Google Fonts)"
for f in ofl/poppins/Poppins-Bold.ttf ofl/poppins/Poppins-ExtraBold.ttf ofl/poppins/Poppins-Black.ttf \
         ofl/anton/Anton-Regular.ttf ofl/bebasneue/BebasNeue-Regular.ttf \
         ofl/mukta/Mukta-Bold.ttf ofl/mukta/Mukta-ExtraBold.ttf ofl/hind/Hind-Bold.ttf \
         "ofl/baloo2/Baloo2%5Bwght%5D.ttf" "ofl/montserrat/Montserrat%5Bwght%5D.ttf" \
         "ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf" "ofl/inter/Inter%5Bopsz,wght%5D.ttf"; do
  n="$(basename "$f" | sed 's/%5B/[/;s/%5D/]/')"
  [ -s "$FONTS/$n" ] || curl -sSfL -o "$FONTS/$n" "https://raw.githubusercontent.com/google/fonts/main/$f"
done
# pycairo finds Inter / JetBrains Mono by family name, so register them with fontconfig
mkdir -p ~/.fonts && cp "$FONTS"/*.ttf ~/.fonts/ && fc-cache -f >/dev/null

echo "== Kokoro offline TTS model (Hindi voices: hf_alpha hf_beta hm_omega hm_psi)"
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "$MODELS/$f" ] || curl -sSfL -o "$MODELS/$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done

echo "== rembg background-removal model"
python3 -c "from rembg import new_session; new_session('u2net')" >/dev/null 2>&1 || true

echo "== checks"
python3 - <<'PY'
from PIL import features
assert features.check('raqm'), "Pillow lacks raqm: Devanagari text will render broken"
import kokoro_onnx, moviepy, cv2, numpy, soundfile, pydub
print("all python imports ok, raqm", features.version('raqm'))
PY
echo "setup complete"
