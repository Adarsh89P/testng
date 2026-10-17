"""Offline reference-conditioned voice generation (run in /home/user/venv-tts).

  /home/user/venv-tts/bin/python tools/voice_clone.py lines.json reference.wav outdir

1. AI4Bharat Indic-TTS (Hindi FastPitch + HiFi-GAN, female speaker) speaks each line of the day's script, unchanged.
2. FreeVC24 (MIT, coqui-tts) converts every line to the timbre of reference.wav (a voice we have the rights to use).
Writes outdir/000.wav, 001.wav, ... (one per line). CPU only; ~3 s of compute per second of speech.
"""
import json, os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("TTS_HOME", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "models", "coqui"))
from TTS.api import TTS
import indic_tts

if __name__ == "__main__":
    lines, ref, od = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
    os.makedirs(od, exist_ok=True)
    synth = indic_tts.make_synth()
    vc = TTS("voice_conversion_models/multilingual/vctk/freevc24", progress_bar=False)
    for i, text in enumerate(lines):
        raw = os.path.join(od, f"raw_{i:03d}.wav")
        spoken = text.replace("।", ".")            # the model's vocabulary has '.' but not the Devanagari danda
        synth.save_wav(synth.tts(spoken, speaker_name="female"), raw)
        vc.voice_conversion_to_file(source_wav=raw, target_wav=ref, file_path=os.path.join(od, f"{i:03d}.wav"))
        print(f"line {i + 1}/{len(lines)} done", flush=True)
