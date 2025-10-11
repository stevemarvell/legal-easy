import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Button,
  Typography,
  Breadcrumbs,
  Link,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Home as HomeIcon,
  Folder as CaseIcon,
  Description as DocumentIcon
} from '@mui/icons-material';
import DocumentViewer from '../components/DocumentManagement/DocumentViewer';
import { documentService } from '../services/documentService';
import { Document } from '../types/document';

const DocumentDetail: React.FC = () => {
  const { caseId, documentId } = useParams<{ caseId: string; documentId: string }>();
  const navigate = useNavigate();
  const [document, setDocument] = useState<Document | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDocument = async () => {
      if (!documentId) return;
      
      try {
        setLoading(true);
        setError(null);
        const fetchedDocument = await documentService.getDocumentById(documentId);
        setDocument(fetchedDocument);
      } catch (err) {
        console.error('Failed to fetch document:', err);
        setError('Failed to load document. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchDocument();
  }, [documentId]);

  const handleBackToDocuments = () => {
    if (caseId) {
      navigate(`/cases/${caseId}/documents`);
    } else {
      navigate('/documents');
    }
  };

  const handleBackToCase = () => {
    if (caseId) {
      navigate(`/cases/${caseId}`);
    }
  };

  const handleBreadcrumbNavigation = (path: string) => {
    navigate(path);
  };

  if (loading) {
    return (
      <Container maxWidth="xl">
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="xl">
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
        <Button
          variant="outlined"
          startIcon={<ArrowBackIcon />}
          onClick={handleBackToDocuments}
        >
          Back to Documents
        </Button>
      </Container>
    );
  }

  if (!document) {
    return (
      <Container maxWidth="xl">
        <Alert severity="warning" sx={{ mb: 4 }}>
          Document not found
        </Alert>
        <Button
          variant="outlined"
          startIcon={<ArrowBackIcon />}
          onClick={handleBackToDocuments}
        >
          Back to Documents
        </Button>
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
            onClick={handleBackToDocuments}
            sx={{ mb: 2 }}
          >
            Back to Documents
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
            {caseId && (
              <Link
                component="button"
                variant="body2"
                onClick={handleBackToCase}
                sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
              >
                Case {caseId}
              </Link>
            )}
            <Link
              component="button"
              variant="body2"
              onClick={handleBackToDocuments}
              sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
            >
              Documents
            </Link>
            <Typography color="text.primary" variant="body2" sx={{ display: 'flex', alignItems: 'center' }}>
              <DocumentIcon sx={{ mr: 0.5 }} fontSize="inherit" />
              {document.name}
            </Typography>
          </Breadcrumbs>

          <Typography variant="h3" component="h1" color="primary">
            {document.name}
          </Typography>
          <Typography variant="h6" color="text.secondary">
            {document.id} • {document.type} • {document.size ? `${Math.round(document.size / 1024)} KB` : 'Unknown size'}
          </Typography>
        </Box>

        {/* Document Viewer */}
        <DocumentViewer
          document={document}
          onDocumentAnalyzed={() => {
            // Refresh document data after analysis
            window.location.reload();
          }}
        />
      </Box>
    </Container>
  );
};

export default DocumentDetail;