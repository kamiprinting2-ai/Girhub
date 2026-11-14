"""Kami paper mascot (brand version): cream sheet, forest outline, blush folded
corners, the logo's pink swoosh as a sash and the logo's four-point star.
mascot(pose) -> inline <svg> string. Poses: wave, plane, gift, pencil, doc, star, card, question
"""
F, C, B, S, R = '#2E3B2A', '#F6F3EC', '#E2CDCC', '#A7B591', '#D3959B'
STAR = 'M0 -20C1 -7 7 -1 20 0C7 1 1 7 0 20C-1 7 -7 1 -20 0C-7 -1 -1 -7 0 -20Z'

def _star(x, y, s, col):
    return f'<path d="{STAR}" transform="translate({x} {y}) scale({s})" fill="{col}"/>'

def _hand(x, y):
    return f'<circle cx="{x}" cy="{y}" r="12" fill="{C}" stroke="{F}" stroke-width="7"/>'

def _arm(d):
    return f'<path d="{d}" fill="none" stroke="{F}" stroke-width="9" stroke-linecap="round"/>'

def mascot(pose='wave', mouth='smile', size=None):
    p = []
    # shadow + legs
    p.append(f'<ellipse cx="150" cy="330" rx="88" ry="10" fill="{F}" opacity=".14"/>')
    p.append(_arm('M124 292 L120 318') + _arm('M176 292 L180 318'))
    p.append(f'<ellipse cx="114" cy="321" rx="17" ry="9" fill="{F}"/><ellipse cx="186" cy="321" rx="17" ry="9" fill="{F}"/>')
    back, front = [], []
    # arms / props
    if pose == 'wave':
        back.append(_arm('M74 215 C52 232 50 252 58 266') + _hand(58, 268))
        front.append(_arm('M226 205 C258 186 268 156 262 124') + _hand(262, 116))
        front.append(f'<path d="M282 96 q10 -8 6 -20 M292 116 q14 -2 18 -14" fill="none" stroke="{F}" stroke-width="5" stroke-linecap="round"/>')
    elif pose == 'plane':
        back.append(_arm('M226 215 C246 232 248 252 240 266') + _hand(240, 268))
        front.append(_arm('M74 200 C52 196 40 186 34 176') + _hand(34, 172))
        front.append(f'<g transform="translate(-30 112) rotate(-12)"><path d="M0 40 L92 0 L60 58 Z" fill="{B}" stroke="{F}" stroke-width="6" stroke-linejoin="round"/>'
                     f'<path d="M92 0 L36 46 L44 72 Z" fill="{C}" stroke="{F}" stroke-width="6" stroke-linejoin="round"/></g>')
        front.append(f'<path d="M-40 150 q-14 6 -22 0 M-46 172 q-12 8 -24 4" fill="none" stroke="{S}" stroke-width="5" stroke-linecap="round"/>')
    elif pose == 'gift':
        front.append(f'<rect x="104" y="228" width="92" height="66" rx="6" fill="{B}" stroke="{F}" stroke-width="7"/>'
                     f'<rect x="98" y="214" width="104" height="20" rx="5" fill="{C}" stroke="{F}" stroke-width="7"/>'
                     f'<path d="M150 214 V294" stroke="{S}" stroke-width="12"/><path d="M150 214 c-14 -26 -40 -18 -26 -2 M150 214 c14 -26 40 -18 26 -2" fill="none" stroke="{F}" stroke-width="6" stroke-linecap="round"/>')
        front.append(_arm('M74 215 C80 236 90 248 100 252') + _hand(102, 254))
        front.append(_arm('M226 215 C220 236 210 248 200 252') + _hand(198, 254))
    elif pose == 'pencil':
        back.append(_arm('M74 215 C52 232 50 252 58 266') + _hand(58, 268))
        front.append(f'<g transform="translate(262 190) rotate(18)"><rect x="-13" y="-120" width="26" height="150" fill="{S}" stroke="{F}" stroke-width="6"/>'
                     f'<path d="M-13 30 L0 62 L13 30 Z" fill="{C}" stroke="{F}" stroke-width="6" stroke-linejoin="round"/><path d="M-4 52 L0 62 L4 52 Z" fill="{F}"/>'
                     f'<rect x="-13" y="-140" width="26" height="22" rx="6" fill="{B}" stroke="{F}" stroke-width="6"/></g>')
        front.append(_arm('M226 210 C242 206 252 200 258 192') + _hand(260, 190))
    elif pose in ('doc', 'star', 'card'):
        back.append(_arm('M74 215 C52 232 50 252 58 266') + _hand(58, 268))
        if pose == 'card':
            front.append(f'<g transform="translate(232 150) rotate(-10)"><rect x="0" y="0" width="96" height="60" rx="8" fill="{C}" stroke="{F}" stroke-width="6"/>'
                         f'<circle cx="24" cy="26" r="9" fill="{B}"/><path d="M44 22 h36 M44 38 h26 M16 46 h20" stroke="{F}" stroke-width="5" stroke-linecap="round"/></g>')
        else:
            mark = (f'<circle cx="52" cy="78" r="18" fill="{S}" stroke="{F}" stroke-width="5"/><path d="M43 78 l7 7 12 -13" fill="none" stroke="{F}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
                    if pose == 'doc' else _star(52, 74, 1.1, R))
            front.append(f'<g transform="translate(228 112) rotate(10)"><path d="M0 0 H56 L80 24 V110 H0 Z" fill="{C}" stroke="{F}" stroke-width="6" stroke-linejoin="round"/>'
                         f'<path d="M56 0 V24 H80" fill="{B}" stroke="{F}" stroke-width="6" stroke-linejoin="round"/>'
                         f'<path d="M14 30 H44 M14 46 H40" stroke="{F}" stroke-width="5" stroke-linecap="round"/>{mark}</g>')
        front.append(_arm('M226 216 C232 214 236 210 236 204') + _hand(236, 202))
    elif pose == 'question':
        back.append(_arm('M74 215 C52 232 50 252 58 266') + _hand(58, 268))
        front.append(_arm('M226 222 C222 208 206 206 196 214') + _hand(194, 214))
        front.append(f'<g transform="translate(250 40)"><circle r="34" fill="{B}" stroke="{F}" stroke-width="6"/>'
                     f'<text y="16" text-anchor="middle" font-family="Alexandria, sans-serif" font-weight="700" font-size="46" fill="{F}">?</text></g>')
    # body: sheet with two folded top corners
    body = (f'<path d="M70 112 L112 62 H188 L230 112 V280 Q230 296 214 296 H86 Q70 296 70 280 Z" fill="{C}" stroke="{F}" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="M70 112 L112 62 V98 Q112 112 98 112 Z" fill="{B}" stroke="{F}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M230 112 L188 62 V98 Q188 112 202 112 Z" fill="{B}" stroke="{F}" stroke-width="7" stroke-linejoin="round"/>'
            # logo swoosh as a sash
            f'<path d="M74 250 C118 282 170 226 226 238" fill="none" stroke="{B}" stroke-width="15" stroke-linecap="round"/>')
    eyes = (f'<ellipse cx="122" cy="172" rx="10" ry="12" fill="{F}"/><ellipse cx="178" cy="172" rx="10" ry="12" fill="{F}"/>'
            f'<circle cx="125" cy="167" r="3.5" fill="#fff"/><circle cx="181" cy="167" r="3.5" fill="#fff"/>')
    cheeks = f'<ellipse cx="104" cy="198" rx="13" ry="8" fill="{R}" opacity=".55"/><ellipse cx="196" cy="198" rx="13" ry="8" fill="{R}" opacity=".55"/>'
    if mouth == 'open':
        m = f'<path d="M134 196 Q150 220 166 196 Z" fill="{F}" stroke="{F}" stroke-width="5" stroke-linejoin="round"/><path d="M142 206 Q150 214 158 206" fill="{R}"/>'
    else:
        m = f'<path d="M134 198 Q150 214 166 198" fill="none" stroke="{F}" stroke-width="7" stroke-linecap="round"/>'
    sparkles = _star(262, 46, 1.25, R) + _star(36, 92, .7, S) if pose not in ('question',) else _star(40, 80, .8, S)
    inner = ''.join(p) + ''.join(back) + body + eyes + cheeks + m + ''.join(front) + sparkles
    sz = f' width="{size}" height="{size * 360 / 340:.0f}"' if size else ''
    return f'<svg class="mascot" viewBox="-80 0 420 360"{sz}>{inner}</svg>'

if __name__ == '__main__':
    import os
    poses = ['wave', 'plane', 'gift', 'pencil', 'doc', 'star', 'card', 'question']
    names = ['أهلاً', 'أرسلوا طلبكم', 'التوزيعات', 'المدرسة', 'المعاملات', 'الطباعة', 'التعاون', 'أسئلة']
    cells = ''.join(f'<div class="c">{mascot(p, "open" if p in ("wave", "plane") else "smile", 300)}<b>{n}</b></div>' for p, n in zip(poses, names))
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Kami Mascot</title>
<link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@600;700&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#999}}.post{{width:1600px;height:900px;background:{S};display:grid;grid-template-columns:repeat(4,1fr);align-items:center;justify-items:center;padding:40px;box-sizing:border-box;font-family:Alexandria}}
.c{{display:flex;flex-direction:column;align-items:center}}.c b{{margin-top:6px;font-size:30px;color:{F};background:{C};padding:4px 22px;border-radius:30px}}</style></head>
<body><section class="post" id="mascot-sheet">{cells}</section></body></html>'''
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mascot-sheet.html'), 'w', encoding='utf-8').write(html)
    print('ok')
