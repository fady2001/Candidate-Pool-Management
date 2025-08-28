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
