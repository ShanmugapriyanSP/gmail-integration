from typing import Dict, List

from google.oauth2.credentials import Credentials

from objects.email import Email
from objects.label import Label
from resources.utils import TestUtils


class MockData:

    @staticmethod
    def get_config() -> Dict:
        return {
            "max_email_count": 100,
            "rules_file": "/path/to/rules.yml",
            "google": {
                "credential_file": "/path/to/credential.json",
                "token_file": "/path/to/token.json",
                "scopes": ["scope1", "scope2"],
                "redirect_port": 8080
            },
            "database": {
                "db_name": "test_db",
                "table_name": "emails",
                "host": "localhost",
                "port": "5432",
                "user": "test_user"
            }
        }

    @staticmethod
    def get_valid_google_credentials() -> Credentials:
        return Credentials(
            token='valid_token',
            refresh_token='valid_refresh_token',
            expiry=TestUtils.get_future_date()
        )

    @staticmethod
    def get_expired_google_credentials() -> Credentials:
        return Credentials(
            token="expired_token",
            refresh_token="expired_token",
            expiry=TestUtils.get_past_date()
        )

    @staticmethod
    def get_message_ids():
        return {
            "messages": [
                {"id": "email_id1"},
                {"id": "email_id2"}
            ]
        }

    @staticmethod
    def get_message(email_id) -> Dict:
        return {
            'id': email_id,
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

    @staticmethod
    def get_rules():
        return {
            "rules": [
                {
                    "description": "Rule 1",
                    "predicate": "All",
                    "conditions": [
                        {
                            "field": "From",
                            "predicate": "contains",
                            "value": "U.S. Polo Assn. India"
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
                },
                {
                    "description": "Rule 2",
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
            ]
        }

    @staticmethod
    def get_email_objects(count: int = 2) -> List[Email]:
        emails = []
        for i in range(count):
            emails.append(Email(f"email_id_{i + 1}", "SPAM"))
        return emails

    @staticmethod
    def get_all_labels():
        labels = []
        for label in ["SPAM", "IMPORTANT", "TRASH"]:
            labels.append(Label(label, label))
        return labels
