"""GTA 6 fan Shorts, batch 3 (2026-11-15, VIRAL FORMAT v2). 100% original visuals: stick figures, neon shapes, text cards.
Facts (sources in TOPICS.md): out 19 Nov 2026 on PS5 + Xbox Series X|S (Rockstar); physical editions are a download code in
the box, no disc at launch (Rockstar, via VGC); GTA VI: The Album, 34 original tracks, streaming 19 Nov (Rockstar, Sept 2026);
album listening events 18 Nov at independent record stores (NME); GTA VI: The Festival, Miami (Mana Wynwood) 21 Nov, hosted
by Rockstar + PlayStation (Push Square, Shacknews). RUMOUR: review embargo 18 Nov (insider NateTheHate); no PC version announced."""
import math, sys, os, cv2, numpy as np
from engine import *
from viral import frame_fn_v2, build_v2
from gta_example import controller
from videos_gta_d1 import (room_bg, sofa, neon_bg, dim, fit_sprite, card, big_text, stamp, progress_bar,
                           burst, FL, GREEN, PINK, CYAN, DISC)

OUT = '/home/claude/shorts/out_2026-11-15'
os.makedirs(OUT, exist_ok=True)
GREY = (200, 200, 206)
FAINT = (130, 130, 138)

def tv_screen(img, col=(22, 18, 40)):
    img[432:818, 122:958] = col

def dcard(img, t, t0, y, num, text, sub, accent):
    if t < t0: return
    k = eo(prog(t, t0, t0 + 0.35))
    x = lerp(-960, 70, k)
    over = img.copy()
    cv2.rectangle(over, (int(x), y), (int(x) + 940, y + 190), (18, 16, 26), -1)
    cv2.rectangle(over, (int(x), y), (int(x) + 16, y + 190), accent, -1)
    img[:] = (img * 0.03 + over * 0.97).astype(np.uint8)
    blit(img, label_sprite(num, accent, 64), x + 30, y + 26)
    blit(img, label_sprite('NOV', accent, 26), x + 46, y + 120)
    blit(img, fit_sprite(text, WHITE, 42, 700), x + 200, y + 40)
    blit(img, fit_sprite(sub, (185, 185, 194), 28, 700), x + 202, y + 118)

