#!/usr/bin/env python3
"""Update فهرس-التصاميم.md automatically.

Rewrites only the part between the AUTO markers (sections 7 and 8) from
tools/design_index.json plus a scan of the deliverable folders, and bumps
the «آخر تحديث» date. Everything above the markers (sections 1-6, kept in
sync with the copy on the owner's computer / Google Drive) is left as is.

Run: python3 tools/update_index.py        (prints what changed)
     python3 tools/update_index.py --check (exit 1 if the index is stale)
"""
import datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'فهرس-التصاميم.md')
REG = os.path.join(ROOT, 'tools', 'design_index.json')
START, END = '<!-- AUTO:START (لا تعدل يدوياً، عدّل tools/design_index.json) -->', '<!-- AUTO:END -->'
KINDS = [('فيديو', ('.mp4', '.mov', '.webm')), ('صورة', ('.png', '.jpg', '.jpeg', '.webp')),
         ('PDF', ('.pdf',)), ('صوت', ('.mp3', '.wav', '.m4a')), ('نص', ('.txt', '.md'))]


def files_in(path):
    out = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, path)):
        dn[:] = [d for d in dn if not d.startswith('.')]
        out += [os.path.join(dp, f) for f in fn if not f.startswith('.')]
    return out


def summary(path):
    fs = files_in(path)
    parts = []
    for name, exts in KINDS:
        n = sum(1 for f in fs if f.lower().endswith(exts))
        if n:
            parts.append(f'{n} {name}')
    return ' · '.join(parts) or 'فاضي'


def last_date(path):
    try:
        d = subprocess.run(['git', 'log', '-1', '--format=%ad', '--date=short', '--', path],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except OSError:
        d = ''
    return d or datetime.date.today().isoformat() + ' (مو مرفوع)'


def scan(roots):
    found = []
    for r in roots:
        for p in sorted(glob.glob(os.path.join(ROOT, r))):
            if os.path.isdir(p) and not os.path.basename(p).startswith('.'):
                found.append(os.path.relpath(p, ROOT))
    return found


def esc(s):
    return s.replace('|', '\\|')


def build(reg):
    known = {d['path'] for d in reg['designs']}
    lines = [START, '', '## 7. تصاميم السحابة (الريبو Girhub)',
             'اللي نسويه في سشنات Claude على الويب ينحفظ في الريبو مو في `المشروع\\`. '
             'هذا القسم يتحدث تلقائياً من الملفات نفسها (العدد وتاريخ آخر تعديل).', '']
    groups = []
    for d in reg['designs']:
        if d['group'] not in groups:
            groups.append(d['group'])
    for g in groups:
        lines += [f'### {g}', '| التصميم | المجلد | الملفات | آخر تعديل | المحتوى |', '|---|---|---|---|---|']
        for d in reg['designs']:
            if d['group'] != g:
                continue
            if not os.path.isdir(os.path.join(ROOT, d['path'])):
                lines.append(f"| {esc(d['title'])} | `{d['path']}` | ⚠️ المجلد مو موجود | — | {esc(d['desc'])} |")
                continue
            lines.append(f"| {esc(d['title'])} | `{d['path']}` | {summary(d['path'])} | {last_date(d['path'])} | {esc(d['desc'])} |")
        lines.append('')
    new = [p for p in scan(reg['roots']) if p not in known and not any(p.startswith(k + '/') for k in known)]
    if new:
        lines += ['### جديد (لقطه السكربت، يحتاج وصف في design_index.json)',
                  '| المجلد | الملفات | آخر تعديل |', '|---|---|---|']
        lines += [f'| `{p}` | {summary(p)} | {last_date(p)} |' for p in new]
        lines.append('')
    lines += ['---', '', '## 8. سجل تعديلات السحابة', '| التاريخ | التصميم | التعديل | المجلد |', '|---|---|---|---|']
    for e in sorted(reg['log'], key=lambda e: e['date'], reverse=True):
        lines.append(f"| {e['date']} | {esc(e['design'])} | {esc(e['change'])} | `{e['folder']}` |")
    lines += ['', END, '']
    return '\n'.join(lines), new


def main():
    reg = json.load(open(REG, encoding='utf-8'))
    text = open(INDEX, encoding='utf-8').read()
    auto, new = build(reg)
    if START in text and END in text:
        head = text[:text.index(START)]
        tail = text[text.index(END) + len(END):].lstrip('\n')
    else:
        head, tail = text.rstrip('\n') + '\n\n---\n\n', ''
    old_auto = text[len(head):len(text) - len(tail)] if START in text else ''
    if old_auto.strip() == auto.strip():
        print('الفهرس محدّث، ما فيه تغيير.')
        return 0
    if '--check' in sys.argv:
        print('الفهرس يحتاج تحديث: شغّل python3 tools/update_index.py')
        return 1
    dates = [e['date'] for e in reg['log']] + [datetime.date.today().isoformat()]
    head = re.sub(r'(> آخر تحديث: )\S+', lambda m: m.group(1) + max(dates), head, count=1)
    open(INDEX, 'w', encoding='utf-8').write(head + auto + tail)
    print(f'تحدّث الفهرس: {len(reg["designs"])} تصميم، {len(reg["log"])} سطر في السجل.')
    for p in new:
        print(f'  جديد بدون وصف: {p}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
