import base64
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

path_to_here = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(path_to_here, 'credentials.json')
token_path = os.path.join(path_to_here, 'token.json')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def authenticate() -> Any:
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def create_message(sender: str, recipients: list[str], subject: str, message_text: str) -> dict[str, str]:
    """Create a message for an email.

  Args:
    sender: Email address of the sender.
    recipients: Email addresses of the recipients.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
    message = MIMEMultipart('alternative')
    message['to'] = ", ".join(recipients)
    message['from'] = sender
    message['subject'] = subject
    part1 = MIMEText(message_text, 'html')
    message.attach(part1)
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service: Any, user_id: str, message: dict[str, str]) -> str:
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        google_response = service.users().messages().send(userId=user_id, body=message).execute()
        response: str = f"Message Id: {google_response['id']}"
        print(response)
        return response
    except errors.HttpError as error:
        print(f"An error occurred: {error}")
