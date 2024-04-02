import traceback
from typing import List

from config import Config
from database.postgre_sql_manager import PostgreSqlManager
from model.email import Email
from service.oauth_service import OAuthService
from service.gmail_service import GmailService


class FetchEmails:
    _config_vars: Config

    def __init__(self):
        self._config_vars = Config()
        self._oauth_service = OAuthService(self._config_vars)
        self._gmail_service = GmailService(self._oauth_service)
        self._sql_manager = PostgreSqlManager(self._config_vars)

    def process(self):
        try:
            label_id = self._gmail_service.get_label_id(self._config_vars.search_label)
            emails: List[Email] = self._gmail_service.get_messages_by_label(label_id, self._config_vars.max_email_count)
            self._sql_manager.insert_emails(emails)
        except Exception as ex:
            print(ex)
            traceback.format_exc()
        finally:
            self._sql_manager.close_connection()


if __name__ == "__main__":
    FetchEmails().process()
