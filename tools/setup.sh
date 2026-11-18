#!/usr/bin/env bash
# Kami free toolkit: installs everything the project uses, with no paid services.
# What to use for which job: tools/TOOLKIT.md
# Safe to run again (skips what is already there). Run: bash tools/setup.sh
# Also run automatically by the cloud environment's setup script at the start of each new session.
set -u
log() { echo "[kami-setup] $*"; }

# Node downloads must go through the session proxy (no direct DNS in cloud sessions).
PROFILE_LINE='export NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt NODE_NO_WARNINGS=1'
if [ -f /root/.ccr/ca-bundle.crt ]; then
  eval "$PROFILE_LINE"
  grep -qxF "$PROFILE_LINE" ~/.bashrc 2>/dev/null || echo "$PROFILE_LINE" >> ~/.bashrc
fi

# 1. HyperFrames: HTML -> MP4 video, plus free local tools (cutouts, transcripts, beats, grading)
command -v hyperframes >/dev/null || { log "installing hyperframes"; npm install -g hyperframes >/dev/null 2>&1; }
[ -d ~/.claude/skills/hyperframes ] || { log "installing hyperframes skills"; (cd /tmp && hyperframes skills update >/dev/null 2>&1); }

# 2. Background removal runtime for HyperFrames (CPU build; the CUDA download does not exist here)
ORT=/root/.cache/hyperframes/optional/onnxruntime-node@1.21.1
[ -d "$ORT/node_modules/onnxruntime-node" ] || { log "installing onnxruntime (CPU)"; npm install onnxruntime-node@1.21.1 --onnxruntime-node-install-cuda=skip --prefix "$ORT" >/dev/null 2>&1; }

# 3. Arabic voiceover (free Microsoft Edge voices) and video downloader
python3 -m pip install -q -U edge-tts yt-dlp >/dev/null 2>&1 && log "edge-tts + yt-dlp ready"

# 4. Google Maps scraper (business leads), built from source
if ! command -v google-maps-scraper >/dev/null && command -v go >/dev/null; then
  log "building google-maps-scraper"
  mkdir -p /home/user/tools && cd /home/user/tools
  [ -d google-maps-scraper ] || git clone -q --depth 1 https://github.com/gosom/google-maps-scraper
  (cd google-maps-scraper && go build -o /usr/local/bin/google-maps-scraper . >/dev/null 2>&1)
  mkdir -p ~/.claude/skills && cp -r google-maps-scraper/skills/google-maps-scraper ~/.claude/skills/ 2>/dev/null
fi

# 5. Remotion skills (React videos; the Remotion package itself installs per project) and video-use (edit footage by chat)
ls ~/.claude/skills 2>/dev/null | grep -q '^remotion-create$' || { log "installing remotion skills"; (cd /tmp && npx -y skills add remotion-dev/skills -g -y >/dev/null 2>&1); }
mkdir -p /home/user/tools
[ -d /home/user/tools/video-use ] || GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 https://github.com/browser-use/video-use /home/user/tools/video-use
if [ -d /home/user/tools/video-use ]; then
  (cd /home/user/tools/video-use && pip install -q -e . >/dev/null 2>&1)
  mkdir -p ~/.claude/skills && ln -sfn /home/user/tools/video-use ~/.claude/skills/video-use
fi

log "versions:"
hyperframes --version 2>/dev/null | sed 's/^/  hyperframes /'
edge-tts --version 2>/dev/null | head -1 | sed 's/^/  /'
yt-dlp --version 2>/dev/null | sed 's/^/  yt-dlp /'
command -v google-maps-scraper >/dev/null && echo "  google-maps-scraper ok"
exit 0
