"""Voice-over rule tests: python3 tests/test_voice_pipeline.py  (no network; ~1-2 min, mostly TTS for the checks)."""
import json, os, re, subprocess, sys, tempfile
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "figma"))
import voice_check as V, voice_gen, day05_millers_law as D5

MASTER = V.MASTER
tmp = tempfile.mkdtemp()


def expect_error(fn, exc, words):
    try: fn()
    except exc as e:
        assert all(w in str(e) for w in words), str(e); return str(e)
    raise AssertionError("expected an error")


def test_no_elevenlabs_in_runtime():
    hits = subprocess.run(["grep", "-rliE", "api\\.elevenlabs\\.io|xi-api-key|ELEVENLABS_API_KEY", "figma", "tools", "scripts"],
                          cwd=ROOT, capture_output=True, text=True).stdout.split()
    assert not hits, hits


def test_master_untouched():
    assert V.load_registry()["day04"]["sha256"] == V.sha256(MASTER)


def test_duplicate_of_master_rejected_for_day05():
    expect_error(lambda: V.verify(5, "Miller's Law", MASTER, D5.SCENES, "day05_millers_law"), V.VoiceError, ["byte-identical", "day04"])


def test_reencoded_master_rejected_for_day05():
    p = os.path.join(tmp, "re.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", MASTER, "-b:a", "96k", p], check=True)
    expect_error(lambda: V.verify(5, "Miller's Law", p, D5.SCENES, "day05_millers_law"), V.VoiceError, ["day05"])
    assert "day05" not in V.load_registry()


def test_master_refused_as_clone_reference():
    cfg = os.path.join(tmp, "ref.json")
    json.dump({"file": "assets/voice/day04/full.mp3", "owner": "x", "rights": "own voice"}, open(cfg, "w"))
    voice_gen.REF_CFG = cfg
    expect_error(voice_gen.reference, voice_gen.RefError, ["day04"])


def test_reference_requires_rights():
    cfg = os.path.join(tmp, "ref2.json"); wav = os.path.join(tmp, "r.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=220:d=2", wav], check=True)
    json.dump({"file": wav, "owner": "x"}, open(cfg, "w"))
    voice_gen.REF_CFG = cfg
    expect_error(voice_gen.reference, voice_gen.RefError, ["rights"])


def test_comparison_import_keeps_on_screen_day():
    import importlib, sys as _s, day02_hicks_law as D
    _s.modules.pop("day04_jakobs_law", None)             # force a fresh import (its import sets DAY 4)
    D.DAY, D.NEXT = 6, "Goal-Gradient Effect"
    V._day_scenes(4)                                     # loads day04 for comparison
    assert (D.DAY, D.NEXT) == (6, "Goal-Gradient Effect"), (D.DAY, D.NEXT)


if __name__ == "__main__":
    fails = 0
    for name, fn in [(k, v) for k, v in globals().items() if k.startswith("test_")]:
        try: fn(); print("PASS", name)
        except Exception as e: fails += 1; print("FAIL", name, "-", e)
    sys.exit(1 if fails else 0)
