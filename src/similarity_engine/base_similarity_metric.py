from abc import ABC, abstractmethod
from typing import Dict

from src.similarity_engine.data_models import JobContext


class BaseSimilarityMetric(ABC):
    """Base abstract class for similarity metrics"""

    @abstractmethod
    def calculate(self, candidate: Dict, job_context: JobContext) -> float:
        """Calculate similarity score between candidate and job context"""
        pass