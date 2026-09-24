from odoo import fields, models


class QuotationFollowupLog(models.Model):
    _name = "quotation.followup.log"
    _description = "Quotation Follow-up Log"
    _order = "date desc, id desc"
    _check_company_auto = True

    order_id = fields.Many2one(
        "sale.order", string="Quotation", required=True, ondelete="cascade", index=True
    )
    partner_id = fields.Many2one(related="order_id.partner_id", store=True, string="Customer")
    level_id = fields.Many2one(
        "quotation.followup.level", string="Level", required=True, ondelete="restrict"
    )
    company_id = fields.Many2one(related="order_id.company_id", store=True)
    date = fields.Datetime(required=True, default=fields.Datetime.now)
    result = fields.Selection(
        [("sent", "Sent"), ("failed", "Failed")], required=True, default="sent"
    )
    note = fields.Char()

    _order_level_unique = models.Constraint(
        "unique(order_id, level_id)",
        "A quotation is followed up only once per level.",
    )
