import requests
from dataclasses import dataclass
from DataWorks.logger import logging

@dataclass
class WebsiteScraper:
    url: str

    def scrape(self) -> str:
        logging.info(f"Scraping website: {self.url}")
        response = requests.get(self.url)
        response.raise_for_status()

        logging.info("Website scraped successfully")
        return response.text if response.status_code == 200 else ""
