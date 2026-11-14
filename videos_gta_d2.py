"""GTA 6 fan Shorts, batch 2 (2026-11-14, VIRAL FORMAT v2). 100% original visuals: stick figures, neon shapes, text cards.
Facts (sources in TOPICS.md): out 19 Nov 2026 on PS5 + Xbox Series X|S; Rockstar (10 Nov): 30fps target on consoles, PS5 Pro
gets PSSR + ray-traced shadows; Sony + Microsoft: most pre-ordered game on their stores; PS Store listings: NZ unlocks first
(midnight 19 Nov NZ = 11:00 UK 18 Nov), UK midnight 19 Nov (not confirmed by Rockstar); ~1 GB update spotted by trackers
13 Nov (REPORTED); Vintage Vice City Pack free if bought before 20 Nov; US $79.99 standard / $99.99 Ultimate.
RUMOURS: one global unlock time; disc edition in December."""
import math, sys, os, cv2, numpy as np
from engine import *
from viral import frame_fn_v2, build_v2
from gta_example import controller
from videos_gta_d1 import (room_bg, sofa, neon_bg, dim, fit_sprite, card, big_text, stamp, progress_bar,
                           burst, FL, GREEN, PINK, CYAN, DISC)

OUT = '/home/claude/shorts/out_2026-11-14b'
os.makedirs(OUT, exist_ok=True)
GREY = (200, 200, 206)
FAINT = (130, 130, 138)

def tv_screen(img, col=(22, 18, 40)):
    img[432:818, 122:958] = col

def header(img, text, col, y=470, size=40):
    cv2.rectangle(img, (150, y), (930, y + 74), col, -1)
    s = fit_sprite(text, WHITE, size, 740); blit(img, s, 540 - s.shape[1] / 2, y + 10)

