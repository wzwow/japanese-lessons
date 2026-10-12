#!/usr/bin/env python3
"""Generate neural Japanese audio for a lesson page.
After generating audio, add the lesson to NAV in nav.js and a card in index.html (see README.md).
Usage: python3 make_audio.py lesson-N.html  [--voice ja-JP-NanamiNeural] [--slow -35%]
Reads `const P=[...]` from the page (needs node) and writes to audio/<lesson-name>/:
  p{i}.mp3 (phrase, normal), p{i}_slow.mp3 (phrase, slow), p{i}_w{j}.mp3 (word part j).
i, j are 0-based indexes into P and P[i].parts.  Requires: pip install edge-tts gTTS  (edge-tts preferred; gTTS used if edge fails)
"""
import argparse, asyncio, json, os, re, subprocess
import edge_tts
from gtts import gTTS

def load_phrases(html):
    s = open(html, encoding="utf-8").read()
    m = re.search(r"const P=(\[.*?\]);\s*\n", s, re.S)
    return json.loads(subprocess.check_output(["node", "-e", f"console.log(JSON.stringify({m.group(1)}))"]))

EDGE_OK = True
async def tts(text, path, voice, rate):
    """Try Microsoft Edge neural TTS; if the service refuses (e.g. 403), fall back to Google TTS (gTTS)."""
    global EDGE_OK
    if EDGE_OK:
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(path); return "edge"
        except Exception as e:
            print("edge-tts failed, switching to gTTS:", str(e)[:80]); EDGE_OK = False
    gTTS(text, lang="ja", slow=rate.startswith("-") and rate != "-10%").save(path); return "gtts"

async def main():
    ap = argparse.ArgumentParser(); ap.add_argument("html")
    ap.add_argument("--voice", default="ja-JP-NanamiNeural"); ap.add_argument("--slow", default="-35%")
    ap.add_argument("--force", action="store_true"); a = ap.parse_args()
    name = os.path.splitext(os.path.basename(a.html))[0]
    out = os.path.join(os.path.dirname(os.path.abspath(a.html)), "audio", name); os.makedirs(out, exist_ok=True)
    jobs = []
    for i, p in enumerate(load_phrases(a.html)):
        jobs += [(p["jp"], f"p{i}.mp3", "+0%"), (p["jp"], f"p{i}_slow.mp3", a.slow)]
        jobs += [(w[0], f"p{i}_w{j}.mp3", "-10%") for j, w in enumerate(p["parts"])]
    for text, fn, rate in jobs:
        path = os.path.join(out, fn)
        if a.force or not os.path.exists(path):
            eng = await tts(text, path, a.voice, rate); print("wrote", path, eng, text)
    print(len(jobs), "files in", out)

asyncio.run(main())
