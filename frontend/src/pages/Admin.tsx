import React, { useState } from 'react';
import {
  Container,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Box,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Storage as StorageIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import { apiClient } from '../services/api';

interface CorpusRegenerationResult {
  success: boolean;
  message: string;
  total_documents: number;
  research_areas: string[];
  legal_concepts_count: number;
  last_updated: string;
}

interface DocumentAnalysisResult {
  success: boolean;
  message: string;
  total_documents: number;
  analyzed_documents: number;
  failed_documents: number;
  average_confidence: number;
  processing_time_seconds: number;
}

const Admin: React.FC = () => {
  const [corpusLoading, setCorpusLoading] = useState(false);
  const [corpusResult, setCorpusResult] = useState<CorpusRegenerationResult | null>(null);
  const [corpusError, setCorpusError] = useState<string | null>(null);
  
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<DocumentAnalysisResult | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  const handleRegenerateIndex = async () => {
    setCorpusLoading(true);
    setCorpusError(null);
    setCorpusResult(null);

    try {
      const response = await apiClient.post<CorpusRegenerationResult>('/api/corpus/regenerate-index');
      setCorpusResult(response.data);
    } catch (err: any) {
      console.error('Failed to regenerate corpus index:', err);
      setCorpusError(err.response?.data?.detail || 'Failed to regenerate corpus index');
    } finally {
      setCorpusLoading(false);
    }
  };

  const handleRegenerateAnalysis = async () => {
    setAnalysisLoading(true);
    setAnalysisError(null);
    setAnalysisResult(null);

    try {
      const response = await apiClient.post<DocumentAnalysisResult>('/api/documents/regenerate-analysis');
      setAnalysisResult(response.data);
    } catch (err: any) {
      console.error('Failed to regenerate document analysis:', err);
      setAnalysisError(err.response?.data?.detail || 'Failed to regenerate document analysis');
    } finally {
      setAnalysisLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Typography variant="h4" component="h1" color="primary" gutterBottom>
          System Administration
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Administrative functions for managing the legal AI system
        </Typography>

        {/* Corpus Index Management */}
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <StorageIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                Research Corpus Index
              </Typography>
            </Box>
            
            <Typography variant="body1" color="text.secondary" paragraph>
              The corpus index organizes all legal documents, templates, and precedents for search and analysis. 
              Regenerate the index after adding new legal documents or updating existing ones.
            </Typography>

            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                What the corpus index includes:
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Document Metadata" 
                    secondary="Titles, descriptions, categories, and research areas"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Legal Concept Mapping" 
                    secondary="Links documents to relevant legal concepts for intelligent search"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Document Relationships" 
                    secondary="Connections between related legal materials and precedents"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Search Optimization" 
                    secondary="Enables concept-based search and document discovery"
                  />
                </ListItem>
              </List>
            </Box>

            <Divider sx={{ my: 3 }} />

            {/* Action Button */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
              <Button
                variant="contained"
                color="primary"
                size="large"
                startIcon={corpusLoading ? <CircularProgress size={20} /> : <RefreshIcon />}
                onClick={handleRegenerateIndex}
                disabled={corpusLoading}
              >
                {corpusLoading ? 'Regenerating Index...' : 'Regenerate Corpus Index'}
              </Button>
              
              {corpusLoading && (
                <Typography variant="body2" color="text.secondary">
                  This may take a few moments...
                </Typography>
              )}
            </Box>

            {/* Error Display */}
            {corpusError && (
              <Alert severity="error" sx={{ mb: 3 }} icon={<ErrorIcon />}>
                <Typography variant="body2">
                  <strong>Error:</strong> {corpusError}
                </Typography>
              </Alert>
            )}

            {/* Success Result */}
            {corpusResult && corpusResult.success && (
              <Alert severity="success" sx={{ mb: 3 }} icon={<CheckIcon />}>
                <Typography variant="body2" gutterBottom>
                  <strong>Success:</strong> {corpusResult.message}
                </Typography>
                
                <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  <Chip 
                    label={`${corpusResult.total_documents} Documents`} 
                    color="success" 
                    size="small" 
                  />
                  <Chip 
                    label={`${corpusResult.legal_concepts_count} Legal Concepts`} 
                    color="success" 
                    size="small" 
                  />
                  <Chip 
                    label={`${corpusResult.research_areas.length} Research Areas`} 
                    color="success" 
                    size="small" 
                  />
                </Box>

                {corpusResult.research_areas.length > 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Research Areas:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                      {corpusResult.research_areas.map((area) => (
                        <Chip
                          key={area}
                          label={area}
                          size="small"
                          variant="outlined"
                          color="secondary"
                        />
                      ))}
                    </Box>
                  </Box>
                )}

                <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
                  Last updated: {new Date(corpusResult.last_updated).toLocaleString()}
                </Typography>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Document Analysis Management */}
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <StorageIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                Document Analysis
              </Typography>
            </Box>
            
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              AI-powered analysis of all case documents including key dates, parties, summaries, and legal concepts. 
              Regenerate analysis after updating AI algorithms or to refresh existing analysis results.
            </Typography>

            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                What document analysis includes:
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Key Information Extraction" 
                    secondary="Dates, parties, document types, and important clauses"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="AI-Generated Summaries" 
                    secondary="Concise summaries of document content and purpose"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Confidence Scoring" 
                    secondary="Quality assessment and uncertainty flags for analysis results"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Risk Assessment" 
                    secondary="Potential issues, compliance status, and critical deadlines"
                  />
                </ListItem>
              </List>
            </Box>

            <Divider sx={{ my: 3 }} />

            {/* Action Button */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
              <Button
                variant="contained"
                color="secondary"
                size="large"
                startIcon={analysisLoading ? <CircularProgress size={20} /> : <RefreshIcon />}
                onClick={handleRegenerateAnalysis}
                disabled={analysisLoading}
              >
                {analysisLoading ? 'Regenerating Analysis...' : 'Regenerate Document Analysis'}
              </Button>
              
              {analysisLoading && (
                <Typography variant="body2" color="text.secondary">
                  This may take several minutes for large document collections...
                </Typography>
              )}
            </Box>

            {/* Error Display */}
            {analysisError && (
              <Alert severity="error" sx={{ mb: 3 }} icon={<ErrorIcon />}>
                <Typography variant="body2">
                  <strong>Error:</strong> {analysisError}
                </Typography>
              </Alert>
            )}

            {/* Success Result */}
            {analysisResult && analysisResult.success && (
              <Alert severity="success" sx={{ mb: 3 }} icon={<CheckIcon />}>
                <Typography variant="body2" gutterBottom>
                  <strong>Success:</strong> {analysisResult.message}
                </Typography>
                
                <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  <Chip 
                    label={`${analysisResult.total_documents} Total Documents`} 
                    color="info" 
                    size="small" 
                  />
                  <Chip 
                    label={`${analysisResult.analyzed_documents} Analyzed`} 
                    color="success" 
                    size="small" 
                  />
                  {analysisResult.failed_documents > 0 && (
                    <Chip 
                      label={`${analysisResult.failed_documents} Failed`} 
                      color="error" 
                      size="small" 
                    />
                  )}
                  <Chip 
                    label={`${Math.round(analysisResult.average_confidence * 100)}% Avg Confidence`} 
                    color="secondary" 
                    size="small" 
                  />
                  <Chip 
                    label={`${analysisResult.processing_time_seconds}s Processing Time`} 
                    color="default" 
                    size="small" 
                  />
                </Box>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Future Admin Functions */}
        <Card>
          <CardContent>
            <Typography variant="h5" component="h2" gutterBottom>
              Additional Admin Functions
            </Typography>
            <Typography variant="body2" color="text.secondary">
              More administrative functions will be available here in future updates, including:
            </Typography>
            <List dense sx={{ mt: 1 }}>
              <ListItem>
                <ListItemText 
                  primary="• System Health Monitoring" 
                  secondary="View system status and performance metrics"
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="• Data Export/Import" 
                  secondary="Backup and restore system data"
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="• User Management" 
                  secondary="Manage user accounts and permissions"
                />
              </ListItem>
            </List>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default Admin;