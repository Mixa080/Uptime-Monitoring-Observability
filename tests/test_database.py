import os
import sqlite3
import pytest
from database import init_db, save_ping_result, get_last_results, get_all_urls
import database

TEST_DB_PATH = "test_monitor.db"

@pytest.fixture(autouse=True)
def setup_db():
    database.DB_PATH = TEST_DB_PATH
    init_db()
    yield
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except PermissionError:
            pass

def test_init_db():
    assert os.path.exists(TEST_DB_PATH)
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ping_results'")
    assert cursor.fetchone() is not None
    conn.close()

def test_save_ping_result():
    save_ping_result("http://example.com", 200, 150.5)
    results = get_last_results("http://example.com", 1)
    assert len(results) == 1
    assert results[0][0] == 200
    assert results[0][1] == 150.5

def test_get_last_results():
    save_ping_result("http://example.com", 200, 100.0)
    save_ping_result("http://example.com", 500, 200.0)
    save_ping_result("http://example.com", 200, 150.0)
    
    results = get_last_results("http://example.com", 2)
    assert len(results) == 2
    assert results[0][0] == 200 # most recent (inserted last)
    assert results[1][0] == 500

def test_get_all_urls():
    save_ping_result("http://example.com", 200, 100.0)
    save_ping_result("http://test.com", 200, 100.0)
    urls = get_all_urls()
    assert set(urls) == {"http://example.com", "http://test.com"}
