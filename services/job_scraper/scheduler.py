import asyncio
from typing import List, Dict
from datetime import datetime
import aioschedule
from .providers.linkedin import LinkedInScraper
from .providers.indeed import IndeedScraper
from .providers.bdjobs import BdJobsScraper
from services.shared.utils.logger import setup_logger

class JobScraperScheduler:
    def __init__(self, repository, proxy_manager):
        self.logger = setup_logger(__name__)
        self.scrapers = {
            'linkedin': LinkedInScraper(repository, proxy_manager),
            'indeed': IndeedScraper(repository, proxy_manager),
            'bdjobs': BdJobsScraper(repository, proxy_manager)
        }
        self.search_configs = [
            {'keyword': 'python developer', 'location': 'Remote'},
            {'keyword': 'software engineer', 'location': 'Bangladesh'},
            {'keyword': 'web developer', 'location': 'Dhaka'}
        ]

    async def run_scraper(self, scraper_name: str):
        try:
            scraper = self.scrapers[scraper_name]
            for config in self.search_configs:
                jobs = await scraper.search_jobs(**config)
                for job in jobs:
                    await scraper.process_job(job)
        except Exception as e:
            self.logger.error(f"Error running {scraper_name} scraper: {str(e)}")

    async def start(self):
        aioschedule.every(4).hours.do(self.run_scraper, 'linkedin')
        aioschedule.every(6).hours.do(self.run_scraper, 'indeed')
        aioschedule.every(8).hours.do(self.run_scraper, 'bdjobs')

        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(60)