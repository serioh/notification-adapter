from gmail.email_service import create_message


def test_create_message() -> None:
    try:
        message = create_message('sender', ['to'], 'subject', 'message_text')
        assert message is not None
    except Exception as exc:
        assert False
