"""GTA 6 fan Shorts, batch 4 (2026-11-16, VIRAL FORMAT v2). 100% original visuals: stick figures, neon shapes, text cards.
Facts (sources in TOPICS.md): out Thursday 19 Nov 2026 on PS5 + Xbox Series X|S (Rockstar Newswire); Take-Two Q2 FY27
(9 Nov): "Pre-orders ... are tracking far above our initial expectations" (Shacknews); The Game Awards cut-off is
Fri 20 Nov, so GTA 6 is eligible (GamesRadar, per TGA criteria). NOT CONFIRMED: "$1 billion pre-sales" (analyst estimates /
reports, no Take-Two number), "~90% Ultimate Edition" (unverified report), GTA Online for GTA 6 date (reports only)."""
import math, sys, os, cv2, numpy as np
from engine import *
from viral import frame_fn_v2, build_v2
from gta_example import controller
from videos_gta_d1 import (room_bg, sofa, neon_bg, dim, fit_sprite, card, big_text, stamp, progress_bar,
                           burst, FL, GREEN, PINK, CYAN, DISC)

OUT = '/home/claude/shorts/out_2026-11-16'
os.makedirs(OUT, exist_ok=True)
GREY = (200, 200, 206)
FAINT = (130, 130, 138)

def ncard(img, t, t0, y, num, text, sub, accent, numsize=64):
    if t < t0: return
    k = eo(prog(t, t0, t0 + 0.35))
    x = lerp(-960, 70, k)
    over = img.copy()
    cv2.rectangle(over, (int(x), y), (int(x) + 940, y + 190), (18, 16, 26), -1)
    cv2.rectangle(over, (int(x), y), (int(x) + 16, y + 190), accent, -1)
    img[:] = (img * 0.03 + over * 0.97).astype(np.uint8)
    ns = fit_sprite(num, accent, numsize, 170)
    blit(img, ns, x + 105 - ns.shape[1] / 2, y + 95 - ns.shape[0] / 2)
    blit(img, fit_sprite(text, WHITE, 42, 700), x + 210, y + 40)
    blit(img, fit_sprite(sub, (185, 185, 194), 28, 700), x + 212, y + 118)

