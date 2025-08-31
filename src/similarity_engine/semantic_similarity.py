from typing import Dict

from langchain_core.vectorstores import InMemoryVectorStore
from loguru import logger

from src.similarity_engine.base_similarity_metric import BaseSimilarityMetric
from src.similarity_engine.data_models import JobContext
from src.utils import get_embedding_model


class SemanticSimilarityMetric(BaseSimilarityMetric):
    """Semantic similarity calculation using embeddings"""

    def __init__(self, embeddings=None):
        self.embeddings = embeddings or get_embedding_model()

    def calculate(self, candidate: Dict, job_context: JobContext) -> float:
        """Calculate semantic similarity using cached job summary"""
        try:
            candidate_summary = candidate.get("summary")
            job_summary = job_context.job_summary

            if not candidate_summary or not job_summary:
                return 0.5

            vector_store = InMemoryVectorStore(self.embeddings)
            documents = [job_summary]
            vector_store.add_texts(texts=documents, metadatas=[{"type": "job"}])

            similarity_results = vector_store.similarity_search_with_score(
                query=candidate_summary, k=1
            )

            if similarity_results:
                _, distance_score = similarity_results[0]
                similarity_score = max(0.0, 1.0 - (distance_score / 2.0))
                return min(similarity_score, 1.0)

            return 0.5

        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {e}")
            return 0.5
