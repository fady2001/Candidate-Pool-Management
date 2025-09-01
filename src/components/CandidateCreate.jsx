import * as React from "react";
import { useNavigate } from "react-router";
import useNotifications from "../hooks/useNotifications/useNotifications";
import {
  createOne as createCandidate,
  validate as validateCandidate,
} from "../../data/candidates";
import CandidateForm from "./CandidateForm";
import PageContainer from "./PageContainer";

const INITIAL_FORM_VALUES = {
  name: "",
  email: "",
  phone: "",
  address: "",
  linkedin: "",
  github: "",
  website: "",
  summary: "",
  currentPosition: "",
  currentCompany: "",
  yearsOfExperience: 0,
  skills: [],
};

export default function CandidateCreate() {
  const navigate = useNavigate();
  const notifications = useNotifications();

  const [formState, setFormState] = React.useState(() => ({
    values: INITIAL_FORM_VALUES,
    errors: {},
  }));
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
    setFormValues(INITIAL_FORM_VALUES);
  }, [setFormValues]);

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
      await createCandidate(formValues);
      notifications.show("Candidate created successfully.", {
        severity: "success",
        autoHideDuration: 3000,
      });
      navigate("/candidates");
    } catch (createError) {
      notifications.show(
        `Failed to create candidate. Reason: ${createError.message}`,
        {
          severity: "error",
          autoHideDuration: 3000,
        }
      );
      throw createError;
    }
  }, [formValues, navigate, notifications, setFormErrors]);

  return (
    <PageContainer
      title="New Candidate"
      breadcrumbs={[
        { title: "Candidates", path: "/candidates" },
        { title: "New" },
      ]}
    >
      <CandidateForm
        formState={formState}
        onFieldChange={handleFormFieldChange}
        onSubmit={handleFormSubmit}
        onReset={handleFormReset}
        submitButtonLabel="Create"
      />
    </PageContainer>
  );
}
