"""GTA 6 fan Shorts, batch 6 (2026-11-18, launch eve, VIRAL FORMAT v2). 100% original visuals: stick figures, neon shapes, text cards.
Facts (sources in TOPICS.md): out Thursday 19 Nov 2026 on PS5 + Xbox Series X|S (Rockstar Newswire). The Game Awards 2026
nominations (17 Nov): GTA 6 is the most nominated game, 8 nominations incl. Game of the Year and Best Score and Music; show 10 Dec 2026
(VGC, Push Square, Variety). Pre-release Metacritic USER score of 6.5 from only 5 user ratings, before release (Men's Journal, 16 Nov).
The first Grand Theft Auto came out in 1997. Unlock time and review dates are NOT stated anywhere in this batch."""
import math, sys, os, cv2, numpy as np
from engine import *
from viral import frame_fn_v2, build_v2, make_bedroom
from gta_example import controller
from videos_gta_d1 import (room_bg, sofa, neon_bg, dim, fit_sprite, big_text, stamp, progress_bar,
                           FL, GREEN, PINK, CYAN, DISC)
from videos_gta_d4 import ncard

OUT = '/home/claude/shorts/out_2026-11-18'
os.makedirs(OUT, exist_ok=True)
GREY = (200, 200, 206)
FAINT = (130, 130, 138)

def trophy(img, c, k, col=GOLD):
    if k <= 0: return
    x, y = c; s = 70 * k
    glow(img, (x, y), 260 * k, GOLD, 0.35)
    poly(img, [(x - s, y - s), (x + s, y - s), (x + 0.6 * s, y + 0.3 * s), (x - 0.6 * s, y + 0.3 * s)], col)
    ellipse(img, (x - s, y - 0.55 * s), (0.4 * s, 0.4 * s), 0, 90, 270, col, int(max(2, 10 * k)))
    ellipse(img, (x + s, y - 0.55 * s), (0.4 * s, 0.4 * s), 0, -90, 90, col, int(max(2, 10 * k)))
    poly(img, [(x - 0.15 * s, y + 0.3 * s), (x + 0.15 * s, y + 0.3 * s), (x + 0.15 * s, y + 0.8 * s), (x - 0.15 * s, y + 0.8 * s)], col)
    poly(img, [(x - 0.6 * s, y + 0.8 * s), (x + 0.6 * s, y + 0.8 * s), (x + 0.6 * s, y + 1.05 * s), (x - 0.6 * s, y + 1.05 * s)], col)

