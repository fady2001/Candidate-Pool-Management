from difflib import SequenceMatcher as SM
from typing import Dict, List

from loguru import logger

from src.backend.similarity_engine.base_similarity_metric import BaseSimilarityMetric
from src.backend.similarity_engine.data_models import JobContext


class EducationSimilarityMetric(BaseSimilarityMetric):
    """Education similarity calculation"""

    def calculate(self, candidate: Dict, job_context: JobContext) -> float:
        """Calculate education similarity using cached job requirements"""
        try:
            candidate_education = self._create_candidate_education_text(
                candidate.get("education", []) or []
            )
            job_education_requirements = " ".join(job_context.education_requirements)

            if not job_education_requirements:
                return 0.8

            if not candidate_education:
                return 0.0

            return SM(None, candidate_education, job_education_requirements).ratio()

        except Exception as e:
            logger.error(f"Error calculating education similarity: {e}")
            return 0.0

    def _create_candidate_education_text(self, candidate_education: List) -> str:
        """Create a text representation of candidate education for embedding"""
        education_parts = []

        for edu in candidate_education:
            if isinstance(edu, dict):
                degree = edu.get("degree", "")
                field = edu.get("field_of_study", "")

                edu_text_parts = []
                if degree:
                    edu_text_parts.append(f"Degree: {degree}")
                if field:
                    edu_text_parts.append(f"Field: {field}")

                if edu_text_parts:
                    education_parts.append(". ".join(edu_text_parts))

        return ". ".join(education_parts)

    @staticmethod
    def extract_job_education_requirements(job: Dict) -> List[str]:
        """Extract education requirements from job data - static method for caching"""
        return job.get("education_requirements", []) or []
