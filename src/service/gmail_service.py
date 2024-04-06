import base64
import re
import traceback
from logging import Logger
from typing import List, Dict, Tuple, Union

from bs4 import BeautifulSoup
from google.api.service_pb2 import Service
from googleapiclient.discovery import build

from enums.email_header import EmailHeader
from model.email import Email
from model.label import Label
from service.oauth_service import OAuthService
from utils.generic import GenericUtils


class GmailService:
    _service: Service
    _logger: Logger
    MAX_BATCH_UPDATE: int = 1000

    def __init__(self, oauth: OAuthService):
        self._service = build('gmail', 'v1', credentials=oauth.credentials)
        self._logger = GenericUtils.get_logger(self.__class__.__name__)

    def get_all_labels(self) -> List[Label]:
        """
        Returns all Gmail labels
        :return:
        """
        labels = self._service.users().labels().list(userId='me').execute()
        return [Label(label['id'], label['name']) for label in labels['labels']]

    def parse_email(self, response, label) -> Union[None, Email]:
        """
        """

        email = Email()
        email.label = label
        try:
            email.message_id = response['id']
            payload = response['payload']
            headers = payload['headers']

            header_map = {
                EmailHeader.SUBJECT.value: 'subject',
                EmailHeader.FROM.value: 'sender',
                EmailHeader.TO.value: 'to',
                EmailHeader.RECEIVED_DATE.value: 'received_date'
            }
            # Find Subject, Sender Email, To Email and the Received Date in the headers
            for props in headers:
                if props['name'] in header_map.keys():
                    setattr(email, header_map[props['name']], props['value'])

            parts = payload
            while re.search("multipart/*", parts['mimeType']):
                parts = parts.get('parts')[0]

            # The Body of the message is in Encrypted format. So, we have to decode it.
            data = parts['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)

            soup = BeautifulSoup(decoded_data, "html.parser")
            body = soup.get_text()
            email.message_body = GenericUtils.remove_extra_whitespaces(body)

            self._logger.debug(email)

        except Exception as e:
            self._logger.exception(f"Error parsing email: {e}")
            raise

        return email

    def get_messages_by_label(self, label: Label, limit: int = 5) -> List[Email]:
        """
        Fetch the Message Ids and retrieve each message content by the message ID
        :param label:
        :param limit:
        :return:
        """
        result = self._service.users().messages().list(userId='me', labelIds=[label.id], maxResults=limit).execute()
        messages = result.get('messages')

        if not messages:
            return []

        emails: List[Email] = []
        for msg in messages:
            response = self._service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            email = self.parse_email(response, label.name)
            if email:
                emails.append(email)
        return emails

    @staticmethod
    def batch_message_ids(message_ids, batch_size):
        """
        Generator function to yield batches of message IDs
        :param message_ids:
        :param batch_size:
        :return:
        """
        for i in range(0, len(message_ids), batch_size):
            yield message_ids[i:i + batch_size]

    def batch_modify(self, message_ids: List[str], add_label_ids: List[str] = None, remove_label_ids: List[str] = None):
        """

        :param message_ids:
        :param add_label_ids:
        :param remove_label_ids:
        :return:
        """

        if not message_ids:
            return

        request_body = {}
        if add_label_ids and len(add_label_ids) > 0:
            request_body["addLabelIds"] = add_label_ids
        if remove_label_ids and len(remove_label_ids) > 0:
            request_body["removeLabelIds"] = remove_label_ids

        for msg_ids in self.batch_message_ids(message_ids, self.MAX_BATCH_UPDATE):
            request_body["ids"] = msg_ids
            return self._service.users().messages().batchModify(userId='me', body=request_body).execute()
