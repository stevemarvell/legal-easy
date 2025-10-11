import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Chip,
  Box,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Description as DocumentIcon,
  Email as EmailIcon,
  Gavel as LegalIcon,
  Assignment as ContractIcon,
  Folder as FolderIcon,
  CheckCircle as AnalyzedIcon,
  Schedule as PendingIcon,
  CalendarToday as CalendarIcon,
  Assessment as AssessmentIcon,
  Visibility as ViewIcon,
  PlayArrow as AnalyzeIcon
} from '@mui/icons-material';
import { Document } from '../../types/document';

interface DocumentCardProps {
  document: Document;
  caseId?: string;
  onAnalyze?: (document: Document) => void;
  showCaseInfo?: boolean;
}

const DocumentCard: React.FC<DocumentCardProps> = ({ 
  document, 
  caseId, 
  onAnalyze,
  showCaseInfo = false 
}) => {
  const navigate = useNavigate();

  const getDocumentIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'email':
        return <EmailIcon color="primary" />;
      case 'contract':
        return <ContractIcon color="primary" />;
      case 'legal brief':
        return <LegalIcon color="primary" />;
      default:
        return <DocumentIcon color="primary" />;
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const handleCardClick = (event: React.MouseEvent) => {
    // Prevent navigation if clicking on buttons or other interactive elements
    const target = event.target as HTMLElement;
    if (target.closest('button') || target.closest('.MuiCardActions-root')) {
      return;
    }
    
    // Navigate to document detail page
    if (caseId) {
      navigate(`/cases/${caseId}/documents/${document.id}`);
    } else {
      navigate(`/documents/${document.id}`);
    }
  };

  const handleViewDocument = (event?: React.MouseEvent) => {
    if (event) {
      event.stopPropagation();
    }
    
    if (caseId) {
      navigate(`/cases/${caseId}/documents/${document.id}`);
    } else {
      navigate(`/documents/${document.id}`);
    }
  };

  const handleAnalyzeDocument = (event?: React.MouseEvent) => {
    if (event) {
      event.stopPropagation();
    }
    
    if (onAnalyze) {
      onAnalyze(document);
    }
  };

  return (
    <Card 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        cursor: 'pointer',
        transition: 'all 0.2s ease-in-out',
        border: '1px solid transparent',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: (theme) => theme.shadows[8],
          borderColor: (theme) => theme.palette.primary.main,
        }
      }}
      onClick={handleCardClick}
      title={`Click to view details for ${document.name}`}
      data-testid="document-card"
      role="button"
      tabIndex={0}
    >
      <CardContent sx={{ flexGrow: 1 }}>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box display="flex" alignItems="center" gap={1} flex={1}>
            {getDocumentIcon(document.type)}
            <Typography 
              variant="h6" 
              component="h3" 
              gutterBottom
              sx={{ 
                color: 'primary.main',
                '&:hover': {
                  textDecoration: 'underline'
                },
                fontSize: '1rem',
                lineHeight: 1.2,
                mb: 0
              }}
              data-testid="document-title"
            >
              {document.name}
            </Typography>
          </Box>
          
          <Chip
            icon={document.analysis_completed ? <AnalyzedIcon /> : <PendingIcon />}
            label={document.analysis_completed ? 'Analyzed' : 'Pending'}
            color={document.analysis_completed ? 'success' : 'warning'}
            size="small"
            data-testid="document-analysis-status"
            data-status={document.analysis_completed ? 'completed' : 'pending'}
          />
        </Box>

        {/* Document Metadata */}
        <Box display="flex" alignItems="center" mb={1}>
          <AssessmentIcon color="primary" sx={{ mr: 1, fontSize: 20 }} />
          <Typography variant="body2" color="text.secondary" data-testid="document-type">
            {document.type}
          </Typography>
        </Box>

        <Box display="flex" alignItems="center" mb={1}>
          <FolderIcon color="primary" sx={{ mr: 1, fontSize: 20 }} />
          <Typography variant="body2" color="text.secondary" data-testid="document-size">
            Size: {formatFileSize(document.size)}
          </Typography>
        </Box>

        <Box display="flex" alignItems="center" mb={2}>
          <CalendarIcon color="primary" sx={{ mr: 1, fontSize: 20 }} />
          <Typography variant="body2" color="text.secondary" data-testid="document-upload-date">
            Uploaded: {formatDate(document.upload_date)}
          </Typography>
        </Box>

        {/* Content Preview */}
        {document.content_preview && (
          <Typography variant="body2" color="text.secondary" paragraph data-testid="document-preview">
            {document.content_preview.length > 120
              ? `${document.content_preview.substring(0, 120)}...`
              : document.content_preview
            }
          </Typography>
        )}

        {/* Case Info (if shown) */}
        {showCaseInfo && caseId && (
          <Box mt={2} pt={2} borderTop={1} borderColor="divider">
            <Typography variant="caption" color="text.secondary">
              Case: {caseId}
            </Typography>
          </Box>
        )}
      </CardContent>

      <CardActions>
        <Button
          size="small"
          variant="outlined"
          startIcon={<ViewIcon />}
          onClick={handleViewDocument}
          data-testid="view-document-button"
        >
          View Details
        </Button>
        
        {!document.analysis_completed && onAnalyze && (
          <Button
            size="small"
            variant="contained"
            startIcon={<AnalyzeIcon />}
            onClick={handleAnalyzeDocument}
            data-testid="analyze-document-button"
          >
            Analyze
          </Button>
        )}
      </CardActions>
    </Card>
  );
};

export default DocumentCard;