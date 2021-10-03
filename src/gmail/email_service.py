import base64
import os.path
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

from src.utils import get_project_root

load_dotenv()


ROOT_DIR = get_project_root()
credentials_path = os.path.join(ROOT_DIR, "credentials.json")
token_path = os.path.join(ROOT_DIR, os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


class EmailService:
    def __init__(self, gmail_client: Resource) -> None:
        super().__init__()
        self._gmail_client = gmail_client

    @staticmethod
    def _create_message(
        recipients: list[str], subject: str, html_message: str
    ) -> dict[str, str]:
        """Create a message for an email.

        Args:
            recipients: Email addresses of the recipients.
            subject: The subject of the email message.
            html_message: The text of the email message.

        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEMultipart("alternative")
        message["to"] = ", ".join(recipients)
        message["from"] = "me"
        message["subject"] = subject
        part1 = MIMEText(html_message, "html")
        message.attach(part1)
        return {"raw": base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_email(self, recipients: list[str], subject: str, html_message: str) -> str:
        """Send email using the gmail API.

        Args:
            recipients: Email addresses of the recipients.
            subject: The subject of the email message.
            html_message: The text of the email message.

        Returns:
            The response from the Google API.
        """
        message = self._create_message(recipients, subject, html_message)

        google_response = (
            self._gmail_client.users()
            .messages()
            .send(userId="me", body=message)
            .execute()
        )
        response: str = f"Message Id: {google_response['id']}"
        return response


def authenticate_with_gmail() -> Resource:
    """Authenticates with the Gmail API using local credentials files."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in, or refresh the credentials if
    # credentials.json is present.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)
