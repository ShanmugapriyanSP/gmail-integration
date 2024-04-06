import unittest
from unittest.mock import Mock, patch, call

from objects.label import Label
from resources.mock_data import MockData
from service.gmail_service import GmailService
from service.oauth_service import OAuthService


class TestGmailService(unittest.TestCase):
    def setUp(self):
        self.oauth_service = Mock(spec=OAuthService)
        self.gmail_service = GmailService(self.oauth_service)

    @patch.object(GmailService, 'get_message_by_id')
    @patch.object(GmailService, 'get_message_list_by_label')
    def test_get_messages_by_label(self, mock_message_by_label, mock_message_by_id):
        # GIVEN
        mock_message_by_label.return_value = MockData.get_message_ids()
        mock_message_by_id.side_effect = (
            MockData.get_message('email_id1'),
            MockData.get_message('email_id2')
        )
        label = Label('label_id', 'Test Label')

        # WHEN
        emails = self.gmail_service.get_messages_by_label(label)

        # THEN
        self.assertEqual(len(emails), 2)
        self.assertEqual(emails[0].message_id, 'email_id1')
        self.assertEqual(emails[1].message_id, 'email_id2')

    @patch.object(GmailService, 'batch_modify')
    def test_update_labels(self, mock_batch_modify):
        # GIVEN
        msg_ids = ["msg_id1", "msg_id2", "msg_id3", "msg_id4", "msg_id5"]
        add_label_ids = ["SPAM"]
        remove_label_ids = ["IMPORTANT"]
        self.gmail_service.MAX_BATCH_UPDATE = 3

        # WHEN
        self.gmail_service.update_labels(msg_ids, add_label_ids, remove_label_ids)

        # THEN
        # Verify two batchModify calls are made with maximum of 3 msgIds in each call
        self.assertEqual(mock_batch_modify.call_count, 2)
        first_request = mock_batch_modify.call_args_list[0].args[0]
        second_request = mock_batch_modify.call_args_list[1].args[0]
        # 1st batch
        self.assertEqual(first_request.json(), {
            'addLabelIds': ['SPAM'],
            'removeLabelIds': ['IMPORTANT'],
            'ids': [
                'msg_id1',
                'msg_id2',
                'msg_id3'
            ]
        })
        # 2nd batch
        self.assertEqual(second_request.json(), {
            'addLabelIds': ['SPAM'],
            'removeLabelIds': ['IMPORTANT'],
            'ids': [
                'msg_id4',
                'msg_id5'
            ]
        })

