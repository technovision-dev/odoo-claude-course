from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    quotation_sent_date = fields.Date(
        string="Quotation Sent On",
        copy=False,
        readonly=True,
        help="Set when the quotation is marked as sent. Follow-up levels count from this date.",
    )
    followup_log_ids = fields.One2many(
        "quotation.followup.log", "order_id", string="Follow-ups"
    )
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
