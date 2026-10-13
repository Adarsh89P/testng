# YoutubeAutomation2

Video pipeline for a **new Hinglish YouTube channel** (format to be decided from reference image).
Earlier work (The Broke Brain, What If India) lived in the separate "Youtubeautomation" chat.

## Setup (fresh cloud session)
```bash
bash scripts/setup.sh
```
Installs ffmpeg, Devanagari + display fonts, Python libs, the offline Kokoro TTS model and the rembg model.

## Toolchain
| Need | Tool | Notes |
|---|---|---|
| Voiceover | Kokoro (offline, `kokoro-onnx`) | Hindi voices `hf_alpha`, `hf_beta` (female), `hm_omega`, `hm_psi` (male). Write the script in Devanagari, English words included (e.g. "शॉक"), `lang="hi"`. |
| Frames / text | Pillow with raqm | Devanagari shaping verified. Fonts in `assets/fonts` (Mukta/Hind/Baloo2 for Hindi, Anton/Bebas/Poppins for English). |
| Video | ffmpeg, moviepy, OpenCV | 1080x1920 Shorts or 1920x1080 long-form |
| Cutouts | rembg (u2net) | background removal for images |
| Audio edits | pydub, soundfile | |

## Network limits in this environment
Blocked by egress policy: Microsoft Edge TTS, Hugging Face, Pexels, Pixabay, ElevenLabs, OpenAI.
GitHub and PyPI work. Stock footage/music must come from the user, connectors, or be generated.
