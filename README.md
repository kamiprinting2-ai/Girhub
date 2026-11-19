# Design & Social Media Skills for Claude Code

مجموعة سكلز (Skills) للتصميم والسوشيال ميديا، منزّلة من GitHub ومثبّتة في `.claude/skills/`.
Claude Code يحمّلها تلقائياً لما تشتغل داخل هذا المجلد.

## المصادر / Sources

| المجموعة | المصدر | الرخصة | السكلز |
|---|---|---|---|
| **Canva** (رسمي) | [canva-sdks/canva-skills](https://github.com/canva-sdks/canva-skills) | Apache-2.0 | `edit-design`, `brand-check`, `get-design-feedback`, `implement-feedback`, `resize-for-social-media`, `bulk-create`, `canva-cli` |
| **OpenArt** (رسمي) | [OpenArt-AI/skills](https://github.com/OpenArt-AI/skills) | MIT | `ad-variation`, `ad-remake`, `hook-variants`, `performance-ads`, `ugc`, `tvc`, `pgc`, `talking-head`, `product-listing-video` |
| **Instagram Agent Skill** | [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) | MIT | `ig-reel`, `ig-carousel`, `ig-caption`, `ig-story`, `ig-plan`, `ig-viral`, `ig-audit`, `ig-profile`, `ig-comment`, `ig-reply`, `ig-dm`, `ig-repurpose`, `ig-human` |
| **Metricool** | [Purple-Horizons/metricool-cli](https://github.com/Purple-Horizons/metricool-cli) | MIT (package.json) | `metricool` (+ الـ CLI في `tools/metricool-cli`) |
| **Metricool setup** | [gerritschaefer-hash/metricool-skill](https://github.com/gerritschaefer-hash/metricool-skill) | MIT | `metricool-setup` |
| **Anthropic design** (رسمي) | [anthropics/skills](https://github.com/anthropics/skills) | Apache-2.0 | `canvas-design`, `frontend-design`, `theme-factory`, `brand-guidelines`, `algorithmic-art` |

نسخ الرخص موجودة في `licenses/` وفي مجلد كل سكل من Anthropic.

## الإعداد / Setup

### Canva و OpenArt (MCP)
- **Canva:** مربوط من حساب claude.ai (Settings → Connectors → Canva)، فيشتغل في كل السشنات بنفس الحساب (السحابة والكمبيوتر والجوال). أدواته اسمها `mcp__Canva__*`. لا تضيفه في `.mcp.json`، لأن النسخة اللي هناك تطلب تسجيل دخول منفصل في كل سشن.
- **OpenArt:** ملف `.mcp.json` يضيف `https://mcp.openart.ai/mcp`. أول مرة يطلب منك Claude Code تسجيل الدخول (OAuth). شغّل `/mcp` للتحقق.

### Metricool
```bash
cd tools/metricool-cli
npm install
npm link            # يخلي أمر `metricool` متاح
```
ثم ضيف في `.env` (لا ترفعه على git):
```
METRICOOL_USER_TOKEN=...
METRICOOL_USER_ID=...
METRICOOL_BLOG_ID=...
```
اسأل Claude: "set up Metricool API" وسكل `metricool-setup` يمشي معك خطوة بخطوة.
> ملاحظة: الـ API الخاص بـ Metricool يحتاج خطة Advanced أو أعلى.

### Instagram skills
بعض السكلز فيها سكربتات Python بسيطة (`hookscore.py`, `caption.py`, `detect.py`...) تشتغل بـ Python 3 بدون مكتبات إضافية.

## أمثلة / Examples
- "سوّ لي Reel عن ..." → `ig-reel`
- "Resize this Canva design for Instagram story and TikTok" → `resize-for-social-media`
- "Make 5 UGC ad variations for my product" → `ugc` (OpenArt)
- "شنو أفضل وقت أنشر فيه على إنستغرام؟" → `metricool`

## Instagram voice profile
املأ `instagram/voice.md` بأسلوبك (أو أرسل لـ Claude ثلاث Reels من حسابك وقل "write my voice.md from these").
كل سكلز `ig-*` تقرأ هذا الملف عشان الكتابة تطلع بصوتك أنت.
