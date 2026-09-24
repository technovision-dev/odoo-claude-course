from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class QuotationFollowupLevel(models.Model):
    _name = "quotation.followup.level"
    _description = "Quotation Follow-up Level"
    _order = "sequence, days_after_sent, id"
    _check_company_auto = True

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    days_after_sent = fields.Integer(
        required=True,
        help="Days after the quotation was sent. The follow-up goes out once the quotation is "
        "at least this old and still has no answer.",
    )
    mail_template_id = fields.Many2one(
        "mail.template",
        string="Email Template",
        required=True,
        domain="[('model', '=', 'sale.order')]",
    )
    create_activity = fields.Boolean(
        string="Schedule a To-Do for the salesperson",
        help="Also schedule a To-Do activity on the quotation for its salesperson.",
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )

    _days_company_unique = models.Constraint(
        "unique(days_after_sent, company_id)",
        "Each company can have only one follow-up level per number of days.",
    )

    @api.constrains("days_after_sent")
    def _check_days_after_sent(self):
        for level in self:
            if level.days_after_sent <= 0:
                raise ValidationError(_("A follow-up must be at least one day after sending."))
