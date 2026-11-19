# Project notes for Claude

## Design index (فهرس-التصاميم.md) — read before any design or video
- `فهرس-التصاميم.md` is the owner's master design index. Sections 1-6 come from the copy on their
  computer / Google Drive (file id `1mwzSOTcUwFfgkDorIXgwgIMR8ElgCnOh`, folder `17TbJv_LDf2wvtpPiZze-1mPkIiGQuwTL`).
  Section 1 is the brand style (colors, Readex Pro 700 + IBM Plex Sans Arabic, sizes, no «في» in Readex titles): follow it.
- At the start of a design task: re-read the Drive copy (search_files title contains 'فهرس'); if it changed,
  replace everything above the `AUTO:START` marker in the repo file with it.
- Sections 7-8 are generated. After every new design, video or edit: add/adjust its entry in
  `tools/design_index.json` (`designs` + a `log` line, Arabic, Bahraini dialect), then run
  `python3 tools/update_index.py`. A Stop hook also runs it, so file counts/dates stay current; folders
  with no entry show up under «جديد» until described.
- Then sync to Drive: the Drive API can't overwrite file content, so trash the old
  `فهرس-التصاميم-السحابة.md` in that folder and upload sections 7-8 as a new one with the same name
  (text/markdown, disableConversionToGoogleType). Never touch the owner's main Drive file.

## Instagram skills (ig-*)
The ig-* skills look for the user's voice profile at `~/.claude/instagram/voice.md`.
In this repo the voice profile lives at `instagram/voice.md` (cloud sessions reset the home folder).
At the start of any ig-* task: if `~/.claude/instagram/voice.md` is missing, copy `instagram/` into
`~/.claude/instagram/`, and after editing voice.md / swipe.md / log.md copy them back to `instagram/`
so they are saved in git.
