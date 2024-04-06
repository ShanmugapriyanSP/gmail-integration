from unittest import TestCase
from unittest.mock import patch, Mock, call

from data.sql_client import SqlClient
from fetch_emails import FetchEmails
from resources.mock_data import MockData
from service.gmail_service import GmailService
from utils.generic import GenericUtils


@patch.object(GenericUtils, 'load_yaml', return_value=MockData.get_config())
class TestFetchEmails(TestCase):

    def setUp(self):
        self.gmail_service = Mock(spec=GmailService)
        self.sql_client = Mock(spec=SqlClient)
        self.fetch_emails = FetchEmails(self.gmail_service, self.sql_client)

    def test_process(self, mock_config):
        # GIVEN
        labels = MockData.get_all_labels()
        emails = MockData.get_email_objects(2)
        self.gmail_service.get_all_labels.return_value = labels
        self.gmail_service.get_messages_by_label.return_value = emails

        # WHEN
        self.fetch_emails.process()

        # THEN
        # Verify calls to Gmail Service
        assert self.gmail_service.method_calls == [
            call.get_all_labels(),
            call.get_messages_by_label(
                label=labels[0],
                limit=100
            ),
            call.get_messages_by_label(
                label=labels[1],
                limit=100
            ),
            call.get_messages_by_label(
                label=labels[2],
                limit=100
            )
        ]
        # Verify calls to SQL client
        assert self.sql_client.method_calls == [
            call.insert_emails(emails),
            call.insert_emails(emails),
            call.insert_emails(emails),
            call.close_connection()
        ]
