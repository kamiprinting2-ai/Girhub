---
name: quicky-delegation
description: Delegate routine, no-judgment tasks to the Quicky subagent (haiku); keep design, writing and taste-based work for the main model
source: Drive 00_MASTER_CONTROL/Claude_Master_Memory/memory/quicky-delegation.md (copied 2026-11-19)
---

On 2026-11-15 the user asked for a subagent named **Quicky** that runs on haiku. Its job is routine tasks that need no thinking or taste, and it reports the result back to the model that called it. The definition is in `.claude/agents/quicky.md` in this repo (and `08_AI_SKILLS_AND_AGENTS/Agents/quicky.md` in Drive).

**Why:** The user wants mechanical work done cheaply and quickly, with the main model kept for work that needs judgment.

**How to apply:** For mechanical steps, call it with the Agent tool and `subagent_type: "Quicky"`. Examples: copying, moving or renaming files, listing folders, running a known command and reading the output, exact find-and-replace, checking that files exist, updating index rows with given text. Keep design, copy in Bahraini dialect, brand decisions and anything needing taste in the main model. Check what Quicky returns before telling the user. Related: design-file-workflow, brand-style.
