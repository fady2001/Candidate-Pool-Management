from difflib import SequenceMatcher as SM
from typing import Dict, List, Set

from loguru import logger

from src.similarity_engine.base_similarity_metric import BaseSimilarityMetric
from src.similarity_engine.data_models import JobContext


class SkillsSimilarityMetric(BaseSimilarityMetric):
    """Skills similarity calculation using Jaccard index with fuzzy string matching"""

    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold

    def calculate(self, candidate: Dict, job_context: JobContext) -> float:
        """Calculate skills similarity using cached job skills"""
        try:
            candidate_skills = self._extract_candidate_skills(candidate)
            required_skills = job_context.required_skills

            if not required_skills:
                logger.info("No required skills found for job")
                return 0.8

            if not candidate_skills:
                logger.info("No skills found for candidate")
                return 0.0

            matched_skills = self._fuzzy_match_skills(candidate_skills, required_skills)
            intersection_size = len(matched_skills)
            union_size = len(set(candidate_skills) | set(required_skills))

            if union_size == 0:
                return 0.0

            jaccard_score = intersection_size / union_size
            logger.info(
                f"Skills similarity - Matched: {intersection_size}, Union: {union_size}, Jaccard: {jaccard_score:.4f}"
            )
            return min(jaccard_score, 1.0)

        except Exception as e:
            logger.error(f"Error calculating skills similarity: {e}")
            return 0.0

    def _extract_candidate_skills(self, candidate: Dict) -> List[str]:
        """Extract all skills from candidate data"""
        skills = []
        candidate_skills = candidate.get("skills", []) or []

        for skill_category in candidate_skills:
            if isinstance(skill_category, dict):
                if "skills" in skill_category:
                    skills.extend(skill_category["skills"])
                elif "name" in skill_category:
                    skills.append(skill_category["name"])
            elif isinstance(skill_category, str):
                skills.append(skill_category)

        return [skill for skill in skills if skill and isinstance(skill, str)]

    @staticmethod
    def extract_job_required_skills(job: Dict) -> List[str]:
        """Extract required skills from job data - static method for caching"""
        skills = []
        skill_fields = ["required_skills", "skills", "technical_skills", "core_skills"]

        for field in skill_fields:
            job_skills = job.get(field, []) or []
            for skill_category in job_skills:
                if isinstance(skill_category, dict):
                    if "requirements" in skill_category:
                        skills.extend(skill_category["requirements"])
                    elif "skills" in skill_category:
                        skills.extend(skill_category["skills"])
                    elif "name" in skill_category:
                        skills.append(skill_category["name"])
                elif isinstance(skill_category, str):
                    skills.append(skill_category)

        return [skill for skill in skills if skill and isinstance(skill, str)]

    def _fuzzy_match_skills(
        self, candidate_skills: List[str], required_skills: List[str]
    ) -> Set[str]:
        """Find fuzzy matches between candidate skills and required skills"""
        matched_skills = set()

        for required_skill in required_skills:
            if required_skill in candidate_skills:
                matched_skills.add(required_skill)
                continue

            best_match_ratio = 0
            for candidate_skill in candidate_skills:
                similarity = SM(None, required_skill, candidate_skill).ratio()
                if similarity > best_match_ratio:
                    best_match_ratio = similarity

                if similarity >= self.threshold:
                    matched_skills.add(required_skill)
                    logger.debug(
                        f"Fuzzy match found: '{required_skill}' <-> '{candidate_skill}' (similarity: {similarity:.3f})"
                    )
                    break

            if required_skill not in matched_skills:
                logger.debug(
                    f"No match for required skill: '{required_skill}' (best similarity: {best_match_ratio:.3f})"
                )

        return matched_skills