# =========================================================
# V1  Countdown: 4 days left, launch week is 3 dates
# =========================================================
class LaunchWeek:
    name = '2026-11-15_gta6_4_days_launch_week'; dur = 23.5
    banner = "GTA 6 IS 4 DAYS AWAY. / *BUT THE 19TH IS JUST DAY ONE.*"
    prog = ['Em', 'C', 'G', 'D']; bpm = 112
    bubbles = [(1.4, 3.0, "4 DAYS.\nTHEN I PLAY.", (380, 1080), 'say'),
               (3.1, 4.8, "THAT'S JUST\nTHE START.", (720, 1080), 'say'),
               (13.6, 15.2, "A FESTIVAL?!\nFOR A GAME?!", (380, 1080), 'say'),
               (15.3, 16.8, "...I NEED\nA TICKET.", (380, 1080), 'say')]
    events = [('tick', 0.0), ('boom', 0.5), ('thud', 3.1), ('whoosh', 4.9), ('thud', 5.1), ('thud', 7.6),
              ('thud', 10.1), ('boom', 13.6), ('chime', 15.3), ('whoosh', 17.0)]

    @staticmethod
    def make_bg(): return neon_bg()

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.15, 540, 900)), (1.3, (1.0, 540, 960)), (1.4, (1.3, 380, 1150)), (3.0, (1.3, 380, 1150)),
                      (3.1, (1.3, 720, 1150)), (4.8, (1.3, 720, 1150)), (5.0, (1.0, 540, 960)), (13.4, (1.0, 540, 960)),
                      (13.6, (1.3, 380, 1150)), (16.8, (1.3, 380, 1150)), (17.1, (1.0, 540, 960)), (23.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if 0.5 <= t < 1.0: return 1 - prog(t, 0.5, 1.0)
        if 13.6 <= t < 14.1: return 1 - prog(t, 13.6, 14.1)
        return 0.0

    @staticmethod
    def world(img, t):
        if t < 5.0 or 13.3 <= t < 17.1:
            shock = 13.6 <= t < 15.3
            m = 'sad' if shock else ('smile' if t < 3.1 or t >= 15.3 else 'flat')
            p = person(img, 380, y=1620, face=1, mood=m, front=(150, 20) if shock else (35, 75),
                       rear=(-150, -20) if shock else (-6, 10), bob=-14 * abs(math.sin(t * 9)) if shock else 0)
            if not shock: controller(img, p['fh'])
            person(img, 720, y=1620, face=-1, hair=True, mood='smile',
                   front=(60, 40) if 3.1 <= t < 4.8 else (10, 14))

    @staticmethod
    def ui(img, t):
        if t < 1.4:
            d = '5' if t < 0.5 else '4'
            glow(img, (540, 760), 420, PINK, 0.5)
            big_text(img, d, t, 0.5 if d == '4' else 0.0, 700, 380, WHITE, GOLD, pop=d == '4')
            big_text(img, 'DAYS LEFT', t, 0.0, 950, 96, GOLD, GOLD, pop=False)
        elif t < 5.0:
            big_text(img, '*4* DAYS', t, 1.4, 600, 110, WHITE, GOLD, pop=False)
        if 4.9 <= t < 13.4 or t >= 17.0:
            dim(img, t, 4.9 if t < 13.4 else 17.0)
        if 4.9 <= t < 13.4:
            big_text(img, 'LAUNCH *WEEK*', t, 4.9, 520, 64, WHITE, GOLD, pop=False)
            dcard(img, t, 5.1, 600, '18', 'ALBUM LISTENING PARTIES', 'AT RECORD STORES (PER NME)', CYAN)
            dcard(img, t, 7.6, 830, '19', 'GTA 6 + THE ALBUM', 'PS5 + XBOX SERIES X|S. 34 TRACKS', GOLD)
            dcard(img, t, 10.1, 1060, '21', 'GTA VI: THE FESTIVAL', 'MIAMI. ROCKSTAR + PLAYSTATION', PINK)
            caption(img, 'All dates *November 2026.*', t, 10.8, 13.3, 1340, 46)
        if t >= 17.0:
            caption(img, 'Festival in Miami... / *or sofa at home?*', t, 17.2, 30, 900, 60)
            caption(img, 'Tell me in the comments.', t, 18.4, 30, 1130, 42, GREY, POPM)
            caption(img, DISC, t, 19.0, 30, 1210, 30, FAINT, POPM)

# =========================================================
# V2  Skit: he opened the box, there was no disc
# =========================================================
def game_box(img, c, openk, t):
    x, y = c
    sub = img.copy(); big = np.zeros_like(img)
    _gb(big, (540, 960), openk)
    S = 0.55
    m = big.sum(axis=2) > 0
    M = np.float32([[S, 0, x - 540 * S], [0, S, y - 960 * S]])
    bw = cv2.warpAffine(big, M, (W, H)); mw = cv2.warpAffine(m.astype(np.uint8), M, (W, H)) > 0
    img[mw] = bw[mw]

def _gb(img, c, openk):
    x, y = c
    # case (generic, no logo): dark blue with neon stripe
    cv2.rectangle(img, (int(x - 70), int(y - 95)), (int(x + 70), int(y + 95)), (30, 40, 90), -1)
    cv2.rectangle(img, (int(x - 70), int(y - 95)), (int(x + 70), int(y + 95)), (10, 10, 14), 4)
    if openk > 0:
        # open lid swings left showing a small code card
        lx = x - 70 - 140 * openk
        cv2.rectangle(img, (int(lx), int(y - 95)), (int(x - 70), int(y + 95)), (40, 52, 110), -1)
        cv2.rectangle(img, (int(x - 62), int(y - 87)), (int(x + 62), int(y + 87)), (16, 16, 22), -1)
        cv2.rectangle(img, (int(x - 44), int(y - 30)), (int(x + 44), int(y + 30)), (236, 236, 238), -1)
        blit(img, label_sprite('CODE', INK, 18), x - 40, y - 16)
    else:
        line(img, (x - 70, y + 40), (x + 70, y - 20), PINK, 8)

def digital_console(img, t, hl):
    x0, y0 = 600, 892
    cv2.rectangle(img, (x0, y0), (x0 + 300, y0 + 90), (232, 232, 236), -1)
    cv2.rectangle(img, (x0 + 6, y0 + 30), (x0 + 294, y0 + 40), (30, 30, 36), -1)
    circle(img, (x0 + 30, y0 + 66), 6, BLUE)
    if hl > 0:
        glow(img, (x0 + 150, y0 + 45), 260, GOLD, 0.45 * hl)
        cv2.rectangle(img, (x0 - 6, y0 - 6), (x0 + 306, y0 + 96), GOLD, 5)
        a = fit_sprite('DIGITAL EDITION', GOLD, 30, 420); blit(img, a, x0 + 150 - a.shape[1] / 2, y0 - 130)
        b = fit_sprite('NO DISC DRIVE', RED, 30, 420); blit(img, b, x0 + 150 - b.shape[1] / 2, y0 - 80)

class NoDisc:
    name = '2026-11-15_gta6_box_no_disc'; dur = 23.5
    banner = "HE OPENED HIS GTA 6 BOX. / *THERE WAS NO DISC.*"
    prog = ['Dm', 'Bb', 'F', 'C']; bpm = 104
    bubbles = [(0.2, 1.9, "WHERE'S THE\nDISC?!", (330, 860), 'say'),
               (2.0, 3.6, "IT'S JUST\nA CODE!", (330, 860), 'say'),
               (3.7, 5.5, "YEP. NO DISC.\nIT'S A CODE\nIN THE BOX.", (760, 1000), 'say'),
               (5.6, 7.2, "I'M TAKING IT\nBACK. I WANT\nA DISC!", (330, 860), 'say'),
               (7.3, 8.8, "BRO... LOOK AT\nYOUR CONSOLE.", (760, 1000), 'say'),
               (10.4, 12.0, "...IT HAS NO\nDISC DRIVE.", (330, 860), 'say'),
               (12.1, 13.6, "JUST TYPE\nTHE CODE.", (760, 1000), 'say')]
    events = [('boom', 0.0), ('thud', 0.2), ('thud', 2.0), ('whoosh', 3.7), ('thud', 5.6), ('tick', 7.3),
              ('boom', 8.9), ('chime', 10.4), ('pop', 12.1), ('whoosh', 13.8), ('thud', 14.0), ('thud', 15.8),
              ('whoosh', 17.6)]

    @staticmethod
    def make_bg():
        img = room_bg(); sofa(img, 600, 1040); return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.3, 400, 1000)), (3.6, (1.25, 400, 1000)), (3.8, (1.25, 760, 1100)), (5.5, (1.25, 760, 1100)),
                      (5.6, (1.25, 400, 1000)), (7.2, (1.25, 400, 1000)), (7.4, (1.0, 540, 960)), (8.8, (1.0, 540, 960)),
                      (9.1, (1.4, 700, 960)), (10.3, (1.4, 700, 960)), (10.5, (1.2, 420, 1000)), (12.0, (1.2, 420, 1000)),
                      (12.2, (1.0, 540, 960)), (23.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if t < 0.5: return 1 - prog(t, 0, 0.5)
        if 8.9 <= t < 9.3: return 0.6
        return 0.0

    @staticmethod
    def world(img, t):
        tv_screen(img)
        blit(img, fit_sprite('ENTER CODE: _ _ _ _', (180, 180, 196), 34, 700), 220, 600)
        digital_console(img, t, prog(t, 8.9, 9.2) if 8.9 <= t < 10.45 else 0)
        shout = t < 2.0 or 5.6 <= t < 7.2
        gm = 'angry' if shout else ('sad' if t < 10.4 else ('flat' if t < 12.1 else 'smile'))
        p = person(img, 330, y=FL, face=1, mood=gm, front=(150, -30) if shout else (40, 60),
                   rear=(-150, -20) if shout else (-10, 20), bob=-12 * abs(math.sin(t * 11)) if t < 1.6 else 0,
                   headdown=18 if 8.9 <= t < 10.4 else 0)
        game_box(img, (p['fh'][0] + 20, p['fh'][1] - 10), 1.0, t)
        fm = 'flat' if t < 12.1 else 'smile'
        person(img, 800, y=FL, face=-1, sitk=1, mood=fm, hair=True,
               front=(70, 60) if 7.3 <= t < 8.8 else (35, 75))
        if t >= 12.1: pop_heart(img, (560, 880), t, 12.1, 45)

    @staticmethod
    def ui(img, t):
        if t >= 13.8:
            dim(img, t, 13.8)
            card(img, t, 14.0, 470, '1', 'PHYSICAL = CODE IN BOX', 'NO DISC AT LAUNCH (ROCKSTAR)', GOLD)
            card(img, t, 15.8, 700, '2', 'OUT 19 NOV 2026', 'PS5 + XBOX SERIES X|S', CYAN)
            caption(img, 'Disc or digital: / *which do you buy?*', t, 17.7, 30, 1060, 60)
            caption(img, 'Tell me below.', t, 18.9, 30, 1290, 42, GREY, POPM)
            caption(img, DISC, t, 19.5, 30, 1370, 30, FAINT, POPM)

# =========================================================
# V3  Which fan are you this week?
# =========================================================
PANELS = [((275, 680), '1. THE SPOILER DODGER'), ((805, 680), '2. THE REVIEW READER'),
          ((275, 1170), '3. THE DAY COUNTER'), ((805, 1170), '4. THE HYPE MACHINE')]

def panel(img, t, i, active):
    (cx, cy), lab = PANELS[i]
    x0, y0, x1, y1 = cx - 245, cy - 220, cx + 245, cy + 220
    keep = img.copy()
    cv2.rectangle(img, (x0, y0), (x1, y1), (24, 22, 34), -1)
    gy = cy + 160
    if i == 0:
        # phone face-down with a "MUTED" bell crossed out
        circle(img, (cx + 120, cy - 40), 50, (60, 60, 72))
        sp = label_sprite('MUTED', RED, 22); blit(img, sp, cx + 120 - sp.shape[1] / 2, cy - 54)
        line(img, (cx + 80, cy - 80), (cx + 160, cy), RED, 6)
        person(img, cx - 60, y=gy, s=0.48, face=1, mood='sad', front=(170, -150), rear=(-170, 150), eyes_closed=True)
    elif i == 1:
        cv2.rectangle(img, (cx + 50, cy - 120), (cx + 200, cy + 60), (230, 230, 236), -1)
        for j in range(4):
            yy = cy - 92 + j * 40
            for k in range(5):
                col = GOLD if (k < 4 - (j % 2)) else (180, 180, 190)
                circle(img, (cx + 72 + k * 26, yy), 9, col)
        p = person(img, cx - 70, y=gy, s=0.48, face=1, mood='flat', front=(60, 40))
    elif i == 2:
        cv2.rectangle(img, (cx + 30, cy - 150), (cx + 210, cy + 10), (232, 230, 224), -1)
        cv2.rectangle(img, (cx + 30, cy - 150), (cx + 210, cy - 110), (200, 56, 70), -1)
        d = '4'
        sp = label_sprite(d, INK, 80); blit(img, sp, cx + 120 - sp.shape[1] / 2, cy - 108)
        for k in range(5):
            line(img, (cx + 44 + k * 10, cy - 20), (cx + 44 + k * 10, cy), INK, 3)
        person(img, cx - 80, y=gy, s=0.48, face=1, mood='flat', front=(80, 10))
    else:
        bob = -26 * abs(math.sin(t * 9))
        burst(img, (cx + 120, cy - 70), 70, GOLD, 0.8 + 0.2 * math.sin(t * 12))
        sp = label_sprite('HYPE', INK, 22); blit(img, sp, cx + 120 - sp.shape[1] / 2, cy - 84)
        person(img, cx - 60, y=gy, s=0.48, face=1, mood='smile', front=(170, 10), rear=(-170, -10), bob=bob)
    m = np.ones(img.shape[:2], bool); m[y0:y1, x0:x1] = False
    img[m] = keep[m]
    col = GOLD if active else (60, 60, 72)
    cv2.rectangle(img, (x0, y0), (x1, y1), col, 6 if active else 3)
    blit(img, fit_sprite(lab, GOLD if active else (150, 150, 160), 26, 460), x0 + 12, y1 - 50)
    if not active:
        sub = img[y0 + 3:y1 - 2, x0 + 3:x1 - 2]
        sub[:] = (sub * 0.45).astype(np.uint8)

def backlog(img, x, y, n):
    cols = [(255, 120, 90), (90, 200, 255), (255, 210, 80), (140, 230, 120), (240, 110, 200), (180, 140, 255)]
    for j in range(n):
        cv2.rectangle(img, (x - 70 + (j % 2) * 8, y - (j + 1) * 34), (x + 70 + (j % 2) * 8, y - j * 34 - 4), cols[j % 6], -1)

class WhichFan:
    name = '2026-11-15_gta6_which_fan_are_you'; dur = 22.5
    banner = "GTA 6 WEEK. / *WHICH FAN ARE YOU?*"
    prog = ['A', 'E', 'F#m', 'D']; bpm = 116
    bubbles = [(0.2, 2.4, "LA LA LA!\nNO SPOILERS!", (315, 595), 'say'),
               (2.7, 5.0, "I'LL WAIT\nFOR REVIEWS.", (845, 595), 'say'),
               (5.3, 7.6, "4 DAYS.\n96 HOURS.", (315, 1085), 'say'),
               (7.9, 10.2, "LET'S\nGOOOO!", (845, 1085), 'say'),
               (12.2, 14.4, "I'LL START IT\nAFTER THESE...", (420, 860), 'say')]
    events = [('pop', 0.0), ('tick', 0.5), ('whoosh', 2.6), ('whoosh', 5.2), ('tick', 5.6), ('tick', 6.2),
              ('whoosh', 7.8), ('thud', 10.5), ('chime', 12.0), ('boom', 14.4), ('whoosh', 15.0)]

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
            n = int(kf(t, [(12.0, 2), (14.4, 12)]))
            backlog(img, 760, FL, n)
            if t >= 14.4:
                sp = fit_sprite('142 UNPLAYED GAMES', RED, 40, 700)
                blit(img, sp, 540 - sp.shape[1] / 2, 470 + 0 * t)
            p = person(img, 420, y=FL, face=1, mood='smile' if t < 14.4 else 'sad',
                       front=(60, 40) if t < 14.4 else (150, 15), rear=(-6, 10) if t < 14.4 else (-150, -15))

    @staticmethod
    def ui(img, t):
        if 10.4 <= t < 12.0:
            a = win(t, 10.4, 11.8, 0.2)
            dim(img, t, 10.4, 0.5 * a)
            caption(img, "...and there's *always a #5.*", t, 10.5, 11.8, 1000, 70)
        if 12.0 <= t < 15.0:
            caption(img, '5. *THE BACKLOG GUY*', t, 12.0, 14.8, 1560, 56)
        if t >= 15.0:
            dim(img, t, 15.0)
            caption(img, 'Which one are you? / *Comment 1 to 5.*', t, 15.2, 30, 1050, 58)
            caption(img, 'Tag your friend who is number 5.', t, 16.4, 30, 1240, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 17.0, 30, 1330, 42, GREY, POPM)
            caption(img, DISC, t, 17.4, 30, 1440, 30, FAINT, POPM)

# =========================================================
# V4  Launch week: fact or rumour?
# =========================================================
QUIZ = [("THE GTA 6 ALBUM HAS\n34 ORIGINAL TRACKS", 'CONFIRMED', GREEN, 'STREAMING 19 NOV (ROCKSTAR)'),
        ("REVIEWS GO LIVE\nON 18 NOVEMBER", 'RUMOUR', RED, 'INSIDER REPORT. NOT FROM ROCKSTAR'),
        ("A GTA 6 FESTIVAL\nIN MIAMI ON 21 NOV", 'CONFIRMED', GREEN, 'HOSTED BY ROCKSTAR + PLAYSTATION'),
        ("GTA 6 IS ON PC\nON LAUNCH DAY", 'RUMOUR', RED, 'NO PC VERSION ANNOUNCED YET')]
QT = 3.4

class FactRumour3:
    name = '2026-11-15_gta6_launch_week_fact_or_rumour'; dur = 21.5
    banner = "GTA 6 WEEK: FACT OR RUMOUR? / *#2 FOOLS EVERYONE.*"
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
            caption(img, 'Will you read reviews... / *or play blind?*', t, 13.9, 30, 820, 58)
            caption(img, 'Comment below. Out 19 Nov 2026.', t, 15.2, 30, 1060, 40, GREY, POPM)
            caption(img, 'PS5 + Xbox Series X|S at launch.', t, 15.6, 30, 1140, 30, FAINT, POPM)
            caption(img, DISC, t, 16.0, 30, 1200, 30, FAINT, POPM)

# =========================================================
# V5  Skit: he asked for GTA 6 day off. The boss said no.
# =========================================================
def office_bg():
    img = room_bg(tv=False)
    # window with city night
    cv2.rectangle(img, (120, 440), (960, 860), (16, 20, 44), -1)
    for k, (bx, bh) in enumerate([(160, 220), (260, 300), (380, 180), (480, 260), (600, 320), (720, 200), (830, 280)]):
        cv2.rectangle(img, (bx, 860 - bh), (bx + 90, 860), (30, 34, 60), -1)
        for wy in range(860 - bh + 20, 850, 40):
            for wx in (bx + 16, bx + 52):
                if (wx + wy + k) % 3: cv2.rectangle(img, (wx, wy), (wx + 18, wy + 18), (255, 210, 120), -1)
    cv2.rectangle(img, (120, 440), (960, 860), (10, 10, 14), 12)
    line(img, (540, 440), (540, 860), (10, 10, 14), 10)
    # desk
    cv2.rectangle(img, (520, 1180), (1060, 1220), (80, 60, 50), -1)
    cv2.rectangle(img, (540, 1220), (570, FL), (60, 46, 40), -1); cv2.rectangle(img, (1010, 1220), (1040, FL), (60, 46, 40), -1)
    return img

class BossDayOff:
    name = '2026-11-15_gta6_boss_day_off'; dur = 21.5
    banner = "HE ASKED FOR 19 NOV OFF. / *THE BOSS SAID NO.*"
    prog = ['C', 'G', 'Am', 'F']; bpm = 100
    bubbles = [(0.2, 1.8, "NO.", (820, 880), 'say'),
               (1.9, 3.5, "BUT IT'S\nGTA 6 DAY!", (330, 860), 'say'),
               (3.6, 5.1, "I KNOW.\nTHAT'S WHY.", (820, 880), 'say'),
               (5.2, 6.6, "...WHAT?", (330, 860), 'say'),
               (6.7, 8.6, "I BOOKED\nTHAT DAY OFF\nMONTHS AGO.", (820, 880), 'say'),
               (8.7, 10.4, "SO WHO'S\nRUNNING THE\nOFFICE?!", (330, 860), 'say'),
               (10.5, 12.1, "YOU. TAKE\nTHE 20TH OFF.", (820, 880), 'say'),
               (12.2, 13.6, "...DEAL.", (330, 860), 'say')]
    events = [('boom', 0.0), ('thud', 0.2), ('whoosh', 1.9), ('tick', 3.6), ('thud', 5.2), ('boom', 6.7),
              ('whoosh', 8.7), ('chime', 10.5), ('pop', 12.2), ('whoosh', 13.8)]

    @staticmethod
    def make_bg(): return office_bg()

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.35, 800, 1000)), (1.8, (1.3, 800, 1000)), (1.9, (1.3, 340, 1000)), (3.5, (1.3, 340, 1000)),
                      (3.6, (1.3, 800, 1000)), (5.1, (1.3, 800, 1000)), (5.2, (1.0, 540, 960)), (6.6, (1.0, 540, 960)),
                      (6.7, (1.35, 800, 1000)), (8.6, (1.35, 800, 1000)), (8.7, (1.0, 540, 960)), (23.0, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if t < 0.5: return 1 - prog(t, 0, 0.5)
        if 6.7 <= t < 7.2: return 0.8 * (1 - prog(t, 6.7, 7.2))
        return 0.0

    @staticmethod
    def world(img, t):
        # leave form on the desk
        fx, fy = 505, 1100
        cv2.rectangle(img, (fx, fy), (fx + 290, fy + 80), (236, 236, 238), -1)
        blit(img, label_sprite('LEAVE: 19 NOV', INK, 17), fx + 6, fy + 6)
        if t >= 10.5:
            blit(img, label_sprite('20 NOV: OK', (40, 150, 90), 18), fx + 6, fy + 40)
        else:
            blit(img, label_sprite('DENIED', RED, 22), fx + 40, fy + 38)
        bm = 'flat' if t < 3.6 else ('smile' if t < 8.7 else ('flat' if t < 10.5 else 'smile'))
        person(img, 820, y=FL, face=-1, mood=bm, front=(100, -60) if t < 1.8 else ((60, 40) if 10.5 <= t < 12.1 else (10, 14)))
        if 6.7 <= t < 8.6:
            # boss's own calendar with the 19th circled
            cv2.rectangle(img, (540, 930), (760, 1080), (232, 230, 224), -1)
            cv2.rectangle(img, (540, 930), (760, 966), (200, 56, 70), -1)
            blit(img, label_sprite('NOV', WHITE, 22), 610, 932)
            sp = label_sprite('19', INK, 54); blit(img, sp, 650 - sp.shape[1] / 2, 980)
            ellipse(img, (650, 1020), (62, 44), 0, 0, 360 * clamp(prog(t, 6.8, 7.4)), RED, 6)
        shock = 5.2 <= t < 6.6 or 8.7 <= t < 10.4
        wm = 'sad' if shock else ('smile' if t >= 12.2 else ('flat' if t >= 1.9 else 'sad'))
        p = person(img, 330, y=FL, face=1, mood=wm, front=(150, 15) if shock else ((80, 30) if 1.9 <= t < 3.5 else (35, 75)),
                   rear=(-150, -15) if shock else (-6, 10), bob=-10 * abs(math.sin(t * 10)) if 8.7 <= t < 9.6 else 0)
        if t >= 12.2: pop_heart(img, (580, 900), t, 12.2, 45)

    @staticmethod
    def ui(img, t):
        if t >= 13.8:
            dim(img, t, 13.8)
            caption(img, 'Day off for GTA 6... / *or play after work?*', t, 14.0, 30, 900, 60)
            caption(img, 'Comment your plan.', t, 15.2, 30, 1130, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 15.8, 30, 1210, 40, GREY, POPM)
            caption(img, DISC, t, 16.4, 30, 1300, 30, FAINT, POPM)


VIDS = {'1': LaunchWeek, '2': NoDisc, '3': WhichFan, '4': FactRumour3, '5': BossDayOff}

if __name__ == '__main__':
    V = VIDS[sys.argv[1]]
    if len(sys.argv) > 2:
        f = frame_fn_v2(V, V.make_bg())
        ims = [cv2.resize(cv2.cvtColor(f(float(x)), cv2.COLOR_RGB2BGR), (432, 768)) for x in sys.argv[2:]]
        cv2.imwrite(f'{OUT}/still_{sys.argv[1]}.jpg', np.hstack(ims), [cv2.IMWRITE_JPEG_QUALITY, 82])
    else:
        build_v2(V, OUT, seed=int(sys.argv[1]) * 13); print('done', V.name)
