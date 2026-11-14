"""GTA 6 fan Shorts, 2026-11-14 batch (VIRAL FORMAT v2). 100% original visuals: stick figures, neon shapes, text cards.
Facts used (sources in TOPICS.md): out 19 Nov 2026; digital pre-load opened 10 Nov; up to 212 GB; free printable map + poster
on Rockstar's site on launch day; Xbox One via Xbox Cloud Gaming from 1am ET 19 Nov (buy the game, Series S settings);
no PC version announced."""
import math, sys, os, cv2, numpy as np
from engine import *
from viral import frame_fn_v2, build_v2
from gta_example import controller

OUT = '/home/claude/shorts/out_2026-11-14'
os.makedirs(OUT, exist_ok=True)
FL = 1420                     # floor line for our rooms
GREEN = (80, 220, 130)
PINK = (255, 92, 170)
CYAN = (70, 220, 240)
DISC = 'Fan-made. Not affiliated with Rockstar Games.'

# ---------------- shared scenes / props ----------------
def room_bg(tv=True):
    img = np.zeros((H, W, 3), np.float32)
    img[:FL] = vgrad(FL, (12, 12, 20), (30, 28, 40))[:, None, :]
    img[FL:] = vgrad(H - FL, (46, 42, 54), (14, 14, 18))[:, None, :]
    img = img.astype(np.uint8)
    if tv:
        cv2.rectangle(img, (110, 420), (970, 830), (10, 10, 14), -1)
        g = vgrad(386, (22, 18, 46), (10, 12, 26)).astype(np.uint8)
        img[432:818, 122:958] = g[:, None, :]
        cv2.rectangle(img, (500, 830), (580, 880), (26, 26, 32), -1)
        cv2.rectangle(img, (300, 880), (780, 900), (40, 40, 48), -1)
    return img

def sofa(img, x0, x1):
    cv2.rectangle(img, (x0, 1180), (x1, 1292), (60, 50, 78), -1)
    cv2.rectangle(img, (x0, 1292), (x1, 1360), (76, 64, 98), -1)
    for xx in (x0 + 20, x1 - 20): cv2.rectangle(img, (xx - 8, 1360), (xx + 8, FL), (36, 34, 44), -1)

def neon_bg():
    img = np.zeros((H, W, 3), np.float32)
    img[:1250] = vgrad(1250, (24, 10, 52), (255, 110, 90))[:, None, :]
    img[1250:] = vgrad(H - 1250, (40, 10, 60), (8, 6, 16))[:, None, :]
    img = img.astype(np.uint8)
    # striped sun
    sun = np.zeros_like(img)
    cv2.circle(sun, (540, 1150), 300, (255, 200, 90), -1, cv2.LINE_AA)
    for i, y in enumerate(range(1060, 1260, 34)):
        cv2.rectangle(sun, (0, y), (W, y + 6 + i * 3), (0, 0, 0), -1)
    m = sun.sum(axis=2) > 0
    img[m] = sun[m]
    img[1250:] = (vgrad(H - 1250, (40, 10, 60), (8, 6, 16))[:, None, :]).astype(np.uint8)
    # perspective grid
    for i in range(-12, 13):
        cv2.line(img, (540 + i * 40, 1250), (540 + i * 260, H), (255, 60, 170), 2, cv2.LINE_AA)
    y = 1250.0; d = 12.0
    while y < H:
        cv2.line(img, (0, int(y)), (W, int(y)), (255, 60, 170), 2, cv2.LINE_AA); y += d; d *= 1.32
    cv2.line(img, (0, 1250), (W, 1250), (255, 140, 210), 4, cv2.LINE_AA)
    return img

def dim(img, t, t0, k=0.85):
    a = sm(prog(t, t0, t0 + 0.3))
    if a > 0: img[:] = (img.astype(np.float32) * (1 - k * a)).astype(np.uint8)

def fit_sprite(text, color, size, maxw):
    spr = label_sprite(text, color, size)
    if spr.shape[1] > maxw: spr = scaled(spr, maxw / spr.shape[1])
    return spr

