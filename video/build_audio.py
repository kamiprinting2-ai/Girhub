"""Generate the voiceover (edge-tts, Bahraini male voice), the timeline for the
animation (line start times + mouth envelope), and a soft music bed.

usage: python3 video/build_audio.py
outputs: video/timeline.js, video/out/voice.wav, video/out/mix.wav
"""
import asyncio, json, os, subprocess, wave
import numpy as np
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out'); TMP = os.path.join(OUT, 'lines')
os.makedirs(TMP, exist_ok=True)
VOICE, RATE, PITCH = 'ar-BH-AliNeural', '+12%', '+0Hz'
SR, FPS = 48000, 30

# (scene, on-screen bubble text, what the voice says)
LINES = [
    (0, '٥ أشياء أمي تطلبها من Kami!', 'خمسة أشياء، أمي تطلبها من كامي!'),
    (1, 'رقم ٥.. محد يدري عنه!', 'رقم خمسة، محد يدري عنه!'),
    (2, 'رقم ١: توزيعات المواليد.', 'رقم واحد: توزيعات المواليد.'),
    (2, 'علب، ستيكرات، وكروت باسم البيبي.', 'علب، ستيكرات، وكروت باسم البيبي.'),
    (2, 'وحتى طاولة الاستقبال يطبعونها!', 'وحتى طاولة الاستقبال، يطبعونها!'),
    (3, 'رقم ٢: رمضان، والقرقاعون، والعيد.', 'رقم اثنين: رمضان، والقرقاعون، والعيد.'),
    (3, 'كل موسم له توزيعته.', 'كل موسم، له توزيعته.'),
    (3, 'وأعراس وأعياد ميلاد بعد!', 'وأعراس، وأعياد ميلاد بعد!'),
    (4, 'رقم ٣: الطباعة.', 'رقم ثلاثة: الطباعة.'),
    (4, 'بنرات، بزنس كارد، ستيكرات بقص، وأكريليك.', 'بنرات، بزنس كارد، ستيكرات بقص، وأكريليك.'),
    (5, 'رقم ٤: قرطاسية المدرسة.', 'رقم أربعة: قرطاسية المدرسة.'),
    (5, 'أختي الصغيرة، ستيكر اسمها على كل دفاترها!', 'أختي الصغيرة، ستيكر اسمها على كل دفاترها!'),
    (6, 'ورقم ٥...', 'ورقم خمسة...'),
    (7, 'يخلّصون معاملاتك الحكومية!', 'يخلّصون معاملاتك الحكومية!'),
    (7, 'بطاقة، إسكان، بنفت.. وأنت في البيت.', 'بطاقة، إسكان، بنفت، وأنت في البيت.'),
    (8, 'مدينة عيسى، وعندهم توصيل!', 'مدينة عيسى، وعندهم توصيل!'),
    (9, 'اكتب "Kami" بالتعليقات، ويكلمونك.', 'اكتب كامي بالتعليقات، ويكلمونك.'),
    (10, 'عشان جذي أمي ما تطلب من غيرهم!', 'عشان جذي، أمي ما تطلب من غيرهم!'),
]

async def tts(i, text):
    mp3 = os.path.join(TMP, f'{i:02d}.mp3')
    kw = {'proxy': os.environ.get('HTTPS_PROXY')} if os.environ.get('HTTPS_PROXY') else {}
    await edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH, **kw).save(mp3)
    wav = mp3[:-4] + '.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-ac', '1', '-ar', str(SR), wav], check=True)
    with wave.open(wav) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(a) > 0.01)[0]          # trim leading/trailing silence
    return a[max(0, nz[0] - 800):nz[-1] + 1600] if len(nz) else a

async def main():
    clips = [await tts(i, l[2]) for i, l in enumerate(LINES)]
    t, prev_scene, timeline, parts = 0.45, 0, [], []
    for (scene, text, _), c in zip(LINES, clips):
        if scene != prev_scene:
            t += 0.35
        if scene == 7:                          # beat of suspense after "ورقم خمسة"
            t += 0.15 if text.startswith('بطاقة') else 0.6
        timeline.append({'t': round(t, 3), 'd': round(len(c) / SR, 3), 'text': text, 'scene': scene})
        parts.append((t, c)); t += len(c) / SR + 0.22; prev_scene = scene
    dur = round(t + 2.6, 2)
    voice = np.zeros(int(dur * SR), np.float32)
    for st, c in parts:
        i = int(st * SR); voice[i:i + len(c)] += c

    # mouth envelope per video frame
    hop = SR // FPS
    env = np.array([np.sqrt(np.mean(voice[k:k + hop] ** 2)) for k in range(0, len(voice), hop)])
    env = np.clip(env / (np.percentile(env[env > 0.005], 90) + 1e-9), 0, 1)
    env = np.round(np.convolve(env, [0.25, 0.5, 0.25], 'same'), 2)

    # soft music bed: warm chord pads + plucks, I-V-vi-IV in D major, 100 bpm
    n = len(voice); tt = np.arange(n) / SR; music = np.zeros(n, np.float32)
    beat = 60 / 100; bar = beat * 4
    chords = [[62, 66, 69], [57, 61, 64], [59, 62, 66], [55, 59, 62]]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    for b in range(int(dur / bar) + 1):
        ch = chords[b % 4]; s0 = int(b * bar * SR); s1 = min(n, int((b + 1) * bar * SR))
        if s0 >= n: break
        seg = tt[s0:s1] - b * bar
        pad = sum(np.sin(2 * np.pi * hz(m - 12) * seg) for m in ch) / 3
        music[s0:s1] += 0.10 * pad * np.minimum(1, seg / 0.3) * np.minimum(1, (bar - seg) / 0.3)
        for k in range(8):                      # eighth-note plucks
            ps = int((b * bar + k * beat / 2) * SR)
            if ps >= n: break
            m = ch[[0, 1, 2, 1, 2, 0, 1, 2][k]] + (12 if k % 4 == 3 else 0)
            L = min(int(0.4 * SR), n - ps); x = np.arange(L) / SR
            music[ps:ps + L] += 0.07 * np.sin(2 * np.pi * hz(m) * x) * np.exp(-x * 9)
    fade = np.minimum(1, np.minimum(tt / 1.0, (dur - tt) / 2.0))
    music *= fade
    # duck music under the voice
    vol = np.repeat(env, hop)[:n]; vol = np.pad(vol, (0, n - len(vol)))
    duck = 1 - 0.55 * np.convolve(vol, np.ones(4800) / 4800, 'same')
    mix = voice * 0.95 + music * duck * 0.9
    mix /= max(1.0, np.abs(mix).max() / 0.95)

    def save(path, x):
        with wave.open(path, 'w') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((x * 32767).astype(np.int16).tobytes())
    save(os.path.join(OUT, 'voice.wav'), voice); save(os.path.join(OUT, 'mix.wav'), mix)
    with open(os.path.join(HERE, 'timeline.js'), 'w', encoding='utf-8') as f:
        f.write('window.TL=' + json.dumps({'lines': timeline, 'dur': dur, 'env': env.tolist()}, ensure_ascii=False) + ';')
    print('duration', dur, 's ·', len(timeline), 'lines')

asyncio.run(main())
