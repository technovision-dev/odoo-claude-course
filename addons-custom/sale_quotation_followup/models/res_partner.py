from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    quotation_followup_optout = fields.Boolean(
        string="No quotation follow-ups",
        help="Never send automatic follow-ups for this customer's quotations.",
    )
