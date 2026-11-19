---
name: drive-workspace
description: Google Drive (Kami account) is the workspace and source of truth for every session; read and update the memory sheet at the start and end of every session
source: Drive 00_MASTER_CONTROL/Claude_Master_Memory/memory/drive-workspace.md (copied 2026-11-19)
---

On 2026-11-19 the user made Google Drive (the Kami account) their permanent workspace, "repository" and source of truth. On the same day they confirmed for cloud sessions too: «جميع الملفات والمحادثات وكلشي يكون في جوجل درايف وما يحتاج اخبرك مره ثانيه» (decision D-025).

- **Default folder:** on the PC, `G:\My Drive` is the default working folder. Its root `CLAUDE.md` plus `.claude\skills` and `.claude\agents` make it a complete Claude project.
- **GitHub:** this repo (kamiprinting2-ai/Girhub) is only the launcher for cloud sessions. Deliverables never stay here; they go to Drive.
- **Memory sheet:** CLAUDE_MASTER_MEMORY_AND_ACTIVITY_LOG, ID `1u9QXeksiXo_NjkJ_vmy69KSKR9wHPrcQINmwFPj2lPI`, in 00_MASTER_CONTROL (`1w9jdWBFw_5afzl6fzciywpIjedKknITY`). Tabs 1_MASTER_DASHBOARD … 7_CHANGELOG.
- **Protocol:** the Drive doc Operating_Instructions (`1Apz092cStCcQX5r0lgxVgPOM5BrC1XX81dbpGEs4J2U`).
- **Kami_Printing folder:** `17TbJv_LDf2wvtpPiZze-1mPkIiGQuwTL`.

**Why:** The user wants continuity between sessions, devices and accounts without rereading history, and every file, skill and conversation kept in Drive.

**How to apply:**
- **Start of session:** read the dashboard, the last Session Log rows, the relevant Project Memory row and the open tasks, using the Google Sheets tools.
- **During the session:** search Drive before creating anything. Save deliverables directly in the Drive folders (see design-file-workflow) and to Canva.
- **End of session:** append a Session Log row (S-NNNN), and update Project Memory, Task Tracker, Decision Log, File Registry, Changelog and the dashboard. Read the rows back to verify. Save a readable Markdown summary of the conversation to `00_MASTER_CONTROL/Session_Reports/conversations/` (`1gq5LKjHRuqNf5luoelo5jafYqd-UesT5`).
- **Uploads:** on the PC, Google Drive for desktop mounts My Drive at `G:\My Drive`; writing a file there uploads it. In a cloud session use the Drive connector (`create_file`, `base64Content` = `sha256:<hash>:<absolute path>`, `disableConversionToGoogleType: true`). The connector carries about 3 MB per call, so larger files (videos) are uploaded from the PC: tell the user and log a task.
- **Helper scripts:** `09_TEMPLATES_AND_SYSTEMS/kami-tools/` holds trace.py, pdftext.py and defrag.py.
- **HyperFrames:** the 9 official skills live in Drive at `My Drive/.claude/skills/`. Projects live in `09_TEMPLATES_AND_SYSTEMS/hyperframes/<project>/` (kami-reels). Update steps: `08_AI_SKILLS_AND_AGENTS/Installed_Skills/HYPERFRAMES_SKILLS_SOURCE.md`.
- **One environment:** Google Drive is the ONLY environment («بس بيئة وحده وهي جوجل درايف»). Don't create new work in local folders (Desktop\claude) or keep it only in this repo.
- **Auto-sync (PC only):** the scheduled task «Kami Drive Sync» runs every 30 minutes and at logon, copy-only (never deletes): session transcripts and digests → 00_MASTER_CONTROL/Session_Reports; auto-memory both ways with 00_MASTER_CONTROL/Claude_Master_Memory/memory; skills and agents → 08 and `My Drive/.claude/`; Desktop\claude → Kami_Printing; Downloads → 99_INBOX. The script must stay UTF-8 with BOM.
- Never delete original files.
- **Kami work:** use the kami-design-workflow skill (Drive: `08_AI_SKILLS_AND_AGENTS/Custom_Skills/kami-design-workflow/SKILL.md`; read it with the connector in a cloud session).
