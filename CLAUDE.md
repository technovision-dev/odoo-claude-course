# Odoo custom addons workspace

Version-specific rules are in `.claude/rules/` (`odoo18.md`, `odoo19.md`, `apps-store.md`) and are
loaded with this file. Replace "TechnoVision", the website and the support email with your own.

## Layout

- `./odoo/` - Odoo core, cloned from GitHub. READ-ONLY. Never edit, never create files here.
  Grep it whenever you need a core field name, XML id, method signature, group id or menu id.
  Never write a core field, id or method from memory.
- `./addons-custom/` - our modules. One folder per module, technical name in snake_case.
- `./venv/` - Python virtualenv. Use `./venv/bin/python` if you need Python directly.
- `./odoo.conf` - config (copied from `odoo.conf.example`). `addons_path` = core + `./addons-custom`.
- `./tools/port19.py` - stages the Odoo 19 copy of a module (see `.claude/rules/odoo19.md`).
- Databases: `course18` is the dev database served by the running server. `course18_test` is for
  automated tests only. Never run `-i`/`-u` with `--test-enable` against `course18`.

## Commands

Start the server (usually already running in another terminal):

    ./venv/bin/python odoo/odoo-bin -c odoo.conf -d course18 --dev=all

Update a module on the dev database after adding or removing files, models, fields or XML:

    ./venv/bin/python odoo/odoo-bin -c odoo.conf -d course18 -u MODULE --stop-after-init

Install and test one module on a fresh test database (this is the definition of "done"):

    dropdb --if-exists course18_test
    ./venv/bin/python odoo/odoo-bin -c odoo.conf -d course18_test -i MODULE \
        --test-enable --test-tags /MODULE --stop-after-init

Lint and format:

    ruff check addons-custom/MODULE && ruff format addons-custom/MODULE

Shell into a database:

    ./venv/bin/python odoo/odoo-bin shell -c odoo.conf -d course18

## Verify your work (mandatory)

A task is not finished until:
1. `ruff check` passes on the module.
2. The install + test command exits 0 and the log says `0 failed, 0 error(s)`, with no other
   ERROR or CRITICAL line. (A test that expects a database constraint to fire logs
   `duplicate key value violates unique constraint` at ERROR level: that one is expected.)
3. You have read the log. If there is a traceback, fix it and rerun. Never report "done" on a
   failing install, and never on a run you did not do.
4. If you changed XML, the module also updates cleanly on `course18` with `-u`.

Quote the exact test summary line in your final message.

## Module structure

    MODULE/
    ├── __init__.py            # imports: models, wizard, controllers, report (in that order)
    ├── __manifest__.py
    ├── models/                # one file per model: models/quotation_followup_level.py
    ├── wizard/                # transient models and their views
    ├── controllers/
    ├── report/
    ├── security/
    │   ├── security.xml       # groups and record rules
    │   └── ir.model.access.csv
    ├── views/                 # one file per model, menus.xml last
    ├── data/                  # records the module needs to work (crons, templates, sequences)
    ├── demo/                  # demo data only; never referenced by code
    ├── static/description/    # icon.png, banner.png, index.html, screenshots
    ├── i18n/                  # MODULE.pot + ar.po
    ├── tests/                 # __init__.py + test_*.py
    └── docs/                  # the nine documentation files

Omit folders that would be empty.

## Manifest

```python
{
    "name": "Quotation Follow-ups",
    "summary": "Follow up automatically on quotations sent but not answered, by configurable levels",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "author": "TechnoVision",
    "website": "https://technovision.dev",
    "support": "info@technovision.dev",
    "license": "LGPL-3",
    "depends": ["sale_management", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/mail_template_data.xml",
        "data/ir_cron_data.xml",
        "views/quotation_followup_level_views.xml",
        "views/menus.xml",
    ],
    "demo": ["demo/quotation_followup_level_demo.xml"],
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
```

- `version` is `SERIES.MAJOR.MINOR.PATCH`: `18.0.1.0.0` on the 18.0 branch, `19.0.1.0.0` on 19.0.
  Odoo refuses to install a module whose version does not start with the running series.
- `data` order: groups and rules, access CSV, data, views, menus last. A file may only reference
  ids defined earlier in the list or in a dependency.
- `license`: `LGPL-3` for free modules, `OPL-1` for paid ones (then add `price` and `currency`).
- `depends` lists every module whose models, ids or groups we reference, and nothing else.
- No `description` key: the Apps Store reads `static/description/index.html`.

## Python and ORM

- `from odoo import api, fields, models, Command, _` and
  `from odoo.exceptions import UserError, ValidationError`.
- Every model has `_name` and `_description`. Extensions use `_inherit = "sale.order"` only.
- Field names: `Many2one` ends in `_id`, `One2many`/`Many2many` in `_ids`, dates `*_date`,
  datetimes `*_datetime`; booleans read as statements (`create_activity`, `*_optout`).
- Methods: `_compute_FIELD`, `_inverse_FIELD`, `_search_FIELD`, `_onchange_FIELD`,
  `_check_FIELD`. A compute method assigns a value to every record in `self`.
