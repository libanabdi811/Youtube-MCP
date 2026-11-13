import sys, os, math, subprocess
import numpy as np, cv2
from engine import *
from videos import (tension_bar, lesson, phone, PHONE_ARM, draw_bubbles, frame_fn, STAND, SIT)
import audio

OUT = '/home/claude/shorts/out2'
os.makedirs(OUT, exist_ok=True)

# ---------- props ----------
def problem_box(img, cx, k, lines):
    if k <= 0.02: return
    w, h = 210 * k, 180 * k
    x0, x1, y0 = cx - w / 2, cx + w / 2, GROUND - h
    poly(img, [(x0, y0), (x1, y0), (x1, GROUND), (x0, GROUND)], (70, 28, 34))
    poly(img, [(x0 + 6, y0 + 6), (x1 - 6, y0 + 6), (x1 - 6, GROUND - 6), (x0 + 6, GROUND - 6)], (138, 44, 56))
    glow(img, (cx, GROUND - h / 2), 200 * k, RED, 0.12 * k)
    for i, tx in enumerate(lines):
        spr = scaled(label_sprite(tx, (255, 236, 236), 30), k)
        blit(img, spr, cx - spr.shape[1] / 2, y0 + h * (0.28 + 0.3 * i) - spr.shape[0] / 2)

def gift(img, p):
    x, y = p['fh']; y -= 30
    poly(img, [(x - 70, y - 60), (x + 70, y - 60), (x + 70, y + 55), (x - 70, y + 55)], (200, 58, 72))
    line(img, (x, y - 60), (x, y + 55), GOLD, 14); line(img, (x - 70, y - 5), (x + 70, y - 5), GOLD, 14)
    circle(img, (x - 18, y - 72), 16, GOLD, 8); circle(img, (x + 18, y - 72), 16, GOLD, 8)

def cup(img, p, t):
    x, y = p['fh']
    poly(img, [(x - 22, y - 34), (x + 22, y - 34), (x + 18, y + 10), (x - 18, y + 10)], (236, 232, 222))
    circle(img, (x + 26, y - 14), 12, (236, 232, 222), 6)
    for i in (-10, 6):
        pts = [(x + i + 6 * math.sin(t * 5 + j * 0.8 + i), y - 44 - j * 12) for j in range(5)]
        for a, b in zip(pts, pts[1:]): line(img, a, b, (150, 150, 160), 3)

def glass(img, pos):
    x, y = pos
    poly(img, [(x - 16, y - 40), (x + 16, y - 40), (x + 12, y + 4), (x - 12, y + 4)], (150, 200, 230))

def broken_heart(img, c, size, crack, a=1.0):
    heart(img, c, size, mixc(RED, (120, 60, 66), clamp(crack)) if crack > 0 else RED, a)
    if crack > 0.02:
        x, y = c; s = size / 32
        pts = [(x, y - 10 * s), (x - 4 * s, y - 3 * s), (x + 4 * s, y + 3 * s), (x - 3 * s, y + 9 * s), (x, y + 14 * s)]
        for p0, p1 in zip(pts, pts[1:]): line(img, p0, p1, (16, 16, 20), max(2, 9 * crack * s))

def doll(img, hand, t, face, mood='flat'):
    person(img, hand[0], y=hand[1] + 90, s=0.34, face=face, mood=mood, front=(40 + 30 * math.sin(t * 6), 10))

def small_label(img, text, t, t0, t1, y, color=GOLD, size=34):
    label(img, text, t, t0, t1, y=y, color=color, size=size)

