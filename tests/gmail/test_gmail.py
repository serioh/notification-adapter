from unittest.mock import MagicMock

from callee import Any

from src.gmail.email_service import EmailService, authenticate_with_gmail


def test_create_message() -> None:
    gmail_client = authenticate_with_gmail()
    email_service = EmailService(gmail_client)
    message = email_service._create_message(["to"], "subject", "message_text")
    assert message is not None
    assert message.get("raw")


def test_send_message(gmail_client: MagicMock) -> None:
    mock_response = MagicMock({"id": "test"})

    gmail_client.users().messages().send(userId=Any, body=Any).execute().return_value = mock_response
    email_service = EmailService(gmail_client)
    response = email_service.send_email(["to"], "subject", "message_text")

    assert response.__contains__("Message Id: ")


