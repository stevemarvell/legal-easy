import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Alert,
  CircularProgress,
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
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }} data-testid="document-viewer">
      {/* Document Header */}
      <Card sx={{ mb: 2, flexShrink: 0 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
            <Box flex={1}>
              <Typography variant="h6">
                {document.content_preview}
              </Typography>
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
                  data-testid="analyze-button"
                >
                  {analyzing ? 'Analyzing...' : 'Analyze Document'}
                </Button>
              )}
              {document.analysis_completed && (
                <Box data-testid="analysis-complete">
                  <Chip
                    icon={<AnalyzedIcon />}
                    label="Analysis Complete"
                    color="success"
                    variant="outlined"
                  />
                </Box>
              )}
            </Box>
          </Box>
        </CardContent>
      </Card>

            {/* Header */}
            <Card sx={{ mb: 1, flexShrink: 0 }}>
              <CardContent sx={{ pb: 2 }}>
                <Box display="flex" alignItems="center" justifyContent="space-between">

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
          />
        </Tabs>
      </Card>

      {/* Tab Content */}
      <Box sx={{ flex: 1, minHeight: 0, overflow: 'hidden' }}>
        {/* Document Content Tab */}
        {activeTab === 0 && (
          <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            {/* Content Area - Scrollable Card */}
            <Box sx={{ flex: 1, minHeight: 0 }}>
              {contentLoading ? (
                <Card sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <CircularProgress />
                </Card>
              ) : fullContent ? (
                <Card
                  variant="outlined"
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    backgroundColor: 'background.paper',
                    border: '2px solid',
                    borderColor: 'primary.100',
                    borderRadius: 2,
                    overflow: 'hidden'
                  }}
                >
                  <CardContent
                    sx={{
                      flex: 1,
                      overflow: 'auto',
                      p: 3,
                      '&::-webkit-scrollbar': {
                        width: '12px',
                      },
                      '&::-webkit-scrollbar-track': {
                        backgroundColor: 'grey.100',
                        borderRadius: '6px',
                      },
                      '&::-webkit-scrollbar-thumb': {
                        backgroundColor: 'primary.300',
                        borderRadius: '6px',
                        '&:hover': {
                          backgroundColor: 'primary.400',
                        },
                      },
                    }}
                  >
                    <Typography
                      variant="body2"
                      component="pre"
                      data-testid="document-content"
                      sx={{
                        whiteSpace: 'pre-wrap',
                        fontFamily: 'monospace',
                        fontSize: '0.9rem',
                        lineHeight: 1.7,
                        color: 'text.primary',
                        margin: 0,
                        wordBreak: 'break-word'
                      }}
                    >
                      {fullContent}
                    </Typography>
                  </CardContent>
                </Card>
              ) : (
                <Card sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Alert severity="info">
                    Document content not available
                  </Alert>
                </Card>
              )}
            </Box>
          </Box>
        )}

        {/* AI Analysis Tab */}
        {activeTab === 1 && (
          <Box
            sx={{
              height: '100%',
              overflow: 'auto',
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
            {document.analysis_completed ? (
              <DocumentAnalysis documentId={document.id} key={`analysis-${document.id}`} />
            ) : (
              <Box sx={{ p: 2 }}>
                <Alert severity="info">
                  <Typography variant="body2">
                    AI analysis is not yet available for this document. Click "Analyze Document" above to extract key information such as
                    important dates, parties involved, and legal concepts.
                  </Typography>
                </Alert>
              </Box>
            )}
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default DocumentViewer;