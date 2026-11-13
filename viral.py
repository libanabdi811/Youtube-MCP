"""Viral format v2: cold open, persistent hook banner, camera punch-ins/shake, twist, ~25 s, loopable end."""
import sys, os, math, subprocess
import numpy as np, cv2, functools
from engine import *
import audio
from videos import phone as _p, PHONE_ARM, SIT, STAND

# ---------- camera ----------
def apply_camera(img, s, cx, cy, shake=0.0, t=0.0):
    if shake > 0:
        cx += shake * 14 * math.sin(t * 61); cy += shake * 10 * math.cos(t * 47)
    if s <= 1.001 and shake <= 0: return img, (0.0, 0.0, 1.0)
    s = max(s, 1.0 + 0.02 * (shake > 0))
    w, h = W / s, H / s
    x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    M = np.float32([[s, 0, -x0 * s], [0, s, -y0 * s]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE), (x0, y0, s)

def cam_pt(p, cam):
    x0, y0, s = cam
    return ((p[0] - x0) * s, (p[1] - y0) * s)

# ---------- persistent hook banner ----------
@functools.lru_cache(None)
def banner_sprite(text):
    spr = rich_sprite(text, POPB, 58, WHITE, GOLD, 940, False, 1.15)
    h, w = spr.shape[:2]
    pad = 26
    bg = np.zeros((h + 2 * pad - 40, w + 2 * pad - 20, 4), np.uint8)
    cv2.rectangle(bg, (0, 0), (bg.shape[1] - 1, bg.shape[0] - 1), (12, 12, 16, 215), -1)
    out = bg.copy()
    ys = (out.shape[0] - h) // 2 + 4; xs = (out.shape[1] - w) // 2
    # alpha-composite text onto pill
    sub = out[max(ys, 0):ys + h, xs:xs + w]
    hh, ww = sub.shape[:2]
    a = spr[:hh, :ww, 3:4] / 255.0
    sub[..., :3] = (sub[..., :3] * (1 - a) + spr[:hh, :ww, :3] * a).astype(np.uint8)
    sub[..., 3:4] = np.maximum(sub[..., 3:4], spr[:hh, :ww, 3:4])
    return out

def banner(img, text, t):
    spr = banner_sprite(text)
    k = 0.85 + 0.15 * back(prog(t, 0, 0.25))
    s2 = scaled(spr, k)
    blit(img, s2, (W - s2.shape[1]) / 2, 210 - (s2.shape[0] - spr.shape[0]) / 2)

# ---------- bedroom ----------
def make_bedroom():
    img = make_bg('none')
    cv2.rectangle(img, (760, 610), (1000, 900), (34, 44, 64), -1)
    cv2.circle(img, (930, 680), 30, (210, 214, 196), -1, cv2.LINE_AA)
    cv2.circle(img, (918, 672), 28, (34, 44, 64), -1, cv2.LINE_AA)
    cv2.rectangle(img, (760, 610), (1000, 900), (20, 22, 28), 10)
    cv2.line(img, (880, 610), (880, 900), (20, 22, 28), 8)
    cv2.rectangle(img, (170, 930), (840, 1010), (60, 52, 50), -1)          # headboard
    cv2.rectangle(img, (150, 1110), (860, 1175), (88, 84, 96), -1)         # mattress
    cv2.rectangle(img, (150, 1175), (860, 1215), (54, 52, 60), -1)
    for xx in (170, 840): cv2.rectangle(img, (xx - 8, 1215), (xx + 8, 1250), (36, 38, 44), -1)
    cv2.rectangle(img, (880, 1090), (1010, 1250), (48, 44, 42), -1)        # nightstand
    cv2.rectangle(img, (880, 1080), (1010, 1096), (70, 64, 60), -1)
    return img

def buzz_phone(img, pos, t, on):
    x, y = pos
    if on:
        glow(img, (x, y), 150, BLUE, 0.35)
        for k in (1, 2):
            r = 30 + k * 18 + 8 * math.sin(t * 30)
            ellipse(img, (x, y), (r, r * 0.6), 0, 200, 340, (150, 195, 255), 3)
            ellipse(img, (x, y), (r, r * 0.6), 0, 20, 160, (150, 195, 255), 3)
    poly(img, [(x - 34, y - 9), (x + 34, y - 9), (x + 34, y + 9), (x - 34, y + 9)], (40, 42, 50))
    if on: poly(img, [(x - 30, y - 6), (x + 30, y - 6), (x + 30, y + 6), (x - 30, y + 6)], (150, 195, 255))

# ---------- generic v2 frame builder ----------
def frame_fn_v2(V, bg):
    def f(t):
        img = bg.copy()
        V.world(img, t)
        s, cx, cy = V.cam(t)
        img, cam = apply_camera(img, s, cx, cy, V.shake(t), t)
        for t0, t1, txt, tip, kind in V.bubbles:
            if t0 - 0.05 <= t <= t1 + 0.3:
                p = cam_pt(tip, cam)
                draw_bubble(img, txt, (p[0], max(p[1], 520)), t, t0, t1, kind)
        V.ui(img, t)
        banner(img, V.banner, t)
        return img
    return f

def build_v2(V, outdir, seed=5):
    os.makedirs(outdir, exist_ok=True)
    vid = render(V.name, V.dur, frame_fn_v2(V, V.make_bg()), outdir)
    ev = list(V.events) + [('pop', b[0]) for b in V.bubbles]
    a = audio.mix(V.dur, V.prog, ev, V.bpm, seed) * 0.708
    wav = os.path.join(outdir, V.name + '.wav'); audio.write_wav(wav, a)
    tmp = os.path.join(outdir, V.name + '.tmp.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', vid, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', tmp], check=True)
    os.replace(tmp, os.path.join(outdir, V.name + '.mp4')); os.remove(vid); os.remove(wav)

# ============ EXAMPLE: "Her phone lit up at 2 AM" ============
class Phone2AM:
    name = 'v2_her_phone_lit_up_at_2am'; dur = 24.0
    banner = 'HER PHONE LIT UP AT 2 AM. / *HE SAW THE NAME.*'
    prog = ['Am', 'F', 'Dm', 'E']; bpm = 72
    WX, HX = 340, 720
    bubbles = [(0.4, 2.2, "H: ARE YOU\nOKAY?", (940, 900), 'say'),
               (2.3, 3.9, "WHO IS 'H'?", (720, SIT), 'think'),
               (4.0, 5.6, "WHO IS H?!", (720, SIT), 'say'),
               (5.7, 7.5, "...SHE'S MY\nTHERAPIST.", (340, SIT), 'say'),
               (7.6, 9.9, "I'VE BEEN STRUGGLING.\nI WAS SCARED\nTO TELL YOU.", (340, SIT), 'say'),
               (10.0, 11.6, "SCARED?\nOF ME?", (720, SIT), 'say'),
               (11.7, 13.7, "I DIDN'T WANT YOU\nTO THINK I'M WEAK.", (340, SIT), 'say'),
               (13.8, 16.0, "YOU'RE NOT WEAK.\nWE FACE THIS\nTOGETHER.", (560, SIT), 'say')]
    events = [('boom', 0.0), ('tick', 0.3), ('tick', 0.6), ('tick', 0.9), ('thud', 4.0), ('whoosh', 5.6),
              ('chime', 16.2), ('whoosh', 16.8)]

    @staticmethod
    def make_bg(): return make_bedroom()

    @staticmethod
    def cam(t):
        return kf(t, [(0.0, (1.35, 800, 1000)), (2.2, (1.25, 760, 950)), (4.0, (1.0, 540, 960)), (4.3, (1.3, 720, 900)),
                      (5.6, (1.3, 720, 900)), (5.9, (1.35, 360, 900)), (9.9, (1.25, 380, 900)), (10.2, (1.0, 540, 960)),
                      (16.4, (1.0, 540, 960)), (17.4, (1.15, 540, 1000)), (24.0, (1.15, 540, 1000))])

    @staticmethod
    def shake(t):
        return 1.0 - prog(t, 4.0, 4.6) if 4.0 <= t < 4.6 else 0.0

    @staticmethod
    def world(img, t):
        hx = kf(t, [(13.6, 720), (14.4, 560)])
        hug = kf(t, [(14.2, 0), (14.8, 1)])
        hold = t >= 1.8
        angry = 3.9 <= t < 9.9
        hm = 'angry' if angry else ('sad' if t < 13.8 else 'smile')
        hm = 'flat' if t < 2.3 else hm
        wm = 'flat' if t < 4.0 else ('sad' if t < 14.0 else 'smile')
        glow(img, (520, 950), 300, GOLD, kf(t, [(13.8, 0), (16.0, 0.4)]))
        person(img, 340, face=1, sitk=1, hair=True, mood=wm, headdown=kf(t, [(5.6, 0), (6.0, 22), (13.6, 22), (14.0, 0)]),
               eyes_closed=t < 3.9, front=(lerp(10, 62, hug), lerp(12, -40, hug)))
        p = person(img, hx, face=-1, sitk=1, mood=hm, lean=kf(t, [(3.9, 0), (4.1, 12), (9.9, 12), (10.3, 0)]),
                   front=PHONE_ARM if (hold and t < 10.0) else (lerp(10, 62, hug), lerp(12, -40, hug)))
        if hold and t < 10.0:
            phone(img, p['fh'])
            buzz_phone(img, (945, 1074), t, False)
        else:
            buzz_phone(img, (945, 1074), t, t < 1.8)
        pop_heart(img, (530, 700), t, 16.2, 75)

    @staticmethod
    def ui(img, t):
        label(img, '2:07 AM', t, 0.0, 3.9, y=440, color=(170, 170, 176))
        caption(img, 'Before you accuse, *ask gently.*', t, 16.6, 30, 1415, 56)
        caption(img, "They might be *afraid to tell you.*", t, 18.2, 30, 1505, 50)
        caption(img, 'Would you have reacted like him?', t, 20.4, 30, 1590, 42, (200, 200, 206), POPM)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        f = frame_fn_v2(Phone2AM, Phone2AM.make_bg())
        for t in [float(x) for x in sys.argv[2:]]:
            cv2.imwrite(f'/home/claude/shorts/out3/s_{t:05.1f}.jpg', cv2.cvtColor(f(t), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 80])
    else:
        build_v2(Phone2AM, '/home/claude/shorts/out3')
        print('done')
