import base64
import re
from logging import Logger
from typing import List, Union, Dict

from bs4 import BeautifulSoup
from google.api.service_pb2 import Service
from googleapiclient.discovery import build

from enums.email_header import EmailHeader
from objects.batch_modify_request import BatchModifyRequest
from objects.email import Email
from objects.label import Label
from parser.email_parser import EmailParser
from service.oauth_service import OAuthService
from utils.generic import GenericUtils


class GmailService:
    _service: Service
    _logger: Logger
    MAX_BATCH_UPDATE: int = 1000

    def __init__(self, oauth: OAuthService):
        self._service = build('gmail', 'v1', credentials=oauth.credentials, num_retries=3)
        self._logger = GenericUtils.get_logger(self.__class__.__name__)

    def get_message_list_by_label(self, label_id: str, limit: int = 5) -> Dict:
        return self._service.users().messages().list(userId='me', labelIds=[label_id], maxResults=limit).execute()

    def get_message_by_id(self, msg_id: str) -> Dict:
        return self._service.users().messages().get(userId='me', id=msg_id, format='full').execute()

    def batch_modify(self, batch_modify_request: BatchModifyRequest):
        return self._service.users().messages().batchModify(userId='me', body=batch_modify_request.json()).execute()

    def get_all_labels(self) -> List[Label]:
        """
        Returns all Gmail labels
        :return:
        """
        labels = self._service.users().labels().list(userId='me').execute()
        return [Label(label['id'], label['name']) for label in labels['labels']]

    def get_messages_by_label(self, label: Label, limit: int = 5) -> List[Email]:
        """
        Fetch the Message Ids and retrieve each message content by the message ID
        :param label:
        :param limit:
        :return:
        """
        result = self.get_message_list_by_label(label.id, limit)
        messages = result.get('messages')

        if not messages:
            return []

        emails: List[Email] = []
        for msg in messages:
            response = self.get_message_by_id(msg['id'])
            email = EmailParser.parse(response, label.name, self._logger)
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

    def update_labels(self, message_ids: List[str], add_label_ids: List[str] = None,
                      remove_label_ids: List[str] = None):
        """
        Add / Remove label Ids for the provided message_ids
        :param message_ids:
        :param add_label_ids:
        :param remove_label_ids:
        :return:
        """

        if not message_ids:
            return

        for msg_ids in self.batch_message_ids(message_ids, self.MAX_BATCH_UPDATE):
            self._logger.info(f"Updating Labels for {len(msg_ids)} messages")
            self.batch_modify(BatchModifyRequest(msg_ids, add_label_ids, remove_label_ids))
