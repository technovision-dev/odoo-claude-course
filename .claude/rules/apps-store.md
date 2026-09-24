# Odoo Apps Store listing rules

## `static/description/`

- `icon.png` 128x128. `banner.png` (the card image, referenced from `images` in the manifest).
  Screenshots `screenshot_1.png`, `screenshot_2.png` ... about 1280 px wide.
- `index.html` is a fragment the store sanitises:
  - No `<script>`, no `<style>` block, no external CSS, fonts or iframes. Inline `style="..."`
    and Bootstrap classes only.
  - Images are relative paths inside `static/description/`, never absolute URLs.
  - No `<html>`, `<head>` or `<body>`; start with `<section class="container">`.
  - No links to outside websites and no promotions (discounts, "buy now elsewhere").
    Contact details and a canonical YouTube video are the exceptions.
  - Structure: title and one-sentence value, features with screenshots, how it works,
    compatibility, support and licence.
- Every claim on the page must be true of the code. No "AI-powered" unless it is.
- The page and `docs/README.md` say the same thing.

## Publishing

- The store imports a module from a Git repository branch named after the series (`18.0`).
  Register the repository URL with the branch at `apps.odoo.com/apps/upload`.
- A paid (`OPL-1`) module needs `price` and `currency` in the manifest. Buyers are owed fixes
  for defects in the version they bought.
- A new series (`19.0`) is a new branch registered separately; pushing the branch alone does
  not publish anything.
