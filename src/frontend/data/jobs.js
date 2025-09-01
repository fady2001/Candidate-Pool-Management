// API configuration
const API_BASE_URL = "http://localhost:8000"; // Match your backend API port

// Helper function to handle API responses
async function handleResponse(response) {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || `HTTP error! status: ${response.status}`
    );
  }
  return response.json();
}

// Helper function to build query parameters
function buildQueryParams({ paginationModel, filterModel }) {
  const params = new URLSearchParams();

  // Pagination
  if (paginationModel) {
    params.append(
      "skip",
      (paginationModel.page * paginationModel.pageSize).toString()
    );
    params.append("limit", paginationModel.pageSize.toString());
  }

  // Search/Filter - convert MUI DataGrid filters to backend search
  if (filterModel?.quickFilterValues?.length > 0) {
    params.append("search", filterModel.quickFilterValues.join(" "));
  } else if (filterModel?.items?.length > 0) {
    // Handle specific field filters
    const searchTerms = filterModel.items
      .filter((item) => item.value && item.value.trim())
      .map((item) => item.value)
      .join(" ");
    if (searchTerms) {
      params.append("search", searchTerms);
    }
  }

  return params;
}

export async function getMany({ paginationModel, filterModel, sortModel }) {
  try {
    const queryParams = buildQueryParams({
      paginationModel,
      filterModel,
      sortModel,
    });
    const response = await fetch(`${API_BASE_URL}/jobs?${queryParams}`);
    const jobs = await handleResponse(response);

    // Transform the jobs data to match the expected format
    return {
      items: jobs.map((job) => ({
        id: job.id,
        jobTitle: job.job_title || "N/A",
        company: job.company_info?.name || "N/A",
        department: job.department || "N/A",
        location: job.location || "N/A",
        employmentType: job.employment_type || "N/A",
        workArrangement: job.work_arrangement || "N/A",
        experienceLevel: job.seniority_level || "N/A",
        minExperience: job.min_years_experience || 0,
        maxExperience: job.max_years_experience || 0,
        summary: job.job_summary || "N/A",
        // Format required skills for display
        requiredSkills: job.required_skills
          ? job.required_skills
              .map((skillGroup) =>
                skillGroup.skills ? skillGroup.skills.join(", ") : ""
              )
              .filter((skills) => skills)
              .join(" | ")
          : "N/A",
        // Format salary info for display
        salaryInfo: job.salary_info
          ? `${job.salary_info.currency || ""} ${job.salary_info.min || ""} - ${
              job.salary_info.max || ""
            } ${job.salary_info.frequency || ""}`
          : "N/A",
        urgencyLevel: job.urgency_level || "Normal",
        postedDate: job.posted_date,
        createdAt: job.created_at,
        sourceFile: job.source_file,
      })),
      // For server-side pagination, we need to estimate total count
      itemCount:
        jobs.length === paginationModel?.pageSize
          ? (paginationModel.page + 1) * paginationModel.pageSize + 1
          : (paginationModel?.page || 0) * (paginationModel?.pageSize || 100) +
            jobs.length,
    };
  } catch (error) {
    console.error("Error fetching jobs:", error);
    throw error;
  }
}

export async function getOne(jobId) {
  try {
    const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`);
    const job = await handleResponse(response);

    // Transform the job data
    return {
      id: job.id,
      jobTitle: job.job_title || "N/A",
      jobId: job.job_id || "",
      department: job.department || "N/A",
      employmentType: job.employment_type || "N/A",
      workArrangement: job.work_arrangement || "N/A",
      location: job.location || "N/A",
      company: job.company_info || {},
      summary: job.job_summary || "",
      description: job.job_description || "",
      responsibilities: job.responsibilities || [],
      requiredSkills: job.required_skills || [],
      preferredSkills: job.preferred_skills || [],
      educationRequirements: job.education_requirements || [],
      experienceRequirements: job.experience_requirements || [],
      certificationsRequired: job.certifications_required || [],
      certificationsPreferred: job.certifications_preferred || [],
      languagesRequired: job.languages_required || [],
      minExperience: job.min_years_experience || 0,
      maxExperience: job.max_years_experience || 0,
      seniorityLevel: job.seniority_level || "",
      salaryInfo: job.salary_info || {},
      applicationDeadline: job.application_deadline || "",
      applicationProcess: job.application_process || "",
      contactEmail: job.contact_email || "",
      contactPerson: job.contact_person || "",
      travelRequirements: job.travel_requirements || "",
      securityClearance: job.security_clearance || "",
      visaSponsorship: job.visa_sponsorship || false,
      diversityStatement: job.diversity_statement || "",
      urgencyLevel: job.urgency_level || "Normal",
      postedDate: job.posted_date || "",
      lastUpdated: job.last_updated || "",
      createdAt: job.created_at,
      sourceFile: job.source_file,
    };
  } catch (error) {
    console.error("Error fetching job:", error);
    throw error;
  }
}

export async function deleteOne(jobId) {
  try {
    const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`
      );
    }

    return true;
  } catch (error) {
    console.error("Error deleting job:", error);
    throw error;
  }
}

// Note: Create and Update operations would require backend API endpoints
// For now, these will throw errors indicating they need to be implemented

export async function createOne() {
  throw new Error("Create job functionality requires backend implementation");
}

export async function updateOne() {
  throw new Error("Update job functionality requires backend implementation");
}

// Validation for job data (placeholder)
export function validate(job) {
  let issues = [];

  if (!job.jobTitle) {
    issues = [
      ...issues,
      { message: "Job title is required", path: ["jobTitle"] },
    ];
  }

  if (!job.company) {
    issues = [...issues, { message: "Company is required", path: ["company"] }];
  }

  return { issues };
}
