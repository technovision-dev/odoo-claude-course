# Build Odoo Modules 10x Faster with Claude Code: course workspace

This repository is the workspace for the course by Rasmy Potross (TechnoVision). You clone it
and work inside it: it becomes `~/odoo18`, Odoo's core is cloned into `./odoo` next to your
modules, and Claude Code reads the `CLAUDE.md` and `.claude/` folder from here.

## Start

```
git clone {GITHUB_COURSE_REPO} ~/odoo18
cd ~/odoo18
git switch -c my-work section-0
git clone https://github.com/odoo/odoo.git --branch 18.0 --depth 1 odoo
python3 -m venv venv && source venv/bin/activate
pip install -r odoo/requirements.txt
cp odoo.conf.example odoo.conf && sed -i "s/YOUR_USER/$USER/g" odoo.conf
```

Lecture 1.2 walks through each line, including the system packages and PostgreSQL user.

## What is here

| Path | What it is | Lecture |
|---|---|---|
| `CLAUDE.md` | The conventions Claude Code follows in this workspace | 1.2, 2.4 |
| `.claude/rules/` | Odoo 18 syntax, porting to 19, Apps Store rules | 2.4, 7.4, 8.3 |
| `.claude/settings.json` | Permissions, and two hooks: no edits to Odoo core, ruff after every Python edit | 1.2, 6.3 |
| `.claude/commands/` | `/new-model`, `/add-test`, `/run-tests`, `/write-docs`, `/listing` | 6.1 |
| `.claude/agents/` | `odoo-reviewer`, `odoo-tester` | 6.2, 7.1 |
| `addons-custom/sale_quotation_followup/` | The course project, built section by section | all |
| `docs-templates/` | The nine documentation files | 8.1 |
| `listing-template/` | An Apps Store `index.html` that follows the store's rules | 8.3 |
| `tools/port19.py` | Stages the Odoo 19 copy of a module | 7.4 |
| `ruff.toml` | Lint and format settings used by the hook | 6.3 |

`odoo/`, `venv/`, `data/` and `odoo.conf` are gitignored: they live in the workspace, never in
your commits.

## The course project: Quotation Follow-ups

Follows up automatically on quotations that were sent to customers but not answered: levels
you define (3, 7, 14 days...), one email per level, never a burst, and it stops when the customer
replies, the quotation is confirmed or expires, or the customer opted out. Its documentation is
in `addons-custom/sale_quotation_followup/docs/`. It is LGPL-3: use it, change it, publish it.

## Tags

One tag per section: `section-0` is the empty workspace where Lecture 1.3 starts, and
`section-1` ... `section-10` hold the module as it is at the end of each section. If you fall
behind: `git switch -c catch-up section-5`. The `19.0` branch holds the Odoo 19 version.

## Tests

```
dropdb --if-exists course18_test
./venv/bin/python odoo/odoo-bin -c odoo.conf -d course18_test -i sale_quotation_followup \
    --test-enable --test-tags /sale_quotation_followup --stop-after-init
```

The finished module passes 20 tests on Odoo 18 and on Odoo 19.

## License

The module is LGPL-3. The rest of this repository (CLAUDE.md, `.claude/`, templates, tools)
is MIT: copy it into your own projects.
