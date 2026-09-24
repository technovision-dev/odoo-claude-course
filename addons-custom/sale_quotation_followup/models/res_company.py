from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    quotation_followup_enabled = fields.Boolean(string="Quotation Follow-ups", default=True)
    quotation_followup_skip_expired = fields.Boolean(
        string="Skip expired quotations", default=True
    )
