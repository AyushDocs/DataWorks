from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from DataWorks.logger import logging
from dataclasses import dataclass
from DataWorks.api.EmbeddingsGenerator import EmbeddingsGenerator
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
        embeddings= EmbeddingsGenerator(comments).generate_embeddings()
        similarity_matrix = cosine_similarity(embeddings)
        np.fill_diagonal(similarity_matrix, -np.inf)
        i, j = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
        return comments[i],comments[j]