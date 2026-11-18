"""Reaction Short: FACECAM on top, GAMEPLAY below, white caption box across the join (the user's own recordings only).

usage: python3 react.py FACE.mp4 GAME.mp4 OUT.mp4 "CAPTION TEXT" [SECONDS] [FACE_START] [GAME_START] [CAPTION_SECONDS]
- FACE audio (your voice) is mixed over the game audio.
- Caption shows for CAPTION_SECONDS (default 4) like the reference, then the join line stays.
"""
import sys, os, subprocess, json, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FACE_H = 760                      # top part (facecam)
GAME_Y = FACE_H                   # gameplay fills the rest
GAME_H = H - FACE_H
BOLD = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'

def probe(p):
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type', '-of', 'json', p],
                                  capture_output=True, text=True, check=True).stdout)
    return float(j['format']['duration']), any(s['codec_type'] == 'audio' for s in j['streams'])

def caption_png(path, text):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(BOLD, 64)
    words = text.upper().split(); lines = ['']
    for w in words:
        t = (lines[-1] + ' ' + w).strip()
        if d.textlength(t, font=f) > 860 and lines[-1]: lines.append(w)
        else: lines[-1] = t
    lh = 76; bh = lh * len(lines) + 24
    y0 = GAME_Y - bh // 2
    for i, l in enumerate(lines):
        lw = d.textlength(l, font=f)
        y = y0 + 12 + i * lh
        d.rectangle(((W - lw) / 2 - 22, y - 4, (W + lw) / 2 + 22, y + lh - 4), fill=(255, 255, 255, 255))
    for i, l in enumerate(lines):
        lw = d.textlength(l, font=f)
        d.text(((W - lw) / 2, y0 + 12 + i * lh - 6), l, font=f, fill=(10, 10, 12, 255))
    im.save(path)

def main(face, game, out, text, seconds=None, face_start=0, game_start=0, cap_secs=4):
    face_start, game_start, cap_secs = float(face_start), float(game_start), float(cap_secs)
    df, af = probe(face); dg, ag = probe(game)
    dur = min(df - face_start, dg - game_start, 60.0)
    if seconds: dur = min(dur, float(seconds))
    tmp = tempfile.mkdtemp(); cap = os.path.join(tmp, 'cap.png'); caption_png(cap, text)
    fc = (f'color=c=black:s={W}x{H}:d={dur}:r=30[bg];'
          f'[0:v]trim={face_start}:{face_start + dur},setpts=PTS-STARTPTS,scale={W}:{FACE_H}:force_original_aspect_ratio=increase,crop={W}:{FACE_H},setsar=1,fps=30[f];'
          f'[1:v]trim={game_start}:{game_start + dur},setpts=PTS-STARTPTS,scale={W}:{GAME_H}:force_original_aspect_ratio=increase,crop={W}:{GAME_H},setsar=1,fps=30[g];'
          f'[bg][f]overlay=0:0[t1];[t1][g]overlay=0:{GAME_Y}[t2];'
          f"[t2][2:v]overlay=0:0:enable='lt(t,{cap_secs})',format=yuv420p[v]")
    cmd = ['ffmpeg', '-y', '-v', 'error', '-i', face, '-i', game, '-loop', '1', '-i', cap]
    if af and ag:
        fc += (f';[0:a]atrim={face_start}:{face_start + dur},asetpts=PTS-STARTPTS,volume=1.4[fa];'
               f'[1:a]atrim={game_start}:{game_start + dur},asetpts=PTS-STARTPTS,volume=0.6[ga];[fa][ga]amix=inputs=2:normalize=0[a]')
        amap = ['-map', '[a]']
    elif af: amap = ['-map', '0:a']
    elif ag: amap = ['-map', '1:a']
    else:
        cmd += ['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo']; amap = ['-map', '3:a']
    part = out + '.part.mp4'
    cmd += ['-filter_complex', fc, '-map', '[v]'] + amap + ['-t', f'{dur:.2f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19',
            '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', part]
    subprocess.run(cmd, check=True); os.replace(part, out)
    print('done', out, f'{dur:.1f}s')

if __name__ == '__main__':
    main(*sys.argv[1:])
