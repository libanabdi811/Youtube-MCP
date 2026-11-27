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
- Aim for 40–50 seconds in total (v2 timing below). The first Short ran 68 s; shorter quizzes keep a higher % viewed and loop more.

## v2 optimisations (27 Nov, after the first Short: 431 views / 7 likes / 0 dislikes in ~3 h)
- Timing: `"speed": 1.25, "think": 1.0, "reveal": 1.1`. Intro hook at most ~8 words, spoken in under 3 s,
  e.g. "Name all 8. Most fans fail at 5." Nothing slow before question 1.
- Clues: 2–3 words each so the voice reads them fast; the strongest clue last.
- Question 8 (HOPELESS) should be genuinely hard but fair: it drives "I got 7/8!" comments.
- Outro under 3 s: "Comment your score!" then cut, so the Short loops straight back into the hook.
- Title formula that worked: "Only Real GTA Fans Can Name All 8 🤯 #GTA #Shorts". Keep the challenge + number + emoji,
  but vary the wording and the topic noun (games, cities, cars, GTA 6 facts...).
- Keep one format family (GTA quizzes) so YouTube learns who to show the channel to.

## v3 lessons (27 Nov 17:00, vidIQ data)
- 68 s Who am I? (aa9bZOmfP9I): 650 views in ~10 h, now 65 views/hour, 7 likes, 0 comments, 1.1% engagement.
- 50 s Who am I? part 2 with v2 timing (TSJXgGXX63E): 540 views in 3 h, 270 views/hour, 10 likes, 1 comment, 2.0% engagement.
  => v2 (shorter, faster) is about 4x the views per hour and 2x the engagement. Keep 45–52 s; never go back to 60+.
- The only comment listed all 8 answers with "I think" on the hard ones, so HOPELESS was too easy. Make 7–8 genuinely obscure but fair
  (side characters, spin-off games, small details) so fewer people get 8/8 and more argue in the comments.
- Ask for answers, not just a score: description line "Pause and comment your answers 👇 then check if you were right!"
  Spoken intro can end with "Pause and comment your answers!" when it stays under ~3 s.
- Titles: question form "Can You Name All 8 GTA ...? 🤯 #GTA #Shorts" did best so far.
- The owner replies to comments; keep doing that (it boosts the video).

## Performance check (do this first every run)
For every POSTED video in HISTORY.md from the last 3 days, WebFetch
`https://returnyoutubedislikeapi.com/votes?videoId=VIDEO_ID` (viewCount, likes, dislikes; free, no vidIQ credits).
Write the numbers and the hours since posting into HISTORY.md. Compare views per hour and likes per 100 views between videos;
reuse the topic type, title style and length of the best one, and change what the weakest one did.
If vidiq_balance (free) shows at least 10 credits, instead make ONE vidiq_get_videos_by_ids call with ALL quiz video IDs from the
last 3 days (5 credits total; gives views, likes, comments, views per hour, engagement) — it is more accurate than the free API,
which can be hours out of date. Never call vidiq_video_stats, vidiq_video_comments or vidiq_user_videos from a scheduled run.

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
- AUTOPILOT (owner's instruction, 27 Nov 2026 17:20): the scheduled runs publish on their own, WITHOUT waiting for a yes,
  but only after the independent Reviewer agent passes the video (see "Team" below). At most one quiz per run, two per day.
  If the Reviewer still fails it after one fix, do NOT post: tell the owner what is wrong.

## Team (each scheduled run)
- Lead (the run itself): performance check, picks the topic, writes the config, renders, uploads, records history.
- Reviewer: a SEPARATE agent (Agent tool, general-purpose) that has not seen the writing. Give it the config JSON path, the MP4 path,
  the proposed title/description and this runbook. It must: check every clue and answer is true (WebSearch anything about GTA 6 or
  anything uncertain), check no clue gives away its answer, check the difficulty order, view stills from at least 5 moments
  (ffmpeg -ss T -frames:v 1) for cut-off or overlapping text, confirm 1080x1920, audio, 45–52 s, and title rules
  (max 55 chars, has GTA, no < or >, disclaimer in description). It replies PASS or a list of exact fixes.
- Lead applies the fixes, re-renders, and asks the Reviewer once more. Post only on PASS.

## Upload
1. Push the MP4 to branch `videos`, folder `v/`, date prefix (e.g. `v/2026-11-27_quiz_am.mp4`).
2. vidiq_video_upload with url `https://raw.githubusercontent.com/libanabdi811/Youtube-MCP/videos/v/FILE.mp4` (free).
3. vidiq_social_post_draft_create: YOUTUBE, platformAccountId UC_scPJ-PYyQgFKOgkjACULw, privacyStatus public, categoryId 20,
   title, tags, description + #GTA #GTA6 #Gaming #Shorts #Quiz + disclaimer. No publishAt (posts on approval) unless the owner asks for a time.
4. vidiq_social_post_publish with the draft's postId and revision. Tell the owner it is posted; if YouTube asks for verification, say so.
(Do not call vidiq_user_videos: it costs 5 vidIQ credits and the account is usually near 0.)

## After each run
Append to HISTORY.md: date, slot (AM/PM), title, topic, the 8 answers, and whether it was approved/posted. Push branch `engine`.
