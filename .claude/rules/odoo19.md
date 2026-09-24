# Porting to Odoo 19

The `18.0` branch is what the Apps Store imports for 18; never edit it to make 19 work.
Stage a 19 copy instead (`python3 tools/port19.py addons-custom/MODULE /path/to/19/addons/MODULE`)
and keep a `19.0` branch built from the staged copy that passed its tests.

Every rule below was found by installing real modules on Odoo 19.0, not from release notes.

## The one that fails silently

- **`_sql_constraints` is ignored on 19.** The module installs, no warning is logged, and the
  constraint is never created. Constraints are class attributes instead:

      _days_company_unique = models.Constraint(
          "unique(days_after_sent, company_id)",
          "Each company can have only one follow-up level per number of days.",
      )

  Only a test that expects the constraint to fire catches this. Keep one for every constraint.

## Renamed or removed

- `res.users.groups_id` is `group_ids` (also on `ir.ui.menu`, `ir.ui.view` and actions).
- `res.groups.users` is `user_ids`; `res.groups.category_id` is replaced by `privilege_id`
  pointing to a new `res.groups.privilege` record.
- `<group>` in **search** views accepts neither `expand` nor `string`. Form views still accept
  `<group string="...">`; never strip it there.
- `ir.actions.act_window` `target="inline"` is gone.
- `sale.order.line.tax_id` is `tax_ids`.
- `res.partner.mobile` is gone; only `phone` remains.
- Mail templates are validated when saved: a template that cannot render is refused at write
  time, not at send time.

## Verifying a port

A 19 port is done when the full suite passes on a fresh 19 database, not when it installs.
Run the same install + test command against the Odoo 19 checkout and quote the summary line.
