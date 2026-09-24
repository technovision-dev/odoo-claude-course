# Developer guide

## Models

### `quotation.followup.level` (Quotation Follow-up Level)

| Field | Type | Notes |
|---|---|---|
| `name` | Char | required, translatable |
| `sequence` | Integer | default 10 |
| `days_after_sent` | Integer | required, > 0 (`_check_days_after_sent`) |
| `mail_template_id` | Many2one `mail.template` | required, domain model `sale.order` |
| `create_activity` | Boolean | To-Do for the salesperson |
| `active` | Boolean | default True |
| `company_id` | Many2one `res.company` | required, default current company |

Unique `(days_after_sent, company_id)`. Order `sequence, days_after_sent, id`.

### `quotation.followup.log` (Quotation Follow-up Log)

`order_id`, `partner_id` (related, stored), `level_id`, `company_id` (related, stored), `date`,
`result` (`sent` / `failed`), `note`. Unique `(order_id, level_id)`.

### Extensions

- `sale.order`: `quotation_sent_date` (Date, not copied, set in `write` when `state` becomes
  `sent`), `followup_log_ids`, `followup_count`.
- `res.partner`: `quotation_followup_optout`.
- `res.company`: `quotation_followup_enabled`, `quotation_followup_skip_expired`, shown through
  related fields on `res.config.settings`.

## Engine (`sale.order`)

| Method | Purpose | Safe to override? |
|---|---|---|
| `_find_followup_quotations(today)` | `[(order, level)]` due on `today` | Yes: call `super()` and filter the list |
| `_followup_due_level(today, levels)` | The one level due for an order | Yes |
| `_followup_replied_orders()` | Orders whose customer wrote after sending, in one grouped query | Yes |
| `_send_followup(level)` | Sends, logs, posts the note, schedules the To-Do; returns the log | Yes: call `super()` to keep the log |
| `_cron_send_quotation_followups()` | Scheduled action entry point | Prefer the methods above |
| `action_send_followup_now()` | "Send follow-up now" | Yes |

`today` is always passed in, so the date logic is tested without freezing the clock.

## Odoo 19

The `19.0` branch differs only by the manifest version and `models.Constraint` in place of
`_sql_constraints` (see `.claude/rules/odoo19.md`); `tools/port19.py` produces it.

## Tests

    ./venv/bin/python odoo/odoo-bin -c odoo.conf -d course18_test -i sale_quotation_followup \
        --test-enable --test-tags /sale_quotation_followup --stop-after-init

20 tests: level constraints and ordering, the sent-date stamp and re-sending, level selection (reached,
highest only, once per level), every skip rule, reply detection, sending, logging, failure
handling, the scheduled action and the manual action.
