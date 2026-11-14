"""NEON style v3: synthwave city at night, kinetic slam text, police flashes, beat-synced. Original visuals only."""
import sys, os, math, subprocess, functools
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
import audio
from audio import SR, lowpass, reverb

W, H, FPS = 1080, 1920, 30
BOLD = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
LIME = (170, 255, 60); YEL = (255, 222, 40); PINK = (255, 70, 160); CYAN = (60, 230, 255); WHITE = (255, 255, 255); RED = (255, 50, 60)
HORIZON = 1180
rng = np.random.default_rng(7)

def clamp(x, a=0., b=1.): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3

# ---------- static layers ----------
def sky_layer():
    y = np.linspace(0, 1, HORIZON, dtype=np.float32)[:, None]
    c = np.array([[18, 6, 40], [70, 14, 90], [210, 50, 120], [255, 140, 70]], np.float32)
    stops = [0, 0.45, 0.8, 1.0]
    out = np.zeros((HORIZON, 3), np.float32)
    for i in range(3):
        m = (y[:, 0] >= stops[i]) & (y[:, 0] <= stops[i + 1])
        k = ((y[m, 0] - stops[i]) / (stops[i + 1] - stops[i]))[:, None]
        out[m] = c[i] * (1 - k) + c[i + 1] * k
    sky = np.repeat(out[:, None, :], W, axis=1)
    # stars
    for _ in range(140):
        x, yy = rng.integers(0, W), rng.integers(0, 600)
        sky[yy, x] = 255
    # sun
    cx, cy, r = 540, 1010, 330
    Y, X = np.mgrid[0:HORIZON, 0:W].astype(np.float32)
    d = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    m = d < r
    g = np.clip((Y - (cy - r)) / (2 * r), 0, 1)[..., None]
    sun = np.array([255, 230, 110], np.float32) * (1 - g) + np.array([255, 60, 140], np.float32) * g
    stripes = np.zeros_like(m)
    for i in range(7):
        y0 = cy - 20 + i * 34; stripes |= (Y > y0) & (Y < y0 + 4 + i * 3)
    mm = m & ~stripes
    sky[mm] = sun[mm]
    sky += (np.exp(-((d - r).clip(0)) ** 2 / (2 * 120 ** 2)) * (d >= r))[..., None] * np.array([255, 90, 150]) * 0.35
    return np.clip(sky, 0, 255).astype(np.uint8)

def skyline_layer(width, seed, base_col, hmin, hmax, win_p):
    r = np.random.default_rng(seed)
    lay = np.zeros((HORIZON, width, 4), np.uint8)
    x = 0
    while x < width:
        bw = int(r.integers(50, 130)); bh = int(r.integers(hmin, hmax))
        x1 = min(width, x + bw); y0 = HORIZON - bh
        lay[y0:HORIZON, x:x1, :3] = base_col; lay[y0:HORIZON, x:x1, 3] = 255
        if r.random() < 0.3:  # antenna
            lay[y0 - 40:y0, x + bw // 2 - 2:x + bw // 2 + 2] = (*base_col, 255)
        for wy in range(y0 + 14, HORIZON - 10, 22):
            for wx in range(x + 8, x1 - 10, 16):
                if r.random() < win_p:
                    col = (255, 210, 120) if r.random() < 0.7 else (120, 230, 255)
                    lay[wy:wy + 8, wx:wx + 7, :3] = col
        x = x1 + int(r.integers(0, 10))
    return lay

def palm_sprite(h, flip=False):
    S = int(h * 1.1)
    im = np.zeros((S, S, 4), np.uint8)
    col = (14, 4, 22, 255)
    x0, y0 = S // 2, S - 1
    pts = [(x0 + (k / 20) ** 2 * h * 0.22, y0 - k / 20 * h * 0.92) for k in range(21)]
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        cv2.line(im, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), col, max(4, int(h * 0.035 * (1 - i / 25))), cv2.LINE_AA)
    tx, ty = pts[-1]
    for ang in [-170, -140, -110, -70, -40, -10, 15, -195]:
        a = math.radians(ang); prev = None
        for k in range(16):
            u = k / 15; L = h * 0.45 * u
            p = (tx + math.cos(a) * L, ty + math.sin(a) * L + u * u * h * 0.14)
            if prev: cv2.line(im, (int(prev[0]), int(prev[1])), (int(p[0]), int(p[1])), col, max(3, int(h * 0.03 * (1 - abs(0.5 - u) * 1.5))), cv2.LINE_AA)
            prev = p
    return im[:, ::-1].copy() if flip else im

