"""Three neon GTA 6 Shorts from one script-driven template. Original visuals only."""
import sys, cv2
from neon import *

HANDLE = '@LeonidaUnlocked89'
DISC = 'Fan channel. Not affiliated with Rockstar Games.'

class Scripted:
    """lines: (t0, t1, text, y, size, color); hits: beat drops; police: list of (a, b) windows."""
    def __init__(self, name, dur, lines, hits, police=(), sirens=()):
        self.name, self.dur, self.lines, self.hits = name, dur, lines, hits
        self.risers = hits[1:]; self.sirens = list(sirens); self.police = police
        self.city = City()

    def frame(self, t):
        pol = 1.0 if any(a <= t < b for a, b in self.police) else 0.0
        img = self.city.draw(t, 1.0 + 0.06 * eo(prog(t % 4.0, 0, 4.0)), pol)
        for t0, t1, text, y, size, col in self.lines:
            slam(img, text, t, t0, t1, y, size, col)
        slam(img, HANDLE, t, 0, 99, 1480, 34, (230, 230, 240), 1.0)
        if t > self.dur - 3.2:
            slam(img, DISC, t, self.dur - 3.2, self.dur, 1560, 30, (210, 210, 220), 1.0)
        sk = max([1 - prog(t, h, h + 0.35) for h in self.hits if h <= t] + [0])
        img = shake_img(img, sk * 0.8, t)
        img = flash(img, max([0.55 * (1 - prog(t, h, h + 0.12)) for h in self.hits if h <= t] + [0]))
        img = glitch(img, t, max([1 - prog(t, h - 0.15, h + 0.1) for h in self.hits[1:] if h - 0.15 <= t < h + 0.1] + [0]))
        return img

# 1 - reviews
REVIEWS = Scripted('2026-11-18_gta6_99_metacritic', 21.0, [
    (0.0, 3.0, 'GTA 6 JUST SCORED', 620, 96, WHITE),
    (0.4, 3.0, '99', 840, 300, YEL),
    (3.1, 7.0, 'ON METACRITIC', 680, 110, LIME),
    (3.6, 7.0, 'TIED FOR THE', 860, 84, WHITE),
    (4.2, 7.0, 'HIGHEST EVER', 990, 120, PINK),
    (7.1, 11.0, 'LEVEL WITH', 660, 90, WHITE),
    (7.5, 11.0, 'ZELDA: OCARINA', 820, 96, CYAN),
    (7.9, 11.0, 'OF TIME (1998)', 950, 96, CYAN),
    (11.1, 15.0, '100%', 680, 220, LIME),
    (11.5, 15.0, 'OF CRITICS', 880, 100, WHITE),
    (11.9, 15.0, 'RECOMMEND IT', 1000, 100, WHITE),
    (15.1, 21.0, 'DESERVED 10/10', 660, 110, YEL),
    (15.7, 21.0, 'OR OVERHYPED?', 820, 120, PINK),
    (16.8, 21.0, 'COMMENT BELOW', 1000, 74, LIME),
], [0.0, 0.4, 3.1, 7.1, 11.1, 15.1])

# 2 - the 13-year wait
WAIT = Scripted('2026-11-18_gta6_13_year_wait', 21.0, [
    (0.0, 3.0, 'YOU WAITED', 620, 120, WHITE),
    (0.4, 3.0, '13 YEARS', 820, 200, YEL),
    (3.1, 7.0, 'GTA 5', 640, 150, LIME),
    (3.5, 7.0, 'SEPT 2013', 860, 130, WHITE),
    (7.1, 11.0, 'GTA 6', 640, 150, PINK),
    (7.5, 11.0, '19 NOV 2026', 860, 130, WHITE),
    (11.1, 15.0, "THAT'S", 640, 110, WHITE),
    (11.4, 15.0, '4,811 DAYS', 840, 170, CYAN),
    (15.1, 21.0, 'HOW OLD WERE YOU', 660, 96, WHITE),
    (15.6, 21.0, 'IN 2013?', 840, 160, YEL),
    (16.8, 21.0, 'COMMENT BELOW', 1010, 74, LIME),
], [0.0, 0.4, 3.1, 7.1, 11.1, 15.1])

# 3 - PS5 or Xbox
PLATFORM = Scripted('2026-11-18_gta6_ps5_or_xbox', 20.0, [
    (0.0, 3.0, 'WHERE ARE YOU', 640, 120, WHITE),
    (0.4, 3.0, 'PLAYING GTA 6?', 820, 120, YEL),
    (3.1, 7.0, 'PS5', 760, 280, CYAN),
    (7.1, 11.0, 'XBOX SERIES X|S', 760, 110, LIME),
    (11.1, 14.5, 'PC?', 680, 220, WHITE),
    (11.6, 14.5, 'NOT ANNOUNCED YET', 900, 84, RED),
    (14.6, 20.0, 'PS5 OR XBOX?', 660, 130, YEL),
    (15.2, 20.0, 'TEAM PS5 OR TEAM XBOX', 840, 70, WHITE),
    (16.0, 20.0, 'COMMENT YOURS', 1000, 84, PINK),
], [0.0, 0.4, 3.1, 7.1, 11.1, 14.6], police=[(11.1, 14.5)], sirens=[11.1])

SHORTS = {'1': REVIEWS, '2': WAIT, '3': PLATFORM}

if __name__ == '__main__':
    V = SHORTS[sys.argv[1]]
    if len(sys.argv) > 2:
        for t in map(float, sys.argv[2:]):
            cv2.imwrite(f'/home/claude/shorts/out7/s{sys.argv[1]}_{t:05.1f}.jpg', cv2.cvtColor(V.frame(t), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 80])
    else:
        print(render(V, '/home/claude/shorts/out7'))
