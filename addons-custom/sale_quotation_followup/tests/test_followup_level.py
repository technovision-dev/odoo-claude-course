from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tools import mute_logger

from .common import FollowupCase


@tagged("post_install", "-at_install")
class TestFollowupLevel(FollowupCase):
    def test_level_orders_by_sequence_then_days(self):
        levels = self.env["quotation.followup.level"].search([])
        self.assertEqual(levels, self.level_3 | self.level_14)
        self.assertEqual(levels[0], self.level_3)

    @mute_logger("odoo.sql_db")
    def test_same_days_twice_in_one_company_is_refused(self):
        with self.assertRaises(IntegrityError):
            self.env["quotation.followup.level"].create(
                {
                    "name": "Duplicate",
                    "days_after_sent": 3,
                    "mail_template_id": self.level_3.mail_template_id.id,
                }
            )

    def test_days_must_be_positive(self):
        with self.assertRaises(ValidationError):
            self.env["quotation.followup.level"].create(
                {
                    "name": "Same day",
                    "days_after_sent": 0,
                    "mail_template_id": self.level_3.mail_template_id.id,
                }
            )

    def test_sending_a_quotation_stamps_the_sent_date(self):
        order = self.env["sale.order"].create({"partner_id": self.customer.id})
        self.assertFalse(order.quotation_sent_date)
        order.action_quotation_sent()
        self.assertTrue(order.quotation_sent_date)
        self.assertFalse(order.copy().quotation_sent_date)

    def test_resending_keeps_the_first_sent_date(self):
        order = self.make_quotation(self.TODAY)
        # What the "Send by Email" wizard does when it posts the email.
        order.with_context(mark_so_as_sent=True).message_post(body="Your quotation")
        self.assertEqual(order.quotation_sent_date, self.TODAY)
