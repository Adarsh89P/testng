"""Find voice-over line cuts for a day whose recording has no pauses (ElevenLabs v4 ignores <break> tags).

Reads a TTS reading of the day's script with known line boundaries, aligns it to the uploaded voice-over (DTW over
voice_check MFCC features), maps each boundary across and snaps it to the quietest point within 0.8 s. Prints the
voice similarity, the cuts, the line check and the silence runs (>= 0.3 s) so cuts can be placed between sentences.

Usage (from the repo root):  python3 tools/align_cuts.py <day_module> <dayNN> [upload_name]
e.g.                         python3 tools/align_cuts.py day30_loss_aversion day30
"""
import os, sys, importlib
import numpy as np, librosa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "figma"))
import engine, voice_check as V                                    # noqa: E402


def main(mod_name, key, upload=None):
    M = importlib.import_module(mod_name)
    path = os.path.join(ROOT, "assets", "voice", key, "full.mp3")
    sr = engine.SR
    y = V._load(path, sr)
    if upload: print("name ok:", V.check_upload_name(upload))
    try: print("similarity", round(V.voice_similarity(y, sr), 3))
    except Exception as e: print("similarity: n/a (master missing:", type(e).__name__ + ")")
    engine.NATURAL = False
    segs = [engine.tts(s.spoken, voice="hf_beta", speed=1.05, lang="hi") for s in M.SCENES]
    bounds = np.cumsum([len(s) for s in segs])[:-1] / sr
    hop = int(0.02 * sr)
    A, B = V._feat(np.concatenate(segs), sr), V._feat(y, sr)
    _, wp = librosa.sequence.dtw(A, B, metric="cosine"); wp = wp[::-1]
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    cuts = []
    for b in bounds:
        fa = int(b * sr / hop)
        fb = int(np.median(wp[wp[:, 0] == fa][:, 1]))
        w = int(0.8 * sr / hop); lo, hi = max(0, fb - w), min(len(rms), fb + w)
        cuts.append(round((lo + int(np.argmin(rms[lo:hi]))) * hop / sr, 2))
    print("CUTS", cuts)
    print("line check", V.line_check(y, M.SCENES, cuts))
    s = rms < 0.01; runs = []; i = 0
    while i < len(s):
        if s[i]:
            j = i
            while j < len(s) and s[j]: j += 1
            if j - i >= 15: runs.append((round(i * 0.02, 2), round(j * 0.02, 2)))
            i = j
        else:
            i += 1
    print("silences", runs)


if __name__ == "__main__":
    main(*sys.argv[1:4])
