---
name: pollinations
description: Free AI image generation (and text/audio) through Pollinations (github.com/pollinations/pollinations, MIT) - the free replacement for OpenArt image work. Use when the owner wants an AI-generated image, background, product scene, mockup, sticker art or concept image and no paid generator is needed. Video generation on Pollinations is paid-only, so for video use the openmontage skill.
---

# Pollinations (free OpenArt replacement for images)

- Open source: github.com/pollinations/pollinations (MIT). API: `https://gen.pollinations.ai`.
- Needs a **free** account key (sign in at https://enter.pollinations.ai with GitHub/Google → Keys → create a
  secret key `sk_…`). The free account gets a daily pollen allowance; models marked free-ok run on it.
- Cloud sessions: the key is saved as a network credential for `gen.pollinations.ai` (the proxy injects it),
  so requests can send `Authorization: Bearer dummy`. PC: set the env var `POLLINATIONS_API_KEY`.
- MCP: the repo `.mcp.json` adds the hosted server `https://gen.pollinations.ai/mcp/pollinations`.

## Free image models (checked 2026-11-20 via /image/models; re-check, the list changes)
Best quality: `black-forest-labs/flux.1.1-pro` (256–1440 px, ×32, ≤1.6 MP) · `black-forest-labs/flux.2-flex`
(×16) · `microsoft/mai-image-2.7` / `-flash` (≥768 px, ×16) · `black-forest-labs/flux.1-kontext-pro` (edit with
a reference image). Fast drafts: `black-forest-labs/flux.1-schnell` (`flux`), `tongyi-mai/z-image-turbo`,
`black-forest-labs/flux.2-klein-4b`. All video models are paid-only.

## Generate an image
```bash
curl -sL -H "Authorization: Bearer ${POLLINATIONS_API_KEY:-dummy}" \
  -o out.jpg "https://gen.pollinations.ai/image/$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "PROMPT")?model=black-forest-labs/flux.1.1-pro&width=1088&height=1344&seed=7&nologo=true"
```
List models: `curl -s https://gen.pollinations.ai/image/models`. Keep `seed` fixed to make a variation repeatable.

## Rules
- Kami brand: realistic people only, Gulf/Arab look, no cartoon people; never write the shop address; text in
  the image is unreliable — add Arabic text afterwards in the design (HTML/Canva), not in the prompt.
- Save every generated image to Google Drive (Kami → `Kami_Printing/المشروع/<project>/المصدر/`; drafts →
  `متفرقات`), and say which model and seed made it.
