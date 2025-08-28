import base64
import os
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from loguru import logger

from config import settings


def get_llm(model="gemini-2.5-flash", temperature=0.1) -> ChatGoogleGenerativeAI:
    """Initialize and return a Google Gemini LLM instance."""
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=GOOGLE_API_KEY,
        temperature=temperature,
    )
    logger.info(f"Initialized LLM with model: {model}")
    return llm


def encode_file_to_base64(file_path: str) -> str:
    """Encode an image file to a base64 string."""
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode("utf-8")
    return encoded_string


def get_file_type_extension(file_path: str) -> Tuple[str, str]:
    """Determine file type based on extension"""
    extension = Path(file_path).suffix.lower()
    if extension in settings.SUPPORTED_CV_FORMATS["documents"]:
        return "file", "application/pdf"
    elif extension in settings.SUPPORTED_CV_FORMATS["images"]:
        return "image", f"image/{extension[1:]}"
    else:
        return "unknown", "unknown"
