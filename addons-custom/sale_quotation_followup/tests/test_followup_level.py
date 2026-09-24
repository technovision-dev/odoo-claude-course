from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestFollowupLevel(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # The demo levels (3, 7, 14 days) would collide with ours: the unique rule
        # includes archived rows, so remove them rather than archive them.
        Level = cls.env["quotation.followup.level"]
        Level.with_context(active_test=False).search([]).unlink()
        cls.level = Level.create({"name": "Check-in", "days_after_sent": 3})
        cls.customer = cls.env["res.partner"].create({"name": "Nile Retail"})

    def test_creating_a_level_works(self):
        self.assertEqual(self.level.company_id, self.env.company)
        self.assertTrue(self.level.active)

    @mute_logger("odoo.sql_db")
    def test_same_days_twice_in_one_company_is_refused(self):
        with self.assertRaises(IntegrityError):
            self.env["quotation.followup.level"].create({"name": "Duplicate", "days_after_sent": 3})

    def test_zero_days_is_refused(self):
        with self.assertRaises(ValidationError):
            self.env["quotation.followup.level"].create({"name": "Same day", "days_after_sent": 0})

    def test_sending_a_quotation_stamps_the_sent_date(self):
        order = self.env["sale.order"].create({"partner_id": self.customer.id})
        self.assertFalse(order.quotation_sent_date)
        order.action_quotation_sent()
        self.assertTrue(order.quotation_sent_date)
        self.assertFalse(order.copy().quotation_sent_date)
