# Project notes for Claude

## 0. Google Drive is the workspace (standing rule, always applies)
> **قاعدة صاحب المحل (مكتوبة وثابتة):** كل الملفات والتصاميم والفيديوهات والمشاريع تكون في جوجل درايف.
> أي شي ينسوى في أي جلسة ينرفع للدرايف في نفس الجلسة، بدون ما نسأل. GitHub مو مكان التسليم.

The owner's standing instruction (2026-11-19, D-025): **every file, design, project, video, memory and
conversation lives in Google Drive (Kami account).** This is a permanent written rule for every session,
device and environment. Do not ask again, and do not keep work only on this machine or in this repo.
- Kami designs and projects → `My Drive/Kami_Printing/المشروع/<اسم المشروع>/` (drafts in `متفرقات/`).
- Any other project (personal, other businesses, videos, montages, documents) → its own folder inside
  `My Drive/الملفات الرئيسية/` in the matching 00–99 folder (unsure → `99_INBOX/Unsorted_Files/<اسم المشروع>/`).
- A file too big for the cloud connector (~3 MB per call, e.g. long videos): upload its sources and a
  preview, deliver the file in chat, and say so; the owner said videos need not go to Drive.

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

**Drive layout (D-028, 2026-11-19).** My Drive root holds only two working folders plus Claude's files:
```
My Drive/
├── Kami_Printing/          ← التصاميم (designs) — ID 17TbJv_LDf2wvtpPiZze-1mPkIiGQuwTL
├── الملفات الرئيسية/        ← the main files — ID 1DIxk7dulCzuQRxeOTRySAKVV6wHQwFL7
│   ├── 00_MASTER_CONTROL … 09_TEMPLATES_AND_SYSTEMS, 10_ARCHIVE, 99_INBOX
│   └── 01_BUSINESS_PROJECTS (Business_Plans, Future_Projects, Servix)
├── CLAUDE.md               ← must stay at the root (Claude loads it from there)
└── .claude/                ← must stay at the root (skills, agents, instagram voice)
```
Every path in these notes written as `00_MASTER_CONTROL/…`, `08_AI_SKILLS_AND_AGENTS/…`, `09_…`, `10_ARCHIVE`,
`99_INBOX/…` means `My Drive/الملفات الرئيسية/<that path>`. Kami work is `My Drive/Kami_Printing/…`.
Never put a new top-level folder in My Drive: designs go in Kami_Printing, everything else in الملفات الرئيسية.
Folder IDs did not change in the move, so the IDs below still work.

| Where | Drive folder ID |
|---|---|
| Kami designs: `Kami_Printing/المشروع/<اسم التصميم>/` | `1AtcmoSNbGBe-mPFtxyAD44M1YploQe3D` |
| Kami_Printing root (`فهرس-التصاميم.md`, `امثلة`, `فيديوهاتي`) | `17TbJv_LDf2wvtpPiZze-1mPkIiGQuwTL` |
| Temporary / draft designs: `Kami_Printing/متفرقات/` | `172u6fZtjZ3DDUPNKFGpU54OfygfuVYvc` |
| Ready-to-post videos: `Kami_Printing/فيديوهاتي/` | `1h1DwBrpgIUC126kc2eMeRyTIi1LP_xdE` |
| 00_MASTER_CONTROL (memory, instructions, reports) | `1w9jdWBFw_5afzl6fzciywpIjedKknITY` |
| 99_INBOX / Unsorted_Files | `1dYVLXBACaViydVct19036_QZnMsyN_0c` |

**Canva (D-029):** Canva is connected at the claude.ai account level (connector «Canva», tools `mcp__Canva__*`,
load them with ToolSearch). It works in every session on this account, so make the editable Canva copy of every
design with it (rule D-004). Do not add a `canva` server to `.mcp.json`: that duplicate needs a separate login per
session and always shows as unauthenticated in cloud sessions. If the connector ever fails, tell the owner to
reconnect it in claude.ai → Settings → Connectors.

Upload a local file with `create_file` and `base64Content` set to a file reference
(`sha256:<hash>:<absolute path>`), `disableConversionToGoogleType: true`.

## Creative tools (D-030, 2026-11-20) — all from GitHub, all stored in Drive
| Tool | What for | Skill | Drive |
|---|---|---|---|
| **OpenMontage** (calesthio/OpenMontage, AGPL-3.0) | full video production from an idea/script/footage | `openmontage` | package + installers in `09_TEMPLATES_AND_SYSTEMS/OpenMontage` (`1RhoHwWqDu-ATX_sF1ySnsIc9d0F1XZwk`) |
| **Claude Design** (Trystan-SA/claude-design-system-prompt, MIT) | designer system prompt + 14 design procedures | `claude-design`, `claude-design-*` | `.claude/skills` + `Installed_Skills` |
| **Pollinations** (pollinations/pollinations, MIT) — free replacement for OpenArt images | AI images (free daily tier with a free key); its video models are paid | `pollinations` + `.mcp.json` server `pollinations` | `.claude/skills` + `Installed_Skills` |
OpenArt stays available but is paid; prefer Pollinations for images and OpenMontage (Piper + Remotion/HyperFrames) for video.

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
- D-028 My Drive has two working folders: `Kami_Printing` (designs, at the root) and `الملفات الرئيسية` (all 00–99 folders). `CLAUDE.md` and `.claude` stay at the root.
- D-027 Every skill or agent is also installed in Drive (`My Drive/.claude/skills` + `08_AI_SKILLS_AND_AGENTS/Installed_Skills`; account plugins as zips in `Installed_Skills/Account_Plugins`). When a new skill is added anywhere, copy it to Drive in the same session.

