from difflib import SequenceMatcher as SM
from typing import Dict

from langchain_core.vectorstores import InMemoryVectorStore
from loguru import logger

from src.backend.similarity_engine.base_similarity_metric import BaseSimilarityMetric
from src.backend.similarity_engine.data_models import JobContext
from src.backend.utils import get_embedding_model


class ExperienceSimilarityMetric(BaseSimilarityMetric):
    """Experience similarity calculation based on years and relevance"""

    def __init__(self, embeddings=None):
        self.embeddings = embeddings or get_embedding_model()

    def calculate(self, candidate: Dict, job_context: JobContext) -> float:
        """Calculate experience similarity using cached job data"""
        candidate_years = candidate.get("years_of_experience", 0) or 0
        min_required = job_context.min_years_experience
        max_preferred = job_context.max_years_experience

        # Base score on years of experience
        if candidate_years >= min_required:
            if max_preferred and candidate_years <= max_preferred:
                years_score = 1.0
            elif max_preferred:
                years_score = max(0.8, 1.0 - (candidate_years - max_preferred) * 0.05)
            else:
                years_score = 1.0
        else:
            years_score = max(0.0, candidate_years / max(min_required, 1))

        relevance_score = self._calculate_experience_relevance(candidate, job_context)
        return (years_score * 0.6) + (relevance_score * 0.4)

    def _calculate_experience_relevance(self, candidate: Dict, job_context: JobContext) -> float:
        """Calculate relevance using cached job responsibilities text"""
        candidate_exp = candidate.get("experience", []) or []
        if not candidate_exp:
            return 0.3

        relevance_score = 0.0
        total_positions = len(candidate_exp)

        for exp in candidate_exp:
            if isinstance(exp, dict):
                position_relevance = self._calculate_position_relevance(exp, job_context)
                relevance_score += position_relevance

        return relevance_score / max(total_positions, 1)

    def _calculate_position_relevance(self, experience: Dict, job_context: JobContext) -> float:
        """Calculate relevance of a single position to the job using cached data"""
        exp_title = experience.get("job_title", "").lower()
        job_title = job_context.job_data.get("job_title", "").lower()

        title_score = 0.0
        if exp_title and job_title:
            similarity = SM(None, exp_title, job_title).ratio()
            title_score = similarity
            logger.debug(
                f"Title similarity: '{exp_title}' <-> '{job_title}' (similarity: {similarity:.3f})"
            )

        resp_score = self._calculate_responsibility_similarity(experience, job_context)
        return min((title_score * 0.6) + (resp_score * 0.4), 1.0)

    def _calculate_responsibility_similarity(
        self, experience: Dict, job_context: JobContext
    ) -> float:
        """Calculate responsibility similarity using cached vector store"""
        try:
            candidate_responsibilities = experience.get("responsibilities", [])
            if not candidate_responsibilities:
                logger.debug("No candidate responsibilities found")
                return 0.0

            candidate_resp_text = " ".join(candidate_responsibilities)

            if not job_context.job_responsibilities_text:
                logger.debug("No job context found")
                return 0.0

            # Use cached vector store if available
            if job_context.vector_store is None:
                documents = [f"Job requirements: {job_context.job_responsibilities_text}"]
                job_context.vector_store = InMemoryVectorStore(self.embeddings)
                job_context.vector_store.add_texts(
                    texts=documents, metadatas=[{"type": "job", "source": "requirements"}]
                )

            similarity_results = job_context.vector_store.similarity_search_with_score(
                query=candidate_resp_text, k=1
            )

            if similarity_results:
                _, distance_score = similarity_results[0]
                similarity_score = max(0.0, 1.0 - (distance_score / 2.0))
                logger.debug(
                    f"Responsibility similarity - Distance: {distance_score:.4f}, Similarity: {similarity_score:.4f}"
                )
                return min(similarity_score, 1.0)
            else:
                logger.debug("No similarity results found")
                return 0.0

        except Exception as e:
            logger.error(f"Error calculating responsibility similarity: {e}")
            return 0.0

    @staticmethod
    def extract_job_responsibilities_and_description(job: Dict) -> str:
        """Extract and combine job responsibilities and description - static method for caching"""
        job_text_parts = []

        job_desc = job.get("job_description", "")
        if job_desc:
            job_text_parts.append(job_desc)

        job_summary = job.get("job_summary", "")
        if job_summary:
            job_text_parts.append(job_summary)

        responsibilities = job.get("responsibilities", [])
        if responsibilities:
            job_text_parts.extend(responsibilities)

        return " ".join(job_text_parts).strip()
