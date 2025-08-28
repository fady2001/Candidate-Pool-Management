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

    # Logging configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = PROJECT_ROOT / "logs" / "app.log"

    # API settings (for future web interface)
    API_HOST: str = "localhost"
    API_PORT: int = 8000


# Global settings instance
settings = Settings()
