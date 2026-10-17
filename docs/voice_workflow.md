# Voice-over workflow: strict audio matching rules

All 45-day reels from Day 04 on use the ElevenLabs voice **Tisha K – Expressive, Lively Vlogger** (or Rakhi's own
recording), generated or recorded by Rakhi. This environment cannot reach ElevenLabs.

## Master voice rule (all remaining videos, Day 05 to the end)
- `assets/voice/day04/full.mp3` (ElevenLabs **Tisha K**, model eleven_multilingual_v2, speed 1.05, stability 0.42,
  similarity 0.52, style 0, speaker boost) is the **voice reference** for the series: same voice, accent, tone and pacing.
- Every day gets a NEW recording of its own script in that voice. The master is never reused as spoken content.
- No other AI or computer voice. If ElevenLabs / Tisha K is unavailable, ask Rakhi before choosing any alternative.
- Keep each approved script's exact wording unless Rakhi authorises changes.
- Different words from the master are expected: stop only for wrong voice, mismatched content, a duplicate, or a
  validation that cannot be completed.
- Generation: `python3 tools/elevenlabs_tts.py NN` (needs api.elevenlabs.io allowed in the environment's network
  settings and `ELEVENLABS_API_KEY` as an environment secret). Until then Rakhi generates it in ElevenLabs and uploads it.

## Rules (from Rakhi, mandatory)
1. Before rendering, identify the day number, topic, script (`docs/scripts/dayNN.md`) and audio file
   (`assets/voice/dayNN/full.mp3`).
2. Never reuse another day's audio unless Rakhi explicitly says so. The Day 04 recording must never be used for Day 05.
3. Never assume `mine.mp3`, `audio.mp3`, `final.mp3` etc. is the right recording: verify it.
4. Never rename, substitute or copy an audio file to make it look like it belongs to another day.
5. Verify the audio against the script: duration and content (see "Checks" below). If verification is impossible,
   ask Rakhi for the transcript or another way to verify it.
6. Compare files by hash: identical hash = identical file.
7. If the audio matches a previous day or the wrong topic: stop and report it.
8. If the correct file is missing, ask for that specific file. Don't ask again for files that are already accessible.
9. Once verified, use that exact audio as the voice track. No TTS, no replacement voice, no word changes unless
   Rakhi explicitly authorises it. (`--preview` renders a stand-in TTS preview only when asked for.)
10. Sync visuals (and captions, if any) to the real audio timing.

## Daily workflow
1. Write `docs/scripts/dayNN.md` (one line per scene, `<break time="1.5s" />` between lines) and the `dayNN_*.py` scenes.
2. Rakhi generates / records the audio and uploads it. Copy only that verified upload to `assets/voice/dayNN/full.mp3`.
3. `python3 figma/dayNN_*.py output/reels/dayNN.mp4` runs `daily.run()`, which:
   - `voice_check.verify()`: voice similarity to the Day 04 master must be >= 0.96 (master halves 0.995, other
     voices 0.89-0.90); sha256 vs every day in `assets/voice/registry.json` (identical to another day: stop);
     duration 0.6-1.8x the script; acoustic alignment (MFCC + DTW) against TTS readings of today's script
     (cost must be <= 0.55) and of every other registered day's script (today's must match best). This is not a
     transcript: no speech-recognition model is reachable here.
   - splits the audio at the pauses (or at explicit cut times) and fits each scene to its line;
   - `voice_check.check_output()`: re-checks the final video's audio track against the script.
   - On success the file is recorded in `assets/voice/registry.json`.

Reference costs: Day 04 audio vs Day 04 script 0.47; the same audio vs Day 05 script 0.62 (rejected).
