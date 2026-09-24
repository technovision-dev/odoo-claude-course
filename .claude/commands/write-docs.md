---
description: Write or refresh the nine documentation files of a module from its code and spec
argument-hint: <module>
---

Write the documentation for: $ARGUMENTS

Sources, in this order of authority: the code, `docs/SPEC.md`, the tests. Never write a field,
menu, setting, group or behaviour from memory: find it in the code first. Templates for all
nine files are in `docs-templates/`.

1. Build a fact sheet first and show it to me: every model with its fields (name, type,
   label), every menu path, every setting, every group and what it can do, every cron and its
   interval, every email template, and what data leaves the server. Wait for approval.
2. Write `docs/README.md`, `INSTALLATION.md`, `CONFIGURATION.md`, `USER_GUIDE.md`,
   `DEVELOPER_GUIDE.md`, `FAQ.md`, `CHANGELOG.md`, `SECURITY.md`, `SUPPORT.md` from the
   templates, using only the fact sheet.
3. FAQ answers come from real behaviour in the code (multi-company, upgrade, what happens when
   an email fails). If you cannot point to the code for an answer, leave the question out.
4. Finish by listing every field and menu name the docs mention, each with the file and line
   where it is defined.
