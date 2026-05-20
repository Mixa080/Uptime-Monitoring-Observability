import sqlite3

DB_PATH = "monitor.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ping_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status_code INTEGER,
            ttfb_ms REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_ping_result(url: str, status_code: int, ttfb_ms: float):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ping_results (url, status_code, ttfb_ms)
        VALUES (?, ?, ?)
    ''', (url, status_code, ttfb_ms))
    conn.commit()
    conn.close()

def get_last_results(url: str, limit: int = 3):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT status_code, ttfb_ms, timestamp FROM ping_results
        WHERE url = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (url, limit))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_urls():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT url FROM ping_results')
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results
