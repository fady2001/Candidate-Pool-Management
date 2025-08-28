import json
from typing import Tuple

from langchain_core.prompts import ChatPromptTemplate

from src.models import CVData
from src.prompts import CV_PARSING_SYSTEM_PROMPT
from src.utils import (
    encode_file_to_base64,
    get_file_type_extension,
    get_llm,
)


class GeminiCVParser:
    """CV Parser using Google Gemini model"""

    def __init__(self, model, temperature, parser):
        self.llm = get_llm(model=model, temperature=temperature)
        self.parser = parser

    def parse_cv(self, cv_path: str, file_type_extension: Tuple[str, str]) -> CVData:
        """Parse a signle cv file document or image"""
        try:
            file_based64 = encode_file_to_base64(cv_path)
            prompt_template = ChatPromptTemplate(
                [
                    ("system", CV_PARSING_SYSTEM_PROMPT),
                    (
                        "human",
                        [
                            {
                                "type": "text",
                                "text": f"Please analyze this {file_type_extension[2]} CV and extract all information according to the structured format provided in the system message.",
                            },
                            {
                                "type": file_type_extension[0],
                                "source_type": "base64",
                                "data": file_based64,
                                "mime_type": f"application/{file_type_extension[1]}",
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


if __name__ == "__main__":
    from langchain_core.output_parsers import PydanticOutputParser

    parser = GeminiCVParser(
        model="gemini-2.5-flash",
        temperature=0.1,
        parser=PydanticOutputParser(pydantic_object=CVData),
    )

    # Test with a sample PDF CV
    sample_pdf = (
        r"""E:\ITI Data science\Candidate-Pool-Management\data\raw\cvs\fiona_lin_resume.jpeg"""
    )
    cv_data = parser.parse_cv(sample_pdf, get_file_type_extension(sample_pdf))
    if cv_data:
        print(json.dumps(cv_data.dict(), indent=4))
    else:
        print("Failed to parse CV.")
