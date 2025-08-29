from pathlib import Path
import time
from typing import List

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

from src.config import settings
from src.models import (
    CVBatchData,
    CVBatchResponse,
    CVBatchResult,
    FileInfo,
    JobBatchData,
    JobBatchResponse,
    JobBatchResult,
)
from src.prompts import CV_PARSING_SYSTEM_PROMPT, JOB_DESCRIPTION_PARSING_SYSTEM_PROMPT
from src.utils import (
    create_file_info,
    generate_batch_id,
    get_llm,
)


class GeminiParser:
    """CV and Job Description Parser using Google Gemini model with batch processing support"""

    def __init__(
        self,
        parser: PydanticOutputParser,
        model: str = settings.GEMINI_MODEL,
        temperature: float = settings.GEMINI_TEMPERATURE,
    ) -> None:
        self.llm = get_llm(model=model, temperature=temperature)
        self.parser: PydanticOutputParser = parser

    def parse_cv_batch(self, cv_paths: List[Path]) -> CVBatchData:
        """Parse multiple CV files in a single batch request"""
        batch_start_time = time.time()
        batch_id = generate_batch_id()
        results: List[CVBatchResult] = []

        logger.info(f"Starting CV batch processing: {batch_id} with {len(cv_paths)} files")

        try:
            file_infos: List[FileInfo] = []
            for cv_path in cv_paths:
                try:
                    file_info = create_file_info(cv_path)
                    file_infos.append(file_info)
                except Exception as e:
                    logger.error(f"Error preparing file {cv_path}: {e}")
                    results.append(
                        CVBatchResult(
                            file_info=FileInfo(
                                file_path=cv_path,
                                file_name=cv_path.split("/")[-1],
                                file_type="unknown",
                                mime_type="unknown",
                                file_size_bytes=0,
                                base64_content="",
                            ),
                            cv_data=None,
                            success=False,
                            error_message=str(e),
                            processing_time_seconds=0.0,
                        )
                    )
                    continue

            if not file_infos:
                logger.error("No valid files to process in batch")
                return self._create_empty_cv_batch_result(
                    batch_id, len(cv_paths), batch_start_time
                )

            media_contents = []
            file_descriptions = []

            for i, file_info in enumerate(file_infos):
                media_contents.append(
                    {"type": "text", "text": f"\n--- FILE {i + 1}: {file_info.file_name} ---"}
                )
                media_contents.append(
                    {
                        "type": "media",
                        "source_type": "base64",
                        "data": file_info.base64_content,
                        "mime_type": file_info.mime_type,
                    }
                )
                file_descriptions.append(f"File {i + 1}: {file_info.file_name}")

            instruction_text = (
                f"Please analyze these {len(file_infos)} CV files and extract all information "
                f"according to the structured format provided in the system message. "
                f"Process each CV independently and return structured data for all files in the 'cvs' array.\n\n"
                f"Files to process:\n" + "\n".join(file_descriptions)
            )

            media_contents.insert(0, {"type": "text", "text": instruction_text})

            prompt_template = ChatPromptTemplate(
                [("system", CV_PARSING_SYSTEM_PROMPT), ("human", media_contents)]
            )

            prompt_messages = prompt_template.invoke(
                {
                    "format_instructions": PydanticOutputParser(
                        pydantic_object=CVBatchResponse
                    ).get_format_instructions()
                }
            )

            llm_start_time = time.time()
            try:
                batch_response: CVBatchResponse = self.llm.with_structured_output(
                    CVBatchResponse
                ).invoke(prompt_messages)
                llm_processing_time = time.time() - llm_start_time

                for i, file_info in enumerate(file_infos):
                    if i < len(batch_response.cvs) and batch_response.cvs[i] is not None:
                        results.append(
                            CVBatchResult(
                                file_info=file_info,
                                cv_data=batch_response.cvs[i],
                                success=True,
                                error_message=None,
                                processing_time_seconds=llm_processing_time / len(file_infos),
                            )
                        )
                    else:
                        results.append(
                            CVBatchResult(
                                file_info=file_info,
                                cv_data=None,
                                success=False,
                                error_message="No data returned from LLM for this file",
                                processing_time_seconds=0.0,
                            )
                        )

            except Exception as e:
                logger.error(f"Error during LLM processing for batch {batch_id}: {e}")
                for file_info in file_infos:
                    results.append(
                        CVBatchResult(
                            file_info=file_info,
                            cv_data=None,
                            success=False,
                            error_message=f"LLM processing error: {str(e)}",
                            processing_time_seconds=0.0,
                        )
                    )

        except Exception as e:
            logger.error(f"Critical error in CV batch processing {batch_id}: {e}")
            return self._create_empty_cv_batch_result(
                batch_id, len(cv_paths), batch_start_time, str(e)
            )

        batch_processing_time = time.time() - batch_start_time
        successful_parses = sum(1 for result in results if result.success)
        failed_parses = len(results) - successful_parses

        logger.info(
            f"Completed CV batch {batch_id}: {successful_parses}/{len(results)} successful"
        )

        return CVBatchData(
            batch_id=batch_id,
            total_files=len(cv_paths),
            successful_parses=successful_parses,
            failed_parses=failed_parses,
            batch_processing_time_seconds=batch_processing_time,
            results=results,
        )

    def parse_job_batch(self, jd_paths: List[Path]) -> JobBatchData:
        """Parse multiple job description files in a single batch request"""
        batch_start_time = time.time()
        batch_id = generate_batch_id()
        results: List[JobBatchResult] = []

        logger.info(f"Starting Job batch processing: {batch_id} with {len(jd_paths)} files")

        try:
            file_infos: List[FileInfo] = []
            for jd_path in jd_paths:
                try:
                    file_info = create_file_info(jd_path)
                    file_infos.append(file_info)
                except Exception as e:
                    logger.error(f"Error preparing file {jd_path}: {e}")
                    results.append(
                        JobBatchResult(
                            file_info=FileInfo(
                                file_path=jd_path,
                                file_name=jd_path.split("/")[-1],
                                file_type="unknown",
                                mime_type="unknown",
                                file_size_bytes=0,
                                base64_content="",
                            ),
                            job_data=None,
                            success=False,
                            error_message=str(e),
                            processing_time_seconds=0.0,
                        )
                    )
                    continue

            if not file_infos:
                logger.error("No valid files to process in batch")
                return self._create_empty_job_batch_result(
                    batch_id, len(jd_paths), batch_start_time
                )

            media_contents = []
            file_descriptions = []

            for i, file_info in enumerate(file_infos):
                media_contents.append(
                    {"type": "text", "text": f"\n--- FILE {i + 1}: {file_info.file_name} ---"}
                )
                media_contents.append(
                    {
                        "type": "media",
                        "source_type": "base64",
                        "data": file_info.base64_content,
                        "mime_type": file_info.mime_type,
                    }
                )
                file_descriptions.append(f"File {i + 1}: {file_info.file_name}")

            instruction_text = (
                f"Please analyze these {len(file_infos)} job description files and extract all information "
                f"according to the structured format provided in the system message. "
                f"Process each job description independently and return structured data for all files in the 'jobs' array.\n\n"
                f"Files to process:\n" + "\n".join(file_descriptions)
            )

            media_contents.insert(0, {"type": "text", "text": instruction_text})

            prompt_template = ChatPromptTemplate(
                [("system", JOB_DESCRIPTION_PARSING_SYSTEM_PROMPT), ("human", media_contents)]
            )

            prompt_messages = prompt_template.invoke(
                {
                    "format_instructions": PydanticOutputParser(
                        pydantic_object=JobBatchResponse
                    ).get_format_instructions()
                }
            )

            llm_start_time = time.time()
            try:
                batch_response = self.llm.with_structured_output(JobBatchResponse).invoke(
                    prompt_messages
                )
                llm_processing_time = time.time() - llm_start_time

                for i, file_info in enumerate(file_infos):
                    if i < len(batch_response.jobs) and batch_response.jobs[i] is not None:
                        results.append(
                            JobBatchResult(
                                file_info=file_info,
                                job_data=batch_response.jobs[i],
                                success=True,
                                error_message=None,
                                processing_time_seconds=llm_processing_time / len(file_infos),
                            )
                        )
                    else:
                        results.append(
                            JobBatchResult(
                                file_info=file_info,
                                job_data=None,
                                success=False,
                                error_message="No data returned from LLM for this file",
                                processing_time_seconds=0.0,
                            )
                        )

            except Exception as e:
                logger.error(f"Error during LLM processing for batch {batch_id}: {e}")
                for file_info in file_infos:
                    results.append(
                        JobBatchResult(
                            file_info=file_info,
                            job_data=None,
                            success=False,
                            error_message=f"LLM processing error: {str(e)}",
                            processing_time_seconds=0.0,
                        )
                    )

        except Exception as e:
            logger.error(f"Critical error in Job batch processing {batch_id}: {e}")
            return self._create_empty_job_batch_result(
                batch_id, len(jd_paths), batch_start_time, str(e)
            )

        batch_processing_time = time.time() - batch_start_time
        successful_parses = sum(1 for result in results if result.success)
        failed_parses = len(results) - successful_parses

        logger.info(
            f"Completed Job batch {batch_id}: {successful_parses}/{len(results)} successful"
        )

        return JobBatchData(
            batch_id=batch_id,
            total_files=len(jd_paths),
            successful_parses=successful_parses,
            failed_parses=failed_parses,
            batch_processing_time_seconds=batch_processing_time,
            results=results,
        )

    def _create_empty_cv_batch_result(
        self,
        batch_id: str,
        total_files: int,
        start_time: float,
        error_msg: str = "No valid files to process",
    ) -> CVBatchData:
        """Create an empty CV batch result for error cases"""
        return CVBatchData(
            batch_id=batch_id,
            total_files=total_files,
            successful_parses=0,
            failed_parses=total_files,
            batch_processing_time_seconds=time.time() - start_time,
            results=[],
        )

    def _create_empty_job_batch_result(
        self,
        batch_id: str,
        total_files: int,
        start_time: float,
        error_msg: str = "No valid files to process",
    ) -> JobBatchData:
        """Create an empty Job batch result for error cases"""
        return JobBatchData(
            batch_id=batch_id,
            total_files=total_files,
            successful_parses=0,
            failed_parses=total_files,
            batch_processing_time_seconds=time.time() - start_time,
            results=[],
        )
