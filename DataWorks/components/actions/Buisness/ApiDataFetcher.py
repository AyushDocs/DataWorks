import requests
from dataclasses import dataclass
from DataWorks.logger import logging

@dataclass
class ApiDataFetcher:
    api_url: str
    headers: dict = None
    params: dict = None
    output_file: str = None

    def fetch(self) -> dict:
        logging.info(f"Fetching data from API: {self.api_url}")
        response = requests.get(self.api_url, headers=self.headers, params=self.params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        if self.output_file:
            with open(self.output_file, "w") as f:
                f.write(response.text)

            logging.info(f"Data successfully fetched and saved to {self.output_file}")

        return response.json()
