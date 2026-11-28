# Quiz Shorts history (newest last; never repeat a question set)

## 2026-11-27 — prototypes (made in chat, not posted)
- "GTA 6 QUIZ" multiple choice: Leonida / 19 Nov 2026 / 13 years after GTA 5.
- "Who am I?" GTA characters (example_who_am_i.json): Lucia, CJ, Trevor, Michael, Tommy Vercetti, Niko Bellic, Lester, Claude.
  The owner liked this one. It was not uploaded by the schedule; it can be posted as the first video if the owner asks.
- POSTED 2026-11-27 06:39 UK: "Only Real GTA Fans Can Name All 8 🤯 #GTA #Shorts" — the Who am I? set above (original beat),
  https://www.youtube.com/watch?v=aa9bZOmfP9I (v/2026-11-27_quiz_who_am_i.mp4). Do not reuse these 8 characters as a set.

## 2026-11-27 AM — "Name These 8 GTA Games From 3 Clues" (not posted yet, awaiting owner's yes)
- Topic: guess the GTA game from 3 clues (card "WHICH GAME?"). Config: quiz/2026-11-27_am_which_game.json, seed 42.
- Answers: GTA 6, GTA 5, San Andreas, Vice City, GTA 4, GTA 3, Chinatown Wars, London 1969.
- Engine: added `card` config key (card header text) and auto-shrink of long list answers so they never hit the clue card.

## 2026-11-27 AM (scheduled run) — "Can You Name All 8 GTA Characters? 🤯 #GTA #Shorts" — POSTED
- Topic: Who am I? part 2 (card "WHO AM I?"), v2 timing (speed 1.25, think 0.9, reveal 1.0), 49.9 s. Config: quiz/2026-11-27_am_who_am_i_2.json, seed 7319.
- Answers: Franklin, Jason, Big Smoke, Roman, Lance Vance, Catalina, Ken Rosenberg, Toni Cipriani.
- Jason facts (GTA 6 lead, ex-Army, Lucia's partner) checked with WebSearch.
- POSTED 2026-11-27 ~11:20 UK: https://www.youtube.com/watch?v=TSJXgGXX63E (video ID TSJXgGXX63E, v/2026-11-27_quiz_am_who_am_i_2.mp4).

## 2026-11-27 PM — "Can You Name These 8 GTA Games? 🎮 #GTA #Shorts" (re-cut of the AM which-game quiz with v2 timing, 54 s)
- Config quiz/2026-11-27_pm_which_game_v2.json (shorter clues). POSTED (scheduled public at 18:00 UK): https://www.youtube.com/watch?v=PtSGW_AYH6M (video ID PtSGW_AYH6M, v/2026-11-27_quiz_which_game_v2.mp4).
  Not a new question set: same 8 games as the AM which-game draft, which will not be posted separately.

## 2026-11-27 PM (scheduled run) — "Can You Name These 8 GTA Characters? 🤯 #GTA #Shorts" — POSTED
- Topic: Who am I? part 3 (card "WHO AM I?"), v2 timing, 50.8 s, background bg/neon_ocean_drive.jpg (rotated off vice_sunset). Config: quiz/2026-11-27_pm_who_am_i_3.json, seed 9184, bpm 116.
- Answers: Lamar, Sweet, Brucie, Johnny Klebitz, Boobie Ike, Victor Vance, Huang Lee, Zero.
- Improvements tried: back to the characters format (best vph); harder 6–8 (VCS, Chinatown Wars, SA side character Zero) so fewer get 8/8;
  one GTA 6 side character (Boobie Ike, checked with WebSearch); outro asks for answers ("Comment your answers!"); new background.
- Reviewer agent: PASS first time.
- POSTED 2026-11-27 ~19:50 UK: https://www.youtube.com/watch?v=yULEZZz_Y-g (video ID yULEZZz_Y-g, v/2026-11-27_quiz_pm_who_am_i_3.mp4).

## Performance
- 2026-11-27 09:52 UK, aa9bZOmfP9I (68 s Who am I?): 431 views, 7 likes, 0 dislikes ~3 h after posting (~140 views/h, 1.6 likes per 100 views).
- 2026-11-27 10:50 UK: performance check could not run (returnyoutubedislikeapi.com fetch blocked by a permission prompt nobody answered). Used last numbers: characters format = best so far, so repeated it with a new set.
- 2026-11-27 17:00 UK (vidIQ): aa9bZOmfP9I 650 views / 7 likes / 0 comments / 65 vph (68 s); TSJXgGXX63E 540 views / 10 likes / 1 comment / 270 vph (50 s, v2). v2 wins clearly.
- 2026-11-27 19:45 UK (vidIQ): aa9bZOmfP9I 650 views / 7 likes / 0 comments / 50 vph (13 h); TSJXgGXX63E 923 views / 16 likes / 2 comments / 185 vph (5.7 h, 1.7 likes/100);
  PtSGW_AYH6M (which-game, 55 s) 20 views / 0 likes / 0 comments / 20 vph (1.7 h) — weak start. Characters format with 50 s wins; game-guess format paused.
- 2026-11-28 08:44 UK (vidIQ): TSJXgGXX63E 1,022 views / 16 likes / 2 comments; aa9bZOmfP9I 683 / 8 / 0; PtSGW_AYH6M (games) 288 / 9 / 0 (3.1% engagement, best like rate);
  yULEZZz_Y-g (characters part 3) 3 views / 0 likes in 13 h = stuck. Likely: 4 uploads in 13 h, posted <2 h after PtSGW, near-duplicate title/look of TSJXgGXX63E.
  Owner decided the v4 rules in QUIZ_RUNBOOK.md (8 h spacing, new title angle, new look, rotate topic type, leave stuck videos up, never repost).
