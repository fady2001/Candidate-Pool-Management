from pathlib import Path
from typing import List

from loguru import logger

from src.batch_processor import BatchProcessor
from src.config import settings
from src.db_utils import (
    save_candidate_to_database,
    save_cv_batch_results_to_json,
    save_job_batch_results_to_json,
    save_job_description_to_database,
)
from src.models import BatchProcessingStats, CVBatchData, JobBatchData


def cvs_main():
    """
    |---------------------------------------------------------------------------|
    |                     information extraction from files                     |
    |---------------------------------------------------------------------------|
    """
    # 1. initialize the batch processor
    batch_processor = BatchProcessor()

    # 2. read cvs directory
    cvs_directory = settings.CV_DIRECTORY
    cv_files: List[Path] = []
    if cvs_directory.exists():
        logger.info(f"Reading CV files from directory: {cvs_directory}")
        for ext in settings.SUPPORTED_CV_FORMATS["all"]:
            cv_files.extend(list(cvs_directory.glob(f"*{ext}")))
    else:
        logger.error(f"CV directory {cvs_directory} does not exist.")
        return

    if not cv_files:
        logger.error(
            "No CV files found in the specified directory. make sure of the directory or supported formats."
        )
        logger.warning(f"Supported formats are {settings.SUPPORTED_CV_FORMATS['all']}")
        return

    logger.info("files to be processed:")
    for i, file in enumerate(cv_files):
        logger.info(f"    {i + 1}. {file.name}")

    # 3. Process the files in batches
    logger.info(f"Processing with batch size: {settings.BATCH_SIZE_CV}")

    function_results = batch_processor.process_cv_files(
        file_paths=cv_files,
        batch_size=4,
        max_size_mb=settings.MAX_FILE_SIZE_MB,
    )
    stats: BatchProcessingStats = function_results[0]
    processed_cvs: List[CVBatchData] = function_results[1]

    # 4. save result
    if settings.SAVE_INTO_DB:
        for batch in processed_cvs:
            for file in batch.results:
                save_candidate_to_database(file.cv_data, str(file.file_info.file_path))

    if settings.SAVE_INTO_JSON:
        for batch in processed_cvs:
            save_cv_batch_results_to_json(batch, settings.PROCESSED_DATA_DIR)

    # Display results
    logger.info("Processing completed!")
    logger.info(f"Session ID: {stats.session_id}")
    logger.info(f"Total batches: {stats.total_batches}")
    logger.info(f"Total files: {stats.total_files}")
    logger.info(f"Total successful: {stats.total_successful}")
    logger.info(f"Total failed: {stats.total_failed}")
    logger.info(f"Success rate: {stats.success_rate:.1f}%")
    logger.info(f"Processing time: {stats.total_processing_time_seconds:.2f} seconds")
    logger.info(
        f"average file processing time: {stats.total_processing_time_seconds / stats.total_files:.2f} seconds"
    )
    logger.info(f"average_batch_size: {stats.average_batch_size:.2f}")

    # Data has already been saved above in the batch processing loop


def jd_main():
    """
    |---------------------------------------------------------------------------|
    |                     information extraction from files                     |
    |---------------------------------------------------------------------------|
    """
    # 1. initialize the batch processor
    batch_processor = BatchProcessor()

    # 2. read job descriptions directory
    job_directory = settings.JOB_DESCRIPTIONS_DIR
    job_files: List[Path] = []
    if job_directory.exists():
        logger.info(f"Reading Job Description files from directory: {job_directory}")
        for ext in settings.SUPPORTED_CV_FORMATS["all"]:
            job_files.extend(list(job_directory.glob(f"*{ext}")))
    else:
        logger.error(f"Job Description directory {job_directory} does not exist.")
        return

    if not job_files:
        logger.error(
            "No Job Description files found in the specified directory. make sure of the directory or supported formats."
        )
        logger.warning(f"Supported formats are {settings.SUPPORTED_CV_FORMATS['all']}")
        return

    logger.info("files to be processed:")
    for i, file in enumerate(job_files):
        logger.info(f"    {i + 1}. {file.name}")

    # 3. Process the files in batches
    logger.info(f"Processing with batch size: {settings.BATCH_SIZE_JOB}")
    function_results = batch_processor.process_job_files(
        file_paths=job_files,
        batch_size=2,
        max_size_mb=settings.MAX_FILE_SIZE_MB,
    )

    stats: BatchProcessingStats = function_results[0]
    processed_jds: List[JobBatchData] = function_results[1]

    # 4. save result
    if settings.SAVE_INTO_DB:
        for batch in processed_jds:
            for file in batch.results:
                save_job_description_to_database(file.job_data, str(file.file_info.file_path))

    if settings.SAVE_INTO_JSON:
        for batch in processed_jds:
            save_job_batch_results_to_json(batch, settings.PROCESSED_DATA_DIR)

    # Display results
    logger.info("Processing completed!")
    logger.info(f"Session ID: {stats.session_id}")
    logger.info(f"Total batches: {stats.total_batches}")
    logger.info(f"Total files: {stats.total_files}")
    logger.info(f"Total successful: {stats.total_successful}")
    logger.info(f"Total failed: {stats.total_failed}")
    logger.info(f"Success rate: {stats.success_rate:.1f}%")
    logger.info(f"Processing time: {stats.total_processing_time_seconds:.2f} seconds")
    logger.info(
        f"average file processing time: {stats.total_processing_time_seconds / stats.total_files:.2f} seconds"
    )
    logger.info(f"average_batch_size: {stats.average_batch_size:.2f}")
    return stats


if __name__ == "__main__":
    jd_main()
