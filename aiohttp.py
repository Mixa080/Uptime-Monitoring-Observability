# Dummy aiohttp to satisfy imports for tests since it cannot be installed on Python 3.14 without MSVC tools

class ClientSession:
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