def card(img, t, t0, y, num, text, sub=None, accent=GOLD):
    if t < t0: return
    k = eo(prog(t, t0, t0 + 0.35))
    x = lerp(-960, 70, k)
    hh = 190 if sub else 136
    over = img.copy()
    cv2.rectangle(over, (int(x), y), (int(x) + 940, y + hh), (18, 16, 26), -1)
    cv2.rectangle(over, (int(x), y), (int(x) + 16, y + hh), accent, -1)
    img[:] = (img * 0.03 + over * 0.97).astype(np.uint8)
    blit(img, label_sprite(num, accent, 70), x + 38, y + 22)
    blit(img, fit_sprite(text, WHITE, 46, 790), x + 130, y + 36)
    if sub: blit(img, fit_sprite(sub, (185, 185, 194), 30, 790), x + 132, y + 116)

def big_text(img, text, t, t0, y, size, color=WHITE, hl=GOLD, pop=True):
    if t < t0: return
    spr = rich_sprite(text, POPB, size, color, hl, 1000)
    s = 0.7 + 0.3 * back(prog(t, t0, t0 + 0.3)) if pop else 1.0
    s2 = scaled(spr, s)
    blit(img, s2, (W - s2.shape[1]) / 2, y - s2.shape[0] / 2)

def cloud_icon(img, c, k, col=(220, 236, 255)):
    if k <= 0: return
    x, y = c; r = 46 * k
    glow(img, c, 220 * k, BLUE, 0.4)
    for dx, dy, rr in [(-1.1, 0.2, 0.8), (0, -0.3, 1.1), (1.1, 0.2, 0.8)]:
        circle(img, (x + dx * r, y + dy * r), rr * r, col)
    poly(img, [(x - 1.9 * r, y + 0.2 * r), (x + 1.9 * r, y + 0.2 * r), (x + 1.9 * r, y + 0.95 * r), (x - 1.9 * r, y + 0.95 * r)], col)

def stamp(img, text, t, t0, c, col, size=64):
    if t < t0: return
    k = back(prog(t, t0, t0 + 0.25))
    spr = label_sprite(text, col, size)
    h, w = spr.shape[:2]
    box = np.zeros((h + 30, w + 30, 4), np.uint8)
    cv2.rectangle(box, (4, 4), (w + 25, h + 25), col + (255,), 8)
    box[15:15 + h, 15:15 + w] = np.maximum(box[15:15 + h, 15:15 + w], spr)
    M = cv2.getRotationMatrix2D(((w + 30) / 2, (h + 30) / 2), 8, 1.0)
    box = cv2.warpAffine(box, M, (w + 30, h + 30))
    s2 = scaled(box, 1.8 - 0.8 * k)
    blit(img, s2, c[0] - s2.shape[1] / 2, c[1] - s2.shape[0] / 2, clamp(k * 1.5))

def progress_bar(img, x0, y, w, frac, col=GREEN, h=34):
    cv2.rectangle(img, (x0, y), (x0 + w, y + h), (50, 50, 60), -1)
    cv2.rectangle(img, (x0, y), (x0 + int(w * frac), y + h), col, -1)
    cv2.rectangle(img, (x0, y), (x0 + w, y + h), (200, 200, 210), 3)

