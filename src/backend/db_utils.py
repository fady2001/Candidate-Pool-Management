import json
from pathlib import Path
from typing import Optional

from loguru import logger

from src.backend.crud import CandidateService, JobService
from src.backend.database import db_manager
from src.backend.models import CVBatchData, CVData, JobBatchData, JobData


def initialize_database():
    """Initialize database tables"""
    try:
        db_manager.init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


def save_candidate_to_database(
    cv_data: CVData, source_file: Optional[str] = None
) -> Optional[dict]:
    """
    Save a single candidate to the database

    Args:
        cv_data: CVData object containing candidate information
        source_file: Path to the original CV file

    Returns:
        Created candidate dict or None if creation failed
    """
    try:
        logger.info(f"Saving candidate to database: {cv_data.full_name}")
        result = CandidateService.create_candidate(cv_data, source_file)

        if result:
            logger.info(
                f"Successfully saved candidate {cv_data.full_name} with ID: {result.get('id')}"
            )
            return result
        else:
            logger.error(f"Failed to save candidate {cv_data.full_name}")
            return None

    except Exception as e:
        logger.error(f"Error saving candidate {cv_data.full_name}: {str(e)}")
        return None


def save_job_description_to_database(
    job_data: JobData, source_file: Optional[str] = None
) -> Optional[dict]:
    """
    Save a single job description to the database

    Args:
        job_data: JobData object containing job information
        source_file: Path to the original job description file

    Returns:
        Created job dict or None if creation failed
    """
    try:
        logger.info(f"Saving job description to database: {job_data.job_title}")
        result = JobService.create_job(job_data, source_file)

        if result:
            logger.info(f"Successfully saved job {job_data.job_title} with ID: {result.get('id')}")
            return result
        else:
            logger.error(f"Failed to save job {job_data.job_title}")
            return None

    except Exception as e:
        logger.error(f"Error saving job {job_data.job_title}: {str(e)}")
        return None


def save_cv_batch_results_to_json(batch_result: CVBatchData, output_dir: str):
    """Save CV batch results to files"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    batch_summary_file = output_path / f"cv_batch_{batch_result.batch_id}_summary.json"
    with open(batch_summary_file, "w", encoding="utf-8") as f:
        json.dump(batch_result.dict(), f, indent=2, ensure_ascii=False)

    for result in batch_result.results:
        if result.success and result.cv_data:
            cv_filename = Path(result.file_info.file_name).stem
            cv_output_file = output_path / f"parsed_{cv_filename}.json"
            with open(cv_output_file, "w", encoding="utf-8") as f:
                json.dump(result.cv_data.dict(), f, indent=2, ensure_ascii=False)


def save_job_batch_results_to_json(batch_result: JobBatchData, output_dir: str):
    """Save Job batch results to files"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    batch_summary_file = output_path / f"job_batch_{batch_result.batch_id}_summary.json"
    with open(batch_summary_file, "w", encoding="utf-8") as f:
        json.dump(batch_result.dict(), f, indent=2, ensure_ascii=False)

    for result in batch_result.results:
        if result.success and result.job_data:
            job_filename = Path(result.file_info.file_name).stem
            job_output_file = output_path / f"parsed_{job_filename}.json"
            with open(job_output_file, "w", encoding="utf-8") as f:
                json.dump(result.job_data.dict(), f, indent=2, ensure_ascii=False)
