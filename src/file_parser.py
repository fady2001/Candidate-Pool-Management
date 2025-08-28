from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config import settings
from src.models import CVData, JobData
from src.prompts import CV_PARSING_SYSTEM_PROMPT, JOB_DESCRIPTION_PARSING_SYSTEM_PROMPT
from src.utils import (
    encode_file_to_base64,
    get_file_type_extension,
    get_llm,
)


class GeminiParser:
    """CV Parser using Google Gemini model"""

    def __init__(
        self,
        parser: PydanticOutputParser,
        model: str = settings.GEMINI_MODEL,
        temperature: float = settings.GEMINI_TEMPERATURE,
    ) -> None:
        self.llm = get_llm(model=model, temperature=temperature)
        self.parser: PydanticOutputParser = parser

    def parse_cv(self, cv_path: str) -> CVData:
        """Parse a signle cv file document or image"""
        try:
            file_type_extension = get_file_type_extension(cv_path)
            file_based64 = encode_file_to_base64(cv_path)
            prompt_template = ChatPromptTemplate(
                [
                    ("system", CV_PARSING_SYSTEM_PROMPT),
                    (
                        "human",
                        [
                            {
                                "type": "text",
                                "text": "Please analyze this CV and extract all information according to the structured format provided in the system message.",
                            },
                            {
                                "type": "media",
                                "source_type": "base64",
                                "data": file_based64,
                                "mime_type": file_type_extension[1],
                            },
                        ],
                    ),
                ]
            )
            prompt_messages = prompt_template.invoke(
                {"format_instructions": self.parser.get_format_instructions()}
            )
            parsed_data = self.llm.with_structured_output(CVData).invoke(prompt_messages)
            return parsed_data

        except Exception as e:
            print(f"Error parsing {file_type_extension[0]} {cv_path}: {e}")
            return None

    def parse_job_description(self, jd_path: str) -> JobData:
        """Parse a job description text and extract structured information"""
        try:
            file_type_extension = get_file_type_extension(jd_path)
            file_based64 = encode_file_to_base64(jd_path)
            prompt_template = ChatPromptTemplate(
                [
                    ("system", JOB_DESCRIPTION_PARSING_SYSTEM_PROMPT),
                    (
                        "human",
                        [
                            {
                                "type": "text",
                                "text": "Please analyze this job description document and extract all information according to the structured format provided in the system message.",
                            },
                            {
                                "type": "media",
                                "source_type": "base64",
                                "data": file_based64,
                                "mime_type": file_type_extension[1],
                            },
                        ],
                    ),
                ]
            )

            prompt_messages = prompt_template.invoke(
                {"format_instructions": self.parser.get_format_instructions()}
            )
            parsed_data = self.llm.with_structured_output(JobData).invoke(prompt_messages)
            return parsed_data

        except Exception as e:
            print(f"Error parsing job description: {e}")
            return None
