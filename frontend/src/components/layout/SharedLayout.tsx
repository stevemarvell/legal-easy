import React from 'react';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  TextField,
  InputAdornment,
  Breadcrumbs,
  Link,
  Button
} from '@mui/material';
import {
  Search as SearchIcon,
  Home as HomeIcon,
  Folder as CaseIcon,
  Description as DocumentIcon,
  MenuBook as PlaybookIcon,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';

interface SharedLayoutProps {
  title: string;
  subtitle?: string;
  showSearchBar?: boolean;
  searchPlaceholder?: string;
  searchValue?: string;
  onSearchChange?: (value: string) => void;
  breadcrumbs?: Array<{
    label: string;
    path?: string;
    icon?: React.ReactNode;
  }>;
  showBackButton?: boolean;
  backButtonLabel?: string;
  onBackClick?: () => void;
  children: React.ReactNode;
}

const SharedLayout: React.FC<SharedLayoutProps> = ({
  title,
  subtitle,
  showSearchBar = false,
  searchPlaceholder = "Search...",
  searchValue = "",
  onSearchChange,
  breadcrumbs = [],
  showBackButton = false,
  backButtonLabel = "Back",
  onBackClick,
  children
}) => {
  const location = useLocation();
  const navigate = useNavigate();

  const handleBreadcrumbNavigation = (path: string) => {
    navigate(path);
  };

  const handleBackClick = () => {
    if (onBackClick) {
      onBackClick();
    } else {
      navigate(-1);
    }
  };

  // Generate default breadcrumbs based on current path if none provided
  const getDefaultBreadcrumbs = (): Array<{
    label: string;
    path?: string;
    icon?: React.ReactNode;
  }> => {
    const pathSegments = location.pathname.split('/').filter(Boolean);
    const defaultBreadcrumbs: Array<{
      label: string;
      path?: string;
      icon?: React.ReactNode;
    }> = [
      {
        label: 'Dashboard',
        path: '/',
        icon: <HomeIcon sx={{ mr: 0.5 }} fontSize="inherit" />
      }
    ];

    if (pathSegments.length > 0) {
      const firstSegment = pathSegments[0];
      let icon;
      let label;

      switch (firstSegment) {
        case 'cases':
          icon = <CaseIcon sx={{ mr: 0.5 }} fontSize="inherit" />;
          label = 'Cases';
          break;
        case 'documents':
          icon = <DocumentIcon sx={{ mr: 0.5 }} fontSize="inherit" />;
          label = 'Documents';
          break;
        case 'playbooks':
          icon = <PlaybookIcon sx={{ mr: 0.5 }} fontSize="inherit" />;
          label = 'Playbooks';
          break;
        default:
          label = firstSegment.charAt(0).toUpperCase() + firstSegment.slice(1);
          icon = undefined;
      }

      defaultBreadcrumbs.push({
        label,
        path: `/${firstSegment}`,
        icon
      });

      // Add additional segments if they exist
      if (pathSegments.length > 1) {
        for (let i = 1; i < pathSegments.length; i++) {
          const segment = pathSegments[i];
          const path = '/' + pathSegments.slice(0, i + 1).join('/');
          defaultBreadcrumbs.push({
            label: segment.charAt(0).toUpperCase() + segment.slice(1),
            path
          });
        }
      }
    }

    return defaultBreadcrumbs;
  };

  const finalBreadcrumbs = breadcrumbs.length > 0 ? breadcrumbs : getDefaultBreadcrumbs();

  return (
    <Container maxWidth="xl">
      <Box>
        {/* Header Section */}
        <Box mb={4}>
          {/* Back Button */}
          {showBackButton && (
            <Button
              variant="outlined"
              startIcon={<ArrowBackIcon />}
              onClick={handleBackClick}
              sx={{ mb: 2 }}
              data-testid="back-button"
            >
              {backButtonLabel}
            </Button>
          )}

          {/* Breadcrumbs */}
          {finalBreadcrumbs.length > 1 && (
            <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
              {finalBreadcrumbs.map((breadcrumb, index) => {
                const isLast = index === finalBreadcrumbs.length - 1;
                
                if (isLast) {
                  return (
                    <Typography key={index} color="text.primary" variant="body2">
                      {breadcrumb.label}
                    </Typography>
                  );
                }

                return (
                  <Link
                    key={index}
                    component="button"
                    variant="body2"
                    onClick={() => breadcrumb.path && handleBreadcrumbNavigation(breadcrumb.path)}
                    sx={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      textDecoration: 'none',
                      color: 'text.secondary',
                      '&:hover': {
                        color: 'primary.main'
                      }
                    }}
                  >
                    {breadcrumb.icon && breadcrumb.icon}
                    {breadcrumb.label}
                  </Link>
                );
              })}
            </Breadcrumbs>
          )}

          {/* Title and Subtitle */}
          <Typography variant="h3" component="h1" color="primary" gutterBottom data-testid="page-title">
            {title}
          </Typography>
          {subtitle && (
            <Typography variant="h6" color="text.secondary" gutterBottom data-testid="page-subtitle">
              {subtitle}
            </Typography>
          )}

          {/* Search Bar */}
          {showSearchBar && (
            <TextField
              fullWidth
              variant="outlined"
              placeholder={searchPlaceholder}
              value={searchValue}
              onChange={(e) => onSearchChange?.(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="primary" />
                  </InputAdornment>
                ),
              }}
              sx={{ mt: 2 }}
              data-testid="search-input"
            />
          )}
        </Box>

        {/* Main Content */}
        <Box>
          {children}
        </Box>
      </Box>
    </Container>
  );
};

export default SharedLayout;