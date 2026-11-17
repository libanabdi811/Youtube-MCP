"""GTA 6 fan Shorts, batch 5 (2026-11-17, VIRAL FORMAT v2). 100% original visuals: stick figures, neon shapes, text cards.
Facts (sources in TOPICS.md): out Thursday 19 Nov 2026 on PS5 + Xbox Series X|S (Rockstar Newswire); Rockstar has released
the official launch trailer (VGC / gHacks); CNN 16 Nov 2026 headline calls GTA VI "the biggest entertainment event of the year".
NOT ANNOUNCED: PS4 version, Nintendo Switch 2 version. Exact unlock time not stated as fact anywhere in this batch."""
import math, sys, os, cv2, numpy as np
from engine import *
from viral import frame_fn_v2, build_v2, make_bedroom
from gta_example import controller
from videos_gta_d1 import (room_bg, sofa, neon_bg, dim, fit_sprite, big_text, stamp, progress_bar,
                           FL, GREEN, PINK, CYAN, DISC)
from videos_gta_d4 import ncard

OUT = '/home/claude/shorts/out_2026-11-17'
os.makedirs(OUT, exist_ok=True)
GREY = (200, 200, 206)
FAINT = (130, 130, 138)

# =========================================================
# K1  Countdown: 48 hours, what's real
# =========================================================
class Hours48:
    name = '2026-11-17_gta6_48_hours_whats_real'; dur = 23.0
    banner = "GTA 6 IN 48 HOURS. / *HERE'S WHAT'S REAL.*"
    prog = ['Em', 'C', 'G', 'D']; bpm = 114
    bubbles = [(1.4, 3.0, "2 DAYS.\nI CAN'T SLEEP.", (380, 1080), 'say'),
               (3.1, 4.7, "THEN LEARN\nWHAT'S REAL.", (720, 1080), 'say'),
               (13.6, 15.1, "48 HOURS IS\n2,880 MINUTES.", (380, 1080), 'say'),
               (15.2, 16.8, "PLEASE STOP\nDOING MATHS.", (720, 1080), 'say')]
    events = [('tick', 0.0), ('boom', 0.5), ('thud', 3.1), ('whoosh', 4.9), ('thud', 5.1), ('thud', 7.6),
              ('thud', 10.1), ('boom', 11.0), ('thud', 13.6), ('chime', 15.2), ('whoosh', 17.0)]

    @staticmethod
    def make_bg(): return neon_bg()

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.15, 540, 900)), (1.3, (1.0, 540, 960)), (1.4, (1.3, 380, 1150)), (3.0, (1.3, 380, 1150)),
                      (3.1, (1.3, 720, 1150)), (4.7, (1.3, 720, 1150)), (4.9, (1.0, 540, 960)), (13.4, (1.0, 540, 960)),
                      (13.6, (1.3, 380, 1150)), (15.1, (1.3, 380, 1150)), (15.2, (1.3, 720, 1150)), (16.8, (1.3, 720, 1150)),
                      (17.1, (1.0, 540, 960)), (23.0, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if 0.5 <= t < 1.0: return 1 - prog(t, 0.5, 1.0)
        if 11.0 <= t < 11.5: return 0.8 * (1 - prog(t, 11.0, 11.5))
        return 0.0

    @staticmethod
    def world(img, t):
        if t < 4.9 or 13.3 <= t < 17.1:
            maths = 13.6 <= t < 15.2
            p = person(img, 380, y=1620, face=1, mood='smile' if not maths else 'flat',
                       front=(150, -50) if maths else (35, 75), rear=(-6, 10))
            if not maths: controller(img, p['fh'])
            tired = 15.2 <= t < 16.8
            person(img, 720, y=1620, face=-1, mood='sad' if tired else 'smile',
                   front=(60, 40) if (3.1 <= t < 4.7) else ((150, 15) if tired else (10, 14)),
                   headdown=14 if tired else 0)

    @staticmethod
    def ui(img, t):
        if t < 1.4:
            d = '72' if t < 0.5 else '48'
            glow(img, (540, 760), 420, PINK, 0.5)
            big_text(img, d, t, 0.5 if d == '48' else 0.0, 700, 330, WHITE, GOLD, pop=d == '48')
            big_text(img, 'HOURS LEFT', t, 0.0, 950, 96, GOLD, GOLD, pop=False)
        elif t < 4.9:
            big_text(img, '*48* HOURS LEFT', t, 1.4, 1740, 90, WHITE, GOLD, pop=False)
        if 4.9 <= t < 13.4 or t >= 17.0:
            dim(img, t, 4.9 if t < 13.4 else 17.0)
        if 4.9 <= t < 13.4:
            big_text(img, "WHAT'S *REAL*", t, 4.9, 520, 64, WHITE, GOLD, pop=False)
            ncard(img, t, 5.1, 600, 'THU', 'LAUNCH DAY: 19 NOVEMBER', 'PS5 + XBOX SERIES X|S. ROCKSTAR', GOLD)
            ncard(img, t, 7.6, 830, 'OUT', 'THE LAUNCH TRAILER', 'ALREADY RELEASED BY ROCKSTAR', CYAN)
            ncard(img, t, 10.1, 1060, 'CNN', '"BIGGEST ENTERTAINMENT', 'EVENT OF THE YEAR"  (CNN, 16 NOV)', PINK)
            caption(img, 'Not a movie. *A video game.*', t, 11.0, 13.3, 1330, 52)
        if t >= 17.0:
            caption(img, "What's the FIRST thing / *you'll do in GTA 6?*", t, 17.2, 30, 900, 60)
            caption(img, 'Comment it below.', t, 18.4, 30, 1130, 42, GREY, POPM)
            caption(img, DISC, t, 19.0, 30, 1210, 30, FAINT, POPM)

# =========================================================
# K2  Skit: everything ready... then the TV remote died
# =========================================================
def tv_screen(img, t, on):
    if on:
        g = vgrad(386, (60, 20, 100), (240, 110, 90)).astype(np.uint8)
        img[432:818, 122:958] = g[:, None, :]
        sp = fit_sprite('PRESS START', WHITE, 50, 600)
        blit(img, sp, 540 - sp.shape[1] / 2, 590, 0.8 + 0.2 * math.sin(t * 4))
    else:
        sp = fit_sprite('NO SIGNAL', (150, 150, 170), 46, 600)
        blit(img, sp, 540 - sp.shape[1] / 2 + 30 * math.sin(t * 0.9), 600)

def remote(img, hand, dead=True):
    x, y = hand
    poly(img, [(x - 13, y - 40), (x + 13, y - 40), (x + 13, y + 22), (x - 13, y + 22)], (34, 34, 42))
    circle(img, (x, y - 26), 6, (120, 40, 40) if dead else RED)
    for j in range(3): circle(img, (x, y - 8 + j * 11), 3, (90, 90, 100))

class DeadRemote:
    name = '2026-11-17_gta6_dead_tv_remote'; dur = 21.5
    banner = "READY FOR GTA 6 FOR MONTHS. / *THEN THE REMOTE DIED.*"
    prog = ['Dm', 'Bb', 'F', 'C']; bpm = 106
    bubbles = [(0.2, 1.9, "COME ON...\nCOME ON!!", (330, 960), 'say'),
               (2.0, 3.6, "CONSOLE: READY.\nGAME: READY.\nREMOTE: DEAD.", (330, 960), 'think'),
               (3.7, 5.2, "WHO TOOK THE\nBATTERIES?!", (330, 960), 'say'),
               (6.6, 8.2, "TRIED THE BUTTON\nON THE TV?", (760, 960), 'say'),
               (8.3, 9.6, "...THE TV HAS\nBUTTONS?!", (330, 960), 'say'),
               (10.0, 11.5, "YOU'RE\nWELCOME.", (760, 960), 'say'),
               (11.6, 13.2, "TOP 10 DAD.\nMAYBE TOP 3.", (330, 960), 'say')]
    events = [('boom', 0.0), ('tick', 0.3), ('tick', 0.6), ('tick', 0.9), ('whoosh', 2.0), ('thud', 3.7),
              ('tick', 5.4), ('tick', 5.8), ('thud', 6.6), ('thud', 8.3), ('boom', 9.7), ('chime', 10.0),
              ('pop', 11.6), ('whoosh', 13.6)]

    @staticmethod
    def make_bg():
        img = room_bg(); sofa(img, 120, 560); return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.35, 340, 1150)), (1.9, (1.3, 340, 1150)), (2.0, (1.0, 540, 960)), (3.6, (1.0, 540, 960)),
                      (3.7, (1.3, 340, 1150)), (5.2, (1.3, 340, 1150)), (5.4, (1.0, 540, 960)), (6.5, (1.0, 540, 960)),
                      (6.6, (1.3, 760, 1150)), (8.2, (1.3, 760, 1150)), (8.3, (1.35, 340, 1150)), (9.6, (1.35, 340, 1150)),
                      (9.7, (1.0, 540, 960)), (21.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if t < 0.5: return 0.8 * (1 - prog(t, 0, 0.5))
        if 3.7 <= t < 4.2: return 1 - prog(t, 3.7, 4.2)
        if 9.7 <= t < 10.2: return 0.8 * (1 - prog(t, 9.7, 10.2))
        return 0.0

    @staticmethod
    def world(img, t):
        on = t >= 9.7
        tv_screen(img, t, on)
        if on and t < 10.4: glow(img, (540, 625), 380, (255, 160, 120), 0.5 * (1 - prog(t, 9.7, 10.4)))
        lab = fit_sprite('LAUNCH NIGHT', GOLD, 34, 500); blit(img, lab, 540 - lab.shape[1] / 2, 1560)
        shout = 3.7 <= t < 5.2
        shock = 8.3 <= t < 9.6
        mash = t < 2.0
        hm = 'angry' if shout else ('sad' if (shock or 2.0 <= t < 3.7) else ('smile' if t >= 10.0 else 'flat'))
        p = person(img, 330, y=FL, face=1, sitk=1, mood=hm,
                   front=(150, -30) if (shout or shock) else ((60, 20) if mash else (35, 75)),
                   rear=(-150, -20) if (shout or shock) else (-6, 10),
                   bob=-12 * abs(math.sin(t * 11)) if (shout or mash) else 0)
        if not (shout or shock):
            if t < 9.7: remote(img, (p['fh'][0], p['fh'][1] + 6 * math.sin(t * 40) if mash else p['fh'][1]))
            else: controller(img, p['fh'])
        if t >= 5.4:
            dx = kf(t, [(5.4, 1180), (6.5, 760), (9.0, 760), (9.6, 900), (10.0, 760)])
            press = 9.0 <= t < 10.0
            d = person(img, dx, y=FL, face=-1, mood='smile' if t >= 10.0 else 'flat',
                       front=(150, -60) if press else ((60, 40) if 6.6 <= t < 8.2 else (10, 14)),
                       walk=(t * 7, 1.0) if 5.4 <= t < 6.5 else None)
            if press:
                circle(img, (945, 805), 9, GOLD)
        if t >= 11.6: pop_heart(img, (545, 880), t, 11.6, 45)

    @staticmethod
    def ui(img, t):
        if t >= 13.6:
            dim(img, t, 13.6)
            caption(img, 'What almost ruined / *YOUR launch night?*', t, 13.8, 30, 900, 60)
            caption(img, 'Wrong answers only.', t, 15.0, 30, 1130, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 15.6, 30, 1210, 40, GREY, POPM)
            caption(img, DISC, t, 16.2, 30, 1300, 30, FAINT, POPM)

# =========================================================
# K3  Which gamer are you, 2 days before GTA 6?
# =========================================================
PANELS = [((275, 680), '1. THE REFRESHER'), ((805, 680), '2. THE REWATCHER'),
          ((275, 1170), '3. THE PLANNER'), ((805, 1170), '4. "NOT HYPED"')]

def panel(img, t, i, active):
    (cx, cy), lab = PANELS[i]
    x0, y0, x1, y1 = cx - 245, cy - 220, cx + 245, cy + 220
    keep = img.copy()
    cv2.rectangle(img, (x0, y0), (x1, y1), (24, 22, 34), -1)
    gy = cy + 160
    if i == 0:
        c = (cx + 120, cy - 80)
        a0 = (t * 400) % 360
        ellipse(img, c, (48, 48), 0, a0, a0 + 290, CYAN, 9)
        ang = math.radians(a0 + 290)
        tip = (c[0] + 48 * math.cos(ang), c[1] + 48 * math.sin(ang))
        circle(img, tip, 12, CYAN)
        p = person(img, cx - 80, y=gy, s=0.48, face=1, mood='flat', front=(40, 60))
        phone(img, p['fh'], on=True)
    elif i == 1:
        cv2.rectangle(img, (cx + 20, cy - 140), (cx + 220, cy - 20), (40, 40, 56), -1)
        poly(img, [(cx + 100, cy - 110), (cx + 100, cy - 50), (cx + 150, cy - 80)], WHITE)
        n = 40 + int(t * 3) % 60
        sp = label_sprite(f'x{n}', GOLD, 28); blit(img, sp, cx + 120 - sp.shape[1] / 2, cy - 5)
        p = person(img, cx - 80, y=gy, s=0.48, face=1, mood='smile', front=(40, 60))
        controller(img, p['fh'])
    elif i == 2:
        cv2.rectangle(img, (cx + 30, cy - 160), (cx + 210, cy + 20), (230, 228, 220), -1)
        for j in range(4):
            yy = cy - 125 + j * 40
            line(img, (cx + 90, yy), (cx + 190, yy), (120, 120, 130), 5)
            if (t * 1.6) % 4 > j:
                line(img, (cx + 50, yy), (cx + 60, yy + 10), GREEN, 5); line(img, (cx + 60, yy + 10), (cx + 78, yy - 12), GREEN, 5)
        person(img, cx - 80, y=gy, s=0.48, face=1, mood='smile', front=(60, 30))
    else:
        k = 0.5 + 0.5 * math.sin(t * 5)
        glow(img, (cx + 130, cy - 90), 110, GOLD, 0.3 * k)
        sp = label_sprite('2 DAYS', GOLD, 30); blit(img, sp, cx + 130 - sp.shape[1] / 2, cy - 110)
        person(img, cx - 60, y=gy, s=0.48, face=1, mood='flat', front=(70, -40), rear=(-70, -40),
               bob=-6 * abs(math.sin(t * 14)))
    m = np.ones(img.shape[:2], bool); m[y0:y1, x0:x1] = False
    img[m] = keep[m]
    col = GOLD if active else (60, 60, 72)
    cv2.rectangle(img, (x0, y0), (x1, y1), col, 6 if active else 3)
    blit(img, fit_sprite(lab, GOLD if active else (150, 150, 160), 26, 460), x0 + 12, y1 - 50)
    if not active:
        sub = img[y0 + 3:y1 - 2, x0 + 3:x1 - 2]
        sub[:] = (sub * 0.45).astype(np.uint8)

class TwoDaysWhich:
    name = '2026-11-17_gta6_2_days_which_gamer'; dur = 22.5
    banner = "2 DAYS BEFORE GTA 6. / *WHICH GAMER ARE YOU?*"
    prog = ['A', 'E', 'F#m', 'D']; bpm = 118
    bubbles = [(0.2, 2.4, "REFRESH.\nREFRESH.", (315, 595), 'say'),
               (2.7, 5.0, "ONE MORE\nWATCH.", (845, 595), 'say'),
               (5.3, 7.6, "DAY 1 PLAN:\nPAGE 6 OF 9.", (315, 1085), 'say'),
               (7.9, 10.2, "IT'S JUST\nA GAME.", (845, 1085), 'say'),
               (12.0, 13.4, "SEE YOU THURSDAY\nFOR GTA 6!", (760, 960), 'say'),
               (13.5, 14.9, "...THIS\nTHURSDAY?!", (330, 800), 'say')]
    events = [('pop', 0.0), ('tick', 0.5), ('tick', 1.0), ('whoosh', 2.6), ('whoosh', 5.2), ('whoosh', 7.8),
              ('thud', 10.5), ('chime', 12.0), ('boom', 13.5), ('whoosh', 15.4)]

    @staticmethod
    def make_bg(): return room_bg(tv=False)

    @staticmethod
    def cam(t):
        keys = []
        for i, ((cx, cy), _) in enumerate(PANELS):
            a = i * 2.6
            keys += [(a + 0.15, (1.32, cx, cy)), (a + 2.45, (1.32, cx, cy))]
        keys += [(10.5, (1.0, 540, 960)), (13.4, (1.0, 540, 960)), (13.5, (1.3, 330, 1050)), (14.9, (1.3, 330, 1050)),
                 (15.2, (1.0, 540, 960)), (22.5, (1.0, 540, 960))]
        return kf(t, keys)

    @staticmethod
    def shake(t):
        if 13.5 <= t < 14.0: return 1 - prog(t, 13.5, 14.0)
        return 0.0

    @staticmethod
    def world(img, t):
        if t < 10.6:
            act = min(3, int(t / 2.6)) if t < 10.4 else -1
            for i in range(4): panel(img, t, i, i == act)
        else:
            shock = 13.5 <= t < 15.2
            p = person(img, 330, y=FL, face=1, mood='sad' if shock else 'flat',
                       front=(150, 15) if shock else (35, 75), rear=(-150, -15) if shock else (-6, 10),
                       bob=-12 * abs(math.sin(t * 10)) if shock else 0)
            if not shock: phone(img, p['fh'], on=True)
            person(img, 760, y=FL, face=-1, mood='smile', front=(60, 40) if 12.0 <= t < 13.4 else (10, 14))

    @staticmethod
    def ui(img, t):
        if 10.4 <= t < 12.0:
            a = win(t, 10.4, 11.8, 0.2)
            dim(img, t, 10.4, 0.5 * a)
            caption(img, "...and there's *always a #5.*", t, 10.5, 11.8, 1250, 70)
        if 12.0 <= t < 15.4:
            caption(img, '5. *THE ONE WHO FORGOT*', t, 12.0, 15.2, 1560, 56)
        if t >= 15.4:
            dim(img, t, 15.4)
            caption(img, 'Which one are you? / *Comment 1 to 5.*', t, 15.6, 30, 1050, 58)
            caption(img, 'Tag your friend who is number 5.', t, 16.8, 30, 1240, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 17.4, 30, 1330, 42, GREY, POPM)
            caption(img, DISC, t, 17.8, 30, 1440, 30, FAINT, POPM)

# =========================================================
# K4  Launch-week myths: real or not announced?
# =========================================================
QUIZ = [("GTA 6 IS COMING\nOUT ON PS4", 'NOT ANNOUNCED', RED, 'ROCKSTAR NAMED PS5 + XBOX SERIES X|S'),
        ("THE OFFICIAL LAUNCH\nTRAILER IS ALREADY OUT", 'TRUE', GREEN, 'RELEASED BY ROCKSTAR BEFORE LAUNCH'),
        ("GTA 6 LAUNCHES ON\nNINTENDO SWITCH 2", 'NOT ANNOUNCED', RED, 'NO SWITCH 2 VERSION HAS BEEN ANNOUNCED'),
        ("LAUNCH DAY IS\nA THURSDAY", 'TRUE', GREEN, '19 NOVEMBER 2026. CONFIRMED BY ROCKSTAR')]
QT = 3.4

class Myths4:
    name = '2026-11-17_gta6_launch_myths_checked'; dur = 21.5
    banner = "GTA 6 IN 2 DAYS: 4 MYTHS. / *#2 IS ACTUALLY TRUE.*"
    prog = ['Gm', 'Eb', 'Bb', 'F']; bpm = 120
    bubbles = [(5.6, 6.9, "WAIT, IT'S\nALREADY OUT?!", (820, 1310), 'say')]
    events = sum([[('tick', i * QT + 0.4), ('tick', i * QT + 1.0), ('tick', i * QT + 1.6),
                   ('boom' if i == 1 else 'thud', i * QT + 2.0), ('whoosh', i * QT + 3.3)] for i in range(4)], []) + \
             [('chime', 14.0)]

    @staticmethod
    def make_bg(): return room_bg(tv=False)

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.0, 540, 960)), (5.4, (1.0, 540, 960)), (5.6, (1.12, 640, 857)), (6.9, (1.12, 640, 857)),
                      (7.1, (1.0, 540, 960)), (21.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if 5.4 <= t < 5.9: return 1 - prog(t, 5.4, 5.9)
        return 0.0

    @staticmethod
    def world(img, t):
        i = int(t / QT)
        shock = 5.4 <= t < 6.9
        if i < 4:
            st, verdict, col, nt = QUIZ[i]
            lt = t - i * QT
            num = label_sprite(f'MYTH #{i + 1} OF 4', GOLD, 34); blit(img, num, 540 - num.shape[1] / 2, 470)
            cv2.rectangle(img, (70, 540), (1010, 860), (24, 22, 36), -1)
            cv2.rectangle(img, (70, 540), (1010, 860), (90, 80, 130), 4)
            for j, ln in enumerate(st.split('\n')):
                sp = fit_sprite(ln, WHITE, 46, 880); blit(img, sp, 540 - sp.shape[1] / 2, 610 + j * 100)
            if lt < 2.0: progress_bar(img, 190, 900, 700, 1 - lt / 2.0, GOLD, 22)
            stamp(img, verdict, t, i * QT + 2.0, (540, 990), col, 58 if len(verdict) > 6 else 64)
            if lt >= 2.2:
                sp = fit_sprite(nt, (210, 210, 220), 28, 960); blit(img, sp, 540 - sp.shape[1] / 2, 1075)
            mood = 'sad' if shock else ('smile' if lt >= 2.0 else 'flat')
        else:
            mood = 'smile'
        p = person(img, 820, y=1760, s=0.75, face=-1, mood=mood,
                   front=(150, 15) if shock else (35, 75), rear=(-150, -15) if shock else (-6, 10))
        if not shock: controller(img, p['fh'])

    @staticmethod
    def ui(img, t):
        if t >= 13.7:
            dim(img, t, 13.7)
            caption(img, 'Which one did you / *believe?*', t, 13.9, 30, 820, 60)
            caption(img, 'Comment the number. Out 19 Nov 2026.', t, 15.2, 30, 1060, 40, GREY, POPM)
            caption(img, 'PS5 + Xbox Series X|S at launch.', t, 15.6, 30, 1140, 30, FAINT, POPM)
            caption(img, DISC, t, 16.0, 30, 1200, 30, FAINT, POPM)

# =========================================================
# K5  Skit: he slept to skip to GTA 6. It didn't work.
# =========================================================
class NapSkip:
    name = '2026-11-17_gta6_nap_to_skip_time'; dur = 21.5
    banner = "HE SLEPT TO SKIP TO GTA 6. / *IT DIDN'T WORK.*"
    prog = ['C', 'G', 'Am', 'F']; bpm = 98
    bubbles = [(0.3, 1.9, "IS IT\nTHURSDAY?!", (360, 820), 'say'),
               (2.0, 3.5, "TUESDAY. 2:31 PM.", (360, 820), 'think'),
               (3.6, 5.1, "I SLEPT\n20 MINUTES?!", (360, 820), 'say'),
               (6.5, 8.2, "WANT TIME\nTO FLY?", (760, 820), 'say'),
               (8.3, 10.0, "HELP ME MOVE\nMY SOFA.", (760, 820), 'say'),
               (10.1, 11.6, "...GOODNIGHT.", (360, 820), 'say'),
               (11.7, 13.2, "IT'S 2:32 PM!", (760, 820), 'say')]
    events = [('boom', 0.0), ('thud', 0.3), ('tick', 2.0), ('tick', 2.4), ('thud', 3.6), ('tick', 5.4), ('tick', 5.8),
              ('whoosh', 6.5), ('thud', 8.3), ('pop', 10.1), ('chime', 11.7), ('whoosh', 13.6)]

    @staticmethod
    def make_bg():
        img = make_bedroom()
        g = vgrad(280, (120, 180, 240), (200, 225, 250)).astype(np.uint8)
        img[615:895, 765:875] = g[:280, None, :][:, :, :]
        img[615:895, 885:995] = g[:280, None, :][:, :, :]
        cv2.circle(img, (940, 680), 26, (255, 236, 160), -1, cv2.LINE_AA)
        return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.35, 380, 950)), (1.9, (1.3, 380, 950)), (2.0, (1.3, 420, 950)), (5.1, (1.25, 400, 950)),
                      (5.3, (1.0, 540, 960)), (6.4, (1.0, 540, 960)), (6.5, (1.3, 760, 950)), (10.0, (1.3, 760, 950)),
                      (10.1, (1.35, 380, 950)), (11.6, (1.35, 380, 950)), (11.7, (1.0, 540, 960)), (21.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if t < 0.5: return 1 - prog(t, 0, 0.5)
        if 3.6 <= t < 4.1: return 0.8 * (1 - prog(t, 3.6, 4.1))
        return 0.0

    @staticmethod
    def world(img, t):
        # bedside clock
        ck = fit_sprite('2:31 PM' if t < 11.7 else '2:32 PM', RED, 34, 200)
        cv2.rectangle(img, (895, 1030), (995, 1078), (20, 18, 22), -1)
        blit(img, ck, 945 - ck.shape[1] / 2, 1038)
        sleepy = 10.1 <= t < 11.7
        shock = 3.6 <= t < 5.1
        jump = t < 1.9
        hm = 'smile' if jump else ('sad' if (shock or 2.0 <= t < 3.6 or 8.3 <= t < 10.1) else 'flat')
        p = person(img, 360, face=1, sitk=1, mood=hm, eyes_closed=sleepy or t >= 11.7,
                   front=(150, -40) if (jump or shock) else ((22, 98) if 2.0 <= t < 3.6 else (35, 75)),
                   rear=(-150, -30) if (jump or shock) else (-6, 10),
                   bob=-16 * abs(math.sin(t * 10)) if jump else 0, headdown=18 if t >= 10.1 else 0)
        if 2.0 <= t < 3.6: phone(img, p['fh'], on=True)
        if t >= 5.3:
            fx = kf(t, [(5.3, 1180), (6.4, 760)])
            person(img, fx, face=-1, hair=True, mood='smile' if t < 11.7 else 'angry',
                   front=(60, 40) if (6.5 <= t < 10.0 or 11.7 <= t < 13.2) else (10, 14),
                   walk=(t * 7, 1.0) if t < 6.4 else None)
        if t >= 10.4:
            for j in range(3):
                k = ((t - 10.4) * 0.8 + j * 0.33) % 1
                sp = label_sprite('Z', (180, 190, 230), int(30 + 20 * k))
                blit(img, sp, 430 + 50 * k + j * 10, 760 - 140 * k, 1 - k)

    @staticmethod
    def ui(img, t):
        if t >= 13.6:
            dim(img, t, 13.6)
            caption(img, 'How are you surviving / *the last 48 hours?*', t, 13.8, 30, 900, 60)
            caption(img, 'Best answer gets pinned.', t, 15.0, 30, 1130, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 15.6, 30, 1210, 40, GREY, POPM)
            caption(img, DISC, t, 16.2, 30, 1300, 30, FAINT, POPM)


VIDS = {'1': Hours48, '2': DeadRemote, '3': TwoDaysWhich, '4': Myths4, '5': NapSkip}

if __name__ == '__main__':
    V = VIDS[sys.argv[1]]
    if len(sys.argv) > 2:
        f = frame_fn_v2(V, V.make_bg())
        ims = [cv2.resize(cv2.cvtColor(f(float(x)), cv2.COLOR_RGB2BGR), (432, 768)) for x in sys.argv[2:]]
        cv2.imwrite(f'{OUT}/still_{sys.argv[1]}.jpg', np.hstack(ims), [cv2.IMWRITE_JPEG_QUALITY, 82])
    else:
        build_v2(V, OUT, seed=int(sys.argv[1]) * 17); print('done', V.name)
