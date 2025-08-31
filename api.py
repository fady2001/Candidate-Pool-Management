from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel
import uvicorn

from src.crud import CandidateService, JobService
from src.models import CVData, JobData
from src.similarity_engine import AdvancedSimilarityEngine


class MatchResponse(BaseModel):
    candidate_id: int
    candidate_name: Optional[str]
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    semantic_similarity: float
    seniority_match: float
    detailed_breakdown: Dict[str, Any]


class PaginationResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool


# Initialize FastAPI app
app = FastAPI(
    title="Candidate Pool Management API",
    description="API for managing candidates, job descriptions, and candidate-job matching",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize similarity engine
similarity_engine = AdvancedSimilarityEngine()


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Candidate Pool Management API",
        "version": "1.0.0",
        "endpoints": {
            "candidates": "/candidates",
            "jobs": "/jobs",
            "matching": "/jobs/{job_id}/matching-candidates",
        },
    }


@app.get("/candidates", response_model=List[CVData])
async def get_all_candidates(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search term for filtering candidates"),
) -> List[CVData]:
    """
    Retrieve all candidates with optional pagination and search

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (1-1000)
    - **search**: Search term to filter candidates by name, email, position, or company
    """
    try:
        logger.info(f"Fetching candidates: skip={skip}, limit={limit}, search={search}")

        candidates = CandidateService.get_candidates(skip=skip, limit=limit, search_term=search)

        if not candidates:
            logger.info("No candidates found")
            return []

        # Convert to response format
        result = []
        for candidate in candidates:
            result.append(
                CVData(
                    id=candidate["id"],
                    full_name=candidate.get("full_name"),
                    email=candidate.get("email"),
                    phone=candidate.get("phone"),
                    address=candidate.get("address"),
                    linkedin=candidate.get("linkedin"),
                    github=candidate.get("github"),
                    website=candidate.get("website"),
                    summary=candidate.get("summary"),
                    education=candidate.get("education", []),
                    experience=candidate.get("experience", []),
                    skills=candidate.get("skills", []),
                    certifications=candidate.get("certifications", []),
                    languages=candidate.get("languages", []),
                    projects=candidate.get("projects", []),
                    awards=candidate.get("awards", []),
                    publications=candidate.get("publications", []),
                    years_of_experience=candidate.get("years_of_experience"),
                    current_position=candidate.get("current_position"),
                    current_company=candidate.get("current_company"),
                )
            )

        logger.info(f"Retrieved {len(result)} candidates")
        return result

    except Exception as e:
        logger.error(f"Error retrieving candidates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving candidates: {str(e)}")


@app.get("/candidates/{candidate_id}", response_model=CVData)
async def get_candidate_by_id(candidate_id: int) -> CVData:
    """
    Retrieve a specific candidate by ID

    - **candidate_id**: The ID of the candidate to retrieve
    """
    try:
        logger.info(f"Fetching candidate with ID: {candidate_id}")

        candidate = CandidateService.get_candidate_by_id(candidate_id)

        if not candidate:
            raise HTTPException(
                status_code=404, detail=f"Candidate with ID {candidate_id} not found"
            )

        result = CVData(
            id=candidate["id"],
            full_name=candidate.get("full_name"),
            email=candidate.get("email"),
            phone=candidate.get("phone"),
            address=candidate.get("address"),
            linkedin=candidate.get("linkedin"),
            github=candidate.get("github"),
            website=candidate.get("website"),
            summary=candidate.get("summary"),
            education=candidate.get("education", []),
            experience=candidate.get("experience", []),
            skills=candidate.get("skills", []),
            certifications=candidate.get("certifications", []),
            languages=candidate.get("languages", []),
            projects=candidate.get("projects", []),
            awards=candidate.get("awards", []),
            publications=candidate.get("publications", []),
            years_of_experience=candidate.get("years_of_experience"),
            current_position=candidate.get("current_position"),
            current_company=candidate.get("current_company"),
        )

        logger.info(f"Retrieved candidate: {candidate.get('full_name')}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving candidate {candidate_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving candidate: {str(e)}")


@app.get("/jobs", response_model=List[JobData])
async def get_all_job_descriptions(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search term for filtering job descriptions"),
) -> List[JobData]:
    """
    Retrieve all job descriptions with optional pagination and search

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (1-1000)
    - **search**: Search term to filter jobs by title, department, location, or summary
    """
    try:
        logger.info(f"Fetching job descriptions: skip={skip}, limit={limit}, search={search}")

        jobs = JobService.get_jobs(skip=skip, limit=limit, search_term=search)

        if not jobs:
            logger.info("No job descriptions found")
            return []

        # Convert to response format
        result = []
        for job in jobs:
            result.append(
                JobData(
                    job_title=job.get("job_title"),
                    job_id=job.get("job_id"),
                    department=job.get("department"),
                    employment_type=job.get("employment_type"),
                    work_arrangement=job.get("work_arrangement"),
                    location=job.get("location"),
                    company=job.get("company_info"),
                    job_summary=job.get("job_summary"),
                    job_description=job.get("job_description"),
                    responsibilities=job.get("responsibilities", []),
                    required_skills=job.get("required_skills", []),
                    preferred_skills=job.get("preferred_skills", []),
                    education_requirements=job.get("education_requirements", []),
                    experience_requirements=job.get("experience_requirements", []),
                    certifications_required=job.get("certifications_required", []),
                    certifications_preferred=job.get("certifications_preferred", []),
                    languages_required=job.get("languages_required", []),
                    salary_info=job.get("salary_info"),
                    application_deadline=job.get("application_deadline"),
                    application_process=job.get("application_process"),
                    contact_email=job.get("contact_email"),
                    contact_person=job.get("contact_person"),
                    travel_requirements=job.get("travel_requirements"),
                    security_clearance=job.get("security_clearance"),
                    visa_sponsorship=job.get("visa_sponsorship"),
                    diversity_statement=job.get("diversity_statement"),
                    posted_date=job.get("posted_date"),
                    last_updated=job.get("last_updated"),
                    urgency_level=job.get("urgency_level"),
                    seniority_level=job.get("seniority_level"),
                    min_years_experience=job.get("min_years_experience"),
                    max_years_experience=job.get("max_years_experience"),
                )
            )

        logger.info(f"Retrieved {len(result)} job descriptions")
        return result

    except Exception as e:
        logger.error(f"Error retrieving job descriptions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving job descriptions: {str(e)}")


