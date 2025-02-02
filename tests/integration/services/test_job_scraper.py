import pytest
from services.job_scraper.scheduler import JobScraperScheduler
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_scheduler():
    mock_repository = Mock()
    mock_proxy_manager = Mock()
    
    scheduler = JobScraperScheduler(mock_repository, mock_proxy_manager)
    
    with patch('services.job_scraper.providers.linkedin.LinkedInScraper.search_jobs') as mock_search:
        mock_search.return_value = [
            {
                'title': 'Test Job',
                'company': 'Test Company',
                'location': 'Remote',
                'job_url': 'https://example.com/job/1',
                'source_site': 'LinkedIn'
            }
        ]
        
        await scheduler.run_scraper('linkedin')
        assert mock_search.called
        assert mock_repository.create_job.called