# Voice-over workflow (offline, no ElevenLabs)

The pipeline never connects to ElevenLabs: no API key, no network access, no subscription.

## Voices
- **Master reference:** `assets/voice/day04/full.mp3`, the Day 04 Tisha K recording Rakhi supplied. It is kept
  unchanged (hash in `assets/voice/registry.json`, checked by the tests) and is **never** reused as another day's
  voice-over. Tisha K is a third-party voice licensed through ElevenLabs, so it is **not** used as a cloning target.
- **Clone reference (for generated voice-overs):** a recording of a voice we have the rights to (Rakhi's own voice,
  or a voice licensed for cloning), declared in `assets/voice/reference.json`:
  `{"file": "assets/voice/reference/rakhi.wav", "owner": "Rakhi", "rights": "own voice"}` (30-60 s, clean, no music).
  `voice_gen.reference()` refuses a reference without stated rights, or one identical to any day's voice-over.

## Each day
1. Script: `SCENES[*].spoken` in `figma/dayNN_*.py` (the approved wording; `docs/scripts/dayNN.md` mirrors it).
2. Voice-over, one of:
   - **Generated offline:** `python3 figma/dayNN_*.py OUT --generate`, which runs `tools/voice_clone.py` in
     `/home/user/venv-tts`: AI4Bharat Indic-TTS (Hindi female) speaks each line unchanged, then FreeVC24 (MIT)
     converts it to the clone reference's voice. Writes `assets/voice/dayNN/full.wav` (+ `.json` provenance).
     About 2 min of CPU for a 1-minute script.
   - **Recorded / supplied:** Rakhi uploads that day's own recording, saved as `assets/voice/dayNN/full.mp3`.
3. `daily.run()` verifies, then renders:
   - sha256 vs every registered day: identical to another day: stop;
   - voice similarity to the series voice (clone reference if configured, else the Day 04 master) >= 0.96;
   - duration 0.6-1.8x the script; content: MFCC+DTW alignment to TTS readings of today's script (<= 0.55) and better
     than any other registered day's script (acoustic check, not a transcript);
   - splits at the pauses, fits each scene to its line, renders, and re-checks the final video's audio track.
4. No stand-in TTS in a final video. `--preview` is for visual previews only, when asked.

## Rules (from Rakhi)
Never reuse another day's audio; never trust a file name (`mine.mp3` etc.) without verification; never rename or
substitute files across days; compare by hash; stop and report on duplicates, wrong voice or wrong topic; ask only for
files that are genuinely missing; keep each script's exact wording; sync visuals to the real audio.

## Tests
`python3 tests/test_voice_pipeline.py`: no ElevenLabs in runtime code, master untouched, duplicate / re-encoded master
rejected for Day 05, master refused as clone reference, reference must state rights.

## Setup (new session)
`INDIC=1 bash scripts/setup.sh` installs the venv, Indic-TTS and the FreeVC24 + WavLM weights (GitHub-hosted, ~2.6 GB).
