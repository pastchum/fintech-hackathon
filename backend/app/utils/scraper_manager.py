import asyncio
from app.utils.subprocess_manager import SubprocessManager
# this is the class that will manage the different scrapers
class ScraperManager:
    def __init__(self, scraper_type="default"):
        self.scraper_type = scraper_type
        self.scraper_scripts = {
            "default": "default_scraper.py",
            "advanced": "advanced_scraper.py",
            "company": "company_scraper.py",
        }

    async def run_scraper(self, prompt, source_url):
        """
        Run the selected scraper asynchronously.
        """
        if self.scraper_type not in self.scraper_scripts:
            raise ValueError(f"Unknown scraper type: {self.scraper_type}")

        subprocess_manager = SubprocessManager(self.scraper_scripts[self.scraper_type])
        return await subprocess_manager.run(prompt, source_url)
