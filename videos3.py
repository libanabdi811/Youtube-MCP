import sys, os, math, subprocess
import numpy as np, cv2
from engine import *
from videos import (tension_bar, lesson, phone, PHONE_ARM, draw_bubbles, frame_fn, STAND, SIT)
import audio

OUT = '/home/claude/shorts/out_2026-11-13'
os.makedirs(OUT, exist_ok=True)
JUICE = (255, 170, 60)

# ---------- props ----------
def snow(img, t):
    for i in range(28):
        x = 808 + (i * 37) % 226 + 6 * math.sin(t * 1.3 + i)
        y = 650 + ((t * 45 + i * 53) % 320)
        circle(img, (x, y), 4 + (i % 3), (225, 232, 245))

def storm(img, top, k, t):
    if k <= 0.02: return
    x, y = top[0], top[1] - 70 - 40 * (1 - k)
    col = mixc((40, 42, 50), (96, 98, 108), k)
    for dx, dy, r in ((-50, 6, 34), (-12, -16, 42), (34, 0, 36), (64, 12, 26), (-78, 14, 22)):
        circle(img, (x + dx, y + dy), r * (0.6 + 0.4 * k), col)
    if k > 0.5 and int(t * 5) % 3 == 0:
        pts = [(x + 6, y + 30), (x - 8, y + 58), (x + 8, y + 58), (x - 6, y + 90)]
        for a, b in zip(pts, pts[1:]): line(img, a, b, GOLD, 6)

def plates(img, n):
    for i in range(int(n)):
        ellipse(img, (968, 1036 - i * 15), (62, 11), 0, 0, 360, (210, 214, 222), -1)
        ellipse(img, (968, 1036 - i * 15), (62, 11), 0, 0, 360, (120, 124, 132), 2)

def juice(img, pos):
    x, y = pos
    poly(img, [(x - 16, y - 40), (x + 16, y - 40), (x + 12, y + 4), (x - 12, y + 4)], (150, 200, 230))
    poly(img, [(x - 14, y - 24), (x + 14, y - 24), (x + 12, y + 2), (x - 12, y + 2)], JUICE)

def fallen_glass(img, x):
    poly(img, [(x - 40, GROUND - 4), (x + 4, GROUND - 20), (x + 8, GROUND - 4), (x - 36, GROUND + 10)], (150, 200, 230))

def puddle(img, x, k):
    if k <= 0.02: return
    ellipse(img, (x, GROUND + 10), (110 * k, 18 * k), 0, 0, 360, JUICE, -1)

