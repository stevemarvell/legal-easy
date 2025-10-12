import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Alert,
  CircularProgress,
  IconButton,
  Tooltip,
  Button
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Description as DocumentIcon
} from '@mui/icons-material';
import { documentsService } from '../../services/documentsService';
import { Document } from '../../types/document';

interface DocumentViewerProps {
  document: Document;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({
  document: initialDocument
}) => {
  const [document, setDocument] = useState<Document>(initialDocument);
  const [error, setError] = useState<string | null>(null);
  const [fullContent, setFullContent] = useState<string>('');
  const [contentLoading, setContentLoading] = useState(false);

  // Update document when prop changes
  useEffect(() => {
    setDocument(initialDocument);
  }, [initialDocument]);

  // Fetch full document content when document is loaded
  useEffect(() => {
    if (document && !fullContent) {
      loadFullContent();
    }
  }, [document, fullContent]);

  const loadFullContent = async () => {
    if (!document) return;

    try {
      setContentLoading(true);
      const contentData = await documentsService.getDocumentContent(document.id);
      setFullContent(contentData.content);
    } catch (err) {
      console.error('Failed to load document content:', err);
      setError('Failed to load full document content.');
    } finally {
      setContentLoading(false);
    }
  };

  const handleRefreshContent = async () => {
    setFullContent('');
    setError(null);
    await loadFullContent();
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (!document) {
    return (
      <Alert severity="warning">
        Document not found
      </Alert>
    );
  }

  return (
    <Box>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Document Information Card */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
            <Box display="flex" alignItems="center" gap={2}>
              <DocumentIcon color="primary" />
              <Typography variant="h6" component="h2">
                {document.name}
              </Typography>
            </Box>
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

          {/* Document Metadata */}
          <Box display="grid" gridTemplateColumns={{ xs: '1fr', sm: 'repeat(2, 1fr)', md: 'repeat(4, 1fr)' }} gap={2} mb={3}>
            <Box>
              <Typography variant="caption" color="text.secondary">
                Document ID
              </Typography>
              <Typography variant="body2" fontWeight="medium">
                {document.id}
              </Typography>
            </Box>
            <Box>
              <Typography variant="caption" color="text.secondary">
                Type
              </Typography>
              <Typography variant="body2" fontWeight="medium">
                {document.type}
              </Typography>
            </Box>
            <Box>
              <Typography variant="caption" color="text.secondary">
                Size
              </Typography>
              <Typography variant="body2" fontWeight="medium">
                {formatFileSize(document.size)}
              </Typography>
            </Box>
            <Box>
              <Typography variant="caption" color="text.secondary">
                Upload Date
              </Typography>
              <Typography variant="body2" fontWeight="medium">
                {formatDate(document.upload_date)}
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Document Content */}
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h6" component="h3">
              Document Content
            </Typography>
            {contentLoading && <CircularProgress size={20} />}
          </Box>

          {contentLoading ? (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
              <CircularProgress />
            </Box>
          ) : fullContent ? (
            <Box
              sx={{
                backgroundColor: 'grey.50',
                border: '1px solid',
                borderColor: 'grey.200',
                borderRadius: 1,
                p: 2,
                maxHeight: '600px',
                overflow: 'auto',
                fontFamily: 'monospace',
                fontSize: '0.875rem',
                lineHeight: 1.6,
                whiteSpace: 'pre-wrap'
              }}
            >
              {fullContent}
            </Box>
          ) : document.content_preview ? (
            <Box>
              <Typography variant="subtitle2" gutterBottom color="text.secondary">
                Preview:
              </Typography>
              <Box
                sx={{
                  backgroundColor: 'grey.50',
                  border: '1px solid',
                  borderColor: 'grey.200',
                  borderRadius: 1,
                  p: 2,
                  fontFamily: 'monospace',
                  fontSize: '0.875rem',
                  lineHeight: 1.6,
                  whiteSpace: 'pre-wrap'
                }}
              >
                {document.content_preview}
              </Box>
              <Button
                variant="outlined"
                onClick={loadFullContent}
                sx={{ mt: 2 }}
                startIcon={<DocumentIcon />}
              >
                Load Full Content
              </Button>
            </Box>
          ) : (
            <Alert severity="info">
              No preview available for this document
            </Alert>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default DocumentViewer;