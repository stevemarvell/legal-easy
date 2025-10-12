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
  Info as InfoIcon,
  Analytics as AnalyticsIcon
} from '@mui/icons-material';
import { apiClient } from '../services/api';
import { APP_NAME } from '../constants/branding';
import { useDocumentTitle } from '../hooks/useDocumentTitle';

interface CorpusRegenerationResult {
  success: boolean;
  message: string;
  total_documents: number;
  research_areas: string[];
  legal_concepts_count: number;
  last_updated: string;
}



interface CaseAnalysisResult {
  success: boolean;
  message: string;
  total_cases: number;
  analyzed_cases: number;
  failed_cases: number;
  average_confidence: number;
  processing_time_seconds: number;
  analysis_types: string[];
}

const Admin: React.FC = () => {
  useDocumentTitle('System Administration');

  const [corpusLoading, setCorpusLoading] = useState(false);
  const [corpusResult, setCorpusResult] = useState<CorpusRegenerationResult | null>(null);
  const [corpusError, setCorpusError] = useState<string | null>(null);



  const [caseAnalysisLoading, setCaseAnalysisLoading] = useState(false);
  const [caseAnalysisResult, setCaseAnalysisResult] = useState<CaseAnalysisResult | null>(null);
  const [caseAnalysisError, setCaseAnalysisError] = useState<string | null>(null);



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



  const handleRegenerateCaseAnalysis = async () => {
    setCaseAnalysisLoading(true);
    setCaseAnalysisError(null);
    setCaseAnalysisResult(null);

    try {
      // Comprehensive analysis that includes case overview, documents, and research
      const response = await apiClient.post<CaseAnalysisResult>('/api/cases/comprehensive-analysis');
      setCaseAnalysisResult(response.data);
    } catch (err: any) {
      console.error('Failed to run comprehensive case analysis:', err);
      setCaseAnalysisError(err.response?.data?.detail || 'Failed to run comprehensive case analysis');
    } finally {
      setCaseAnalysisLoading(false);
    }
  };



  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Typography variant="h4" component="h1" color="primary" gutterBottom>
          System Administration
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
          Administrative functions for managing the {APP_NAME} system
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

            <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
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
                  Last updated: {new Date(corpusResult.last_updated).toLocaleString('en-GB')}
                </Typography>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Comprehensive Case Analysis */}
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <AnalyticsIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                Comprehensive Case Analysis
              </Typography>
            </Box>

            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              Comprehensive AI-powered analysis that integrates case overview and details, document analysis, 
              and research corpus to provide strategic insights and recommendations for all cases.
            </Typography>

            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                What comprehensive case analysis includes:
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Case Overview & Details Analysis"
                    secondary="Extracts legal elements, timeline, parties, issues, and evidence from case descriptions"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Document Integration"
                    secondary="Links case documents with extracted key information, summaries, and legal concepts"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Research Correlation"
                    secondary="Matches cases with relevant precedents, statutes, and legal materials from corpus"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Strategic Recommendations"
                    secondary="AI-generated legal strategies based on playbook rules and comprehensive case analysis"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Risk & Strength Assessment"
                    secondary="Comprehensive evaluation of case strengths, weaknesses, and potential outcomes"
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
                startIcon={caseAnalysisLoading ? <CircularProgress size={20} /> : <AnalyticsIcon />}
                onClick={handleRegenerateCaseAnalysis}
                disabled={caseAnalysisLoading}
              >
                {caseAnalysisLoading ? 'Analyzing Cases...' : 'Analyze Case Overview, Documents & Research'}
              </Button>

              {caseAnalysisLoading && (
                <Typography variant="body2" color="text.secondary">
                  This may take several minutes for comprehensive analysis...
                </Typography>
              )}
            </Box>

            {/* Error Display */}
            {caseAnalysisError && (
              <Alert severity="error" sx={{ mb: 3 }} icon={<ErrorIcon />}>
                <Typography variant="body2">
                  <strong>Error:</strong> {caseAnalysisError}
                </Typography>
              </Alert>
            )}

            {/* Success Result */}
            {caseAnalysisResult && caseAnalysisResult.success && (
              <Alert severity="success" sx={{ mb: 3 }} icon={<CheckIcon />}>
                <Typography variant="body2" gutterBottom>
                  <strong>Success:</strong> {caseAnalysisResult.message}
                </Typography>

                <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  <Chip
                    label={`${caseAnalysisResult.total_cases} Total Cases`}
                    color="info"
                    size="small"
                  />
                  <Chip
                    label={`${caseAnalysisResult.analyzed_cases} Analyzed`}
                    color="success"
                    size="small"
                  />
                  {caseAnalysisResult.failed_cases > 0 && (
                    <Chip
                      label={`${caseAnalysisResult.failed_cases} Failed`}
                      color="error"
                      size="small"
                    />
                  )}
                  <Chip
                    label={`${Math.round(caseAnalysisResult.average_confidence * 100)}% Avg Confidence`}
                    color="secondary"
                    size="small"
                  />
                  <Chip
                    label={`${caseAnalysisResult.processing_time_seconds}s Processing Time`}
                    color="default"
                    size="small"
                  />
                </Box>

                {caseAnalysisResult.analysis_types.length > 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Analysis Types:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                      {caseAnalysisResult.analysis_types.map((type) => (
                        <Chip
                          key={type}
                          label={type}
                          size="small"
                          variant="outlined"
                          color="secondary"
                        />
                      ))}
                    </Box>
                  </Box>
                )}
              </Alert>
            )}
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default Admin;