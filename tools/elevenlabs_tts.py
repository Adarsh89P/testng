"""Generate a day's voice-over with the ElevenLabs Tisha K voice, same settings as the Day 04 master.

Needs network access to api.elevenlabs.io and the env var ELEVENLABS_API_KEY (Rakhi's account; set it as an
environment secret, never commit it). Reads the lines from docs/scripts/dayNN.md (the fenced block) unchanged.

  python3 tools/elevenlabs_tts.py 5            -> assets/voice/day05/full.mp3
"""
import json, os, re, sys, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
API = "https://api.elevenlabs.io/v1"
VOICE_NAME = "Tisha K"
# Settings decoded from the master file name "..._pvc_sp105_s42_sb52_se0_b_m2.mp3"
MODEL = "eleven_multilingual_v2"
SETTINGS = {"speed": 1.05, "stability": 0.42, "similarity_boost": 0.52, "style": 0.0, "use_speaker_boost": True}


def call(path, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r: return r.read()


def voice_id():
    vid = os.environ.get("TISHA_VOICE_ID")
    if vid: return vid
    for v in json.loads(call("/voices"))["voices"]:
        if v["name"].lower().startswith(VOICE_NAME.lower()): return v["voice_id"]
    sys.exit(f"'{VOICE_NAME}' is not in this ElevenLabs account's voices; add it from the Voice Library or set TISHA_VOICE_ID")


def script_text(day):
    md = open(os.path.join(ROOT, "docs", "scripts", f"day{day:02d}.md"), encoding="utf-8").read()
    m = re.search(r"```\n(.*?)\n```", md, re.S)
    if not m: sys.exit("no fenced script block in the day's script file")
    return m.group(1).strip()


if __name__ == "__main__":
    day = int(sys.argv[1])
    out = os.path.join(ROOT, "assets", "voice", f"day{day:02d}", "full.mp3")
    if os.path.exists(out): sys.exit(f"{out} already exists; not overwriting")
    audio = call(f"/text-to-speech/{voice_id()}?output_format=mp3_44100_128",
                 {"text": script_text(day), "model_id": MODEL, "voice_settings": SETTINGS})
    os.makedirs(os.path.dirname(out), exist_ok=True); open(out, "wb").write(audio)
    print("wrote", out, len(audio), "bytes; now run the day's script so voice_check verifies it")