The sheet is the live source: read `5_DECISION_LOG` for new decisions added after this list.

## Design index (فهرس-التصاميم.md) — the ORIGINAL is on Google Drive
The owner made the Drive file the original and gave standing permission to edit it automatically,
every time, without asking. It lives in Drive folder `17TbJv_LDf2wvtpPiZze-1mPkIiGQuwTL`
(Kami_Printing/المشروع/). Its file id changes on every save (the owner's local Claude also re-creates it),
so always find it by: `search_files` query `parentId = '17TbJv_LDf2wvtpPiZze-1mPkIiGQuwTL' and title = 'فهرس-التصاميم.md'`.
The repo copy `فهرس-التصاميم.md` is a mirror.

1. **Start of every design/video task:** find the Drive file, `download_file_content` it, then
   `python3 tools/update_index.py --pull <downloaded path>`. Follow section 1 (style: sage gradient
   #B2BF9D→#9CAB86 with two stars, Readex Pro 700 + IBM Plex Sans Arabic, sizes, no «في» in Readex titles).
2. **After every new design, video or edit:** pull again (step 1, the owner may have edited meanwhile), then
   edit the owner's sections directly: add the design to the repo-designs section (section 6) and a row at the
   top of the log section (التاريخ | التصميم | التعديل | المجلد), short, Bahraini dialect, same style as
   existing rows. Add new folders to `tools/design_index.json`, run `python3 tools/update_index.py`.
3. **Save to Drive:** the Drive tools can't overwrite content, so: `get_file_metadata` on the id you pulled;
   if `modifiedTime` changed, go back to step 2. Otherwise `create_file` the repo file into that folder
   (title `فهرس-التصاميم.md`, contentMimeType text/markdown, disableConversionToGoogleType true), and
   only after it succeeds `trash_file` the old id. Trash nothing else in Drive. Then commit the mirror.
- The last section (between `AUTO:START` / `AUTO:END`) is generated by the script (file counts, dates,
  undescribed folders); a Stop hook refreshes it. Never hand-edit it.

## Every design goes to the Kami Drive (owner's standing rule, 2026-11-19)
All images, designs and projects must also live in the owner's Google Drive under `Kami_Printing/المشروع/`
(folder id `1AtcmoSNbGBe-mPFtxyAD44M1YploQe3D`), not only in this repo or in chat. This applies to every
new design and every edit, without being asked:
- One Drive folder per design directly in `المشروع/`, named in Arabic like the owner's own (e.g. `أكواب وصحون`,
  `كوب الخريجين`). Search before creating and reuse a folder that already exists.
- The original goes in the folder itself; each edit goes in a `تعديل N` subfolder (never overwrite or trash files there).
  Include the caption (`كابشن.txt`) and a preview when there is one.
- Upload limit from a cloud session is ~3 MB per file. For a bigger file: images without transparency as high-quality
  JPG; transparent PNGs as a 256-colour palette PNG (say so in the index); file sets as several zips under 3 MB.
  Never skip a file silently; if something still cannot go up, tell the owner which file and why.
- Write the Drive path in the design's row in فهرس-التصاميم.md.

## Instagram skills (ig-*)
The 13 ig-* skills (Instagram Agent Skill, MIT) are installed in three places, all identical:
this repo `.claude/skills/ig-*`, Drive `My Drive/.claude/skills/ig-*` (active for the Drive workspace),
and Drive `08_AI_SKILLS_AND_AGENTS/Installed_Skills/ig-*` (library).

The skills look for the user's voice profile at `~/.claude/instagram/voice.md`.
The master copy is in Drive: `My Drive/.claude/instagram/` (folder `1bG1hnpLX3nTB-GxL6rUMFsuko9ggFQwd`:
voice.md, log.md, content/, reels/). A mirror lives in this repo at `instagram/`.
At the start of any ig-* task: if `~/.claude/instagram/voice.md` is missing, copy `instagram/` into
`~/.claude/instagram/`. After editing voice.md / swipe.md / log.md, upload the changed file to the Drive
folder above (Drive is the source of truth) and copy it back to `instagram/` here.
Agents: `kami-reviewer` (QA before delivery) and `Quicky` (routine work) are in `.claude/agents/` and in
Drive `My Drive/.claude/agents/` + `08_AI_SKILLS_AND_AGENTS/Agents/`.
