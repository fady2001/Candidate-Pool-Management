from pathlib import Path
from typing import List

from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    MODELS_DIR: Path = PROJECT_ROOT / "models"
    REPORTS_DIR: Path = PROJECT_ROOT / "reports"

    SUPPORTED_CV_FORMATS: List[str] = {
        "images": [".png", ".jpg", ".jpeg"],
        "documents": [".pdf", ".docx", ".doc"],
        "all": [".png", ".jpg", ".jpeg", ".pdf", ".docx", ".doc"],
    }
    CV_DIRECTORY: Path = RAW_DATA_DIR / "cvs"
    JOB_DESCRIPTIONS_DIR: Path = RAW_DATA_DIR / "Job Descriptions"

    # Batch processing configuration
    BATCH_SIZE_CV: int = 3
    BATCH_SIZE_JOB: int = 2
    MAX_FILE_SIZE_MB: int = 20
    BATCH_RETRY_ATTEMPTS: int = 3
    BATCH_DELAY_SECONDS: float = 1.0

    # Logging configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = PROJECT_ROOT / "logs" / "app.log"

    # API settings (for future web interface)
    API_HOST: str = "localhost"
    API_PORT: int = 8000

    # Gemini model settings
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_TEMPERATURE: float = 0.1


# Global settings instance
settings = Settings()
