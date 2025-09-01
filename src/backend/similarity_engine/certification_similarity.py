from difflib import SequenceMatcher as SM
from typing import Dict, List

from loguru import logger

from src.backend.similarity_engine.base_similarity_metric import BaseSimilarityMetric
from src.backend.similarity_engine.data_models import JobContext


class CertificationSimilarityMetric(BaseSimilarityMetric):
    """Certification similarity calculation"""

    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    def calculate(self, candidate: Dict, job_context: JobContext) -> float:
        """Calculate certification similarity using cached job requirements"""
        try:
            candidate_certifications = self._extract_candidate_certifications(candidate)
            required_certifications = job_context.required_certifications

            if not required_certifications:
                logger.debug("No certification requirements found for job")
                return 0.9

            if not candidate_certifications:
                logger.debug("No certifications found for candidate")
                return 0.0

            matched_certifications = 0
            total_required = len(required_certifications)

            for required_cert in required_certifications:
                if self._find_matching_certification(required_cert, candidate_certifications):
                    matched_certifications += 1

            certification_similarity = matched_certifications / max(total_required, 1)
            logger.debug(
                f"Certification similarity - Required: {total_required}, Matched: {matched_certifications}, Score: {certification_similarity:.4f}"
            )
            return min(certification_similarity, 1.0)

        except Exception as e:
            logger.error(f"Error calculating certification similarity: {e}")
            return 0.5

    def _extract_candidate_certifications(self, candidate: Dict) -> List[str]:
        """Extract certifications from candidate data"""
        certifications = []
        candidate_certs = candidate.get("certifications", []) or []

        for cert in candidate_certs:
            if isinstance(cert, dict):
                cert_name = cert.get("name", "") or cert.get("certification", "")
                if cert_name:
                    certifications.append(cert_name.lower().strip())
            elif isinstance(cert, str):
                certifications.append(cert.lower().strip())

        return [cert for cert in certifications if cert]

    @staticmethod
    def extract_job_required_certifications(job: Dict) -> List[str]:
        """Extract required certifications from job data - static method for caching"""
        certifications = []
        cert_fields = [
            "required_certifications",
            "certifications",
            "certification_requirements",
            "preferred_certifications",
        ]

        for field in cert_fields:
            job_certs = job.get(field, []) or []
            for cert in job_certs:
                if isinstance(cert, dict):
                    cert_name = cert.get("name", "") or cert.get("certification", "")
                    if cert_name:
                        certifications.append(cert_name.lower().strip())
                elif isinstance(cert, str):
                    certifications.append(cert.lower().strip())

        return [cert for cert in certifications if cert]

    def _find_matching_certification(
        self, required_cert: str, candidate_certifications: List[str]
    ) -> bool:
        """Find if a required certification has a match in candidate's certifications"""
        if required_cert in candidate_certifications:
            return True

        for candidate_cert in candidate_certifications:
            similarity = SM(None, required_cert, candidate_cert).ratio()
            if similarity >= self.threshold:
                logger.debug(
                    f"Certification fuzzy match: '{required_cert}' <-> '{candidate_cert}' (similarity: {similarity:.3f})"
                )
                return True

        return False
