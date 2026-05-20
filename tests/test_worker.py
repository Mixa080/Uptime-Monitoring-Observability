import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from worker import ping_url

@pytest.mark.asyncio
async def test_ping_url_success():
    mock_session = MagicMock()
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_session.get.return_value.__aenter__.return_value = mock_response

    with patch('worker.save_ping_result') as mock_save:
        await ping_url(mock_session, "http://example.com")
        mock_save.assert_called_once()
        args = mock_save.call_args[0]
        assert args[0] == "http://example.com"
        assert args[1] == 200
        assert args[2] >= 0

@pytest.mark.asyncio
async def test_ping_url_failure():
    mock_session = MagicMock()
    mock_session.get.side_effect = Exception("Network error")

    with patch('worker.save_ping_result') as mock_save:
        await ping_url(mock_session, "http://error.com")
        mock_save.assert_called_once()
        args = mock_save.call_args[0]
        assert args[0] == "http://error.com"
        assert args[1] == 0
