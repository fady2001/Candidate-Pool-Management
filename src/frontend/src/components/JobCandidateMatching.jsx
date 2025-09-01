import * as React from "react";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Chip from "@mui/material/Chip";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import LinearProgress from "@mui/material/LinearProgress";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import Slider from "@mui/material/Slider";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Tooltip from "@mui/material/Tooltip";
import IconButton from "@mui/material/IconButton";
import { DataGrid, GridActionsCellItem, gridClasses } from "@mui/x-data-grid";
import PersonIcon from "@mui/icons-material/Person";
import WorkIcon from "@mui/icons-material/Work";
import SchoolIcon from "@mui/icons-material/School";
import BuildIcon from "@mui/icons-material/Build";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import RefreshIcon from "@mui/icons-material/Refresh";
import VisibilityIcon from "@mui/icons-material/Visibility";
import { useNavigate } from "react-router";
import useNotifications from "../hooks/useNotifications/useNotifications";
import { getMany as getJobs } from "../../data/jobs";
import { getMatchingCandidates } from "../../data/matching";
import PageContainer from "./PageContainer";

const INITIAL_PAGE_SIZE = 10;

export default function JobCandidateMatching() {
  const navigate = useNavigate();
  const notifications = useNotifications();

  // State for job selection and filters
  const [selectedJobId, setSelectedJobId] = React.useState("");
  const [selectedJob, setSelectedJob] = React.useState(null);
  const [minScore, setMinScore] = React.useState(0.3);
  const [maxResults, setMaxResults] = React.useState(50);

  // State for jobs list
  const [jobs, setJobs] = React.useState([]);
  const [jobsLoading, setJobsLoading] = React.useState(true);

  // State for matching results
  const [matchingCandidates, setMatchingCandidates] = React.useState([]);
  const [matchingLoading, setMatchingLoading] = React.useState(false);
  const [matchingError, setMatchingError] = React.useState(null);

  // Load jobs on component mount
  React.useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = React.useCallback(async () => {
    setJobsLoading(true);
    try {
      const jobsData = await getJobs({
        paginationModel: { page: 0, pageSize: 1000 },
        filterModel: { items: [] },
        sortModel: [],
      });
      setJobs(jobsData.items);
    } catch (error) {
      notifications.show(`Failed to load jobs: ${error.message}`, {
        severity: "error",
        autoHideDuration: 3000,
      });
    }
    setJobsLoading(false);
  }, [notifications]);

  const handleJobChange = React.useCallback(
    (event) => {
      const jobId = event.target.value;
      setSelectedJobId(jobId);
      const job = jobs.find((j) => j.id === jobId);
      setSelectedJob(job);
      setMatchingCandidates([]);
      setMatchingError(null);
    },
    [jobs]
  );

  const handleFindMatches = React.useCallback(async () => {
    if (!selectedJobId) {
      notifications.show("Please select a job first", {
        severity: "warning",
        autoHideDuration: 3000,
      });
      return;
    }

    setMatchingLoading(true);
    setMatchingError(null);
    try {
      const matches = await getMatchingCandidates({
        jobId: selectedJobId,
        minScore: minScore,
        limit: maxResults,
      });
      setMatchingCandidates(matches);

      notifications.show(
        `Found ${matches.length} matching candidates with score ≥ ${Math.round(
          minScore * 100
        )}%`,
        {
          severity: "success",
          autoHideDuration: 3000,
        }
      );
    } catch (error) {
      setMatchingError(error);
      notifications.show(
        `Failed to find matching candidates: ${error.message}`,
        {
          severity: "error",
          autoHideDuration: 3000,
        }
      );
    }
    setMatchingLoading(false);
  }, [selectedJobId, minScore, maxResults, notifications]);

  const handleViewCandidate = React.useCallback(
    (candidateId) => () => {
      navigate(`/candidates/${candidateId}`);
    },
    [navigate]
  );

  const renderScoreProgress = React.useCallback((params) => {
    const score = params.value;
    const percentage = Math.round(score * 100);

    let color = "error";
    if (percentage >= 80) color = "success";
    else if (percentage >= 60) color = "warning";
    else if (percentage >= 40) color = "info";

    return (
      <Box sx={{ display: "flex", alignItems: "center", width: "100%" }}>
        <Box sx={{ width: "100%", mr: 1 }}>
          <LinearProgress
            variant="determinate"
            value={percentage}
            color={color}
            sx={{ height: 8, borderRadius: 5 }}
          />
        </Box>
        <Box sx={{ minWidth: 35 }}>
          <Typography variant="body2" color="text.secondary">
            {percentage}%
          </Typography>
        </Box>
      </Box>
    );
  }, []);

  const renderCandidateInfo = React.useCallback((params) => {
    return (
      <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
        <PersonIcon fontSize="small" color="action" />
        <Box>
          <Typography variant="body2" sx={{ fontWeight: "medium" }}>
            {params.value}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            ID: {params.row.candidateId}
          </Typography>
        </Box>
      </Box>
    );
  }, []);

  const columns = React.useMemo(
    () => [
      {
        field: "candidateName",
        headerName: "Candidate",
        width: 200,
        renderCell: renderCandidateInfo,
      },
      {
        field: "overallScore",
        headerName: "Overall Match",
        width: 150,
        renderCell: renderScoreProgress,
      },
      {
        field: "skillsScore",
        headerName: "Skills",
        width: 120,
        renderCell: (params) => (
          <Tooltip title="Skills compatibility score">
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <BuildIcon fontSize="small" color="action" />
              <Typography variant="body2">
                {Math.round(params.value * 100)}%
              </Typography>
            </Box>
          </Tooltip>
        ),
      },
      {
        field: "experienceScore",
        headerName: "Experience",
        width: 120,
        renderCell: (params) => (
          <Tooltip title="Experience relevance score">
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <WorkIcon fontSize="small" color="action" />
              <Typography variant="body2">
                {Math.round(params.value * 100)}%
              </Typography>
            </Box>
          </Tooltip>
        ),
      },
      {
        field: "educationScore",
        headerName: "Education",
        width: 120,
        renderCell: (params) => (
          <Tooltip title="Education compatibility score">
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <SchoolIcon fontSize="small" color="action" />
              <Typography variant="body2">
                {Math.round(params.value * 100)}%
              </Typography>
            </Box>
          </Tooltip>
        ),
      },
      {
        field: "seniorityMatch",
        headerName: "Seniority",
        width: 120,
        renderCell: (params) => {
          const percentage = Math.round(params.value * 100);
          return (
            <Chip
              label={`${percentage}%`}
              variant="outlined"
              size="small"
              color={
                percentage >= 80
                  ? "success"
                  : percentage >= 60
                  ? "warning"
                  : "default"
              }
            />
          );
        },
      },
      {
        field: "actions",
        type: "actions",
        headerName: "Actions",
        width: 100,
        getActions: ({ row }) => [
          <GridActionsCellItem
            key="view"
            icon={<VisibilityIcon />}
            label="View Profile"
            onClick={handleViewCandidate(row.candidateId)}
          />,
        ],
      },
    ],
    [renderCandidateInfo, renderScoreProgress, handleViewCandidate]
  );

  const pageTitle = "Job-Candidate Matching";

  return (
    <PageContainer
      title={pageTitle}
      breadcrumbs={[{ title: pageTitle }]}
      actions={
        <Stack direction="row" alignItems="center" spacing={1}>
          <Tooltip
            title="Refresh jobs list"
            placement="right"
            enterDelay={1000}
          >
            <IconButton size="small" onClick={loadJobs} disabled={jobsLoading}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Stack>
      }
    >
      <Box sx={{ flex: 1, width: "100%" }}>
        <Grid container spacing={3}>
          {/* Job Selection and Filters */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Find Matching Candidates
                </Typography>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs={12} md={4}>
                    <FormControl fullWidth>
                      <InputLabel>Select Job</InputLabel>
                      <Select
                        value={selectedJobId}
                        onChange={handleJobChange}
                        label="Select Job"
                        disabled={jobsLoading}
                      >
                        {jobs.map((job) => (
                          <MenuItem key={job.id} value={job.id}>
                            {job.jobTitle} - {job.company}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Typography gutterBottom>
                      Minimum Score: {Math.round(minScore * 100)}%
                    </Typography>
                    <Slider
                      value={minScore}
                      onChange={(_, value) => setMinScore(value)}
                      min={0}
                      max={1}
                      step={0.05}
                      marks={[
                        { value: 0, label: "0%" },
                        { value: 0.5, label: "50%" },
                        { value: 1, label: "100%" },
                      ]}
                    />
                  </Grid>
                  <Grid item xs={12} md={2}>
                    <FormControl fullWidth>
                      <InputLabel>Max Results</InputLabel>
                      <Select
                        value={maxResults}
                        onChange={(e) => setMaxResults(e.target.value)}
                        label="Max Results"
                      >
                        <MenuItem value={10}>10</MenuItem>
                        <MenuItem value={25}>25</MenuItem>
                        <MenuItem value={50}>50</MenuItem>
                        <MenuItem value={100}>100</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Button
                      variant="contained"
                      onClick={handleFindMatches}
                      disabled={!selectedJobId || matchingLoading}
                      fullWidth
                      size="large"
                      startIcon={<TrendingUpIcon />}
                    >
                      {matchingLoading ? "Finding..." : "Find Matches"}
                    </Button>
                  </Grid>
                </Grid>

                {/* Selected Job Info */}
                {selectedJob && (
                  <Box
                    sx={{ mt: 2, p: 2, bgcolor: "grey.50", borderRadius: 1 }}
                  >
                    <Typography variant="subtitle2" gutterBottom>
                      Selected Job:
                    </Typography>
                    <Typography variant="body2">
                      <strong>{selectedJob.jobTitle}</strong> at{" "}
                      {selectedJob.company}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {selectedJob.location} • {selectedJob.employmentType} •{" "}
                      {selectedJob.experienceLevel}
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* Results */}
          <Grid item xs={12}>
            {matchingError ? (
              <Alert severity="error">
                Failed to find matching candidates: {matchingError.message}
                <br />
                <small>
                  Make sure the backend API is running on http://localhost:8000
                </small>
              </Alert>
            ) : matchingCandidates.length > 0 ? (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Matching Candidates ({matchingCandidates.length})
                  </Typography>
                  <DataGrid
                    rows={matchingCandidates}
                    columns={columns}
                    getRowId={(row) => row.candidateId}
                    pagination
                    paginationMode="client"
                    pageSizeOptions={[5, INITIAL_PAGE_SIZE, 25, 50]}
                    initialState={{
                      pagination: {
                        paginationModel: { pageSize: INITIAL_PAGE_SIZE },
                      },
                    }}
                    disableRowSelectionOnClick
                    loading={matchingLoading}
                    sx={{
                      height: 600,
                      [`& .${gridClasses.columnHeader}, & .${gridClasses.cell}`]:
                        {
                          outline: "transparent",
                        },
                      [`& .${gridClasses.columnHeader}:focus-within, & .${gridClasses.cell}:focus-within`]:
                        {
                          outline: "none",
                        },
                      "& .MuiDataGrid-cell": {
                        borderBottom: "1px solid #f0f0f0",
                      },
                    }}
                  />
                </CardContent>
              </Card>
            ) : selectedJobId && !matchingLoading ? (
              <Card>
                <CardContent>
                  <Typography
                    variant="h6"
                    color="text.secondary"
                    textAlign="center"
                  >
                    No matching candidates found
                  </Typography>
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    textAlign="center"
                  >
                    Try lowering the minimum score threshold
                  </Typography>
                </CardContent>
              </Card>
            ) : !selectedJobId ? (
              <Card>
                <CardContent>
                  <Typography
                    variant="h6"
                    color="text.secondary"
                    textAlign="center"
                  >
                    Select a job to find matching candidates
                  </Typography>
                </CardContent>
              </Card>
            ) : null}
          </Grid>
        </Grid>
      </Box>
    </PageContainer>
  );
}
