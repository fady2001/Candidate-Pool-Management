"""
CRUD operations for candidate pool management system using sqlite3.
"""

import json
import sqlite3
from typing import Any, Dict, List, Optional

from loguru import logger

from .database import db_manager
from .models import CVData, JobData


class CandidateService:
    """Service class for candidate CRUD operations"""

    @staticmethod
    def create_candidate(
        cv_data: CVData, source_file: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new candidate from CVData

        Args:
            cv_data: CVData object containing candidate information
            source_file: Path to the original CV file

        Returns:
            Created candidate dict or None if creation failed
        """
        try:
            # Convert Pydantic models to JSON strings for storage
            education_json = (
                json.dumps([edu.dict() for edu in cv_data.education])
                if cv_data.education
                else None
            )
            experience_json = (
                json.dumps([exp.dict() for exp in cv_data.experience])
                if cv_data.experience
                else None
            )
            skills_json = (
                json.dumps([skill.dict() for skill in cv_data.skills]) if cv_data.skills else None
            )
            certifications_json = (
                json.dumps([cert.dict() for cert in cv_data.certifications])
                if cv_data.certifications
                else None
            )
            languages_json = (
                json.dumps([lang.dict() for lang in cv_data.languages])
                if cv_data.languages
                else None
            )
            projects_json = json.dumps(cv_data.projects) if cv_data.projects else None
            awards_json = json.dumps(cv_data.awards) if cv_data.awards else None
            publications_json = json.dumps(cv_data.publications) if cv_data.publications else None

            query = """
                INSERT INTO candidates (
                    full_name, email, phone, address, linkedin, github, website,
                    summary, years_of_experience, current_position, current_company,
                    education, experience, skills, certifications, languages,
                    projects, awards, publications, source_file
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            params = (
                cv_data.full_name,
                cv_data.email,
                cv_data.phone,
                cv_data.address,
                cv_data.linkedin,
                cv_data.github,
                cv_data.website,
                cv_data.summary,
                cv_data.years_of_experience,
                cv_data.current_position,
                cv_data.current_company,
                education_json,
                experience_json,
                skills_json,
                certifications_json,
                languages_json,
                projects_json,
                awards_json,
                publications_json,
                source_file,
            )

            candidate_id = db_manager.execute_query(query, params)

            if candidate_id:
                logger.info(f"Created candidate: {cv_data.full_name} (ID: {candidate_id})")
                return CandidateService.get_candidate_by_id(candidate_id)
            return None

        except sqlite3.IntegrityError as e:
            logger.error(f"Failed to create candidate - integrity error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Failed to create candidate: {str(e)}")
            return None

    @staticmethod
    def get_candidate_by_id(candidate_id: int) -> Optional[Dict[str, Any]]:
        """Get candidate by ID"""
        try:
            query = "SELECT * FROM candidates WHERE id = ?"
            row = db_manager.execute_query(query, (candidate_id,), fetch_one=True)

            if row:
                return CandidateService._row_to_dict(row)
            return None
        except Exception as e:
            logger.error(f"Failed to get candidate {candidate_id}: {str(e)}")
            return None

    @staticmethod
    def get_candidates(
        skip: int = 0,
        limit: int = 100,
        search_term: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get candidates with optional filtering and pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            search_term: Search in name, email, current position, or company

        Returns:
            List of candidate dictionaries
        """
        try:
            query = "SELECT * FROM candidates WHERE 1=1"
            params = []

            if search_term:
                query += " AND (full_name LIKE ? OR email LIKE ? OR current_position LIKE ? OR current_company LIKE ?)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, skip])

            rows = db_manager.execute_query(query, tuple(params), fetch_all=True)

            return [CandidateService._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get candidates: {str(e)}")
            return []

    @staticmethod
    def update_candidate(candidate_id: int, cv_data: CVData) -> Optional[Dict[str, Any]]:
        """Update existing candidate"""
        try:
            # Convert Pydantic models to JSON strings
            education_json = (
                json.dumps([edu.dict() for edu in cv_data.education])
                if cv_data.education
                else None
            )
            experience_json = (
                json.dumps([exp.dict() for exp in cv_data.experience])
                if cv_data.experience
                else None
            )
            skills_json = (
                json.dumps([skill.dict() for skill in cv_data.skills]) if cv_data.skills else None
            )
            certifications_json = (
                json.dumps([cert.dict() for cert in cv_data.certifications])
                if cv_data.certifications
                else None
            )
            languages_json = (
                json.dumps([lang.dict() for lang in cv_data.languages])
                if cv_data.languages
                else None
            )
            projects_json = json.dumps(cv_data.projects) if cv_data.projects else None
            awards_json = json.dumps(cv_data.awards) if cv_data.awards else None
            publications_json = json.dumps(cv_data.publications) if cv_data.publications else None

            query = """
                UPDATE candidates SET
                    full_name = ?, email = ?, phone = ?, address = ?, linkedin = ?,
                    github = ?, website = ?, summary = ?, years_of_experience = ?,
                    current_position = ?, current_company = ?, education = ?,
                    experience = ?, skills = ?, certifications = ?, languages = ?,
                    projects = ?, awards = ?, publications = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """

            params = (
                cv_data.full_name,
                cv_data.email,
                cv_data.phone,
                cv_data.address,
                cv_data.linkedin,
                cv_data.github,
                cv_data.website,
                cv_data.summary,
                cv_data.years_of_experience,
                cv_data.current_position,
                cv_data.current_company,
                education_json,
                experience_json,
                skills_json,
                certifications_json,
                languages_json,
                projects_json,
                awards_json,
                publications_json,
                candidate_id,
            )

            db_manager.execute_query(query, params)
            logger.info(f"Updated candidate ID: {candidate_id}")
            return CandidateService.get_candidate(candidate_id)

        except Exception as e:
            logger.error(f"Failed to update candidate {candidate_id}: {str(e)}")
            return None

    @staticmethod
    def delete_candidate(candidate_id: int) -> bool:
        """
        Delete candidate

        Args:
            candidate_id: ID of candidate to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            query = "DELETE FROM candidates WHERE id = ?"
            db_manager.execute_query(query, (candidate_id,))
            logger.info(f"Permanently deleted candidate ID: {candidate_id}")

        except Exception as e:
            logger.error(f"Failed to delete candidate {candidate_id}: {str(e)}")
            return False

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        """Convert SQLite row to dictionary with JSON parsing"""
        data = dict(row)

        # Parse JSON fields
        json_fields = [
            "education",
            "experience",
            "skills",
            "certifications",
            "languages",
            "projects",
            "awards",
            "publications",
        ]

        for field in json_fields:
            if data.get(field):
                try:
                    data[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    data[field] = None

        return data


class JobService:
    """Service class for job description CRUD operations"""

    @staticmethod
    def create_job(
        job_data: JobData, source_file: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new job description from JobData

        Args:
            job_data: JobData object containing job information
            source_file: Path to the original job description file

        Returns:
            Created job dict or None if creation failed
        """
        try:
            # Convert complex objects to JSON strings
            responsibilities_json = (
                json.dumps(job_data.responsibilities) if job_data.responsibilities else None
            )
            company_info_json = json.dumps(job_data.company.dict()) if job_data.company else None
            required_skills_json = (
                json.dumps([skill.dict() for skill in job_data.required_skills])
                if job_data.required_skills
                else None
            )
            preferred_skills_json = (
                json.dumps([skill.dict() for skill in job_data.preferred_skills])
                if job_data.preferred_skills
                else None
            )
            education_requirements_json = (
                json.dumps(job_data.education_requirements)
                if job_data.education_requirements
                else None
            )
            experience_requirements_json = (
                json.dumps(job_data.experience_requirements)
                if job_data.experience_requirements
                else None
            )
            certifications_required_json = (
                json.dumps(job_data.certifications_required)
                if job_data.certifications_required
                else None
            )
            certifications_preferred_json = (
                json.dumps(job_data.certifications_preferred)
                if job_data.certifications_preferred
                else None
            )
            languages_required_json = (
                json.dumps([lang.dict() for lang in job_data.languages_required])
                if job_data.languages_required
                else None
            )
            salary_info_json = (
                json.dumps(job_data.salary_info.dict()) if job_data.salary_info else None
            )

            query = """
                INSERT INTO job_descriptions (
                    job_title, job_id, department, employment_type, work_arrangement,
                    location, job_summary, job_description, responsibilities, company_info,
                    required_skills, preferred_skills, education_requirements, experience_requirements,
                    certifications_required, certifications_preferred, languages_required,
                    min_years_experience, max_years_experience, seniority_level, salary_info,
                    application_deadline, application_process, contact_email, contact_person,
                    travel_requirements, security_clearance, visa_sponsorship, diversity_statement,
                    urgency_level, posted_date, last_updated, source_file
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            params = (
                job_data.job_title,
                job_data.job_id,
                job_data.department,
                job_data.employment_type,
                job_data.work_arrangement,
                job_data.location,
                job_data.job_summary,
                job_data.job_description,
                responsibilities_json,
                company_info_json,
                required_skills_json,
                preferred_skills_json,
                education_requirements_json,
                experience_requirements_json,
                certifications_required_json,
                certifications_preferred_json,
                languages_required_json,
                job_data.min_years_experience,
                job_data.max_years_experience,
                job_data.seniority_level,
                salary_info_json,
                job_data.application_deadline,
                job_data.application_process,
                job_data.contact_email,
                job_data.contact_person,
                job_data.travel_requirements,
                job_data.security_clearance,
                job_data.visa_sponsorship,
                job_data.diversity_statement,
                job_data.urgency_level,
                job_data.posted_date,
                job_data.last_updated,
                source_file,
            )

            job_id = db_manager.execute_query(query, params)

            if job_id:
                logger.info(f"Created job: {job_data.job_title} (ID: {job_id})")
                return JobService.get_job(job_id)
            return None

        except sqlite3.IntegrityError as e:
            logger.error(f"Failed to create job - integrity error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Failed to create job: {str(e)}")
            return None

    @staticmethod
    def get_job(job_id: int) -> Optional[Dict[str, Any]]:
        """Get job description by ID"""
        try:
            query = "SELECT * FROM job_descriptions WHERE id = ?"
            row = db_manager.execute_query(query, (job_id,), fetch_one=True)

            if row:
                return JobService._row_to_dict(row)
            return None
        except Exception as e:
            logger.error(f"Failed to get job {job_id}: {str(e)}")
            return None

    @staticmethod
    def get_job_by_job_id(job_id: str) -> Optional[Dict[str, Any]]:
        """Get job description by external job ID"""
        try:
            query = "SELECT * FROM job_descriptions WHERE job_id = ?"
            row = db_manager.execute_query(query, (job_id,), fetch_one=True)

            if row:
                return JobService._row_to_dict(row)
            return None
        except Exception as e:
            logger.error(f"Failed to get job by job_id {job_id}: {str(e)}")
            return None

    @staticmethod
    def get_jobs(
        skip: int = 0,
        limit: int = 100,
        search_term: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get job descriptions with optional filtering and pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            search_term: Search in title, department, location, or summary

        Returns:
            List of job description dictionaries
        """
        try:
            query = "SELECT * FROM job_descriptions WHERE 1=1"
            params = []

            if search_term:
                query += " AND (job_title LIKE ? OR department LIKE ? OR location LIKE ? OR job_summary LIKE ?)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, skip])

            rows = db_manager.execute_query(query, tuple(params), fetch_all=True)

            return [JobService._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get jobs: {str(e)}")
            return []

    @staticmethod
    def update_job(job_id: int, job_data: JobData) -> Optional[Dict[str, Any]]:
        """Update existing job description"""
        try:
            # Convert complex objects to JSON strings
            responsibilities_json = (
                json.dumps(job_data.responsibilities) if job_data.responsibilities else None
            )
            company_info_json = json.dumps(job_data.company.dict()) if job_data.company else None
            required_skills_json = (
                json.dumps([skill.dict() for skill in job_data.required_skills])
                if job_data.required_skills
                else None
            )
            preferred_skills_json = (
                json.dumps([skill.dict() for skill in job_data.preferred_skills])
                if job_data.preferred_skills
                else None
            )
            education_requirements_json = (
                json.dumps(job_data.education_requirements)
                if job_data.education_requirements
                else None
            )
            experience_requirements_json = (
                json.dumps(job_data.experience_requirements)
                if job_data.experience_requirements
                else None
            )
            certifications_required_json = (
                json.dumps(job_data.certifications_required)
                if job_data.certifications_required
                else None
            )
            certifications_preferred_json = (
                json.dumps(job_data.certifications_preferred)
                if job_data.certifications_preferred
                else None
            )
            languages_required_json = (
                json.dumps([lang.dict() for lang in job_data.languages_required])
                if job_data.languages_required
                else None
            )
            salary_info_json = (
                json.dumps(job_data.salary_info.dict()) if job_data.salary_info else None
            )

            query = """
                UPDATE job_descriptions SET
                    job_title = ?, job_id = ?, department = ?, employment_type = ?,
                    work_arrangement = ?, location = ?, job_summary = ?, job_description = ?,
                    responsibilities = ?, company_info = ?, required_skills = ?, preferred_skills = ?,
                    education_requirements = ?, experience_requirements = ?, certifications_required = ?,
                    certifications_preferred = ?, languages_required = ?, min_years_experience = ?,
                    max_years_experience = ?, seniority_level = ?, salary_info = ?,
                    application_deadline = ?, application_process = ?, contact_email = ?,
                    contact_person = ?, travel_requirements = ?, security_clearance = ?,
                    visa_sponsorship = ?, diversity_statement = ?, urgency_level = ?,
                    posted_date = ?, last_updated = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """

            params = (
                job_data.job_title,
                job_data.job_id,
                job_data.department,
                job_data.employment_type,
                job_data.work_arrangement,
                job_data.location,
                job_data.job_summary,
                job_data.job_description,
                responsibilities_json,
                company_info_json,
                required_skills_json,
                preferred_skills_json,
                education_requirements_json,
                experience_requirements_json,
                certifications_required_json,
                certifications_preferred_json,
                languages_required_json,
                job_data.min_years_experience,
                job_data.max_years_experience,
                job_data.seniority_level,
                salary_info_json,
                job_data.application_deadline,
                job_data.application_process,
                job_data.contact_email,
                job_data.contact_person,
                job_data.travel_requirements,
                job_data.security_clearance,
                job_data.visa_sponsorship,
                job_data.diversity_statement,
                job_data.urgency_level,
                job_data.posted_date,
                job_data.last_updated,
                job_id,
            )

            db_manager.execute_query(query, params)
            logger.info(f"Updated job ID: {job_id}")
            return JobService.get_job(job_id)

        except Exception as e:
            logger.error(f"Failed to update job {job_id}: {str(e)}")
            return None

    @staticmethod
    def delete_job(job_id: int) -> bool:
        """
        Delete job description (soft delete by default)

        Args:
            job_id: ID of job to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            query = "DELETE FROM job_descriptions WHERE id = ?"
            db_manager.execute_query(query, (job_id,))
            logger.info(f"Permanently deleted job ID: {job_id}")

        except Exception as e:
            logger.error(f"Failed to delete job {job_id}: {str(e)}")
            return False

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        """Convert SQLite row to dictionary with JSON parsing"""
        data = dict(row)

        # Parse JSON fields
        json_fields = [
            "responsibilities",
            "company_info",
            "required_skills",
            "preferred_skills",
            "education_requirements",
            "experience_requirements",
            "certifications_required",
            "certifications_preferred",
            "languages_required",
            "salary_info",
        ]

        for field in json_fields:
            if data.get(field):
                try:
                    data[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    data[field] = None

        return data


class MatchService:
    """Service class for candidate-job matching operations"""

    @staticmethod
    def create_match(
        candidate_id: int,
        job_id: int,
        overall_score: float,
        skills_score: Optional[float] = None,
        experience_score: Optional[float] = None,
        education_score: Optional[float] = None,
        match_details: Optional[Dict] = None,
    ) -> Optional[int]:
        """Create a new candidate-job match record"""
        try:
            match_details_json = json.dumps(match_details) if match_details else None

            query = """
                INSERT INTO candidate_job_matches (
                    candidate_id, job_id, overall_score, skills_score,
                    experience_score, education_score, match_details
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            params = (
                candidate_id,
                job_id,
                overall_score,
                skills_score,
                experience_score,
                education_score,
                match_details_json,
            )

            match_id = db_manager.execute_query(query, params)
            logger.info(
                f"Created match: Candidate {candidate_id} - Job {job_id} (Score: {overall_score})"
            )
            return match_id

        except Exception as e:
            logger.error(f"Failed to create match: {str(e)}")
            return None

    @staticmethod
    def get_matches_for_candidate(
        candidate_id: int, min_score: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get all job matches for a candidate"""
        try:
            query = "SELECT * FROM candidate_job_matches WHERE candidate_id = ?"
            params = [candidate_id]

            if min_score is not None:
                query += " AND overall_score >= ?"
                params.append(min_score)

            query += " ORDER BY overall_score DESC"

            rows = db_manager.execute_query(query, tuple(params), fetch_all=True)
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get matches for candidate {candidate_id}: {str(e)}")
            return []

    @staticmethod
    def get_matches_for_job(
        job_id: int, min_score: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get all candidate matches for a job"""
        try:
            query = "SELECT * FROM candidate_job_matches WHERE job_id = ?"
            params = [job_id]

            if min_score is not None:
                query += " AND overall_score >= ?"
                params.append(min_score)

            query += " ORDER BY overall_score DESC"

            rows = db_manager.execute_query(query, tuple(params), fetch_all=True)
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get matches for job {job_id}: {str(e)}")
            return []