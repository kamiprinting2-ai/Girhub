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

## Instagram skills (ig-*)
The ig-* skills look for the user's voice profile at `~/.claude/instagram/voice.md`.
In this repo the voice profile lives at `instagram/voice.md` (cloud sessions reset the home folder).
At the start of any ig-* task: if `~/.claude/instagram/voice.md` is missing, copy `instagram/` into
`~/.claude/instagram/`, and after editing voice.md / swipe.md / log.md copy them back to `instagram/`
so they are saved in git.
