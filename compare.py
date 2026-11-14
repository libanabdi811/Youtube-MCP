"""Split-screen OLD vs NEW comparison Short from the user's own gameplay clips.

usage: python3 compare.py OLD.mp4 NEW.mp4 OUT.mp4 "" [OLD_LABEL] [NEW_LABEL] [SECONDS] ["PROMPT 1|PROMPT 2"]
(set CMP_TOP=260 for a hook banner on top)
- OLD on top, NEW below, 1080x1920, bold year labels, hook banner, fan disclaimer at the end.
- Audio: the NEW clip's game audio (falls back to OLD, then silence).
"""
import sys, os, subprocess, json, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
import os as _os
TOP = int(_os.environ.get('CMP_TOP', '0'))   # 0 = no banner (example style)
GAP = 10
HALF = (1920 - TOP - GAP) // 2
Y1, Y2 = TOP, TOP + HALF + GAP
BOLD = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
LIME = (170, 255, 60); YEL = (255, 222, 40); GOLD = (255, 196, 61)

def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type',
                          '-of', 'json', path], capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    return float(j['format']['duration']), any(s['codec_type'] == 'audio' for s in j['streams'])

def stroke_text(d, xy, text, font, fill, sw=8):
    d.text(xy, text, font=font, fill=fill, stroke_width=sw, stroke_fill=(0, 0, 0))

def overlay_png(path, hook, old_label, new_label, old_tag='GTA V', new_tag='GTA VI', prompts=None):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if TOP:
        d.rectangle((0, 0, W, TOP), fill=(8, 8, 10, 255))
        parts = [p.strip() for p in hook.split('/')]
        f = ImageFont.truetype(BOLD, 64); y = 50 if len(parts) > 1 else 95
        for p in parts:
            hl = p.startswith('*') and p.endswith('*'); p = p.strip('*'); w = d.textlength(p, font=f)
            stroke_text(d, ((W - w) / 2, y), p, f, GOLD if hl else (255, 255, 255), 4); y += 82
    d.rectangle((0, Y1 + HALF, W, Y2), fill=(245, 245, 245, 255))
    fl = ImageFont.truetype(BOLD, 130); ft = ImageFont.truetype(BOLD, 64)
    for lab, tag, yy, col in ((old_label, old_tag, Y1 + 60, LIME), (new_label, new_tag, Y2 + 30, YEL)):
        w = d.textlength(lab, font=fl)
        stroke_text(d, (W - w - 50, yy), lab, fl, col, 10)
        stroke_text(d, (50, yy + 20), tag, ft, (255, 255, 255), 7)   # plain text tag, no game logos
    if prompts:   # e.g. "SLIM JIM|SMASH WINDOW": action labels on the NEW half
        fp = ImageFont.truetype(BOLD, 46)
        for i, p in enumerate(prompts.split('|')):
            y = Y2 + HALF - 260 + i * 70
            d.ellipse((300, y, 350, y + 50), outline=(255, 255, 255), width=5)
            stroke_text(d, (370, y - 2), p.upper(), fp, (255, 255, 255), 5)
    im.save(path)

def outro_png(path):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(BOLD, 52); f2 = ImageFont.truetype(BOLD, 30)
    q = 'Which one looks better?'
    w = d.textlength(q, font=f)
    d.rounded_rectangle(((W - w) / 2 - 30, 1440, (W + w) / 2 + 30, 1530), 24, fill=(0, 0, 0, 200))
    stroke_text(d, ((W - w) / 2, 1450), q, f, (255, 255, 255), 3)
    t = 'Fan-made. Not affiliated with Rockstar Games.'
    w = d.textlength(t, font=f2)
    stroke_text(d, ((W - w) / 2, 1560), t, f2, (200, 200, 200), 2)
    im.save(path)

def main(old, new, out, hook='', old_label='2013', new_label='2026', seconds=None, prompts=None):
    d_old, a_old = probe(old); d_new, a_new = probe(new)
    dur = min(d_old, d_new, 25.0)
    if seconds: dur = min(dur, float(seconds))
    tmp = tempfile.mkdtemp()
    ov = os.path.join(tmp, 'ov.png'); outro = os.path.join(tmp, 'outro.png')
    overlay_png(ov, hook, old_label, new_label, prompts=prompts); outro_png(outro)
    cs = f'scale={W}:{HALF}:force_original_aspect_ratio=increase,crop={W}:{HALF},setsar=1,fps=30'
    fc = (f'color=c=black:s={W}x{H}:d={dur}:r=30[bg];'
          f'[0:v]trim=0:{dur},setpts=PTS-STARTPTS,{cs}[a];'
          f'[1:v]trim=0:{dur},setpts=PTS-STARTPTS,{cs}[b];'
          f'[bg][a]overlay=0:{Y1}[t1];[t1][b]overlay=0:{Y2}[t2];'
          f'[t2][2:v]overlay=0:0[t3];'
          f"[t3][3:v]overlay=0:0:enable='gte(t,{max(dur - 4, 0):.2f})',format=yuv420p[v]")
    cmd = ['ffmpeg', '-y', '-v', 'error', '-i', old, '-i', new, '-loop', '1', '-i', ov, '-loop', '1', '-i', outro]
    if a_new: amap = ['-map', '1:a']
    elif a_old: amap = ['-map', '0:a']
    else:
        cmd += ['-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=stereo']; amap = ['-map', '4:a']
    part = out + '.part.mp4'
    cmd += ['-filter_complex', fc, '-map', '[v]'] + amap + ['-t', f'{dur:.2f}', '-c:v', 'libx264', '-preset', 'veryfast',
            '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', part]
    subprocess.run(cmd, check=True)
    os.replace(part, out)
    print('done', out, f'{dur:.1f}s')

if __name__ == '__main__':
    a = sys.argv[1:]
    main(*a)
