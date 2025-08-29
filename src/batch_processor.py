from datetime import datetime
import json
from pathlib import Path
import time
from typing import List, Optional

from langchain_core.output_parsers import PydanticOutputParser
from loguru import logger

from src.config import settings
from src.file_parser import GeminiParser
from src.models import (
    BatchProcessingStats,
    CVBatchData,
    CVData,
    JobBatchData,
    JobData,
)
from src.utils import (
    calculate_success_rate,
    create_batches,
    filter_supported_files,
    generate_session_id,
)


class BatchProcessor:
    """High-level batch processor for CVs and Job Descriptions"""

    def __init__(
        self,
        model: str = settings.GEMINI_MODEL,
        temperature: float = settings.GEMINI_TEMPERATURE,
    ):
        cv_parser = PydanticOutputParser(pydantic_object=CVData)
        job_parser = PydanticOutputParser(pydantic_object=JobData)

        self.cv_gemini_parser = GeminiParser(cv_parser, model, temperature)
        self.job_gemini_parser = GeminiParser(job_parser, model, temperature)

        logger.info("BatchProcessor initialized with batch processing capabilities")

    def process_cv_files(
        self,
        file_paths: List[str],
        batch_size: Optional[int] = None,
        max_size_mb: Optional[int] = None,
        save_results: bool = True,
        output_dir: Optional[str] = None,
    ) -> BatchProcessingStats:
        """
        Process multiple CV files in batches

        Args:
            file_paths: List of CV file paths to process
            batch_size: Number of files per batch (uses config default if None)
            max_size_mb: Maximum total size per batch in MB (uses config default if None)
            save_results: Whether to save individual results to files
            output_dir: Directory to save results (uses config default if None)

        Returns:
            BatchProcessingStats with overall processing statistics
        """
        session_start_time = time.time()
        session_id = generate_session_id()

        batch_size = batch_size or settings.BATCH_SIZE_CV
        max_size_mb = max_size_mb or settings.MAX_FILE_SIZE_MB
        output_dir = output_dir or settings.PROCESSED_DATA_DIR

        logger.info(f"Starting CV batch processing session: {session_id}")
        logger.info(f"Processing {len(file_paths)} files with batch size {batch_size}")

        supported_files = filter_supported_files(file_paths)
        if len(supported_files) < len(file_paths):
            logger.warning(
                f"Filtered out {len(file_paths) - len(supported_files)} unsupported files"
            )

        if not supported_files:
            logger.error("No supported files to process")
            return self._create_empty_stats(session_id, session_start_time, "CV")

        batches = create_batches(supported_files, batch_size, max_size_mb)
        logger.info(f"Created {len(batches)} batches for processing")

        all_batch_results: List[CVBatchData] = []
        total_successful = 0
        total_failed = 0

        for i, batch_files in enumerate(batches, 1):
            logger.info(f"Processing batch {i}/{len(batches)} with {len(batch_files)} files")

            if i > 1 and settings.BATCH_DELAY_SECONDS > 0:
                time.sleep(settings.BATCH_DELAY_SECONDS)

            batch_result = self._process_cv_batch_with_retry(batch_files)
            all_batch_results.append(batch_result)

            total_successful += batch_result.successful_parses
            total_failed += batch_result.failed_parses

            if save_results:
                self._save_cv_batch_results(batch_result, output_dir)

            logger.info(
                f"Batch {i} completed: {batch_result.successful_parses}/{batch_result.total_files} successful"
            )

        session_end_time = time.time()
        total_processing_time = session_end_time - session_start_time

        stats = BatchProcessingStats(
            session_id=session_id,
            total_batches=len(batches),
            total_files=len(supported_files),
            total_successful=total_successful,
            total_failed=total_failed,
            total_processing_time_seconds=total_processing_time,
            average_batch_size=len(supported_files) / len(batches) if batches else 0,
            success_rate=calculate_success_rate(total_successful, len(supported_files)),
            start_time=datetime.fromtimestamp(session_start_time).isoformat(),
            end_time=datetime.fromtimestamp(session_end_time).isoformat(),
        )

        logger.info(f"CV batch processing session {session_id} completed")
        logger.info(
            f"Overall success rate: {stats.success_rate:.1f}% ({total_successful}/{len(supported_files)})"
        )

        return stats

    def process_job_files(
        self,
        file_paths: List[str],
        batch_size: Optional[int] = None,
        max_size_mb: Optional[int] = None,
        save_results: bool = True,
        output_dir: Optional[str] = None,
    ) -> BatchProcessingStats:
        """
        Process multiple job description files in batches

        Args:
            file_paths: List of job description file paths to process
            batch_size: Number of files per batch (uses config default if None)
            max_size_mb: Maximum total size per batch in MB (uses config default if None)
            save_results: Whether to save individual results to files
            output_dir: Directory to save results (uses config default if None)

        Returns:
            BatchProcessingStats with overall processing statistics
        """
        session_start_time = time.time()
        session_id = generate_session_id()

        batch_size = batch_size or settings.BATCH_SIZE_JOB
        max_size_mb = max_size_mb or settings.MAX_FILE_SIZE_MB
        output_dir = output_dir or settings.PROCESSED_DATA_DIR

        logger.info(f"Starting Job batch processing session: {session_id}")
        logger.info(f"Processing {len(file_paths)} files with batch size {batch_size}")

        supported_files = filter_supported_files(file_paths)
        if len(supported_files) < len(file_paths):
            logger.warning(
                f"Filtered out {len(file_paths) - len(supported_files)} unsupported files"
            )

        if not supported_files:
            logger.error("No supported files to process")
            return self._create_empty_stats(session_id, session_start_time, "Job")

        batches = create_batches(supported_files, batch_size, max_size_mb)
        logger.info(f"Created {len(batches)} batches for processing")

        all_batch_results: List[JobBatchData] = []
        total_successful = 0
        total_failed = 0

        for i, batch_files in enumerate(batches, 1):
            logger.info(f"Processing batch {i}/{len(batches)} with {len(batch_files)} files")

            if i > 1 and settings.BATCH_DELAY_SECONDS > 0:
                time.sleep(settings.BATCH_DELAY_SECONDS)

            batch_result = self._process_job_batch_with_retry(batch_files)
            all_batch_results.append(batch_result)

            total_successful += batch_result.successful_parses
            total_failed += batch_result.failed_parses

            if save_results:
                self._save_job_batch_results(batch_result, output_dir)

            logger.info(
                f"Batch {i} completed: {batch_result.successful_parses}/{batch_result.total_files} successful"
            )

        session_end_time = time.time()
        total_processing_time = session_end_time - session_start_time

        stats = BatchProcessingStats(
            session_id=session_id,
            total_batches=len(batches),
            total_files=len(supported_files),
            total_successful=total_successful,
            total_failed=total_failed,
            total_processing_time_seconds=total_processing_time,
            average_batch_size=len(supported_files) / len(batches) if batches else 0,
            success_rate=calculate_success_rate(total_successful, len(supported_files)),
            start_time=datetime.fromtimestamp(session_start_time).isoformat(),
            end_time=datetime.fromtimestamp(session_end_time).isoformat(),
        )

        logger.info(f"Job batch processing session {session_id} completed")
        logger.info(
            f"Overall success rate: {stats.success_rate:.1f}% ({total_successful}/{len(supported_files)})"
        )

        return stats

    def _process_cv_batch_with_retry(self, batch_files: List[str]) -> CVBatchData:
        """Process a CV batch with retry logic"""
        last_exception = None

        for attempt in range(settings.BATCH_RETRY_ATTEMPTS):
            try:
                if attempt > 0:
                    logger.info(
                        f"Retrying CV batch processing (attempt {attempt + 1}/{settings.BATCH_RETRY_ATTEMPTS})"
                    )
                    time.sleep(settings.BATCH_DELAY_SECONDS)

                return self.cv_gemini_parser.parse_cv_batch(batch_files)

            except Exception as e:
                last_exception = e
                logger.error(f"CV batch processing attempt {attempt + 1} failed: {e}")

        logger.error(f"CV batch processing failed after {settings.BATCH_RETRY_ATTEMPTS} attempts")
        return self.cv_gemini_parser._create_empty_cv_batch_result(
            "failed_batch", len(batch_files), time.time(), str(last_exception)
        )

    def _process_job_batch_with_retry(self, batch_files: List[str]) -> JobBatchData:
        """Process a Job batch with retry logic"""
        last_exception = None

        for attempt in range(settings.BATCH_RETRY_ATTEMPTS):
            try:
                if attempt > 0:
                    logger.info(
                        f"Retrying Job batch processing (attempt {attempt + 1}/{settings.BATCH_RETRY_ATTEMPTS})"
                    )
                    time.sleep(settings.BATCH_DELAY_SECONDS)

                return self.job_gemini_parser.parse_job_batch(batch_files)

            except Exception as e:
                last_exception = e
                logger.error(f"Job batch processing attempt {attempt + 1} failed: {e}")

        logger.error(f"Job batch processing failed after {settings.BATCH_RETRY_ATTEMPTS} attempts")
        return self.job_gemini_parser._create_empty_job_batch_result(
            "failed_batch", len(batch_files), time.time(), str(last_exception)
        )

    def _save_cv_batch_results(self, batch_result: CVBatchData, output_dir: str):
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

    def _save_job_batch_results(self, batch_result: JobBatchData, output_dir: str):
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

    def _create_empty_stats(
        self, session_id: str, start_time: float, file_type: str
    ) -> BatchProcessingStats:
        """Create empty statistics for error cases"""
        end_time = time.time()
        return BatchProcessingStats(
            session_id=session_id,
            total_batches=0,
            total_files=0,
            total_successful=0,
            total_failed=0,
            total_processing_time_seconds=end_time - start_time,
            average_batch_size=0.0,
            success_rate=0.0,
            start_time=datetime.fromtimestamp(start_time).isoformat(),
            end_time=datetime.fromtimestamp(end_time).isoformat(),
        )
