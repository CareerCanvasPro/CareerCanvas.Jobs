from ..base_scraper import BaseScraper
from typing import List, Dict, Any
import aiohttp
from bs4 import BeautifulSoup
from services.shared.utils.proxy_manager import ProxyManager

class LinkedInScraper(BaseScraper):
    def __init__(self, repository, proxy_manager: ProxyManager):
        super().__init__(repository)
        self.proxy_manager = proxy_manager
        self.base_url = "https://www.linkedin.com/jobs/search"
        
    async def search_jobs(self, 
                         keyword: str, 
                         location: str = None, 
                         job_type: str = None) -> List[Dict[str, Any]]:
        try:
            params = {
                "keywords": keyword,
                "location": location,
                "f_WT": "2" if job_type == "REMOTE" else None,
                "sortBy": "DD"
            }
            
            proxy = await self.proxy_manager.get_proxy()
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.base_url, 
                    params=params,
                    proxy=proxy,
                    headers=self._get_headers()
                ) as response:
                    if response.status != 200:
                        self.logger.error(f"LinkedIn search failed: {response.status}")
                        return []
                        
                    html = await response.text()
                    return self._parse_search_results(html)
                    
        except Exception as e:
            self.logger.error(f"Error searching LinkedIn jobs: {str(e)}")
            return []
            
    async def extract_job_details(self, job_url: str) -> Dict[str, Any]:
        try:
            proxy = await self.proxy_manager.get_proxy()
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    job_url,
                    proxy=proxy,
                    headers=self._get_headers()
                ) as response:
                    if response.status != 200:
                        return None
                        
                    html = await response.text()
                    return self._parse_job_details(html)
                    
        except Exception as e:
            self.logger.error(f"Error extracting job details from {job_url}: {str(e)}")
            return None
            
    def _get_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
    def _parse_search_results(self, html: str) -> List[Dict[str, Any]]:
        jobs = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for job_card in soup.select('.job-search-card'):
            try:
                jobs.append({
                    'title': job_card.select_one('.job-title').text.strip(),
                    'company': job_card.select_one('.company-name').text.strip(),
                    'location': job_card.select_one('.job-location').text.strip(),
                    'job_url': job_card.select_one('a.job-link')['href'],
                    'source_site': 'LinkedIn'
                })
            except Exception as e:
                self.logger.warning(f"Error parsing job card: {str(e)}")
                continue
                
        return jobs