# =========================================================
# V1  Countdown: 5 days, 3 things to do (confirmed facts)
# =========================================================
class Countdown5:
    name = '2026-11-14_gta6_5_days_3_things'; dur = 22.0
    banner = "GTA 6 IS 5 DAYS AWAY. / *DO THESE 3 THINGS NOW.*"
    prog = ['Am', 'F', 'C', 'G']; bpm = 110
    bubbles = [(2.6, 4.3, "5 DAYS?!\nI'M NOT READY!", (540, 1060), 'say'),
               (12.6, 14.4, "PRE-LOAD OPENED\n4 DAYS AGO?!", (540, 1060), 'say')]
    events = [('tick', 0.0), ('boom', 0.6), ('whoosh', 4.4), ('thud', 4.6), ('thud', 7.0), ('boom', 7.3),
              ('thud', 9.6), ('whoosh', 12.4), ('chime', 14.6), ('whoosh', 15.0)]

    @staticmethod
    def make_bg(): return neon_bg()

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.2, 540, 900)), (2.4, (1.0, 540, 960)), (2.6, (1.25, 540, 1150)), (4.3, (1.25, 540, 1150)),
                      (4.5, (1.0, 540, 960)), (12.4, (1.0, 540, 960)), (12.6, (1.3, 540, 1150)), (14.4, (1.3, 540, 1150)),
                      (14.8, (1.0, 540, 960)), (22, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if 0.6 <= t < 1.1: return 1 - prog(t, 0.6, 1.1)
        if 7.3 <= t < 7.8: return 0.8 * (1 - prog(t, 7.3, 7.8))
        if 12.6 <= t < 13.0: return 0.6
        return 0.0

    @staticmethod
    def world(img, t):
        # gamer in front of the sun (on stage 0-4.4 and 12.4-14.6)
        on = t < 4.5 or 12.3 <= t < 14.8
        if on:
            panic = 2.6 <= t < 4.4 or 12.6 <= t < 14.5
            p = person(img, 540, y=1620, face=1, mood='sad' if panic else 'flat',
                       front=(150, 20) if panic else (35, 75), rear=(-150, -20) if panic else (-6, 10),
                       bob=-14 * abs(math.sin(t * 9)) if panic else 0)
            if not panic: controller(img, p['fh'])

    @staticmethod
    def ui(img, t):
        if t < 2.5:
            d = '6' if t < 0.6 else '5'
            k = sm(prog(t, 0.6, 0.75))
            glow(img, (540, 820), 420, PINK, 0.5)
            big_text(img, d, t, 0.6 if d == '5' else 0.0, 760, 380, WHITE, GOLD, pop=d == '5')
            big_text(img, 'DAYS LEFT', t, 0.0, 1010, 96, GOLD, GOLD, pop=False)
        if 4.4 <= t < 12.4 or t >= 14.6:
            dim(img, t, 4.4 if t < 12.4 else 14.6)
        if 4.4 <= t < 12.4:
            card(img, t, 4.6, 520, '1', 'PRE-LOAD IS LIVE', 'DIGITAL: OPEN SINCE 10 NOV')
            card(img, t, 7.0, 750, '2', 'MAKE ROOM: 212 GB', 'ROCKSTAR SAYS UP TO 212 GB', RED)
            card(img, t, 9.6, 980, '3', 'DAY 1: FREE MAP+POSTER', "PRINTABLE, ON ROCKSTAR'S SITE")
            caption(img, 'Out *19 November 2026.*', t, 10.3, 12.3, 1290, 50)
        if t >= 14.6:
            card(img, t, 14.6, 560, '!', 'OUT 19 NOV 2026', 'PS5 + XBOX SERIES X|S')
            caption(img, 'Already pre-loaded... or *still deleting games?*', t, 15.2, 30, 1300, 54)
            caption(img, 'Tell me in the comments.', t, 16.4, 30, 1480, 42, (200, 200, 206), POPM)
            caption(img, DISC, t, 17.0, 30, 1560, 30, (130, 130, 138), POPM)

# =========================================================
# V2  Skit: 212 GB, he picks the wrong game to delete
# =========================================================
GAMES = [("OLD RACING GAME", "48 GB"), ("ZOMBIE SHOOTER", "75 GB"), ("FARM GAME", "140 GB"), ("MY OLD SAVES", "9 GB")]

def storage_ui(img, t):
    x0, y0 = 150, 455
    alert = t < 13.2
    hdr = (200, 50, 64) if alert else (40, 150, 90)
    if alert and t < 2.0 and int(t * 6) % 2: hdr = (140, 30, 44)
    cv2.rectangle(img, (x0, y0), (x0 + 780, y0 + 70), hdr, -1)
    hs = fit_sprite('NOT ENOUGH STORAGE' if alert else 'STORAGE: READY', WHITE, 36, 740)
    blit(img, hs, x0 + 390 - hs.shape[1] / 2, y0 + 8)
    blit(img, fit_sprite('GTA 6 NEEDS UP TO 212 GB', GOLD, 26, 740), x0 + 20, y0 + 84)
    sel = 2 if 3.6 <= t < 13.2 else (-1 if t < 2.2 else int(clamp((t - 2.2) / 0.7, 0, 2)))
    for i, (g, s) in enumerate(GAMES):
        y = y0 + 140 + i * 56
        if i == sel and t < 13.2: cv2.rectangle(img, (x0 + 6, y - 6), (x0 + 774, y + 46), (60, 60, 90), -1)
        col = WHITE
        gone = (i in (0, 1, 3)) and t >= 13.4 + 0.35 * i * 0.5
        if gone: col = (110, 110, 120)
        if i == 2 and t >= 7.6: g = "MUM'S FARM (900 HRS)"; col = PINK
        blit(img, fit_sprite(g, col, 28, 560), x0 + 20, y)
        blit(img, label_sprite(s, col, 28), x0 + 620, y)
        if gone: cv2.line(img, (x0 + 20, y + 22), (x0 + 760, y + 22), RED, 4, cv2.LINE_AA)
    if 4.9 <= t < 6.0:  # delete confirm popup
        cv2.rectangle(img, (330, 600), (750, 720), (20, 20, 28), -1); cv2.rectangle(img, (330, 600), (750, 720), RED, 4)
        sp = label_sprite('DELETE? [YES]', WHITE, 34); blit(img, sp, 540 - sp.shape[1] / 2, 636)

class WrongDelete:
    name = '2026-11-14_gta6_212gb_wrong_game'; dur = 24.0
    banner = "HE NEEDED 212 GB FOR GTA 6. / *HE PICKED THE WRONG GAME.*"
    prog = ['Dm', 'Bb', 'F', 'C']; bpm = 104
    bubbles = [(0.3, 2.0, "212 GB?!", (380, 1010), 'say'),
               (2.2, 3.8, "WHAT'S BIG...", (380, 1010), 'think'),
               (3.9, 5.5, "FARM GAME?\nNEVER PLAYED IT.", (380, 1010), 'say'),
               (5.9, 7.4, "STOP.", (990, 900), 'say'),
               (7.6, 9.3, "THAT'S MY FARM.\n900 HOURS.", (820, 880), 'say'),
               (9.4, 11.0, "YOU... PLAY\nGAMES?!", (380, 1010), 'say'),
               (11.1, 13.1, "WHO DO YOU THINK\nPRE-ORDERED\nGTA 6?", (820, 880), 'say'),
               (13.3, 15.0, "...DELETING\nMY OWN STUFF.", (380, 1010), 'say'),
               (15.1, 16.6, "AND I PLAY\nFIRST.", (820, 880), 'say')]
    events = [('boom', 0.0), ('tick', 2.4), ('tick', 3.1), ('tick', 3.6), ('pop', 4.9), ('thud', 5.9),
              ('whoosh', 6.2), ('thud', 11.2), ('crack', 13.4), ('crack', 13.6), ('crack', 13.8), ('chime', 14.2),
              ('whoosh', 16.8)]

    @staticmethod
    def make_bg():
        img = room_bg(); sofa(img, 160, 640); return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.3, 540, 760)), (2.0, (1.3, 540, 760)), (2.2, (1.0, 540, 960)), (5.8, (1.0, 540, 960)),
                      (6.0, (1.15, 760, 1000)), (7.4, (1.15, 760, 1000)), (7.6, (1.0, 540, 960)), (11.1, (1.0, 540, 960)),
                      (24, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if t < 0.5: return 1 - prog(t, 0, 0.5)
        if 5.9 <= t < 6.4: return 1 - prog(t, 5.9, 6.4)
        if 11.1 <= t < 11.5: return 0.5
        return 0.0

    @staticmethod
    def world(img, t):
        storage_ui(img, t)
        shock = t < 2.0 or 5.9 <= t < 7.5 or 9.4 <= t < 11.0 or 11.1 <= t < 13.1
        gm = 'sad' if shock else ('smile' if 14.2 <= t < 15.0 or t > 16.6 else 'flat')
        p = person(img, 380, y=FL, face=1, sitk=1, mood=gm, front=(35, 75), bob=-10 * abs(math.sin(t * 10)) if t < 1.0 else 0)
        controller(img, p['fh'])
        if t >= 6.0:
            wk = prog(t, 6.0, 7.4)
            mx = lerp(1200, 820, eo(wk))
            mm = 'angry' if t < 11.0 else 'smile'
            person(img, mx, y=FL, face=-1, hair=True, dress=True, mood=mm,
                   walk=(t * 9, 1 - wk) if wk < 1 else None,
                   front=(150, 10) if 5.9 <= t < 9.4 else (20, 20), rear=(-20, 40) if t >= 9.4 else (-6, 10))
        if t >= 16.6: pop_heart(img, (600, 760), t, 16.6, 60)

    @staticmethod
    def ui(img, t):
        if t >= 16.8:
            dim(img, t, 16.8)
            card(img, t, 16.8, 520, '!', 'UP TO 212 GB', "ROCKSTAR'S FIGURE. PRE-LOAD IS LIVE.", RED)
            caption(img, 'What would YOU delete *for GTA 6?*', t, 17.4, 30, 1240, 56)
            caption(img, 'Tell me below.', t, 18.6, 30, 1420, 42, (200, 200, 206), POPM)
            caption(img, DISC, t, 19.2, 30, 1500, 30, (130, 130, 138), POPM)

# =========================================================
# V3  Which gamer are you on GTA 6 night?
# =========================================================
PANELS = [((275, 680), '1. THE SPEEDRUNNER'), ((805, 680), '2. THE TOURIST'),
          ((275, 1170), '3. THE CHAOS ONE'), ((805, 1170), '4. THE PATIENT ONE')]

def burst(img, c, r, col, k):
    pts = []
    for i in range(16):
        a = i / 16 * 2 * math.pi; rr = r * (1.0 if i % 2 == 0 else 0.5) * k
        pts.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a)))
    poly(img, pts, col)

