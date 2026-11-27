"""Character-quiz Short generator (format: numbered EASY/MEDIUM/IMPOSSIBLE/HOPELESS list,
word-by-word voice intro, picture + shrinking timer bar, answer written into the list).
Usage: python quiz/quiz.py config.json out.mp4   (see quiz/QUIZ_RUNBOOK.md)"""
import json, math, os, subprocess, sys
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

cfg = json.load(open(sys.argv[1])); OUT = sys.argv[2]
W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import audio
from audio import lowpass, reverb
FONT = os.path.join(HERE, "LuckiestGuy.ttf")
def F(s): return ImageFont.truetype(FONT, s)
WORK = os.path.join(os.path.dirname(os.path.abspath(OUT)), "_work"); os.makedirs(WORK, exist_ok=True)

# ---------- voice ----------
from kokoro import KPipeline
pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
VOICE, SPEED, SR = cfg.get("voice", "am_michael"), cfg.get("speed", 1.1), 24000
def tts(text):
    auds, words, off = [], [], 0.0
    for r in pipe(text, voice=VOICE, speed=SPEED):
        a = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        for tk in (r.tokens or []):
            if tk.start_ts is not None and any(c.isalnum() for c in tk.text):
                words.append((tk.text, off + tk.start_ts, off + (tk.end_ts or tk.start_ts + 0.3)))
        auds.append(a); off += len(a) / SR
    return np.concatenate(auds), words

intro_audio, intro_words = tts(cfg["intro"])
INTRO = len(intro_audio) / SR + 0.4
Qs = cfg["questions"]
ans_audio = [tts(q["answer"])[0] for q in Qs]
clue_audio = [tts(". ".join(q["clues"]) + ".")[0] for q in Qs]
REVEAL = cfg.get("reveal", 1.8)
TIMERS = [len(c) / SR + 0.3 + cfg.get("think", 2.0) for c in clue_audio]
STARTS = []; acc = 0.0
for tm in TIMERS: STARTS.append(acc); acc += tm + REVEAL
QTOTAL = acc
OUTRO = 3.0
outro_audio, outro_words = tts(cfg.get("outro", "How many did you get? Comment below!"))
OUTRO = max(OUTRO, len(outro_audio) / SR + 0.6)
TOTAL = INTRO + QTOTAL + OUTRO

# ---------- static background ----------
def cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))
bg = cover(Image.open(os.path.join(HERE, cfg.get("background", "bg_vice_sunset.png"))).convert("RGB"), W, H)
bg = ImageEnhance.Color(bg).enhance(1.15)

LEVELS = [("EASY:", (60, 230, 60), [0, 1, 2]), ("MEDIUM:", (245, 235, 30), [3, 4]),
          ("IMPOSSIBLE:", (235, 25, 25), [5, 6]), ("HOPELESS:", (40, 140, 255), [7])]
WORD_COLORS = [(255, 235, 40), (60, 230, 255), (255, 255, 255), (255, 235, 40), (120, 255, 90)]

