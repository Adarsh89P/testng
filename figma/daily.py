"""Shared entry point for the daily reels: strict voice-over rules (docs/voice_workflow.md).

  python3 dayNN_*.py OUT             render with the day's verified voice-over (stops if missing / wrong / reused)
  python3 dayNN_*.py OUT --preview   visuals preview with stand-in TTS (only when explicitly asked for)
"""
import os, sys
import engine, voice_check

W, H = 1080, 1920


def vo_path(day):
    return os.path.join(voice_check.ROOT, "assets", "voice", f"day{day:02d}", "full.mp3")


def run(day, topic, scenes, module, out=None, cuts="auto"):
    out = out or sys.argv[1]
    if "--preview" in sys.argv:
        print(f"day{day:02d} PREVIEW with stand-in TTS (not the final voice)")
        d = engine.render(scenes, out, W, H, cap_y=None, voice="hf_beta", lang="hi", natural=False, voice_fx=False)
        print("duration", round(d, 1), "s"); return
    path = vo_path(day)
    try:
        voice_check.verify(day, topic, path, scenes, module)
    except voice_check.VoiceError as e:
        sys.exit(f"STOP: {e}")
    clips = engine.split_audio(path, cuts, n=len(scenes))
    d = engine.render(scenes, out, W, H, cap_y=None, voice="hf_beta", lang="hi", natural=False, voice_fx=False,
                      voice_clips=clips)
    voice_check.check_output(out, scenes, f"day{day:02d}")
    print("duration", round(d, 1), "s ·", out)
