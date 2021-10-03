from unittest.mock import MagicMock

import pytest


@pytest.fixture
def gmail_client() -> MagicMock:
    return MagicMock()
