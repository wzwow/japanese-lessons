# Daily Japanese lessons

Interactive Japanese lessons (audio playback, slow mode, 🎤 say-it-back).

## Adding a new lesson
1. Copy `lessons/lesson-3.html` to `lessons/lesson-N.html`, set `const LESSON="lesson-N"`, title, `<h1>`, and the `P` phrase array, and the `V` extra-vocabulary array (5-6 items, `[jp, romaji, en]`; shown in the right sidebar).
2. Generate audio: `python3 make_audio.py lessons/lesson-N.html` (writes `lessons/audio/lesson-N/*.mp3`: phrases `pI*.mp3`, word parts `pI_wJ.mp3`, vocab `vK.mp3`).
3. **Add one line to `NAV` in `nav.js`** (href relative to the repo root), and add a card to `index.html`.
4. Bundle audio: from `lessons/` run `tar czf - audio/lesson-N | base64 -w 76 > ../audio-bundle.b64`, then push; the
   "Unpack audio" GitHub Action decodes it and commits the mp3s.

Every page includes the sidebar with `<script src="nav.js">` (root) or `<script src="../nav.js">` (lessons/). Keep all links relative.

## Making a lesson from the template (Lesson 4 onward)
Lessons from 4 onward follow `plan.html` and are built from `lessons/_template.html`. The page engine is shared; **only the data block between `/*DATA*/` and `/*END DATA*/` changes.**

1. Copy `lessons/_template.html` (or the latest lesson, e.g. `lesson-4.html`) to `lessons/lesson-N.html`.
2. Fill in the data block. Where each part comes from in `plan.html`:
   - `META`: stage, week, lesson number and `total` (42 in Stage 1). Week *n* covers lessons 7n−6 to 7n. Set `review:true` on lessons 7, 14, 21, … ("How the plan works"). A review page shows only the warm-up and quiz.
   - `P` (4–5 new phrases): the week's **Target phrases** table in that stage's week card. Add a usage note to each.
   - `G` (one grammar point: pattern, explanation, 2–3 examples, common mistake): the week's **Grammar** list, one bullet per lesson.
   - `V` (5–6 extra vocab, right sidebar): the week's **Vocab themes**.
   - `D` (4–6 line designer–client dialogue): use today's phrases and recycle 2–3 earlier ones ("Review & spaced repetition", point 3). Lesson 4's sample is in "Lesson page design".
   - `WARM` (3–4 warm-up phrases): earlier phrases from 1, 3, 7, 14 and 30 days back. Use `ref:"lesson-X:pI"` to reuse that lesson's mp3.
   - `Q` (4–5 quiz items): mix `listen`, `choose`, `particle` and `order` ("Lesson page design" ⑦).
   - `S` (3 speak-back prompts): English prompt plus target Japanese ("Lesson page design" ⑧).
   - For any word written in Latin letters, add a katakana `say` text so the audio reads correctly. Add `"わ"` as the say-text for the particle は.
3. `python3 make_audio.py lessons/lesson-N.html` generates `p*, v*, r*, g*, d*, q*, s*` mp3s in `lessons/audio/lesson-N/`.
4. Add the lesson to `NAV` in `nav.js`, add a card in `index.html`, set the previous lesson's `META.next`, and bump `DONE` and the "Done / Next up" text in `plan.html`.
5. Bundle and push the new audio (see above).

Progress (completed lessons, quiz best scores, warm-up 😊/😐/😕 ratings) is saved in the browser's `localStorage`, so no backend is needed.

**No personalization:** lesson content uses generic sample names (田中, 山田, スミス) and an example country (アメリカ) rather than any real learner's name or location. Notes tell learners to swap in their own.
