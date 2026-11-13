# Home & Heart Stories — daily Shorts runbook

Channel: @HomeAndHeartStories (YouTube channel ID UC_scPJ-PYyQgFKOgkjACULw)
Repo: libanabdi811/Youtube-MCP. Branch `engine` = this code. Branch `videos` = rendered MP4s (folder `v/`).

## Pipeline
1. `git clone --depth 1 -b engine https://github.com/libanabdi811/youtube-mcp /home/claude/shorts`
2. Write `/home/claude/shorts/videos_dayN.py` with 5 new video classes, copying the
   structure of `videos2.py` (B1..B5). Reuse helpers from `engine.py` / `videos.py`
   (person, bubbles, caption, lesson, label, tension_bar, pop_heart, props, rewind).
   OUT dir must be `/home/claude/shorts/out_<date>`.
3. Render stills at the busiest moments of each video, look at them, fix overlaps
   (captions wrap at ~980px: keep lesson lines short, size 46–56).
4. Render: `python3 videos_dayN.py <key>` for each (max 2–3 in parallel; 2 CPUs).
5. Push MP4s to branch `videos` under `v/` (clone that branch separately, depth 1),
   then import each into vidIQ with `vidiq_video_upload` url =
   `https://raw.githubusercontent.com/libanabdi811/Youtube-MCP/videos/v/<file>.mp4`
6. `vidiq_social_post_draft_create` one draft per video: YouTube destination,
   platformAccountId UC_scPJ-PYyQgFKOgkjACULw, privacyStatus public, categoryId 22,
   title, tags, text = description + hashtags, publishAt today 09:00/12:00/15:00/18:00/21:00 Europe/London.
7. Ask the user for approval. Only after they reply yes: `vidiq_social_post_publish`
   for each, then confirm with `vidiq_user_videos` (privacyStatus private + scheduledPublishAt).
8. Append the topics to TOPICS.md on branch `engine` and push.

## Content rules
- 5 per day: Marriage advice, Better husband, Better wife, Family & parenting, Relationship lesson.
- Hook in first 2 s; story; lesson; question CTA. 30–40 s. Never blame one gender.
- No invented statistics or expert quotes. No repeated topics (check TOPICS.md).
- YouTube rejects < or > in titles, descriptions and tags: never use them (no arrows).
- Style: dark scenes, white stick figures, speech bubbles, gold/red/blue accents, synthesized music.

## VIRAL FORMAT v2 (use this from 2026-11-13; old format underperformed)
Use `viral.py` (frame_fn_v2 / build_v2; example class `Phone2AM`) instead of the old frame_fn.
- **Length 20–28 s.** Shorter = more full watches and loops. No dead time.
- **Frame 1 = the drama, not a title card.** Open mid-moment (a phone buzzing, a slammed door, a shout). Never a dimmed intro card.
- **Persistent hook banner** at the top for the whole video (`banner = 'LINE ONE. / *PAYOFF LINE.*'`). Curiosity gap: tease the twist without lying.
- **A twist or reveal by ~40% of the runtime**: the obvious assumption is wrong (e.g. the 2 AM text was her therapist). Honest, not cheap clickbait; never cheating/abuse bait.
- **Camera**: punch-in on whoever speaks (cam keyframes 1.25–1.35x), wide shot for reactions, one short shake on the impact moment.
- **Bubbles 1.5–2.3 s each**, max 3 short lines. Every 2–3 s something changes on screen.
- **Ending ≤ 8 s**: one lesson line + one smaller line + a *debate question* ("Would you have reacted like him?"); questions that people answer in comments beat generic CTAs.
- **Titles**: ≤ 55 chars, curiosity + emotion, mirror the banner (e.g. "Her phone lit up at 2 AM. He saw the name.").
- Rotate formats: twist reveal, "which one are you?" split-screen, POV, "3 words that…", before/after.
- Check performance in TOPICS.md each run: copy what got the most views, drop what didn't.
