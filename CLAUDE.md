# Project notes for Claude

## Instagram skills (ig-*)
The ig-* skills look for the user's voice profile at `~/.claude/instagram/voice.md`.
In this repo the voice profile lives at `instagram/voice.md` (cloud sessions reset the home folder).
At the start of any ig-* task: if `~/.claude/instagram/voice.md` is missing, copy `instagram/` into
`~/.claude/instagram/`, and after editing voice.md / swipe.md / log.md copy them back to `instagram/`
so they are saved in git.

## Design index (فهرس-التصاميم.md) - read first, update automatically
`فهرس-التصاميم.md` at the repo root is the design index: brand style, every design, and the change log.
The owner also keeps a copy in Google Drive: `Kami_Printing/فهرس-التصاميم.md`.
- Before any design task (post, carousel, story, highlight, reel cover, sticker, label, print, mockup), read the index
  and follow section 1 (style, fonts, colors, sizes, fixed elements, the «في» rule). It overrides the older style in `templates/README.md`.
- After every new design or edit, without being asked, update the index in the same commit as the design:
  add or update its row in section 6 (or the matching section), add a row at the top of the section 7 log
  (date, design, change, folder), bump «آخر تحديث», then commit and push.
- Edits go in a new `تعديل N/` folder next to the original; never overwrite the original files.
- Write the index in Arabic (Bahraini dialect), the same way as the existing rows.
