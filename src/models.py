from typing import List, Optional

from pydantic import BaseModel, Field


class Education(BaseModel):
    """Education information model"""

    degree: Optional[str] = Field(description="Degree name (e.g., Bachelor's, Master's, PhD)")
    field_of_study: Optional[str] = Field(description="Field of study or major")
    institution: Optional[str] = Field(description="Educational institution name")
    graduation_year: Optional[str] = Field(description="Graduation year")
    gpa: Optional[str] = Field(description="GPA if mentioned")


class Experience(BaseModel):
    """Work experience model"""

    job_title: Optional[str] = Field(description="Job title or position")
    company: Optional[str] = Field(description="Company name")
    duration: Optional[str] = Field(description="Employment duration")
    location: Optional[str] = Field(description="Job location")
    responsibilities: List[str] = Field(
        default=[], description="Key responsibilities and achievements"
    )


class Skill(BaseModel):
    """Skill model"""

    category: Optional[str] = Field(description="Skill category (e.g., Technical, Soft Skills)")
    skills: List[str] = Field(default=[], description="List of skills")


class Certification(BaseModel):
    """Certification model"""

    name: Optional[str] = Field(description="Certification name")
    issuer: Optional[str] = Field(description="Issuing organization")
    date: Optional[str] = Field(description="Date obtained")
    expiry_date: Optional[str] = Field(description="Expiry date if applicable")


class Language(BaseModel):
    """Language proficiency model"""

    name: Optional[str] = Field(description="Language name")
    proficiency: Optional[str] = Field(
        description="Proficiency level (e.g., Basic, Professional, Native)"
    )


class CVData(BaseModel):
    """Complete CV data structure"""

    # Personal Information
    full_name: Optional[str] = Field(description="Full name of the candidate")
    email: Optional[str] = Field(description="Email address")
    phone: Optional[str] = Field(description="Phone number")
    address: Optional[str] = Field(description="Full address")
    linkedin: Optional[str] = Field(description="LinkedIn profile URL")
    github: Optional[str] = Field(description="GitHub profile URL")
    website: Optional[str] = Field(description="Personal website or portfolio URL")

    # Professional Summary
    summary: Optional[str] = Field(description="Professional summary or objective")

    # Education
    education: List[Education] = Field(default=[], description="Educational background")

    # Experience
    experience: List[Experience] = Field(default=[], description="Work experience")

    # Skills
    skills: List[Skill] = Field(default=[], description="Skills categorized by type")

    # Certifications
    certifications: List[Certification] = Field(
        default=[], description="Professional certifications"
    )

    # Additional Information
    languages: List[Language] = Field(default=[], description="Languages spoken")
    projects: List[str] = Field(default=[], description="Notable projects")
    awards: List[str] = Field(default=[], description="Awards and honors")
    publications: List[str] = Field(default=[], description="Publications")

    # Metadata
    years_of_experience: Optional[int] = Field(
        description="Total years of professional experience"
    )
    current_position: Optional[str] = Field(description="Current job title")
    current_company: Optional[str] = Field(description="Current company")


class JobRequirement(BaseModel):
    """Job requirement model"""

    category: Optional[str] = Field(
        description="Requirement category (e.g., Technical, Educational, Experience)"
    )
    requirements: List[str] = Field(default=[], description="List of specific requirements")
    level: Optional[str] = Field(
        description="Required level (e.g., Beginner, Intermediate, Advanced, Expert)"
    )


class CompanyInfo(BaseModel):
    """Company information model"""

    name: Optional[str] = Field(description="Company name")
    industry: Optional[str] = Field(description="Industry sector")
    size: Optional[str] = Field(
        description="Company size (e.g., Startup, Small, Medium, Large, Enterprise)"
    )
    location: Optional[str] = Field(description="Company location or headquarters")
    website: Optional[str] = Field(description="Company website URL")
    description: Optional[str] = Field(description="Brief company description")


class SalaryInfo(BaseModel):
    """Salary and compensation information model"""

    min_salary: Optional[int] = Field(description="Minimum salary amount")
    max_salary: Optional[int] = Field(description="Maximum salary amount")
    currency: Optional[str] = Field(description="Currency code (e.g., USD, EUR, GBP)")
    period: Optional[str] = Field(description="Salary period (e.g., annually, monthly, hourly)")
    benefits: List[str] = Field(default=[], description="Additional benefits and perks")


