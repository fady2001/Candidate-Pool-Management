import * as React from "react";
import CssBaseline from "@mui/material/CssBaseline";
import { createHashRouter, RouterProvider } from "react-router";
import DashboardLayout from "./components/DashboardLayout";
import CandidateList from "./components/CandidateList";
import JobList from "./components/JobList";
import JobCandidateMatching from "./components/JobCandidateMatching";
import EmployeeShow from "./components/EmployeeShow";
import EmployeeCreate from "./components/EmployeeCreate";
import EmployeeEdit from "./components/EmployeeEdit";
import NotificationsProvider from "./hooks/useNotifications/NotificationsProvider";
import DialogsProvider from "./hooks/useDialogs/DialogsProvider";
import AppTheme from "./theme/AppTheme";
import {
  dataGridCustomizations,
  datePickersCustomizations,
  sidebarCustomizations,
  formInputCustomizations,
} from "./theme/customizations";

const router = createHashRouter([
  {
    Component: DashboardLayout,
    children: [
      {
        path: "/candidates",
        Component: CandidateList,
      },
      {
        path: "/candidates/:candidateId",
        Component: EmployeeShow, // TODO: Update to CandidateShow
      },
      {
        path: "/candidates/new",
        Component: EmployeeCreate, // TODO: Update to CandidateCreate
      },
      {
        path: "/candidates/:candidateId/edit",
        Component: EmployeeEdit, // TODO: Update to CandidateEdit
      },
      // Job routes
      {
        path: "/jobs",
        Component: JobList,
      },
      {
        path: "/jobs/:jobId",
        Component: EmployeeShow, // TODO: Create JobShow component
      },
      {
        path: "/jobs/new",
        Component: EmployeeCreate, // TODO: Create JobCreate component
      },
      {
        path: "/jobs/:jobId/edit",
        Component: EmployeeEdit, // TODO: Create JobEdit component
      },
      // Job-Candidate Matching route
      {
        path: "/matching",
        Component: JobCandidateMatching,
      },
      // Keep old employee routes for backward compatibility
      {
        path: "/employees",
        Component: CandidateList,
      },
      {
        path: "/employees/:employeeId",
        Component: EmployeeShow,
      },
      {
        path: "/employees/new",
        Component: EmployeeCreate,
      },
      {
        path: "/employees/:employeeId/edit",
        Component: EmployeeEdit,
      },
      // Fallback route
      {
        path: "*",
        Component: CandidateList,
      },
    ],
  },
]);

const themeComponents = {
  ...dataGridCustomizations,
  ...datePickersCustomizations,
  ...sidebarCustomizations,
  ...formInputCustomizations,
};

export default function CrudDashboard(props) {
  return (
    <AppTheme {...props} themeComponents={themeComponents}>
      <CssBaseline enableColorScheme />
      <NotificationsProvider>
        <DialogsProvider>
          <RouterProvider router={router} />
        </DialogsProvider>
      </NotificationsProvider>
    </AppTheme>
  );
}
