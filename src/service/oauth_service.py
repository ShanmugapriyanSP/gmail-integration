import os
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config import Config


class OAuthService:
    _credential_file: str
    _token_file: str
    _scopes: List[str]
    _redirect_port_number: int
    __credentials: Credentials

    def __init__(self, config_vars: Config):
        self._credential_file = config_vars.credential_file
        self._token_file = config_vars.token_file
        self._scopes = config_vars.scopes
        self._redirect_port_number = config_vars.redirect_port
        self.__credentials = self.__authenticate()

    def __authenticate(self) -> Credentials:
        """
        Load credentials from the local token file if exists otherwise
        get consent from user using credential file which will create
        a local token file as cache
        :return:
        """
        credentials = None
        if os.path.exists(self._token_file):
            credentials = Credentials.from_authorized_user_file(self._token_file, self._scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:

            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())

            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    self._credential_file, self._scopes
                )
                credentials = flow.run_local_server(port=self._redirect_port_number)

            # Save the credentials for the next run
            with open(self._token_file, "w") as token:
                token.write(credentials.to_json())

        return credentials

    @property
    def credentials(self) -> Credentials:
        return self.__credentials
