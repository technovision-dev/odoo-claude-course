# User guide

## Sending a quotation

Nothing changes: send it with **Send by Email** or **Mark as Sent**. The quotation then shows
**Quotation Sent On** next to the expiration date. Follow-ups count from that day.

## Seeing the follow-ups on a quotation

A **Follow-ups** button appears at the top of the quotation once one was sent. It opens the
log: date, level, result. Each follow-up also posts a note in the chatter.

All follow-ups: **Sales > Orders > Quotation Follow-ups**. The **Failed** filter shows
emails that could not be sent.

## Sending the next follow-up now

1. Open a sent quotation, or select several in the quotation list.
2. **Actions > Send follow-up now**.

The next level not yet sent goes out immediately, whatever the quotation's age. It is refused
for a quotation that is not in "Quotation Sent", for a customer who opted out, and when every
level was already sent.

## Stopping follow-ups for one quotation

Any of these stops them: the customer replies on the quotation (an email reply that reaches
the chatter, or a portal comment), the quotation is confirmed or cancelled, or it expires
(when the company skips expired quotations).

## When something goes wrong

| You see | Why | What to do |
|---|---|---|
| No follow-up was sent | No level reached yet, the customer replied or opted out, the quotation expired, or follow-ups are off in Settings | Check the quotation's dates and chatter, and the setting |
| A log line with result "Failed" | The email could not be generated; the reason is in the Note column | Fix the template, then use **Send follow-up now** |
| Only one follow-up after a long pause | By design: only the latest level reached is sent | Nothing |
