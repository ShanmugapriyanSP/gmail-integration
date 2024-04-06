import base64
import re
from logging import Logger
from typing import Union, Dict

from bs4 import BeautifulSoup

from enums.email_header import EmailHeader
from objects.email import Email
from parser.parser import Parser
from utils.generic import GenericUtils


class EmailParser(Parser):

    @staticmethod
    def parse(response: Dict, label: str, logger: Logger) -> Union[None, Email]:
        """
        Parses the email response and returns an Email object
        :param response:
        :param label:
        :param logger:
        :return:
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

            logger.debug(email)

        except Exception as e:
            logger.exception(f"Error parsing email: {e}")
            raise

        return email
