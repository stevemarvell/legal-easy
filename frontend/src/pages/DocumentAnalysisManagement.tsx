import React from 'react';
import {
  Box,
  Container,
  Typography,
  Breadcrumbs,
  Link
} from '@mui/material';
import {
  Home as HomeIcon,
  Psychology as AIIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import DocumentAnalysis from '../components/DocumentManagement/DocumentAnalysis';

const DocumentAnalysisManagement: React.FC = () => {
  const navigate = useNavigate();

  const handleBreadcrumbNavigation = (path: string) => {
    navigate(path);
  };

  return (
    <Container maxWidth="xl">
      <Box>
        {/* Header with Navigation */}
        <Box mb={4}>
          {/* Breadcrumbs */}
          <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
            <Link
              component="button"
              variant="body2"
              onClick={() => handleBreadcrumbNavigation('/')}
              sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
            >
              <HomeIcon sx={{ mr: 0.5 }} fontSize="inherit" />
              Dashboard
            </Link>
            <Typography color="text.primary" variant="body2" sx={{ display: 'flex', alignItems: 'center' }}>
              <AIIcon sx={{ mr: 0.5 }} fontSize="inherit" />
              Document Analysis
            </Typography>
          </Breadcrumbs>

          <Typography variant="h3" component="h1" color="primary">
            AI Document Analysis
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Manage and run AI analysis on all legal documents
          </Typography>
        </Box>

        {/* Document Analysis Management Interface */}
        <DocumentAnalysis showManagementInterface={true} />
      </Box>
    </Container>
  );
};

export default DocumentAnalysisManagement;