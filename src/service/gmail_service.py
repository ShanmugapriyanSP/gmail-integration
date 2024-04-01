import base64
import os
from pathlib import Path

from bs4 import BeautifulSoup
from google.api.service_pb2 import Service
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

TOKEN_PATH = str(Path(__file__).parent / "../../token.json")
CREDENTIALS = str(Path(__file__).parent / "../../credentials.json")

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
port_number = 53669
redirect_uri = f'http://localhost:{port_number}/'


class GmailService:
    __creds: dict
    _service: Service

    def __init__(self):
        self.authenticate()
        self._service = build('gmail', 'v1', credentials=self.__creds)

    def authenticate(self) -> None:
        creds = None
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS, SCOPES
                )
                creds = flow.run_local_server(port=port_number)
            # Save the credentials for the next run
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())

        self.__creds = creds

    def get_label_id(self, search_label) -> str:
        labels = self._service.users().labels().list(userId='me').execute()
        label_id = None

        for label in labels['labels']:
            if label['name'] == search_label:
                label_id = label['id']
                break

        return label_id

    def get_messages_by_label(self, label_id: str, limit: int = 5) -> None:
        result = self._service.users().messages().list(userId='me', labelIds=[label_id]).execute()
        messages = result.get('messages')[:limit]

        # iterate through all the messages
        for msg in messages:
            # Get the message from its id
            txt = self._service.users().messages().get(userId='me', id=msg['id']).execute()

            # Use try-except to avoid any Errors
            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']

                # Look for Subject and Sender Email in the headers
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        sender = d['value']

                # The Body of the message is in Encrypted format. So, we have to decode it.
                # Get the data and decode it with base 64 decoder.
                parts = payload.get('parts')[0]
                data = parts['body']['data']
                data = data.replace("-", "+").replace("_", "/")
                decoded_data = base64.b64decode(data)

                # Now, the data obtained is in lxml. So, we will parse
                # it with BeautifulSoup library
                soup = BeautifulSoup(decoded_data, "lxml")
                body = soup.body()

                # Printing the subject, sender's email and message
                print("Subject: ", subject)
                print("From: ", sender)
                print("Message: ", body)
                print('\n')
            except Exception as ex:
                print(f"error - {ex}")

