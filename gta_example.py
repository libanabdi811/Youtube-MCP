"""GTA 6 test Short: '5 days to GTA 6' countdown skit + confirmed facts. Original visuals only."""
import math, cv2, numpy as np
from engine import *
from viral import frame_fn_v2, build_v2, banner
from videos import STAND, SIT
import viral

WEEK = ['14', '15', '16', '17', '18', '19', '20']

def make_gamer_room():
    img = make_bg('none')
    # TV (generic neon screen)
    cv2.rectangle(img, (60, 700), (500, 960), (14, 14, 18), -1)
    g = np.linspace(0, 1, 236)[:, None]
    scr = (np.array([70, 20, 110]) * (1 - g) + np.array([240, 110, 90]) * g).astype(np.uint8)
    img[712:948, 72:488] = scr[:, None, :]
    cv2.circle(img, (280, 880), 70, (255, 214, 120), -1, cv2.LINE_AA)
    img[900:948, 72:488] = (40, 14, 60)
    cv2.rectangle(img, (240, 960), (320, 990), (30, 30, 36), -1)
    cv2.rectangle(img, (120, 990), (440, 1010), (44, 44, 52), -1)
    # sofa (right)
    cv2.rectangle(img, (560, 1000), (1040, 1112), (60, 50, 78), -1)
    cv2.rectangle(img, (560, 1112), (1040, 1185), (76, 64, 98), -1)
    for xx in (580, 1020): cv2.rectangle(img, (xx - 8, 1185), (xx + 8, 1250), (36, 34, 44), -1)
    return img

def calendar(img, t, cx=700, cy=540):
    w, h = 540, 230
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    cv2.rectangle(img, (x0, y0), (x0 + w, y0 + h), (232, 230, 224), -1)
    cv2.rectangle(img, (x0, y0), (x0 + w, y0 + 56), (200, 56, 70), -1)
    spr0 = label_sprite('NOVEMBER', (255, 255, 255), 30); blit(img, spr0, cx - spr0.shape[1] / 2, y0 + 6)
    cw = w / 7
    for i, d in enumerate(WEEK):
        spr = label_sprite(d, INK, 30)
        x = x0 + cw * i + cw / 2 - spr.shape[1] / 2 + 4
        blit(img, spr, x, y0 + 110)
        if d == '19':
            ellipse(img, (x0 + cw * i + cw / 2, y0 + 142), (34, 30), 0, 0, 360 * clamp(prog(t, 0.2, 0.9)), RED, 5)
        if d == '14':
            k = prog(t, 0.6, 1.1)
            c = (x0 + cw * i + cw / 2, y0 + 142)
            line(img, (c[0] - 24, c[1] - 24), (lerp(c[0] - 24, c[0] + 24, k), lerp(c[1] - 24, c[1] + 24, k)), RED, 6)
            if k >= 1: line(img, (c[0] + 24, c[1] - 24), (lerp(c[0] + 24, c[0] - 24, prog(t, 1.1, 1.4)), lerp(c[1] - 24, c[1] + 24, prog(t, 1.1, 1.4))), RED, 6)

def controller(img, hand):
    x, y = hand
    poly(img, [(x - 34, y - 14), (x + 34, y - 14), (x + 40, y + 12), (x - 40, y + 12)], (30, 30, 38))
    circle(img, (x - 16, y - 2), 5, (90, 90, 100)); circle(img, (x + 18, y - 2), 5, (255, 120, 140))

def fact_card(img, t, t0, y, num, text, sub=None):
    if t < t0: return
    k = eo(prog(t, t0, t0 + 0.35))
    x = lerp(-960, 70, k)
    hh = 186 if sub else 136
    over = img.copy()
    cv2.rectangle(over, (int(x), y), (int(x) + 940, y + hh), (18, 16, 26), -1)
    cv2.rectangle(over, (int(x), y), (int(x) + 16, y + hh), GOLD, -1)
    img[:] = (img * 0.03 + over * 0.97).astype(np.uint8)
    blit(img, label_sprite(num, GOLD, 70), x + 38, y + 22)
    blit(img, label_sprite(text, WHITE, 46), x + 130, y + 36)
    if sub: blit(img, label_sprite(sub, (175, 175, 184), 32), x + 132, y + 116)

