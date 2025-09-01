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
    const response = await fetch(`${API_BASE_URL}/candidates?${queryParams}`);
    const candidates = await handleResponse(response);

    // Transform the candidates data to match the expected format
    return {
      items: candidates.map((candidate) => ({
        id: candidate.id,
        name: candidate.full_name || "N/A",
        email: candidate.email || "N/A",
        phone: candidate.phone || "N/A",
        currentPosition: candidate.current_position || "N/A",
        currentCompany: candidate.current_company || "N/A",
        yearsOfExperience: candidate.years_of_experience || 0,
        location: candidate.address || "N/A",
        linkedin: candidate.linkedin || "",
        github: candidate.github || "",
        website: candidate.website || "",
        summary: candidate.summary || "",
        // Add formatted skills for display
        skills: candidate.skills
          ? candidate.skills
              .map((skillGroup) =>
                skillGroup.skills ? skillGroup.skills.join(", ") : ""
              )
              .filter((skills) => skills)
              .join(" | ")
          : "N/A",
        // Add education for display
        education: candidate.education
          ? candidate.education
              .map(
                (edu) =>
                  `${edu.degree || ""} ${edu.field_of_study || ""} (${
                    edu.institution || ""
                  })`
              )
              .filter((edu) => edu.trim() !== " ()")
              .join(", ")
          : "N/A",
        createdAt: candidate.created_at,
        sourceFile: candidate.source_file,
      })),
      // For server-side pagination, we need to estimate total count
      // Since the backend doesn't return total count, we'll use the items length
      // and add some logic to handle pagination properly
      itemCount:
        candidates.length === paginationModel?.pageSize
          ? (paginationModel.page + 1) * paginationModel.pageSize + 1
          : (paginationModel?.page || 0) * (paginationModel?.pageSize || 100) +
            candidates.length,
    };
  } catch (error) {
    console.error("Error fetching candidates:", error);
    throw error;
  }
}

export async function getOne(candidateId) {
  try {
    const response = await fetch(`${API_BASE_URL}/candidates/${candidateId}`);
    const candidate = await handleResponse(response);

    // Transform the candidate data
    return {
      id: candidate.id,
      name: candidate.full_name || "N/A",
      email: candidate.email || "N/A",
      phone: candidate.phone || "N/A",
      address: candidate.address || "N/A",
      linkedin: candidate.linkedin || "",
      github: candidate.github || "",
      website: candidate.website || "",
      summary: candidate.summary || "",
      currentPosition: candidate.current_position || "N/A",
      currentCompany: candidate.current_company || "N/A",
      yearsOfExperience: candidate.years_of_experience || 0,
      education: candidate.education || [],
      experience: candidate.experience || [],
      skills: candidate.skills || [],
      certifications: candidate.certifications || [],
      languages: candidate.languages || [],
      projects: candidate.projects || [],
      awards: candidate.awards || [],
      publications: candidate.publications || [],
      createdAt: candidate.created_at,
      sourceFile: candidate.source_file,
    };
  } catch (error) {
    console.error("Error fetching candidate:", error);
    throw error;
  }
}

// Note: Create, Update, and Delete operations would require backend API endpoints
// For now, these will throw errors indicating they need to be implemented

export async function createOne() {
  throw new Error(
    "Create candidate functionality requires backend implementation"
  );
}

export async function updateOne() {
  throw new Error(
    "Update candidate functionality requires backend implementation"
  );
}

export async function deleteOne() {
  throw new Error(
    "Delete candidate functionality requires backend implementation"
  );
}

// Validation for candidate data (placeholder)
export function validate(candidate) {
  let issues = [];

  if (!candidate.name) {
    issues = [...issues, { message: "Name is required", path: ["name"] }];
  }

  if (!candidate.email) {
    issues = [...issues, { message: "Email is required", path: ["email"] }];
  }

  return { issues };
}
