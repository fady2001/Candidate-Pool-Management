import * as React from "react";
import PropTypes from "prop-types";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import Divider from "@mui/material/Divider";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import IconButton from "@mui/material/IconButton";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import SaveIcon from "@mui/icons-material/Save";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import { useNavigate } from "react-router";

function CandidateForm(props) {
  const {
    formState,
    onFieldChange,
    onSubmit,
    onReset,
    submitButtonLabel = "Save",
    isLoading = false,
    error,
  } = props;

  const navigate = useNavigate();
  const { values: formValues, errors: formErrors } = formState;

  const handleBack = React.useCallback(() => {
    navigate("/candidates");
  }, [navigate]);

  const handleFormSubmit = React.useCallback(
    async (event) => {
      event.preventDefault();
      try {
        await onSubmit();
      } catch {
        // Error handling is done in the parent component
      }
    },
    [onSubmit]
  );

  const handleSkillAdd = React.useCallback(
    (categoryIndex) => {
      const newSkills = [...(formValues.skills || [])];
      if (!newSkills[categoryIndex]) {
        newSkills[categoryIndex] = { category: "", skills: [] };
      }
      newSkills[categoryIndex].skills.push("");
      onFieldChange("skills", newSkills);
    },
    [formValues.skills, onFieldChange]
  );

  const handleSkillRemove = React.useCallback(
    (categoryIndex, skillIndex) => {
      const newSkills = [...(formValues.skills || [])];
      newSkills[categoryIndex].skills.splice(skillIndex, 1);
      onFieldChange("skills", newSkills);
    },
    [formValues.skills, onFieldChange]
  );

  const handleSkillChange = React.useCallback(
    (categoryIndex, skillIndex, value) => {
      const newSkills = [...(formValues.skills || [])];
      if (!newSkills[categoryIndex]) {
        newSkills[categoryIndex] = { category: "", skills: [] };
      }
      newSkills[categoryIndex].skills[skillIndex] = value;
      onFieldChange("skills", newSkills);
    },
    [formValues.skills, onFieldChange]
  );

  const handleSkillCategoryChange = React.useCallback(
    (categoryIndex, value) => {
      const newSkills = [...(formValues.skills || [])];
      if (!newSkills[categoryIndex]) {
        newSkills[categoryIndex] = { category: "", skills: [] };
      }
      newSkills[categoryIndex].category = value;
      onFieldChange("skills", newSkills);
    },
    [formValues.skills, onFieldChange]
  );

  const addSkillCategory = React.useCallback(() => {
    const newSkills = [...(formValues.skills || [])];
    newSkills.push({ category: "", skills: [""] });
    onFieldChange("skills", newSkills);
  }, [formValues.skills, onFieldChange]);

  const removeSkillCategory = React.useCallback(
    (categoryIndex) => {
      const newSkills = [...(formValues.skills || [])];
      newSkills.splice(categoryIndex, 1);
      onFieldChange("skills", newSkills);
    },
    [formValues.skills, onFieldChange]
  );

  if (isLoading) {
    return (
      <Box
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          width: "100%",
          m: 1,
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1, width: "100%" }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error.message}
        </Alert>
      )}

      <form onSubmit={handleFormSubmit}>
        <Grid container spacing={2} sx={{ width: "100%" }}>
          {/* Basic Information */}
          <Grid size={{ xs: 12 }}>
            <Paper sx={{ px: 2, py: 2 }}>
              <Typography variant="h6" gutterBottom>
                Basic Information
              </Typography>
              <Grid container spacing={2}>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <TextField
                    label="Full Name"
                    value={formValues.name || ""}
                    onChange={(event) =>
                      onFieldChange("name", event.target.value)
                    }
                    error={!!formErrors.name}
                    helperText={formErrors.name}
                    fullWidth
                    required
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <TextField
                    label="Years of Experience"
                    type="number"
                    value={formValues.yearsOfExperience || ""}
                    onChange={(event) =>
                      onFieldChange(
                        "yearsOfExperience",
                        parseInt(event.target.value) || 0
                      )
                    }
                    error={!!formErrors.yearsOfExperience}
                    helperText={formErrors.yearsOfExperience}
                    fullWidth
                  />
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          {/* Contact Information */}
          <Grid size={{ xs: 12 }}>
            <Paper sx={{ px: 2, py: 2 }}>
              <Typography variant="h6" gutterBottom>
                Contact Information
              </Typography>
              <Grid container spacing={2}>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <TextField
                    label="Email"
                    type="email"
                    value={formValues.email || ""}
                    onChange={(event) =>
                      onFieldChange("email", event.target.value)
                    }
                    error={!!formErrors.email}
                    helperText={formErrors.email}
                    fullWidth
                    required
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <TextField
                    label="Phone"
                    value={formValues.phone || ""}
                    onChange={(event) =>
                      onFieldChange("phone", event.target.value)
                    }
                    error={!!formErrors.phone}
                    helperText={formErrors.phone}
                    fullWidth
                  />
                </Grid>
                <Grid size={{ xs: 12 }}>
                  <TextField
                    label="Address"
                    value={formValues.address || ""}
                    onChange={(event) =>
                      onFieldChange("address", event.target.value)
                    }
                    error={!!formErrors.address}
                    helperText={formErrors.address}
                    fullWidth
                  />
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          {/* Current Position */}
          <Grid size={{ xs: 12 }}>
            <Paper sx={{ px: 2, py: 2 }}>
              <Typography variant="h6" gutterBottom>
                Current Position
              </Typography>
              <Grid container spacing={2}>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <TextField
                    label="Current Position"
                    value={formValues.currentPosition || ""}
                    onChange={(event) =>
                      onFieldChange("currentPosition", event.target.value)
                    }
                    error={!!formErrors.currentPosition}
                    helperText={formErrors.currentPosition}
                    fullWidth
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <TextField
                    label="Current Company"
                    value={formValues.currentCompany || ""}
                    onChange={(event) =>
                      onFieldChange("currentCompany", event.target.value)
                    }
                    error={!!formErrors.currentCompany}
                    helperText={formErrors.currentCompany}
                    fullWidth
                  />
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          {/* Profile Links */}
          <Grid size={{ xs: 12 }}>
            <Paper sx={{ px: 2, py: 2 }}>
              <Typography variant="h6" gutterBottom>
                Profile Links
              </Typography>
              <Grid container spacing={2}>
                <Grid size={{ xs: 12, sm: 4 }}>
                  <TextField
                    label="LinkedIn URL"
                    value={formValues.linkedin || ""}
                    onChange={(event) =>
                      onFieldChange("linkedin", event.target.value)
                    }
                    error={!!formErrors.linkedin}
                    helperText={formErrors.linkedin}
                    fullWidth
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 4 }}>
                  <TextField
                    label="GitHub URL"
                    value={formValues.github || ""}
                    onChange={(event) =>
                      onFieldChange("github", event.target.value)
                    }
                    error={!!formErrors.github}
                    helperText={formErrors.github}
                    fullWidth
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 4 }}>
                  <TextField
                    label="Website URL"
                    value={formValues.website || ""}
                    onChange={(event) =>
                      onFieldChange("website", event.target.value)
                    }
                    error={!!formErrors.website}
                    helperText={formErrors.website}
                    fullWidth
                  />
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          {/* Summary */}
          <Grid size={{ xs: 12 }}>
            <Paper sx={{ px: 2, py: 2 }}>
              <Typography variant="h6" gutterBottom>
                Summary
              </Typography>
              <TextField
                label="Professional Summary"
                value={formValues.summary || ""}
                onChange={(event) =>
                  onFieldChange("summary", event.target.value)
                }
                error={!!formErrors.summary}
                helperText={formErrors.summary}
                fullWidth
                multiline
                rows={4}
              />
            </Paper>
          </Grid>

          {/* Skills */}
          <Grid size={{ xs: 12 }}>
            <Paper sx={{ px: 2, py: 2 }}>
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  mb: 2,
                }}
              >
                <Typography variant="h6">Skills</Typography>
                <Button
                  startIcon={<AddIcon />}
                  onClick={addSkillCategory}
                  size="small"
                >
                  Add Category
                </Button>
              </Box>

              {(formValues.skills || []).map((skillCategory, categoryIndex) => (
                <Box
                  key={categoryIndex}
                  sx={{
                    mb: 2,
                    border: "1px solid #e0e0e0",
                    borderRadius: 1,
                    p: 2,
                  }}
                >
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      mb: 1,
                    }}
                  >
                    <TextField
                      label="Category"
                      value={skillCategory.category || ""}
                      onChange={(event) =>
                        handleSkillCategoryChange(
                          categoryIndex,
                          event.target.value
                        )
                      }
                      size="small"
                      sx={{ flexGrow: 1, mr: 1 }}
                    />
                    <IconButton
                      onClick={() => removeSkillCategory(categoryIndex)}
                      size="small"
                      color="error"
                    >
                      <RemoveIcon />
                    </IconButton>
                  </Box>

                  {(skillCategory.skills || []).map((skill, skillIndex) => (
                    <Box
                      key={skillIndex}
                      sx={{ display: "flex", alignItems: "center", mb: 1 }}
                    >
                      <TextField
                        label="Skill"
                        value={skill}
                        onChange={(event) =>
                          handleSkillChange(
                            categoryIndex,
                            skillIndex,
                            event.target.value
                          )
                        }
                        size="small"
                        sx={{ flexGrow: 1, mr: 1 }}
                      />
                      <IconButton
                        onClick={() =>
                          handleSkillRemove(categoryIndex, skillIndex)
                        }
                        size="small"
                        color="error"
                      >
                        <RemoveIcon />
                      </IconButton>
                    </Box>
                  ))}

                  <Button
                    startIcon={<AddIcon />}
                    onClick={() => handleSkillAdd(categoryIndex)}
                    size="small"
                    variant="outlined"
                  >
                    Add Skill
                  </Button>
                </Box>
              ))}
            </Paper>
          </Grid>
        </Grid>

        <Divider sx={{ my: 3 }} />

        <Stack direction="row" spacing={2} justifyContent="space-between">
          <Button
            variant="outlined"
            startIcon={<ArrowBackIcon />}
            onClick={handleBack}
          >
            Back
          </Button>
          <Stack direction="row" spacing={2}>
            <Button
              variant="outlined"
              startIcon={<RestartAltIcon />}
              onClick={onReset}
            >
              Reset
            </Button>
            <Button type="submit" variant="contained" startIcon={<SaveIcon />}>
              {submitButtonLabel}
            </Button>
          </Stack>
        </Stack>
      </form>
    </Box>
  );
}

CandidateForm.propTypes = {
  formState: PropTypes.shape({
    values: PropTypes.object.isRequired,
    errors: PropTypes.object.isRequired,
  }).isRequired,
  onFieldChange: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  onReset: PropTypes.func.isRequired,
  submitButtonLabel: PropTypes.string,
  isLoading: PropTypes.bool,
  error: PropTypes.object,
};

export default CandidateForm;