def txt(d, s, xy, size, fill, stroke=7, anchor="lm"):
    d.text(xy, s, font=F(size), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

# list layout positions
rows = []; y = 480
for name, col, idxs in LEVELS:
    rows.append(("lvl", name, col, y)); y += 96
    for i in idxs: rows.append(("num", i, None, y)); y += 92
    y += 8

# pictures
def load_pic(q, i):
    p = q.get("image")
    if p and os.path.exists(p):
        im = Image.open(p).convert("RGB")
    else:  # placeholder mystery card
        im = Image.new("RGB", (600, 760), (25, 20, 45)); d = ImageDraw.Draw(im)
        for k in range(760): d.line([(0, k), (600, k)], fill=(40 + k // 20, 20, 70 + k // 12))
        d.ellipse([200, 120, 400, 330], fill=(8, 6, 15)); d.rounded_rectangle([130, 340, 470, 760], radius=90, fill=(8, 6, 15))
        txt(d, "?", (300, 250), 150, (255, 235, 40), 8, "mm")
    im = cover(im, 600, 760) if im.width / im.height < 1.2 else cover(im, 600, 760)
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width, im.height], radius=40, fill=255)
    card = Image.new("RGBA", (im.width + 16, im.height + 16), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([0, 0, card.width - 1, card.height - 1], radius=48, fill=(255, 255, 255, 255))
    card.paste(im, (8, 8), m)
    return card
CW, CH = 560, 640
def wrap(text, font, maxw, d):
    out, cur = [], ""
    for w in text.split():
        t2 = (cur + " " + w).strip()
        if d.textlength(t2, font=font) <= maxw: cur = t2
        else: out.append(cur); cur = w
    out.append(cur); return out
def clue_card(qi, tl, timer):
    q = Qs[qi]; card = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, CW - 1, CH - 1], radius=44, fill=(255, 255, 255, 255))
    d.rounded_rectangle([8, 8, CW - 9, CH - 9], radius=38, fill=(18, 10, 40, 235))
    d.rounded_rectangle([8, 8, CW - 9, 140], radius=38, fill=(240, 20, 85, 255)); d.rectangle([8, 100, CW - 9, 140], fill=(240, 20, 85, 255))
    txt(d, "WHO AM I?", (CW // 2, 78), 70, (255, 255, 255), 6, "mm")
    n = len(q["clues"]); span = max(timer - cfg.get("think", 2.0), 0.5)
    y = 200; f = F(60)
    for k, cl in enumerate(q["clues"]):
        tk = span * k / n
        if tl < tk: break
        pp = ease((tl - tk) / 0.2)
        lines = wrap(cl, f, CW - 110, d)
        col = (255, 235, 40) if k % 2 == 0 else (60, 230, 255)
        txt(d, "-", (40, y + 34), 60, col, 5, "lm")
        for ln in lines:
            d.text((80 + int((1 - pp) * 60), y + 34), ln, font=f, fill=(255, 255, 255) if pp > 0.5 else (200, 200, 200), anchor="lm", stroke_width=5, stroke_fill=(0, 0, 0)); y += 70
        y += 40
    return card

def base_frame(t, revealed_upto, partial=None):
    im = bg.copy().convert("RGBA"); d = ImageDraw.Draw(im)
    # title pill
    title = cfg.get("title", "GTA 6 QUIZ")
    d.rounded_rectangle([150, 120, W - 150, 255], radius=26, fill=(240, 20, 85), outline=(255, 255, 255), width=4)
    txt(d, title, (W // 2, 192), 96, (255, 255, 255), 8, "mm")
    return im, d

def draw_list(d, revealed_upto, partial=None):
    for kind, a, col, yy in rows:
        if kind == "lvl": txt(d, a, (45, yy), 84, col, 8)
        else:
            s = f"{a + 1})-"
            if a < revealed_upto: s += " " + Qs[a]["answer"]
            elif partial is not None and a == partial[0]: s += " " + Qs[a]["answer"][:partial[1]]
            txt(d, s, (70, yy), 76, (255, 255, 255), 8)

def bar(d, frac, t):
    x0, x1, y0, y1 = 220, W - 220, 300, 352
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=(235, 235, 235), outline=(255, 255, 255), width=4)
    col = (40, 200, 60) if frac > 0.6 else ((250, 210, 20) if frac > 0.3 else (240, 40, 40))
    if frac > 0.02:
        xe = x0 + 6 + int((x1 - x0 - 12) * frac)
        d.rounded_rectangle([x0 + 6, y0 + 6, xe, y1 - 6], radius=20, fill=col)
        lt = tuple(min(255, c + 60) for c in col)
        off = int(t * 120) % 60
        for sx in range(x0 - 60 + off, xe, 60):  # moving stripes
            d.polygon([(max(sx, x0 + 6), y1 - 8), (min(sx + 20, xe), y0 + 8), (min(sx + 40, xe), y0 + 8), (max(sx + 20, x0 + 6), y1 - 8)], fill=lt)

def render(fi):
    t = fi / FPS
    if t < INTRO:
        im, d = base_frame(t, 0); draw_list(d, 0)
        cur = [w for w in intro_words if w[1] <= t]
        if cur:
            k = len(cur) - 1; w = cur[-1]
            p = ease((t - w[1]) / 0.12)
            txt(d, w[0].upper().strip(".,!?"), (W // 2, 360), int(92 * (0.7 + 0.3 * p)), WORD_COLORS[k % len(WORD_COLORS)], 8, "mm")
        return im.convert("RGB")
    tq = t - INTRO
    qi = len(Qs) if tq >= QTOTAL else max(i for i in range(len(Qs)) if STARTS[i] <= tq)
    if qi >= len(Qs):
        to = tq - QTOTAL
        im, d = base_frame(t, len(Qs)); draw_list(d, len(Qs))
        cur = [w for w in outro_words if w[1] <= to]
        if cur:
            w = cur[-1]; txt(d, w[0].upper().strip(".,!?"), (W // 2, 360), 92, WORD_COLORS[(len(cur) - 1) % 5], 8, "mm")
        return im.convert("RGB")
    tl = tq - STARTS[qi]; TIMER = TIMERS[qi]
    if tl < TIMER:
        im, d = base_frame(t, qi)
        bar(d, 1 - tl / TIMER, t); lst = (qi, None)
    else:
        tr = tl - TIMER
        n = len(Qs[qi]["answer"]); chars = min(n, int(n * tr / 0.45) + 1)
        im, d = base_frame(t, qi, (qi, chars)); lst = (qi, (qi, chars))
    # picture on the right with pop-in
    p = ease(tl / 0.25)
    c = clue_card(qi, tl, TIMER)
    s = 0.6 + 0.4 * p
    c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))))
    cx, cy = 790, 1000
    im.alpha_composite(c, (cx - c.width // 2, cy - c.height // 2))
    d = ImageDraw.Draw(im); draw_list(d, lst[0], lst[1])
    return im.convert("RGB")

# ---------- video ----------
silent = os.path.join(WORK, "silent.mp4")
pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                       "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
for fi in range(int(TOTAL * FPS)): pr.stdin.write(render(fi).tobytes())
pr.stdin.close(); pr.wait()

# ---------- audio: voice + pops ----------
va = np.zeros(int(TOTAL * SR) + SR)
def put(t, a, g=1.0): i = int(t * SR); va[i:i + len(a)] += g * a[:len(va) - i]
put(0.15, intro_audio)
tt = np.arange(int(SR * 0.12)) / SR
pop = 0.5 * np.sin(2 * np.pi * (500 + 1500 * tt / 0.12) * tt) * np.exp(-tt * 25)
td = np.arange(int(SR * 0.6)) / SR
ding = 0.35 * (np.sin(2 * np.pi * 988 * td) + 0.5 * np.sin(2 * np.pi * 1480 * td)) * np.exp(-td * 6)
for i in range(len(Qs)):
    b = INTRO + STARTS[i]; tm = TIMERS[i]
    put(b, pop); put(b + 0.3, clue_audio[i]); put(b + tm, ding); put(b + tm + 0.05, ans_audio[i])
put(INTRO + QTOTAL + 0.2, outro_audio)
voice = os.path.join(WORK, "voice.wav"); sf.write(voice, np.clip(va, -1, 1), SR)
# original synthesized beat (royalty-free), from neon.beat_music
SRM = audio.SR
def beat_music(dur, bpm=118, seed=3, notes=(45, 45, 48, 43)):
    n = int(dur * SRM); out = np.zeros(n); beat = 60 / bpm
    r = np.random.default_rng(seed)
    def add(sig, at):
        s = int(at * SRM); e = min(n, s + len(sig))
        if s < n: out[s:e] += sig[:e - s]
    tt = np.arange(int(0.35 * SRM)) / SRM
    kick = np.sin(2 * np.pi * np.cumsum(55 + 120 * np.exp(-tt * 30)) / SRM) * np.exp(-tt * 9) * 0.9
    sn_t = np.arange(int(0.25 * SRM)) / SRM
    snare = (lowpass(r.standard_normal(len(sn_t)), 6000) * np.exp(-sn_t * 18) * 0.35 + np.sin(2 * np.pi * 190 * sn_t) * np.exp(-sn_t * 25) * 0.3)
    hh_t = np.arange(int(0.05 * SRM)) / SRM
    hat = np.diff(np.concatenate([[0], r.standard_normal(len(hh_t))])) * np.exp(-hh_t * 80) * 0.08
    nb = int(dur / beat) + 1
    for b in range(nb):
        add(kick, b * beat)
        if b % 2 == 1: add(snare, b * beat)
        add(hat, b * beat + beat / 2)
        root = notes[(b // 8) % len(notes)]
        for k, semi in enumerate((0, 12, 7, 12)):
            f = audio.hz(root + semi + 12)
            L = int(beat / 4 * SRM * 0.9); st = np.arange(L) / SRM
            saw = 2 * ((st * f) % 1) - 1
            add(lowpass(saw, 1800) * np.exp(-st * 10) * 0.12, b * beat + k * beat / 4)
        f = audio.hz(root); L = int(beat * SRM); st = np.arange(L) / SRM
        add(np.sin(2 * np.pi * f * st) * (1 - np.exp(-st * 60)) * np.exp(-st * 2) * 0.35, b * beat)
    out = reverb(out, 1.2, 0.15, seed)
    return out

music = os.path.join(WORK, "music.wav")
audio.write_wav(music, beat_music(TOTAL + 1, bpm=cfg.get("bpm", 112), seed=cfg.get("seed", 3)))
fc = f"[1:a]volume={cfg.get('music_volume', 0.22)},afade=t=out:st={TOTAL - 2:.2f}:d=2,atrim=0:{TOTAL:.2f}[m];[2:a]volume=1.6[v];[m][v]amix=inputs=2:normalize=0[a]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-stream_loop", "-1", "-i", music, "-i", voice,
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", OUT], check=True)
print("done", round(TOTAL, 1), "s")
