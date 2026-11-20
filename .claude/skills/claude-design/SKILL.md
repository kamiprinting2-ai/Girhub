---
name: claude-design
description: Work like Anthropic's Claude Design tool - an opinionated, accessibility-aware, anti-AI-slop designer that builds HTML/CSS/SVG design artifacts (pages, prototypes, decks, posters, motion). Use for any new design, UI, prototype, deck or visual when quality and taste matter; read system-prompt.md first, then chain the claude-design-* procedure skills.
---

# Claude Design (open-source recreation)

Source: github.com/Trystan-SA/claude-design-system-prompt (MIT, commit 3c3ddb0), a reverse-engineered
version of the system prompt behind Anthropic's Claude Design, plus 14 procedure skills.

**How to use:** read `system-prompt.md` in this folder (20 chapters: workflow, content and aesthetic discipline,
hierarchy, accessibility, interaction, system thinking) and follow it for the whole task. Then use the
procedure skills when the task matches:
- `claude-design-accessibility-audit`
- `claude-design-ai-slop-check`
- `claude-design-component-extract`
- `claude-design-design-system-extract`
- `claude-design-discovery-questions`
- `claude-design-frontend-aesthetic-direction`
- `claude-design-generate-variations`
- `claude-design-hierarchy-rhythm-review`
- `claude-design-interaction-states-pass`
- `claude-design-make-a-deck`
- `claude-design-make-a-prototype`
- `claude-design-make-tweakable`
- `claude-design-polish-pass`
- `claude-design-wireframe`

Typical flows: `discovery-questions -> frontend-aesthetic-direction -> wireframe -> make-a-prototype -> polish-pass`;
brand-aware: `design-system-extract -> generate-variations -> make-tweakable -> polish-pass`.

> **Kami Printing note:** for any Kami design the brand rules in CLAUDE.md / brand-style memory win over this skill's taste defaults (sage gradient, Readex Pro + IBM Plex Sans Arabic, Bahraini dialect). Save every result to Google Drive (Kami_Printing/المشروع/<project>/) and make the editable Canva copy.
