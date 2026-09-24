# Security

## Groups and access

| Model | Salesperson (`sales_team.group_sale_salesman`) | Sales manager (`sales_team.group_sale_manager`) |
|---|---|---|
| `quotation.followup.level` | read | read, write, create, delete |
| `quotation.followup.log` | read, write, create | read, write, create, delete |

Salespeople create log entries when they use **Send follow-up now**. The Follow-up Levels menu
is visible to sales managers only.

## Record rules

`quotation.followup.level` and `quotation.followup.log`: `company_id in company_ids`.

## Data that leaves the server

Follow-up emails to the quotation's customer, through Odoo's normal outgoing mail. No other
service is contacted.

## Elevated rights in code

One `sudo()`: `_followup_replied_orders` reads the author and date of messages posted on
quotations the user can already read, in one grouped query, and returns nothing else.
