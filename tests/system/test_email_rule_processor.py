from unittest import TestCase
from unittest.mock import patch, Mock, call

from data.sql_client import SqlClient
from email_rule_processor import EmailRuleProcessor
from resources.mock_data import MockData
from service.gmail_service import GmailService
from utils.generic import GenericUtils


@patch.object(GenericUtils, 'load_yaml', return_value=MockData.get_config())
class TestEmailRuleProcessor(TestCase):

    def setUp(self):
        self.gmail_service = Mock(spec=GmailService)
        self.sql_client = Mock(spec=SqlClient)
        self.email_rule_processor = EmailRuleProcessor(self.gmail_service, self.sql_client)

    @patch.object(GenericUtils, 'load_json')
    def test_process(self, mock_rules, mock_config):
        # GIVEN
        mock_rules.return_value = MockData.get_rules()
        self.sql_client.fetch_emails.side_effect = (
            MockData.get_email_objects(2),
            MockData.get_email_objects(3)
        )
        # WHEN
        self.email_rule_processor.process()

        # THEN
        # Verify calls to SQL Client
        assert self.sql_client.method_calls == [
            call.fetch_emails(
                "SELECT message_id, label FROM emails WHERE sender LIKE '%U.S. Polo Assn. India%' AND "
                "subject LIKE '%Upto 40% off on luxury handbags%' AND "
                "AGE(CURRENT_TIMESTAMP, received_date) < INTERVAL '2 months'"
            ),
            call.fetch_emails(
                "SELECT message_id, label FROM emails WHERE receiver != 'shanmugapriyan9696@gmail.com' OR "
                "subject = 'Re: WES Verification - 11-CS-045'"
            )
        ]
        # Verify calls to Gmail Service
        assert self.gmail_service.method_calls == [
            call.update_labels(
                message_ids=['email_id_1', 'email_id_2'],
                add_label_ids=['IMPORTANT'],
                remove_label_ids=['SPAM']
            ),
            call.update_labels(
                message_ids=['email_id_1', 'email_id_2'],
                add_label_ids=[],
                remove_label_ids=['UNREAD']
            ),
            call.update_labels(
                message_ids=['email_id_1', 'email_id_2', 'email_id_3'],
                add_label_ids=['UNREAD'],
                remove_label_ids=[]
            )
        ]
