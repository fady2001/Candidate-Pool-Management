import * as React from 'react';
import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import Link from '@mui/material/Link';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import GitHubIcon from '@mui/icons-material/GitHub';
import LanguageIcon from '@mui/icons-material/Language';
import WorkIcon from '@mui/icons-material/Work';
import SchoolIcon from '@mui/icons-material/School';
import { useNavigate, useParams } from 'react-router';
import dayjs from 'dayjs';
import { useDialogs } from '../hooks/useDialogs/useDialogs';
import useNotifications from '../hooks/useNotifications/useNotifications';
import {
  deleteOne as deleteCandidate,
  getOne as getCandidate,
} from '../../data/candidates';
import PageContainer from './PageContainer';

export default function CandidateShow() {
  const { candidateId } = useParams();
  const navigate = useNavigate();

  const dialogs = useDialogs();
  const notifications = useNotifications();

  const [candidate, setCandidate] = React.useState(null);
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  const loadData = React.useCallback(async () => {
    setError(null);
    setIsLoading(true);

    try {
      const showData = await getCandidate(Number(candidateId));
      setCandidate(showData);
    } catch (showDataError) {
      setError(showDataError);
    }
    setIsLoading(false);
  }, [candidateId]);

  React.useEffect(() => {
    loadData();
  }, [loadData]);

  const handleCandidateEdit = React.useCallback(() => {
    navigate(`/candidates/${candidateId}/edit`);
  }, [navigate, candidateId]);

  const handleCandidateDelete = React.useCallback(async () => {
    if (!candidate) {
      return;
    }

    const confirmed = await dialogs.confirm(
      `Do you wish to delete ${candidate.name}?`,
      {
        title: `Delete candidate?`,
        severity: 'error',
        okText: 'Delete',
        cancelText: 'Cancel',
      },
    );

    if (confirmed) {
      setIsLoading(true);
      try {
        await deleteCandidate(Number(candidateId));
        navigate('/candidates');
        notifications.show('Candidate deleted successfully.', {
          severity: 'success',
          autoHideDuration: 3000,
        });
      } catch (deleteError) {
        notifications.show(
          `Failed to delete candidate. Reason: ${deleteError.message}`,
          {
            severity: 'error',
            autoHideDuration: 3000,
          },
        );
      }
      setIsLoading(false);
    }
  }, [candidate, dialogs, candidateId, navigate, notifications]);

  const handleBack = React.useCallback(() => {
    navigate('/candidates');
  }, [navigate]);

  const renderProfileLinks = React.useCallback(() => {
    if (!candidate) return null;
    
    const links = [];
    if (candidate.linkedin) {
      links.push(
        <Link key="linkedin" href={candidate.linkedin} target="_blank" rel="noopener noreferrer">
          <Chip icon={<LinkedInIcon />} label="LinkedIn" variant="outlined" size="small" clickable />
        </Link>
      );
    }
    if (candidate.github) {
      links.push(
        <Link key="github" href={candidate.github} target="_blank" rel="noopener noreferrer">
          <Chip icon={<GitHubIcon />} label="GitHub" variant="outlined" size="small" clickable />
        </Link>
      );
    }
    if (candidate.website) {
      links.push(
        <Link key="website" href={candidate.website} target="_blank" rel="noopener noreferrer">
          <Chip icon={<LanguageIcon />} label="Website" variant="outlined" size="small" clickable />
        </Link>
      );
    }
    return links.length > 0 ? <Stack direction="row" spacing={1}>{links}</Stack> : null;
  }, [candidate]);

  const renderSkills = React.useCallback(() => {
    if (!candidate?.skills || candidate.skills.length === 0) return "N/A";
    
    return candidate.skills.map((skillGroup, index) => (
      <Box key={index} sx={{ mb: 1 }}>
        {skillGroup.category && (
          <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 'bold' }}>
            {skillGroup.category}:
          </Typography>
        )}
        <Box sx={{ mt: 0.5 }}>
          {skillGroup.skills?.map((skill, skillIndex) => (
            <Chip key={skillIndex} label={skill} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
          ))}
        </Box>
      </Box>
    ));
  }, [candidate]);

  const renderEducation = React.useCallback(() => {
    if (!candidate?.education || candidate.education.length === 0) return "N/A";
    
    return candidate.education.map((edu, index) => (
      <Box key={index} sx={{ mb: 1 }}>
        <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
          {edu.degree} {edu.field_of_study && `in ${edu.field_of_study}`}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {edu.institution} {edu.graduation_year && `(${edu.graduation_year})`}
        </Typography>
        {edu.gpa && (
          <Typography variant="caption" color="text.secondary">
            GPA: {edu.gpa}
          </Typography>
        )}
      </Box>
    ));
  }, [candidate]);

  const renderExperience = React.useCallback(() => {
    if (!candidate?.experience || candidate.experience.length === 0) return "N/A";
    
    return candidate.experience.map((exp, index) => (
      <Box key={index} sx={{ mb: 2 }}>
        <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
          {exp.position} at {exp.company}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {exp.start_date} - {exp.end_date || 'Present'}
        </Typography>
        {exp.description && (
          <Typography variant="body2" sx={{ mt: 0.5 }}>
            {exp.description}
          </Typography>
        )}
      </Box>
    ));
  }, [candidate]);

  const renderShow = React.useMemo(() => {
    if (isLoading) {
      return (
        <Box
          sx={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            width: '100%',
            m: 1,
          }}
        >
          <CircularProgress />
        </Box>
      );
    }
    if (error) {
      return (
        <Box sx={{ flexGrow: 1 }}>
          <Alert severity="error">
            Failed to load candidate: {error.message}
            <br />
            <small>Make sure the backend API is running on http://localhost:8000</small>
          </Alert>
        </Box>
      );
    }

    return candidate ? (
      <Box sx={{ flexGrow: 1, width: '100%' }}>
        <Grid container spacing={2} sx={{ width: '100%' }}>
          {/* Basic Information */}
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Name</Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                {candidate.name}
              </Typography>
            </Paper>
          </Grid>
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Experience</Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                {candidate.yearsOfExperience} years
              </Typography>
            </Paper>
          </Grid>
          
          {/* Contact Information */}
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Email</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <EmailIcon fontSize="small" color="action" />
                <Typography variant="body1" sx={{ mb: 1 }}>
                  {candidate.email}
                </Typography>
              </Box>
            </Paper>
          </Grid>
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Phone</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <PhoneIcon fontSize="small" color="action" />
                <Typography variant="body1" sx={{ mb: 1 }}>
                  {candidate.phone}
                </Typography>
              </Box>
            </Paper>
          </Grid>
          
          {/* Current Position */}
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Current Position</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <WorkIcon fontSize="small" color="action" />
                <Typography variant="body1" sx={{ mb: 1 }}>
                  {candidate.currentPosition}
                </Typography>
              </Box>
            </Paper>
          </Grid>
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Current Company</Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                {candidate.currentCompany}
              </Typography>
            </Paper>
          </Grid>
          
          {/* Location */}
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Location</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LocationOnIcon fontSize="small" color="action" />
                <Typography variant="body1" sx={{ mb: 1 }}>
                  {candidate.address}
                </Typography>
              </Box>
            </Paper>
          </Grid>
          
          {/* Profile Links */}
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Profile Links</Typography>
              <Box sx={{ mb: 1 }}>
                {renderProfileLinks()}
              </Box>
            </Paper>
          </Grid>

          {/* Summary */}
          {candidate.summary && candidate.summary !== "N/A" && (
            <Grid size={{ xs: 12 }}>
              <Paper sx={{ px: 2, py: 1 }}>
                <Typography variant="overline">Summary</Typography>
                <Typography variant="body1" sx={{ mb: 1 }}>
                  {candidate.summary}
                </Typography>
              </Paper>
            </Grid>
          )}

          {/* Skills */}
          <Grid size={{ xs: 12 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Skills</Typography>
              <Box sx={{ mb: 1 }}>
                {renderSkills()}
              </Box>
            </Paper>
          </Grid>

          {/* Education */}
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Education</Typography>
              <Box sx={{ mb: 1 }}>
                {renderEducation()}
              </Box>
            </Paper>
          </Grid>

          {/* Experience */}
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Work Experience</Typography>
              <Box sx={{ mb: 1 }}>
                {renderExperience()}
              </Box>
            </Paper>
          </Grid>

          {/* Source Information */}
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Source File</Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                {candidate.sourceFile || "N/A"}
              </Typography>
            </Paper>
          </Grid>
          <Grid size={{ xs: 12, sm: 6 }}>
            <Paper sx={{ px: 2, py: 1 }}>
              <Typography variant="overline">Added Date</Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                {candidate.createdAt ? dayjs(candidate.createdAt).format('MMMM D, YYYY') : "N/A"}
              </Typography>
            </Paper>
          </Grid>
        </Grid>
        
        <Divider sx={{ my: 3 }} />
        <Stack direction="row" spacing={2} justifyContent="space-between">
          <Button
            variant="contained"
            startIcon={<ArrowBackIcon />}
            onClick={handleBack}
          >
            Back
          </Button>
          <Stack direction="row" spacing={2}>
            <Button
              variant="contained"
              startIcon={<EditIcon />}
              onClick={handleCandidateEdit}
            >
              Edit
            </Button>
            <Button
              variant="contained"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={handleCandidateDelete}
            >
              Delete
            </Button>
          </Stack>
        </Stack>
      </Box>
    ) : null;
  }, [
    isLoading,
    error,
    candidate,
    handleBack,
    handleCandidateEdit,
    handleCandidateDelete,
    renderProfileLinks,
    renderSkills,
    renderEducation,
    renderExperience,
  ]);

  const pageTitle = `Candidate ${candidateId}`;

  return (
    <PageContainer
      title={pageTitle}
      breadcrumbs={[
        { title: 'Candidates', path: '/candidates' },
        { title: pageTitle },
      ]}
    >
      <Box sx={{ display: 'flex', flex: 1, width: '100%' }}>{renderShow}</Box>
    </PageContainer>
  );
}