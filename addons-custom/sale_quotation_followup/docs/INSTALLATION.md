# Installation

## Requirements

- Odoo 18.0 (or 19.0 from the `19.0` branch), Community or Enterprise.
- Installed automatically as dependencies: Sales, Discuss.
- No extra Python packages.

## Steps

1. Copy the `sale_quotation_followup` folder into a directory on your `addons_path`.
2. Restart Odoo.
3. **Apps > Update Apps List**, search "Quotation Follow-ups", **Install**.

## Check that it works

- **Sales > Configuration > Follow-up Levels** exists (sales managers).
- **Settings > Technical > Scheduled Actions** lists "Quotation Follow-ups: send due
  follow-ups", running every day.
- Two email templates exist: "Quotation Follow-up: Friendly" and
  "Quotation Follow-up: Last reminder".

A database without demo data starts with no level, so nothing is sent until you create one
(see [Configuration](CONFIGURATION.md)).

## Uninstalling

Removes the levels, the log, the settings and the scheduled action. Notes already posted on
quotations and emails already sent stay.
