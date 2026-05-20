# Sentinel Uptime Monitor

Sentinel is a lightweight, autonomous asynchronous uptime monitoring system written in Python. It pings a list of given URLs to check their availability and Time to First Byte (TTFB), logs the results into a local SQLite database, and provides a critical alerting mechanism if any website is down for consecutive checks.

## Project Architecture

The system consists of three main modules:

1. **Database Module (`database.py`)**
   Handles the local SQLite database initialization and operations. It records the ping results (status code and TTFB) and retrieves the latest logs for analysis.

2. **Async Worker (`worker.py`)**
   An asynchronous worker utilizing `aiohttp` and `asyncio`. It runs in a continuous loop, pinging predefined URLs every 60 seconds and saving the results via the database module.

3. **Alerting Module (`alert.py`)**
   Reads the database records and triggers a `[CRITICAL ALERT]` in the console if a specific website has been down (status code `0` or `>= 400`) for the last 3 consecutive checks.

## Prerequisites

- Python 3.10+
- `aiohttp`
- `pytest`
- `pytest-asyncio`

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

### Start the Worker
To start monitoring the URLs, run the worker script:

```bash
python worker.py
```

### Check Alerts
To manually verify the status of monitored websites and print alerts if necessary, run the alert script:

```bash
python alert.py
```

## Running Tests

The project is fully covered by unit tests using `pytest` and `unittest.mock`. To run the test suite:

```bash
pytest tests/
```

## License
MIT License