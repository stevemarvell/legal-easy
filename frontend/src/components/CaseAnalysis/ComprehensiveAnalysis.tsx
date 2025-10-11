import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Button,
  Grid,
  LinearProgress
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Assessment as AssessmentIcon,
  Lightbulb as RecommendationIcon,
  Gavel as PrecedentIcon,
  CheckCircle as StrengthIcon,
  Warning as WeaknessIcon,
  Folder as EvidenceIcon,
  MenuBook as PlaybookIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import { playbookService } from '../../services/playbookService';
import { ComprehensiveAnalysis } from '../../types/playbook';

interface ComprehensiveAnalysisProps {
  caseId: string;
  onAnalysisComplete?: (analysis: ComprehensiveAnalysis) => void;
}

const ComprehensiveAnalysisComponent: React.FC<ComprehensiveAnalysisProps> = ({
  caseId,
  onAnalysisComplete
}) => {
  const [analysis, setAnalysis] = useState<ComprehensiveAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalysis();
  }, [caseId]);

  const fetchAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await playbookService.getComprehensiveAnalysis(caseId);
      setAnalysis(result);
      onAnalysisComplete?.(result);
    } catch (err: any) {
      console.error('Failed to fetch comprehensive analysis:', err);
      setError(err.message || 'Failed to load case analysis');
    } finally {
      setLoading(false);
    }
  };

  const getStrengthColor = (strength: string) => {
    switch (strength) {
      case 'Strong': return 'success';
      case 'Moderate': return 'warning';
      case 'Weak': return 'error';
      default: return 'default';
    }
  };

  const getConfidenceLevel = (confidence: number) => {
    if (confidence >= 0.8) return { label: 'High', color: 'success' };
    if (confidence >= 0.6) return { label: 'Medium', color: 'warning' };
    return { label: 'Low', color: 'error' };
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'error';
      case 'Medium': return 'warning';
      case 'Low': return 'info';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box display="flex" flexDirection="column" alignItems="center" py={4}>
            <CircularProgress sx={{ mb: 2 }} />
            <Typography variant="body1">Analyzing case with playbook...</Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={fetchAnalysis}
          >
            Retry Analysis
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!analysis) {
    return (
      <Card>
        <CardContent>
          <Alert severity="info">
            No analysis data available for this case.
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const confidenceInfo = getConfidenceLevel(analysis.case_strength_assessment.confidence_level);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      {/* Header */}
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
            <Typography variant="h5" component="h2" gutterBottom>
              Comprehensive Case Analysis
            </Typography>
            <Button
              variant="outlined"
              size="small"
              startIcon={<RefreshIcon />}
              onClick={fetchAnalysis}
            >
              Refresh
            </Button>
          </Box>

          {analysis.applied_playbook && (
            <Box display="flex" alignItems="center" gap={2} mb={2}>
              <PlaybookIcon color="primary" />
              <Typography variant="body1">
                Applied Playbook: <strong>{analysis.applied_playbook.name}</strong>
              </Typography>
              <Chip
                label={analysis.applied_playbook.case_type}
                variant="outlined"
                size="small"
              />
            </Box>
          )}

          {analysis.fallback_reason && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              <strong>Fallback Analysis:</strong> {analysis.fallback_reason}
            </Alert>
          )}

          <Typography variant="body2" color="text.secondary">
            Analysis completed: {new Date(analysis.analysis_timestamp).toLocaleString()}
          </Typography>
        </CardContent>
      </Card>

      {/* Case Strength Assessment */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box display="flex" alignItems="center" gap={2}>
            <AssessmentIcon color="primary" />
            <Typography variant="h6">Case Strength Assessment</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Box mb={3}>
                <Typography variant="subtitle1" gutterBottom>
                  Overall Strength
                </Typography>
                <Box display="flex" alignItems="center" gap={2} mb={2}>
                  <Chip
                    label={analysis.case_strength_assessment.overall_strength}
                    color={getStrengthColor(analysis.case_strength_assessment.overall_strength) as any}
                    size="large"
                  />
                  <Box flex={1}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Confidence: {confidenceInfo.label} ({Math.round(analysis.case_strength_assessment.confidence_level * 100)}%)
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={analysis.case_strength_assessment.confidence_level * 100}
                      color={confidenceInfo.color as any}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                </Box>
              </Box>
            </Grid>

            <Grid item xs={12} md={6}>
              {analysis.case_strength_assessment.key_strengths.length > 0 && (
                <Box mb={3}>
                  <Typography variant="subtitle1" gutterBottom>
                    Key Strengths
                  </Typography>
                  <List dense>
                    {analysis.case_strength_assessment.key_strengths.map((strength, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <StrengthIcon color="success" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={strength} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </Grid>

            <Grid item xs={12} md={6}>
              {analysis.case_strength_assessment.potential_weaknesses.length > 0 && (
                <Box mb={3}>
                  <Typography variant="subtitle1" gutterBottom>
                    Potential Weaknesses
                  </Typography>
                  <List dense>
                    {analysis.case_strength_assessment.potential_weaknesses.map((weakness, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <WeaknessIcon color="warning" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={weakness} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </Grid>

            <Grid item xs={12} md={6}>
              {analysis.case_strength_assessment.supporting_evidence.length > 0 && (
                <Box mb={3}>
                  <Typography variant="subtitle1" gutterBottom>
                    Supporting Evidence Required
                  </Typography>
                  <List dense>
                    {analysis.case_strength_assessment.supporting_evidence.map((evidence, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <EvidenceIcon color="info" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={evidence} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Strategic Recommendations */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box display="flex" alignItems="center" gap={2}>
            <RecommendationIcon color="primary" />
            <Typography variant="h6">Strategic Recommendations</Typography>
            <Chip label={analysis.strategic_recommendations.length} size="small" />
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {analysis.strategic_recommendations.map((recommendation, index) => (
              <Card key={recommendation.id} variant="outlined">
                <CardContent>
                  <Box display="flex" justifyContent="between" alignItems="flex-start" mb={2}>
                    <Typography variant="h6" component="h3">
                      {recommendation.title}
                    </Typography>
                    <Chip
                      label={recommendation.priority}
                      color={getPriorityColor(recommendation.priority) as any}
                      size="small"
                    />
                  </Box>
                  <Typography variant="body1" paragraph>
                    {recommendation.description}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    <strong>Rationale:</strong> {recommendation.rationale}
                  </Typography>
                  {recommendation.supporting_precedents.length > 0 && (
                    <Box>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        <strong>Supporting Precedents:</strong>
                      </Typography>
                      <Box display="flex" flexWrap="wrap" gap={1}>
                        {recommendation.supporting_precedents.map((precedent, idx) => (
                          <Chip key={idx} label={precedent} variant="outlined" size="small" />
                        ))}
                      </Box>
                    </Box>
                  )}
                </CardContent>
              </Card>
            ))}
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* Relevant Precedents */}
      {analysis.relevant_precedents.length > 0 && (
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Box display="flex" alignItems="center" gap={2}>
              <PrecedentIcon color="primary" />
              <Typography variant="h6">Relevant Legal Precedents</Typography>
              <Chip label={analysis.relevant_precedents.length} size="small" />
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {analysis.relevant_precedents.map((precedent, index) => (
                <Card key={precedent.id} variant="outlined">
                  <CardContent>
                    <Box display="flex" justifyContent="between" alignItems="flex-start" mb={1}>
                      <Typography variant="h6" component="h3">
                        {precedent.title}
                      </Typography>
                      <Chip
                        label={precedent.category}
                        variant="outlined"
                        size="small"
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {precedent.relevance}
                    </Typography>
                    {precedent.key_principle && (
                      <Typography variant="body2">
                        <strong>Key Principle:</strong> {precedent.key_principle}
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              ))}
            </Box>
          </AccordionDetails>
        </Accordion>
      )}
    </Box>
  );
};

export default ComprehensiveAnalysisComponent;