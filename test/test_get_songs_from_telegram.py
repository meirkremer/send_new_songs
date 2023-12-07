from get_songs_from_telegram import order_data, connect_telegram
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_telegram_client():
    # Create a mock TelegramClient for testing
    client = Mock()
    client.iter_messages.return_value = [
        Mock(file=Mock(ext='.mp3')),
        Mock(file=Mock(ext='.jpg')),
        Mock(file=Mock(ext='.mp3')),
        Mock(file=Mock(ext='.zip')),
        Mock(file=Mock(ext='.jpg')),
    ]
    return client


def test_order_data():
    # Test the order_data function
    data = [Mock(file=Mock(ext=ext)) for ext in ['.mp3', '.jpg', '.mp3', '.zip', '.jpg']]
    print('\n', data)
    result = order_data(data)
    assert len(result) == 2
    assert isinstance(result, dict)
    assert all(isinstance(item, list) and len(item) == 2 for item in result.values())


# def test_connect_telegram(mock_telegram_client):
#     # Test the connect_telegram function with a mock client
#     songs = connect_telegram()
#     assert isinstance(songs, dict)
