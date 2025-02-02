import pytest
from services.shared.utils.proxy_manager import ProxyManager

@pytest.mark.asyncio
async def test_proxy_manager():
    proxy_list = [
        "http://proxy1.example.com:8080",
        "http://proxy2.example.com:8080",
        "http://proxy3.example.com:8080"
    ]
    
    manager = ProxyManager(proxy_list)
    proxy = await manager.get_proxy()
    assert proxy in proxy_list
    
    await manager.mark_proxy_failed(proxy)
    new_proxy = await manager.get_proxy()
    assert new_proxy != proxy