class GTA5Days:
    name = 'gta6_test_5_days_to_go'; dur = 24.0
    banner = "GTA 6 IS 5 DAYS AWAY. / *HERE'S WHAT'S CONFIRMED.*"
    prog = ['Em', 'C', 'G', 'D']; bpm = 96
    bubbles = [(2.9, 4.6, "BRO... DID YOU\nSEE THE NEWS?!", (330, 900), 'say'),
               (4.7, 6.3, "NO. DON'T SAY\nDELAYED.", (800, 792), 'say'),
               (6.4, 8.0, "...IT'S STILL\nNOV 19.", (330, 900), 'say'),
               (8.2, 9.7, "LET'S GOOO!", (800, STAND), 'say')]
    events = [('boom', 0.0), ('tick', 0.7), ('tick', 1.15), ('pop', 2.3), ('thud', 4.7), ('chime', 8.2),
              ('whoosh', 9.8), ('thud', 10.0), ('thud', 12.4), ('thud', 14.8), ('whoosh', 17.6)]

    @staticmethod
    def make_bg(): return make_gamer_room()

    @staticmethod
    def cam(t):
        return kf(t, [(0.0, (1.8, 700, 600)), (1.6, (1.6, 700, 640)), (2.3, (1.0, 540, 960)), (4.7, (1.0, 540, 960)),
                      (4.95, (1.4, 800, 900)), (6.3, (1.4, 800, 900)), (6.6, (1.0, 540, 960)), (24, (1.0, 540, 960))])

    @staticmethod
    def shake(t):
        if 4.7 <= t < 5.2: return 1 - prog(t, 4.7, 5.2)
        if 8.2 <= t < 8.6: return 0.6 * (1 - prog(t, 8.2, 8.6))
        return 0.0

    @staticmethod
    def world(img, t):
        calendar(img, t)
        sk = kf(t, [(8.0, 1.0), (8.4, 0.0)])
        bob = -26 * abs(math.sin((t - 8.4) * 7)) if 8.4 <= t < 9.8 else 0
        mood = step(t, [(0, 'flat'), (4.7, 'sad'), (6.5, 'flat'), (7.6, 'smile')])
        p = person(img, 800, face=-1, sitk=sk, mood=mood, bob=bob,
                   front=(145, 15) if 8.2 <= t < 9.8 else (35, 75),
                   rear=(-145, -15) if 8.2 <= t < 9.8 else (-6, 10))
        if not (8.2 <= t < 9.8): controller(img, p['fh'])
        if 8.2 <= t < 9.8: glow(img, (800, 800), 240, GOLD, 0.35)
        # friend's call shown as a phone icon near TV side
        if 2.3 <= t < 8.1:
            pc = (330, 1010)
            glow(img, pc, 110, BLUE, 0.3)
            poly(img, [(pc[0] - 30, pc[1] - 50), (pc[0] + 30, pc[1] - 50), (pc[0] + 30, pc[1] + 50), (pc[0] - 30, pc[1] + 50)], (40, 42, 50))
            poly(img, [(pc[0] - 24, pc[1] - 42), (pc[0] + 24, pc[1] - 42), (pc[0] + 24, pc[1] + 42), (pc[0] - 24, pc[1] + 42)], (150, 195, 255))
            blit(img, label_sprite('FRIEND', INK, 14), pc[0] - 30, pc[1] - 12)

    @staticmethod
    def ui(img, t):
        if t < 2.4:
            spr = label_sprite('5 DAYS', GOLD, 96)
            s2 = scaled(spr, 0.8 + 0.2 * back(prog(t, 0.0, 0.3))); blit(img, s2, (W - s2.shape[1]) / 2, 1010)
        if t >= 9.8:
            k = sm(prog(t, 9.8, 10.1))
            img[:] = (img.astype(np.float32) * (1 - 0.85 * k)).astype(np.uint8)
            fact_card(img, t, 10.0, 470, '1', 'OUT 19 NOV 2026')
            fact_card(img, t, 12.4, 660, '2', 'PS5 + XBOX SERIES X|S', 'PC: NOT CONFIRMED YET')
            fact_card(img, t, 14.8, 900, '3', 'SET IN LEONIDA,', 'HOME OF VICE CITY')
        caption(img, 'Day one... or *waiting for reviews?*', t, 17.6, 30, 1420, 56)
        caption(img, 'Tell me in the comments.', t, 18.6, 30, 1520, 42, (200, 200, 206), POPM)
        caption(img, 'Fan-made. Not affiliated with Rockstar Games.', t, 19.4, 30, 1590, 30, (130, 130, 138), POPM)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        f = frame_fn_v2(GTA5Days, GTA5Days.make_bg())
        for t in [float(x) for x in sys.argv[1:]]:
            cv2.imwrite(f'/home/claude/shorts/out4/s_{t:05.1f}.jpg', cv2.cvtColor(f(t), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 80])
    else:
        build_v2(GTA5Days, '/home/claude/shorts/out4', seed=19); print('done')
