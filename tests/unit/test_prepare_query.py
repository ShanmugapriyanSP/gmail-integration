from unittest import TestCase

from email_rule_processor import EmailRuleProcessor
from model.rule import Rule


class TestPrepareQuery(TestCase):

    def test_prepare_query_all_condition(self):
        # GIVEN
        rule_json = {
            "predicate": "All",
            "conditions": [
                {
                    "field": "From",
                    "predicate": "contains",
                    "value": "hello@offers.uspoloassn.in"
                },
                {
                    "field": "Subject",
                    "predicate": "contains",
                    "value": "Upto 40% off on luxury handbags"
                },
                {
                    "field": "Date Received",
                    "predicate": "less than",
                    "value": "2 months"
                }
            ],
            "actions": {
                "Move Message": "IMPORTANT",
                "Mark as read": True
            }
        }
        rule = Rule(rule_json)

        # WHEN
        query = EmailRuleProcessor.prepare_query(rule.predicate, rule.conditions)

        # THEN
        self.assertEqual(query, "SELECT message_id, label from emails "
                                "WHERE sender LIKE '%hello@offers.uspoloassn.in%' AND "
                                "subject LIKE '%Upto 40% off on luxury handbags%' AND "
                                "AGE(CURRENT_TIMESTAMP, received_date) < INTERVAL '2 months'")

    def test_prepare_query_any_condition(self):
        # GIVEN
        rule_json = {
            "predicate": "Any",
            "conditions": [
                {
                    "field": "To",
                    "predicate": "does not equal",
                    "value": "shanmugapriyan9696@gmail.com"
                },
                {
                    "field": "Subject",
                    "predicate": "equals",
                    "value": "Re: WES Verification - 11-CS-045"
                }
            ],
            "actions": {
                "Mark as Read": False
            }
        }
        rule = Rule(rule_json)

        # WHEN
        query = EmailRuleProcessor.prepare_query(rule.predicate, rule.conditions)

        # THEN
        self.assertEqual(query, "SELECT message_id, label from emails "
                                "WHERE receiver != 'shanmugapriyan9696@gmail.com' OR "
                                "subject = 'Re: WES Verification - 11-CS-045'")

    def test_error_raised_for_unknown_predicate(self):
        # GIVEN
        rule_json = {
            "predicate": "Both",
            "conditions": [
                {
                    "field": "To",
                    "predicate": "does not equal",
                    "value": "shanmugapriyan9696@gmail.com"
                },
                {
                    "field": "Subject",
                    "predicate": "equals",
                    "value": "Re: WES Verification - 11-CS-045"
                }
            ],
            "actions": {
                "Mark as Read": False
            }
        }
        rule = Rule(rule_json)

        # WHEN
        with self.assertRaises(NotImplementedError) as ex:
            EmailRuleProcessor.prepare_query(rule.predicate, rule.conditions)

        # THEN
        self.assertEqual(str(ex.exception), "Predicate both is not defined!!")