def blit(img, spr, x, y, a=1.0):
    h, w = spr.shape[:2]; x = int(round(x)); y = int(round(y))
    xa, ya, xb, yb = max(0, x), max(0, y), min(img.shape[1], x + w), min(img.shape[0], y + h)
    if xa >= xb or ya >= yb or a <= 0.01: return
    s = spr[ya - y:yb - y, xa - x:xb - x].astype(np.float32)
    al = s[..., 3:4] / 255 * a
    d = img[ya:yb, xa:xb].astype(np.float32)
    img[ya:yb, xa:xb] = (d * (1 - al) + s[..., :3] * al).astype(np.uint8)

def add_glow(img, cx, cy, R, col, k):
    R = int(R); x0, y0 = int(cx) - R, int(cy) - R
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + 2 * R), min(H, y0 + 2 * R)
    if xa >= xb or ya >= yb: return
    Y, X = np.mgrid[ya:yb, xa:xb].astype(np.float32)
    g = np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * (R / 2.5) ** 2))
    sub = img[ya:yb, xa:xb].astype(np.float32) + g[..., None] * np.array(col, np.float32) * k
    img[ya:yb, xa:xb] = np.clip(sub, 0, 255).astype(np.uint8)

class City:
    def __init__(self):
        self.sky = sky_layer()
        self.far = skyline_layer(W * 3, 1, (40, 14, 60), 120, 330, 0.18)
        self.near = skyline_layer(W * 3, 2, (22, 6, 34), 200, 560, 0.28)
        self.palmL = palm_sprite(1150); self.palmR = palm_sprite(950, True)

    def draw(self, t, zoom=1.0, police=0.0):
        img = np.zeros((H, W, 3), np.uint8)
        img[:HORIZON] = self.sky
        for lay, speed in ((self.far, 18), (self.near, 46)):
            off = int(t * speed) % (lay.shape[1] - W)
            blit(img, lay[:, off:off + W], 0, 0)
        # road / synth grid
        img[HORIZON:] = (20, 6, 34)
        for i in range(26):
            z = ((i / 26) + t * 0.55) % 1.0
            yy = int(HORIZON + (H - HORIZON) * z ** 2.2)
            cv2.line(img, (0, yy), (W, yy), (255, 60, 170), 2 + int(3 * z), cv2.LINE_AA)
        for k in range(-12, 13):
            cv2.line(img, (540 + k * 14, HORIZON), (540 + k * 220, H), (255, 60, 170), 2, cv2.LINE_AA)
        # light trails
        for j in range(5):
            ph = (t * 0.9 + j * 0.21) % 1.0
            y = int(HORIZON + 20 + j * 9 + ph * 40)
            x = int(-300 + ph * (W + 600)) if j % 2 == 0 else int(W + 300 - ph * (W + 600))
            col = (255, 240, 200) if j % 2 == 0 else (255, 40, 60)
            cv2.line(img, (x - 160, y), (x, y), col, 4, cv2.LINE_AA)
            add_glow(img, x, y, 60, col, 0.35)
        blit(img, self.palmL, -520, H - self.palmL.shape[0] + 90)
        blit(img, self.palmR, W - self.palmR.shape[1] + 440, H - self.palmR.shape[0] + 60)
        if police > 0:
            blue = (int(t * 8) % 2 == 0)
            ov = np.zeros_like(img, np.float32)
            Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
            edge = np.exp(-(X if blue else (W - X)) / 260)[..., None]
            ov += edge * (np.array([40, 80, 255]) if blue else np.array([255, 30, 40]))
            img = np.clip(img + ov * 0.8 * police, 0, 255).astype(np.uint8)
        if zoom > 1.001:
            M = np.float32([[zoom, 0, -(zoom - 1) * W / 2], [0, zoom, -(zoom - 1) * H * 0.55]])
            img = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        return img

