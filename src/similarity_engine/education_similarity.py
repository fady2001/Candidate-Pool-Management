from difflib import SequenceMatcher as SM
from typing import Dict, List

from loguru import logger

from src.similarity_engine.base_similarity_metric import BaseSimilarityMetric
from src.similarity_engine.data_models import JobContext


class EducationSimilarityMetric(BaseSimilarityMetric):
    """Education similarity calculation"""

    def calculate(self, candidate: Dict, job_context: JobContext) -> float:
        """Calculate education similarity using cached job requirements"""
        try:
            candidate_education = candidate.get("education", []) or []
            job_education_requirements = job_context.education_requirements

            if not job_education_requirements:
                return 0.8

            if not candidate_education:
                return 0.0

            candidate_degrees = []
            candidate_fields = []

            for edu in candidate_education:
                if isinstance(edu, dict):
                    degree = edu.get("degree", "")
                    field = edu.get("field_of_study", "")
                    if degree:
                        candidate_degrees.append(degree.lower())
                    if field:
                        candidate_fields.append(field.lower())

            education_score = 0.0
            total_requirements = len(job_education_requirements)

            for requirement in job_education_requirements:
                req_lower = requirement.lower()
                degree_match = any(
                    SM(None, req_lower, deg).ratio() > 0.7 for deg in candidate_degrees
                )
                field_match = any(
                    SM(None, req_lower, field).ratio() > 0.7 for field in candidate_fields
                )

                if degree_match or field_match:
                    education_score += 1.0

            return education_score / max(total_requirements, 1)

        except Exception as e:
            logger.error(f"Error calculating education similarity: {e}")
            return 0.0

    @staticmethod
    def extract_job_education_requirements(job: Dict) -> List[str]:
        """Extract education requirements from job data - static method for caching"""
        return job.get("education_requirements", []) or []
