from .base import JobAPIException

class ScraperException(JobAPIException):
    def __init__(self, message: str, error_code: str = "SCRAPER_ERROR", status_code: int = 500):
        super().__init__(message, error_code, status_code)

class ProxyError(ScraperException):
    def __init__(self, message: str = "Proxy connection failed"):
        super().__init__(message, "PROXY_ERROR", 503)

class RateLimitError(ScraperException):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, "RATE_LIMIT_ERROR", 429)

class ValidationError(ScraperException):
    def __init__(self, message: str = "Invalid job data"):
        super().__init__(message, "VALIDATION_ERROR", 422)