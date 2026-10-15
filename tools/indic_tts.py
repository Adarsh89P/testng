"""Indic-TTS (AI4Bharat) Hindi synthesis: FastPitch + HiFi-GAN trained on native-speaker studio recordings.
Run with the isolated venv: /home/user/venv-tts/bin/python tools/indic_tts.py OUT.wav SPEAKER "text"
"""
import sys, os, json, tempfile, warnings
warnings.filterwarnings("ignore")
import torch
from TTS.utils.synthesizer import Synthesizer

ROOT = os.path.join(os.path.dirname(__file__), "..", "assets", "models", "indic", "hi")
FP, HG = os.path.join(ROOT, "fastpitch"), os.path.join(ROOT, "hifigan")


def make_synth():
    cfg = json.load(open(os.path.join(FP, "config.json")))
    spk = os.path.join(FP, "speakers.pth")
    cfg["speakers_file"] = spk
    if "model_args" in cfg: cfg["model_args"]["speakers_file"] = spk
    tmp = os.path.join(tempfile.mkdtemp(), "config.json"); json.dump(cfg, open(tmp, "w"))
    return Synthesizer(tts_checkpoint=os.path.join(FP, "best_model.pth"), tts_config_path=tmp, tts_speakers_file=spk,
                       vocoder_checkpoint=os.path.join(HG, "best_model.pth"), vocoder_config=os.path.join(HG, "config.json"),
                       use_cuda=False)


if __name__ == "__main__":
    s = make_synth()
    if len(sys.argv) == 4 and sys.argv[1] == "--batch":          # --batch lines.json outdir  (one model load)
        lines = json.load(open(sys.argv[2])); od = sys.argv[3]; os.makedirs(od, exist_ok=True)
        for i, (spk, text) in enumerate(lines):
            s.save_wav(s.tts(text, speaker_name=spk), os.path.join(od, f"{i:03d}.wav"))
        print("batch", len(lines)); sys.exit()
    if len(sys.argv) < 4:
        print("speakers:", list(s.tts_model.speaker_manager.name_to_id)); sys.exit()
    out, spk, text = sys.argv[1], sys.argv[2], sys.argv[3]
    wav = s.tts(text, speaker_name=spk)
    s.save_wav(wav, out); print("saved", out)
