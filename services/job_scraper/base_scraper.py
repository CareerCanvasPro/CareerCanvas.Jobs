from abc import ABC, abstractmethod
from typing import List, Dict, Any
from services.shared.database.repository import JobRepository
from services.shared.utils.logger import setup_logger
from datetime import datetime
from services.shared.exceptions.scraper import ScraperException, ProxyError, RateLimitError, ValidationError
from .validators import ScrapedJobValidator

class BaseScraper(ABC):
    def __init__(self, repository: JobRepository):
        self.repository = repository
        self.logger = setup_logger(self.__class__.__name__)

    @abstractmethod
    async def search_jobs(self, 
                         keyword: str, 
                         location: str = None, 
                         job_type: str = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def extract_job_details(self, job_url: str) -> Dict[str, Any]:
        pass

    async def process_job(self, job_data: Dict[str, Any]) -> bool:
        try:
            # Validate job data
            validated_data = ScrapedJobValidator(**job_data).dict(exclude_none=True)
            
            # Check for existing job
            existing_job = await self.repository.get_job_by_url(validated_data['job_url'])
            if existing_job:
                self.logger.info(f"Job already exists: {validated_data['job_url']}")
                return False

            # Add metadata
            validated_data['date_scraped'] = datetime.utcnow()
            
            # Save to database
            await self.repository.create_job(validated_data)
            self.logger.info(f"Successfully processed job: {validated_data['job_url']}")
            return True
            
        except ValidationError as e:
            self.logger.warning(f"Invalid job data: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error processing job: {str(e)}")
            raise ScraperException(f"Failed to process job: {str(e)}")