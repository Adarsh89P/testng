# Project notes for Claude

- Daily "45 Days · 45 UX Laws" reels for Design with Rakhi (@rakhi.ux) live in `figma/dayNN_*.py` (Day 02 visual pattern).
- **Voice-over: follow `docs/voice_workflow.md` strictly.** Each day needs its own verified recording at
  `assets/voice/dayNN/full.mp3`; never reuse another day's audio, never substitute TTS without explicit permission.
  Render through `daily.run()` so `voice_check` enforces hash / duration / content checks.
- No ElevenLabs anywhere in the pipeline. Day 04 Tisha K mp3 = master reference only (never reused, never cloned).
  New voice-overs: `--generate` (offline Indic-TTS + FreeVC24 toward the rights-cleared reference in
  `assets/voice/reference.json`) or Rakhi's own recording. Never switch to another voice without asking Rakhi.
