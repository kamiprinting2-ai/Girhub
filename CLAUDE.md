# Project notes for Claude

## Instagram skills (ig-*)
The ig-* skills look for the user's voice profile at `~/.claude/instagram/voice.md`.
In this repo the voice profile lives at `instagram/voice.md` (cloud sessions reset the home folder).
At the start of any ig-* task: if `~/.claude/instagram/voice.md` is missing, copy `instagram/` into
`~/.claude/instagram/`, and after editing voice.md / swipe.md / log.md copy them back to `instagram/`
so they are saved in git.

## Design index (فهرس-التصاميم.md) - Google Drive is the master, update it automatically
The master copy is in the owner's Google Drive: folder `Kami_Printing` (folder id `17TbJv_LDf2wvtpPiZze-1mPkIiGQuwTL`),
file `فهرس-التصاميم.md`. `فهرس-التصاميم.md` at the repo root is a mirror kept in git. If they differ, Drive wins.
The owner gave standing permission (2026-11-19) to update the Drive file automatically, every time, without asking.

Before any design task (post, carousel, story, highlight, reel cover, sticker, label, print, mockup):
1. Find the file: Google Drive `search_files` with `title = 'فهرس-التصاميم.md' and parentId = '17TbJv_LDf2wvtpPiZze-1mPkIiGQuwTL'`
   (the file id changes on every update, so always search; never reuse an old id).
2. `download_file_content` and copy it over the repo `فهرس-التصاميم.md`.
3. Follow section 1 (style, fonts, colors, sizes, fixed elements, the «في» rule). It overrides the older style in `templates/README.md`.

After every new design or edit, without being asked:
1. Download the Drive file again (the owner may have edited it) and apply the change on top of it:
   add or update the design's row (section 6 for designs stored in this repo), add a row at the top of the section 7 log
   (date, design, change, folder), and bump «آخر تحديث». Write it in Arabic (Bahraini dialect) like the existing rows.
2. The Drive tools cannot edit a file's content, so replace it: `create_file` in the same folder with the same title,
   `contentMimeType: text/markdown`, `disableConversionToGoogleType: true`, content as a `sha256:<hash>:<path>` file reference.
   Download the new file and `cmp` it with the local one. Only if identical, `trash_file` the old id (it stays in the trash 30 days).
   If anything fails, keep the old file and tell the owner.
3. Commit the repo mirror together with the design and push.

Edits go in a new `تعديل N/` folder next to the original; never overwrite the original files.
