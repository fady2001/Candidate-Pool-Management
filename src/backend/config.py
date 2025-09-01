from datetime import datetime
from pathlib import Path
from typing import List

from loguru import logger
from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    INTERIM_DATA_DIR: Path = DATA_DIR / "interim"
    MODELS_DIR: Path = PROJECT_ROOT / "models"
    REPORTS_DIR: Path = PROJECT_ROOT / "reports"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"

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

    # Database configuration
    DATABASE_NAME: str = "perfect_candidate_pool.db"
    DATABASE_DIR: str = f"{DATA_DIR}/{DATABASE_NAME}"
    DATABASE_URL: str = f"sqlite:///{DATABASE_DIR}"
    DATABASE_TIMEOUT: int = 30

    # Logging configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = PROJECT_ROOT / "logs" / "app.log"

    # API settings (for future web interface)
    API_HOST: str = "localhost"
    API_PORT: int = 8000

    # Gemini model settings
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_TEMPERATURE: float = 0.1

    # saving cv or jd result
    SAVE_INTO_JSON: bool = False
    SAVE_INTO_DB: bool = True


# Global settings instance
settings = Settings()

settings.LOGS_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"app_{timestamp}.log"
log_filepath = settings.LOGS_DIR / log_filename

# remove default logger
logger.remove()

# configure logger to log to console and file
logger.add(
    lambda msg: print(f"[LOG] {msg}", end=""),
    format="{time:HH:mm:ss} | {level} | {message}",
    level=settings.LOG_LEVEL,
)
logger.add(
    log_filepath,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
    level=settings.LOG_LEVEL,
    rotation="10 MB",
    retention="30 days",
    compression="zip",
)
