---
description: Build the Odoo Apps Store page (static/description/index.html) for a module
argument-hint: <module>
---

Build the Apps Store listing for: $ARGUMENTS

Follow `.claude/rules/apps-store.md` exactly; start from `listing-template/index.html`.

1. Read `docs/README.md`, `docs/USER_GUIDE.md` and the manifest. The page says the same as the
   README; every claim must be true of the code.
2. List the screenshots the page needs (one per feature) and check which exist in
   `static/description/`. For each missing one, tell me what screen to capture; do not invent
   file names on the page for images that do not exist.
3. Write `static/description/index.html`: a fragment, inline styles and Bootstrap classes only,
   relative image paths, no script, no style block, no outside links.
4. Check it: grep the file for `<script`, `<style`, `http://`, `https://` (only an allowed
   YouTube link may remain) and `src="/`. Report what you found.
