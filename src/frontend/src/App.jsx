import * as React from "react";
import CssBaseline from "@mui/material/CssBaseline";
import { createHashRouter, RouterProvider } from "react-router";
import DashboardLayout from "./components/DashboardLayout";
import CandidateList from "./components/CandidateList";
import JobList from "./components/JobList";
import JobCandidateMatching from "./components/JobCandidateMatching";
import CandidateShow from "./components/CandidateShow";
import CandidateCreate from "./components/CandidateCreate";
import CandidateEdit from "./components/CandidateEdit";
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
        Component: CandidateShow,
      },
      {
        path: "/candidates/new",
        Component: CandidateCreate,
      },
      {
        path: "/candidates/:candidateId/edit",
        Component: CandidateEdit,
      },
      // Job routes
      {
        path: "/jobs",
        Component: JobList,
      },
      // Job-Candidate Matching route
      {
        path: "/matching",
        Component: JobCandidateMatching,
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