- `create` is always `@api.model_create_multi def create(self, vals_list)`.
- Display names: `_compute_display_name`. `name_get` no longer exists; never write it.
- Always set `_order`. Environment-dependent defaults are lambdas:
  `default=lambda self: self.env.company`.
- Unique and check constraints: see the rules file for the series. Python constraints use
  `@api.constrains` and raise `ValidationError(_("..."))`.
- Multi-company models: `_check_company_auto = True`, `check_company=True` on related
  Many2one fields, and a record rule on `company_id in company_ids`.
- Never search inside a loop (N+1). Use one `search` with a domain, `_read_group` for
  aggregates, and `mapped`/`filtered` on recordsets.
- `sudo()` only with a comment saying why it is safe. Never on a whole workflow method.
- No raw SQL unless there is a stated performance reason; then parameters, never formatting.
- User-facing strings in `_()`, with arguments passed to `_()`, not `%` after it. Log messages
  are not translated.
- Per-company settings are fields on `res.company` shown through related fields on
  `res.config.settings`. Global settings use `ir.config_parameter` with keys prefixed by the
  module name.
- Crons: an `@api.model def _cron_NAME(self)` that calls the real logic. Never swallow an error
  silently: log it and record it where a user will see it.
- Chatter: inherit `["mail.thread", "mail.activity.mixin"]`; post notes with
  `message_post(..., subtype_xmlid="mail.mt_note")`; send templates with
  `template.send_mail(record.id)` and let the mail queue deliver.
- Dates: `fields.Date.context_today(self)` for the user's today. Pass "today" into date logic
  (`_find_followup_quotations(today)`) so tests never depend on the real clock.
- Style: ruff (config in `ruff.toml`), double quotes, f-strings, no commented-out code.

## Security

`security/ir.model.access.csv` header, exactly:

    id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink

- `id`: `access_MODEL_UNDERSCORED_ROLE`, e.g. `access_quotation_followup_level_manager`.
- `model_id:id`: `model_` + the model name with dots as underscores:
  `quotation.followup.level` becomes `model_quotation_followup_level`.
- `group_id:id`: a fully qualified external id (`sales_team.group_sale_manager`).
- Every model, transient ones included, gets at least one access line.
- Record rules for multi-company: `domain_force` = `[('company_id', 'in', company_ids)]`.
- Menus and actions for manager-only models carry `groups="..."`.

## Views

See `.claude/rules/odoo18.md` for the syntax. In short: `<list>` never `<tree>`, no `attrs` or
`states`, `<chatter/>`. Grep the core view before inheriting it to get the real anchor.

- View ids: `MODEL_UNDERSCORED_view_list`, `_view_form`, `_view_search`; action
  `MODEL_UNDERSCORED_action`; menu `menu_MODEL_UNDERSCORED`.
- Sequence fields get `widget="handle"`; models with `active` get an "Archived" filter.
- `company_id` in views carries `groups="base.group_multi_company"`.

## Data files

- Crons, mail templates, groups and sequences go in `<data noupdate="1">` so an update does not
  overwrite what an administrator changed.
- Mail templates: `model_id`, `subject` with `{{ object.name }}`, `partner_to`
  `{{ object.partner_id.id }}`, `lang` `{{ object.partner_id.lang }}`, `body_html` as QWeb with
  `<t t-out="..."/>`, `auto_delete` False.

## Tests

- `tests/__init__.py` imports every `test_*.py`. Shared fixtures in a `common.py` base class.
- `from odoo.tests import TransactionCase, tagged`; every class
  `@tagged("post_install", "-at_install")`; fixtures in `setUpClass`.
- Expected constraint errors: `@mute_logger("odoo.sql_db")` and
  `with self.assertRaises(IntegrityError)`. Validation errors: `assertRaises(ValidationError)`.
- Test names state the behaviour: `test_opted_out_customer_is_skipped`, not `test_3`.
- Test our logic, not Odoo's. One test per rule in `docs/SPEC.md`.
- Never delete or weaken a test to make it pass.

## Docs

Nine Markdown files in `docs/`: README, INSTALLATION, CONFIGURATION, USER_GUIDE,
DEVELOPER_GUIDE, FAQ, CHANGELOG, SECURITY, SUPPORT. Templates are in `docs-templates/`.
Written from the code and `docs/SPEC.md`, never from memory: every field, menu and setting a
doc names must exist in the code.

## Git

- One repository per module, one branch per series: `18.0`, `19.0`.
- Commit messages: `[ADD]`, `[FIX]`, `[IMP]`, `[REF]`, `[REM]`, `[DOC]` + module + short text:
  `[IMP] sale_quotation_followup: skip customers who replied`.

## Working with me

- For any task touching more than one file, plan first and wait for my approval.
- When the spec is ambiguous, ask. Do not invent features; list anything extra under "Extras".
- When an install or test fails, show the last 15 lines of the traceback and your fix.
- Keep answers short: code and commands over prose.
