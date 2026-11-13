import numpy as np, cv2, math, functools, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
GROUND = 1250
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
POPB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
POPM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'

WHITE = (236, 236, 238)
DIM = (118, 118, 124)
HAIR = (150, 126, 110)
RED = (232, 72, 85)
GOLD = (255, 196, 61)
BLUE = (110, 170, 255)
INK = (18, 18, 22)

# ---------------- timing helpers ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def sm(x): x = clamp(x); return x * x * (3 - 2 * x)
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def ei(x): x = clamp(x); return x ** 3
def back(x):
    x = clamp(x); c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def lerp(a, b, x): return a + (b - a) * x
def win(t, a, b, f=0.25): return sm(prog(t, a, a + f)) * (1 - sm(prog(t, b, b + f)))

def kf(t, keys):
    """smooth keyframes [(t,v),...]"""
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            x = sm(prog(t, t0, t1))
            if isinstance(v0, tuple): return tuple(lerp(a, b, x) for a, b in zip(v0, v1))
            return lerp(v0, v1, x)
    return keys[-1][1]

def step(t, keys):
    v = keys[0][1]
    for tt, vv in keys:
        if t >= tt: v = vv
    return v

def walkstate(t, keys):
    x = kf(t, keys)
    dx = abs(kf(t + 0.04, keys) - kf(t - 0.04, keys))
    amp = clamp(dx / 6.0)
    return x, (x * 0.05, amp)

def mixc(a, b, x): return tuple(int(lerp(p, q, x)) for p, q in zip(a, b))

# ---------------- primitives (sub-pixel AA) ----------------
SH = 4; M = 16
def P(p): return (int(round(p[0] * M)), int(round(p[1] * M)))
def line(img, a, b, col, th): cv2.line(img, P(a), P(b), col, max(1, int(th)), cv2.LINE_AA, SH)
def circle(img, c, r, col, th=-1):
    cv2.circle(img, P(c), max(1, int(round(r * M))), col, th if th < 0 else max(1, int(th)), cv2.LINE_AA, SH)
def poly(img, pts, col):
    cv2.fillPoly(img, [np.array([P(p) for p in pts], np.int32)], col, cv2.LINE_AA, SH)
def ellipse(img, c, ax, ang, a0, a1, col, th):
    cv2.ellipse(img, P(c), (max(1, int(ax[0] * M)), max(1, int(ax[1] * M))), ang, a0, a1, col, th, cv2.LINE_AA, SH)

@functools.lru_cache(None)
def gsprite(R):
    yy, xx = np.mgrid[-R:R, -R:R].astype(np.float32)
    return np.exp(-(xx ** 2 + yy ** 2) / (2 * (R / 2.6) ** 2)).astype(np.float32)

def glow(img, c, R, color, k):
    if k <= 0.003: return
    R = int(R); g = gsprite(R)
    x0, y0 = int(c[0]) - R, int(c[1]) - R
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + 2 * R), min(H, y0 + 2 * R)
    if xa >= xb or ya >= yb: return
    sub = img[ya:yb, xa:xb].astype(np.float32)
    sub += g[ya - y0:yb - y0, xa - x0:xb - x0, None] * (np.array(color, np.float32) * k)
    img[ya:yb, xa:xb] = np.clip(sub, 0, 255).astype(np.uint8)

def blit(img, spr, x, y, a=1.0):
    if a <= 0.01: return
    h, w = spr.shape[:2]; x = int(round(x)); y = int(round(y))
    xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if xa >= xb or ya >= yb: return
    s = spr[ya - y:yb - y, xa - x:xb - x].astype(np.float32)
    al = s[..., 3:4] / 255.0 * a
    d = img[ya:yb, xa:xb].astype(np.float32)
    img[ya:yb, xa:xb] = (d * (1 - al) + s[..., :3] * al).astype(np.uint8)

def scaled(spr, k):
    if abs(k - 1) < 0.01: return spr
    h, w = spr.shape[:2]
    return cv2.resize(spr, (max(1, int(w * k)), max(1, int(h * k))), interpolation=cv2.INTER_LINEAR)

# ---------------- text ----------------
@functools.lru_cache(None)
def font(path, size): return ImageFont.truetype(path, size)

def spaced_w(txt, f, sp): return sum(f.getlength(c) for c in txt) + sp * max(0, len(txt) - 1)
def draw_spaced(d, xy, txt, f, sp, fill):
    x, y = xy
    for c in txt:
        d.text((x, y), c, font=f, fill=fill); x += f.getlength(c) + sp