def panel(img, t, i, active):
    (cx, cy), lab = PANELS[i]
    x0, y0, x1, y1 = cx - 245, cy - 220, cx + 245, cy + 220
    keep = img.copy()
    cv2.rectangle(img, (x0, y0), (x1, y1), (24, 22, 34), -1)
    gy = cy + 160
    if i == 0:
        for j in range(4):
            yy = cy - 30 + j * 40; xx = cx - 200 + ((t * 600 + j * 90) % 160)
            line(img, (xx, yy), (xx + 70, yy), (120, 120, 140), 5)
        person(img, cx + 20, y=gy, s=0.48, face=1, mood='angry', walk=(t * 14, 1), lean=12)
    elif i == 1:
        circle(img, (cx + 120, cy - 60), 60, (255, 170, 90))
        cv2.rectangle(img, (x0, cy - 20), (x1, cy - 10), (24, 22, 34), -1)
        person(img, cx - 40, y=gy, s=0.48, face=1, mood='smile', front=(150, -60))
    elif i == 2:
        burst(img, (cx + 110, cy - 40), 90, (255, 150, 60), 0.85 + 0.15 * math.sin(t * 12))
        person(img, cx - 40, y=gy, s=0.48, face=1, mood='smile', front=(150, 15), rear=(-150, -15),
               bob=-12 * abs(math.sin(t * 8)))
    else:
        circle(img, (cx + 130, cy - 70), 48, (230, 230, 236)); circle(img, (cx + 130, cy - 70), 42, (40, 40, 50))
        a = t * 3
        line(img, (cx + 130, cy - 70), (cx + 130 + 30 * math.sin(a), cy - 70 - 30 * math.cos(a)), GOLD, 5)
        person(img, cx - 40, y=gy, s=0.48, face=1, sitk=1, mood='flat', front=(70, 100), rear=(70, 100))
        cv2.rectangle(img, (cx - 110, gy - 70), (cx + 30, gy), (60, 50, 78), -1)
    m = np.ones(img.shape[:2], bool); m[y0:y1, x0:x1] = False
    img[m] = keep[m]
    col = GOLD if active else (60, 60, 72)
    cv2.rectangle(img, (x0, y0), (x1, y1), col, 6 if active else 3)
    blit(img, fit_sprite(lab, GOLD if active else (150, 150, 160), 28, 460), x0 + 12, y1 - 50)
    if not active:
        sub = img[y0 + 3:y1 - 2, x0 + 3:x1 - 2]
        sub[:] = (sub * 0.45).astype(np.uint8)

