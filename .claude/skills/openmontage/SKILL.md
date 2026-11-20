---
name: openmontage
description: Produce complete videos with OpenMontage, the open-source agentic video production system (12 pipelines, 100+ tools, Remotion/HyperFrames rendering, free local narration with Piper). Use when the owner asks for an explainer, ad, reel, montage, documentary-style edit or any finished video produced from an idea, script or existing footage.
---

# OpenMontage (github.com/calesthio/OpenMontage, AGPL-3.0)

OpenMontage is a full project you run, not a single prompt. It is stored in Google Drive and installed on the
machine that does the work.

## Where it lives
- Drive package (source of truth): `My Drive/الملفات الرئيسية/09_TEMPLATES_AND_SYSTEMS/OpenMontage/`
  - `OpenMontage.zip.part00…06` + `OpenMontage.zip.sha256` (source snapshot, demo videos removed)
  - `install-openmontage.ps1` (Windows PC) · `install-openmontage.sh` (cloud/Linux/macOS) · `اقرأني.md`
- Runnable copy: PC `%USERPROFILE%\OpenMontage` · cloud session `~/OpenMontage`
  (the Python venv and node_modules are too heavy to keep inside Drive).

## Use it
1. Install if missing:
   - PC: run `install-openmontage.ps1` from the Drive folder (or `-FromGit` for the newest version).
   - Cloud: `bash install-openmontage.sh` (download it from the Drive folder) or clone
     `https://github.com/calesthio/OpenMontage` into `~/OpenMontage`, then the same setup steps.
2. Work inside the OpenMontage folder and read its `AGENT_GUIDE.md` before anything else; it routes the request
   to the right pipeline.
3. Free path first: Piper TTS (local), Remotion/HyperFrames animation, royalty-free stock. Paid providers
   (FAL, ElevenLabs, Kling, Runway…) need keys in `.env` — never invent keys; ask the owner.
4. Kami work keeps the brand rules (sage palette, Readex Pro + IBM Plex Sans Arabic, Bahraini dialect) and goes
   through `kami-reviewer` before delivery.
5. Save the result to Google Drive: Kami videos → `Kami_Printing/فيديوهاتي` or the project folder; other
   projects → their folder in `الملفات الرئيسية`. Files over ~3 MB can't be uploaded from a cloud session:
   upload sources + a preview and deliver the video in chat.
