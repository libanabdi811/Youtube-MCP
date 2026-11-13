import sys, os, math, subprocess
import numpy as np, cv2
from engine import *
import audio

OUT = '/home/claude/shorts/out'
os.makedirs(OUT, exist_ok=True)
STAND = 668; SIT = 792

# ---------- shared props ----------
def tension_bar(img, t, t0, t1, fill):
    a = win(t, t0, t1, 0.3)
    if a <= 0: return
    spr = label_sprite('TENSION', (170, 170, 176), 28)
    blit(img, spr, (W - spr.shape[1]) / 2, 1296, a)
    x0, x1, y = 330, 750, 1350
    over = img.copy()
    cv2.line(over, (x0, y), (x1, y), (54, 54, 60), 18, cv2.LINE_AA)
    if fill > 0.01:
        col = mixc(GOLD, RED, clamp(fill * 1.3))
        cv2.line(over, (x0, y), (int(lerp(x0, x1, fill)), y), col, 18, cv2.LINE_AA)
    img[:] = (img * (1 - a) + over * a).astype(np.uint8)

CRACK = [(540, 1250), (528, 1290), (552, 1330), (534, 1380), (552, 1400)]
def crack(img, k):
    if k <= 0: return
    n = k * (len(CRACK) - 1)
    for i in range(int(math.ceil(n))):
        f = clamp(n - i)
        a, b = CRACK[i], CRACK[i + 1]
        line(img, a, (lerp(a[0], b[0], f), lerp(a[1], b[1], f)), (200, 70, 78), 6)

def bags(img, p):
    for hnd in (p['fh'], p['rh']):
        x, y = hnd
        poly(img, [(x - 26, y + 6), (x + 26, y + 6), (x + 30, y + 70), (x - 30, y + 70)], (186, 160, 124))
        line(img, (x - 10, y + 8), (x, y - 4), (150, 128, 98), 4); line(img, (x + 10, y + 8), (x, y - 4), (150, 128, 98), 4)

def wrench(img, p):
    x, y = p['fh']
    line(img, (x, y), (x + 8, y - 70), (170, 174, 184), 10)
    circle(img, (x + 9, y - 78), 15, (170, 174, 184)); circle(img, (x + 13, y - 86), 7, (24, 25, 30))

def flower(img, p, face):
    x, y = p['fh']
    line(img, (x, y + 10), (x + face * 6, y - 60), (90, 150, 100), 6)
    for i in range(5):
        a = i / 5 * 2 * math.pi
        circle(img, (x + face * 6 + 13 * math.cos(a), y - 70 + 13 * math.sin(a)), 11, RED)
    circle(img, (x + face * 6, y - 70), 8, GOLD)

def paper(img, p, up=True):
    x, y = p['fh']
    if up: y -= 40
    poly(img, [(x - 44, y - 34), (x + 44, y - 34), (x + 44, y + 34), (x - 44, y + 34)], (245, 245, 240))
    circle(img, (x + 28, y - 18), 9, GOLD)
    for dx in (-18, 4):
        circle(img, (x + dx, y - 8), 6, (60, 110, 200))
        line(img, (x + dx, y - 2), (x + dx, y + 18), (60, 110, 200), 3)
    heart(img, (x - 7, y + 22), 10, RED)

def album(img, p):
    x, y = p['fh']
    poly(img, [(x - 46, y - 40), (x + 46, y - 40), (x + 46, y + 26), (x - 46, y + 26)], (140, 98, 68))
    poly(img, [(x - 36, y - 30), (x - 2, y - 30), (x - 2, y + 2), (x - 36, y + 2)], (220, 214, 200))
    poly(img, [(x + 6, y - 30), (x + 38, y - 30), (x + 38, y + 2), (x + 6, y + 2)], (220, 214, 200))

def orb(img, p, k):
    c = p['chest']
    glow(img, c, 70 + 70 * k, GOLD, 0.45 * k)
    circle(img, c, 6 + 8 * clamp(k, 0, 1.5), mixc((80, 70, 40), GOLD, clamp(k)))

def lesson(img, t, a0, a1, b0, b1, A, B, bsize=50, asize=50, bpath=POPB, bcol=WHITE):
    sa = rich_sprite(A, POPB, asize, WHITE, GOLD)
    caption(img, A, t, a0, a1, 1400, asize)
    caption(img, B, t, b0, b1, 1400 + sa.shape[0] - 44, bsize, bcol, bpath)

