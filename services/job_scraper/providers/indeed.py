from ..base_scraper import BaseScraper
from typing import List, Dict, Any
import aiohttp
from bs4 import BeautifulSoup
from services.shared.utils.proxy_manager import ProxyManager

class IndeedScraper(BaseScraper):
    def __init__(self, repository, proxy_manager: ProxyManager):
        super().__init__(repository)
        self.proxy_manager = proxy_manager
        self.base_url = "https://www.indeed.com/jobs"
        
    async def search_jobs(self, keyword: str, location: str = None, job_type: str = None) -> List[Dict[str, Any]]:
        try:
            params = {
                "q": keyword,
                "l": location,
                "remote": "1" if job_type == "REMOTE" else None,
                "sort": "date"
            }
            
            proxy = await self.proxy_manager.get_proxy()
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, proxy=proxy, headers=self._get_headers()) as response:
                    if response.status != 200:
                        self.logger.error(f"Indeed search failed: {response.status}")
                        return []
                    html = await response.text()
                    return self._parse_search_results(html)
                    
        except Exception as e:
            self.logger.error(f"Error searching Indeed jobs: {str(e)}")
            return []
            
    def _parse_search_results(self, html: str) -> List[Dict[str, Any]]:
        jobs = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for job_card in soup.select('.job_seen_beacon'):
            try:
                jobs.append({
                    'title': job_card.select_one('h2.jobTitle').text.strip(),
                    'company': job_card.select_one('span.companyName').text.strip(),
                    'location': job_card.select_one('div.companyLocation').text.strip(),
                    'job_url': 'https://www.indeed.com' + job_card.select_one('a.jcs-JobTitle')['href'],
                    'source_site': 'Indeed'
                })
            except Exception as e:
                self.logger.warning(f"Error parsing Indeed job card: {str(e)}")
                continue
                
        return jobs