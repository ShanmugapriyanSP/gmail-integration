
from logging import Logger
from typing import List

from config import Config
from data.sql_client import SqlClient
from objects.email import Email
from objects.label import Label
from service.gmail_service import GmailService
from service.oauth_service import OAuthService
from utils.generic import GenericUtils


class FetchEmails:
    _config_vars: Config
    _gmail_service: GmailService
    _sql_client: SqlClient
    _logger: Logger

    def __init__(self, gmail_service: GmailService, sql_client: SqlClient):
        self._config_vars = Config()
        self._gmail_service = gmail_service
        self._sql_client = sql_client
        self._logger = GenericUtils.get_logger(self.__class__.__name__)

    def process(self):
        """
        * Fetch all Gmail labels
        * For each Gmail label, fetch up to the configured max email count
        * Insert the emails into the database
        :return:
        """
        try:
            count = 0
            labels: List[Label] = self._gmail_service.get_all_labels()
            for label in labels:
                emails: List[Email] = self._gmail_service.get_messages_by_label(
                    label=label,
                    limit=self._config_vars.max_email_count
                )
                self._logger.info(f"Fetched {len(emails) if emails else 0} Emails for Label - {label.name}")
                if emails:
                    self._sql_client.insert_emails(emails)
                    count += len(emails)
        except Exception as ex:
            self._logger.exception(f"Error occurred in the process method: {ex}")
            raise
        finally:
            self._sql_client.close_connection()

        self._logger.info(f"Total of {count} emails persisted in the database!!")


if __name__ == "__main__":
    FetchEmails(
        gmail_service=GmailService(OAuthService()),
        sql_client=SqlClient()
    ).process()
