import aiohttp
from typing import List, Optional
import random
import asyncio

class ProxyManager:
    def __init__(self, proxy_list: List[str]):
        self.proxies = proxy_list
        self.working_proxies = set(proxy_list)
        self.failed_proxies = set()
        self.lock = asyncio.Lock()

    async def get_proxy(self) -> Optional[str]:
        async with self.lock:
            if not self.working_proxies:
                await self._refresh_proxies()
            return random.choice(list(self.working_proxies)) if self.working_proxies else None

    async def mark_proxy_failed(self, proxy: str):
        async with self.lock:
            self.working_proxies.discard(proxy)
            self.failed_proxies.add(proxy)

    async def _refresh_proxies(self):
        self.working_proxies = set(self.proxies)
        self.failed_proxies.clear()