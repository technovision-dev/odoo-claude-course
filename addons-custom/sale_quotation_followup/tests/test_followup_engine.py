from datetime import timedelta
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tools import mute_logger

from .common import FollowupCase


@tagged("post_install", "-at_install")
class TestFollowupEngine(FollowupCase):
    def days_ago(self, days):
        return self.TODAY - timedelta(days=days)

    def test_quotation_is_due_once_it_reaches_a_level(self):
        young = self.make_quotation(self.days_ago(2))
        ready = self.make_quotation(self.days_ago(3))
        due = self.due()
        self.assertNotIn(young, due)
        self.assertEqual(due[ready], self.level_3)

    def test_missed_days_send_only_the_highest_level(self):
        # The cron did not run for two weeks: one email, the last one, not two.
        order = self.make_quotation(self.days_ago(20))
        self.assertEqual(self.due()[order], self.level_14)

    def test_a_level_is_sent_only_once(self):
        order = self.make_quotation(self.days_ago(3))
        order._send_followup(self.level_3)
        self.assertNotIn(order, self.due())
        self.assertNotIn(order, self.due(self.TODAY + timedelta(days=5)))
        self.assertEqual(self.due(self.TODAY + timedelta(days=11))[order], self.level_14)

    def test_opted_out_customer_is_skipped(self):
        self.customer.quotation_followup_optout = True
        self.assertNotIn(self.make_quotation(self.days_ago(5)), self.due())

    def test_opt_out_on_the_company_covers_its_contacts(self):
        company = self.env["res.partner"].create(
            {"name": "Delta Foods", "is_company": True, "quotation_followup_optout": True}
        )
        contact = self.env["res.partner"].create(
            {"name": "Mona", "parent_id": company.id, "email": "mona@delta.example"}
        )
        self.assertNotIn(self.make_quotation(self.days_ago(5), partner=contact), self.due())

    def test_expired_quotation_is_skipped_unless_configured(self):
        order = self.make_quotation(self.days_ago(5), validity=self.days_ago(1))
        self.assertNotIn(order, self.due())
        self.company.quotation_followup_skip_expired = False
        self.assertIn(order, self.due())

    def test_confirmed_order_is_not_followed_up(self):
        order = self.make_quotation(self.days_ago(5))
        order.action_confirm()
        self.assertNotIn(order, self.due())

    def test_disabled_company_sends_nothing(self):
        order = self.make_quotation(self.days_ago(5))
        self.company.quotation_followup_enabled = False
        self.assertNotIn(order, self.due())

    def test_customer_reply_after_sending_stops_follow_ups(self):
        order = self.make_quotation(self.days_ago(5))
        order.message_post(
            body="Can you do 10% off?", author_id=self.customer.id, message_type="comment"
        )
        # The message is dated today; the quotation was sent five days ago.
        self.assertNotIn(order, self.due(self.TODAY + timedelta(days=400)))

    def test_salesperson_note_does_not_count_as_a_reply(self):
        order = self.make_quotation(self.days_ago(5))
        order.message_post(body="Called, no answer.", author_id=self.salesperson.partner_id.id)
        self.assertIn(order, self.due())

    def test_sending_logs_posts_a_note_and_schedules_an_activity(self):
        order = self.make_quotation(self.days_ago(14))
        log = order._send_followup(self.level_14)
        self.assertEqual(log.result, "sent")
        self.assertEqual(order.followup_count, 1)
        self.assertIn("Last reminder", order.message_ids[0].body)
        activity = order.activity_ids.filtered(lambda a: a.user_id == self.salesperson)
        self.assertTrue(activity)

    def test_a_failed_send_is_logged_and_does_not_raise(self):
        order = self.make_quotation(self.days_ago(3))
        Template = self.registry["mail.template"]
        with (
            patch.object(Template, "send_mail", side_effect=UserError("Template broken")),
            mute_logger("odoo.addons.sale_quotation_followup.models.sale_order"),
        ):
            log = order._send_followup(self.level_3)
        self.assertEqual(log.result, "failed")
        self.assertIn("Template broken", log.note)
        self.assertFalse(order.activity_ids)

    def test_cron_runs(self):
        self.make_quotation(self.days_ago(3))
        self.env["sale.order"]._cron_send_quotation_followups()

    def test_send_now_sends_the_next_unsent_level(self):
        order = self.make_quotation(self.TODAY)
        order.action_send_followup_now()
        self.assertEqual(order.followup_log_ids.level_id, self.level_3)
        order.action_send_followup_now()
        self.assertEqual(order.followup_log_ids.level_id, self.level_3 | self.level_14)
        with self.assertRaises(UserError):
            order.action_send_followup_now()

    def test_send_now_refuses_an_opted_out_customer(self):
        order = self.make_quotation(self.TODAY)
        self.customer.quotation_followup_optout = True
        with self.assertRaises(UserError):
            order.action_send_followup_now()
