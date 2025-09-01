from typing import Dict

from loguru import logger

from src.backend.similarity_engine.base_similarity_metric import BaseSimilarityMetric
from src.backend.similarity_engine.data_models import JobContext


class SenioritySimilarityMetric(BaseSimilarityMetric):
    """Seniority level compatibility calculation"""

    def calculate(self, candidate: Dict, job_context: JobContext) -> float:
        """Calculate seniority level compatibility using cached job data"""
        try:
            candidate_years = candidate.get("years_of_experience", 0) or 0
            job_seniority = job_context.seniority_level.lower()
            job_min_years = job_context.min_years_experience

            seniority_ranges = {
                "entry-level": (0, 2),
                "junior": (0, 3),
                "mid-level": (3, 7),
                "senior": (7, 15),
                "executive": (15, 100),
                "lead": (5, 100),
                "principal": (10, 100),
            }

            if job_seniority in seniority_ranges:
                min_years, max_years = seniority_ranges[job_seniority]
                if min_years <= candidate_years <= max_years:
                    return 1.0
                elif candidate_years < min_years:
                    return max(0.3, candidate_years / max(min_years, 1))
                else:
                    return max(0.7, 1.0 - (candidate_years - max_years) * 0.05)

            if job_min_years > 0:
                if candidate_years >= job_min_years:
                    return 1.0
                else:
                    return max(0.3, candidate_years / job_min_years)

            return 0.8

        except Exception as e:
            logger.error(f"Error calculating seniority match: {e}")
            return 0.8
