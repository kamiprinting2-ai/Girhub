#!/usr/bin/env python3
"""Keep فهرس-التصاميم.md current.

The original lives on Google Drive (Kami_Printing/المشروع/فهرس-التصاميم.md).
Everything above the AUTO marker is the owner's text and is never rewritten
here; the block between the AUTO markers at the end is generated: a status
table of the repo's design folders (file counts, last change) plus any new
folder that the index does not describe yet.

  python3 tools/update_index.py                 refresh the AUTO block
  python3 tools/update_index.py --pull FILE     take FILE (fresh Drive download) as the
                                                owner's text, then refresh the AUTO block
  python3 tools/update_index.py --check         exit 1 if the AUTO block is stale
"""
import datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'فهرس-التصاميم.md')
REG = os.path.join(ROOT, 'tools', 'design_index.json')
START = '<!-- AUTO:START (يتولد تلقائياً من tools/update_index.py، لا تعدله) -->'
END = '<!-- AUTO:END -->'
START_RE = re.compile(r'\n*(---\s*\n+)?<!-- AUTO:START.*?-->.*?<!-- AUTO:END -->\n*', re.S)
KINDS = [('فيديو', ('.mp4', '.mov', '.webm')), ('صورة', ('.png', '.jpg', '.jpeg', '.webp')),
         ('PDF', ('.pdf',)), ('صوت', ('.mp3', '.wav', '.m4a')), ('HTML', ('.html',)), ('نص', ('.txt', '.md'))]


def files_in(path):
    out = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, path)):
        dn[:] = [d for d in dn if not d.startswith('.')]
        out += [os.path.join(dp, f) for f in fn if not f.startswith('.')]
    return out


def summary(path):
    fs = files_in(path)
    parts = [f'{n} {name}' for name, exts in KINDS
             if (n := sum(1 for f in fs if f.lower().endswith(exts)))]
    return ' · '.join(parts) or 'فاضي'


def last_date(path):
    try:
        st = subprocess.run(['git', 'status', '--porcelain', '--', path], cwd=ROOT,
                            capture_output=True, text=True).stdout.strip()
        d = subprocess.run(['git', 'log', '-1', '--format=%ad', '--date=short', '--', path],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except OSError:
        st, d = '', ''
    if st or not d:
        return datetime.date.today().isoformat() + ' (مو مرفوع)'
    return d


def scan(roots):
    found = []
    for r in roots:
        for p in sorted(glob.glob(os.path.join(ROOT, r))):
            if os.path.isdir(p) and not os.path.basename(p).startswith('.'):
                found.append(os.path.relpath(p, ROOT))
    return found


def build(reg, owner_text):
    nums = [int(n) for n in re.findall(r'^## (\d+)\.', owner_text, re.M)]
    sec = (max(nums) + 1) if nums else 1
    known = [d['path'] for d in reg['designs']]
    lines = [START, '', f'## {sec}. حالة ملفات المستودع (تلقائي)',
             'هذا القسم يتحدث بروحه من ملفات المستودع: كم ملف في كل مجلد، ومتى آخر تعديل. '
             'الوصف والسجل في الأقسام اللي فوق.', '',
             '| التصميم | المجلد | الملفات | آخر تعديل |', '|---|---|---|---|']
    for d in reg['designs']:
        if os.path.isdir(os.path.join(ROOT, d['path'])):
            lines.append(f"| {d['title']} | `{d['path']}` | {summary(d['path'])} | {last_date(d['path'])} |")
        else:
            lines.append(f"| {d['title']} | `{d['path']}` | ⚠️ المجلد مو موجود | — |")
    new = [p for p in scan(reg['roots'])
           if p not in known and not any(p.startswith(k + '/') for k in known)]
    if new:
        lines += ['', '**مجلدات جديدة ما لها وصف للحين** (ضيفوها فوق وفي `tools/design_index.json`):', '']
        lines += [f'- `{p}`: {summary(p)}، {last_date(p)}' for p in new]
    lines += ['', END, '']
    return '\n'.join(lines), new


def owner_part(text):
    return START_RE.sub('\n', text).rstrip('\n') + '\n'


def main():
    reg = json.load(open(REG, encoding='utf-8'))
    if '--pull' in sys.argv:
        src = sys.argv[sys.argv.index('--pull') + 1]
        text = open(src, encoding='utf-8').read()
    else:
        text = open(INDEX, encoding='utf-8').read()
    owner = owner_part(text)
    auto, new = build(reg, owner)
    out = owner + '\n---\n\n' + auto
    cur = open(INDEX, encoding='utf-8').read() if os.path.exists(INDEX) else ''
    if cur == out:
        print('الفهرس محدّث، ما فيه تغيير.')
        return 0
    if '--check' in sys.argv:
        print('الفهرس يحتاج تحديث: شغّل python3 tools/update_index.py')
        return 1
    open(INDEX, 'w', encoding='utf-8').write(out)
    print(f'تحدّث الفهرس ({len(reg["designs"])} مجلد).')
    for p in new:
        print(f'  جديد بدون وصف: {p}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
