import logging
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    quotation_sent_date = fields.Date(
        string="Quotation Sent On",
        copy=False,
        readonly=True,
        help="Set when the quotation is marked as sent. Follow-up levels count from this date.",
    )
    followup_log_ids = fields.One2many("quotation.followup.log", "order_id", string="Follow-ups")
    followup_count = fields.Integer(compute="_compute_followup_count")

    @api.depends("followup_log_ids")
    def _compute_followup_count(self):
        for order in self:
            order.followup_count = len(order.followup_log_ids)

    def write(self, vals):
        # Both ways Odoo marks a quotation as sent (the "Send by Email" wizard and
        # "Mark as Sent") end in write({"state": "sent"}), so this is the one place
        # that sees every send.
        if vals.get("state") == "sent" and "quotation_sent_date" not in vals:
            vals = dict(vals, quotation_sent_date=fields.Date.context_today(self))
        return super().write(vals)

    def action_view_followups(self):
        """Open the follow-up log of this quotation."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Follow-ups"),
            "res_model": "quotation.followup.log",
            "view_mode": "list,form",
            "domain": [("order_id", "=", self.id)],
            "context": {"create": False},
        }

    # ------------------------------------------------------------------
    # Engine
    # ------------------------------------------------------------------

    def _followup_replied_orders(self):
        """Return the orders in ``self`` whose customer wrote on them after sending."""
        if not self:
            return self.browse()
        # sudo: we read only the author and date of messages posted on the
        # quotations in self, which the caller can already read. One grouped
        # query for the whole batch instead of one search per quotation.
        rows = (
            self.env["mail.message"]
            .sudo()
            ._read_group(
                [
                    ("model", "=", "sale.order"),
                    ("res_id", "in", self.ids),
                    ("message_type", "in", ("email", "comment")),
                    ("author_id", "!=", False),
                ],
                ["res_id", "author_id"],
                ["date:max"],
            )
        )
        orders = {order.id: order for order in self}
        replied = set()
        for res_id, author, last_date in rows:
            order = orders[res_id]
            customer = order.partner_id.commercial_partner_id
            if (
                author.commercial_partner_id == customer
                and last_date.date() >= order.quotation_sent_date
            ):
                replied.add(res_id)
        return self.browse(sorted(replied))

    def _followup_due_level(self, today, levels):
        """Return the level this quotation is due on ``today``, or an empty recordset.

        Only the highest level the quotation has reached is sent: if the cron did
        not run for a few days, the customer gets one email, not a burst of them.
        """
        self.ensure_one()
        age = (today - self.quotation_sent_date).days
        reached = levels.filtered(
            lambda lvl: lvl.company_id == self.company_id and lvl.days_after_sent <= age
        )
        if not reached:
            return levels.browse()
        top = reached.sorted("days_after_sent")[-1]
        if top in self.followup_log_ids.level_id:
            return levels.browse()
        return top

    @api.model
    def _find_followup_quotations(self, today):
        """Return ``[(order, level)]`` for every quotation due a follow-up on ``today``."""
        levels = self.env["quotation.followup.level"].search([])
        companies = levels.company_id.filtered("quotation_followup_enabled")
        if not companies:
            return []
        first_day = min(levels.mapped("days_after_sent"))
        orders = self.search(
            [
                ("state", "=", "sent"),
                ("quotation_sent_date", "<=", today - timedelta(days=first_day)),
                ("company_id", "in", companies.ids),
                ("partner_id.quotation_followup_optout", "=", False),
                ("partner_id.commercial_partner_id.quotation_followup_optout", "=", False),
            ]
        )
        orders = orders.filtered(
            lambda o: (
                not (
                    o.company_id.quotation_followup_skip_expired
                    and o.validity_date
                    and o.validity_date < today
                )
            )
        )
        orders -= orders._followup_replied_orders()
        due = []
        for order in orders:
            level = order._followup_due_level(today, levels)
            if level:
                due.append((order, level))
        return due

    def _send_followup(self, level):
        """Send ``level``'s email for this quotation, record the result and return the log."""
        self.ensure_one()
        try:
            with self.env.cr.savepoint():
                level.mail_template_id.send_mail(self.id)
            result, note = "sent", False
        except Exception as error:  # noqa: BLE001 - one bad template must not stop the batch
            _logger.exception("Follow-up %s failed for %s", level.name, self.name)
            result, note = "failed", str(error)[:250]

        Log = self.env["quotation.followup.log"]
        vals = {"result": result, "note": note, "date": fields.Datetime.now()}
        log = Log.search([("order_id", "=", self.id), ("level_id", "=", level.id)])
        if log:
            log.write(vals)
        else:
            log = Log.create({"order_id": self.id, "level_id": level.id, **vals})

        if result == "sent":
            self.message_post(
                body=_("Follow-up “%s” sent to the customer.", level.name),
                message_type="comment",
                subtype_xmlid="mail.mt_note",
            )
            if level.create_activity and self.user_id:
                self.activity_schedule(
                    "mail.mail_activity_data_todo",
                    summary=_("Follow up on quotation %s", self.name),
                    user_id=self.user_id.id,
                )
        return log

    @api.model
    def _cron_send_quotation_followups(self):
        """Daily: send every follow-up that is due today."""
        due = self._find_followup_quotations(fields.Date.context_today(self))
        for order, level in due:
            order._send_followup(level)
        _logger.info("Quotation follow-ups: %d due, processed", len(due))

    def action_send_followup_now(self):
        """Send each selected quotation's next unsent level now, whatever its age."""
        levels = self.env["quotation.followup.level"].search([])
        for order in self:
            if order.state != "sent":
                raise UserError(_("Only sent quotations can be followed up (%s).", order.name))
            partner = order.partner_id
            if partner.quotation_followup_optout or (
                partner.commercial_partner_id.quotation_followup_optout
            ):
                raise UserError(
                    _("%s has opted out of quotation follow-ups.", partner.display_name)
                )
            done = order.followup_log_ids.filtered(lambda log: log.result == "sent").level_id
            next_level = levels.filtered(
                lambda lvl: lvl.company_id == order.company_id and lvl not in done
            )[:1]
            if not next_level:
                raise UserError(_("%s has already received every follow-up.", order.name))
            order._send_followup(next_level)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success",
                "message": _("Follow-ups sent: %s", len(self)),
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
