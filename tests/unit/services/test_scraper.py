import pytest
from services.job_scraper.providers.linkedin import LinkedInScraper
from services.job_scraper.providers.indeed import IndeedScraper
from services.job_scraper.providers.bdjobs import BdJobsScraper
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_linkedin_scraper():
    mock_repository = Mock()
    mock_proxy_manager = Mock()
    scraper = LinkedInScraper(mock_repository, mock_proxy_manager)
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text.return_value = '<html><body></body></html>'
        
        jobs = await scraper.search_jobs('python developer', 'Remote')
        assert isinstance(jobs, list)

@pytest.mark.asyncio
async def test_indeed_scraper():
    mock_repository = Mock()
    mock_proxy_manager = Mock()
    scraper = IndeedScraper(mock_repository, mock_proxy_manager)
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text.return_value = '<html><body></body></html>'
        
        jobs = await scraper.search_jobs('software engineer', 'Dhaka')
        assert isinstance(jobs, list)