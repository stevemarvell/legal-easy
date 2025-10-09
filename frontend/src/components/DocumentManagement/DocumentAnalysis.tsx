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
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Paper,
  Tooltip
} from '@mui/material';
import {
  Psychology as AIIcon,
  Event as DateIcon,
  Person as PersonIcon,
  Gavel as LegalIcon,
  Assignment as SummaryIcon,
  TrendingUp as ConfidenceIcon,
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import { documentService } from '../../services/documentService';
import { DocumentAnalysis as DocumentAnalysisType } from '../../types/document';

interface DocumentAnalysisProps {
  documentId: string;
  analysis?: DocumentAnalysisType; // Optional pre-loaded analysis
}

const DocumentAnalysis: React.FC<DocumentAnalysisProps> = ({ 
  documentId, 
  analysis: preloadedAnalysis 
}) => {
  const [analysis, setAnalysis] = useState<DocumentAnalysisType | null>(preloadedAnalysis || null);
  const [loading, setLoading] = useState(!preloadedAnalysis);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      if (preloadedAnalysis) {
        setAnalysis(preloadedAnalysis);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const fetchedAnalysis = await documentService.getDocumentAnalysis(documentId);
        setAnalysis(fetchedAnalysis);
      } catch (err) {
        console.error('Failed to fetch document analysis:', err);
        setError('Failed to load document analysis. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    if (documentId) {
      fetchAnalysis();
    }
  }, [documentId, preloadedAnalysis]);

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getConfidenceColor = (score: number): 'success' | 'warning' | 'error' => {
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'error';
  };

  const getConfidenceIcon = (score: number) => {
    if (score >= 0.8) return <CheckIcon color="success" />;
    return <WarningIcon color="warning" />;
  };

  const formatConfidenceScore = (score: number): string => {
    return `${Math.round(score * 100)}%`;
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="300px">
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

  if (!analysis) {
    return (
      <Alert severity="info" sx={{ mb: 2 }}>
        No analysis available for this document
      </Alert>
    );
  }

  return (
    <Box>
      {/* Analysis Header */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <AIIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h5" component="h2">
              AI Document Analysis
            </Typography>
          </Box>
          <Typography variant="body2" color="text.secondary">
            Automated analysis results for document {analysis.document_id}
          </Typography>
        </CardContent>
      </Card>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        {/* Document Summary */}
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <SummaryIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6">
                Document Summary
              </Typography>
            </Box>
            <Divider sx={{ mb: 2 }} />
            <Paper variant="outlined" sx={{ p: 2, backgroundColor: 'grey.50' }}>
              <Typography variant="body1">
                {analysis.summary}
              </Typography>
            </Paper>
          </CardContent>
        </Card>

        {/* Key Information and Legal Analysis */}
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
          {/* Key Information */}
          <Box sx={{ flex: 1 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Key Information
                </Typography>
                <Divider sx={{ mb: 2 }} />

                {/* Key Dates */}
                <Accordion defaultExpanded>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box display="flex" alignItems="center" gap={1}>
                      <DateIcon color="primary" />
                      <Typography variant="subtitle1">
                        Key Dates ({analysis.key_dates.length})
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    {analysis.key_dates.length > 0 ? (
                      <List dense>
                        {analysis.key_dates.map((date, index) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <DateIcon fontSize="small" />
                            </ListItemIcon>
                            <ListItemText primary={formatDate(date)} />
                          </ListItem>
                        ))}
                      </List>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No key dates identified
                      </Typography>
                    )}
                  </AccordionDetails>
                </Accordion>

                {/* Parties Involved */}
                <Accordion defaultExpanded>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box display="flex" alignItems="center" gap={1}>
                      <PersonIcon color="primary" />
                      <Typography variant="subtitle1">
                        Parties Involved ({analysis.parties_involved.length})
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    {analysis.parties_involved.length > 0 ? (
                      <List dense>
                        {analysis.parties_involved.map((party, index) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <PersonIcon fontSize="small" />
                            </ListItemIcon>
                            <ListItemText primary={party} />
                          </ListItem>
                        ))}
                      </List>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No parties identified
                      </Typography>
                    )}
                  </AccordionDetails>
                </Accordion>
              </CardContent>
            </Card>
          </Box>

          {/* Legal Analysis */}
          <Box sx={{ flex: 1 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Legal Analysis
                </Typography>
                <Divider sx={{ mb: 2 }} />

                {/* Document Type */}
                <Box mb={3}>
                  <Typography variant="subtitle2" gutterBottom>
                    Document Classification
                  </Typography>
                  <Chip
                    label={analysis.document_type}
                    color="primary"
                    variant="outlined"
                    size="medium"
                  />
                </Box>

                {/* Key Clauses */}
                <Accordion defaultExpanded>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box display="flex" alignItems="center" gap={1}>
                      <LegalIcon color="primary" />
                      <Typography variant="subtitle1">
                        Key Clauses ({analysis.key_clauses.length})
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    {analysis.key_clauses.length > 0 ? (
                      <List dense>
                        {analysis.key_clauses.map((clause, index) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <LegalIcon fontSize="small" />
                            </ListItemIcon>
                            <ListItemText 
                              primary={clause}
                              primaryTypographyProps={{ variant: 'body2' }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No key clauses identified
                      </Typography>
                    )}
                  </AccordionDetails>
                </Accordion>
              </CardContent>
            </Card>
          </Box>
        </Box>

        {/* Confidence Scores */}
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <ConfidenceIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6">
                Analysis Confidence Scores
              </Typography>
            </Box>
            <Divider sx={{ mb: 3 }} />

            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
              {Object.entries(analysis.confidence_scores).map(([category, score]) => (
                <Box key={category} sx={{ minWidth: 200, flex: '1 1 200px' }}>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                    <Typography variant="subtitle2" sx={{ textTransform: 'capitalize' }}>
                      {category.replace('_', ' ')}
                    </Typography>
                    <Box display="flex" alignItems="center" gap={0.5}>
                      <Tooltip title={`Confidence: ${formatConfidenceScore(score)}`}>
                        {getConfidenceIcon(score)}
                      </Tooltip>
                      <Typography variant="body2" fontWeight="bold">
                        {formatConfidenceScore(score)}
                      </Typography>
                    </Box>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={score * 100}
                    color={getConfidenceColor(score)}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
              ))}
            </Box>

            <Alert severity="info" sx={{ mt: 3 }}>
              <Typography variant="body2">
                Confidence scores indicate the AI's certainty in the extracted information. 
                Scores above 80% are considered highly reliable, while scores below 60% may require manual review.
              </Typography>
            </Alert>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default DocumentAnalysis;