# ---------- kinetic text ----------
@functools.lru_cache(None)
def slam_sprite(text, size, col, stroke=12, maxw=1000):
    f = ImageFont.truetype(BOLD, size)
    words = text.split(' '); lines = ['']
    for w in words:
        test = (lines[-1] + ' ' + w).strip()
        if f.getlength(test) > maxw and lines[-1]: lines.append(w)
        else: lines[-1] = test
    lh = int(size * 1.18)
    w = int(max(f.getlength(l) for l in lines)) + 2 * stroke + 20
    h = lh * len(lines) + 2 * stroke + 30
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        lw = f.getlength(l)
        d.text(((w - lw) / 2, stroke + i * lh - size * 0.1), l, font=f, fill=col + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return np.array(im)

def slam(img, text, t, t0, t1, y, size=110, col=WHITE, from_scale=1.8):
    if t < t0 or t > t1: return
    spr = slam_sprite(text, size, col)
    k = eo(prog(t, t0, t0 + 0.14))
    s = from_scale + (1 - from_scale) * k
    out = 1 - prog(t, t1 - 0.08, t1)
    sp = spr if abs(s - 1) < 0.01 else cv2.resize(spr, (max(1, int(spr.shape[1] * s)), max(1, int(spr.shape[0] * s))))
    blit(img, sp, (W - sp.shape[1]) / 2, y - sp.shape[0] / 2, min(1.0, k * 1.5) * out)

def shake_img(img, k, t):
    if k <= 0: return img
    dx = int(k * 26 * math.sin(t * 73)); dy = int(k * 18 * math.cos(t * 59))
    return np.roll(np.roll(img, dx, axis=1), dy, axis=0)

def flash(img, k):
    if k <= 0: return img
    return np.clip(img.astype(np.float32) + 255 * k, 0, 255).astype(np.uint8)

def glitch(img, t, k):
    if k <= 0: return img
    r = np.random.default_rng(int(t * 100))
    o = img.copy()
    for _ in range(int(10 * k)):
        y0 = r.integers(0, H - 60); hh = r.integers(10, 60)
        o[y0:y0 + hh] = np.roll(o[y0:y0 + hh], r.integers(-80, 80), axis=1)
    o[..., 0] = np.roll(o[..., 0], int(12 * k), axis=1)
    return o

# ---------- beat music ----------
def beat_music(dur, bpm=118, seed=3, notes=(45, 45, 48, 43)):
    n = int(dur * SR); out = np.zeros(n); beat = 60 / bpm
    r = np.random.default_rng(seed)
    def add(sig, at):
        s = int(at * SR); e = min(n, s + len(sig))
        if s < n: out[s:e] += sig[:e - s]
    tt = np.arange(int(0.35 * SR)) / SR
    kick = np.sin(2 * np.pi * np.cumsum(55 + 120 * np.exp(-tt * 30)) / SR) * np.exp(-tt * 9) * 0.9
    sn_t = np.arange(int(0.25 * SR)) / SR
    snare = (lowpass(r.standard_normal(len(sn_t)), 6000) * np.exp(-sn_t * 18) * 0.35 + np.sin(2 * np.pi * 190 * sn_t) * np.exp(-sn_t * 25) * 0.3)
    hh_t = np.arange(int(0.05 * SR)) / SR
    hat = np.diff(np.concatenate([[0], r.standard_normal(len(hh_t))])) * np.exp(-hh_t * 80) * 0.08
    nb = int(dur / beat) + 1
    for b in range(nb):
        add(kick, b * beat)
        if b % 2 == 1: add(snare, b * beat)
        add(hat, b * beat + beat / 2)
        root = notes[(b // 8) % len(notes)]
        for k, semi in enumerate((0, 12, 7, 12)):
            f = audio.hz(root + semi + 12)
            L = int(beat / 4 * SR * 0.9); st = np.arange(L) / SR
            saw = 2 * ((st * f) % 1) - 1
            add(lowpass(saw, 1800) * np.exp(-st * 10) * 0.12, b * beat + k * beat / 4)
        f = audio.hz(root); L = int(beat * SR); st = np.arange(L) / SR
        add(np.sin(2 * np.pi * f * st) * (1 - np.exp(-st * 60)) * np.exp(-st * 2) * 0.35, b * beat)
    out = reverb(out, 1.2, 0.15, seed)
    return out

def riser(dur=0.8):
    L = int(dur * SR); t = np.arange(L) / SR
    x = np.random.default_rng(1).standard_normal(L)
    return lowpass(x, 4000) * (t / dur) ** 2 * 0.3

def hit():
    L = int(0.8 * SR); t = np.arange(L) / SR
    return (np.sin(2 * np.pi * np.cumsum(80 * np.exp(-t * 3) + 35) / SR) * np.exp(-t * 4) * 0.8 +
            lowpass(np.random.default_rng(2).standard_normal(L), 2500) * np.exp(-t * 10) * 0.4)

def siren(dur=1.6):
    L = int(dur * SR); t = np.arange(L) / SR
    f = 700 + 250 * np.sign(np.sin(2 * np.pi * 2.5 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.12 * np.minimum(1, t * 5) * np.minimum(1, (dur - t) * 5)

def mix_track(dur, hits, risers=(), sirens=(), bpm=118):
    m = beat_music(dur, bpm)
    for at, sig in [(a, hit()) for a in hits] + [(a - 0.8, riser()) for a in risers] + [(a, siren()) for a in sirens]:
        s = int(max(0, at) * SR); e = min(len(m), s + len(sig)); m[s:e] += sig[:e - s]
    m = np.tanh(m * 1.2); m *= 0.8 / (np.abs(m).max() + 1e-9)
    nf = int(0.3 * SR); m[-nf:] *= np.linspace(1, 0.4, nf)
    return m

# ---------- sample: GTA 6 in 5 days ----------
BPM = 118; B = 60 / BPM

class Sample:
    name = 'gta6_neon_sample_5_days'; dur = 22.0
    hits = [0.0, 2.0, 2.6, 5.1, 9.2, 13.3, 17.4]
    risers = [2.0, 5.1, 9.2, 13.3, 17.4]
    sirens = [5.1]

    def __init__(self): self.city = City()

    def frame(self, t):
        police = 1.0 if 5.1 <= t < 7.0 else 0.0
        zoom = 1.0 + 0.06 * eo(prog(t % 4.1, 0, 4.1))
        img = self.city.draw(t, zoom, police)
        # 0-2: hook
        slam(img, 'GTA 6', t, 0.0, 2.0, 680, 250, YEL)
        if t < 2.0:
            n = 7 - int(min(2, t / 0.45))
            slam(img, f'{n} DAYS LEFT' if n != 5 else '5 DAYS LEFT', t, 0.05, 2.0, 960, 110, WHITE, 1.2)
        # 2-5: date
        slam(img, 'ROCKSTAR CONFIRMED IT:', t, 2.0, 5.0, 660, 66, WHITE)
        slam(img, 'NOVEMBER 19', t, 2.6, 5.0, 860, 130, LIME)
        # 5-9: platforms
        slam(img, '#1', t, 5.1, 9.1, 640, 130, YEL)
        slam(img, 'PS5 + XBOX SERIES X|S', t, 5.3, 9.1, 830, 70, WHITE)
        slam(img, 'PC? NOT YET.', t, 6.8, 9.1, 1000, 96, RED)
        # 9-13: map
        slam(img, '#2', t, 9.2, 13.2, 640, 130, YEL)
        slam(img, 'THE STATE OF LEONIDA', t, 9.4, 13.2, 830, 76, WHITE)
        slam(img, 'HOME OF VICE CITY', t, 10.6, 13.2, 1000, 90, PINK)
        # 13-17: leads
        slam(img, '#3', t, 13.3, 17.3, 640, 130, YEL)
        slam(img, 'TWO PLAYABLE LEADS', t, 13.5, 17.3, 830, 80, WHITE)
        slam(img, 'JASON & LUCIA', t, 14.7, 17.3, 1000, 112, CYAN)
        # 17-22: debate
        slam(img, 'DAY ONE...', t, 17.4, 22.0, 640, 140, WHITE)
        slam(img, 'OR WAIT FOR REVIEWS?', t, 18.2, 22.0, 820, 78, LIME)
        slam(img, 'COMMENT BELOW', t, 19.4, 22.0, 980, 70, YEL)
        if t > 19.4:
            slam(img, 'Fan channel. Not affiliated with Rockstar Games.', t, 19.4, 22.0, 1560, 30, (210, 210, 220), 1.0)
        slam(img, '@LeonidaUnlocked89', t, 0, 99, 1480, 34, (230, 230, 240), 1.0)
        # fx
        sk = max([1 - prog(t, h, h + 0.35) for h in self.hits if h <= t] + [0])
        img = shake_img(img, sk * 0.8, t)
        img = flash(img, max([0.55 * (1 - prog(t, h, h + 0.12)) for h in self.hits if h <= t] + [0]))
        img = glitch(img, t, max([1 - prog(t, h - 0.15, h + 0.1) for h in self.hits[1:] if h - 0.15 <= t < h + 0.1] + [0]))
        return img

def render(V, outdir):
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.join(outdir, V.name + '.v.tmp.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for i in range(int(V.dur * FPS)): p.stdin.write(V.frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    wav = os.path.join(outdir, V.name + '.wav')
    audio.write_wav(wav, mix_track(V.dur, V.hits, V.risers, V.sirens))
    out = os.path.join(outdir, V.name + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
                    '-b:a', '192k', '-shortest', '-movflags', '+faststart', out + '.part.mp4'], check=True)
    os.replace(out + '.part.mp4', out); os.remove(tmp); os.remove(wav)
    return out

if __name__ == '__main__':
    V = Sample()
    if len(sys.argv) > 1:
        for t in map(float, sys.argv[1:]):
            cv2.imwrite(f'/home/claude/shorts/out5/s_{t:05.1f}.jpg', cv2.cvtColor(V.frame(t), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 80])
    else:
        print(render(V, '/home/claude/shorts/out5'))