# =========================================================
# V1  Countdown: 5 days left, 3 new confirmed facts
# =========================================================
class FiveDaysFacts:
    name = '2026-11-14b_gta6_5_days_new_facts'; dur = 22.5
    banner = "GTA 6: 5 DAYS LEFT. / *3 NEW CONFIRMED FACTS.*"
    prog = ['Em', 'C', 'G', 'D']; bpm = 112
    bubbles = [(2.6, 4.3, "TELL ME\nEVERYTHING.", (540, 1060), 'say'),
               (12.6, 14.2, "30 FPS?!", (540, 1060), 'say'),
               (14.3, 16.0, "...I'M STILL\nPLAYING 300 HOURS.", (540, 1060), 'say')]
    events = [('tick', 0.0), ('boom', 0.6), ('whoosh', 4.4), ('thud', 4.6), ('thud', 7.0), ('thud', 9.6),
              ('boom', 12.6), ('chime', 14.4), ('whoosh', 16.2)]

    @staticmethod
    def make_bg(): return neon_bg()

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.2, 540, 900)), (2.4, (1.0, 540, 960)), (2.6, (1.25, 540, 1150)), (4.3, (1.25, 540, 1150)),
                      (4.5, (1.0, 540, 960)), (12.4, (1.0, 540, 960)), (12.6, (1.3, 540, 1150)), (16.0, (1.3, 540, 1150)),
                      (16.3, (1.0, 540, 960)), (22.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if 0.6 <= t < 1.1: return 1 - prog(t, 0.6, 1.1)
        if 12.6 <= t < 13.1: return 1 - prog(t, 12.6, 13.1)
        return 0.0

    @staticmethod
    def world(img, t):
        if t < 4.5 or 12.3 <= t < 16.3:
            panic = 12.6 <= t < 14.3
            happy = 14.3 <= t
            p = person(img, 540, y=1620, face=1, mood='sad' if panic else ('smile' if happy else 'flat'),
                       front=(150, 20) if panic else (35, 75), rear=(-150, -20) if panic else (-6, 10),
                       bob=-14 * abs(math.sin(t * 9)) if panic else 0)
            if not panic: controller(img, p['fh'])

    @staticmethod
    def ui(img, t):
        if t < 2.5:
            d = '6' if t < 0.6 else '5'
            glow(img, (540, 820), 420, PINK, 0.5)
            big_text(img, d, t, 0.6 if d == '5' else 0.0, 760, 380, WHITE, GOLD, pop=d == '5')
            big_text(img, 'DAYS LEFT', t, 0.0, 1010, 96, GOLD, GOLD, pop=False)
        if 4.4 <= t < 12.4 or t >= 16.2:
            dim(img, t, 4.4 if t < 12.4 else 16.2)
        if 4.4 <= t < 12.4:
            card(img, t, 4.6, 520, '1', '30 FPS TARGET', 'ON PS5 + XBOX SERIES X|S (ROCKSTAR)')
            card(img, t, 7.0, 750, '2', 'PS5 PRO GETS EXTRAS', 'PSSR + RAY-TRACED SHADOWS', CYAN)
            card(img, t, 9.6, 980, '3', 'RECORD PRE-ORDERS', 'SONY + XBOX: MOST EVER ON THEIR STORES', PINK)
            caption(img, 'Out *19 November 2026.*', t, 10.3, 12.3, 1290, 50)
        if t >= 16.2:
            caption(img, 'Is 30 FPS a dealbreaker... / *or do you not care?*', t, 16.4, 30, 900, 58)
            caption(img, 'Tell me in the comments.', t, 17.6, 30, 1130, 42, GREY, POPM)
            caption(img, DISC, t, 18.2, 30, 1210, 30, FAINT, POPM)

# =========================================================
# V2  Skit: his Kiwi mate gets GTA 6 13 hours earlier
# =========================================================
class KiwiMate:
    name = '2026-11-14b_gta6_kiwi_mate_13_hours'; dur = 24.5
    banner = "HIS MATE GETS GTA 6 / *13 HOURS EARLIER.*"
    prog = ['G', 'D', 'Em', 'C']; bpm = 100
    bubbles = [(0.2, 2.0, "IT'S MIDNIGHT HERE.\nIT'S UNLOCKING.", (470, 760), 'say'),
               (2.1, 3.7, "IT'S 11 AM HERE!\n13 MORE HOURS?!", (400, 990), 'say'),
               (3.9, 5.4, "DON'T YOU DARE\nSPOIL ANYTHING.", (400, 990), 'say'),
               (5.6, 7.3, "SPOIL IT?\nI'M NOT EVEN\nSTARTING.", (470, 760), 'say'),
               (7.4, 8.8, "...WHAT?", (400, 990), 'say'),
               (9.0, 11.0, "WE SAID WE'D\nPLAY TOGETHER.\nI'LL WAIT.", (470, 760), 'say'),
               (11.2, 12.8, "13 HOURS?\nFOR ME?", (400, 990), 'say'),
               (12.9, 14.6, "GO TO SLEEP.\nSEE YOU AT\nMIDNIGHT.", (470, 760), 'say')]
    events = [('boom', 0.0), ('thud', 2.1), ('whoosh', 5.6), ('thud', 7.4), ('chime', 9.2), ('pop', 14.6),
              ('whoosh', 15.0), ('thud', 15.2), ('thud', 17.0), ('whoosh', 19.0)]

    @staticmethod
    def make_bg():
        img = room_bg(); sofa(img, 160, 640); return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.3, 540, 640)), (2.0, (1.3, 540, 640)), (2.2, (1.25, 420, 1000)), (5.4, (1.25, 420, 1000)),
                      (5.6, (1.0, 540, 960)), (7.4, (1.0, 540, 960)), (7.5, (1.35, 400, 1050)), (8.8, (1.35, 400, 1050)),
                      (9.0, (1.2, 540, 680)), (11.0, (1.2, 540, 680)), (11.2, (1.0, 540, 960)), (24.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if 2.1 <= t < 2.6: return 1 - prog(t, 2.1, 2.6)
        if 7.4 <= t < 7.8: return 0.7
        return 0.0

    @staticmethod
    def world(img, t):
        # video call on the TV: friend in NZ, at night
        tv_screen(img, (14, 16, 40))
        circle(img, (860, 520), 40, (230, 230, 210)); circle(img, (845, 510), 38, (14, 16, 40))
        for sx, sy in [(700, 480), (760, 560), (620, 520), (900, 640)]: circle(img, (sx, sy), 4, WHITE)
        blit(img, label_sprite('NZ  00:00  19 NOV', CYAN, 22), 140, 446)
        cv2.rectangle(img, (180, 740), (520, 818), (60, 50, 78), -1)
        fm = 'smile' if t < 7.4 or t >= 9.0 else 'flat'
        fp = person(img, 330, y=818, s=0.5, face=1, sitk=1, mood=fm, front=(35, 75))
        controller(img, (fp['fh'][0], fp['fh'][1]))
        if t >= 12.9:
            pop_heart(img, (330, 600), t, 12.9, 40)
        cv2.rectangle(img, (110, 420), (970, 830), (10, 10, 14), 12)
        # UK gamer on the sofa
        shock = 2.1 <= t < 3.7 or 7.4 <= t < 8.8
        um = 'sad' if shock else ('angry' if 3.9 <= t < 5.4 else ('smile' if t >= 11.2 else 'flat'))
        p = person(img, 400, y=FL, face=1, sitk=1, mood=um,
                   front=(150, 15) if shock else (35, 75), rear=(-150, -15) if shock else (-6, 10),
                   bob=-10 * abs(math.sin(t * 10)) if 2.1 <= t < 3.0 else 0)
        if not shock: controller(img, p['fh'])
        if t >= 14.6: pop_heart(img, (560, 980), t, 14.6, 55)

    @staticmethod
    def ui(img, t):
        if t < 15.0:
            label(img, 'UK  11:00 AM  18 NOV', t, 2.1, 15.0, y=1720, color=GOLD, size=34)
        if t >= 15.0:
            dim(img, t, 15.0)
            card(img, t, 15.2, 470, '1', 'NEW ZEALAND IS FIRST', 'MIDNIGHT 19 NOV, NZ TIME', CYAN)
            card(img, t, 17.0, 700, '2', 'UK: MIDNIGHT 19 NOV', 'ABOUT 13 HOURS AFTER NZ', GOLD)
            caption(img, "Per PlayStation Store listings. Rockstar hasn't confirmed times.", t, 17.6, 30, 940, 28, FAINT, POPM)
            caption(img, 'Would you wait 13 hours / *for your friend?*', t, 19.2, 30, 1120, 58)
            caption(img, 'Tag the friend you play with.', t, 20.4, 30, 1350, 42, GREY, POPM)
            caption(img, DISC, t, 21.0, 30, 1430, 30, FAINT, POPM)

# =========================================================
# V3  Skit: midnight, then "UPDATE REQUIRED"
# =========================================================
class UpdateRequired:
    name = '2026-11-14b_gta6_midnight_update'; dur = 22.5
    banner = "MIDNIGHT. GTA 6 UNLOCKS. / *THEN THIS POPS UP.*"
    prog = ['Dm', 'Bb', 'F', 'C']; bpm = 108
    bubbles = [(0.3, 2.0, "NO NO NO!\nNOT NOW!", (330, 850), 'say'),
               (2.1, 3.7, "HOW BIG?!\nHOW LONG?!", (330, 850), 'say'),
               (3.9, 5.4, "RELAX.", (800, 980), 'say'),
               (5.6, 7.4, "I LEFT IT IN\nREST MODE WITH\nAUTO-UPDATES ON.", (800, 980), 'say'),
               (7.6, 9.0, "...YOU DID\nTHAT FOR ME?", (330, 850), 'say'),
               (9.1, 10.6, "YOU OWE ME\nSECOND GO.", (800, 980), 'say')]
    events = [('boom', 0.0), ('thud', 0.3), ('tick', 2.4), ('tick', 2.9), ('tick', 3.4), ('whoosh', 3.9),
              ('chime', 6.4), ('thud', 7.6), ('pop', 10.6), ('whoosh', 10.8), ('thud', 11.0), ('thud', 13.0),
              ('whoosh', 15.2)]

    @staticmethod
    def make_bg():
        img = room_bg(); sofa(img, 600, 1040); return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.3, 540, 700)), (2.0, (1.25, 460, 860)), (3.7, (1.25, 460, 860)), (3.9, (1.0, 540, 960)),
                      (4.0, (1.25, 760, 1080)), (5.4, (1.25, 760, 1080)), (5.6, (1.0, 540, 960)), (7.6, (1.0, 540, 960)),
                      (7.7, (1.15, 400, 960)), (9.0, (1.15, 400, 960)), (9.2, (1.0, 540, 960)), (22.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if t < 0.6: return 1 - prog(t, 0, 0.6)
        if 6.4 <= t < 6.8: return 0.5
        return 0.0

    @staticmethod
    def world(img, t):
        tv_screen(img)
        done = t >= 6.4
        flash = (not done) and int(t * 5) % 2 == 0 and t < 2.0
        header(img, 'READY TO PLAY' if done else 'UPDATE REQUIRED', (40, 150, 90) if done else ((140, 30, 44) if flash else (200, 50, 64)))
        frac = 1.0 if done else (0.0 if t < 5.6 else kf(t, [(5.6, 0.0), (6.4, 1.0)]))
        progress_bar(img, 200, 640, 680, frac)
        pct = label_sprite(f'{int(frac * 100)}%', WHITE, 40); blit(img, pct, 540 - pct.shape[1] / 2, 570)
        blit(img, fit_sprite('00:00  19 NOV', (180, 180, 196), 28, 600), 380, 720)
        gm = 'sad' if t < 7.6 else 'smile'
        panic = t < 3.8
        p = person(img, 330, y=FL, face=1, mood=gm, front=(150, 15) if panic else (35, 75),
                   rear=(-150, -15) if panic else (-6, 10), bob=-12 * abs(math.sin(t * 11)) if t < 2.0 else 0)
        if not panic: controller(img, p['fh'])
        rm = 'flat' if t < 9.1 else 'smile'
        person(img, 800, y=FL, face=-1, sitk=1, mood=rm, hair=True, eyes_closed=t < 3.8, front=(20, 40),
               headdown=10 if t < 3.8 else 0)
        if t >= 7.6: pop_heart(img, (560, 900), t, 7.6, 50)

    @staticmethod
    def ui(img, t):
        if t >= 10.8:
            dim(img, t, 10.8)
            card(img, t, 11.0, 480, '1', 'REPORTED: ~1 GB PATCH', 'TRACKERS SPOTTED IT ON 13 NOV', BLUE)
            card(img, t, 13.0, 720, '2', 'TURN ON AUTO-UPDATES', 'LEAVE THE CONSOLE IN REST MODE', GREEN)
            caption(img, 'Stay up for midnight... / *or play after a sleep?*', t, 15.3, 30, 1060, 56)
            caption(img, 'Tell me below.', t, 16.5, 30, 1290, 42, GREY, POPM)
            caption(img, DISC, t, 17.1, 30, 1370, 30, FAINT, POPM)

# =========================================================
# V4  Which gamer are you on launch night? (new types)
# =========================================================
PANELS = [((275, 680), '1. THE ALARM SETTER'), ((805, 680), '2. THE SNACK HOARDER'),
          ((275, 1170), '3. "ONE MORE MISSION"'), ((805, 1170), '4. THE RADIO SURFER')]

def note(img, c, col):
    circle(img, c, 12, col); line(img, (c[0] + 10, c[1]), (c[0] + 10, c[1] - 46), col, 5)
    line(img, (c[0] + 10, c[1] - 46), (c[0] + 30, c[1] - 34), col, 5)

def panel(img, t, i, active):
    (cx, cy), lab = PANELS[i]
    x0, y0, x1, y1 = cx - 245, cy - 220, cx + 245, cy + 220
    keep = img.copy()
    cv2.rectangle(img, (x0, y0), (x1, y1), (24, 22, 34), -1)
    gy = cy + 160
    if i == 0:
        circle(img, (cx + 120, cy + 10), 58, (230, 230, 236)); circle(img, (cx + 120, cy + 10), 50, (40, 40, 50))
        sp = label_sprite('11:59', RED, 24); blit(img, sp, cx + 120 - sp.shape[1] / 2, cy - 12)
        for k in (1, 2):
            r = 64 + k * 12 + 4 * math.sin(t * 30)
            ellipse(img, (cx + 120, cy + 10), (r, r), 0, 200, 250, GOLD, 3); ellipse(img, (cx + 120, cy + 10), (r, r), 0, 290, 340, GOLD, 3)
        person(img, cx - 60, y=gy, s=0.48, face=1, mood='smile', front=(150, -40))
    elif i == 1:
        cols = [(255, 120, 90), (90, 200, 255), (255, 210, 80), (140, 230, 120), (240, 110, 200)]
        for j in range(9):
            r, c = divmod(j, 3)
            bx = cx + 40 + c * 52 - r * 4; by = gy - 40 - r * 50
            cv2.rectangle(img, (int(bx), int(by)), (int(bx + 46), int(by + 44)), cols[j % 5], -1)
        person(img, cx - 90, y=gy, s=0.48, face=1, sitk=1, mood='smile', front=(100, -20))
    elif i == 2:
        cv2.rectangle(img, (cx + 40, cy - 160), (cx + 220, cy + 10), (60, 80, 120), -1)
        circle(img, (cx + 130, cy + 10), 60, (255, 170, 90))
        cv2.rectangle(img, (cx + 40, cy + 10), (cx + 220, cy + 80), (24, 22, 34), -1)
        cv2.rectangle(img, (cx + 40, cy - 160), (cx + 220, cy + 10), (20, 20, 26), 6)
        sp = label_sprite('6:00 AM', GOLD, 22); blit(img, sp, cx + 60, cy + 20)
        p = person(img, cx - 80, y=gy, s=0.48, face=1, sitk=1, mood='flat', front=(35, 75), headdown=8)
        controller(img, p['fh'])
    else:
        bob = -10 * abs(math.sin(t * 8))
        for j in range(3):
            ph = (t * 0.8 + j / 3) % 1
            note(img, (cx + 60 + j * 50, cy - 40 - ph * 120), [PINK, CYAN, GOLD][j])
        p = person(img, cx - 60, y=gy, s=0.48, face=1, sitk=1, mood='smile', front=(35, 75), bob=bob)
        controller(img, p['fh'])
    m = np.ones(img.shape[:2], bool); m[y0:y1, x0:x1] = False
    img[m] = keep[m]
    col = GOLD if active else (60, 60, 72)
    cv2.rectangle(img, (x0, y0), (x1, y1), col, 6 if active else 3)
    blit(img, fit_sprite(lab, GOLD if active else (150, 150, 160), 26, 460), x0 + 12, y1 - 50)
    if not active:
        sub = img[y0 + 3:y1 - 2, x0 + 3:x1 - 2]
        sub[:] = (sub * 0.45).astype(np.uint8)

class WhichGamer2:
    name = '2026-11-14b_gta6_launch_night_which_one'; dur = 22.5
    banner = "GTA 6 LAUNCH NIGHT. / *WHICH ONE ARE YOU?*"
    prog = ['A', 'E', 'F#m', 'D']; bpm = 116
    bubbles = [(0.2, 2.4, "ALARM AT 11:59.\nAND 11:58.", (315, 595), 'say'),
               (2.7, 5.0, "40 SNACKS.\nMINIMUM.", (845, 595), 'say'),
               (5.3, 7.6, "JUST ONE MORE\nMISSION...", (315, 1085), 'say'),
               (7.9, 10.2, "NEXT STATION.\nNEXT STATION.", (845, 1085), 'say'),
               (12.2, 14.4, "ZZZ...", (600, 1080), 'think')]
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
            cv2.rectangle(img, (110, 440), (970, 830), (10, 10, 14), -1)
            img[452:818, 122:958] = (22, 18, 40)
            on = t >= 12.0
            header(img, 'UNLOCKED' if on else '23:59', (40, 150, 90) if on else (60, 60, 80), y=560, size=48)
            sofa(img, 280, 800)
            awake = t >= 14.4
            p = person(img, 540, y=FL, face=1, sitk=1, mood='sad' if awake else 'flat', eyes_closed=not awake,
                       front=(150, 15) if awake else (40, 95), rear=(-150, -15) if awake else (-6, 10),
                       headdown=0 if awake else 28)
            if not awake: controller(img, p['fh'])

    @staticmethod
    def ui(img, t):
        if 10.4 <= t < 12.0:
            a = win(t, 10.4, 11.8, 0.2)
            dim(img, t, 10.4, 0.5 * a)
            caption(img, "...and there's *always a #5.*", t, 10.5, 11.8, 1000, 70)
        if 12.0 <= t < 15.0:
            caption(img, '5. *ASLEEP AT 11:58*', t, 12.0, 14.8, 1500, 56)
        if t >= 15.0:
            dim(img, t, 15.0)
            caption(img, 'Which one are you? / *Comment 1 to 5.*', t, 15.2, 30, 1050, 58)
            caption(img, 'Tag your friend who is number 5.', t, 16.4, 30, 1240, 42, GREY, POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 17.0, 30, 1330, 42, GREY, POPM)
            caption(img, DISC, t, 17.4, 30, 1440, 30, FAINT, POPM)

# =========================================================
# V5  Confirmed or rumour?
# =========================================================
QUIZ = [("FREE VINTAGE VICE CITY\nPACK IF YOU BUY EARLY", 'CONFIRMED', GREEN, 'BUY BEFORE 20 NOV (ROCKSTAR)'),
        ("ONE GLOBAL UNLOCK TIME\nFOR EVERYONE", 'RUMOUR', RED, 'STORE LISTINGS SHOW MIDNIGHT LOCAL TIME'),
        ("STANDARD EDITION:\n$79.99 IN THE US", 'CONFIRMED', GREEN, 'ULTIMATE EDITION: $99.99'),
        ("A DISC EDITION IS\nCOMING IN DECEMBER", 'RUMOUR', RED, 'NOT CONFIRMED BY ROCKSTAR')]
QT = 3.4

class ConfirmedRumour:
    name = '2026-11-14b_gta6_confirmed_or_rumour'; dur = 21.5
    banner = "GTA 6: FACT OR RUMOUR? / *DON'T FALL FOR #2.*"
    prog = ['Gm', 'Eb', 'Bb', 'F']; bpm = 120
    bubbles = [(5.6, 6.9, "WAIT, THAT'S\nNOT REAL?!", (820, 1310), 'say')]
    events = sum([[('tick', i * QT + 0.4), ('tick', i * QT + 1.0), ('tick', i * QT + 1.6),
                   ('boom' if i == 1 else 'thud', i * QT + 2.0), ('whoosh', i * QT + 3.3)] for i in range(4)], []) + \
             [('chime', 14.0)]

    @staticmethod
    def make_bg(): return room_bg(tv=False)

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.0, 540, 960)), (21.5, (1.0, 540, 960))])

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
            caption(img, 'Which rumour do you / *think is true?*', t, 13.9, 30, 820, 58)
            caption(img, 'Comment below. Out 19 Nov 2026.', t, 15.2, 30, 1060, 40, GREY, POPM)
            caption(img, 'Prices: US list prices. Vary by region.', t, 15.6, 30, 1140, 30, FAINT, POPM)
            caption(img, DISC, t, 16.0, 30, 1200, 30, FAINT, POPM)


VIDS = {'1': FiveDaysFacts, '2': KiwiMate, '3': UpdateRequired, '4': WhichGamer2, '5': ConfirmedRumour}

if __name__ == '__main__':
    V = VIDS[sys.argv[1]]
    if len(sys.argv) > 2:
        f = frame_fn_v2(V, V.make_bg())
        ims = [cv2.resize(cv2.cvtColor(f(float(x)), cv2.COLOR_RGB2BGR), (432, 768)) for x in sys.argv[2:]]
        cv2.imwrite(f'{OUT}/still_{sys.argv[1]}.jpg', np.hstack(ims), [cv2.IMWRITE_JPEG_QUALITY, 82])
    else:
        build_v2(V, OUT, seed=int(sys.argv[1]) * 11); print('done', V.name)
