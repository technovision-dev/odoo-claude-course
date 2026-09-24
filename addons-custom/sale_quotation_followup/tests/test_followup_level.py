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