# =========================================================
# J1  Countdown: 3 days, 3 numbers (#3 is not confirmed)
# =========================================================
class ThreeNumbers:
    name = '2026-11-16_gta6_3_days_3_numbers'; dur = 23.0
    banner = "GTA 6 IN 3 DAYS: 3 NUMBERS. / *#3 ISN'T WHAT YOU THINK.*"
    prog = ['Em', 'C', 'G', 'D']; bpm = 112
    bubbles = [(1.4, 3.0, "3 DAYS.\nI CAN'T WAIT.", (380, 1080), 'say'),
               (3.1, 4.7, "LOOK AT\nTHESE NUMBERS.", (720, 1080), 'say'),
               (13.6, 15.1, "WAIT... THAT'S\nNOT OFFICIAL?!", (380, 1080), 'say'),
               (15.2, 16.8, "NOPE. NO REAL\nNUMBER YET.", (720, 1080), 'say')]
    events = [('tick', 0.0), ('boom', 0.5), ('thud', 3.1), ('whoosh', 4.9), ('thud', 5.1), ('thud', 7.6),
              ('thud', 10.1), ('boom', 11.2), ('thud', 13.6), ('chime', 15.2), ('whoosh', 17.0)]

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
        if 11.2 <= t < 11.7: return 1 - prog(t, 11.2, 11.7)
        if 13.6 <= t < 14.0: return 0.7 * (1 - prog(t, 13.6, 14.0))
        return 0.0

    @staticmethod
    def world(img, t):
        if t < 4.9 or 13.3 <= t < 17.1:
            shock = 13.6 <= t < 15.2
            m = 'sad' if shock else 'smile'
            p = person(img, 380, y=1620, face=1, mood=m, front=(150, 20) if shock else (35, 75),
                       rear=(-150, -20) if shock else (-6, 10), bob=-14 * abs(math.sin(t * 9)) if shock else 0)
            if not shock: controller(img, p['fh'])
            person(img, 720, y=1620, face=-1, mood='flat' if t >= 13.3 else 'smile',
                   front=(60, 40) if (3.1 <= t < 4.7 or 15.2 <= t < 16.8) else (10, 14))

    @staticmethod
    def ui(img, t):
        if t < 1.4:
            d = '4' if t < 0.5 else '3'
            glow(img, (540, 760), 420, PINK, 0.5)
            big_text(img, d, t, 0.5 if d == '3' else 0.0, 700, 380, WHITE, GOLD, pop=d == '3')
            big_text(img, 'DAYS LEFT', t, 0.0, 950, 96, GOLD, GOLD, pop=False)
        elif t < 4.9:
            big_text(img, '*3* DAYS LEFT', t, 1.4, 1740, 90, WHITE, GOLD, pop=False)
        if 4.9 <= t < 13.4 or t >= 17.0:
            dim(img, t, 4.9 if t < 13.4 else 17.0)
        if 4.9 <= t < 13.4:
            big_text(img, '3 *NUMBERS*', t, 4.9, 520, 64, WHITE, GOLD, pop=False)
            ncard(img, t, 5.1, 600, '19', 'THURSDAY = LAUNCH DAY', 'NOV 19. CONFIRMED BY ROCKSTAR', GOLD)
            ncard(img, t, 7.6, 830, '2', 'CONSOLES AT LAUNCH', 'PS5 + XBOX SERIES X|S', CYAN)
            ncard(img, t, 10.1, 1060, '$1B', 'PRE-SALES?', 'YOU KEEP SEEING THIS NUMBER...', PINK)
            stamp(img, 'NOT CONFIRMED', t, 11.2, (560, 1310), RED, 54)
            caption(img, 'Take-Two only said: *far above expectations.*', t, 11.8, 13.3, 1460, 40)
        if t >= 17.0:
            caption(img, 'Will GTA 6 win / *Game of the Year?*', t, 17.2, 30, 900, 62)
            caption(img, 'Yes or no in the comments.', t, 18.4, 30, 1130, 42, GREY, POPM)
            caption(img, DISC, t, 19.0, 30, 1210, 30, FAINT, POPM)

# =========================================================
# J2  Skit: he hung up on a "spoiler" call. It was his gran.
# =========================================================
def table_phone(img, t, ring, caller=None):
    x, y = 470, 1250
    cv2.rectangle(img, (380, 1270), (560, 1290), (70, 56, 48), -1)
    cv2.rectangle(img, (395, 1290), (410, FL), (50, 40, 36), -1); cv2.rectangle(img, (530, 1290), (545, FL), (50, 40, 36), -1)
    if ring:
        glow(img, (x, y), 150, BLUE, 0.35)
        for k in (1, 2):
            r = 40 + k * 20 + 8 * math.sin(t * 30)
            ellipse(img, (x, y), (r, r * 0.6), 0, 200, 340, (150, 195, 255), 3)
            ellipse(img, (x, y), (r, r * 0.6), 0, 20, 160, (150, 195, 255), 3)
    poly(img, [(x - 40, y - 10), (x + 40, y - 10), (x + 40, y + 12), (x - 40, y + 12)], (40, 42, 50))
    if ring: poly(img, [(x - 36, y - 7), (x + 36, y - 7), (x + 36, y + 9), (x - 36, y + 9)], (150, 195, 255))
    if caller:
        sp = fit_sprite(caller, WHITE, 30, 400); blit(img, sp, x - sp.shape[1] / 2, y - 120)

