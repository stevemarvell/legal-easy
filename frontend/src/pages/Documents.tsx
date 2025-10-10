import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Button,
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
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleDocumentSelect = (document: Document) => {
    setSelectedDocument(document);
  };

  const handleDocumentAnalyzed = () => {
    // Trigger refresh of document list to update analysis status
    setRefreshTrigger(prev => prev + 1);
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

        {/* Main Content - Two Column Layout */}
        <Box sx={{ display: 'flex', gap: 3, height: 'calc(100vh - 180px)' }}>
          {/* Left Column - Document List */}
          <Box sx={{ width: '350px', flexShrink: 0 }}>
            <Typography variant="h6" gutterBottom>
              Case Documents
            </Typography>
            <DocumentList
              caseId={caseId}
              onDocumentSelect={handleDocumentSelect}
              selectedDocumentId={selectedDocument?.id}
              refreshTrigger={refreshTrigger}
            />
          </Box>

          {/* Right Column - Document Analysis & Content */}
          <Box sx={{ flex: 1, minWidth: 0 }}>
            {selectedDocument ? (
              <DocumentViewer
                document={selectedDocument}
                onDocumentAnalyzed={handleDocumentAnalyzed}
              />
            ) : (
              <Box 
                sx={{ 
                  height: '100%', 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  flexDirection: 'column',
                  textAlign: 'center',
                  bgcolor: 'grey.50',
                  borderRadius: 1,
                  border: '1px dashed',
                  borderColor: 'grey.300'
                }}
              >
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  Select a document to view
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Choose a document from the list to view its AI analysis and content
                </Typography>
              </Box>
            )}
          </Box>
        </Box>
      </Box>
    </Container>
  );
};

export default Documents;