@app.get("/jobs/{job_id}", response_model=JobData)
async def get_job_by_id(job_id: int) -> JobData:
    """
    Retrieve a specific job description by ID

    - **job_id**: The ID of the job description to retrieve
    """
    try:
        logger.info(f"Fetching job description with ID: {job_id}")

        job = JobService.get_job(job_id)

        if not job:
            raise HTTPException(
                status_code=404, detail=f"Job description with ID {job_id} not found"
            )

        result = JobData(
            job_title=job.get("job_title"),
            job_id=job.get("job_id"),
            department=job.get("department"),
            employment_type=job.get("employment_type"),
            work_arrangement=job.get("work_arrangement"),
            location=job.get("location"),
            company=job.get("company_info"),
            job_summary=job.get("job_summary"),
            job_description=job.get("job_description"),
            responsibilities=job.get("responsibilities", []),
            required_skills=job.get("required_skills", []),
            preferred_skills=job.get("preferred_skills", []),
            education_requirements=job.get("education_requirements", []),
            experience_requirements=job.get("experience_requirements", []),
            certifications_required=job.get("certifications_required", []),
            certifications_preferred=job.get("certifications_preferred", []),
            languages_required=job.get("languages_required", []),
            salary_info=job.get("salary_info"),
            application_deadline=job.get("application_deadline"),
            application_process=job.get("application_process"),
            contact_email=job.get("contact_email"),
            contact_person=job.get("contact_person"),
            travel_requirements=job.get("travel_requirements"),
            security_clearance=job.get("security_clearance"),
            visa_sponsorship=job.get("visa_sponsorship"),
            diversity_statement=job.get("diversity_statement"),
            posted_date=job.get("posted_date"),
            last_updated=job.get("last_updated"),
            urgency_level=job.get("urgency_level"),
            seniority_level=job.get("seniority_level"),
            min_years_experience=job.get("min_years_experience"),
            max_years_experience=job.get("max_years_experience"),
        )

        logger.info(f"Retrieved job: {job.get('job_title')}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving job: {str(e)}")


@app.get("/jobs/{job_id}/matching-candidates", response_model=List[MatchResponse])
async def get_matching_candidates_for_job(
    job_id: int,
    min_score: float = Query(
        0.0, ge=0.0, le=1.0, description="Minimum similarity score threshold"
    ),
    limit: int = Query(50, ge=1, le=500, description="Maximum number of candidates to return"),
) -> List[MatchResponse]:
    """
    Retrieve candidates that match a specific job description

    - **job_id**: The ID of the job description to match candidates against
    - **min_score**: Minimum similarity score threshold (0.0 to 1.0)
    - **limit**: Maximum number of matching candidates to return (1-500)
    """
    try:
        logger.info(f"Finding matching candidates for job ID: {job_id}, min_score: {min_score}")

        # First, verify the job exists
        job = JobService.get_job(job_id)
        if not job:
            raise HTTPException(
                status_code=404, detail=f"Job description with ID {job_id} not found"
            )

        # Get all candidates (we'll process them in batches for efficiency)
        all_candidates = CandidateService.get_candidates(
            skip=0, limit=1000
        )  # Adjust based on your data size

        if not all_candidates:
            logger.info("No candidates found in database")
            return []

        # Extract candidate IDs
        candidate_ids = [candidate["id"] for candidate in all_candidates]

        # Calculate similarity scores using the similarity engine
        logger.info(f"Calculating similarity scores for {len(candidate_ids)} candidates")
        similarity_results = similarity_engine.calculate_similarity_batch(candidate_ids, job_id)

        # Filter by minimum score and prepare response
        matching_candidates = []
        for i, result in enumerate(similarity_results):
            if result.overall_score >= min_score:
                candidate = all_candidates[i]
                matching_candidates.append(
                    MatchResponse(
                        candidate_id=candidate["id"],
                        candidate_name=candidate.get("full_name"),
                        overall_score=result.overall_score,
                        skills_score=result.skills_score,
                        experience_score=result.experience_score,
                        education_score=result.education_score,
                        semantic_similarity=result.semantic_similarity,
                        seniority_match=result.seniority_match,
                        detailed_breakdown=result.detailed_breakdown,
                    )
                )

        # Sort by overall score (descending) and limit results
        matching_candidates.sort(key=lambda x: x.overall_score, reverse=True)
        matching_candidates = matching_candidates[:limit]

        logger.info(
            f"Found {len(matching_candidates)} matching candidates above threshold {min_score}"
        )
        return matching_candidates

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error finding matching candidates for job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error finding matching candidates: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
