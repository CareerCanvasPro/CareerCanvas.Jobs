from datetime import datetime, timedelta
from .repository import JobRepository
from .cache import CacheManager
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class DataLifecycleManager:
    def __init__(self, repository: JobRepository, cache: CacheManager):
        self.repository = repository
        self.cache = cache

    async def cleanup_old_jobs(self, days: int = 30) -> int:
        try:
            cutoff = datetime.utcnow() - timedelta(days=days)
            updated = await self.repository.deactivate_old_jobs(days)
            await self.cache.clear_pattern("jobs:*")
            logger.info(f"Deactivated {updated} jobs older than {days} days")
            return updated
        except Exception as e:
            logger.error(f"Error during job cleanup: {str(e)}")
            raise

    async def archive_jobs(self, months: int = 6):
        try:
            cutoff = datetime.utcnow() - timedelta(days=months * 30)
            archived = await self.repository.archive_jobs_before_date(cutoff)
            logger.info(f"Archived {archived} jobs older than {months} months")
            return archived
        except Exception as e:
            logger.error(f"Error during job archival: {str(e)}")
            raise