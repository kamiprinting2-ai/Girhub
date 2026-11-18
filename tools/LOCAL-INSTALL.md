# تثبيت الأدوات على جهازك (Mac / Windows / Linux)

افتح Terminal (أو PowerShell على ويندوز) والصق السطور بالترتيب. المطلوب قبل: Node 22 أو أحدث، و Python 3.10 أو أحدث، و ffmpeg.

```bash
# 0) مرة وحدة: ffmpeg
brew install ffmpeg            # Mac
winget install Gyan.FFmpeg     # Windows

# 1) HyperFrames: الفيديو من HTML + قص الخلفية + تفريغ الكلام (Whisper)
npm install -g hyperframes
hyperframes skills update

# 2) مهارات Remotion (١٢ مهارة)
npx skills add remotion-dev/skills -g -y

# 3) video-use: مونتاج الفيديو بالدردشة
git clone https://github.com/browser-use/video-use ~/Developer/video-use
cd ~/Developer/video-use && pip install -e .
mkdir -p ~/.claude/skills && ln -sfn ~/Developer/video-use ~/.claude/skills/video-use
#   ويندوز: بدل السطر الأخير  mklink /D "%USERPROFILE%\.claude\skills\video-use" "%USERPROFILE%\Developer\video-use"

# 4) تنزيل الفيديوهات وصوت عربي مجاني
pip install -U yt-dlp edge-tts
```

بعدها افتح Claude Code في مجلد مشروعك، وأي مهارة تظهر تلقائي.
ملاحظة: video-use يحتاج مفتاح ElevenLabs للتفريغ (لا ترسله في الدردشة، حطه في ملف .env داخل مجلد video-use). البديل المجاني: `hyperframes transcribe`.
Editly ما ثبّتناه: ما يشتغل على Node 22.
