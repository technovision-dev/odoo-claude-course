# Odoo 18 syntax

Applies to every module on the `18.0` branch.

## Views

- List views are `<list>`; actions use `view_mode` `list,form`. `<tree>` is gone.
- No `attrs` and no `states`. Use Python expressions directly:
  `invisible="state != 'sent'"`, `readonly="not active"`, `required="create_activity"`,
  `column_invisible="..."` in lists.
- Forms end with `<chatter/>`, not the old `oe_chatter` div.
- Smart buttons go inside `<div name="button_box" position="inside">` when inheriting a form
  that already has a button box (`sale.view_order_form` does).
- Settings pages inherit the app's settings view and add a `<setting>` inside an existing
  `<block>` (Sales: `sale.res_config_settings_view_form`, block
  `quotation_order_setting_container`). Use `company_dependent="1"` for company fields.
- Search views: `<filter>` elements may sit directly in `<search>`; avoid `<group expand=...>`
  (it is invalid on Odoo 19, so leaving it out keeps one view for both series).

## Models

- Unique and check constraints use the list form:

      _sql_constraints = [
          ("days_company_unique", "unique(days_after_sent, company_id)", "User message."),
      ]

  On 19 this attribute is ignored silently; see `odoo19.md`.
- `res.users` groups field is `groups_id`; `res.groups` users field is `users`.

## Data

- `ir.cron` has no `numbercall` and no `doall`. Fields: `name`, `model_id`, `state` = `code`,
  `code`, `interval_number`, `interval_type`, `user_id`, `active`.
- Mail template bodies are QWeb: `<t t-out="object.name"/>`, not `${object.name}`.
