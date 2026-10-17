# Project notes for Claude

- Daily "45 Days · 45 UX Laws" reels for Design with Rakhi (@rakhi.ux) live in `figma/dayNN_*.py` (Day 02 visual pattern).
- **Voice-over: follow `docs/voice_workflow.md` strictly.** Each day needs its own verified recording at
  `assets/voice/dayNN/full.mp3`; never reuse another day's audio, never substitute TTS without explicit permission.
  Render through `daily.run()` so `voice_check` enforces hash / duration / content checks.
- Master voice: the Day 04 Tisha K recording is the voice reference for every remaining video; each day needs a new
  Tisha K recording of its own script (`tools/elevenlabs_tts.py`). Never switch voices without asking Rakhi.
