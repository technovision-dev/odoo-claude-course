# Configuration

## Settings

**Sales > Configuration > Settings**, block **Quotations & Orders**, setting
**Quotation Follow-ups** (per company):

| Setting | Default | Effect |
|---|---|---|
| Quotation Follow-ups | On | Off: the scheduled action sends nothing for this company. |
| Skip expired quotations | On | Quotations past their validity date get no follow-up. |

## Follow-up levels

**Sales > Configuration > Follow-up Levels**. Sales managers only.

| Field | Meaning | Example |
|---|---|---|
| Name | Shown in the log and in the note on the quotation | Friendly check-in |
| Days After Sent | The level applies once the quotation is at least this many days old. 1 or more; one level per number of days per company | 3 |
| Email Template | The email sent (a template on Sales Order) | Quotation Follow-up: Friendly |
| Schedule a To-Do for the salesperson | Also creates a To-Do activity for the quotation's salesperson | On for the last level |
| Company | Levels apply to quotations of their company | |

Archived levels are never sent. The two included templates can be edited under
**Settings > Technical > Email Templates**.

## Customers who must not be followed up

On the contact, tab **Sales & Purchase**, tick **No quotation follow-ups**. Ticking it on a
company covers all of its contacts.

## Scheduled action

| Name | Interval | What it does |
|---|---|---|
| Quotation Follow-ups: send due follow-ups | 1 day | Sends every follow-up due today |

## Multi-company

Levels, settings and the log are per company. A quotation only uses levels of its own company.
