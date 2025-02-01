import os 
import requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from DataWorks.logger import logging
from dataclasses import dataclass

@dataclass
class SimilarCommentFinder:
    input_file:str
    output_file:str

    def find_comments(self):
        comm1,comm2 = self.get_most_similar_two_comments()
        with open(self.output_file, "w") as f:
            f.write(f"{comm1}{comm2}")
        logging.info("Found and wrote most similar comments")

    def get_most_similar_two_comments(self):
        input_file = self.input_file
        with open(input_file, "r") as f:
            comments = f.readlines()
        url = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}",
            "Content-Type": "application/json",
        }
        data = {"model": "text-embedding-3-small", "input": comments}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        embeddings = [item["embedding"] for item in response_json["data"]]
        if not embeddings:
            return None, None, None
        similarity_matrix = cosine_similarity(embeddings)
        np.fill_diagonal(similarity_matrix, -np.inf)
        i, j = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
        return comments[i],comments[j]