class WhichGamer:
    name = '2026-11-14_gta6_which_gamer_are_you'; dur = 22.5
    banner = "5 GAMERS ON GTA 6 NIGHT. / *WHICH ONE ARE YOU?*"
    prog = ['C', 'G', 'Am', 'F']; bpm = 116
    bubbles = [(0.2, 2.4, "STORY. NOW.\nNO DISTRACTIONS.", (315, 595), 'say'),
               (2.7, 5.0, "I'M JUST GONNA\nLOOK AROUND.", (845, 595), 'say'),
               (5.3, 7.6, "WHAT DOES THIS\nBUTTON DO?", (315, 1085), 'say'),
               (7.9, 10.2, "I'LL WAIT FOR\nTHE REVIEWS.", (845, 1085), 'say'),
               (12.0, 14.0, "COME ON...\nCOME ON...", (540, 1000), 'say')]
    events = [('pop', 0.0), ('whoosh', 2.6), ('whoosh', 5.2), ('boom', 5.4), ('whoosh', 7.8), ('tick', 9.0),
              ('thud', 10.5), ('tick', 11.6), ('tick', 12.4), ('tick', 13.2), ('thud', 14.2), ('whoosh', 15.0)]
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
        if 5.3 <= t < 5.8: return 0.8 * (1 - prog(t, 5.3, 5.8))
        if 14.2 <= t < 14.7: return 1 - prog(t, 14.2, 14.7)
        return 0.0

    @staticmethod
    def world(img, t):
        if t < 10.6:
            act = min(3, int(t / 2.6)) if t < 10.4 else -1
            for i in range(4): panel(img, t, i, i == act)
        else:
            # #5 full-screen: stuck at 99 %
            cv2.rectangle(img, (110, 440), (970, 830), (10, 10, 14), -1)
            img[452:818, 122:958] = (22, 18, 40)
            frac = kf(t, [(10.8, 0.86), (11.8, 0.99), (22.5, 0.99)])
            progress_bar(img, 200, 640, 680, frac)
            pct = label_sprite(f'{int(frac * 100)}%', WHITE, 44); blit(img, pct, 540 - pct.shape[1] / 2, 560)
            blit(img, fit_sprite('DOWNLOADING...', (180, 180, 196), 30, 600), 330, 720)
            sofa(img, 280, 800)
            p = person(img, 540, y=FL, face=1, sitk=1, mood='sad' if t >= 14.2 else 'flat', front=(35, 75),
                       bob=-8 * abs(math.sin(t * 6)))
            controller(img, p['fh'])

    @staticmethod
    def ui(img, t):
        if 10.4 <= t < 12.0:
            a = win(t, 10.4, 11.8, 0.2)
            dim(img, t, 10.4, 0.5 * a)
            caption(img, "...and there's *always a #5.*", t, 10.5, 11.8, 1000, 70)
        if 11.9 <= t < 14.8:
            caption(img, '5. *THE ONE STUCK AT 99%*', t, 11.9, 14.6, 1480, 54)
        if t >= 14.8:
            dim(img, t, 14.8)
            caption(img, 'Which one are you? / *Comment 1 to 5.*', t, 15.0, 30, 1050, 58)
            caption(img, 'Tag your friend who is number 3.', t, 16.2, 30, 1240, 42, (200, 200, 206), POPM)
            caption(img, 'GTA 6 is out 19 November 2026.', t, 16.8, 30, 1330, 42, (200, 200, 206), POPM)
            caption(img, DISC, t, 17.2, 30, 1440, 30, (130, 130, 138), POPM)

