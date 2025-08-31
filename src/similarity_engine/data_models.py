

'''
|----------------------------------------------------------|
|               similarity score calculation               |
|----------------------------------------------------------|
'''
from typing import Any, Dict, List, Optional

from langchain_core.vectorstores import InMemoryVectorStore
from pydantic import BaseModel


class SimilarityScore(BaseModel):
    """Comprehensive similarity score breakdown"""

    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    semantic_similarity: float
    seniority_match: float
    detailed_breakdown: Dict[str, Any]
    
class RequirementMatch(BaseModel):
    """Individual requirement matching result"""

    requirement: str
    candidate_evidence: List[str]
    match_score: float
    match_type: str
    confidence: float
    
class JobContext(BaseModel):
    """Cached job context for efficient comparison with multiple candidates"""

    job_id: int
    job_data: Dict
    required_skills: List[str]
    job_responsibilities_text: str
    education_requirements: List[str]
    required_languages: List[Dict[str, str]]
    required_certifications: List[str]
    min_years_experience: int
    max_years_experience: Optional[int]
    seniority_level: str
    job_summary: str
    vector_store: Optional[InMemoryVectorStore] = None
