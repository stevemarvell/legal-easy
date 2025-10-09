import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Alert,
  CircularProgress,
  Divider,
  Grid,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Tabs,
  Tab
} from '@mui/material';
import {
  Description as DocumentIcon,
  Person as PersonIcon,
  Event as DateIcon,
  Category as TypeIcon,
  FileDownload as SizeIcon,
  CheckCircle as AnalyzedIcon,
  Schedule as PendingIcon,
  ExpandMore as ExpandMoreIcon,
  Visibility as PreviewIcon,
  Psychology as AnalysisIcon
} from '@mui/icons-material';
import { documentService } from '../../services/documentService';
import { Document } from '../../types/document';
import DocumentAnalysis from './DocumentAnalysis';

interface DocumentViewerProps {
  documentId: string;
  document?: Document; // Optional pre-loaded document
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ documentId, document: preloadedDocument }) => {
  const [document, setDocument] = useState<Document | null>(preloadedDocument || null);
  const [loading, setLoading] = useState(!preloadedDocument);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    const fetchDocument = async () => {
      if (preloadedDocument) {
        setDocument(preloadedDocument);
        setLoading(false);
        return;
      }

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

    if (documentId) {
      fetchDocument();
    }
  }, [documentId, preloadedDocument]);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (analyzed: boolean) => {
    return analyzed ? 'success' : 'warning';
  };

  const getStatusIcon = (analyzed: boolean) => {
    return analyzed ? <AnalyzedIcon /> : <PendingIcon />;
  };

  const getStatusText = (analyzed: boolean) => {
    return analyzed ? 'AI Analysis Complete' : 'Analysis Pending';
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!document) {
    return (
      <Alert severity="warning" sx={{ mb: 2 }}>
        Document not found
      </Alert>
    );
  }

  return (
    <Box>
      {/* Document Header */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
            <Box flex={1}>
              <Typography variant="h5" component="h2" gutterBottom>
                {document.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Document ID: {document.id}
              </Typography>
            </Box>
            <Chip
              icon={getStatusIcon(document.analysis_completed)}
              label={getStatusText(document.analysis_completed)}
              color={getStatusColor(document.analysis_completed)}
              variant="outlined"
            />
          </Box>
        </CardContent>
      </Card>

      {/* Tabs Navigation */}
      <Card sx={{ mb: 3 }}>
        <Tabs 
          value={activeTab} 
          onChange={handleTabChange}
          variant="fullWidth"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab 
            icon={<PreviewIcon />} 
            label="Document Preview" 
            iconPosition="start"
          />
          <Tab 
            icon={<AnalysisIcon />} 
            label="AI Analysis" 
            iconPosition="start"
            disabled={!document.analysis_completed}
          />
        </Tabs>
      </Card>

      {/* Tab Content */}
      {activeTab === 0 && (
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
          {/* Document Metadata */}
          <Box sx={{ width: { xs: '100%', md: '33%' } }}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Document Information
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <TypeIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Document Type"
                      secondary={document.type}
                    />
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <SizeIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="File Size"
                      secondary={formatFileSize(document.size)}
                    />
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <DateIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Upload Date"
                      secondary={formatDate(document.upload_date)}
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>

            {/* Analysis Status Card */}
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Analysis Status
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                <Box display="flex" alignItems="center" gap={1} mb={2}>
                  {getStatusIcon(document.analysis_completed)}
                  <Typography variant="body1">
                    {getStatusText(document.analysis_completed)}
                  </Typography>
                </Box>

                {document.analysis_completed ? (
                  <Alert severity="success" sx={{ mt: 2 }}>
                    AI analysis is complete. Switch to the "AI Analysis" tab to view detailed results.
                  </Alert>
                ) : (
                  <Alert severity="warning" sx={{ mt: 2 }}>
                    This document is pending AI analysis. Analysis will extract key information such as 
                    important dates, parties involved, and legal concepts.
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Box>

          {/* Document Preview */}
          <Box sx={{ flex: 1 }}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <PreviewIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">
                    Document Preview
                  </Typography>
                </Box>
                <Divider sx={{ mb: 2 }} />
                
                {document.content_preview ? (
                  <Paper 
                    variant="outlined" 
                    sx={{ 
                      p: 2, 
                      backgroundColor: 'grey.50',
                      maxHeight: '500px',
                      overflow: 'auto'
                    }}
                  >
                    <Typography 
                      variant="body2" 
                      component="pre"
                      sx={{ 
                        whiteSpace: 'pre-wrap',
                        fontFamily: 'monospace',
                        fontSize: '0.875rem',
                        lineHeight: 1.6
                      }}
                    >
                      {document.content_preview}
                    </Typography>
                  </Paper>
                ) : (
                  <Alert severity="info">
                    No preview available for this document
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Box>
        </Box>
      )}

      {/* AI Analysis Tab */}
      {activeTab === 1 && document.analysis_completed && (
        <DocumentAnalysis documentId={document.id} />
      )}
    </Box>
  );
};

export default DocumentViewer;