# =========================================================
# V4  Skit: console from 2013 (Xbox One via cloud)
# =========================================================
def old_console(img, t):
    x0, y0 = 370, 905
    cv2.rectangle(img, (x0, y0), (x0 + 340, y0 + 70), (34, 34, 38), -1)
    cv2.rectangle(img, (x0, y0), (x0 + 340, y0 + 70), (70, 70, 76), 3)
    cv2.rectangle(img, (x0 + 230, y0 + 14), (x0 + 320, y0 + 56), (24, 24, 28), -1)
    for k in range(3):  # cobweb
        ellipse(img, (x0 + 4, y0 + 4), (26 + k * 16, 26 + k * 16), 0, 0, 90, (170, 170, 176), 2)
    line(img, (x0 + 4, y0 + 4), (x0 + 60, y0 + 50), (170, 170, 176), 2)
    sp = label_sprite('2013', (150, 150, 156), 22); blit(img, sp, x0 + 20, y0 + 22)

class CloudConsole:
    name = '2026-11-14_gta6_console_from_2013'; dur = 23.5
    banner = "HIS CONSOLE IS FROM 2013. / *IT STILL GETS GTA 6.*"
    prog = ['Em', 'C', 'D', 'Bm']; bpm = 100
    bubbles = [(0.2, 1.9, "BRO. THAT THING\nIS FROM 2013.", (300, 980), 'say'),
               (2.0, 3.6, "NO WAY IT\nRUNS GTA 6.", (300, 980), 'say'),
               (3.8, 5.4, "IT DOESN'T HAVE\nTO RUN IT.", (800, 1030), 'say'),
               (5.6, 7.1, "IT STREAMS IT.", (800, 1030), 'say'),
               (7.2, 8.6, "...WAIT, WHAT?", (300, 980), 'say')]
    events = [('boom', 0.0), ('thud', 2.0), ('whoosh', 5.5), ('chime', 5.7), ('thud', 7.2), ('whoosh', 8.7),
              ('thud', 9.0), ('thud', 11.2), ('thud', 13.4), ('whoosh', 15.8)]

    @staticmethod
    def make_bg():
        img = room_bg(); sofa(img, 600, 1040); return img

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.35, 460, 930)), (3.6, (1.3, 440, 960)), (3.8, (1.0, 540, 960)), (3.9, (1.25, 760, 1050)),
                      (5.4, (1.25, 760, 1050)), (5.6, (1.0, 540, 960)), (7.2, (1.0, 540, 960)), (7.3, (1.35, 320, 1000)),
                      (8.6, (1.35, 320, 1000)), (8.8, (1.0, 540, 960)), (23.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if t < 0.5: return 1 - prog(t, 0, 0.5)
        if 7.2 <= t < 7.7: return 1 - prog(t, 7.2, 7.7)
        return 0.0

    @staticmethod
    def world(img, t):
        old_console(img, t)
        ck = back(prog(t, 5.5, 5.9))
        if t >= 5.5:
            for j in range(5):
                yy = 905 - ((t * 140 + j * 40) % 200)
                circle(img, (540, yy), 6, (180, 210, 255))
            cloud_icon(img, (540, 640), ck)
            sp = label_sprite('XBOX CLOUD GAMING', WHITE, 28)
            blit(img, sp, 540 - sp.shape[1] / 2, 740, clamp(ck))
        fm = 'smile' if t < 3.6 else ('flat' if t < 7.2 else 'sad')
        person(img, 300, y=FL, face=1, mood=fm, front=(120, 0) if t < 3.6 else ((150, 15) if 7.2 <= t < 8.6 else (10, 12)),
               rear=(-150, -15) if 7.2 <= t < 8.6 else (-6, 10), bob=-8 * abs(math.sin(t * 12)) if t < 1.6 else 0)
        p = person(img, 800, y=FL, face=-1, sitk=1, mood='smile' if 5.6 <= t else 'flat', front=(35, 75))
        controller(img, p['fh'])

    @staticmethod
    def ui(img, t):
        if t >= 8.7:
            dim(img, t, 8.7)
            card(img, t, 9.0, 480, '1', 'XBOX ONE: VIA CLOUD', 'XBOX CLOUD GAMING, FROM DAY ONE', BLUE)
            card(img, t, 11.2, 700, '2', 'FROM 19 NOV, 1AM ET', 'THAT IS 6AM IN THE UK', BLUE)
            card(img, t, 13.4, 920, '3', 'CATCH: BUY THE GAME', 'STREAMS AT SERIES S SETTINGS', RED)
        if t >= 15.8:
            caption(img, 'Cloud on day one... or *wait for new hardware?*', t, 15.9, 30, 1250, 52)
            caption(img, 'Source: Xbox Wire, 10 Nov 2026.', t, 17.0, 30, 1430, 36, (200, 200, 206), POPM)
            caption(img, DISC, t, 17.4, 30, 1500, 30, (130, 130, 138), POPM)

# =========================================================
# V5  True or false (confirmed vs rumour)
# =========================================================
QUIZ = [("GTA 6 COMES OUT\nON 19 NOV 2026", 'TRUE', GREEN, 'CONFIRMED BY ROCKSTAR'),
        ("YOU CAN PLAY IT\nON PC AT LAUNCH", 'FALSE', RED, 'NO PC VERSION ANNOUNCED. PC LATER = RUMOUR'),
        ("YOU CAN PLAY IT\nON AN XBOX ONE", 'TRUE', GREEN, 'VIA XBOX CLOUD GAMING. YOU STILL BUY IT.'),
        ("PRE-LOAD HASN'T\nSTARTED YET", 'FALSE', RED, 'DIGITAL PRE-LOAD OPENED 10 NOV')]
QT = 3.4

class TrueFalse:
    name = '2026-11-14_gta6_true_or_false'; dur = 21.5
    banner = "GTA 6: TRUE OR FALSE? / *#3 SOUNDS FAKE. IT'S NOT.*"
    prog = ['Gm', 'Eb', 'Bb', 'F']; bpm = 120
    bubbles = [(9.0, 10.1, "WAIT, WHAT?!", (820, 1290), 'say')]
    events = sum([[('tick', i * QT + 0.4), ('tick', i * QT + 1.0), ('tick', i * QT + 1.6),
                   ('boom' if i == 2 else 'thud', i * QT + 2.0), ('whoosh', i * QT + 3.3)] for i in range(4)], []) + \
             [('chime', 14.0)]

    @staticmethod
    def make_bg(): return room_bg(tv=False)

    @staticmethod
    def cam(t):
        return kf(t, [(0, (1.0, 540, 960)), (8.8, (1.0, 540, 960)), (8.9, (1.15, 540, 900)), (10.0, (1.15, 540, 900)),
                      (10.2, (1.0, 540, 960)), (21.5, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if 8.8 <= t < 9.3: return 1 - prog(t, 8.8, 9.3)
        return 0.0

    @staticmethod
    def world(img, t):
        i = int(t / QT)
        if i < 4:
            st, verdict, col, note = QUIZ[i]
            lt = t - i * QT
            num = label_sprite(f'#{i + 1} OF 4', GOLD, 34); blit(img, num, 540 - num.shape[1] / 2, 470)
            cv2.rectangle(img, (70, 540), (1010, 860), (24, 22, 36), -1)
            cv2.rectangle(img, (70, 540), (1010, 860), (90, 80, 130), 4)
            for j, ln in enumerate(st.split('\n')):
                sp = fit_sprite(ln, WHITE, 50, 880); blit(img, sp, 540 - sp.shape[1] / 2, 610 + j * 100)
            if lt < 2.0: progress_bar(img, 190, 900, 700, 1 - lt / 2.0, GOLD, 22)
            stamp(img, verdict, t, i * QT + 2.0, (540, 990), col, 72)
            if lt >= 2.2:
                sp = fit_sprite(note, (210, 210, 220), 28, 960); blit(img, sp, 540 - sp.shape[1] / 2, 1090)
            mood = 'sad' if (i == 2 and lt >= 2.0) else ('smile' if lt >= 2.0 else 'flat')
        else:
            mood = 'smile'
        p = person(img, 820, y=1700, s=0.75, face=-1, mood=mood,
                   front=(150, 15) if 8.8 <= t < 10.2 else (35, 75), rear=(-150, -15) if 8.8 <= t < 10.2 else (-6, 10))
        if not (8.8 <= t < 10.2): controller(img, p['fh'])

    @staticmethod
    def ui(img, t):
        if t >= 13.7:
            dim(img, t, 13.7)
            caption(img, 'How many did you get right? *Comment your score.*', t, 13.9, 30, 820, 58)
            caption(img, 'Out 19 Nov 2026 on PS5 and Xbox Series X|S.', t, 15.2, 30, 1060, 38, (200, 200, 206), POPM)
            caption(img, DISC, t, 15.8, 30, 1150, 30, (130, 130, 138), POPM)

VIDS = {'1': Countdown5, '2': WrongDelete, '3': WhichGamer, '4': CloudConsole, '5': TrueFalse}

if __name__ == '__main__':
    V = VIDS[sys.argv[1]]
    if len(sys.argv) > 2:
        f = frame_fn_v2(V, V.make_bg())
        ims = [cv2.resize(cv2.cvtColor(f(float(x)), cv2.COLOR_RGB2BGR), (432, 768)) for x in sys.argv[2:]]
        cv2.imwrite(f'{OUT}/still_{sys.argv[1]}.jpg', np.hstack(ims), [cv2.IMWRITE_JPEG_QUALITY, 82])
    else:
        build_v2(V, OUT, seed=int(sys.argv[1]) * 7); print('done', V.name)
