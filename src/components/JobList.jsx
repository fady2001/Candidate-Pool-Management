import * as React from "react";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";
import Tooltip from "@mui/material/Tooltip";
import Chip from "@mui/material/Chip";
import Link from "@mui/material/Link";
import { DataGrid, GridActionsCellItem, gridClasses } from "@mui/x-data-grid";
import AddIcon from "@mui/icons-material/Add";
import RefreshIcon from "@mui/icons-material/Refresh";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import WorkIcon from "@mui/icons-material/Work";
import BusinessIcon from "@mui/icons-material/Business";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import { useLocation, useNavigate, useSearchParams } from "react-router";
import { useDialogs } from "../hooks/useDialogs/useDialogs";
import useNotifications from "../hooks/useNotifications/useNotifications";
import { deleteOne as deleteJob, getMany as getJobs } from "../../data/jobs";
import PageContainer from "./PageContainer";

const INITIAL_PAGE_SIZE = 10;

export default function JobList() {
  const { pathname } = useLocation();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const dialogs = useDialogs();
  const notifications = useNotifications();

  const [paginationModel, setPaginationModel] = React.useState({
    page: searchParams.get("page") ? Number(searchParams.get("page")) : 0,
    pageSize: searchParams.get("pageSize")
      ? Number(searchParams.get("pageSize"))
      : INITIAL_PAGE_SIZE,
  });
  const [filterModel, setFilterModel] = React.useState(
    searchParams.get("filter")
      ? JSON.parse(searchParams.get("filter") ?? "")
      : { items: [] }
  );
  const [sortModel, setSortModel] = React.useState(
    searchParams.get("sort") ? JSON.parse(searchParams.get("sort") ?? "") : []
  );

  const [rowsState, setRowsState] = React.useState({
    rows: [],
    rowCount: 0,
  });

  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  const handlePaginationModelChange = React.useCallback(
    (model) => {
      setPaginationModel(model);

      searchParams.set("page", String(model.page));
      searchParams.set("pageSize", String(model.pageSize));

      const newSearchParamsString = searchParams.toString();

      navigate(
        `${pathname}${newSearchParamsString ? "?" : ""}${newSearchParamsString}`
      );
    },
    [navigate, pathname, searchParams]
  );

  const handleFilterModelChange = React.useCallback(
    (model) => {
      setFilterModel(model);

      if (
        model.items.length > 0 ||
        (model.quickFilterValues && model.quickFilterValues.length > 0)
      ) {
        searchParams.set("filter", JSON.stringify(model));
      } else {
        searchParams.delete("filter");
      }

      const newSearchParamsString = searchParams.toString();

      navigate(
        `${pathname}${newSearchParamsString ? "?" : ""}${newSearchParamsString}`
      );
    },
    [navigate, pathname, searchParams]
  );

  const handleSortModelChange = React.useCallback(
    (model) => {
      setSortModel(model);

      if (model.length > 0) {
        searchParams.set("sort", JSON.stringify(model));
      } else {
        searchParams.delete("sort");
      }

      const newSearchParamsString = searchParams.toString();

      navigate(
        `${pathname}${newSearchParamsString ? "?" : ""}${newSearchParamsString}`
      );
    },
    [navigate, pathname, searchParams]
  );

  const loadData = React.useCallback(async () => {
    setError(null);
    setIsLoading(true);

    try {
      const listData = await getJobs({
        paginationModel,
        sortModel,
        filterModel,
      });

      setRowsState({
        rows: listData.items,
        rowCount: listData.itemCount,
      });
    } catch (listDataError) {
      setError(listDataError);
    }

    setIsLoading(false);
  }, [paginationModel, sortModel, filterModel]);

  React.useEffect(() => {
    loadData();
  }, [loadData]);

  const handleRefresh = React.useCallback(() => {
    if (!isLoading) {
      loadData();
    }
  }, [isLoading, loadData]);

  const handleRowClick = React.useCallback(
    ({ row }) => {
      navigate(`/jobs/${row.id}`);
    },
    [navigate]
  );

  const handleCreateClick = React.useCallback(() => {
    navigate("/jobs/new");
  }, [navigate]);

  const handleRowEdit = React.useCallback(
    (job) => () => {
      navigate(`/jobs/${job.id}/edit`);
    },
    [navigate]
  );

  const handleRowDelete = React.useCallback(
    (job) => async () => {
      const confirmed = await dialogs.confirm(
        `Do you wish to delete ${job.jobTitle}?`,
        {
          title: `Delete job?`,
          severity: "error",
          okText: "Delete",
          cancelText: "Cancel",
        }
      );

      if (confirmed) {
        setIsLoading(true);
        try {
          await deleteJob(Number(job.id));

          notifications.show("Job deleted successfully.", {
            severity: "success",
            autoHideDuration: 3000,
          });
          loadData();
        } catch (deleteError) {
          notifications.show(
            `Failed to delete job. Reason: ${deleteError.message}`,
            {
              severity: "error",
              autoHideDuration: 3000,
            }
          );
        }
        setIsLoading(false);
      }
    },
    [dialogs, notifications, loadData]
  );

  const renderExperienceRange = React.useCallback((params) => {
    const { minExperience, maxExperience } = params.row;
    if (minExperience === 0 && maxExperience === 0) {
      return "Not specified";
    }
    if (minExperience === maxExperience) {
      return `${minExperience} years`;
    }
    return `${minExperience}-${maxExperience} years`;
  }, []);

  const renderJobInfo = React.useCallback((params) => {
    const { jobTitle, company, department } = params.row;
    return (
      <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
        <WorkIcon fontSize="small" color="action" />
        <Box>
          <Box sx={{ fontWeight: "medium" }}>{jobTitle}</Box>
          <Box sx={{ fontSize: "0.75rem", color: "text.secondary" }}>
            {company} {department && department !== "N/A" && `• ${department}`}
          </Box>
        </Box>
      </Box>
    );
  }, []);

  const initialState = React.useMemo(
    () => ({
      pagination: { paginationModel: { pageSize: INITIAL_PAGE_SIZE } },
    }),
    []
  );

  const columns = React.useMemo(
    () => [
      {
        field: "id",
        headerName: "ID",
        width: 70,
        type: "number",
      },
      {
        field: "jobTitle",
        headerName: "Job",
        width: 250,
        renderCell: renderJobInfo,
      },
      {
        field: "location",
        headerName: "Location",
        width: 150,
        renderCell: (params) => (
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <LocationOnIcon fontSize="small" color="action" />
            {params.value}
          </Box>
        ),
      },
      {
        field: "employmentType",
        headerName: "Type",
        width: 120,
        renderCell: (params) => (
          <Chip
            label={params.value}
            variant="outlined"
            size="small"
            color={
              params.value === "Full-time"
                ? "primary"
                : params.value === "Contract"
                ? "secondary"
                : "default"
            }
          />
        ),
      },
      {
        field: "workArrangement",
        headerName: "Work Style",
        width: 120,
        renderCell: (params) => (
          <Chip
            label={params.value}
            variant="outlined"
            size="small"
            color={
              params.value === "Remote"
                ? "success"
                : params.value === "Hybrid"
                ? "info"
                : "default"
            }
          />
        ),
      },
      {
        field: "experienceLevel",
        headerName: "Level",
        width: 120,
        renderCell: (params) => (
          <Chip
            label={params.value}
            variant="outlined"
            size="small"
            color={
              params.value === "Senior"
                ? "primary"
                : params.value === "Mid-level"
                ? "secondary"
                : "default"
            }
          />
        ),
      },
      {
        field: "experience",
        headerName: "Experience",
        width: 120,
        renderCell: renderExperienceRange,
      },
      {
        field: "salaryInfo",
        headerName: "Salary",
        width: 150,
        renderCell: (params) => (
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            {params.value !== "N/A" && (
              <AttachMoneyIcon fontSize="small" color="action" />
            )}
            <Tooltip title={params.value} placement="top">
              <Box
                sx={{
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                  fontSize: "0.875rem",
                }}
              >
                {params.value}
              </Box>
            </Tooltip>
          </Box>
        ),
      },
      {
        field: "urgencyLevel",
        headerName: "Urgency",
        width: 100,
        renderCell: (params) => (
          <Chip
            label={params.value}
            variant="outlined"
            size="small"
            color={
              params.value === "Urgent"
                ? "error"
                : params.value === "High"
                ? "warning"
                : "default"
            }
          />
        ),
      },
      {
        field: "postedDate",
        headerName: "Posted",
        type: "dateTime",
        valueGetter: (value) => value && new Date(value),
        width: 120,
      },
      {
        field: "actions",
        type: "actions",
        flex: 1,
        align: "right",
        getActions: ({ row }) => [
          <GridActionsCellItem
            key="edit-item"
            icon={<EditIcon />}
            label="Edit"
            onClick={handleRowEdit(row)}
          />,
          <GridActionsCellItem
            key="delete-item"
            icon={<DeleteIcon />}
            label="Delete"
            onClick={handleRowDelete(row)}
          />,
        ],
      },
    ],
    [handleRowEdit, handleRowDelete, renderJobInfo, renderExperienceRange]
  );

  const pageTitle = "Job Descriptions";

  return (
    <PageContainer
      title={pageTitle}
      breadcrumbs={[{ title: pageTitle }]}
      actions={
        <Stack direction="row" alignItems="center" spacing={1}>
          <Tooltip title="Reload data" placement="right" enterDelay={1000}>
            <div>
              <IconButton
                size="small"
                aria-label="refresh"
                onClick={handleRefresh}
              >
                <RefreshIcon />
              </IconButton>
            </div>
          </Tooltip>
          <Button
            variant="contained"
            onClick={handleCreateClick}
            startIcon={<AddIcon />}
          >
            Add Job
          </Button>
        </Stack>
      }
    >
      <Box sx={{ flex: 1, width: "100%" }}>
        {error ? (
          <Box sx={{ flexGrow: 1 }}>
            <Alert severity="error">
              Failed to load jobs: {error.message}
              <br />
              <small>
                Make sure the backend API is running on http://localhost:8000
              </small>
            </Alert>
          </Box>
        ) : (
          <DataGrid
            rows={rowsState.rows}
            rowCount={rowsState.rowCount}
            columns={columns}
            pagination
            sortingMode="server"
            filterMode="server"
            paginationMode="server"
            paginationModel={paginationModel}
            onPaginationModelChange={handlePaginationModelChange}
            sortModel={sortModel}
            onSortModelChange={handleSortModelChange}
            filterModel={filterModel}
            onFilterModelChange={handleFilterModelChange}
            disableRowSelectionOnClick
            onRowClick={handleRowClick}
            loading={isLoading}
            initialState={initialState}
            slots={{ toolbar: true }}
            slotProps={{
              toolbar: {
                showQuickFilter: true,
                quickFilterProps: { debounceMs: 500 },
              },
              loadingOverlay: {
                variant: "circular-progress",
                noRowsVariant: "circular-progress",
              },
              baseIconButton: {
                size: "small",
              },
            }}
            pageSizeOptions={[5, INITIAL_PAGE_SIZE, 25, 50]}
            sx={{
              [`& .${gridClasses.columnHeader}, & .${gridClasses.cell}`]: {
                outline: "transparent",
              },
              [`& .${gridClasses.columnHeader}:focus-within, & .${gridClasses.cell}:focus-within`]:
                {
                  outline: "none",
                },
              [`& .${gridClasses.row}:hover`]: {
                cursor: "pointer",
              },
              // Custom styling for better job display
              "& .MuiDataGrid-cell": {
                borderBottom: "1px solid #f0f0f0",
              },
              "& .MuiDataGrid-row": {
                "&:nth-of-type(even)": {
                  backgroundColor: "#fafafa",
                },
              },
            }}
          />
        )}
      </Box>
    </PageContainer>
  );
}
