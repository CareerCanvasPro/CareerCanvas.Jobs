from datadog import initialize, statsd
import time
from functools import wraps

class MetricsCollector:
    def __init__(self, service_name: str):
        self.service_name = service_name
        initialize(statsd_host='localhost', statsd_port=8125)
    
    def timing(self, metric_name: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start = time.time()
                result = await func(*args, **kwargs)
                duration = time.time() - start
                statsd.timing(f"{self.service_name}.{metric_name}", duration)
                return result
            return wrapper
        return decorator