import httpx
from .config import settings


class StreamerProxyClient:
    def __init__(self) -> None:
        self.base_url = settings.streamer_proxy_url.rstrip('/')
        self.headers = {'X-Api-Key': settings.streamer_proxy_api_key}

    async def health(self) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f'{self.base_url}/health')
            response.raise_for_status()
            return response.json()

    async def get_twitch_auth_url(self) -> str | None:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(f'{self.base_url}/twitch/auth-url', headers=self.headers)
            response.raise_for_status()
            data = response.json()
        if isinstance(data, dict):
            return data.get('auth_url') or data.get('url') or data.get('redirect_url')
        return None

    async def get_twitch_me(self) -> dict:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(f'{self.base_url}/twitch/me', headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def setup_twitch(self) -> dict:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(f'{self.base_url}/twitch/setup', headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def get_chatters(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(f'{self.base_url}/chatters', headers=self.headers)
            response.raise_for_status()
            return response.json().get('data', [])

    async def get_dota_status(self) -> dict:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(f'{self.base_url}/dota/status', headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def connect_dota(self, steam_guard_code: str | None = None) -> dict:
        payload = {'steam_guard_code': steam_guard_code} if steam_guard_code else {}
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f'{self.base_url}/dota/connect', headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def get_lobby(self) -> dict:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(f'{self.base_url}/dota/lobby', headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def invite(self, steam_id: str) -> dict:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(f'{self.base_url}/dota/invite', headers=self.headers, json={'steam_id': steam_id})
            response.raise_for_status()
            return response.json()


streamer_proxy = StreamerProxyClient()
