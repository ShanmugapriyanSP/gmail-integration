import logging
from unittest import TestCase

from parser.email_parser import EmailParser


class TestEmailParser(TestCase):
    def test_parse_email(self):
        response = {
            'id': 'email_id',
            'payload': {
                'headers': [
                    {'name': 'Subject', 'value': 'Test Email'},
                    {'name': 'From', 'value': 'sender@example.com'},
                    {'name': 'To', 'value': 'receiver@example.com'},
                    {'name': 'Date', 'value': 'Mon, 1 Apr 2024 16:28:14 +0530 (IST)'}
                ],
                'body': {'data': 'VGVzdCBtYWlsIGJvZHk='},
                'mimeType': 'text/html'
            }
        }
        label = 'Test Label'

        email = EmailParser.parse(response, label, logging.getLogger())

        self.assertIsNotNone(email)
        self.assertEqual(email.label, label)
        self.assertEqual(email.subject, 'Test Email')
        self.assertEqual(email.sender, 'sender@example.com')
        self.assertEqual(email.to, 'receiver@example.com')
        self.assertEqual(email.received_date, '2024-04-01 16:28:14')
        self.assertEqual(email.message_body, "Test mail body")