# =========================================================
# M1  Countdown: 1 day left, already up for Game of the Year
# =========================================================
class GotyEve:
    name = '2026-11-18_gta6_1_day_up_for_goty'; dur = 23.0
    banner = "NOT EVEN OUT YET. / *ALREADY UP FOR GOTY.*"
    prog = ['Em', 'C', 'G', 'D']; bpm = 116
    bubbles = [(1.4, 3.0, "1 DAY TO GTA 6!", (380, 1080), 'say'),
               (3.1, 4.7, "AND IT'S UP FOR\nGAME OF THE YEAR.", (720, 1080), 'say'),
               (13.6, 15.1, "SO I'M PLAYING A\nFUTURE WINNER?", (380, 1080), 'say'),
               (15.2, 16.8, "WE FIND OUT\n10 DECEMBER.", (720, 1080), 'say')]
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
        if 3.1 <= t < 3.5: return 0.6 * (1 - prog(t, 3.1, 3.5))
        if 11.0 <= t < 11.5: return 0.8 * (1 - prog(t, 11.0, 11.5))
        return 0.0

    @staticmethod
    def world(img, t):
        if t < 4.9 or 13.3 <= t < 17.1:
            if 3.1 <= t < 4.9 or 13.3 <= t < 17.1:
                trophy(img, (550, 1230), eo(prog(t, 3.1 if t < 4.9 else 13.3, (3.1 if t < 4.9 else 13.3) + 0.4)))
            wow = 3.1 <= t < 4.9
            p = person(img, 380, y=1620, face=1, mood='smile',
                       front=(150, -50) if wow else (35, 75), rear=(-150, -40) if wow else (-6, 10),
                       bob=-12 * abs(math.sin(t * 10)) if wow else 0)
            if not wow: controller(img, p['fh'])
            q = person(img, 720, y=1620, face=-1, mood='smile',
                       front=(40, 60) if t < 3.1 else ((60, 40) if (3.1 <= t < 4.7 or 15.2 <= t < 16.8) else (10, 14)))
            if t < 3.1: phone(img, q['fh'], on=True)

    @staticmethod
    def ui(img, t):
        if t < 1.4:
            d = '2' if t < 0.5 else '1'
            glow(img, (540, 760), 420, PINK, 0.5)
            big_text(img, d, t, 0.5 if d == '1' else 0.0, 700, 380, WHITE, GOLD, pop=d == '1')
            big_text(img, 'DAY LEFT' if d == '1' else 'DAYS LEFT', t, 0.0, 960, 96, GOLD, GOLD, pop=False)
        elif t < 4.9:
            big_text(img, '*1* DAY LEFT', t, 1.4, 1760, 90, WHITE, GOLD, pop=False)
        if 4.9 <= t < 13.4 or t >= 17.0:
            dim(img, t, 4.9 if t < 13.4 else 17.0)
        if 4.9 <= t < 13.4:
            big_text(img, "THE GAME AWARDS *2026*", t, 4.9, 520, 60, WHITE, GOLD, pop=False)
            ncard(img, t, 5.1, 600, '8', 'NOMINATIONS FOR GTA 6', 'THE MOST OF ANY GAME THIS YEAR', GOLD, 90)
            ncard(img, t, 7.6, 830, 'GOTY', 'GAME OF THE YEAR', 'ONE OF 6 NOMINEES', CYAN, 56)
            ncard(img, t, 10.1, 1060, '10', 'DECEMBER: THE SHOW', 'WINNERS REVEALED LIVE', PINK, 90)
            caption(img, 'Nominated *before anyone played it.*', t, 11.0, 13.3, 1330, 52)
        if t >= 17.0:
            caption(img, 'Should a game be nominated / *before it is even out?*', t, 17.2, 30, 900, 58)
            caption(img, 'Comment YES or NO.', t, 18.4, 30, 1130, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 19.0, 30, 1210, 40, GREY, POPM)
            caption(img, DISC, t, 19.6, 30, 1300, 30, FAINT, POPM)

# =========================================================
# M2  Skit: he cleaned his room for GTA 6. Mum got suspicious.
# =========================================================
def sparkle(img, c, t, ph, col=(255, 240, 180)):
    k = 0.5 + 0.5 * math.sin(t * 6 + ph)
    x, y = c; r = 10 + 16 * k
    line(img, (x - r, y), (x + r, y), col, 4); line(img, (x, y - r), (x, y + r), col, 4)

def broom(img, hand):
    x, y = hand
    line(img, (x, y - 120), (x + 10, y + 150), (150, 110, 70), 8)
    poly(img, [(x - 25, y + 150), (x + 45, y + 150), (x + 60, y + 215), (x - 40, y + 215)], (200, 170, 90))

