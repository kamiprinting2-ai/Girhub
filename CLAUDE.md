# Project notes for Claude

## 0. Google Drive is the workspace (standing rule, always applies)
The owner's standing instruction (2026-11-19): **all files, designs, videos, memory and
conversations live in Google Drive (Kami account).** Do not ask again in any session.

- This GitHub repo is only a launcher for cloud sessions (skills + scripts). Do not deliver work here.
- Every deliverable (design, video, PDF, PNG, caption, document) is uploaded to Drive with the
  Google Drive connector. Do not commit new deliverables to this repo.
- At the **start** of every session read `My Drive/CLAUDE.md`
  (file ID `1Tqk4YFDExKTWkMPTKas2WjDHEntUvP0r`) and follow it: open the memory sheet
  **CLAUDE_MASTER_MEMORY_AND_ACTIVITY_LOG** (`1u9QXeksiXo_NjkJ_vmy69KSKR9wHPrcQINmwFPj2lPI`),
  read `1_MASTER_DASHBOARD`, the last rows of `2_SESSION_LOG` and the open rows of `4_TASK_TRACKER`.
- At the **end** of every session: append a `2_SESSION_LOG` row (next S-NNNN), update the other
  tabs that changed, read them back, and save a readable Markdown summary of the conversation to
  `00_MASTER_CONTROL/Session_Reports/conversations/` (folder ID `1gq5LKjHRuqNf5luoelo5jafYqd-UesT5`).
- Search Drive before creating files. Never overwrite or delete originals; revisions go in `تعديل N`.
- Reply in Arabic (Bahraini dialect for marketing and design text).

| Where | Drive folder ID |
|---|---|
| Kami designs: `Kami_Printing/المشروع/<اسم التصميم>/` | `1AtcmoSNbGBe-mPFtxyAD44M1YploQe3D` |
| Kami_Printing root (`فهرس-التصاميم.md`, `امثلة`, `فيديوهاتي`) | `17TbJv_LDf2wvtpPiZze-1mPkIiGQuwTL` |
| Temporary / draft designs: `Kami_Printing/متفرقات/` | `172u6fZtjZ3DDUPNKFGpU54OfygfuVYvc` |
| Ready-to-post videos: `Kami_Printing/فيديوهاتي/` | `1h1DwBrpgIUC126kc2eMeRyTIi1LP_xdE` |
| 00_MASTER_CONTROL (memory, instructions, reports) | `1w9jdWBFw_5afzl6fzciywpIjedKknITY` |
| 99_INBOX / Unsorted_Files | `1dYVLXBACaViydVct19036_QZnMsyN_0c` |

Upload a local file with `create_file` and `base64Content` set to a file reference
(`sha256:<hash>:<absolute path>`), `disableConversionToGoogleType: true`.

## 1. Memory (copied from Drive `00_MASTER_CONTROL/Claude_Master_Memory/memory/`)
These files load into every session. If a rule changes, update the Drive copy and this copy together.

@.claude/memory/drive-workspace.md
@.claude/memory/reply-in-arabic.md
@.claude/memory/bahraini-dialect.md
@.claude/memory/brand-style.md
@.claude/memory/design-file-workflow.md
@.claude/memory/decor-print-style.md
@.claude/memory/quicky-delegation.md

## 2. Standing decisions (from the memory sheet `5_DECISION_LOG`)
- D-001 New designs copy the green «المشروع» post style (sage gradient, Readex Pro + IBM Plex Sans Arabic, 4-point stars).
- D-002 All marketing text in Bahraini dialect (no سوا/لمين).
- D-003 Times written in English with AM/PM.
- D-004 Each design in its own folder; revisions saved as تعديل 1/2/3; editable Canva copy.
- D-005 Routine no-taste tasks go to the Quicky subagent (haiku).
- D-006 Reels overlay: logo without background (cut-out).
- D-010 Opening-hours vinyl: 30x30 cm, wider «للطباعة», phone icon + brand stars.
- D-011 Decor prints use the retro gallery-wall poster style.
- D-012 Wall prints use logo colors only (sage, light pink, cream, dark green).
- D-013 Receipt wall print: no striped frame; torn-edge receipt on plain pink.
- D-014 Framed wall prints printed matte 250–300gsm (under review).
- D-015 / D-021 / D-024 / D-025 Google Drive is the only workspace and source of truth for every session; the memory sheet is Claude's memory; never ask again.
- D-016 Never delete or move original files during migration.
- D-026 Temporary designs go in `Kami_Printing/متفرقات`.

The sheet is the live source: read `5_DECISION_LOG` for new decisions added after this list.

## Instagram skills (ig-*)
The ig-* skills look for the user's voice profile at `~/.claude/instagram/voice.md`.
In this repo the voice profile lives at `instagram/voice.md` (cloud sessions reset the home folder).
At the start of any ig-* task: if `~/.claude/instagram/voice.md` is missing, copy `instagram/` into
`~/.claude/instagram/`, and after editing voice.md / swipe.md / log.md copy them back to `instagram/`
so they are saved in git.
