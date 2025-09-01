import * as React from "react";
import { useNavigate, useParams } from "react-router";
import useNotifications from "../hooks/useNotifications/useNotifications";
import {
  getOne as getCandidate,
  updateOne as updateCandidate,
  validate as validateCandidate,
} from "../../data/candidates";
import CandidateForm from "./CandidateForm";
import PageContainer from "./PageContainer";

export default function CandidateEdit() {
  const { candidateId } = useParams();
  const navigate = useNavigate();
  const notifications = useNotifications();

  const [formState, setFormState] = React.useState(() => ({
    values: {},
    errors: {},
  }));
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  const formValues = formState.values;
  const formErrors = formState.errors;

  const setFormValues = React.useCallback((newFormValues) => {
    setFormState((previousState) => ({
      ...previousState,
      values: newFormValues,
    }));
  }, []);

  const setFormErrors = React.useCallback((newFormErrors) => {
    setFormState((previousState) => ({
      ...previousState,
      errors: newFormErrors,
    }));
  }, []);

  const loadData = React.useCallback(async () => {
    setError(null);
    setIsLoading(true);

    try {
      const editData = await getCandidate(Number(candidateId));
      setFormValues(editData);
    } catch (editDataError) {
      setError(editDataError);
    }
    setIsLoading(false);
  }, [candidateId, setFormValues]);

  React.useEffect(() => {
    loadData();
  }, [loadData]);

  const handleFormFieldChange = React.useCallback(
    (name, value) => {
      const validateField = async (values) => {
        const { issues } = validateCandidate(values);
        setFormErrors({
          ...formErrors,
          [name]: issues?.find((issue) => issue.path?.[0] === name)?.message,
        });
      };

      const newFormValues = { ...formValues, [name]: value };
      setFormValues(newFormValues);
      validateField(newFormValues);
    },
    [formValues, formErrors, setFormErrors, setFormValues]
  );

  const handleFormReset = React.useCallback(() => {
    loadData();
  }, [loadData]);

  const handleFormSubmit = React.useCallback(async () => {
    const { issues } = validateCandidate(formValues);
    if (issues && issues.length > 0) {
      setFormErrors(
        Object.fromEntries(
          issues.map((issue) => [issue.path?.[0], issue.message])
        )
      );
      return;
    }
    setFormErrors({});

    try {
      await updateCandidate(Number(candidateId), formValues);
      notifications.show("Candidate updated successfully.", {
        severity: "success",
        autoHideDuration: 3000,
      });
      navigate(`/candidates/${candidateId}`);
    } catch (updateError) {
      notifications.show(
        `Failed to update candidate. Reason: ${updateError.message}`,
        {
          severity: "error",
          autoHideDuration: 3000,
        }
      );
      throw updateError;
    }
  }, [candidateId, formValues, navigate, notifications, setFormErrors]);

  const pageTitle = `Edit Candidate ${candidateId}`;

  return (
    <PageContainer
      title={pageTitle}
      breadcrumbs={[
        { title: "Candidates", path: "/candidates" },
        {
          title: `Candidate ${candidateId}`,
          path: `/candidates/${candidateId}`,
        },
        { title: "Edit" },
      ]}
    >
      <CandidateForm
        formState={formState}
        onFieldChange={handleFormFieldChange}
        onSubmit={handleFormSubmit}
        onReset={handleFormReset}
        submitButtonLabel="Update"
        isLoading={isLoading}
        error={error}
      />
    </PageContainer>
  );
}
