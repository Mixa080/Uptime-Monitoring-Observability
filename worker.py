import asyncio
import aiohttp
import time
from database import save_ping_result, init_db

URLS_TO_PING = [
    "https://google.com",
    "https://nonexistent-site.xyz"
]

async def ping_url(session, url):
    start_time = time.monotonic()
    try:
        async with session.get(url, timeout=5) as response:
            status_code = response.status
            await response.read()
            ttfb_ms = (time.monotonic() - start_time) * 1000
    except Exception as e:
        status_code = 0
        ttfb_ms = 0.0

    save_ping_result(url, status_code, ttfb_ms)
    print(f"Pinged {url}: status {status_code}, ttfb {ttfb_ms:.2f}ms")

async def worker_loop():
    init_db()
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [ping_url(session, url) for url in URLS_TO_PING]
            await asyncio.gather(*tasks)
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(worker_loop())
