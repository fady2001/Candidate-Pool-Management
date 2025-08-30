"""
Database models and schema for candidate pool management system using sqlite3.
"""

from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Optional

from loguru import logger

from src.config import settings


class DatabaseManager:
    """Database manager for SQLite operations"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            self.db_path = settings.DATABASE_DIR
        else:
            self.db_path = db_path

        logger.info(f"Using database at: {self.db_path}")

        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self.init_database()

    def init_database(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Create candidates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    linkedin TEXT,
                    github TEXT,
                    website TEXT,
                    summary TEXT,
                    years_of_experience INTEGER,
                    current_position TEXT,
                    current_company TEXT,
                    education TEXT,  -- JSON string
                    experience TEXT,  -- JSON string
                    skills TEXT,  -- JSON string
                    certifications TEXT,  -- JSON string
                    languages TEXT,  -- JSON string
                    projects TEXT,  -- JSON string
                    awards TEXT,  -- JSON string
                    publications TEXT,  -- JSON string
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    source_file TEXT
                )
            """)

            # Create job_descriptions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_descriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_title TEXT NOT NULL,
                    job_id TEXT UNIQUE,
                    department TEXT,
                    employment_type TEXT,
                    work_arrangement TEXT,
                    location TEXT,
                    job_summary TEXT,
                    job_description TEXT,
                    responsibilities TEXT,  -- JSON string
                    company_info TEXT,  -- JSON string
                    required_skills TEXT,  -- JSON string
                    preferred_skills TEXT,  -- JSON string
                    education_requirements TEXT,  -- JSON string
                    experience_requirements TEXT,  -- JSON string
                    certifications_required TEXT,  -- JSON string
                    certifications_preferred TEXT,  -- JSON string
                    languages_required TEXT,  -- JSON string
                    min_years_experience INTEGER,
                    max_years_experience INTEGER,
                    seniority_level TEXT,
                    salary_info TEXT,  -- JSON string
                    application_deadline TEXT,
                    application_process TEXT,
                    contact_email TEXT,
                    contact_person TEXT,
                    travel_requirements TEXT,
                    security_clearance TEXT,
                    visa_sponsorship BOOLEAN,
                    diversity_statement TEXT,
                    urgency_level TEXT,
                    posted_date TEXT,
                    last_updated TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    source_file TEXT
                )
            """)

            # Create candidate_job_matches table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS candidate_job_matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id INTEGER NOT NULL,
                    job_id INTEGER NOT NULL,
                    overall_score REAL,
                    skills_score REAL,
                    experience_score REAL,
                    education_score REAL,
                    match_details TEXT,  -- JSON string
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (candidate_id) REFERENCES candidates (id),
                    FOREIGN KEY (job_id) REFERENCES job_descriptions (id)
                )
            """)

            conn.commit()

            self._reset_autoincrement_sequences(conn.cursor())

            logger.info("Database tables created successfully")

    def _reset_autoincrement_sequences(self, cursor):
        """Reset auto-increment sequences to start from the last existing ID in each table"""
        tables = ["candidates", "job_descriptions", "candidate_job_matches"]

        for table in tables:
            try:
                # Get the maximum ID from the table
                cursor.execute(f"SELECT MAX(id) FROM {table}")
                max_id = cursor.fetchone()[0]

                if max_id is not None:
                    # Update the sqlite_sequence table to set the next auto-increment value
                    cursor.execute(
                        "INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES (?, ?)",
                        (table, max_id),
                    )
                    logger.info(f"Reset auto-increment for {table} to start from {max_id + 1}")
                else:
                    logger.info(f"No existing data in {table}, auto-increment will start from 1")
            except sqlite3.Error as e:
                logger.warning(f"Could not reset auto-increment for {table}: {e}")

    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(self.db_path, timeout=settings.DATABASE_TIMEOUT)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(
        self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False
    ):
        """Execute a query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.lastrowid


# Global database manager instance
db_manager = DatabaseManager()


def create_tables():
    """Create all database tables"""
    db_manager.init_database()


def get_db_connection():
    """Get database connection"""
    return db_manager.get_connection()
