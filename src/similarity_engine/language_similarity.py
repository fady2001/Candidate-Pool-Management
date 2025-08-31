from difflib import SequenceMatcher as SM
from typing import Dict, List

from loguru import logger

from src.similarity_engine.base_similarity_metric import BaseSimilarityMetric
from src.similarity_engine.data_models import JobContext


class LanguageSimilarityMetric(BaseSimilarityMetric):
    """Language similarity calculation"""

    def calculate(self, candidate: Dict, job_context: JobContext) -> float:
        """Calculate language similarity using cached job requirements"""
        try:
            candidate_languages = self._extract_candidate_languages(candidate)
            required_languages = job_context.required_languages

            if not required_languages:
                logger.debug("No language requirements found for job")
                return 0.9

            if not candidate_languages:
                logger.debug("No languages found for candidate")
                return 0.0

            total_score = 0.0
            total_requirements = len(required_languages)

            for required_lang in required_languages:
                lang_score = self._calculate_single_language_match(
                    required_lang, candidate_languages
                )
                total_score += lang_score

            language_similarity = total_score / max(total_requirements, 1)
            logger.debug(
                f"Language similarity - Required: {len(required_languages)}, Candidate has: {len(candidate_languages)}, Score: {language_similarity:.4f}"
            )
            return min(language_similarity, 1.0)

        except Exception as e:
            logger.error(f"Error calculating language similarity: {e}")
            return 0.5

    def _extract_candidate_languages(self, candidate: Dict) -> List[Dict[str, str]]:
        """Extract languages from candidate data with proficiency levels"""
        languages = []
        candidate_languages = candidate.get("languages", []) or []

        for lang in candidate_languages:
            if isinstance(lang, dict):
                language_name = lang.get("language", "").lower()
                proficiency = lang.get("proficiency", "").lower()
                if language_name:
                    languages.append({"language": language_name, "proficiency": proficiency})
            elif isinstance(lang, str):
                languages.append({"language": lang.lower(), "proficiency": "fluent"})

        return languages

    @staticmethod
    def extract_job_required_languages(job: Dict) -> List[Dict[str, str]]:
        """Extract required languages from job data - static method for caching"""
        languages = []
        lang_fields = ["required_languages", "languages", "language_requirements"]

        for field in lang_fields:
            job_languages = job.get(field, []) or []
            for lang in job_languages:
                if isinstance(lang, dict):
                    language_name = lang.get("language", "").lower()
                    required_level = (
                        lang.get("level", "").lower() or lang.get("proficiency", "").lower()
                    )
                    if language_name:
                        languages.append(
                            {
                                "language": language_name,
                                "required_level": required_level or "basic",
                            }
                        )
                elif isinstance(lang, str):
                    languages.append({"language": lang.lower(), "required_level": "basic"})

        return languages

    def _calculate_single_language_match(
        self, required_lang: Dict[str, str], candidate_languages: List[Dict[str, str]]
    ) -> float:
        """Calculate match score for a single required language"""
        required_name = required_lang["language"]
        required_level = required_lang.get("required_level", "basic")

        proficiency_levels = {
            "basic": 1,
            "elementary": 1,
            "beginner": 1,
            "intermediate": 2,
            "conversational": 2,
            "advanced": 3,
            "fluent": 4,
            "native": 5,
            "bilingual": 5,
        }

        required_level_score = proficiency_levels.get(required_level, 1)
        best_match_score = 0.0

        for candidate_lang in candidate_languages:
            candidate_name = candidate_lang["language"]
            candidate_proficiency = candidate_lang.get("proficiency", "basic")

            name_similarity = SM(None, required_name, candidate_name).ratio()

            if name_similarity >= 0.8:
                candidate_level_score = proficiency_levels.get(candidate_proficiency, 1)
                if candidate_level_score >= required_level_score:
                    proficiency_match = 1.0
                else:
                    proficiency_match = candidate_level_score / required_level_score

                total_match = name_similarity * proficiency_match
                best_match_score = max(best_match_score, total_match)

        return best_match_score
