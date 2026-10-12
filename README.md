# Daily Japanese lessons

Interactive Japanese lessons (audio playback, slow mode, 🎤 say-it-back).

## Adding a new lesson
1. Copy `lessons/lesson-3.html` to `lessons/lesson-N.html`, set `const LESSON="lesson-N"`, title, `<h1>`, and the `P` phrase array.
2. Generate audio: `python3 make_audio.py lessons/lesson-N.html` (writes `lessons/audio/lesson-N/*.mp3`).
3. **Add one line to `NAV` in `nav.js`** (href relative to the repo root), and add a card to `index.html`.
4. Bundle audio: from `lessons/` run `tar czf - audio/lesson-N | base64 -w 76 > ../audio-bundle.b64`, then push; the
   "Unpack audio" GitHub Action decodes it and commits the mp3s.

Every page includes the sidebar with `<script src="nav.js">` (root) or `<script src="../nav.js">` (lessons/). Keep all links relative.