class CleanRoom:
    name = '2026-11-18_gta6_cleaned_room_mum_suspicious'; dur = 21.5
    banner = "CLEAN ROOM FOR GTA 6?! / *MUM GOT SUSPICIOUS.*"
    prog = ['C', 'Am', 'F', 'G']; bpm = 104
    bubbles = [(0.2, 1.9, "YOUR ROOM...\nIT'S CLEAN?!", (760, 880), 'say'),
               (2.0, 3.5, "BIG NIGHT\nTOMORROW.", (340, 880), 'say'),
               (3.6, 5.1, "BIG NIGHT?\nA DATE?!", (760, 880), 'think'),
               (5.2, 6.7, "WHO IS IT?!\nTELL ME!", (760, 880), 'say'),
               (6.8, 8.3, "...GTA 6, MUM.", (340, 880), 'say'),
               (8.4, 10.1, "THEN CLEAN THE\nKITCHEN FOR\nYOUR DATE TOO.", (760, 880), 'say'),
               (10.2, 11.7, "...DEAL.", (340, 880), 'say'),
               (11.8, 13.3, "WHO ARE YOU\nAND WHERE IS\nMY SON?", (760, 880), 'say')]
    events = [('boom', 0.0), ('chime', 0.3), ('thud', 2.0), ('whoosh', 3.6), ('thud', 5.2), ('boom', 6.8),
              ('tick', 8.4), ('thud', 10.2), ('chime', 11.8), ('whoosh', 13.6)]

    @staticmethod
    def make_bg():
        img = make_bedroom()
        cv2.rectangle(img, (930, 300), (1060, 1250), (70, 54, 44), -1)    # open door frame
        cv2.rectangle(img, (945, 315), (1045, 1250), (26, 24, 30), -1)
        return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.35, 760, 1080)), (1.9, (1.3, 760, 1080)), (2.0, (1.3, 340, 1080)), (3.5, (1.3, 340, 1080)),
                      (3.6, (1.3, 760, 1080)), (6.7, (1.3, 760, 1080)), (6.8, (1.35, 340, 1080)), (8.3, (1.35, 340, 1080)),
                      (8.4, (1.0, 540, 960)), (10.1, (1.0, 540, 960)), (10.2, (1.3, 340, 1080)), (11.7, (1.3, 340, 1080)),
                      (11.8, (1.0, 540, 960)), (21.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if t < 0.5: return 0.8 * (1 - prog(t, 0, 0.5))
        if 6.8 <= t < 7.3: return 0.7 * (1 - prog(t, 6.8, 7.3))
        return 0.0

    @staticmethod
    def world(img, t):
        for i, c in enumerate([(220, 1080), (520, 1060), (700, 1290), (140, 1330), (860, 1010)]):
            sparkle(img, c, t, i * 1.3)
        lab = fit_sprite('THE NIGHT BEFORE GTA 6', GOLD, 32, 600); blit(img, lab, 540 - lab.shape[1] / 2, 1730)
        mum_talk = any(a <= t < b for a, b in [(0.2, 1.9), (5.2, 6.7), (8.4, 10.1), (11.8, 13.3)])
        shock = t < 1.9 or 11.8 <= t < 13.3
        mm = 'sad' if (shock and t < 1.9) else ('smile' if 3.6 <= t < 6.7 or t >= 8.4 else 'flat')
        person(img, 760, y=1500, face=-1, hair=True, mood=mm,
               front=(150, -40) if shock else ((60, 40) if mum_talk else (10, 14)),
               rear=(-150, -30) if shock else (-6, 10), bob=-10 * abs(math.sin(t * 9)) if 3.6 <= t < 6.7 else 0)
        sad = 8.4 <= t < 10.2
        p = person(img, 340, y=1500, face=1, mood='sad' if sad else ('smile' if t < 6.8 or t >= 10.2 else 'flat'),
                   front=(40, 30), headdown=12 if sad else 0)
        broom(img, p['fh'])
        if 3.6 <= t < 6.7:
            for j in range(2): pop_heart(img, (640 + j * 90, 1000), t, 3.6 + j * 0.3, 40)

    @staticmethod
    def ui(img, t):
        if t >= 13.6:
            dim(img, t, 13.6)
            caption(img, "What's YOUR launch night / *prep ritual?*", t, 13.8, 30, 900, 60)
            caption(img, 'Best answer gets pinned.', t, 15.0, 30, 1130, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 15.6, 30, 1210, 40, GREY, POPM)
            caption(img, DISC, t, 16.2, 30, 1300, 30, FAINT, POPM)

# =========================================================
# M3  Which gamer are you on GTA 6 eve?
# =========================================================
PANELS = [((275, 680), '1. THE CHARGER'), ((805, 680), '2. THE EARLY SLEEPER'),
          ((275, 1170), '3. THE GROUP CHAT'), ((805, 1170), '4. THE VIBE SETTER')]

def battery(img, x, y, frac, col):
    cv2.rectangle(img, (x, y), (x + 70, y + 32), (200, 200, 210), 3)
    cv2.rectangle(img, (x + 70, y + 9), (x + 78, y + 23), (200, 200, 210), -1)
    cv2.rectangle(img, (x + 5, y + 5), (x + 5 + int(60 * frac), y + 27), col, -1)

def panel(img, t, i, active):
    (cx, cy), lab = PANELS[i]
    x0, y0, x1, y1 = cx - 245, cy - 220, cx + 245, cy + 220
    keep = img.copy()
    cv2.rectangle(img, (x0, y0), (x1, y1), (24, 22, 34), -1)
    gy = cy + 160
    if i == 0:
        for j in range(3):
            battery(img, cx + 60, cy - 160 + j * 55, 0.3 + 0.7 * (((t * 0.5) + j * 0.3) % 1), GREEN)
        p = person(img, cx - 80, y=gy, s=0.48, face=1, mood='smile', front=(40, 60))
        controller(img, p['fh'])
    elif i == 1:
        sp = fit_sprite('7:00 PM', RED, 30, 200)
        cv2.rectangle(img, (cx + 60, cy - 30), (cx + 220, cy + 20), (14, 14, 18), -1)
        blit(img, sp, cx + 140 - sp.shape[1] / 2, cy - 24)
        cv2.rectangle(img, (cx - 210, gy - 40), (cx + 60, gy), (80, 76, 96), -1)
        person(img, cx - 80, y=gy - 40, s=0.48, face=1, mood='flat', eyes_closed=True, front=(30, 70), headdown=10)
        for j in range(3):
            k = ((t * 0.8) + j * 0.33) % 1
            sp = label_sprite('Z', (180, 190, 230), int(24 + 16 * k))
            blit(img, sp, cx - 30 + 40 * k + j * 8, cy - 40 - 110 * k, 1 - k)
    elif i == 2:
        p = person(img, cx - 80, y=gy, s=0.48, face=1, mood='smile', front=(40, 60))
        phone(img, p['fh'], on=True)
        n = 900 + int(t * 37) % 99
        cv2.circle(img, (cx + 130, cy - 20), 62, RED, -1, cv2.LINE_AA)
        sp = fit_sprite(f'{n}+', WHITE, 34, 110); blit(img, sp, cx + 130 - sp.shape[1] / 2, cy - 40)
    else:
        k = 0.5 + 0.5 * math.sin(t * 3)
        glow(img, (cx + 100, cy - 90), 160, PINK, 0.35 * k + 0.15)
        glow(img, (cx - 100, cy - 120), 140, CYAN, 0.25 * (1 - k) + 0.1)
        p = person(img, cx - 40, y=gy, s=0.48, face=1, mood='smile', front=(40, 60))
        hx, hy = p['head'] if 'head' in p else (cx - 40, gy - 230)
        cv2.rectangle(img, (int(hx - 18), int(hy - 8)), (int(hx + 26), int(hy + 6)), (10, 10, 14), -1)
        controller(img, p['fh'])
    m = np.ones(img.shape[:2], bool); m[y0:y1, x0:x1] = False
    img[m] = keep[m]
    col = GOLD if active else (60, 60, 72)
    cv2.rectangle(img, (x0, y0), (x1, y1), col, 6 if active else 3)
    blit(img, fit_sprite(lab, GOLD if active else (150, 150, 160), 26, 460), x0 + 12, y1 - 50)
    if not active:
        sub = img[y0 + 3:y1 - 2, x0 + 3:x1 - 2]
        sub[:] = (sub * 0.45).astype(np.uint8)

class EveWhich:
    name = '2026-11-18_gta6_eve_which_gamer'; dur = 22.5
    banner = "GTA 6 IS TOMORROW. / *WHICH GAMER ARE YOU?*"
    prog = ['A', 'E', 'F#m', 'D']; bpm = 118
    bubbles = [(0.2, 2.4, "3 CONTROLLERS.\nALL AT 100%.", (315, 595), 'say'),
               (2.7, 5.0, "ZZZ... WAKE ME\nFOR GTA 6.", (845, 595), 'think'),
               (5.3, 7.6, "WHO'S ONLINE\nTOMORROW?!", (315, 1085), 'say'),
               (7.9, 10.2, "IT'S ABOUT\nTHE VIBE.", (845, 1085), 'say'),
               (12.0, 13.4, "YOU SAID YOU'D\nWAIT A WEEK!", (760, 960), 'say'),
               (13.5, 14.9, "I SAID\nA WEEK-ISH.", (330, 800), 'say')]
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
            caught = t >= 12.0
            p = person(img, 330, y=FL, face=1, mood='smile' if 13.5 <= t < 15.2 else 'flat',
                       front=(35, 75), bob=-8 * abs(math.sin(t * 12)) if t < 12.0 else 0)
            controller(img, p['fh'])
            sp = fit_sprite('DAY 1. MINUTE 1.', CYAN, 30, 400); blit(img, sp, 330 - sp.shape[1] / 2, 1450)
            person(img, 760, y=FL, face=-1, mood='angry' if caught and t < 13.5 else 'smile',
                   front=(150, -30) if 12.0 <= t < 13.4 else (10, 14))

    @staticmethod
    def ui(img, t):
        if 10.4 <= t < 12.0:
            a = win(t, 10.4, 11.8, 0.2)
            dim(img, t, 10.4, 0.5 * a)
            caption(img, "...and there's *always a #5.*", t, 10.5, 11.8, 1250, 70)
        if 12.0 <= t < 15.4:
            caption(img, '5. *"I\'LL WAIT FOR REVIEWS"*', t, 12.0, 15.2, 1560, 54)
        if t >= 15.4:
            dim(img, t, 15.4)
            caption(img, 'Which one are you? / *Comment 1 to 5.*', t, 15.6, 30, 1050, 58)
            caption(img, 'Tag your friend who is number 5.', t, 16.8, 30, 1240, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 17.4, 30, 1330, 42, GREY, POPM)
            caption(img, DISC, t, 17.8, 30, 1440, 30, FAINT, POPM)

# =========================================================
# M4  GTA 6 already has a score? 4 claims checked
# =========================================================
QUIZ = [("GTA 6 ALREADY HAS A\nMETACRITIC SCORE", 'USER SCORE ONLY', GOLD, 'USER RATINGS BEFORE RELEASE. NOT CRITICS'),
        ("A 6.5 USER SCORE MEANS\nGTA 6 IS BAD", 'MISLEADING', RED, 'IT CAME FROM 5 RATINGS. NOBODY HAD PLAYED IT'),
        ("IT'S NOMINATED FOR\nBEST SCORE AND MUSIC", 'TRUE', GREEN, 'ONE OF ITS 8 GAME AWARDS NOMINATIONS'),
        ("LAUNCH DAY IS\nTOMORROW", 'TRUE', GREEN, 'THURSDAY 19 NOVEMBER 2026. ROCKSTAR')]
QT = 3.4

class ScoreCheck:
    name = '2026-11-18_gta6_already_has_a_score'; dur = 21.5
    banner = "GTA 6 ALREADY HAS A SCORE? / *READ THE SMALL PRINT.*"
    prog = ['Gm', 'Eb', 'Bb', 'F']; bpm = 120
    bubbles = [(5.6, 6.9, "5 RATINGS?!\nTHAT'S IT?!", (820, 1330), 'say')]
    events = sum([[('tick', i * QT + 0.4), ('tick', i * QT + 1.0), ('tick', i * QT + 1.6),
                   ('boom' if i == 1 else 'thud', i * QT + 2.0), ('whoosh', i * QT + 3.3)] for i in range(4)], []) + \
             [('chime', 14.0)]

    @staticmethod
    def make_bg(): return room_bg(tv=False)

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.0, 540, 960)), (5.4, (1.0, 540, 960)), (5.6, (1.0, 540, 960)), (6.9, (1.0, 540, 960)),
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
            num = label_sprite(f'CLAIM #{i + 1} OF 4', GOLD, 34); blit(img, num, 540 - num.shape[1] / 2, 470)
            cv2.rectangle(img, (70, 540), (1010, 860), (24, 22, 36), -1)
            cv2.rectangle(img, (70, 540), (1010, 860), (90, 80, 130), 4)
            for j, ln in enumerate(st.split('\n')):
                sp = fit_sprite(ln, WHITE, 46, 880); blit(img, sp, 540 - sp.shape[1] / 2, 610 + j * 100)
            if lt < 2.0: progress_bar(img, 190, 900, 700, 1 - lt / 2.0, GOLD, 22)
            stamp(img, verdict, t, i * QT + 2.0, (540, 990), col, 50 if len(verdict) > 10 else (58 if len(verdict) > 6 else 64))
            if lt >= 2.2:
                sp = fit_sprite(nt, (210, 210, 220), 28, 960); blit(img, sp, 540 - sp.shape[1] / 2, 1085)
            mood = 'sad' if shock else ('smile' if lt >= 2.0 else 'flat')
        else:
            mood = 'smile'
        p = person(img, 820, y=1840, s=0.75, face=-1, mood=mood,
                   front=(150, 15) if shock else (35, 75), rear=(-150, -15) if shock else (-6, 10))
        if not shock: controller(img, p['fh'])

    @staticmethod
    def ui(img, t):
        if t >= 13.7:
            dim(img, t, 13.7)
            caption(img, 'Day-one player or / *waiting for real reviews?*', t, 13.9, 30, 820, 58)
            caption(img, 'Comment DAY ONE or WAIT.', t, 15.2, 30, 1060, 40, GREY, POPM)
            caption(img, 'User score reported by Men\'s Journal, 16 Nov.', t, 15.6, 30, 1140, 30, FAINT, POPM)
            caption(img, DISC, t, 16.0, 30, 1200, 30, FAINT, POPM)

