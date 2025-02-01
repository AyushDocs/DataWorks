import requests
import os
from typing import List
from dataclasses import dataclass

@dataclass
class EmbeddingsGenerator:
    comments:List[str]
    def generate_embeddings(self):
        url = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}",
            "Content-Type": "application/json",
        }
        data = {"model": "text-embedding-3-small", "input": self.comments}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        return [item["embedding"] for item in response_json["data"]]