"""Synthesized (fully original, royalty-free) music bed + sound effects."""
import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7,
        'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}

def hz(midi): return 440.0 * 2 ** ((midi - 69) / 12)

def chord_notes(name, octave=4):
    minor = name.endswith('m')
    root = NOTE[name[:-1] if minor else name] + 12 * (octave + 1)
    return [root, root + (3 if minor else 4), root + 7]

def lowpass(x, fc, order=2):
    return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), x)

def reverb(x, secs=2.2, mix=0.32, seed=1):
    n = int(SR * secs); rng = np.random.default_rng(seed)
    ir = rng.standard_normal(n) * np.exp(-np.linspace(0, 7, n))
    ir = lowpass(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
    wet = fftconvolve(x, ir)[:len(x)]
    return x * (1 - mix) + wet * mix * 3

def env_adsr(n, a, r):
    e = np.ones(n); na = min(int(a * SR), n // 2); nr = min(int(r * SR), n // 2)
    if n < 4: return np.zeros(n)
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr)
    return e

def music(dur, prog, bpm=66, seed=0, duck=()):
    n = int(dur * SR); out = np.zeros(n); t = np.arange(n) / SR
    beat = 60 / bpm; bar = beat * 4
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(dur / bar)) + 1
    pad = np.zeros(n); pl = np.zeros(n); bass = np.zeros(n)
    for b in range(nb):
        ch = prog[b % len(prog)]
        s0 = int(b * bar * SR); s1 = min(n, int((b + 1) * bar * SR + 0.6 * SR))
        if s0 >= n: break
        seg = np.arange(s1 - s0) / SR
        e = env_adsr(s1 - s0, 0.9, 0.9)
        for m in chord_notes(ch, 3) + [chord_notes(ch, 4)[0]]:
            f = hz(m)
            for det in (-0.12, 0.12):
                ff = f * 2 ** (det / 12)
                pad[s0:s1] += e * (np.sin(2 * np.pi * ff * seg) + 0.35 * np.sin(4 * np.pi * ff * seg) + 0.15 * np.sin(6 * np.pi * ff * seg)) * 0.05
        bf = hz(chord_notes(ch, 2)[0])
        bass[s0:s1] += e * np.sin(2 * np.pi * bf * seg) * 0.16
        # soft piano arpeggio
        tones = chord_notes(ch, 4) + [chord_notes(ch, 5)[0]]
        pattern = [0, 1, 2, 3, 2, 1, 2, 3]
        for i, pi in enumerate(pattern):
            st = b * bar + i * beat / 2
            if st >= dur: break
            if rng.random() < 0.18 and i % 2: continue
            f = hz(tones[pi]); L = int(1.8 * SR); s = int(st * SR); e2 = min(n, s + L)
            sg = np.arange(e2 - s) / SR
            v = (np.sin(2 * np.pi * f * sg) + 0.3 * np.sin(4 * np.pi * f * sg) * np.exp(-sg * 6) + 0.12 * np.sin(6 * np.pi * f * sg) * np.exp(-sg * 9))
            v *= np.exp(-sg * 2.6) * (1 - np.exp(-sg * 400)) * (0.085 if i % 4 == 0 else 0.06)
            pl[s:e2] += v
    pad = lowpass(pad, 1400)
    out = pad + bass + pl
    out = reverb(out, 2.6, 0.35, seed)
    g = np.ones(n)
    g[:int(0.02 * SR)] = np.linspace(0, 1, int(0.02 * SR))
    for a, b, lvl in duck:
        ia, ib = int(a * SR), int(b * SR)
        g[ia:ib] = np.minimum(g[ia:ib], lvl)
    g = lowpass(g, 6)
    return out * g

def sfx(kind, seed=0):
    rng = np.random.default_rng(seed)
    if kind == 'pop':
        L = int(0.09 * SR); t = np.arange(L) / SR
        f = 700 + 900 * (t / t[-1])
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45) * 0.22
    if kind == 'tick':
        L = int(0.12 * SR); t = np.arange(L) / SR
        return np.sin(2 * np.pi * 1500 * t) * np.exp(-t * 60) * 0.18
    if kind == 'whoosh':
        L = int(0.7 * SR); t = np.arange(L) / SR
        x = rng.standard_normal(L)
        x = sosfilt(butter(2, [400, 3500], 'band', fs=SR, output='sos'), x)
        return x * np.sin(np.pi * t / t[-1]) ** 2 * 0.25
    if kind == 'thud':
        L = int(0.45 * SR); t = np.arange(L) / SR
        f = 90 * np.exp(-t * 4) + 45
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 0.6
        x += lowpass(rng.standard_normal(L), 900) * np.exp(-t * 40) * 0.25
        return x
    if kind == 'knock':
        out = np.zeros(int(0.5 * SR))
        for st in (0, 0.22):
            L = int(0.12 * SR); t = np.arange(L) / SR
            k = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 50) * 0.5 + lowpass(rng.standard_normal(L), 2000) * np.exp(-t * 80) * 0.4
            s = int(st * SR); out[s:s + L] += k
        return out
    if kind == 'boom':
        L = int(1.6 * SR); t = np.arange(L) / SR
        f = 70 * np.exp(-t * 2) + 32
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6) * 0.7
        x += lowpass(rng.standard_normal(L), 400) * np.exp(-t * 6) * 0.3
        return x
    if kind == 'chime':
        L = int(2.0 * SR); t = np.arange(L) / SR
        x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * d) * a for f, d, a in ((1318.5, 2.5, 0.12), (1760, 3, 0.09), (2637, 4, 0.05)))
        x[int(0.12 * SR):] += (np.sin(2 * np.pi * 1975.5 * t) * np.exp(-t * 3) * 0.08)[:L - int(0.12 * SR)]
        return x
    if kind == 'rewind':
        L = int(1.0 * SR); t = np.arange(L) / SR
        f = 900 * np.exp(-t * 2.2) + 120
        x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.05
        x += sosfilt(butter(2, [800, 5000], 'band', fs=SR, output='sos'), rng.standard_normal(L)) * 0.12
        return lowpass(x, 3000) * np.sin(np.pi * t / t[-1]) ** 0.5
    if kind == 'crack':
        L = int(0.6 * SR); t = np.arange(L) / SR
        x = rng.standard_normal(L) * (rng.random(L) < 0.08) * np.exp(-t * 7) * 0.5
        return lowpass(x, 3500) + np.sin(2 * np.pi * 60 * t) * np.exp(-t * 8) * 0.3
    raise ValueError(kind)

def mix(dur, prog, events, bpm=66, seed=0, duck=()):
    m = music(dur, prog, bpm, seed, duck) * 0.9
    fx = np.zeros_like(m)
    for i, (kind, t) in enumerate(events):
        x = sfx(kind, seed + i); s = int(t * SR)
        if s >= len(fx): continue
        e = min(len(fx), s + len(x)); fx[s:e] += x[:e - s]
    fx = reverb(fx, 1.2, 0.18, seed + 7)
    out = m + fx
    # fade tail
    nf = int(0.5 * SR); out[-nf:] *= np.linspace(1, 0.35, nf)
    out = np.tanh(out * 1.4) / np.tanh(1.4)
    out *= 0.85 / (np.abs(out).max() + 1e-9)
    return out

def write_wav(path, x):
    st = np.stack([x, x], 1)
    d = (np.clip(st, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())
