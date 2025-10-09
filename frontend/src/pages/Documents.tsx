import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Button,
  Grid,
  Typography,
  Breadcrumbs,
  Link
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Home as HomeIcon,
  Folder as CaseIcon
} from '@mui/icons-material';
import DocumentList from '../components/DocumentManagement/DocumentList';
import DocumentViewer from '../components/DocumentManagement/DocumentViewer';
import { Document } from '../types/document';

const Documents: React.FC = () => {
  const { caseId } = useParams<{ caseId: string }>();
  const navigate = useNavigate();
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);

  const handleDocumentSelect = (document: Document) => {
    setSelectedDocument(document);
  };

  const handleBackToCase = () => {
    navigate(`/cases/${caseId}`);
  };

  const handleBreadcrumbNavigation = (path: string) => {
    navigate(path);
  };

  if (!caseId) {
    return (
      <Container maxWidth="xl">
        <Typography variant="h4" color="error">
          Case ID is required
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box>
        {/* Header with Navigation */}
        <Box mb={4}>
          <Button
            variant="outlined"
            startIcon={<ArrowBackIcon />}
            onClick={handleBackToCase}
            sx={{ mb: 2 }}
          >
            Back to Case
          </Button>

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
            <Link
              component="button"
              variant="body2"
              onClick={() => handleBreadcrumbNavigation('/cases')}
              sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
            >
              <CaseIcon sx={{ mr: 0.5 }} fontSize="inherit" />
              Cases
            </Link>
            <Link
              component="button"
              variant="body2"
              onClick={handleBackToCase}
              sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
            >
              Case {caseId}
            </Link>
            <Typography color="text.primary" variant="body2">
              Documents
            </Typography>
          </Breadcrumbs>

          <Typography variant="h3" component="h1" color="primary">
            Document Management
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Case {caseId}
          </Typography>
        </Box>

        {/* Main Content */}
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
          {/* Document List */}
          <Box sx={{ width: { xs: '100%', md: selectedDocument ? '33%' : '100%' } }}>
            <DocumentList
              caseId={caseId}
              onDocumentSelect={handleDocumentSelect}
              selectedDocumentId={selectedDocument?.id}
            />
          </Box>

          {/* Document Viewer */}
          {selectedDocument && (
            <Box sx={{ flex: 1 }}>
              <DocumentViewer
                documentId={selectedDocument.id}
                document={selectedDocument}
              />
            </Box>
          )}
        </Box>

        {/* Empty State */}
        {!selectedDocument && (
          <Box mt={4} textAlign="center">
            <Typography variant="h6" color="text.secondary" gutterBottom>
              Select a document to view details
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Choose a document from the list above to view its contents and analysis results
            </Typography>
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default Documents;