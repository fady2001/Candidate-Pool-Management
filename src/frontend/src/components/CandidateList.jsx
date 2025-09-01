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
import PersonIcon from "@mui/icons-material/Person";
import WorkIcon from "@mui/icons-material/Work";
import EmailIcon from "@mui/icons-material/Email";
import PhoneIcon from "@mui/icons-material/Phone";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import GitHubIcon from "@mui/icons-material/GitHub";
import LanguageIcon from "@mui/icons-material/Language";
import { useLocation, useNavigate, useSearchParams } from "react-router";
import { useDialogs } from "../hooks/useDialogs/useDialogs";
import useNotifications from "../hooks/useNotifications/useNotifications";
import {
  deleteOne as deleteCandidate,
  getMany as getCandidates,
} from "../../data/candidates";
import PageContainer from "./PageContainer";

const INITIAL_PAGE_SIZE = 10;

export default function CandidateList() {
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
      const listData = await getCandidates({
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
      navigate(`/candidates/${row.id}`);
    },
    [navigate]
  );

  const handleCreateClick = React.useCallback(() => {
    navigate("/candidates/new");
  }, [navigate]);

  const handleRowEdit = React.useCallback(
    (candidate) => () => {
      navigate(`/candidates/${candidate.id}/edit`);
    },
    [navigate]
  );

  const handleRowDelete = React.useCallback(
    (candidate) => async () => {
      const confirmed = await dialogs.confirm(
        `Do you wish to delete ${candidate.name}?`,
        {
          title: `Delete candidate?`,
          severity: "error",
          okText: "Delete",
          cancelText: "Cancel",
        }
      );

      if (confirmed) {
        setIsLoading(true);
        try {
          await deleteCandidate(Number(candidate.id));

          notifications.show("Candidate deleted successfully.", {
            severity: "success",
            autoHideDuration: 3000,
          });
          loadData();
        } catch (deleteError) {
          notifications.show(
            `Failed to delete candidate. Reason: ${deleteError.message}`,
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

  const renderProfileLinks = React.useCallback((params) => {
    const { linkedin, github, website } = params.row;
    const links = [];

    if (linkedin) {
      links.push(
        <Tooltip key="linkedin" title="LinkedIn Profile">
          <IconButton
            size="small"
            component={Link}
            href={linkedin}
            target="_blank"
            rel="noopener noreferrer"
            sx={{ color: "#0077B5" }}
          >
            <LinkedInIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      );
    }

    if (github) {
      links.push(
        <Tooltip key="github" title="GitHub Profile">
          <IconButton
            size="small"
            component={Link}
            href={github}
            target="_blank"
            rel="noopener noreferrer"
            sx={{ color: "#333" }}
          >
            <GitHubIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      );
    }

    if (website) {
      links.push(
        <Tooltip key="website" title="Website">
          <IconButton
            size="small"
            component={Link}
            href={website}
            target="_blank"
            rel="noopener noreferrer"
            sx={{ color: "#1976d2" }}
          >
            <LanguageIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      );
    }

    return <Box sx={{ display: "flex", gap: 0.5 }}>{links}</Box>;
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
        field: "name",
        headerName: "Name",
        width: 180,
        renderCell: (params) => (
          <Box sx={{ display: "flex", alignItems: "start", gap: 1 }}>
            <PersonIcon fontSize="small" color="action" sx={{marginTop:'15px'}}/>
            <Box>
              <Box sx={{ fontWeight: "medium" }}>{params.value}</Box>
              {params.row.email && (
                <Box sx={{ fontSize: "0.75rem", color: "text.secondary" }}>
                  {params.row.email}
                </Box>
              )}
            </Box>
          </Box>
        ),
      },
      {
        field: "currentPosition",
        headerName: "Current Position",
        width: 200,
        renderCell: (params) => (
          <Box>
            <Box sx={{ fontWeight: "medium" }}>{params.value}</Box>
            {params.row.currentCompany &&
              params.row.currentCompany !== "N/A" && (
                <Box sx={{ fontSize: "0.75rem", color: "text.secondary" }}>
                  {params.row.currentCompany}
                </Box>
              )}
          </Box>
        ),
      },
      {
        field: "yearsOfExperience",
        headerName: "Experience",
        type: "number",
        width: 120,
        renderCell: (params) => (
          <Chip
            label={`${params.value} years`}
            variant="outlined"
            size="small"
            color={
              params.value >= 5
                ? "primary"
                : params.value >= 2
                ? "secondary"
                : "default"
            }
          />
        ),
      },
      {
        field: "location",
        headerName: "Location",
        width: 150,
      },
      {
        field: "skills",
        headerName: "Skills",
        width: 250,
        renderCell: (params) => (
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
        ),
      },
      {
        field: "profileLinks",
        headerName: "Profiles",
        width: 120,
        sortable: false,
        filterable: false,
        renderCell: renderProfileLinks,
      },
      {
        field: "createdAt",
        headerName: "Added",
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
    [handleRowEdit, handleRowDelete, renderProfileLinks]
  );

  const pageTitle = "Candidates";

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
            Add Candidate
          </Button>
        </Stack>
      }
    >
      <Box sx={{ flex: 1, width: "100%" }}>
        {error ? (
          <Box sx={{ flexGrow: 1 }}>
            <Alert severity="error">
              Failed to load candidates: {error.message}
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
              // Custom styling for better candidate display
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
