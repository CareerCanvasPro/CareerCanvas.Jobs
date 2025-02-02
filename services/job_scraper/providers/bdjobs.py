from ..base_scraper import BaseScraper
from typing import List, Dict, Any
import aiohttp
from bs4 import BeautifulSoup
from services.shared.utils.proxy_manager import ProxyManager

class BdJobsScraper(BaseScraper):
    def __init__(self, repository, proxy_manager: ProxyManager):
        super().__init__(repository)
        self.proxy_manager = proxy_manager
        self.base_url = "https://jobs.bdjobs.com/jobsearch.asp"
        
    async def search_jobs(self, keyword: str, location: str = None, job_type: str = None) -> List[Dict[str, Any]]:
        try:
            params = {
                'fcatId': '',
                'keyword': keyword,
                'location': location or '',
                'worktype': '3' if job_type == "REMOTE" else ''
            }
            
            proxy = await self.proxy_manager.get_proxy()
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, proxy=proxy, headers=self._get_headers()) as response:
                    if response.status != 200:
                        self.logger.error(f"BdJobs search failed: {response.status}")
                        return []
                    html = await response.text()
                    return self._parse_search_results(html)
                    
        except Exception as e:
            self.logger.error(f"Error searching BdJobs: {str(e)}")
            return []
            
    def _parse_search_results(self, html: str) -> List[Dict[str, Any]]:
        jobs = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for job_card in soup.select('.job-title-text'):
            try:
                company_elem = job_card.find_next('div', class_='company-name')
                location_elem = job_card.find_next('div', class_='location-name')
                
                jobs.append({
                    'title': job_card.text.strip(),
                    'company': company_elem.text.strip() if company_elem else 'Unknown',
                    'location': location_elem.text.strip() if location_elem else 'Bangladesh',
                    'job_url': 'https://jobs.bdjobs.com' + job_card.parent['href'],
                    'source_site': 'BdJobs'
                })
            except Exception as e:
                self.logger.warning(f"Error parsing BdJobs job card: {str(e)}")
                continue
                
        return jobs