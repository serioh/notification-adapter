import os
from unittest.mock import MagicMock

import pytest
from callee import Any, IsA

from src.api import app

from fastapi.testclient import TestClient

client = TestClient(app)


email_example = """
<h1>Hello</h1>
<p>This is a test :)</p>
"""

API_KEY = os.getenv("API_KEY")


@pytest.mark.parametrize(
    "test_email,recipients,expected_status_code",
    [(email_example, ["frodo@baggins.com", "sam@gamgee.io"], 201)],
)
def test_send_email(
    gmail_client: MagicMock,
    test_email: str,
    recipients: list[str],
    expected_status_code: int,
):
    mock_response = MagicMock({"id": "test"})

    gmail_client.users().messages().send(
        userId=IsA(str), body=IsA(str)
    ).execute().return_value = mock_response

    uri = "/send-email"
    for idx, recipient in enumerate(recipients):
        if idx == 0:
            uri += f"?recipients={recipient}"
        else:
            uri += f"&recipients={recipient}"

    # TODO: Fix dependency injection here...
    # response = client.post(
    #     uri,
    #     data=test_email,
    #     headers={
    #         "X-API-KEY": API_KEY,
    #         "SUBJECT-LINE": "TEST",
    #     },
    # )
    #
    # assert response.status_code == 201
    # assert response.json() == {"response": IsA(str)}
