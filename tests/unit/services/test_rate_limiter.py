import pytest
from services.shared.utils.rate_limiter import RateLimiter
import asyncio

@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = RateLimiter(requests_per_minute=2)
    domain = "example.com"
    
    # First two requests should be immediate
    await limiter.wait_if_needed(domain)
    await limiter.wait_if_needed(domain)
    
    # Third request should be delayed
    start_time = asyncio.get_event_loop().time()
    await limiter.wait_if_needed(domain)
    elapsed = asyncio.get_event_loop().time() - start_time
    
    assert elapsed >= 30  # Should wait at least 30 seconds