# =========================================================
# M5  Skit: he said dad wouldn't get GTA 6. Dad was there in 1997.
# =========================================================
class Dad1997:
    name = '2026-11-18_gta6_dad_was_there_in_1997'; dur = 22.0
    banner = "DAD WOULDN'T GET GTA 6? / *THEN DAD SPOKE.*"
    prog = ['Dm', 'Bb', 'F', 'C']; bpm = 100
    bubbles = [(0.2, 1.9, "DAD, YOU WOULDN'T\nGET GTA 6.", (330, 960), 'say'),
               (2.0, 3.5, "WOULDN'T\nGET IT?", (760, 960), 'say'),
               (3.6, 5.1, "IT'S FOR\nREAL GAMERS.", (330, 960), 'say'),
               (5.2, 6.9, "SON. I PLAYED\nTHE FIRST ONE.", (760, 960), 'say'),
               (7.0, 8.4, "THE FIRST\nONE?!", (330, 960), 'say'),
               (10.0, 11.6, "BEFORE YOU\nWERE BORN.", (760, 960), 'say'),
               (11.7, 13.3, "...PLAYER 2,\nDAD?", (330, 960), 'say')]
    events = [('pop', 0.0), ('thud', 2.0), ('tick', 3.6), ('thud', 5.2), ('boom', 7.0), ('boom', 8.5),
              ('chime', 10.0), ('pop', 11.7), ('whoosh', 13.8)]

    @staticmethod
    def make_bg():
        img = room_bg(); sofa(img, 120, 960); return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.35, 330, 1080)), (1.9, (1.3, 330, 1080)), (2.0, (1.3, 760, 1080)), (3.5, (1.3, 760, 1080)),
                      (3.6, (1.3, 330, 1080)), (5.1, (1.3, 330, 1080)), (5.2, (1.35, 760, 1080)), (6.9, (1.35, 760, 1080)),
                      (7.0, (1.35, 330, 1080)), (8.4, (1.35, 330, 1080)), (8.5, (1.0, 540, 960)), (21.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if 7.0 <= t < 7.5: return 0.8 * (1 - prog(t, 7.0, 7.5))
        if 8.5 <= t < 9.0: return 1 - prog(t, 8.5, 9.0)
        return 0.0

    @staticmethod
    def world(img, t):
        if t >= 8.5:
            k = eo(prog(t, 8.5, 8.9))
            glow(img, (540, 625), 380, GOLD, 0.4 * k)
            if k > 0: big_text(img, '*1997*', t, 8.5, 600, 170, WHITE, GOLD)
            sp = fit_sprite('THE FIRST GRAND THEFT AUTO', (220, 220, 230), 30, 760)
            if t >= 8.8: blit(img, sp, 540 - sp.shape[1] / 2, 720)
        else:
            sp = fit_sprite('GTA 6: TOMORROW', (180, 170, 220), 40, 700); blit(img, sp, 540 - sp.shape[1] / 2, 740)
        shock = 7.0 <= t < 10.0
        sm_ = 'sad' if shock else ('smile' if t >= 11.7 or t < 2.0 else 'flat')
        p = person(img, 330, y=FL, face=1, sitk=1, mood=sm_,
                   front=(150, -30) if shock else ((60, 30) if (t < 1.9 or 3.6 <= t < 5.1) else (35, 75)),
                   rear=(-150, -20) if shock else (-6, 10))
        if not shock and not (t < 1.9 or 3.6 <= t < 5.1): controller(img, p['fh'])
        dm = 'smile' if t >= 5.2 else 'flat'
        d = person(img, 760, y=FL, s=1.05, face=-1, sitk=1, mood=dm,
                   front=(60, 40) if (2.0 <= t < 3.5 or 5.2 <= t < 6.9 or 10.0 <= t < 11.6) else (35, 75))
        hx, hy = d['fh'] if t < 2.0 else d['fh']
        if t >= 11.9: controller(img, d['fh'])
        if t >= 11.7: pop_heart(img, (545, 880), t, 11.9, 45)

    @staticmethod
    def ui(img, t):
        if t >= 13.8:
            dim(img, t, 13.8)
            caption(img, 'Who got YOU / *into gaming?*', t, 14.0, 30, 900, 62)
            caption(img, 'Tag them below.', t, 15.2, 30, 1130, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 15.8, 30, 1210, 40, GREY, POPM)
            caption(img, DISC, t, 16.4, 30, 1300, 30, FAINT, POPM)


VIDS = {'1': GotyEve, '2': CleanRoom, '3': EveWhich, '4': ScoreCheck, '5': Dad1997}

if __name__ == '__main__':
    V = VIDS[sys.argv[1]]
    if len(sys.argv) > 2:
        f = frame_fn_v2(V, V.make_bg())
        ims = [cv2.resize(cv2.cvtColor(f(float(x)), cv2.COLOR_RGB2BGR), (432, 768)) for x in sys.argv[2:]]
        cv2.imwrite(f'{OUT}/still_{sys.argv[1]}.jpg', np.hstack(ims), [cv2.IMWRITE_JPEG_QUALITY, 82])
    else:
        build_v2(V, OUT, seed=int(sys.argv[1]) * 17); print('done', V.name)
