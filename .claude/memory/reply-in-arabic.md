---
name: reply-in-arabic
description: Every reply to the user must be in Arabic, always (summaries, technical reports, wrap-up recaps, questions). Never switch to English
source: Drive 00_MASTER_CONTROL/Claude_Master_Memory/memory/reply-in-arabic.md (copied 2026-11-19)
---

On 2026-11-19 the user corrected me twice in a row: «بالعربي» and then «بالعربي دايما». That came after I wrote a summary and a technical answer in English, even though CLAUDE.md already says to reply in Arabic.

**Why:** The user reads Arabic. English replies are useless to them, even when the work itself (code, paths, sheet entries) is technical or in English.

**How to apply:**
- Write every user-visible message in Arabic, using easy Bahraini/Gulf wording. That covers:
  - progress updates
  - final summaries
  - the wrap-up recap and question
  - button labels
  - questions in the AskUserQuestion tool
  - the task list items
- File paths, command names and tool names can stay as they are, inside Arabic sentences.
- The Drive memory sheet and code may stay in English. Only what the user reads must be Arabic.
- Marketing text follows bahraini-dialect.
