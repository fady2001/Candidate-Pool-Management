import base64
import os
from pathlib import Path
import time
from typing import List, Tuple
import uuid

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from loguru import logger

from src.backend.config import settings
from src.backend.models import FileInfo


def get_llm(model="gemini-2.5-flash", temperature=0.1) -> ChatGoogleGenerativeAI:
    """Initialize and return a Google Gemini LLM instance."""
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(
        model=model, google_api_key=GOOGLE_API_KEY, temperature=temperature
    )
    logger.info(f"Initialized LLM with model: {model}")
    return llm


def get_embedding_model(model="models/embedding-001") -> GoogleGenerativeAIEmbeddings:
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    embedding_model = GoogleGenerativeAIEmbeddings(model=model, google_api_key=GOOGLE_API_KEY)
    return embedding_model


def encode_file_to_base64(file_path: str) -> str:
    """Encode an image file to a base64 string."""
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode("utf-8")
    return encoded_string


def get_file_type_extension(file_path: Path) -> Tuple[str, str]:
    """Determine file type based on extension"""
    extension = file_path.suffix.lower()
    if extension in settings.SUPPORTED_CV_FORMATS["documents"]:
        return "file", "application/pdf"
    elif extension in settings.SUPPORTED_CV_FORMATS["images"]:
        return "image", "image/jpeg"
    else:
        return "unknown", "unknown"


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes"""
    return os.path.getsize(file_path)


def create_file_info(file_path: Path) -> FileInfo:
    """Create FileInfo object for a given file"""
    file_type, mime_type = get_file_type_extension(file_path)
    file_size = get_file_size(file_path)
    base64_content = encode_file_to_base64(file_path)

    return FileInfo(
        file_path=str(file_path),
        file_name=file_path.name,
        file_type=file_type,
        mime_type=mime_type,
        file_size_bytes=file_size,
        base64_content=base64_content,
    )


def create_batches(
    file_paths: List[Path], batch_size: int, max_size_mb: int = None
) -> List[List[Path]]:
    """
    Create batches of files based on batch size and optional maximum total size per batch.

    Args:
        file_paths: List of file paths to batch
        batch_size: Maximum number of files per batch
        max_size_mb: Maximum total size per batch in MB (optional)

    Returns:
        List of batches, where each batch is a list of file paths
    """
    if not file_paths:
        return []

    batches: List[List[Path]] = []
    current_batch: List[Path] = []
    current_batch_size_bytes = 0
    max_size_bytes = max_size_mb * 1024 * 1024 if max_size_mb else float("inf")

    for file_path in file_paths:
        try:
            file_size = get_file_size(file_path)

            if (
                len(current_batch) >= batch_size
                or current_batch_size_bytes + file_size > max_size_bytes
            ):
                if current_batch:
                    batches.append(current_batch)
                    current_batch = []
                    current_batch_size_bytes = 0

            current_batch.append(file_path)
            current_batch_size_bytes += file_size

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            continue

    if current_batch:
        batches.append(current_batch)

    logger.info(f"Created {len(batches)} batches from {len(file_paths)} files")
    return batches


def generate_batch_id() -> str:
    """Generate a unique batch ID"""
    return f"batch_{uuid.uuid4().hex[:8]}_{int(time.time())}"


def generate_session_id() -> str:
    """Generate a unique session ID"""
    return f"session_{uuid.uuid4().hex[:8]}_{int(time.time())}"


def calculate_success_rate(successful: int, total: int) -> float:
    """Calculate success rate as percentage"""
    if total == 0:
        return 0.0
    return (successful / total) * 100.0


def filter_supported_files(file_paths: List[Path]) -> List[Path]:
    """Filter out unsupported file types"""
    supported_files = []

    for file_path in file_paths:
        file_type, _ = get_file_type_extension(file_path)
        if file_type != "unknown":
            supported_files.append(file_path)
        else:
            logger.warning(f"Skipping unsupported file: {file_path.name}")

    return supported_files
