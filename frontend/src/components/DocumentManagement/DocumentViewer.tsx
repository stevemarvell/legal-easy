import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Alert,
  CircularProgress,
  Paper,
  IconButton,
  Tooltip,
  Button,
  Tabs,
  Tab
} from '@mui/material';
import {
  CheckCircle as AnalyzedIcon,
  Schedule as PendingIcon,
  Refresh as RefreshIcon,
  Psychology as AnalyzeIcon,
  Description as DocumentIcon,
  Analytics as AnalysisIcon
} from '@mui/icons-material';
import { documentService } from '../../services/documentService';
import { Document } from '../../types/document';
import DocumentAnalysis from './DocumentAnalysis';

interface DocumentViewerProps {
  document: Document;
  onDocumentAnalyzed?: () => void;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({
  document: initialDocument,
  onDocumentAnalyzed
}) => {
  const [document, setDocument] = useState<Document>(initialDocument);
  const [error, setError] = useState<string | null>(null);

  const [fullContent, setFullContent] = useState<string>('');
  const [contentLoading, setContentLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [activeTab, setActiveTab] = useState(0);

  // Update document when prop changes
  useEffect(() => {
    setDocument(initialDocument);
  }, [initialDocument]);

  // Fetch full document content when document is loaded
  useEffect(() => {
    const fetchContent = async () => {
      try {
        setContentLoading(true);
        const contentData = await documentService.getDocumentContent(document.id);
        setFullContent(contentData.content);
      } catch (err) {
        console.error('Failed to fetch document content:', err);
        // Fallback to content preview if full content fails
        setFullContent(document.content_preview || 'Content not available');
      } finally {
        setContentLoading(false);
      }
    };

    fetchContent();
  }, [document.id]);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
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



  const handleRefreshContent = async () => {
    try {
      setContentLoading(true);
      const contentData = await documentService.getDocumentContent(document.id);
      setFullContent(contentData.content);
    } catch (err) {
      console.error('Failed to refresh document content:', err);
      setError('Failed to refresh document content');
    } finally {
      setContentLoading(false);
    }
  };

  const handleAnalyzeDocument = async () => {
    try {
      setAnalyzing(true);
      await documentService.analyzeDocument(document.id);
      // Refresh document to get updated analysis status
      const updatedDocument = await documentService.getDocumentById(document.id);
      setDocument(updatedDocument);
      // Switch to analysis tab after successful analysis
      setActiveTab(1);
      // Notify parent component to refresh document list
      onDocumentAnalyzed?.();
    } catch (err) {
      console.error('Failed to analyze document:', err);
      setError('Failed to analyze document. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Document Header */}
      <Card sx={{ mb: 2, flexShrink: 0 }}>
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
            <Box display="flex" alignItems="center" gap={2}>
              <Chip
                icon={getStatusIcon(document.analysis_completed)}
                label={getStatusText(document.analysis_completed)}
                color={getStatusColor(document.analysis_completed)}
                variant="outlined"
              />
              {!document.analysis_completed && (
                <Button
                  variant="contained"
                  startIcon={analyzing ? <CircularProgress size={16} /> : <AnalyzeIcon />}
                  onClick={handleAnalyzeDocument}
                  disabled={analyzing}
                  size="small"
                >
                  {analyzing ? 'Analyzing...' : 'Analyze Document'}
                </Button>
              )}
            </Box>
          </Box>
        </CardContent>
      </Card>



      {/* Tabs Navigation */}
      <Card sx={{ mb: 2, flexShrink: 0 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="fullWidth"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab
            icon={<DocumentIcon />}
            label="Document"
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
      <Box sx={{ flex: 1, minHeight: 0 }}>
        {/* Document Content Tab */}
        {activeTab === 0 && (
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column', pb: 1 }}>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Box display="flex" alignItems="center" gap={2}>
                  <Typography variant="h6">
                    Document Content
                  </Typography>
                  <Chip
                    size="small"
                    label={document.type}
                    variant="outlined"
                  />
                  <Chip
                    size="small"
                    label={formatFileSize(document.size)}
                    variant="outlined"
                  />
                </Box>
                <Box display="flex" alignItems="center" gap={1}>
                  {contentLoading && <CircularProgress size={16} />}
                  <Tooltip title="Refresh content">
                    <IconButton
                      onClick={handleRefreshContent}
                      disabled={contentLoading}
                      size="small"
                    >
                      <RefreshIcon />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>

              {contentLoading ? (
                <Box display="flex" justifyContent="center" alignItems="center" flex={1}>
                  <CircularProgress />
                </Box>
              ) : fullContent ? (
                <Paper
                  variant="outlined"
                  sx={{
                    flex: 1,
                    p: 2,
                    backgroundColor: 'grey.50',
                    overflow: 'auto',
                    border: '1px solid',
                    borderColor: 'grey.300',
                    borderRadius: 1,
                    '&::-webkit-scrollbar': {
                      width: '8px',
                    },
                    '&::-webkit-scrollbar-track': {
                      backgroundColor: 'grey.100',
                      borderRadius: '4px',
                    },
                    '&::-webkit-scrollbar-thumb': {
                      backgroundColor: 'grey.400',
                      borderRadius: '4px',
                      '&:hover': {
                        backgroundColor: 'grey.500',
                      },
                    },
                  }}
                >
                  <Typography
                    variant="body2"
                    component="pre"
                    sx={{
                      whiteSpace: 'pre-wrap',
                      fontFamily: 'monospace',
                      fontSize: '0.8rem',
                      lineHeight: 1.5,
                      color: 'text.primary',
                      margin: 0
                    }}
                  >
                    {fullContent}
                  </Typography>
                </Paper>
              ) : (
                <Alert severity="info">
                  Document content not available
                </Alert>
              )}
            </CardContent>
          </Card>
        )}

        {/* AI Analysis Tab */}
        {activeTab === 1 && document.analysis_completed && (
          <Box sx={{ height: '100%', overflow: 'auto', p: 1 }}>
            <DocumentAnalysis documentId={document.id} key={`analysis-${document.id}`} />
          </Box>
        )}

        {/* Analysis Not Available Message */}
        {activeTab === 1 && !document.analysis_completed && (
          <Alert severity="info">
            <Typography variant="body2">
              AI analysis is not yet available for this document. Click "Analyze Document" above to extract key information such as
              important dates, parties involved, and legal concepts.
            </Typography>
          </Alert>
        )}
      </Box>
    </Box>
  );
};

export default DocumentViewer;