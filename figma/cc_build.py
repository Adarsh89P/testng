"""Build word-timed captions (CC) for a reel whose narration came from our Kokoro pipeline.

Each line is given as phrases: (devanagari_phrase_for_timing, roman_hinglish_caption). The line's audio is
re-synthesised with the same voice/speed, located in the source audio by cross-correlation, and split into
phrases proportionally to each phrase's own synthesized length. Output: JSON list of
{"t0","t1","text"} phrase cues in source-video time.

usage: python3 cc_build.py SOURCE.mp4 OUT.json
"""
import sys, json, subprocess
import numpy as np
from kokoro_onnx import Kokoro
from engine import M

SR = 24000
VOICE, SPEED = "hf_beta", 1.05
MIN_DURS = [4.6, 6.0, 7.0, 6.0, 6.0, 8.0, 5.5, 6.0]     # reel 5 scene min_dur values (original render)
PAD = 0.6

LINES = [
    [("यू एक्स डिज़ाइनर हो?", "UX designer ho?"), ("तो बताओ,", "Toh batao,"), ("लेबर इल्यूज़न क्या है?", "Labor Illusion kya hai?")],
    [("चलो समझते हैं,", "Chalo samajhte hain,"), ("हमारे लाइव ऐप ज़ोमैटो से।", "hamare live app Zomato se."),
     ("फ्राइडे रात,", "Friday raat,"), ("नौ बजकर सैंतालीस मिनट।", "9:47 PM."),
     ("रोहन ने बिरयानी ऑर्डर की।", "Rohan ne biryani order ki."), ("डिलीवरी,", "Delivery,"), ("तीस मिनट।", "30 minute.")],
    [("अब दो ऐप्स सोचो।", "Ab do apps socho."), ("दोनों में इंतज़ार तीस मिनट।", "Dono mein intezaar 30 minute."),
     ("ऐप ए में सिर्फ लिखा है,", "App A mein sirf likha hai,"), ("ऑर्डर प्लेस्ड।", "\"Order placed.\""),
     ("ऐप बी में राइडर मैप पर चलता दिखता है।", "App B mein rider map par chalta dikhta hai.")],
    [("ऐप ए में रोहन बार बार ऐप खोलता है।", "App A mein Rohan baar baar app kholta hai."),
     ("कुछ बदलता ही नहीं।", "Kuch badalta hi nahi."), ("तीस मिनट,", "30 minute,"), ("एक घंटे जैसे लगते हैं।", "ek ghante jaise lagte hain.")],
    [("ऐप बी में वही तीस मिनट,", "App B mein wahi 30 minute,"), ("पर हर स्टेप दिखता है।", "par har step dikhta hai."),
     ("खाना बन रहा है,", "Khana ban raha hai,"), ("राइडर निकल गया।", "rider nikal gaya."), ("रोहन शांत है।", "Rohan shaant hai.")],
    [("यही है लेबर इल्यूज़न।", "Yahi hai Labor Illusion."),
     ("हार्वर्ड बिज़नेस स्कूल की रिसर्च कहती है,", "Harvard Business School ki research kehti hai,"),
     ("जब यूज़र को काम होता दिखता है,", "jab user ko kaam hota dikhta hai,"),
     ("तो इंतज़ार कम खलता है,", "toh intezaar kam khalta hai,"),
     ("और वो सर्विस को ज़्यादा वैल्यू देता है।", "aur woh service ko zyada value deta hai.")],
    [("इसीलिए ज़ोमैटो में हर स्टेप का अपडेट आता है,", "Isiliye Zomato mein har step ka update aata hai,"),
     ("और राइडर लाइव दिखता है।", "aur rider live dikhta hai.")],
    [("तो अगली बार डिज़ाइन में खाली स्पिनर मत दिखाओ,", "Toh agli baar design mein khaali spinner mat dikhao,"),
     ("प्रोग्रेस दिखाओ।", "progress dikhao."), ("अगला यूएक्स लॉ जानने के लिए फॉलो करो।", "Agla UX law jaanne ke liye follow karo.")],
]

_K = None


def synth(text):
    global _K
    if _K is None: _K = Kokoro(f"{M}/kokoro-v1.0.onnx", f"{M}/voices-v1.0.bin")
    s, _ = _K.create(text, voice=VOICE, speed=SPEED, lang="hi")
    return s.astype(np.float32)


def phrase_cues(phrases, start, dur):
    """Split [start, start+dur] across phrases proportionally to their own synthesized lengths."""
    lens = np.array([len(synth(d)) for d, _ in phrases], float)
    w = lens / lens.sum(); out, t = [], start
    for (d, r), f in zip(phrases, w):
        out.append({"t0": round(t, 3), "t1": round(t + f * dur, 3), "text": r}); t += f * dur
    return out


def main():
    src, out = sys.argv[1], sys.argv[2]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.float32)
    cues, t0 = [], 0.25
    for i, phrases in enumerate(LINES):
        full = synth(" ".join(d for d, _ in phrases))
        L = len(full) / SR
        guess = t0 + 0.1
        # refine start by cross-correlating the first second of the line against the source
        seg = full[:SR]; best, bo = -1e9, guess
        for o in np.arange(guess - 0.3, guess + 0.3, 0.005):
            j = int(o * SR)
            if j < 0 or j + len(seg) > len(audio): continue
            v = float(np.dot(seg, audio[j:j + len(seg)]))
            if v > best: best, bo = v, o
        print(f"line {i + 1}: predicted {guess:.3f}s, matched {bo:.3f}s, length {L:.2f}s")
        cues += phrase_cues(phrases, bo, L)
        t0 += max(L + PAD, MIN_DURS[i])
    json.dump(cues, open(out, "w"), ensure_ascii=False, indent=1)
    print(len(cues), "cues ->", out)


if __name__ == "__main__":
    main()
