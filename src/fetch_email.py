from config import Config
from service.oauth_service import OAuthService
from service.gmail_service import GmailService


class FetchEmails:
    _config_vars: Config

    def __init__(self):
        self._config_vars = Config()
        self._oauth_service = OAuthService(self._config_vars)
        self._gmail_service = GmailService(self._oauth_service)

    def process(self):
        label_id = self._gmail_service.get_label_id(self._config_vars.search_label)
        self._gmail_service.get_messages_by_label(label_id, self._config_vars.max_email_count)


if __name__ == "__main__":
    FetchEmails().process()
