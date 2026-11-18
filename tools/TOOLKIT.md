# Kami free toolkit

The owner wants everything free, with no paid services or usage limits. Do not install or suggest paid
generators (Higgsfield, muapi, OpenArt, paid ElevenLabs runs) unless the owner asks by name.
`bash tools/setup.sh` installs everything below and is safe to re-run; the cloud environment runs it
at the start of each new session. If a tool is missing, run it instead of asking the owner.

| Job | Tool | Notes |
|---|---|---|
| Posts, carousels, stories (1080x1350 / 1080x1920) | `templates/*.py` + `node templates/render.js` | Theme: see «قرارات صاحب المجلد» in SESSION_HANDOFF.md |
| Motion video, reels, kinetic Arabic type | khaam-motion skill, HyperFrames (`hyperframes` skill) | HTML -> MP4, runs on CPU |
| Arabic voiceover | `edge-tts --proxy "$HTTPS_PROXY" --voice ar-BH-LailaNeural` (or ar-BH-AliNeural, ar-SA-*) | `--proxy` is required here |
| Captions / word timing | `hyperframes transcribe <file> --model small --language ar` | check brand names by hand |
| Cut out a product or person | `hyperframes remove-background <in> -o <out.png>` | works on images and video |
| Product mockups with the real logo | Three.js renders (see `templates/packaging_carousel.py` history) | no AI text errors |
| Business leads from Google Maps | `google-maps-scraper` skill / command | |
| Download a reference video | `yt-dlp <url>` | TikTok works. Instagram needs a logged-in cookies file (anonymous access is blocked); otherwise ask the owner to drop the file in the chat. YouTube blocks cloud servers. |

No GPU here: free AI image/video generation is not good enough on this machine. For photoreal shots
use the free daily ElevenLabs quota only when the owner asks, or render mockups.
In this cloud session Node needs `NODE_USE_ENV_PROXY=1` for downloads (tools/setup.sh sets it).