@functools.lru_cache(None)
def bubble_sprite(text, kind='say', tail='c', size=42):
    S = 2
    f = font(MONO, size * S); sp = 4 * S
    lines = text.split('\n'); lh = int(size * 1.28 * S)
    tw = max(spaced_w(l, f, sp) for l in lines); th = lh * len(lines)
    padx, pady = 34 * S, 22 * S
    bw, bh = int(tw + 2 * padx), int(th + 2 * pady)
    m = 12 * S
    cw, ch = bw + 2 * m, bh + m + 70 * S
    im = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fx = {'l': 0.24, 'c': 0.5, 'r': 0.76}[tail]
    tipx = m + bw * fx
    ol = (18, 18, 22, 255); fill = (246, 246, 248, 255)
    if kind == 'say':
        tip = (tipx + (-16 if tail == 'r' else 16 if tail == 'l' else 0) * S, m + bh + 44 * S)
        d.polygon([(tipx - 22 * S, m + bh - 30 * S), (tipx + 22 * S, m + bh - 30 * S), tip], fill=ol)
        d.rounded_rectangle((m - 5 * S, m - 5 * S, m + bw + 5 * S, m + bh + 5 * S), radius=min(34 * S, bh // 2 + 5 * S), fill=ol)
        d.rounded_rectangle((m, m, m + bw, m + bh), radius=min(30 * S, bh // 2), fill=fill)
        d.polygon([(tipx - 15 * S, m + bh - 24 * S), (tipx + 15 * S, m + bh - 24 * S),
                   (tip[0] + (tipx - tip[0]) * 0.25, tip[1] - 14 * S)], fill=fill)
        tipy = tip[1]
    else:
        d.rounded_rectangle((m - 5 * S, m - 5 * S, m + bw + 5 * S, m + bh + 5 * S), radius=bh // 2 + 5 * S, fill=ol)
        d.rounded_rectangle((m, m, m + bw, m + bh), radius=bh // 2, fill=fill)
        for (oy, r) in [(20, 13), (46, 8)]:
            cy = m + bh + oy * S
            d.ellipse((tipx - (r + 4) * S, cy - (r + 4) * S, tipx + (r + 4) * S, cy + (r + 4) * S), fill=ol)
            d.ellipse((tipx - r * S, cy - r * S, tipx + r * S, cy + r * S), fill=fill)
        tipy = m + bh + 56 * S
    y = m + pady - int(size * 0.12 * S)
    for l in lines:
        draw_spaced(d, (m + (bw - spaced_w(l, f, sp)) / 2, y), l, f, sp, INK + (255,)); y += lh
    im = im.resize((cw // S, ch // S), Image.LANCZOS)
    return np.array(im), (tipx / S, tipy / S)

def draw_bubble(img, text, tip, t, t0, t1, kind='say', tail=None):
    if t < t0 or t > t1 + 0.25: return
    if tail is None: tail = 'l' if tip[0] < 540 else 'r'
    spr, (tx, ty) = bubble_sprite(text, kind, tail)
    k = 0.3 + 0.7 * back(prog(t, t0, t0 + 0.3))
    a = sm(prog(t, t0, t0 + 0.12)) * (1 - sm(prog(t, t1, t1 + 0.22)))
    s2 = scaled(spr, k)
    x = tip[0] - tx * k; y = tip[1] - ty * k
    w = s2.shape[1]
    x = min(max(x, 24), W - 24 - w)
    blit(img, s2, x, y, a)

def parse_hl(text):
    toks = []; hl = False
    for part in text.split('*'):
        for w in part.split(' '):
            if w: toks.append((w, hl))
        hl = not hl
    return toks

@functools.lru_cache(None)
def rich_sprite(text, path=POPB, size=60, color=WHITE, hl=GOLD, maxw=980, shadow=True, lead=1.22):
    f = font(path, size)
    toks = parse_hl(text); spw = f.getlength(' ')
    lines = [[]]; cur = 0
    for w, h in toks:
        if w == '/':
            lines.append([]); cur = 0; continue
        lw = f.getlength(w)
        if lines[-1] and cur + spw + lw > maxw:
            lines.append([]); cur = 0
        lines[-1].append((w, h)); cur += (spw if len(lines[-1]) > 1 else 0) + lw
    lh = int(size * lead)
    widths = [sum(f.getlength(w) for w, _ in L) + spw * max(0, len(L) - 1) for L in lines]
    cw = int(max(widths)) + 60; ch = lh * len(lines) + 60
    txt = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    y = 30 - int(size * 0.08)
    for L, lw in zip(lines, widths):
        x = (cw - lw) / 2
        for w, h in L:
            d.text((x, y), w, font=f, fill=(hl if h else color) + (255,)); x += f.getlength(w) + spw
        y += lh
    if shadow:
        a = np.array(txt)[..., 3]
        sh = Image.fromarray(a).filter(ImageFilter.GaussianBlur(9))
        sha = (np.array(sh).astype(np.float32) * 0.95).astype(np.uint8)
        base = np.zeros((ch, cw, 4), np.uint8); base[..., 3] = sha
        out = Image.alpha_composite(Image.fromarray(base), txt)
        return np.array(out)
    return np.array(txt)

def caption(img, text, t, t0, t1, y=1430, size=60, color=WHITE, path=POPB, hl=GOLD):
    a = win(t, t0, t1, 0.3)
    if a <= 0: return
    spr = rich_sprite(text, path, size, color, hl)
    dy = (1 - eo(prog(t, t0, t0 + 0.4))) * 26
    blit(img, spr, (W - spr.shape[1]) / 2, y - 30 + dy, a)

@functools.lru_cache(None)
def label_sprite(text, color, size=40):
    f = font(MONO, size); sp = 7
    w = int(spaced_w(text, f, sp)) + 40; h = int(size * 1.6)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    draw_spaced(d, (20, 6), text, f, sp, color + (255,))
    return np.array(im)

def label(img, text, t, t0, t1, y=250, color=WHITE, size=40, x=None):
    if t < t0 or t > t1 + 0.3: return
    n = int(math.ceil(len(text) * prog(t, t0, t0 + 0.04 * len(text) + 0.05)))
    if n <= 0: return
    spr = label_sprite(text[:n], color, size)
    full = label_sprite(text, color, size)
    a = 1 - sm(prog(t, t1, t1 + 0.3))
    xx = (W - full.shape[1]) / 2 if x is None else x
    blit(img, spr, xx, y, a)

# ---------------- characters ----------------
def limb(img, start, a1, a2, L1, L2, face, col, th):
    r1 = math.radians(a1)
    k = (start[0] + face * L1 * math.sin(r1), start[1] + L1 * math.cos(r1))
    r2 = math.radians(a1 + a2)
    e = (k[0] + face * L2 * math.sin(r2), k[1] + L2 * math.cos(r2))
    line(img, start, k, col, th); line(img, k, e, col, th)
    circle(img, k, th / 2, col); circle(img, e, th / 2, col)
    return e

def person(img, x, y=GROUND, s=1.0, face=1, col=WHITE, mood='flat', hair=False, dress=False,
           kid=False, lean=0, front=(8, 12), rear=(-6, 10), legs=((0, 0), (0, 0)), sitk=0.0,
           walk=None, headdown=0, nod=0, eyes_closed=False, bob=0.0, headturn=None):
    """Returns dict of key points (hands, head)."""
    th = 30 * s; tth = 40 * s
    hr = 50 * s * (1.42 if kid else 1.0)
    rearcol = mixc(col, (20, 20, 24), 0.28)
    (fa1, fa2), (ra1, ra2) = front, rear
    (l1a, l1b), (l2a, l2b) = legs
    yb = 0
    if walk is not None:
        ph, amp = walk
        l1a = lerp(l1a, 26 * math.sin(ph), amp); l1b = lerp(l1b, -34 * max(0, math.sin(ph + 1.9)), amp)
        l2a = lerp(l2a, -26 * math.sin(ph), amp); l2b = lerp(l2b, -34 * max(0, -math.sin(ph + 1.9)), amp)
        fa1 = lerp(fa1, -20 * math.sin(ph), amp); ra1 = lerp(ra1, 20 * math.sin(ph), amp)
        yb = -6 * amp * abs(math.cos(ph))
    if sitk > 0:
        l1a = lerp(l1a, 88, sitk); l1b = lerp(l1b, -88, sitk)
        l2a = lerp(l2a, 84, sitk); l2b = lerp(l2b, -84, sitk)
    hip = (x, y - lerp(250, 125, sitk) * s + yb + bob)
    rl = math.radians(lean)
    neck = (hip[0] + face * math.sin(rl) * 190 * s, hip[1] - math.cos(rl) * 190 * s)
    sho = (lerp(neck[0], hip[0], 0.1), lerp(neck[1], hip[1], 0.1))
    # rear limbs
    limb(img, hip, l2a, l2b, 128 * s, 124 * s, face, rearcol, th)
    rh = limb(img, sho, ra1 + lean, ra2, 112 * s, 104 * s, face, rearcol, th)
    if dress and sitk < 0.5:
        wy = lerp(neck[1], hip[1], 0.72)
        poly(img, [(hip[0] - 20 * s, wy), (hip[0] + 20 * s, wy), (hip[0] + 62 * s, hip[1] + 112 * s),
                   (hip[0] - 62 * s, hip[1] + 112 * s)], col)
    line(img, hip, neck, col, tth); circle(img, hip, tth / 2, col); circle(img, neck, tth / 2, col)
    limb(img, hip, l1a, l1b, 128 * s, 124 * s, face, col, th)
    fh = limb(img, sho, fa1 + lean, fa2, 112 * s, 104 * s, face, col, th)
    ha = math.radians(lean + headdown)
    c = (neck[0] + face * math.sin(ha) * (hr + 14 * s), neck[1] - math.cos(ha) * (hr + 14 * s) + nod)
    if hair:
        ellipse(img, (c[0] - face * 0.22 * hr, c[1] + 0.12 * hr), (1.06 * hr, 1.12 * hr), 0, 0, 360, HAIR, -1)
        circle(img, (c[0] - face * 0.86 * hr, c[1] - 0.5 * hr), 0.4 * hr, HAIR)
    circle(img, c, hr, col)
    if hair:
        ellipse(img, (c[0] - face * 0.08 * hr, c[1] - 0.38 * hr), (1.0 * hr, 0.6 * hr), 0, 180, 360, HAIR, -1)
    face_feat(img, c, hr, face if headturn is None else headturn, mood, eyes_closed, headdown)
    return {'head': c, 'hr': hr, 'fh': fh, 'rh': rh, 'neck': neck, 'hip': hip,
            'chest': (lerp(neck[0], hip[0], 0.3), lerp(neck[1], hip[1], 0.3)),
            'top': (c[0], c[1] - hr)}

def face_feat(img, c, r, face, mood, closed, hd):
    ey = c[1] - 0.06 * r + 0.18 * r * clamp(hd / 30)
    e1 = (c[0] + face * 0.16 * r, ey); e2 = (c[0] + face * 0.58 * r, ey)
    th = max(2, r * 0.07)
    if closed or mood == 'closed':
        for e in (e1, e2): line(img, (e[0] - 0.09 * r, e[1] + 0.02 * r), (e[0] + 0.09 * r, e[1] + 0.02 * r), INK, th)
    else:
        for e in (e1, e2): circle(img, e, 0.095 * r, INK)
    mc = (c[0] + face * 0.38 * r, c[1] + 0.42 * r + 0.1 * r * clamp(hd / 30))
    if mood in ('smile', 'happy'):
        ellipse(img, (mc[0], mc[1] - 0.08 * r), (0.2 * r, 0.14 * r), 0, 10, 170, INK, int(th))
    elif mood == 'sad':
        ellipse(img, (mc[0], mc[1] + 0.07 * r), (0.17 * r, 0.1 * r), 0, 200, 340, INK, int(th))
        line(img, (e1[0] - face * 0.13 * r, e1[1] - 0.2 * r), (e1[0] + face * 0.12 * r, e1[1] - 0.3 * r), INK, th * 0.8)
        line(img, (e2[0] - face * 0.12 * r, e2[1] - 0.3 * r), (e2[0] + face * 0.13 * r, e2[1] - 0.2 * r), INK, th * 0.8)
    elif mood == 'angry':
        ellipse(img, mc, (0.13 * r, 0.09 * r), 0, 0, 360, INK, -1)
        line(img, (e1[0] - 0.12 * r * face, e1[1] - 0.26 * r), (e1[0] + 0.12 * r * face, e1[1] - 0.16 * r), INK, th)
        line(img, (e2[0] + 0.12 * r * face, e2[1] - 0.26 * r), (e2[0] - 0.12 * r * face, e2[1] - 0.16 * r), INK, th)
    else:
        line(img, (mc[0] - 0.13 * r, mc[1]), (mc[0] + 0.13 * r, mc[1]), INK, th)

def heart(img, c, size, col=RED, a=1.0):
    if size <= 1: return
    pts = []
    for i in range(48):
        u = i / 48 * 2 * math.pi
        x = 16 * math.sin(u) ** 3
        y = -(13 * math.cos(u) - 5 * math.cos(2 * u) - 2 * math.cos(3 * u) - math.cos(4 * u))
        pts.append((c[0] + x * size / 32, c[1] + y * size / 32))
    glow(img, c, size * 1.6, col, 0.35 * a)
    poly(img, pts, col)

def pop_heart(img, c, t, t0, size=70):
    if t < t0: return
    k = back(prog(t, t0, t0 + 0.4))
    yy = c[1] - 18 * math.sin((t - t0) * 2.2) * clamp(t - t0 - 0.4)
    heart(img, (c[0], yy), size * k)

def phone(img, hand, on=True, face=1):
    x, y = hand
    if on: glow(img, (x, y - 10), 120, BLUE, 0.22)
    poly(img, [(x - 15, y - 34), (x + 15, y - 34), (x + 15, y + 20), (x - 15, y + 20)], (40, 42, 50))
    if on: poly(img, [(x - 11, y - 30), (x + 11, y - 30), (x + 11, y + 16), (x - 11, y + 16)], (150, 195, 255))

# ---------------- backgrounds ----------------
def vgrad(h, c0, c1):
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    return (np.array(c0, np.float32) * (1 - t) + np.array(c1, np.float32) * t)

def make_bg(kind):
    img = np.zeros((H, W, 3), np.float32)
    img[:GROUND] = vgrad(GROUND, (12, 13, 17), (30, 32, 38))[:, None, :]
    img[GROUND:] = vgrad(H - GROUND, (44, 46, 52), (14, 15, 18))[:, None, :]
    img = img.astype(np.uint8)
    lamp_x = 540
    def window(x0, y0, w, h):
        cv2.rectangle(img, (x0, y0), (x0 + w, y0 + h), (52, 66, 88), -1)
        g = vgrad(h, (70, 92, 124), (40, 52, 72)).astype(np.uint8)
        img[y0:y0 + h, x0:x0 + w] = g[:, None, :]
        for i in range(1, 3):
            cv2.line(img, (x0 + w * i // 3, y0), (x0 + w * i // 3, y0 + h), (22, 24, 30), 8)
        cv2.line(img, (x0, y0 + h // 2), (x0 + w, y0 + h // 2), (22, 24, 30), 8)
        cv2.rectangle(img, (x0, y0), (x0 + w, y0 + h), (22, 24, 30), 10)
    if kind in ('kitchen', 'living'):
        window(40 if kind == 'kitchen' else 800, 640, 240, 340)
    if kind == 'kitchen':
        cv2.rectangle(img, (790, 1060), (1080, 1250), (46, 48, 55), -1)
        cv2.rectangle(img, (775, 1046), (1080, 1066), (78, 80, 88), -1)
        for i in range(3): cv2.rectangle(img, (812 + i * 92, 1090), (884 + i * 92, 1220), (38, 40, 46), 4)
        cv2.rectangle(img, (800, 700), (1080, 880), (40, 42, 48), -1)
        cv2.line(img, (940, 700), (940, 880), (30, 31, 36), 4)
    if kind == 'living':
        sx0, sx1 = 280, 800
        cv2.rectangle(img, (sx0, 985), (sx1, 1112), (58, 60, 68), -1)
        cv2.rectangle(img, (sx0 - 40, 1050), (sx0 + 10, 1185), (66, 68, 76), -1)
        cv2.rectangle(img, (sx1 - 10, 1050), (sx1 + 40, 1185), (66, 68, 76), -1)
        cv2.rectangle(img, (sx0 + 10, 1112), (sx1 - 10, 1185), (72, 74, 82), -1)
        cv2.line(img, (540, 1115), (540, 1182), (58, 60, 68), 4)
        for xx in (sx0 - 20, sx1 + 20): cv2.rectangle(img, (xx - 8, 1185), (xx + 8, 1250), (36, 38, 44), -1)
        cv2.line(img, (110, 1250), (110, 800), (60, 60, 66), 8)
        pts = np.array([[70, 800], [150, 800], [130, 730], [90, 730]], np.int32)
        cv2.fillPoly(img, [pts], (80, 76, 70))
    if kind == 'home':
        cv2.rectangle(img, (40, 760), (250, 1250), (24, 25, 30), -1)
        cv2.rectangle(img, (40, 760), (250, 1250), (70, 72, 80), 12)
        cv2.circle(img, (220, 1020), 8, (90, 92, 100), -1)
        cv2.rectangle(img, (690, 760), (980, 790), (66, 68, 76), -1)  # shelf
        cv2.rectangle(img, (720, 700), (770, 760), (52, 54, 60), -1)
        cv2.rectangle(img, (790, 720), (820, 760), (60, 62, 70), -1)
        # chair (right, facing left)
        cv2.rectangle(img, (735, 1112), (905, 1134), (70, 72, 80), -1)
        cv2.rectangle(img, (885, 940), (905, 1134), (70, 72, 80), -1)
        for xx in (745, 893): cv2.rectangle(img, (xx - 6, 1134), (xx + 6, 1250), (50, 52, 58), -1)
    out = img.astype(np.float32)
    # lamp
    if kind != 'none':
        cv2.line(img, (lamp_x, 0), (lamp_x, 520), (70, 70, 76), 3)
        out = img.astype(np.float32)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        cone = np.clip(1 - np.abs(xx - lamp_x) / (60 + (yy - 540).clip(0) * 0.62), 0, 1) * (yy > 540) * np.exp(-((yy - 540).clip(0)) / 1300)
        pool = np.exp(-(((xx - lamp_x) / 520) ** 2 + ((yy - GROUND - 40) / 110) ** 2))
        out += (cone ** 1.4 * 26 + pool * 22)[..., None] * np.array([1.0, 0.92, 0.75], np.float32)
        out += gsprite_full(lamp_x, 548, 140)[..., None] * np.array([255, 205, 120], np.float32) * 0.5
    # vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.55 * np.clip((((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.48) / (H * 0.62)) ** 2), 0, 1)
    out *= v[..., None]
    img = np.clip(out, 0, 255).astype(np.uint8)
    if kind != 'none':
        pts = np.array([[lamp_x - 70, 548], [lamp_x + 70, 548], [lamp_x + 34, 506], [lamp_x - 34, 506]], np.int32)
        cv2.fillPoly(img, [pts], (34, 34, 38), cv2.LINE_AA)
        cv2.ellipse(img, (lamp_x, 548), (54, 9), 0, 0, 180, (255, 226, 170), -1, cv2.LINE_AA)
    return img

def gsprite_full(cx, cy, R):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * (R / 2.2) ** 2))

# ---------------- effects ----------------
def hook_overlay(img, text, t, end=2.5):
    if t > end + 0.45: return img
    k = 1 - sm(prog(t, end, end + 0.4))
    out = (img.astype(np.float32) * (1 - 0.68 * k)).astype(np.uint8)
    spr = rich_sprite(text, POPB, 84, WHITE, GOLD, 960, True, 1.16)
    s = 1.12 - 0.12 * eo(prog(t, 0, 0.35))
    s2 = scaled(spr, s)
    blit(out, s2, (W - s2.shape[1]) / 2, 330 - (s2.shape[0] - spr.shape[0]) / 2, k)
    return out

def rewind_fx(img, t, a, b):
    k = prog(t, a, b)
    out = img.astype(np.float32)
    g = out.mean(axis=2, keepdims=True)
    out = g * np.array([0.8, 0.9, 1.15], np.float32) * 0.85
    rng = np.random.default_rng(int(t * 30))
    o = out.astype(np.uint8)
    for _ in range(7):
        y0 = rng.integers(0, H - 80); hh = rng.integers(8, 70)
        o[y0:y0 + hh] = np.roll(o[y0:y0 + hh], rng.integers(-60, 60), axis=1)
    o[::4] = (o[::4].astype(np.float32) * 0.7).astype(np.uint8)
    spr = label_sprite('<< REWIND', WHITE, 54)
    blit(o, spr, (W - spr.shape[1]) / 2, 900, 1.0 if int(t * 6) % 2 == 0 else 0.55)
    return o

# ---------------- render ----------------
def render(name, dur, frame_fn, outdir):
    tmp = os.path.join(outdir, name + '.video.tmp.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19',
                          '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    for i in range(n):
        p.stdin.write(frame_fn(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    assert p.returncode == 0
    return tmp
