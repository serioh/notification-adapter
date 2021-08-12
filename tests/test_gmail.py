from gmail.email_service import authenticate, create_message


def test_authenticate():
    try:
        service = authenticate()
        assert service is not None
    except Exception as exc:
        assert False


def test_create_message():
    try:
        message = create_message('sender', 'to', 'subject', 'message_text')
        assert message is not None
    except Exception as exc:
        assert False