class JobData(BaseModel):
    """Complete job description data structure"""

    # Job Basic Information
    job_title: Optional[str] = Field(description="Job title or position name")
    job_id: Optional[str] = Field(description="Job posting ID or reference number")
    department: Optional[str] = Field(description="Department or team")
    employment_type: Optional[str] = Field(
        description="Employment type (e.g., Full-time, Part-time, Contract, Freelance)"
    )
    work_arrangement: Optional[str] = Field(
        description="Work arrangement (e.g., Remote, Hybrid, On-site)"
    )
    location: Optional[str] = Field(description="Job location")

    # Company Information
    company: Optional[CompanyInfo] = Field(description="Company details")

    # Job Description
    job_summary: Optional[str] = Field(description="Brief job summary or overview")
    job_description: Optional[str] = Field(description="Detailed job description")
    responsibilities: List[str] = Field(default=[], description="Key responsibilities and duties")

    # Requirements and Qualifications
    required_skills: List[JobRequirement] = Field(
        default=[], description="Required skills categorized by type"
    )
    preferred_skills: List[JobRequirement] = Field(
        default=[], description="Preferred/nice-to-have skills"
    )
    education_requirements: List[str] = Field(default=[], description="Educational requirements")
    experience_requirements: List[str] = Field(default=[], description="Experience requirements")
    certifications_required: List[str] = Field(default=[], description="Required certifications")
    certifications_preferred: List[str] = Field(default=[], description="Preferred certifications")
    languages_required: List[Language] = Field(default=[], description="Required language skills")

    # Compensation and Benefits
    salary_info: Optional[SalaryInfo] = Field(description="Salary and compensation details")

    # Application Information
    application_deadline: Optional[str] = Field(description="Application deadline date")
    application_process: Optional[str] = Field(description="How to apply or application process")
    contact_email: Optional[str] = Field(description="Contact email for applications or inquiries")
    contact_person: Optional[str] = Field(description="Contact person name")

    # Additional Information
    travel_requirements: Optional[str] = Field(description="Travel requirements if any")
    security_clearance: Optional[str] = Field(description="Security clearance requirements")
    visa_sponsorship: Optional[bool] = Field(description="Whether visa sponsorship is available")
    diversity_statement: Optional[str] = Field(
        description="Company diversity and inclusion statement"
    )

    # Metadata
    posted_date: Optional[str] = Field(description="Job posting date")
    last_updated: Optional[str] = Field(description="Last updated date")
    urgency_level: Optional[str] = Field(description="Urgency level (e.g., Urgent, Normal, Low)")
    seniority_level: Optional[str] = Field(
        description="Seniority level (e.g., Entry-level, Mid-level, Senior, Executive)"
    )
    min_years_experience: Optional[int] = Field(description="Minimum years of experience required")
    max_years_experience: Optional[int] = Field(
        description="Maximum years of experience preferred"
    )


# Batch Processing Models


class FileInfo(BaseModel):
    """File information for batch processing"""

    file_path: str = Field(description="Path to the file")
    file_name: str = Field(description="Original filename")
    file_type: str = Field(description="File type (image/document)")
    mime_type: str = Field(description="MIME type of the file")
    file_size_bytes: int = Field(description="File size in bytes")
    base64_content: str = Field(description="Base64 encoded file content")


class CVBatchResult(BaseModel):
    """Result for a single CV in batch processing"""

    file_info: FileInfo = Field(description="Information about the processed file")
    cv_data: Optional[CVData] = Field(description="Extracted CV data, null if parsing failed")
    success: bool = Field(description="Whether parsing was successful")
    error_message: Optional[str] = Field(description="Error message if parsing failed")
    processing_time_seconds: Optional[float] = Field(description="Time taken to process this CV")


class JobBatchResult(BaseModel):
    """Result for a single job description in batch processing"""

    file_info: FileInfo = Field(description="Information about the processed file")
    job_data: Optional[JobData] = Field(description="Extracted job data, null if parsing failed")
    success: bool = Field(description="Whether parsing was successful")
    error_message: Optional[str] = Field(description="Error message if parsing failed")
    processing_time_seconds: Optional[float] = Field(
        description="Time taken to process this job description"
    )


class CVBatchResponse(BaseModel):
    """Structured response for CV batch processing from LLM"""

    cvs: List[CVData] = Field(description="List of extracted CV data for each file")


class JobBatchResponse(BaseModel):
    """Structured response for Job batch processing from LLM"""

    jobs: List[JobData] = Field(description="List of extracted job data for each file")


class CVBatchData(BaseModel):
    """Batch processing result for multiple CVs"""

    batch_id: str = Field(description="Unique identifier for this batch")
    total_files: int = Field(description="Total number of files in the batch")
    successful_parses: int = Field(description="Number of successfully parsed files")
    failed_parses: int = Field(description="Number of failed parses")
    batch_processing_time_seconds: float = Field(
        description="Total time taken for the entire batch"
    )
    results: List[CVBatchResult] = Field(description="Individual results for each CV")


class JobBatchData(BaseModel):
    """Batch processing result for multiple job descriptions"""

    batch_id: str = Field(description="Unique identifier for this batch")
    total_files: int = Field(description="Total number of files in the batch")
    successful_parses: int = Field(description="Number of successfully parsed files")
    failed_parses: int = Field(description="Number of failed parses")
    batch_processing_time_seconds: float = Field(
        description="Total time taken for the entire batch"
    )
    results: List[JobBatchResult] = Field(
        description="Individual results for each job description"
    )


class BatchProcessingStats(BaseModel):
    """Overall statistics for batch processing session"""

    session_id: str = Field(description="Unique identifier for the processing session")
    total_batches: int = Field(description="Total number of batches processed")
    total_files: int = Field(description="Total number of files processed")
    total_successful: int = Field(description="Total number of successful parses")
    total_failed: int = Field(description="Total number of failed parses")
    total_processing_time_seconds: float = Field(description="Total time for entire session")
    average_batch_size: float = Field(description="Average number of files per batch")
    success_rate: float = Field(description="Success rate as percentage")
    start_time: str = Field(description="Session start timestamp")
    end_time: str = Field(description="Session end timestamp")
