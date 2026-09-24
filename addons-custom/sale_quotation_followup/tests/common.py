from datetime import date

from odoo import Command
from odoo.tests import TransactionCase


class FollowupCase(TransactionCase):
    """Shared fixtures: two levels (3 and 14 days) and a way to make sent quotations."""

    TODAY = date(2026, 3, 20)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company.quotation_followup_enabled = True
        cls.company.quotation_followup_skip_expired = True
        # Demo levels would collide with ours: the unique (days, company) rule
        # includes archived rows, so remove them rather than archive them.
        cls.env["quotation.followup.level"].with_context(active_test=False).search([]).unlink()
        template = cls.env.ref("sale_quotation_followup.mail_template_followup_friendly")
        Level = cls.env["quotation.followup.level"]
        cls.level_3 = Level.create(
            {"name": "Check-in", "days_after_sent": 3, "mail_template_id": template.id}
        )
        cls.level_14 = Level.create(
            {
                "name": "Last reminder",
                "sequence": 20,
                "days_after_sent": 14,
                "mail_template_id": template.id,
                "create_activity": True,
            }
        )
        cls.salesperson = cls.env["res.users"].create(
            {
                "name": "Sam Seller",
                "login": "sam.seller@example.com",
                "email": "sam.seller@example.com",
            }
        )
        cls.customer = cls.env["res.partner"].create(
            {"name": "Nile Retail", "email": "buyer@nile.example"}
        )
        cls.product = cls.env["product.product"].create({"name": "Consulting", "list_price": 100})

    def make_quotation(self, sent_on, partner=None, validity=None):
        """Create a quotation and mark it sent on ``sent_on``."""
        order = self.env["sale.order"].create(
            {
                "partner_id": (partner or self.customer).id,
                "user_id": self.salesperson.id,
                "validity_date": validity,
                "order_line": [Command.create({"product_id": self.product.id})],
            }
        )
        order.action_quotation_sent()
        order.quotation_sent_date = sent_on
        return order

    def due(self, today=None):
        """The due follow-ups as ``{order: level}``."""
        return dict(self.env["sale.order"]._find_followup_quotations(today or self.TODAY))
