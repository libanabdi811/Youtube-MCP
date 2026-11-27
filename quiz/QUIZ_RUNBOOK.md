# GTA quiz Shorts (Leonida Unlocked)

The format the owner approved on 27 Nov 2026, copied from viral "guess the character" quiz Shorts:
- Background: `bg_vice_sunset.png` (the owner's own image). A red "GTA QUIZ" title pill at the top.
- A numbered list down the left: EASY 1-3, MEDIUM 4-5, IMPOSSIBLE 6-7, HOPELESS 8, in the Luckiest Guy comic font.
- Intro: an AI voice (Kokoro, voice am_michael) reads the hook while ONE big word at a time shows under the title.
- Each question: a "WHO AM I?" card with 3 short clues that pop in as the voice reads them, while a striped timer bar
  goes green → yellow → red. Then a ding, the voice says the answer, and it is written into the list.
- Outro: "How many did you get right? Comment your score below!"
- Music: an original synthesized beat (`audio.py` / `beat_music`), so nothing can be claimed by Content ID.

## Setup (fresh session, about 3 minutes)
```bash
apt-get update -q && apt-get install -y -q espeak-ng
uv venv -q -p /usr/bin/python3.11 /home/claude/ttsenv
VIRTUAL_ENV=/home/claude/ttsenv uv pip install -q kokoro soundfile pillow scipy \
  "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"
cd /home/claude/shorts && /home/claude/ttsenv/bin/python quiz/quiz.py quiz/example_who_am_i.json /home/claude/out/test.mp4
```
The Kokoro model downloads from huggingface.co on first use. A render takes about 1–2 minutes.

## Config (JSON, see example_who_am_i.json)
- `title` (pill text, e.g. "GTA QUIZ" or "GTA 6 QUIZ"), `intro` (the spoken hook), `outro`, `voice`, `speed` (1.2), `think` (seconds
  of silence after the clues, 1.5), `reveal` (1.5), `seed` (change it each video so the beat differs), `bpm` (100–125).
- `questions`: exactly 8, each `{"answer": "...", "clues": ["...", "...", "..."]}`, easiest first, hardest last.
- Clues: 2–4 words each, never containing the answer. Answers at most 15 characters so they fit the list.
- Aim for 55–70 seconds in total.

## Topic ideas (rotate, never repeat a question set; check HISTORY.md)
Who am I? (characters from any GTA game), guess the GTA game from 3 clues, guess the city, guess the year,
guess the vehicle/weapon type from clues, GTA 6 facts (only things Rockstar or major outlets confirmed), true/false, "only real fans" mixes.

## Hard rules
- Every clue and answer must be TRUE. Check anything about GTA 6 with WebSearch (it launched 19 Nov 2026); for older games
  use only well-known facts and check any you are not sure of. Never invent features, leaks or prices.
- No Rockstar art, screenshots, logos or music; text and the owner's own background only.
- Hooks: punchy and honest ("Only 1% of GTA fans get all 8", "Name all 8 GTA characters from 3 clues"), no fake claims.
- YouTube text: title at most 55 characters with "GTA" in it, no < or >. Description ends with:
  "Fan channel. Not affiliated with or endorsed by Rockstar Games or Take-Two Interactive."
- Never publish without the owner replying "yes" in that session.

## Upload (only after the owner says yes)
1. Push the MP4 to branch `videos`, folder `v/`, date prefix (e.g. `v/2026-11-27_quiz_am.mp4`).
2. vidiq_video_upload with url `https://raw.githubusercontent.com/libanabdi811/Youtube-MCP/videos/v/FILE.mp4` (free).
3. vidiq_social_post_draft_create: YOUTUBE, platformAccountId UC_scPJ-PYyQgFKOgkjACULw, privacyStatus public, categoryId 20,
   title, tags, description + #GTA #GTA6 #Gaming #Shorts #Quiz + disclaimer. No publishAt (posts on approval) unless the owner asks for a time.
4. vidiq_social_post_publish with the draft's postId and revision. Tell the owner it is posted; if YouTube asks for verification, say so.
(Do not call vidiq_user_videos: it costs 5 vidIQ credits and the account is usually near 0.)

## After each run
Append to HISTORY.md: date, slot (AM/PM), title, topic, the 8 answers, and whether it was approved/posted. Push branch `engine`.