# ============ B1 Marriage: us vs the problem ============
class B1:
    name = '06_marriage_us_vs_the_problem'; dur = 36.0; bg = 'kitchen'
    hook = "STOP FIGHTING EACH OTHER. *FIGHT THE PROBLEM.*"
    rw = (12.8, 13.8, 12.6, 3.0)
    prog = ['Am', 'F', 'C', 'G']; bpm = 66
    bubbles = [(4.0, 6.0, "YOU SPEND TOO\nMUCH!", (780, STAND), 'say'),
               (6.1, 8.1, "ME?! WHAT\nABOUT YOU?", (300, STAND), 'say'),
               (8.2, 10.0, "THIS IS YOUR\nFAULT!", (780, STAND), 'say'),
               (14.4, 16.6, "THE BILLS ARE\nSCARING ME.", (300, STAND), 'say'),
               (16.7, 18.2, "ME TOO.", (780, STAND), 'say'),
               (20.0, 22.2, "LET'S MAKE\nA PLAN.\nTOGETHER.", (800, STAND), 'say'),
               (22.3, 24.2, "YOU AND ME\nVS. THIS.", (640, STAND), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('thud', 2.7), ('rewind', 12.8), ('whoosh', 13.75), ('whoosh', 18.3),
              ('chime', 26.6), ('whoosh', 27.1)]

    @staticmethod
    def scene(img, t):
        if t < 13.8:
            label(img, 'THE OLD WAY', t, 2.6, 12.8, color=RED)
            tension_bar(img, t, 3.8, 12.8, kf(t, [(4.0, 0.1), (10.0, 0.95)]))
            problem_box(img, 540, back(prog(t, 2.6, 3.0)) * kf(t, [(4.0, 1.0), (10.0, 1.55)]), ['BILLS', 'STRESS'])
            m = 'angry' if t > 4.0 else 'flat'
            person(img, 300, face=1, mood=m, hair=True, dress=True,
                   front=(kf(t, [(6.0, 8), (6.3, 70), (7.9, 70), (8.2, 8)]), 15))
            person(img, 780, face=-1, mood=m, front=(kf(t, [(3.9, 8), (4.2, 80), (9.8, 80), (10.1, 8)]), 10))
            caption(img, 'Bills are piling up.', t, 2.8, 5.6)
            caption(img, 'They fought *each other.* The problem *grew.*', t, 10.2, 13.0)
        else:
            label(img, 'THE BETTER WAY', t, 13.8, 27.0, color=BLUE)
            problem_box(img, 540, kf(t, [(24.0, 1.0), (26.5, 0.5)]), ['BILLS', 'STRESS'])
            wx, ww = walkstate(t, [(18.2, 300), (19.8, 650)])
            wface = 1 if t < 19.9 else -1
            wm = step(t, [(0, 'sad'), (20.2, 'smile')])
            hm = step(t, [(0, 'sad'), (19.9, 'smile')])
            person(img, 800, face=-1, mood=hm, front=(kf(t, [(20.0, 8), (20.6, 58)]), kf(t, [(20.0, 12), (20.6, -30)])))
            person(img, wx, face=wface, mood=wm, hair=True, dress=True, walk=ww)
            pop_heart(img, (725, 600), t, 26.6, 70)
            lesson(img, t, 27.2, 32.6, 28.4, 32.6, "It's not *you vs. me.*", "It's *us vs. the problem.*", 56, 56)
            caption(img, 'What problem will you face *together* this week?', t, 32.8, 40, size=54)

# ============ B2 Husband: small daily love ============
class B2:
    name = '07_better_husband_small_daily_love'; dur = 36.0; bg = 'kitchen'
    hook = "SHE DOESN'T NEED A GRAND GESTURE. SHE NEEDS *THIS.*"
    rw = (12.8, 13.8, 12.6, 2.8)
    prog = ['F', 'C', 'Dm', 'Bb']; bpm = 66
    bubbles = [(4.3, 6.0, "HAPPY\nANNIVERSARY!", (720, STAND), 'say'),
               (6.0, 7.6, "WOW!\nTHANK YOU!", (330, STAND), 'say'),
               (8.6, 10.2, "HOW WAS\nYOUR DAY?", (330, STAND), 'say'),
               (10.3, 11.6, "HMM.", (720, STAND), 'say'),
               (14.4, 16.2, "MORNING,\nLOVE.", (720, STAND), 'say'),
               (17.0, 18.8, "HOW WAS\nYOUR DAY?", (720, STAND), 'say'),
               (19.4, 21.2, "I'M PROUD\nOF YOU.", (720, STAND), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('chime', 6.3), ('whoosh', 7.8), ('rewind', 12.8), ('whoosh', 13.75),
              ('whoosh', 16.8), ('whoosh', 19.2)] + [('tick', 21.6 + i * 0.25) for i in range(10)] + [('chime', 24.8), ('whoosh', 25.5)]

    @staticmethod
    def scene(img, t):
        if t < 13.8:
            label(img, 'ONE BIG DAY', t, 2.6, 7.6, color=GOLD)
            label(img, 'THE OTHER 364 DAYS', t, 7.8, 12.8, color=(170, 170, 176))
            hx, hw = walkstate(t, [(2.6, 1180), (4.2, 720)])
            wm = step(t, [(0, 'flat'), (5.8, 'smile'), (8.0, 'flat'), (10.4, 'sad')])
            person(img, 330, face=1, mood=wm, hair=True, dress=True, headdown=18 if t > 10.4 else 0)
            if t < 7.8:
                p = person(img, hx, face=-1, mood='smile', walk=hw, front=(60, 30))
                gift(img, p)
                if 6.3 <= t < 7.8: heart(img, (330, 600), 50 * back(prog(t, 6.3, 6.7)) * (1 - prog(t, 7.2, 7.8)))
            else:
                p = person(img, 720, face=-1, headdown=22, front=PHONE_ARM)
                phone(img, p['fh'])
            caption(img, "One big moment can't fill *364 empty days.*", t, 10.4, 13.0)
        else:
            label(img, 'SMALL. EVERY DAY.', t, 13.8, 25.4, color=BLUE)
            if t < 21.6:
                d = 1 if t < 16.8 else 2 if t < 19.2 else 3
            else:
                d = int(lerp(4, 365, ei(prog(t, 21.6, 24.2))))
            spr = label_sprite(f'DAY {d}', GOLD, 44)
            blit(img, spr, (W - spr.shape[1]) / 2, 330)
            warm = kf(t, [(14.4, 0.05), (24.4, 0.6)])
            hug = kf(t, [(23.6, 0), (24.4, 1)])
            wx, ww = walkstate(t, [(23.2, 330), (24.2, 470)])
            hx, hw = walkstate(t, [(23.2, 720), (24.2, 600)])
            glow(img, (wx, 950), 260, GOLD, warm * 0.45)
            person(img, wx, face=1, mood='smile' if t > 14.8 else 'flat', hair=True, dress=True, walk=ww,
                   front=(lerp(8, 62, hug), lerp(12, -40, hug)))
            p = person(img, hx, face=-1, mood='smile', walk=hw,
                       front=(lerp(60 if t < 16.6 else 8, 62, hug), lerp(30 if t < 16.6 else 12, -40, hug)))
            if t < 16.6: cup(img, p, t)
            nod = 0
            pop_heart(img, (535, 600), t, 24.8, 75)
            lesson(img, t, 25.6, 31.4, 26.8, 31.4, "Love isn't built in *one big moment.*", "It's built in *small, daily* ones.", 54, 54)
            caption(img, 'What small thing will you do *tomorrow morning?*', t, 31.6, 40, size=54)

# ============ B3 Wife: honour in public ============
GUEST = (112, 112, 118)
class B3:
    name = '08_better_wife_honour_in_public'; dur = 36.0; bg = 'living'
    hook = "THE WAY YOU TALK ABOUT HIM *IN FRONT OF OTHERS...*"
    rw = (12.8, 13.8, 12.6, 4.4)
    prog = ['C', 'Am', 'F', 'G']; bpm = 68
    bubbles = [(5.6, 7.8, "HE CAN'T DO\nANYTHING RIGHT!", (420, STAND), 'say'),
               (7.9, 9.2, "HA HA!", (120, 760), 'say'),
               (8.2, 9.4, "HA!", (960, 760), 'say'),
               (14.2, 16.6, "DON'T WORRY,\nLOVE. HAPPENS\nTO ALL OF US.", (420, STAND), 'say'),
               (16.8, 19.4, "HE'S THE BEST\nTHING THAT EVER\nHAPPENED TO ME.", (420, STAND), 'say'),
               (19.5, 20.8, "AWW!", (120, 760), 'say'),
               (21.0, 22.8, "AND YOU\nTO ME.", (660, STAND), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('crack', 4.1), ('rewind', 12.8), ('whoosh', 13.75), ('chime', 23.0), ('whoosh', 23.5)]

    @staticmethod
    def scene(img, t):
        for gx, gf in ((120, 1), (960, -1)):
            person(img, gx, s=0.82, face=gf, col=GUEST, mood='smile' if (7.9 <= t < 9.4 or t > 19.4) else 'flat')
        # glass spill (both versions start after spill)
        hp = None
        if t < 13.8:
            label(img, 'DINNER WITH FRIENDS', t, 2.6, 5.4, color=(170, 170, 176))
            label(img, 'IN FRONT OF EVERYONE', t, 5.6, 12.8, color=RED)
            shrink = kf(t, [(8.0, 1.0), (10.0, 0.9)])
            col = mixc(WHITE, DIM, prog(t, 8.0, 10.0))
            hm = step(t, [(0, 'smile'), (4.1, 'flat'), (8.0, 'sad')])
            hp = person(img, 660, s=shrink, face=-1, col=col, mood=hm, headdown=kf(t, [(8.0, 0), (9.0, 25)]),
                        front=(50, 40) if t < 4.0 else (8, 12))
            wm = step(t, [(0, 'smile'), (5.6, 'angry'), (7.9, 'smile')])
            person(img, 420, face=1, hair=True, dress=True, mood=wm, front=(kf(t, [(5.5, 8), (5.8, 70), (7.6, 70), (7.9, 8)]), 15))
            if t < 4.0: glass(img, hp['fh'])
            else:
                q = prog(t, 4.0, 4.4)
                gy = lerp(hp['fh'][1], GROUND - 4, ei(q))
                glass(img, (hp['fh'][0] - 30 * q, gy))
                if q >= 1:
                    for dx in (-60, -30, 4, 30): circle(img, (hp['fh'][0] - 30 + dx, GROUND + 8), 9, (110, 160, 210))
            caption(img, 'He makes a *small mistake.*', t, 2.8, 5.4)
            caption(img, 'Every joke in public *chips away at respect.*', t, 9.6, 13.0)
        else:
            label(img, 'TRY AGAIN', t, 13.8, 23.4, color=BLUE)
            tall = kf(t, [(17.0, 1.0), (19.4, 1.06)])
            glow(img, (660, 900), 280, GOLD, kf(t, [(17.0, 0), (19.4, 0.35)]))
            hp = person(img, 660, s=tall, face=-1, mood=step(t, [(0, 'flat'), (14.6, 'smile')]))
            for dx in (-90, -60, -26, 0): circle(img, (600 + dx, GROUND + 8), 9, (110, 160, 210))
            glass(img, (600, GROUND - 4))
            person(img, 420, face=1, hair=True, dress=True, mood='smile', front=(kf(t, [(14.2, 8), (14.6, 60)]), 10))
            pop_heart(img, (540, 600), t, 23.0, 70)
            lesson(img, t, 23.6, 29.4, 24.8, 29.4, 'Correct *in private.*', 'Honour *in public.*', 60, 60)
            caption(img, 'And it goes *both ways.*', t, 29.6, 32.4)
            caption(img, 'Do you *honour* your partner in public?', t, 32.6, 40, size=56)

# ============ B4 Parenting: kids copy your marriage ============
class B4:
    name = '09_parenting_they_learn_by_watching'; dur = 37.0; bg = 'living'
    hook = "YOUR KIDS LEARN LOVE BY *WATCHING YOU.*"
    rw = (12.8, 13.8, 12.6, 3.0)
    prog = ['Em', 'C', 'G', 'D']; bpm = 64
    bubbles = [(3.4, 5.2, "YOU NEVER\nLISTEN!", (640, STAND), 'say'),
               (5.3, 7.0, "WHY WOULD I?!", (300, STAND), 'say'),
               (8.0, 10.0, "YOU NEVER\nLISTEN!", (540, 890), 'say'),
               (14.2, 16.0, "I FEEL\nUNHEARD.", (640, STAND), 'say'),
               (16.1, 18.4, "I'M SORRY.\nI'M LISTENING\nNOW.", (300, STAND), 'say'),
               (20.4, 22.6, "I'M SORRY.\nI'M LISTENING.", (540, 890), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('whoosh', 7.3), ('rewind', 12.8), ('whoosh', 13.75), ('whoosh', 19.8),
              ('chime', 22.8), ('whoosh', 25.2)]

    @staticmethod
    def scene(img, t):
        later1 = 7.4 <= t < 13.8
        later2 = t >= 19.8
        if t < 13.8:
            label(img, 'WHAT THEY SEE', t, 2.6, 7.2, color=RED)
            label(img, 'LATER...', t, 7.4, 12.8, color=(170, 170, 176))
        else:
            label(img, 'TRY AGAIN', t, 13.8, 19.6, color=BLUE)
            label(img, 'LATER...', t, 19.8, 25.2, color=BLUE)
        if not later1 and not later2:
            angry = t < 13.8 and t > 3.3
            wx, ww = walkstate(t, [(18.4, 300), (19.4, 410)])
            hx, hw = walkstate(t, [(18.4, 640), (19.4, 560)])
            hold = kf(t, [(19.0, 0), (19.5, 1)]) if t >= 13.8 else 0
            person(img, wx, face=1, hair=True, dress=True, walk=ww, mood='angry' if angry and t > 5.2 else ('smile' if t > 18.4 else 'flat'),
                   front=(lerp(8, 40, hold), 10))
            person(img, hx, face=-1, walk=hw, mood='angry' if angry else ('sad' if 14 < t < 18 else ('smile' if t > 18.4 else 'flat')),
                   front=(lerp(8, 40, hold), 10) if t >= 13.8 else (kf(t, [(3.3, 8), (3.6, 80), (5.0, 80), (5.3, 8)]), 10))
            covering = t < 13.8 and t > 3.6
            person(img, 900, s=0.58, kid=True, face=-1, mood='sad' if covering else ('smile' if t > 18.4 else 'flat'),
                   front=(150, -60) if covering else (8, 10), rear=(-150, 60) if covering else (-6, 10),
                   headdown=12 if covering else 0)
        else:
            k = person(img, 540, s=0.58, kid=True, face=1, mood='flat' if later1 else 'smile',
                       front=(75, 20), rear=(-75, 20))
            mood = 'angry' if later1 else 'smile'
            doll(img, k['fh'], t, -1, mood); doll(img, k['rh'], t + 1, 1, mood)
            if later2: pop_heart(img, (540, 800), t, 22.8, 50)
            caption(img, 'Children copy *what they see.*', t, 9.8, 13.0)
            caption(img, 'Same child. *Different lesson.*', t, 22.2, 25.2)
        lesson(img, t, 25.4, 31.0, 26.6, 31.0, "Your marriage is their *first love story.*", 'Make it one *worth copying.*', 50, 48)
        caption(img, 'What are your kids *learning* from you?', t, 31.2, 40, size=56)

# ============ B5 Lesson: the real apology ============
class B5:
    name = '10_relationship_the_real_apology'; dur = 36.0; bg = 'plain'
    hook = "\"SORRY\" ISN'T ALWAYS *AN APOLOGY.*"
    rw = (12.8, 13.8, 12.6, 5.6)
    prog = ['Dm', 'Bb', 'F', 'C']; bpm = 62
    bubbles = [(5.8, 7.8, "SORRY IF YOU\nWERE UPSET.", (740, STAND), 'say'),
               (7.9, 9.6, "...CAN WE\nMOVE ON NOW?", (740, STAND), 'say'),
               (14.2, 16.2, "I WAS WRONG\nTO SAY THAT.", (740, STAND), 'say'),
               (16.3, 18.4, "I HURT YOU,\nAND I'M SORRY.", (740, STAND), 'say'),
               (18.5, 20.8, "WHAT CAN I DO\nTO MAKE IT\nRIGHT?", (740, STAND), 'say'),
               (21.0, 23.0, "THANK YOU\nFOR SAYING\nTHAT.", (340, STAND), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('crack', 8.0), ('rewind', 12.8), ('whoosh', 13.75), ('tick', 14.2),
              ('tick', 16.3), ('tick', 18.5), ('chime', 24.4), ('whoosh', 25.0)]

    @staticmethod
    def scene(img, t):
        if t < 13.8:
            label(img, 'THE NEXT MORNING', t, 2.6, 5.6, color=(170, 170, 176))
            label(img, 'APOLOGY #1', t, 5.7, 12.8, color=RED)
            crack = kf(t, [(2.6, 0.6), (8.0, 0.6), (9.0, 1.0)])
            wf = 1 if t < 10.0 else -1
            w = person(img, 340, face=wf, mood='sad', hair=True, dress=True, headdown=15 if t < 10 else 25)
            person(img, 740, face=-1, mood='flat', front=(8, 12) if t < 7.9 else (40, -20))
            broken_heart(img, (w['chest'][0], w['chest'][1] + 10), 60, crack)
            caption(img, 'He said something *hurtful* last night.', t, 2.8, 5.6)
            caption(img, "That's not an apology. *That's an exit.*", t, 10.0, 13.0)
        else:
            label(img, 'APOLOGY #2', t, 13.8, 24.6, color=BLUE)
            for txt, a, y in (('1. OWN IT', 14.2, 1300), ('2. NAME THE HURT', 16.3, 1350), ('3. REPAIR IT', 18.5, 1400)):
                label(img, txt, t, a, 24.4, y=y, color=GOLD, size=32)
            crack = kf(t, [(14.2, 0.6), (16.3, 0.4), (18.5, 0.2), (21.0, 0.0)])
            wx, ww = walkstate(t, [(23.2, 340), (24.2, 480)])
            hx, hw = walkstate(t, [(23.2, 740), (24.2, 600)])
            hug = kf(t, [(23.8, 0), (24.3, 1)])
            w = person(img, wx, face=1, mood=step(t, [(0, 'sad'), (21.0, 'smile')]), hair=True, dress=True, walk=ww,
                       headdown=kf(t, [(14.2, 15), (18.5, 0)]), front=(lerp(8, 62, hug), lerp(12, -40, hug)))
            person(img, hx, face=-1, mood=step(t, [(0, 'sad'), (21.0, 'smile')]), walk=hw,
                   front=(lerp(8, 62, hug), lerp(12, -40, hug)))
            if t < 23.6:
                broken_heart(img, (w['chest'][0], w['chest'][1] + 10), 60, crack)
            pop_heart(img, (540, 600), t, 24.4, 80)
            lesson(img, t, 25.0, 31.0, 26.2, 31.0, "A real apology doesn't just say sorry.", 'It *owns it,* names it, and *repairs it.*', 50, 50)
            caption(img, 'Which part is *hardest* for you?', t, 31.2, 40)

VIDEOS = {'6': B1, '7': B2, '8': B3, '9': B4, '10': B5}

def build(key):
    V = VIDEOS[key]
    vid = render(V.name, V.dur, frame_fn(V), OUT)
    ev = list(V.events) + [('pop', b[0]) for b in V.bubbles]
    duck = [(V.rw[0], V.rw[1], 0.25)] if V.rw else []
    a = audio.mix(V.dur, V.prog, ev, V.bpm, int(key) * 11, duck) * 0.708
    wav = os.path.join(OUT, V.name + '.wav'); audio.write_wav(wav, a)
    tmp = os.path.join(OUT, V.name + '.tmp.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', vid, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', tmp], check=True)
    os.replace(tmp, os.path.join(OUT, V.name + '.mp4'))
    os.remove(vid); os.remove(wav)
    print('done', V.name)

def stills(key, times):
    V = VIDEOS[key]; f = frame_fn(V)
    for t in times:
        cv2.imwrite(f'{OUT}/still_{int(key):02d}_{t:05.1f}.jpg', cv2.cvtColor(f(t), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 85])

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        stills(sys.argv[2], [float(x) for x in sys.argv[3:]])
    else:
        build(sys.argv[1])
