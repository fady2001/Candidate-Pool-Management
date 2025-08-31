from typing import Dict, List, Optional

from loguru import logger

from src.crud import CandidateService, JobService
from src.similarity_engine.certification_similarity import CertificationSimilarityMetric
from src.similarity_engine.data_models import JobContext, SimilarityScore
from src.similarity_engine.education_similarity import EducationSimilarityMetric
from src.similarity_engine.experience_similarity import ExperienceSimilarityMetric
from src.similarity_engine.language_similarity import LanguageSimilarityMetric
from src.similarity_engine.semantic_similarity import SemanticSimilarityMetric
from src.similarity_engine.seniority_similarity import SenioritySimilarityMetric
from src.similarity_engine.skills_similarity import SkillsSimilarityMetric
from src.utils import get_embedding_model


class AdvancedSimilarityEngine:
    """Advanced similarity engine using multiple metric classes for candidate-job matching with caching"""

    def __init__(self):
        self.embeddings = get_embedding_model()
        self._job_context_cache: Dict[int, JobContext] = {}

        # Initialize metric classes
        self.skills_metric = SkillsSimilarityMetric()
        self.experience_metric = ExperienceSimilarityMetric(self.embeddings)
        self.education_metric = EducationSimilarityMetric()
        self.semantic_metric = SemanticSimilarityMetric(self.embeddings)
        self.seniority_metric = SenioritySimilarityMetric()
        self.language_metric = LanguageSimilarityMetric()
        self.certification_metric = CertificationSimilarityMetric()

    def preprocess_job(self, job_id: int) -> JobContext:
        """Preprocess and cache job data for efficient comparison with multiple candidates"""
        if job_id in self._job_context_cache:
            return self._job_context_cache[job_id]

        job = JobService.get_job(job_id)
        if not job:
            logger.error(f"Could not find job {job_id}")
            raise ValueError(f"Job {job_id} not found")

        logger.info(f"Preprocessing job: {job.get('job_title', 'Unknown')} (ID: {job_id})")

        # Extract and cache all job-related data
        job_context = JobContext(
            job_id=job_id,
            job_data=job,
            required_skills=self.skills_metric.extract_job_required_skills(job),
            job_responsibilities_text=self.experience_metric.extract_job_responsibilities_and_description(
                job
            ),
            education_requirements=self.education_metric.extract_job_education_requirements(job),
            required_languages=self.language_metric.extract_job_required_languages(job),
            required_certifications=self.certification_metric.extract_job_required_certifications(
                job
            ),
            min_years_experience=job.get("min_years_experience", 0) or 0,
            max_years_experience=job.get("max_years_experience"),
            seniority_level=job.get("seniority_level", "") or "",
            job_summary=job.get("job_summary", "") or "",
        )

        # Cache the job context
        self._job_context_cache[job_id] = job_context
        logger.info(f"Job {job_id} preprocessed and cached successfully")

        return job_context

    def calculate_similarity_batch(
        self, candidate_ids: List[int], job_id: int, weights: Optional[Dict[str, float]] = None
    ) -> List[SimilarityScore]:
        """Calculate similarity for multiple candidates against a single job (optimized)"""
        # Preprocess job once for all candidates
        job_context = self.preprocess_job(job_id)

        results = []
        for candidate_id in candidate_ids:
            score = self._calculate_similarity_with_context(candidate_id, job_context, weights)
            results.append(score)

        return results

    def calculate_similarity(
        self, candidate_id: int, job_id: int, weights: Optional[Dict[str, float]] = None
    ) -> SimilarityScore:
        """Calculate similarity score between candidate and job (single comparison)"""
        job_context = self.preprocess_job(job_id)
        return self._calculate_similarity_with_context(candidate_id, job_context, weights)

    def _calculate_similarity_with_context(
        self,
        candidate_id: int,
        job_context: JobContext,
        weights: Optional[Dict[str, float]] = None,
    ) -> SimilarityScore:
        """Calculate similarity using preprocessed job context"""
        # Default weights
        if weights is None:
            weights = {
                "skills": 0.30,
                "experience": 0.25,
                "education": 0.15,
                "language": 0.03,
                "certification": 0.02,
                "semantic": 0.05,
                "seniority": 0.02,
            }

        # Fetch candidate data
        candidate = CandidateService.get_candidate_by_id(candidate_id)
        if not candidate:
            logger.error(f"Could not find candidate {candidate_id}")
            return self._create_empty_score()

        logger.info(
            f"Calculating similarity: {candidate.get('full_name', 'Unknown')} -> {job_context.job_data.get('job_title', 'Unknown')}"
        )

        # Calculate individual scores using cached job context
        skills_score = self.skills_metric.calculate(candidate, job_context)
        experience_score = self.experience_metric.calculate(candidate, job_context)
        education_score = self.education_metric.calculate(candidate, job_context)
        language_score = self.language_metric.calculate(candidate, job_context)
        certification_score = self.certification_metric.calculate(candidate, job_context)
        semantic_score = self.semantic_metric.calculate(candidate, job_context)
        seniority_score = self.seniority_metric.calculate(candidate, job_context)

        # Calculate weighted overall score
        overall_score = (
            skills_score * weights["skills"]
            + experience_score * weights["experience"]
            + education_score * weights["education"]
            + semantic_score * weights["semantic"]
            + seniority_score * weights["seniority"]
            + language_score * weights["language"]
            + certification_score * weights["certification"]
        )
        overall_score /= sum(weights.values())

        return SimilarityScore(
            overall_score=round(overall_score, 4),
            skills_score=round(skills_score, 4),
            experience_score=round(experience_score, 4),
            education_score=round(education_score, 4),
            semantic_similarity=round(semantic_score, 4),
            seniority_match=round(seniority_score, 4),
            detailed_breakdown={
                "certification_score": round(certification_score, 4),
                "weights_used": weights,
                "job_id": job_context.job_id,
                "cached": True,
            },
        )

    def clear_cache(self, job_id: Optional[int] = None):
        """Clear cached job context for specific job or all jobs"""
        if job_id:
            self._job_context_cache.pop(job_id, None)
            logger.info(f"Cleared cache for job {job_id}")
        else:
            self._job_context_cache.clear()
            logger.info("Cleared all job context cache")

    def get_cached_job_ids(self) -> List[int]:
        """Get list of cached job IDs"""
        return list(self._job_context_cache.keys())

    def _create_empty_score(self) -> SimilarityScore:
        """Create empty similarity score for error cases"""
        return SimilarityScore(
            overall_score=0.0,
            skills_score=0.0,
            experience_score=0.0,
            education_score=0.0,
            semantic_similarity=0.0,
            seniority_match=0.0,
            detailed_breakdown={},
        )


if __name__ == "__main__":
    engine = AdvancedSimilarityEngine()

    # Example: Compare multiple candidates against job 3
    candidate_ids = [21, 22, 23, 24, 25]
    results = engine.calculate_similarity_batch(candidate_ids, 3)

    for i, result in enumerate(results):
        print(f"Candidate {candidate_ids[i]}: {result.overall_score}")
