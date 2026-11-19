---
name: design-file-workflow
description: How to organize design files, reference examples and revisions, directly in Google Drive (01_BUSINESS_PROJECTS/Kami_Printing)
source: Drive 00_MASTER_CONTROL/Claude_Master_Memory/memory/design-file-workflow.md (copied 2026-11-19)
---

From 2026-11-19 on, the design workspace lives in Google Drive: `My Drive/01_BUSINESS_PROJECTS/Kami_Printing/` (call it KAMI, folder ID `17TbJv_LDf2wvtpPiZze-1mPkIiGQuwTL`). The old `C:\Users\user\Desktop\claude` is a legacy local copy. Don't save new work there, and don't leave deliverables only in this GitHub repo.
- `KAMI/امثلة/` holds the user's reference examples, one or more per design or occasion (مناسبة). Before designing, look there for examples that fit the request and follow them.
- `KAMI/المشروع/` (`1AtcmoSNbGBe-mPFtxyAD44M1YploQe3D`) holds the designs. Every new design gets its own folder named after it: `KAMI/المشروع/<اسم التصميم>/`. The original goes inside that folder, and sources go in `المصدر/`.
- `KAMI/متفرقات/` (`172u6fZtjZ3DDUPNKFGpU54OfygfuVYvc`) holds temporary and draft designs. Approved ones move to `المشروع/<اسم التصميم>/`; unused ones go to `10_ARCHIVE` (never deleted). (D-026)
- `KAMI/فيديوهاتي/` (`1h1DwBrpgIUC126kc2eMeRyTIi1LP_xdE`) holds ready-to-post reels, covers and captions.
- Revisions: when the user asks for changes, make a new file in the same folder named `تعديل 1`, `تعديل 2`, `تعديل 3` and so on, so earlier versions are kept. Never put a revision in a different folder.

- **Save every design in two places:** the Drive folder `KAMI/المشروع/<اسم التصميم>/`, and Canva as an editable design under the same name, so text and elements can be changed later. Put the final PNG/PDF exports and a `canva-link.txt` with the Canva link in that Drive folder. Make revisions in Canva too, then export them as `تعديل N` into the same folder.
- All design text is in Bahraini dialect: see bahraini-dialect.
- **Design index:** `KAMI/فهرس-التصاميم.md` (`1rQY7NJvVMC64tF6AvGz0z9nIWEeblSra`) lists every design: folder, latest version, slide text, prices, hours, brand facts and a change log. **Update it every time** a design is created or edited (new row in the table + a line in سجل التعديلات). To answer questions about design content, read the index before opening images. Graphify was removed on 2026-11-14 at the user's request (too many tokens). Don't reinstall it unless the user asks.

**Why:** The user wants every design and all of its versions in one place in Google Drive, reachable from any device. New designs should follow their examples, and every design should stay editable in Canva.

**How to apply:** Do this for every design request, whatever the tool (Canva, OpenArt, HTML and so on). If a design exists only online, as with Canva, still make its Drive folder with an export or link file. If it isn't clear whether to edit in place or make a new تعديل file, make a new تعديل file. Without the synced G: drive, upload with the Drive connector. Related: drive-workspace, brand-style.