class SpoilerGran:
    name = '2026-11-16_gta6_spoiler_call_gran'; dur = 22.5
    banner = "A GTA 6 SPOILER CALL. / *HE HUNG UP TOO FAST.*"
    prog = ['Dm', 'Bb', 'F', 'C']; bpm = 104
    bubbles = [(0.2, 1.9, "DID YOU SEE WHAT\nHAPPENS IN THE...", (470, 1110), 'say'),
               (2.0, 3.5, "NO SPOILERS!!", (760, 960), 'say'),
               (3.6, 5.1, "MUTED. BLOCKED.\nNOBODY RUINS\nTHIS FOR ME.", (760, 960), 'think'),
               (6.7, 8.5, "...IN THE MENU?\nI CAN'T FIND\nTHE START BUTTON!", (330, 860), 'say'),
               (8.6, 10.0, "GRAN?! YOU\nBOUGHT GTA 6?!", (760, 960), 'say'),
               (10.1, 11.8, "I WANTED TO\nPLAY WITH YOU,\nLOVE.", (330, 860), 'say'),
               (11.9, 13.4, "SIT DOWN.\nI'LL SHOW YOU.", (760, 960), 'say')]
    events = [('boom', 0.0), ('tick', 0.3), ('tick', 0.6), ('thud', 2.0), ('whoosh', 3.6), ('tick', 5.2), ('tick', 5.5),
              ('boom', 5.9), ('thud', 6.7), ('chime', 8.6), ('pop', 10.1), ('pop', 11.9), ('whoosh', 13.8)]

    @staticmethod
    def make_bg():
        img = room_bg(); sofa(img, 600, 1040); return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.35, 500, 1150)), (1.9, (1.3, 500, 1150)), (2.0, (1.3, 780, 1050)), (5.1, (1.25, 780, 1050)),
                      (5.3, (1.0, 540, 960)), (6.6, (1.0, 540, 960)), (6.7, (1.3, 340, 1000)), (8.5, (1.3, 340, 1000)),
                      (8.6, (1.3, 780, 1050)), (10.0, (1.3, 780, 1050)), (10.1, (1.0, 540, 960)), (22.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if 2.0 <= t < 2.5: return 1 - prog(t, 2.0, 2.5)
        if 5.9 <= t < 6.3: return 0.7 * (1 - prog(t, 5.9, 6.3))
        return 0.0

    @staticmethod
    def world(img, t):
        tv_on = True
        sp = fit_sprite('PRESS START', (200, 200, 220), 40, 600)
        blit(img, sp, 540 - sp.shape[1] / 2, 740 + 6 * math.sin(t * 3))
        table_phone(img, t, t < 1.9, 'INCOMING CALL' if t < 1.9 else None)
        if 5.9 <= t < 6.7:
            a = fit_sprite('KNOCK KNOCK', GOLD, 46, 600); blit(img, a, 540 - a.shape[1] / 2, 1500)
        shout = 2.0 <= t < 3.6
        shock = 8.6 <= t < 10.0
        hm = 'angry' if shout else ('sad' if shock else ('smile' if t >= 11.9 else 'flat'))
        p = person(img, 800, y=FL, face=-1, sitk=1, mood=hm,
                   front=(150, -30) if shout or shock else (35, 75), rear=(-150, -20) if shout or shock else (-6, 10),
                   bob=-12 * abs(math.sin(t * 11)) if shout else 0)
        if not (shout or shock): controller(img, p['fh'])
        if t >= 5.9:
            gx = kf(t, [(5.9, 1180), (6.6, 330)])
            g = person(img, gx, y=FL, face=1, hair=True, dress=True, mood='smile' if t >= 10.1 else 'flat',
                       front=(60, 40) if 6.7 <= t < 8.5 else (35, 75))
            phone(img, g['fh'], on=True)
        if t >= 11.9: pop_heart(img, (560, 880), t, 11.9, 45)

    @staticmethod
    def ui(img, t):
        if t >= 13.8:
            dim(img, t, 13.8)
            caption(img, 'Who is watching you play / *GTA 6 first?*', t, 14.0, 30, 900, 58)
            caption(img, 'Tag them below.', t, 15.2, 30, 1130, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 15.8, 30, 1210, 40, GREY, POPM)
            caption(img, DISC, t, 16.4, 30, 1300, 30, FAINT, POPM)

# =========================================================
# J3  Which gamer are you in the first hour?
# =========================================================
PANELS = [((275, 680), '1. THE SKIPPER'), ((805, 680), '2. THE SETTINGS GUY'),
          ((275, 1170), '3. THE WANDERER'), ((805, 1170), '4. THE NARRATOR')]

def panel(img, t, i, active):
    (cx, cy), lab = PANELS[i]
    x0, y0, x1, y1 = cx - 245, cy - 220, cx + 245, cy + 220
    keep = img.copy()
    cv2.rectangle(img, (x0, y0), (x1, y1), (24, 22, 34), -1)
    gy = cy + 160
    if i == 0:
        cv2.rectangle(img, (cx + 40, cy - 110), (cx + 210, cy - 40), (236, 236, 240), -1)
        sp = label_sprite('SKIP', INK, 34); blit(img, sp, cx + 125 - sp.shape[1] / 2, cy - 100)
        k = (t * 3) % 1
        if k < 0.5: cv2.rectangle(img, (cx + 34, cy - 116), (cx + 216, cy - 34), GOLD, 5)
        p = person(img, cx - 70, y=gy, s=0.48, face=1, mood='flat', front=(40, 60))
        controller(img, p['fh'])
    elif i == 1:
        for j in range(4):
            yy = cy - 130 + j * 50
            line(img, (cx + 30, yy), (cx + 210, yy), (120, 120, 134), 6)
            kx = cx + 30 + 180 * (0.5 + 0.45 * math.sin(t * 2.5 + j * 1.7))
            circle(img, (kx, yy), 13, CYAN)
        p = person(img, cx - 80, y=gy, s=0.48, face=1, mood='flat', front=(40, 60))
        controller(img, p['fh'])
    elif i == 2:
        glow(img, (cx + 120, cy - 70), 120, (255, 160, 90), 0.5)
        circle(img, (cx + 120, cy - 70), 50, (255, 190, 100))
        cv2.rectangle(img, (x0 + 4, cy - 30), (x1 - 4, cy + 10), (24, 22, 34), -1)
        line(img, (x0, cy + 40), (x1, cy + 40), (90, 80, 120), 4)
        person(img, cx - 70, y=gy, s=0.48, face=1, mood='smile', walk=(t * 6, 1.0))
    else:
        cv2.rectangle(img, (cx + 60, cy - 130), (cx + 210, cy - 40), (40, 40, 52), -1)
        circle(img, (cx + 135, cy - 85), 26, RED if (t * 2) % 1 < 0.6 else (90, 30, 30))
        sp = label_sprite('LIVE', WHITE, 20); blit(img, sp, cx + 135 - sp.shape[1] / 2, cy - 30)
        person(img, cx - 60, y=gy, s=0.48, face=1, mood='smile', front=(150, -60), rear=(-40, 40),
               bob=-10 * abs(math.sin(t * 8)))
    m = np.ones(img.shape[:2], bool); m[y0:y1, x0:x1] = False
    img[m] = keep[m]
    col = GOLD if active else (60, 60, 72)
    cv2.rectangle(img, (x0, y0), (x1, y1), col, 6 if active else 3)
    blit(img, fit_sprite(lab, GOLD if active else (150, 150, 160), 26, 460), x0 + 12, y1 - 50)
    if not active:
        sub = img[y0 + 3:y1 - 2, x0 + 3:x1 - 2]
        sub[:] = (sub * 0.45).astype(np.uint8)

class FirstHour:
    name = '2026-11-16_gta6_first_hour_which_gamer'; dur = 22.5
    banner = "GTA 6, THE FIRST HOUR. / *WHICH GAMER ARE YOU?*"
    prog = ['A', 'E', 'F#m', 'D']; bpm = 116
    bubbles = [(0.2, 2.4, "SKIP. SKIP.\nSKIP.", (315, 595), 'say'),
               (2.7, 5.0, "BRIGHTNESS...\nTAKE 14.", (845, 595), 'say'),
               (5.3, 7.6, "MISSIONS?\nLATER.", (315, 1085), 'say'),
               (7.9, 10.2, "GUYS, LOOK\nAT THIS!", (845, 1085), 'say'),
               (12.2, 14.4, "I'LL PRESS\nSTART SOON...", (420, 860), 'say')]
    events = [('pop', 0.0), ('tick', 0.5), ('tick', 1.0), ('whoosh', 2.6), ('whoosh', 5.2), ('whoosh', 7.8),
              ('thud', 10.5), ('chime', 12.0), ('boom', 14.4), ('whoosh', 15.0)]

    @staticmethod
    def make_bg(): return room_bg(tv=False)

    @staticmethod
    def cam(t):
        keys = []
        for i, ((cx, cy), _) in enumerate(PANELS):
            a = i * 2.6
            keys += [(a + 0.15, (1.32, cx, cy)), (a + 2.45, (1.32, cx, cy))]
        keys += [(10.5, (1.0, 540, 960)), (22.5, (1.0, 540, 960))]
        return kf(t, keys)

    @staticmethod
    def shake(t):
        if 14.4 <= t < 14.9: return 1 - prog(t, 14.4, 14.9)
        return 0.0

    @staticmethod
    def world(img, t):
        if t < 10.6:
            act = min(3, int(t / 2.6)) if t < 10.4 else -1
            for i in range(4): panel(img, t, i, i == act)
        else:
            # title screen on a big TV, a clock ticking up
            cv2.rectangle(img, (110, 420), (970, 830), (10, 10, 14), -1)
            g = vgrad(386, (60, 20, 100), (240, 110, 90)).astype(np.uint8)
            img[432:818, 122:958] = g[:, None, :]
            sp = fit_sprite('PRESS START', WHITE, 46, 600)
            blit(img, sp, 540 - sp.shape[1] / 2, 470, 0.6 + 0.4 * math.sin(t * 4))
            mins = int(kf(t, [(10.6, 1), (14.4, 45)]))
            ck = fit_sprite(f'0:{mins:02d}:00', RED if t >= 14.4 else GOLD, 44, 400)
            glow(img, (790, 1120), 160, GOLD, 0.25); blit(img, ck, 790 - ck.shape[1] / 2, 1090)
            p = person(img, 420, y=FL, face=1, mood='smile' if t < 14.4 else 'sad',
                       front=(35, 75) if t < 14.4 else (150, 15), rear=(-6, 10) if t < 14.4 else (-150, -15))
            if t < 14.4: controller(img, p['fh'])

    @staticmethod
    def ui(img, t):
        if 10.4 <= t < 12.0:
            a = win(t, 10.4, 11.8, 0.2)
            dim(img, t, 10.4, 0.5 * a)
            caption(img, "...and there's *always a #5.*", t, 10.5, 11.8, 1250, 70)
        if 12.0 <= t < 15.0:
            caption(img, '5. *THE MENU SITTER*', t, 12.0, 14.8, 1560, 56)
            if t >= 14.4: caption(img, '45 minutes on the title screen.', t, 14.4, 14.8, 1650, 38, GREY, POPM)
        if t >= 15.0:
            dim(img, t, 15.0)
            caption(img, 'Which one are you? / *Comment 1 to 5.*', t, 15.2, 30, 1050, 58)
            caption(img, 'Tag your friend who is number 5.', t, 16.4, 30, 1240, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 17.0, 30, 1330, 42, GREY, POPM)
            caption(img, DISC, t, 17.4, 30, 1440, 30, FAINT, POPM)

# =========================================================
# J4  Pre-orders: fact or rumour?
# =========================================================
QUIZ = [("TAKE-TWO: PRE-ORDERS ARE\nFAR ABOVE EXPECTATIONS", 'CONFIRMED', GREEN, 'TAKE-TWO EARNINGS, 9 NOV 2026'),
        ("90% OF PRE-ORDERS ARE\nTHE ULTIMATE EDITION", 'RUMOUR', RED, 'UNVERIFIED REPORT. NOT FROM TAKE-TWO'),
        ("GTA 6 CAN BE NOMINATED\nFOR GAME OF THE YEAR", 'CONFIRMED', GREEN, 'OUT BEFORE THE 20 NOV AWARDS CUT-OFF'),
        ("GTA ONLINE FOR GTA 6\nARRIVES IN EARLY 2027", 'RUMOUR', RED, 'REPORTS ONLY. NO DATE FROM ROCKSTAR')]
QT = 3.4

class FactRumour4:
    name = '2026-11-16_gta6_preorders_fact_or_rumour'; dur = 21.5
    banner = "GTA 6: FACT OR RUMOUR? / *#2 SOUNDS REAL.*"
    prog = ['Gm', 'Eb', 'Bb', 'F']; bpm = 120
    bubbles = [(5.6, 6.9, "WAIT, THAT'S\nNOT OFFICIAL?!", (820, 1310), 'say')]
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
            num = label_sprite(f'#{i + 1} OF 4', GOLD, 34); blit(img, num, 540 - num.shape[1] / 2, 470)
            cv2.rectangle(img, (70, 540), (1010, 860), (24, 22, 36), -1)
            cv2.rectangle(img, (70, 540), (1010, 860), (90, 80, 130), 4)
            for j, ln in enumerate(st.split('\n')):
                sp = fit_sprite(ln, WHITE, 46, 880); blit(img, sp, 540 - sp.shape[1] / 2, 610 + j * 100)
            if lt < 2.0: progress_bar(img, 190, 900, 700, 1 - lt / 2.0, GOLD, 22)
            stamp(img, verdict, t, i * QT + 2.0, (540, 990), col, 64)
            if lt >= 2.2:
                sp = fit_sprite(nt, (210, 210, 220), 28, 960); blit(img, sp, 540 - sp.shape[1] / 2, 1060)
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
            caption(img, 'Did you pre-order? / *Standard or Ultimate?*', t, 13.9, 30, 820, 58)
            caption(img, 'Comment below. Out 19 Nov 2026.', t, 15.2, 30, 1060, 40, GREY, POPM)
            caption(img, 'PS5 + Xbox Series X|S at launch.', t, 15.6, 30, 1140, 30, FAINT, POPM)
            caption(img, DISC, t, 16.0, 30, 1200, 30, FAINT, POPM)

# =========================================================
# J5  Skit: he asked to play all night. She said no.
# =========================================================
class AllNight:
    name = '2026-11-16_gta6_all_night_she_said_no'; dur = 21.5
    banner = "HE WANTED GTA 6 ALL NIGHT. / *SHE SAID NO.*"
    prog = ['C', 'G', 'Am', 'F']; bpm = 100
    bubbles = [(0.2, 1.8, "NO.", (800, 860), 'say'),
               (1.9, 3.5, "JUST LAUNCH\nNIGHT! PLEASE?", (330, 860), 'say'),
               (3.6, 5.0, "NOT ALL NIGHT.\nNO WAY.", (800, 860), 'say'),
               (5.1, 6.5, "...FINE.", (330, 860), 'say'),
               (6.6, 8.5, "BECAUSE I'M\nPLAYING FIRST.", (800, 860), 'say'),
               (8.6, 10.2, "YOU PRE-ORDERED\nIT TOO?!", (330, 860), 'say'),
               (10.3, 11.9, "TWO HOURS EACH.\nI GO FIRST.", (800, 860), 'say'),
               (12.0, 13.4, "...DEAL.", (330, 860), 'say')]
    events = [('boom', 0.0), ('thud', 0.2), ('whoosh', 1.9), ('thud', 3.6), ('tick', 5.1), ('boom', 6.6),
              ('whoosh', 8.6), ('chime', 10.3), ('pop', 12.0), ('whoosh', 13.8)]

    @staticmethod
    def make_bg():
        img = room_bg(); return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.35, 800, 1000)), (1.8, (1.3, 800, 1000)), (1.9, (1.3, 340, 1000)), (3.5, (1.3, 340, 1000)),
                      (3.6, (1.3, 800, 1000)), (5.0, (1.3, 800, 1000)), (5.1, (1.0, 540, 960)), (6.5, (1.0, 540, 960)),
                      (6.6, (1.35, 800, 1000)), (8.5, (1.35, 800, 1000)), (8.6, (1.0, 540, 960)), (21.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if t < 0.5: return 1 - prog(t, 0, 0.5)
        if 6.6 <= t < 7.1: return 0.8 * (1 - prog(t, 6.6, 7.1))
        return 0.0

    @staticmethod
    def world(img, t):
        sp = fit_sprite('GTA 6: 19 NOV', (200, 200, 220), 44, 600)
        blit(img, sp, 540 - sp.shape[1] / 2, 700)
        reveal = t >= 6.6
        sm_ = 'flat' if t < 6.6 else 'smile'
        s = person(img, 800, y=FL, face=-1, hair=True, mood=sm_,
                   front=(150, -40) if 6.6 <= t < 8.5 else ((60, 40) if 10.3 <= t < 11.9 else (10, 14)),
                   rear=(-20, 30))
        if reveal:
            hx, hy = s['fh']
            if 6.6 <= t < 8.6: glow(img, (hx, hy), 160, GOLD, 0.45)
            controller(img, (hx, hy))
        shock = 8.6 <= t < 10.2
        sad = 5.1 <= t < 6.6
        hm = 'sad' if (shock or sad) else ('smile' if t >= 12.0 else 'flat')
        p = person(img, 330, y=FL, face=1, mood=hm,
                   front=(150, 15) if shock else ((80, 30) if 1.9 <= t < 3.5 else (35, 75)),
                   rear=(-150, -15) if shock else (-6, 10), headdown=16 if sad else 0,
                   bob=-10 * abs(math.sin(t * 10)) if shock else 0)
        if not shock: controller(img, p['fh'])
        if t >= 12.0: pop_heart(img, (565, 880), t, 12.0, 45)

    @staticmethod
    def ui(img, t):
        if t >= 13.8:
            dim(img, t, 13.8)
            caption(img, 'Take turns... / *or one console each?*', t, 14.0, 30, 900, 60)
            caption(img, 'Comment your launch night plan.', t, 15.2, 30, 1130, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 15.8, 30, 1210, 40, GREY, POPM)
            caption(img, DISC, t, 16.4, 30, 1300, 30, FAINT, POPM)


VIDS = {'1': ThreeNumbers, '2': SpoilerGran, '3': FirstHour, '4': FactRumour4, '5': AllNight}

if __name__ == '__main__':
    V = VIDS[sys.argv[1]]
    if len(sys.argv) > 2:
        f = frame_fn_v2(V, V.make_bg())
        ims = [cv2.resize(cv2.cvtColor(f(float(x)), cv2.COLOR_RGB2BGR), (432, 768)) for x in sys.argv[2:]]
        cv2.imwrite(f'{OUT}/still_{sys.argv[1]}.jpg', np.hstack(ims), [cv2.IMWRITE_JPEG_QUALITY, 82])
    else:
        build_v2(V, OUT, seed=int(sys.argv[1]) * 13); print('done', V.name)
