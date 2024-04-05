import traceback
from logging import Logger
from typing import List

from config import Config
from data.sql_client import SqlClient
from model.email import Email
from service.oauth_service import OAuthService
from service.gmail_service import GmailService
from utils.generic import GenericUtils


class FetchEmails:
    _config_vars: Config
    _oauth_service: OAuthService
    _gmail_service: GmailService
    _sql_client: SqlClient
    _logger: Logger

    def __init__(self):
        self._config_vars = Config()
        self._oauth_service = OAuthService(self._config_vars)
        self._gmail_service = GmailService(self._oauth_service)
        self._sql_client = SqlClient(self._config_vars)
        self._logger = GenericUtils.get_logger(self.__class__.__name__)

    def process(self):
        """
        * Fetch all Gmail labels
        * For each Gmail label, fetch up to the configured max email count
        * Insert the emails into the data
        :return:
        """
        try:
            labels: List[str] = self._gmail_service.get_all_labels()
            for label_id in labels:
                emails: List[Email] = self._gmail_service.get_messages_by_label(
                    label_id=label_id,
                    limit=self._config_vars.max_email_count
                )
                self._logger.info(f"Fetched {len(emails) if emails else 0} Emails for Label - {label_id}")
                if emails:
                    self._sql_client.insert_emails(emails)
        except Exception as ex:
            self._logger.exception(f"Error occurred in the process method: {ex}")
            raise
        finally:
            self._sql_client.close_connection()


if __name__ == "__main__":
    FetchEmails().process()
