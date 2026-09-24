from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    quotation_followup_enabled = fields.Boolean(
        related="company_id.quotation_followup_enabled", readonly=False
    )
    quotation_followup_skip_expired = fields.Boolean(
        related="company_id.quotation_followup_skip_expired", readonly=False
    )
