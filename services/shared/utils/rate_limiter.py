import asyncio
from datetime import datetime, timedelta
from typing import Dict, List

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[datetime]] = {}

    async def wait_if_needed(self, domain: str):
        now = datetime.utcnow()
        if domain not in self.requests:
            self.requests[domain] = []

        # Clean old requests
        self.requests[domain] = [
            req_time for req_time in self.requests[domain]
            if now - req_time < timedelta(minutes=1)
        ]

        if len(self.requests[domain]) >= self.requests_per_minute:
            sleep_time = 60 - (now - self.requests[domain][0]).seconds
            await asyncio.sleep(sleep_time)
            self.requests[domain] = self.requests[domain][1:]

        self.requests[domain].append(now)