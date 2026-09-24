# Quotation Follow-ups

Follows up automatically on quotations that were sent to customers but not answered.

## What it does

- Sends a follow-up email when a sent quotation reaches a level you define: for example a
  friendly check-in after 3 days, a second follow-up after 7, a last reminder after 14.
- Stops following up as soon as the customer writes on the quotation, the quotation is
  confirmed or expires, or the customer opted out.
- Never sends a burst: if follow-ups did not run for a few days, the customer gets only the
  latest level reached.
- Schedules a To-Do for the salesperson on the levels you choose.
- Logs every follow-up (sent or failed) and shows the count on the quotation.
- Lets a salesperson send the next follow-up by hand from the quotation list or form.

## What it does not do

- It does not read replies sent to an outside mailbox: only messages that reach the
  quotation's chatter count as an answer.
- It does not follow up on confirmed sales orders or invoices.

## Compatibility

| Odoo | Edition | Status |
|---|---|---|
| 18.0 | Community and Enterprise | 20 automated tests pass |
| 19.0 | Community and Enterprise | 20 automated tests pass (branch `19.0`) |

Depends on: the Sales app (`sale_management`) and Discuss (`mail`).

## Documentation

[Installation](INSTALLATION.md) · [Configuration](CONFIGURATION.md) ·
[User guide](USER_GUIDE.md) · [Developer guide](DEVELOPER_GUIDE.md) · [FAQ](FAQ.md) ·
[Security](SECURITY.md) · [Changelog](CHANGELOG.md) · [Support](SUPPORT.md) · [Spec](SPEC.md)
