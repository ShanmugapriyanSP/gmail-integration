import base64
import re
import traceback
from typing import List

from bs4 import BeautifulSoup
from google.api.service_pb2 import Service
from googleapiclient.discovery import build

from model.email import Email
from service.oauth_service import OAuthService
from utils.generic import GenericUtils


class GmailService:
    _service: Service

    def __init__(self, oauth: OAuthService):
        self._service = build('gmail', 'v1', credentials=oauth.credentials)

    def get_label_id(self, search_label) -> str:
        labels = self._service.users().labels().list(userId='me').execute()
        label_id = None

        for label in labels['labels']:
            if label['name'] == search_label:
                label_id = label['id']
                break

        return label_id

    @staticmethod
    def parse_email(text) -> Email:
        """
        """

        email = Email()
        try:
            payload = text['payload']
            headers = payload['headers']

            # Look for Subject and Sender Email in the headers
            for props in headers:
                if props['name'] == 'Subject':
                    email.subject = props['value']
                if props['name'] == 'From':
                    email.sender = props['value']
                if props['name'] == 'Date':
                    email.received_date = props['value']

            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload
            while re.search("multipart/*", parts['mimeType']):
                parts = parts.get('parts')[0]

            data = parts['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)

            soup = BeautifulSoup(decoded_data, "html.parser")
            body = soup.get_text()
            email.message_body = GenericUtils.remove_extra_whitespaces(body)

            # Extract message body (handles text/plain only for simplicity)
            print(email)

        except Exception as e:
            print(f"Error parsing email: {e}")
            traceback.format_exc()

        return email

    def get_messages_by_label(self, label_id: str, limit: int = 5) -> None:
        result = self._service.users().messages().list(userId='me', labelIds=[label_id], maxResults=limit).execute()
        messages = result.get('messages')

        emails: List[Email] = []
        # iterate through all the messages
        for msg in messages:
            # Get the message from its id
            txt = self._service.users().messages().get(userId='me', id=msg['id'], format='full').execute()

            emails.append(self.parse_email(txt))