PHONE_ARM = (22, 98)

# ============ VIDEO 1 ============
class V1:
    name = '01_marriage_5_second_pause'; dur = 36.0; bg = 'kitchen'
    hook = 'ONE HABIT *QUIETLY SAVES* MARRIAGES'
    rw = (13.4, 14.4, 13.2, 3.2)
    prog = ['Am', 'F', 'C', 'G']; bpm = 64
    bubbles = [(3.6, 6.3, "YOU FORGOT\nAGAIN.", (360, STAND), 'say'),
               (7.0, 9.2, "YOU ALWAYS\nNAG!", (700, STAND), 'say'),
               (9.3, 11.4, "I ALWAYS\nNAG?!", (360, STAND), 'say'),
               (14.6, 16.7, "YOU FORGOT\nAGAIN.", (360, STAND), 'say'),
               (16.8, 19.9, "PAUSE.\nBREATHE.", (720, STAND), 'think'),
               (20.0, 22.0, "YOU'RE RIGHT.\nI'M SORRY.", (700, STAND), 'say'),
               (22.1, 24.1, "WHAT CAN\nI DO?", (700, STAND), 'say'),
               (24.3, 26.3, "...I'M JUST\nTIRED TOO.", (360, STAND), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('whoosh', 6.5), ('crack', 10.6), ('whoosh', 11.6), ('rewind', 13.4),
              ('whoosh', 14.35)] + [('tick', 16.9 + i * 0.6) for i in range(5)] + [('chime', 27.6), ('whoosh', 28.3)]

    @staticmethod
    def scene(img, t):
        if t < 14.4:
            label(img, '11:47 PM', t, 2.6, 6.3, color=(170, 170, 176))
            label(img, 'VERSION 1: REACT', t, 6.6, 13.4, color=RED)
            tension_bar(img, t, 6.8, 13.4, kf(t, [(7.0, 0.08), (9.2, 0.5), (11.4, 0.94)]))
            crack(img, prog(t, 10.6, 11.4))
            wx, ww = walkstate(t, [(11.5, 360), (12.6, 290)])
            hx, hw = walkstate(t, [(11.5, 700), (12.6, 780)])
            wmood = step(t, [(0, 'flat'), (9.2, 'angry'), (11.5, 'sad')])
            hmood = step(t, [(0, 'flat'), (7.0, 'angry'), (11.5, 'sad')])
            hd = 18 if t > 11.5 else 0
            wf = person(img, wx, face=1 if t < 11.5 else -1, mood=wmood, hair=True, dress=True, walk=ww, headdown=hd,
                        front=(kf(t, [(9.3, 8), (9.6, 55), (11.2, 55), (11.5, 8)]), kf(t, [(9.3, 12), (9.6, 50), (11.2, 50), (11.5, 12)])))
            person(img, hx, face=-1 if t < 11.5 else 1, mood=hmood, walk=hw, headdown=hd,
                   front=(kf(t, [(6.9, 8), (7.2, 80), (9.0, 80), (9.3, 8)]), kf(t, [(6.9, 12), (7.2, 10), (9.0, 10), (9.3, 12)])))
            caption(img, 'A long day. *One small mistake.*', t, 2.8, 6.2)
            caption(img, 'Two tired people. *Zero winners.*', t, 11.8, 13.6)
        else:
            label(img, 'VERSION 2: PAUSE', t, 14.4, 28.2, color=BLUE)
            tension_bar(img, t, 14.4, 28.0, kf(t, [(14.6, 0.08), (16.6, 0.36), (19.9, 0.36), (24.5, 0.03)]))
            wx, ww = walkstate(t, [(26.2, 360), (27.3, 482)])
            hx, hw = walkstate(t, [(26.2, 700), (27.3, 582)])
            hug = kf(t, [(27.0, 0), (27.5, 1)])
            wmood = step(t, [(0, 'flat'), (24.3, 'sad'), (26.3, 'smile')])
            hmood = step(t, [(0, 'flat'), (26.0, 'smile')])
            if 16.9 <= t < 19.9:
                glow(img, (hx - 30, 810), 190, BLUE, 0.16 + 0.1 * math.sin((t - 16.9) * 4))
            person(img, wx, face=1, mood=wmood, hair=True, dress=True, walk=ww,
                   front=(lerp(8, 62, hug), lerp(12, -40, hug)), headdown=kf(t, [(24.2, 0), (24.6, 14), (26.2, 14), (26.6, 0)]))
            person(img, hx, face=-1, mood=hmood, walk=hw, eyes_closed=16.9 <= t < 19.9,
                   front=(lerp(8, 62, hug), lerp(12, -40, hug)))
            if 16.9 <= t < 19.9:
                i = int((t - 16.9) / 0.6); lt = (t - 16.9) - i * 0.6
                spr = label_sprite(str(5 - i), GOLD, 96)
                s2 = scaled(spr, 0.8 + 0.3 * eo(lt / 0.25))
                blit(img, s2, 900 - s2.shape[1] / 2, 840 - s2.shape[0] / 2, 1 - sm(prog(lt, 0.4, 0.6)))
            pop_heart(img, (530, 600), t, 27.6, 80)
            lesson(img, t, 28.4, 32.8, 29.8, 32.8, "You don't need to win *the argument.*", 'You need to win *each other.*', 50)
            lesson(img, t, 33.0, 40, 33.4, 40, 'Try the *5-second pause* tonight.',
                   'What helps you calm down before you reply?', 40, 52, POPM, (190, 190, 196))

# ============ VIDEO 2 ============
class V2:
    name = '02_better_husband_just_listen'; dur = 37.0; bg = 'living'
    hook = "SHE DIDN'T NEED A SOLUTION. SHE NEEDED *YOU.*"
    rw = (13.0, 14.0, 12.8, 4.8)
    prog = ['Dm', 'Bb', 'F', 'C']; bpm = 62
    WS, HS = 420, 700
    bubbles = [(5.0, 7.1, "TODAY WAS\nSO HARD...", (330, STAND), 'say'),
               (7.2, 9.1, "JUST QUIT\nTHEN.", (700, SIT), 'say'),
               (9.2, 10.6, "FIXED IT.", (720, SIT), 'think'),
               (14.2, 16.2, "TODAY WAS\nSO HARD...", (330, STAND), 'say'),
               (16.7, 19.0, "COME HERE.\nTELL ME\nEVERYTHING.", (700, SIT), 'say'),
               (19.9, 22.2, "MY MANAGER\nYELLED AT ME\nIN FRONT OF\nEVERYONE.", (420, SIT), 'say'),
               (22.3, 24.0, "THAT'S NOT\nOKAY.", (700, SIT), 'say'),
               (24.1, 25.9, "I FELT\nSO SMALL.", (420, SIT), 'say'),
               (26.0, 28.0, "I'M HERE.\nI'M LISTENING.", (700, SIT), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('whoosh', 10.4), ('rewind', 13.0), ('whoosh', 13.95), ('chime', 28.2),
              ('whoosh', 28.5)]

    @staticmethod
    def scene(img, t):
        if t < 13.9:
            label(img, '6:30 PM', t, 2.6, 6.0, color=(170, 170, 176))
            wx, ww = walkstate(t, [(2.5, -90), (4.8, 330), (10.4, 330), (12.6, -130)])
            col = mixc(WHITE, DIM, prog(t, 9.3, 10.3))
            person(img, wx, face=1 if t < 10.4 else -1, mood='sad', hair=True, dress=True, walk=ww, col=col,
                   headdown=18 if t < 9.3 else 28)
            hm = 'smile' if 9.2 <= t < 10.6 else 'flat'
            p = person(img, 700, face=-1, sitk=1, mood=hm, headdown=22, front=PHONE_ARM)
            phone(img, p['fh'])
            caption(img, 'She comes home after a *hard day.*', t, 2.8, 6.0)
            caption(img, 'He offered a solution. She needed *a listener.*', t, 10.6, 13.2)
        else:
            label(img, 'TRY AGAIN', t, 14.0, 28.2, color=BLUE)
            wx, ww = walkstate(t, [(18.3, 330), (19.3, 420)])
            sk = kf(t, [(19.0, 0), (19.7, 1)])
            warm = kf(t, [(23.5, 0), (28.0, 0.55)])
            if warm > 0: glow(img, (480, 960), 260, GOLD, warm * 0.5)
            wm = step(t, [(0, 'sad'), (26.4, 'smile')])
            person(img, wx, face=1, mood=wm, hair=True, dress=True, walk=ww, sitk=sk,
                   headdown=kf(t, [(19.4, 18), (19.9, 6)]), lean=kf(t, [(27.6, 0), (28.4, 16)]))
            down = prog(t, 16.0, 16.6)
            nod = 5 * math.sin(t * 7) if (22.3 <= t < 24 or 26 <= t < 28) else 0
            p = person(img, 700, face=-1, sitk=1, mood='flat' if t < 16.6 else 'smile', headdown=lerp(22, 0, down),
                       front=(lerp(PHONE_ARM[0], 30, down), lerp(PHONE_ARM[1], 20, down)), nod=nod)
            if down < 1:
                phone(img, p['fh'])
            else:
                phone(img, (790, 1100), on=False)
            pop_heart(img, (560, 760), t, 28.2, 70)
            lesson(img, t, 28.6, 34.0, 30.0, 34.0, 'Sometimes listening *is* the solution.',
                   'Try asking: "Do you want advice, or should I just listen?"', 42, 50, POPM, (200, 200, 206))
            caption(img, 'Husbands, *when did you learn this?*', t, 34.2, 40)

# ============ VIDEO 3 ============
class V3:
    name = '03_better_wife_appreciation'; dur = 36.0; bg = 'home'
    hook = "HE DIDN'T STOP CARING. HE STOPPED *FEELING SEEN.*"
    rw = (15.0, 16.0, 14.8, 2.8)
    prog = ['C', 'G', 'Am', 'F']; bpm = 68
    bubbles = [(4.4, 6.2, "I GOT EVERYTHING\nON THE LIST!", (420, STAND), 'say'),
               (6.3, 7.9, "FINALLY.", (820, SIT), 'say'),
               (8.6, 10.0, "I FIXED\nTHE SHELF.", (420, STAND), 'say'),
               (10.1, 11.6, "ABOUT TIME.", (820, SIT), 'say'),
               (13.2, 14.9, "WHY DON'T YOU\nTRY ANYMORE?", (820, SIT), 'say'),
               (16.2, 17.8, "I GOT EVERYTHING\nON THE LIST!", (420, STAND), 'say'),
               (17.9, 19.8, "THANK YOU.\nI NOTICED.", (820, SIT), 'say'),
               (20.8, 22.0, "I FIXED\nTHE SHELF.", (420, STAND), 'say'),
               (22.1, 23.6, "YOU'RE SO\nGOOD AT THIS.", (820, SIT), 'say'),
               (25.0, 26.6, "THESE ARE\nFOR YOU.", (580, STAND), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('whoosh', 8.2), ('whoosh', 11.8), ('rewind', 15.0), ('whoosh', 15.95),
              ('whoosh', 20.6), ('whoosh', 23.8), ('chime', 26.8), ('whoosh', 27.5)]

    @staticmethod
    def scene(img, t):
        if t < 15.9:
            label(img, 'DAY 1', t, 2.6, 8.0); label(img, 'DAY 30', t, 8.2, 11.6); label(img, 'DAY 90', t, 11.8, 15.0)
            hx, hw = walkstate(t, [(2.6, 140), (4.4, 420)])
            hm = step(t, [(0, 'smile'), (7.0, 'flat'), (10.2, 'sad')])
            ok = kf(t, [(2.6, 1.0), (6.6, 1.0), (7.4, 0.6), (10.2, 0.6), (11.0, 0.3), (12.2, 0.3), (13.0, 0.05)])
            front = (8, 12) if t < 8.1 or t >= 11.8 else (40, 70)
            p = person(img, hx, face=1, mood=hm, walk=hw, headdown=0 if t < 11.8 else 20, front=front)
            if t < 8.1: bags(img, p)
            elif t < 11.8: wrench(img, p)
            orb(img, p, ok)
            w = person(img, 820, face=-1, sitk=1, hair=True, mood='flat', headdown=22 if t < 13.0 else 0, front=PHONE_ARM)
            phone(img, w['fh'])
            caption(img, "Effort that's never noticed... *slowly fades.*", t, 11.9, 15.2)
        else:
            label(img, 'DAY 1', t, 16.0, 20.5, color=BLUE); label(img, 'DAY 30', t, 20.6, 23.6, color=BLUE)
            label(img, 'DAY 90', t, 23.8, 27.4, color=BLUE)
            sk = kf(t, [(24.4, 1), (25.0, 0)])
            wm = 'flat' if t < 17.9 else 'smile'
            w = person(img, 820, face=-1, sitk=sk, hair=True, dress=sk < 0.5, mood=wm, headdown=22 if t < 17.5 else 0,
                       front=PHONE_ARM if t < 17.5 else (10, 14))
            if t < 17.5: phone(img, w['fh'])
            hx, hw = walkstate(t, [(23.8, 420), (24.9, 580)])
            ok = kf(t, [(16, 1.0), (18.2, 1.0), (19.2, 1.6), (22.2, 1.6), (23.0, 2.1)])
            if t < 20.5: front = (8, 12)
            elif t < 23.7: front = (40, 70)
            else: front = (kf(t, [(24.6, 30), (25.1, 75)]), 15)
            p = person(img, hx, face=1, mood='smile', walk=hw, front=front)
            if t < 20.5: bags(img, p)
            elif t < 23.7: wrench(img, p)
            else: flower(img, p, 1)
            orb(img, p, ok)
            pop_heart(img, (710, 600), t, 26.8, 70)
            lesson(img, t, 27.6, 33.0, 29.0, 33.0, 'What gets *appreciated,* grows.', 'And it works *both ways.*', 50)
            caption(img, 'Who do you need to *thank tonight?*', t, 33.2, 40)

# ============ VIDEO 4 ============
class V4:
    name = '04_parenting_not_now'; dur = 36.0; bg = 'living'
    hook = 'YOUR CHILD IS LEARNING THIS *FROM YOU RIGHT NOW.*'
    rw = (18.4, 19.4, 18.2, 4.0)
    prog = ['Em', 'C', 'G', 'D']; bpm = 64
    KT = 890
    bubbles = [(4.0, 5.8, "DADDY,\nLOOK!", (400, 890), 'say'),
               (5.9, 7.6, "NOT NOW.", (700, SIT), 'say'),
               (11.8, 13.8, "SON, LOOK!\nOLD PHOTOS\nOF US.", (380, STAND), 'say'),
               (13.9, 15.6, "NOT NOW.", (700, SIT), 'say'),
               (19.6, 21.2, "DADDY,\nLOOK!", (400, 890), 'say'),
               (21.3, 23.3, "WOW! TELL ME\nABOUT IT!", (700, SIT), 'say'),
               (23.4, 25.2, "IT'S YOU\nAND ME!", (400, 890), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('whoosh', 9.7), ('boom', 9.9), ('rewind', 18.4), ('whoosh', 19.35),
              ('chime', 24.0), ('whoosh', 26.4)]

    @staticmethod
    def scene(img, t):
        if t < 9.8:
            label(img, 'AGE 6', t, 2.6, 9.6)
            kx, kw = walkstate(t, [(2.6, -60), (3.9, 400), (7.7, 400), (9.6, -80)])
            up = t < 7.6
            bob = -10 * abs(math.sin(t * 9)) if 4.0 <= t < 5.8 else 0
            k = person(img, kx, s=0.58, kid=True, face=1 if t < 7.7 else -1, mood='smile' if up else 'sad',
                       walk=kw, bob=bob, headdown=0 if up else 24, front=(150, 10) if (up and t > 3.9) else (10, 10))
            paper(img, k, up and t > 3.9)
            p = person(img, 700, face=-1, sitk=1, headdown=22, front=PHONE_ARM)
            phone(img, p['fh'])
        elif t < 19.3:
            label(img, 'AGE 21', t, 11.4, 18.2)
            ox, ow = walkstate(t, [(16.4, 380), (18.0, 210)])
            low = t >= 15.6
            o = person(img, ox, col=(196, 196, 200), lean=7, face=1 if t < 16.4 else -1, walk=ow,
                       mood='smile' if not low else 'sad', headdown=0 if not low else 20,
                       front=(60, 40) if not low else (10, 12))
            # grey hair hint for the older father
            ellipse(img, (o['head'][0], o['head'][1] - 0.45 * o['hr']), (o['hr'] * 0.92, o['hr'] * 0.5), 0, 180, 360, (150, 150, 155), -1)
            album(img, o)
            p = person(img, 700, face=-1, sitk=1, headdown=22, front=PHONE_ARM)
            phone(img, p['fh'])
            caption(img, 'He learned it from *someone.*', t, 15.8, 18.4)
            if t < 11.6:
                k = win(t, 9.8, 11.3, 0.25)
                img[:] = (img.astype(np.float32) * (1 - 0.85 * k)).astype(np.uint8)
                spr = label_sprite('15 YEARS LATER', WHITE, 56)
                blit(img, spr, (W - spr.shape[1]) / 2, 880, k)
        else:
            label(img, 'AGE 6 - AGAIN', t, 19.4, 26.4, color=BLUE)
            kx, kw = walkstate(t, [(25.2, 400), (26.2, 520)])
            bob = -16 * abs(math.sin(t * 8)) if 23.4 <= t < 25.0 else 0
            k = person(img, kx, s=0.58, kid=True, face=1, mood='smile', walk=kw, bob=bob,
                       front=(150, 10) if t < 25.2 else (60, 20))
            paper(img, k, t < 25.2)
            down = prog(t, 20.6, 21.2)
            p = person(img, 700, face=-1, sitk=1, headdown=lerp(22, 0, down), mood='flat' if down < 1 else 'smile',
                       lean=lerp(0, 14, down), front=(lerp(PHONE_ARM[0], 40, down), lerp(PHONE_ARM[1], 30, down)))
            if down < 1: phone(img, p['fh'])
            else: phone(img, (790, 1100), on=False)
            pop_heart(img, (560, 760), t, 24.0, 70)
            lesson(img, t, 26.6, 32.0, 28.0, 32.0, 'Children forget most of what you *gave* them.', 'They remember if you *looked up.*', 50)
            lesson(img, t, 32.2, 40, 32.6, 40, 'Put the phone down for *10 minutes* tonight.',
                   'Tag a parent who does this well.', 42, 50, POPM, (190, 190, 196))

# ============ VIDEO 5 ============
BRICKS = ["I'M FINE.", "FORGET IT.", "PRIDE", "WHATEVER.", "SILENCE", "NOT NOW.", "UNSAID", "TOO TIRED", "IGNORED", "DISTANCE"]
BH = 58
def brick_land(i): return 3.4 + i * 0.95
def brick_remove(i): return 22.6 + (len(BRICKS) - 1 - i) * 0.28

class V5:
    name = '05_relationship_the_wall'; dur = 37.0; bg = 'plain'
    hook = "MOST COUPLES DON'T SEE THE WALL... *UNTIL IT'S TOO HIGH.*"
    rw = None
    prog = ['F#m', 'D', 'A', 'E']; bpm = 60
    bubbles = [(3.0, 4.4, "I'M FINE.", (330, STAND), 'say'),
               (4.3, 5.6, "FORGET IT.", (750, STAND), 'say'),
               (17.9, 20.4, "CAN WE TALK?\nI'M SORRY.", (300, STAND), 'say'),
               (20.5, 22.5, "ME TOO.\nI MISSED US.", (780, STAND), 'say')]
    events = ([('boom', 0), ('whoosh', 2.45)] + [('thud', brick_land(i)) for i in range(len(BRICKS))] +
              [('knock', 17.35)] + [('pop', brick_remove(i) + 0.05) for i in range(len(BRICKS))] +
              [('chime', 27.2), ('whoosh', 27.6)])

    @staticmethod
    def scene(img, t):
        wx, ww = walkstate(t, [(13.4, 330), (14.6, 250), (17.0, 250), (17.4, 300), (25.4, 300), (26.6, 488)])
        hx, hw = walkstate(t, [(13.4, 750), (14.6, 830), (20.2, 830), (20.6, 780), (25.4, 780), (26.6, 592)])
        wf = 1 if (t < 13.4 or t >= 17.0) else -1
        hf = -1 if (t < 13.4 or t >= 20.2) else 1
        wm = step(t, [(0, 'flat'), (6, 'sad'), (25.4, 'smile')])
        hm = step(t, [(0, 'flat'), (6, 'sad'), (25.4, 'smile')])
        whd = kf(t, [(5, 0), (12, 18), (17.0, 22), (17.4, 0)])
        hhd = kf(t, [(5, 0), (12, 18), (20.0, 22), (20.4, 0)])
        hug = kf(t, [(26.3, 0), (26.8, 1)])
        knock = 17.25 <= t < 17.95
        wfront = (95 + 12 * math.sin(t * 28), 10) if knock else (lerp(8, 62, hug), lerp(12, -40, hug))
        person(img, wx, face=wf, mood=wm, hair=True, dress=True, walk=ww, headdown=whd, front=wfront)
        person(img, hx, face=hf, mood=hm, walk=hw, headdown=hhd, front=(lerp(8, 62, hug), lerp(12, -40, hug)))
        for i, txt in enumerate(BRICKS):
            tl = brick_land(i); tr = brick_remove(i)
            if t < tl - 0.4: continue
            rest = GROUND - (i + 1) * BH
            cx = 540 + (10 if i % 2 else -10)
            y = lerp(rest - 520, rest, ei(prog(t, tl - 0.4, tl)))
            a = 1.0
            if t >= tr:
                q = prog(t, tr, tr + 0.75)
                y = rest + 700 * ei(q); cx += (1 if i % 2 else -1) * 140 * q; a = 1 - sm(q)
                if a <= 0.01: continue
            over = img.copy()
            x0, x1 = int(cx - 104), int(cx + 104)
            cv2.rectangle(over, (x0, int(y)), (x1, int(y + BH - 4)), (66, 58, 54), -1)
            cv2.rectangle(over, (x0 + 4, int(y) + 4), (x1 - 4, int(y + BH - 8)), (124, 108, 98), -1)
            cv2.line(over, (x0 + 6, int(y) + 7), (x1 - 6, int(y) + 7), (150, 134, 122), 2)
            spr = label_sprite(txt, (246, 240, 232), 25)
            blit(over, spr, cx - spr.shape[1] / 2, y + (BH - 4 - spr.shape[0]) / 2 + 1)
            img[:] = (img * (1 - a) + over * a).astype(np.uint8) if a < 1 else over
        pop_heart(img, (540, 610), t, 27.2, 80)
        caption(img, 'No big fight. Just *small things.*', t, 2.8, 6.0)
        caption(img, 'A little *pride.* A little *silence.*', t, 6.4, 9.8)
        caption(img, 'Day after day...', t, 10.2, 13.2)
        caption(img, 'Same home. *Miles apart.*', t, 13.6, 17.2)
        lesson(img, t, 27.8, 33.2, 29.4, 33.2, 'Walls are built *one silence* at a time.', 'And bridges? *One honest word* at a time.', 46, 46)
        caption(img, 'Which brick will you *take down today?*', t, 33.4, 40)

VIDEOS = {'1': V1, '2': V2, '3': V3, '4': V4, '5': V5}

def draw_bubbles(img, t, bubbles):
    for t0, t1, txt, tip, kind in bubbles:
        draw_bubble(img, txt, tip, t, t0, t1, kind)

def frame_fn(V):
    bg = make_bg(V.bg)
    def inner(t):
        img = bg.copy(); V.scene(img, t); draw_bubbles(img, t, V.bubbles); return img
    def f(t):
        if V.rw and V.rw[0] <= t < V.rw[1]:
            a, b, sa, sb = V.rw
            ts = lerp(sa, sb, sm(prog(t, a, b)))
            return rewind_fx(inner(ts), t, a, b)
        return hook_overlay(inner(t), V.hook, t)
    return f

def build(key):
    V = VIDEOS[key]
    vid = render(V.name, V.dur, frame_fn(V), OUT)
    ev = list(V.events) + [('pop', b[0]) for b in V.bubbles]
    duck = [(V.rw[0], V.rw[1], 0.25)] if V.rw else []
    a = audio.mix(V.dur, V.prog, ev, V.bpm, int(key) * 11, duck)
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
        cv2.imwrite(f'{OUT}/still_{key}_{t:05.1f}.jpg', cv2.cvtColor(f(t), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 85])

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        stills(sys.argv[2], [float(x) for x in sys.argv[3:]])
    else:
        build(sys.argv[1])