# ============ C1 Marriage: turn toward small moments ============
class C1:
    name = '11_marriage_turn_toward_small_moments'; dur = 36.0; bg = 'living'
    hook = "THE TINY MOMENT *MOST COUPLES MISS.*"
    rw = (12.8, 13.8, 12.6, 3.0)
    prog = ['C', 'G', 'Am', 'F']; bpm = 66
    bubbles = [(3.0, 5.0, "LOOK! IT'S\nSNOWING!", (300, STAND), 'say'),
               (5.1, 6.4, "MM-HMM.", (700, SIT), 'say'),
               (7.0, 9.0, "REMEMBER OUR\nFIRST WINTER?", (300, STAND), 'say'),
               (9.1, 10.2, "HMM.", (700, SIT), 'say'),
               (14.2, 16.0, "LOOK! IT'S\nSNOWING!", (300, STAND), 'say'),
               (16.4, 18.2, "OH WOW!\nSHOW ME!", (700, SIT), 'say'),
               (19.8, 21.6, "REMEMBER OUR\nFIRST WINTER?", (720, STAND), 'say'),
               (21.8, 23.4, "I'LL NEVER\nFORGET IT.", (420, STAND), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('thud', 10.3), ('rewind', 12.8), ('whoosh', 13.75), ('whoosh', 18.3),
              ('chime', 23.8), ('whoosh', 24.4)]

    @staticmethod
    def scene(img, t):
        snow(img, t)
        if t < 13.8:
            label(img, 'EVERY EVENING', t, 2.6, 12.8, color=(170, 170, 176))
            sad = t > 10.2
            person(img, 300, face=1, mood='sad' if sad else 'smile', headdown=18 if sad else 0,
                   front=(kf(t, [(2.9, 8), (3.2, 110), (5.0, 110), (5.3, 8)]), kf(t, [(2.9, 12), (3.2, -10), (5.0, -10), (5.3, 12)])))
            p = person(img, 700, face=-1, sitk=1, hair=True, mood='flat', headdown=22, front=PHONE_ARM)
            phone(img, p['fh'])
            caption(img, 'Tiny moments. *Missed.*', t, 10.4, 13.0)
        else:
            label(img, 'TRY AGAIN', t, 13.8, 24.2, color=BLUE)
            down = kf(t, [(16.0, 0), (16.5, 1)])
            sk = kf(t, [(18.2, 1), (18.9, 0)])
            hx, hw = walkstate(t, [(18.4, 300), (19.6, 540)])
            person(img, hx, face=1, mood='smile', walk=hw,
                   front=(kf(t, [(14.1, 8), (14.4, 110), (16.0, 110), (16.3, 8), (22.6, 8), (23.2, 40)]),
                          kf(t, [(14.1, 12), (14.4, -10), (16.0, -10), (16.3, 12)])))
            wf = -1 if t < 18.6 else 1
            if t < 18.6:
                p = person(img, 700, face=-1, sitk=sk, hair=True, dress=sk < 0.5, mood='smile' if down > 0.5 else 'flat',
                           headdown=lerp(22, 0, down), front=(lerp(PHONE_ARM[0], 8, down), lerp(PHONE_ARM[1], 12, down)))
                if down < 0.5: phone(img, p['fh'])
            else:
                person(img, 720, face=wf, hair=True, dress=True, mood='smile', headturn=-1 if 21.7 < t < 23.5 else None)
            glow(img, (630, 950), 300, GOLD, kf(t, [(19.6, 0), (23.8, 0.4)]))
            pop_heart(img, (630, 600), t, 23.8, 70)
            lesson(img, t, 24.4, 30.6, 25.6, 30.6, "Love lives in *small moments.*", "*Turn toward* them.", 58, 58)
            caption(img, 'When did your partner last *reach for you?*', t, 30.8, 40, size=54)

# ============ C2 Husband: leave work at the door ============
class C2:
    name = '12_better_husband_not_your_leftovers'; dur = 36.0; bg = 'home'
    hook = "DON'T GIVE YOUR FAMILY *YOUR LEFTOVERS.*"
    rw = (12.8, 13.8, 12.6, 2.8)
    prog = ['Dm', 'Bb', 'F', 'C']; bpm = 64
    bubbles = [(4.4, 6.2, "HI, LOVE!\nHOW WAS\nYOUR DAY?", (780, STAND), 'say'),
               (6.3, 7.6, "DON'T ASK.", (400, STAND), 'say'),
               (8.2, 9.4, "DADDY!\nLOOK!", (620, 860), 'say'),
               (9.5, 10.8, "I'M TIRED.", (400, STAND), 'say'),
               (15.0, 17.0, "LEAVE WORK\nAT THE DOOR.", (210, STAND), 'think'),
               (18.8, 20.4, "I'M HOME!\nI MISSED YOU.", (400, STAND), 'say'),
               (20.6, 21.8, "DADDY!", (640, 850), 'say'),
               (22.0, 23.6, "WELCOME\nHOME.", (780, STAND), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('thud', 6.4), ('thud', 9.6), ('rewind', 12.8), ('whoosh', 13.75),
              ('whoosh', 16.2), ('chime', 23.8), ('whoosh', 24.4)]

    @staticmethod
    def scene(img, t):
        if t < 13.8:
            label(img, 'AFTER A HARD DAY', t, 2.6, 12.8, color=RED)
            hx, hw = walkstate(t, [(2.6, 140), (4.2, 400)])
            hp = person(img, hx, face=1, mood='angry', walk=hw, headdown=14)
            storm(img, hp['top'], 1.0, t)
            kx, kw = walkstate(t, [(7.6, 660), (8.2, 570)])
            ks = t > 9.6
            person(img, kx, s=0.58, kid=True, face=-1, walk=kw, mood='sad' if ks else 'smile', headdown=14 if ks else 0,
                   front=(8, 12) if ks else (90, -10))
            wm = 'sad' if t > 6.4 else 'smile'
            person(img, 800, face=-1, hair=True, dress=True, mood=wm)
            caption(img, 'His family got his *leftovers.*', t, 10.6, 13.0)
        else:
            label(img, 'TRY AGAIN', t, 13.8, 24.2, color=BLUE)
            hx, hw = walkstate(t, [(13.8, 160), (14.6, 210), (17.4, 210), (18.6, 400)])
            calm = kf(t, [(15.8, 0), (17.2, 1)])
            hug = kf(t, [(21.0, 0), (21.6, 1)])
            hp = person(img, hx, face=1, mood='smile' if calm > 0.7 else 'flat', walk=hw, headdown=lerp(14, 0, calm),
                        front=(lerp(8, 40, hug), lerp(12, 30, hug)))
            if calm < 1:
                k = 1 - calm
                top = (hp['top'][0], hp['top'][1] - 120 * calm)
                storm(img, top, k, t)
            kx, kw = walkstate(t, [(20.4, 640), (21.2, 520)])
            person(img, kx, s=0.58, kid=True, face=-1, walk=kw, mood='smile', front=(lerp(8, 70, hug), lerp(12, -30, hug)))
            person(img, 800, face=-1, hair=True, dress=True, mood='smile' if t > 18.8 else 'flat')
            glow(img, (520, 950), 300, GOLD, kf(t, [(18.6, 0), (23.8, 0.45)]))
            pop_heart(img, (520, 640), t, 23.8, 70)
            lesson(img, t, 24.4, 30.6, 25.6, 30.6, "Your family deserves your *best,*", "not your *leftovers.*", 54, 54)
            caption(img, 'What will you leave *at the door* tonight?', t, 30.8, 40, size=54)

# ============ C3 Wife: say it kindly and clearly ============
class C3:
    name = '13_better_wife_hints_vs_kind_words'; dur = 37.0; bg = 'kitchen'
    hook = "HINTS DON'T WORK. *KIND WORDS DO.*"
    rw = (12.8, 13.8, 12.6, 3.0)
    prog = ['F', 'Am', 'Dm', 'C']; bpm = 68
    bubbles = [(3.2, 5.0, "SIGH...", (860, STAND), 'say'),
               (5.2, 6.8, "YOU OKAY?", (330, STAND), 'say'),
               (6.9, 8.2, "I'M FINE.", (860, STAND), 'say'),
               (8.3, 9.4, "OKAY!", (330, STAND), 'say'),
               (9.8, 11.8, "HE SHOULD\nJUST KNOW.", (860, STAND), 'think'),
               (14.2, 15.6, "YOU OKAY?", (330, STAND), 'say'),
               (15.8, 18.4, "I'M REALLY\nTIRED TONIGHT.", (860, STAND), 'say'),
               (18.6, 21.0, "COULD YOU HELP\nWITH THE DISHES?", (860, STAND), 'say'),
               (21.2, 23.2, "OF COURSE.\nTHANKS FOR\nTELLING ME.", (420, STAND), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('whoosh', 9.4), ('crack', 10.0), ('rewind', 12.8), ('whoosh', 13.75),
              ('whoosh', 21.4), ('chime', 24.0), ('whoosh', 24.6)]

    @staticmethod
    def scene(img, t):
        if t < 13.8:
            label(img, 'THE HINT', t, 2.6, 12.8, color=RED)
            plates(img, 6)
            wm = step(t, [(0, 'flat'), (3.2, 'sad'), (9.8, 'angry')])
            wash = 50 + 14 * math.sin(t * 6)
            fw = 1 if t < 5.0 or t > 9.4 else -1
            person(img, 860, face=fw, hair=True, dress=True, mood=wm,
                   front=(wash, 40) if fw == 1 else (8, 12), headdown=10)
            hx, hw = walkstate(t, [(9.4, 330), (11.0, -120)])
            person(img, hx, face=1 if t < 9.4 else -1, mood='smile' if t > 8.2 else 'flat', walk=hw)
            caption(img, 'Hints get *missed.* Hurt *grows.*', t, 10.6, 13.0)
        else:
            label(img, 'TRY AGAIN', t, 13.8, 24.4, color=BLUE)
            n = kf(t, [(22.6, 6), (24.4, 1)])
            plates(img, n)
            hx, hw = walkstate(t, [(21.4, 330), (22.6, 650)])
            if t < 22.6:
                person(img, 860, face=-1 if t > 15.0 else 1, hair=True, dress=True,
                       mood='smile' if t > 21.2 else 'flat', front=(8, 12) if t > 15.0 else (50, 40))
                person(img, hx, face=1, mood='smile' if t > 21.0 else 'flat', walk=hw)
            else:
                person(img, 860, face=1, hair=True, dress=True, mood='smile', front=(50 + 14 * math.sin(t * 6), 40))
                person(img, hx, face=1, mood='smile', walk=hw, front=(50 + 14 * math.sin(t * 6 + 1), 40))
            pop_heart(img, (780, 580), t, 24.0, 70)
            lesson(img, t, 24.6, 30.0, 25.8, 30.0, "Hints get *missed.*", "Kind, clear words get *heard.*", 56, 56)
            caption(img, 'And it goes *both ways.*', t, 30.2, 32.6)
            caption(img, 'What do you need to *say out loud?*', t, 32.8, 40, size=56)

# ============ C4 Parenting: connect before you correct ============
class C4:
    name = '14_parenting_connect_before_correct'; dur = 36.0; bg = 'living'
    hook = "WHAT YOUR CHILD HEARS *WHEN YOU SHOUT.*"
    rw = (12.8, 13.8, 12.6, 3.0)
    prog = ['Em', 'C', 'G', 'D']; bpm = 64
    bubbles = [(4.2, 6.2, "WHAT DID\nYOU DO?!", (300, STAND), 'say'),
               (6.3, 8.2, "YOU ALWAYS\nMAKE A MESS!", (300, STAND), 'say'),
               (8.4, 10.2, "I'M BAD.", (660, 880), 'think'),
               (16.2, 18.2, "HEY. IT'S OKAY.\nACCIDENTS\nHAPPEN.", (460, 780), 'say'),
               (18.4, 20.0, "SORRY, DAD.", (680, 880), 'say'),
               (20.2, 22.2, "LET'S CLEAN\nIT TOGETHER.", (460, 780), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('crack', 3.9), ('thud', 4.2), ('rewind', 12.8), ('whoosh', 13.75),
              ('whoosh', 14.2), ('chime', 23.8), ('whoosh', 24.4)]

    @staticmethod
    def scene(img, t):
        if t < 13.8:
            label(img, 'ONE SPILL', t, 2.6, 12.8, color=RED)
            kx, kw = walkstate(t, [(2.6, 780), (3.6, 660)])
            fear = prog(t, 6.3, 8.2)
            ks = lerp(0.58, 0.52, fear)
            k = person(img, kx, s=ks, kid=True, face=-1, walk=kw, mood='sad' if t > 4.0 else 'smile',
                       col=mixc(WHITE, DIM, fear * 0.6), headdown=16 if t > 4.2 else 0,
                       front=(70, 20) if t < 3.8 else (8, 12))
            if t < 3.8: juice(img, k['fh'])
            else:
                q = prog(t, 3.8, 4.0)
                if q < 1: juice(img, (k['fh'][0] - 30 * q, lerp(k['fh'][1], GROUND - 10, q)))
                else:
                    puddle(img, 590, back(prog(t, 4.0, 4.5)))
                    fallen_glass(img, 610)
            fm = 'angry' if t > 4.1 else 'flat'
            person(img, 300, face=1, mood=fm,
                   front=(kf(t, [(4.1, 8), (4.4, 90), (8.0, 90), (8.3, 8)]), kf(t, [(4.1, 12), (4.4, 0)])))
            caption(img, 'He learned to *hide mistakes.*', t, 10.4, 13.0)
        else:
            label(img, 'TRY AGAIN', t, 13.8, 24.2, color=BLUE)
            pk = kf(t, [(22.4, 1), (23.6, 0)])
            puddle(img, 590, pk)
            if t < 22.6: fallen_glass(img, 610)
            hug = kf(t, [(22.8, 0), (23.4, 1)])
            fx, fw = walkstate(t, [(14.2, 300), (15.4, 440)])
            kneel = kf(t, [(15.3, 0), (15.9, 1)])
            person(img, fx, face=1, mood='smile' if t > 15.6 else 'flat', walk=fw, sitk=kneel * 0.5, lean=kneel * 10,
                   front=(lerp(8, 70, hug), lerp(12, -20, hug)))
            person(img, 660, s=0.58, kid=True, face=-1, mood='smile' if t > 20.2 else 'sad', headdown=16 if t < 18.4 else 0,
                   front=(lerp(8, 70, hug), lerp(12, -30, hug)))
            glow(img, (580, 1000), 260, GOLD, kf(t, [(20.2, 0), (23.8, 0.45)]))
            pop_heart(img, (570, 720), t, 23.8, 60)
            lesson(img, t, 24.4, 30.4, 25.6, 30.4, "*Connect* first.", "*Then* correct.", 62, 62)
            caption(img, "How do you react to your child's *mistakes?*", t, 30.6, 40, size=54)

# ============ C5 Lesson: ask before you assume ============
class C5:
    name = '15_relationship_ask_before_you_assume'; dur = 36.0; bg = 'plain'
    hook = "THE STORY IN YOUR HEAD *ISN'T ALWAYS TRUE.*"
    rw = (12.8, 13.8, 12.6, 2.8)
    prog = ['Am', 'F', 'C', 'E']; bpm = 62
    bubbles = [(3.2, 5.0, "SHE FORGOT\nABOUT ME.", (340, STAND), 'think'),
               (5.1, 6.8, "SHE DOESN'T\nCARE.", (340, STAND), 'think'),
               (8.4, 10.2, "YOU NEVER\nTHINK OF ME!", (340, STAND), 'say'),
               (10.3, 11.6, "BUT I...", (740, STAND), 'say'),
               (14.0, 16.0, "WAIT. MAYBE\nSOMETHING\nHAPPENED.", (340, STAND), 'think'),
               (17.6, 19.4, "YOU'RE LATE.\nARE YOU OKAY?", (340, STAND), 'say'),
               (19.6, 21.8, "MY MUM IS IN\nHOSPITAL. MY\nPHONE DIED.", (740, STAND), 'say'),
               (22.0, 23.4, "I'M HERE.\nCOME HERE.", (340, STAND), 'say')]
    events = [('boom', 0), ('whoosh', 2.45), ('tick', 3.0), ('tick', 4.0), ('tick', 5.0), ('tick', 6.0),
              ('whoosh', 7.0), ('crack', 8.4), ('rewind', 12.8), ('whoosh', 13.75), ('whoosh', 16.2),
              ('chime', 24.2), ('whoosh', 24.8)]

    @staticmethod
    def scene(img, t):
        if t < 13.8:
            label(img, 'SHE SAID 7 PM. IT IS 9.', t, 2.6, 12.8, color=(170, 170, 176), size=36)
            tension_bar(img, t, 3.0, 12.8, kf(t, [(3.0, 0.1), (8.4, 0.95)]))
            hm = step(t, [(0, 'flat'), (3.2, 'sad'), (8.2, 'angry')])
            person(img, 340, face=1, mood=hm, front=(kf(t, [(8.3, 8), (8.6, 80), (10.0, 80), (10.3, 8)]), 10))
            wx, ww = walkstate(t, [(7.0, 1180), (8.2, 740)])
            person(img, wx, face=-1, hair=True, dress=True, walk=ww, mood='sad', headdown=16 if t > 10.3 else 6)
            caption(img, 'He believed the story *in his head.*', t, 10.6, 13.0)
        else:
            label(img, 'TRY AGAIN', t, 13.8, 24.6, color=BLUE)
            hx, hw = walkstate(t, [(22.6, 340), (23.6, 480)])
            wx, ww = walkstate(t, [(16.2, 1180), (17.4, 740), (22.6, 740), (23.6, 610)])
            hug = kf(t, [(23.2, 0), (23.8, 1)])
            hm = step(t, [(0, 'flat'), (14.0, 'flat'), (19.6, 'sad'), (22.0, 'smile')])
            person(img, hx, face=1, mood=hm, walk=hw, front=(lerp(8, 62, hug), lerp(12, -40, hug)))
            person(img, wx, face=-1, hair=True, dress=True, walk=ww, mood='sad' if t < 23.4 else 'smile',
                   headdown=10 if t < 23.0 else 0, front=(lerp(8, 62, hug), lerp(12, -40, hug)))
            glow(img, (545, 950), 280, GOLD, kf(t, [(22.0, 0), (24.2, 0.4)]))
            pop_heart(img, (545, 600), t, 24.2, 70)
            lesson(img, t, 24.8, 30.6, 26.0, 30.6, "Silence isn't *proof.*", "*Ask* before you assume.", 58, 58)
            caption(img, "What story do you *tell yourself* when they're late?", t, 30.8, 40, size=52)

VIDEOS = {'11': C1, '12': C2, '13': C3, '14': C4, '15': C5}

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
    os.replace(tmp, os.path.join(OUT, '2026-11-13_' + V.name + '.mp4'))
    os.remove(vid); os.remove(wav)
    print('done', V.name)

def stills(key, times):
    V = VIDEOS[key]; f = frame_fn(V)
    for t in times:
        cv2.imwrite(f'{OUT}/still_{int(key):02d}_{t:05.1f}.jpg', cv2.cvtColor(f(t), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 80])

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        stills(sys.argv[2], [float(x) for x in sys.argv[3:]])
    else:
        build(sys.argv[1])
