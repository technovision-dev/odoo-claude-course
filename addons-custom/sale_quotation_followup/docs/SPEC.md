# Spec: Quotation Follow-ups

## Problem

A salesperson sends a quotation and the customer goes quiet. Following up by hand depends on
someone remembering, and quotations nobody follows up on are often simply lost.

## Users

- Salesperson (`sales_team.group_sale_salesman`): sends quotations, sees follow-ups, can send
  the next follow-up by hand.
- Sales manager (`sales_team.group_sale_manager`): configures levels and settings.

## Rules

1. A quotation's "sent date" is the day it was marked as sent (Send by Email or Mark as Sent).
   Duplicating a quotation does not copy it.
2. A follow-up level has a number of days after sending (> 0), an email template and an
   optional To-Do for the salesperson. One level per number of days per company.
3. Every day, a quotation still in "Quotation Sent" gets the highest level it has reached,
   unless that level was already sent. Missed days never produce a burst of emails.
4. Each level is sent at most once per quotation.
5. No follow-up when: the customer (the contact or its company) opted out; the company turned
   follow-ups off; the quotation expired (validity date passed) and the company skips expired
   quotations; the customer wrote on the quotation on or after the day it was sent.
6. Sending posts a note on the quotation, logs the result, and schedules the To-Do if the level
   asks for it. A failed send is logged as failed with the reason and does not stop the others.
7. "Send follow-up now" sends a quotation's next unsent level immediately, whatever its age, and
   refuses quotations that are not sent, opted-out customers, and quotations with every level
   already sent.
8. Multi-company: levels and logs are per company.

## Out of scope

WhatsApp or SMS (bonus lecture), follow-ups on confirmed orders, reply detection outside Odoo.
