import pytest
from unittest.mock import patch
from alert import check_alerts

@patch('alert.get_all_urls')
@patch('alert.get_last_results')
def test_check_alerts_critical(mock_get_last_results, mock_get_all_urls, capsys):
    mock_get_all_urls.return_value = ["http://example.com"]
    mock_get_last_results.return_value = [(500, 100), (0, 0), (404, 120)]
    
    check_alerts()
    captured = capsys.readouterr()
    assert "[CRITICAL ALERT] http://example.com is DOWN for the last 3 checks!" in captured.out

@patch('alert.get_all_urls')
@patch('alert.get_last_results')
def test_check_alerts_ok(mock_get_last_results, mock_get_all_urls, capsys):
    mock_get_all_urls.return_value = ["http://example.com"]
    mock_get_last_results.return_value = [(200, 100), (0, 0), (404, 120)]
    
    check_alerts()
    captured = capsys.readouterr()
    assert "[CRITICAL ALERT]" not in captured.out
