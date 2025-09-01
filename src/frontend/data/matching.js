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

export async function getMatchingCandidates({
  jobId,
  minScore = 0.0,
  limit = 50,
}) {
  try {
    const params = new URLSearchParams({
      min_score: minScore.toString(),
      limit: limit.toString(),
    });

    const response = await fetch(
      `${API_BASE_URL}/jobs/${jobId}/matching-candidates?${params}`
    );
    const matches = await handleResponse(response);

    // Transform the matching data to include candidate details
    return matches.map((match) => ({
      candidateId: match.candidate_id,
      candidateName: match.candidate_name || "N/A",
      overallScore: match.overall_score,
      skillsScore: match.skills_score,
      experienceScore: match.experience_score,
      educationScore: match.education_score,
      semanticSimilarity: match.semantic_similarity,
      seniorityMatch: match.seniority_match,
      detailedBreakdown: match.detailed_breakdown,
      // Format percentage scores for display
      overallPercentage: Math.round(match.overall_score * 100),
      skillsPercentage: Math.round(match.skills_score * 100),
      experiencePercentage: Math.round(match.experience_score * 100),
      educationPercentage: Math.round(match.education_score * 100),
    }));
  } catch (error) {
    console.error("Error fetching matching candidates:", error);
    throw error;
  }
}
