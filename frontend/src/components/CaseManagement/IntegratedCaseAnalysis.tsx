import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Stack,
  Paper,
  ListItemIcon,
  Tooltip,
  IconButton
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Assessment as AssessmentIcon,
  MenuBook as PlaybookIcon,
  Search as ResearchIcon,
  Lightbulb as RecommendationIcon,
  Timeline as TimelineIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  TrendingUp as TrendingUpIcon,
  Gavel as GavelIcon,
  Description as DocumentIcon,
  Schedule as ScheduleIcon,
  Group as GroupIcon,
  Security as SecurityIcon,
  MonetizationOn as MoneyIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import { apiClient } from '../../services/api';

interface IntegratedAnalysis {
  case_id: string;
  case_info: {
    title: string;
    case_type: string;
    status: string;
    client_name: string;
  };
  document_analysis: {
    summary: {
      total_documents: number;
      document_types: string[];
      key_dates: string[];
      parties_involved: string[];
      key_clauses: string[];
      potential_risks: string[];
      themes: string[];
      timeline: Array<{
        date: string;
        description: string;
        related_documents: string[];
      }>;
    };
  };
  research_analysis: {
    total_found: number;
    top_relevant: Array<{
      id: string;
      title: string;
      category: string;
      relevance_score: number;
      description: string;
    }>;
    categorized: {
      precedents: any[];
      statutes: any[];
      contracts: any[];
      clauses: any[];
    };
    search_terms: string[];
  };
  playbook_analysis: {
    playbook_id: string;
    playbook_name: string;
    applicable_rules: Array<{
      rule_id: string;
      condition: string;
      action: string;
      weight: number;
      description: string;
      legal_basis: string;
    }>;
    decision_path: {
      result: string;
      recommended_actions: string[];
      monetary_range: string;
    };
    monetary_assessment: {
      range: [number, number];
      description: string;
      factors: string[];
    };
    escalation_path: Array<{
      step: number;
      action: string;
      timeline: string;
      description: string;
    }>;
    key_statutes: string[];
    success_factors: string[];
  };
  strategic_recommendations: {
    recommendations: Array<{
      category: string;
      priority: string;
      recommendation: string;
      basis: string;
    }>;
    strength_assessment: {
      overall: string;
      strengths: string[];
      weaknesses: string[];
    };
    next_steps: string[];
    risk_factors: string[];
  };
  case_assessment: {
    overall_score: number;
    assessment_level: string;
    confidence: string;
    component_scores: {
      document_analysis: number;
      research_support: number;
      playbook_alignment: number;
    };
  };
}

interface IntegratedCaseAnalysisProps {
  caseId: string;
}

const IntegratedCaseAnalysis: React.FC<IntegratedCaseAnalysisProps> = ({ caseId }) => {
  const [analysis, setAnalysis] = useState<IntegratedAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.get<IntegratedAnalysis>(`/api/cases/${caseId}/integrated-analysis`);
      setAnalysis(response.data);
    } catch (err: any) {
      console.error('Failed to fetch integrated analysis:', err);
      setError(err.response?.data?.detail || 'Failed to load integrated analysis');
    } finally {
      setLoading(false);
    }
  };

  const refreshAnalysis = async () => {
    try {
      setRefreshing(true);
      await fetchAnalysis();
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchAnalysis();
  }, [caseId]);

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'info';
      default: return 'default';
    }
  };

  const getAssessmentColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'strong': return 'success';
      case 'moderate': return 'warning';
      case 'weak': return 'error';
      default: return 'default';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
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
      <Alert severity="error" sx={{ mb: 4 }}>
        {error}
        <Button onClick={fetchAnalysis} sx={{ ml: 2 }}>
          Retry
        </Button>
      </Alert>
    );
  }

  if (!analysis) {
    return (
      <Alert severity="warning" sx={{ mb: 4 }}>
        No analysis data available
      </Alert>
    );
  }

  return (
    <Box>
      {/* Header with Overall Assessment */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
            <Typography variant="h5" component="h2">
              Integrated Case Analysis
            </Typography>
            <Tooltip title="Refresh Analysis">
              <IconButton onClick={refreshAnalysis} disabled={refreshing}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
          </Box>
          
          <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={3}>
            <Box flex={1} textAlign="center">
              <Typography variant="h3" color="primary" gutterBottom>
                {Math.round(analysis.case_assessment.overall_score * 100)}%
              </Typography>
              <Typography variant="h6" gutterBottom>
                Overall Score
              </Typography>
              <Chip 
                label={analysis.case_assessment.assessment_level}
                color={getAssessmentColor(analysis.case_assessment.assessment_level) as any}
              />
            </Box>
            
            <Box flex={2}>
              <Typography variant="h6" gutterBottom>
                Component Scores
              </Typography>
              <Box mb={2}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2">Document Analysis</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {Math.round(analysis.case_assessment.component_scores.document_analysis * 100)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={analysis.case_assessment.component_scores.document_analysis * 100}
                  sx={{ height: 8, borderRadius: 1 }}
                />
              </Box>
              
              <Box mb={2}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2">Research Support</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {Math.round(analysis.case_assessment.component_scores.research_support * 100)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={analysis.case_assessment.component_scores.research_support * 100}
                  sx={{ height: 8, borderRadius: 1 }}
                />
              </Box>
              
              <Box>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2">Playbook Alignment</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {Math.round(analysis.case_assessment.component_scores.playbook_alignment * 100)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={analysis.case_assessment.component_scores.playbook_alignment * 100}
                  sx={{ height: 8, borderRadius: 1 }}
                />
              </Box>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Strategic Recommendations */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box display="flex" alignItems="center">
            <RecommendationIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6">Strategic Recommendations</Typography>
            <Chip 
              label={`${analysis.strategic_recommendations.recommendations.length} recommendations`}
              size="small"
              sx={{ ml: 2 }}
            />
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={3}>
            <Box flex={2}>
              <List>
                {analysis.strategic_recommendations.recommendations.map((rec, index) => (
                  <ListItem key={index} divider={index < analysis.strategic_recommendations.recommendations.length - 1}>
                    <ListItemIcon>
                      <Chip 
                        label={rec.priority}
                        color={getPriorityColor(rec.priority) as any}
                        size="small"
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={rec.recommendation}
                      secondary={
                        <Box>
                          <Typography variant="caption" color="text.secondary">
                            Category: {rec.category}
                          </Typography>
                          <Typography variant="caption" color="text.secondary" display="block">
                            Basis: {rec.basis}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
            
            <Box flex={1}>
              <Paper sx={{ p: 2, mb: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Next Steps
                </Typography>
                <List dense>
                  {analysis.strategic_recommendations.next_steps.map((step, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <Typography variant="body2" color="primary" fontWeight="bold">
                          {index + 1}.
                        </Typography>
                      </ListItemIcon>
                      <ListItemText primary={step} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
              
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Case Strength
                </Typography>
                <Chip 
                  label={analysis.strategic_recommendations.strength_assessment.overall}
                  color={getAssessmentColor(analysis.strategic_recommendations.strength_assessment.overall) as any}
                  sx={{ mb: 2 }}
                />
                
                <Typography variant="subtitle2" color="success.main" gutterBottom>
                  Strengths:
                </Typography>
                <List dense>
                  {analysis.strategic_recommendations.strength_assessment.strengths.map((strength, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary={strength} />
                    </ListItem>
                  ))}
                </List>
                
                {analysis.strategic_recommendations.strength_assessment.weaknesses.length > 0 && (
                  <>
                    <Typography variant="subtitle2" color="warning.main" gutterBottom sx={{ mt: 2 }}>
                      Weaknesses:
                    </Typography>
                    <List dense>
                      {analysis.strategic_recommendations.strength_assessment.weaknesses.map((weakness, index) => (
                        <ListItem key={index}>
                          <ListItemIcon>
                            <WarningIcon color="warning" fontSize="small" />
                          </ListItemIcon>
                          <ListItemText primary={weakness} />
                        </ListItem>
                      ))}
                    </List>
                  </>
                )}
              </Paper>
            </Box>
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* Document Analysis Summary */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box display="flex" alignItems="center">
            <DocumentIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6">Document Analysis</Typography>
            <Chip 
              label={`${analysis.document_analysis.summary.total_documents} documents`}
              size="small"
              sx={{ ml: 2 }}
            />
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={3}>
            <Box flex={1}>
              <Typography variant="h6" gutterBottom>
                Key Information
              </Typography>
              
              <Box mb={3}>
                <Typography variant="subtitle2" gutterBottom>
                  <ScheduleIcon fontSize="small" sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Key Dates ({analysis.document_analysis.summary.key_dates.length})
                </Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap">
                  {analysis.document_analysis.summary.key_dates.slice(0, 5).map((date, index) => (
                    <Chip key={index} label={date} size="small" variant="outlined" />
                  ))}
                  {analysis.document_analysis.summary.key_dates.length > 5 && (
                    <Chip label={`+${analysis.document_analysis.summary.key_dates.length - 5} more`} size="small" />
                  )}
                </Stack>
              </Box>
              
              <Box mb={3}>
                <Typography variant="subtitle2" gutterBottom>
                  <GroupIcon fontSize="small" sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Parties Involved ({analysis.document_analysis.summary.parties_involved.length})
                </Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap">
                  {analysis.document_analysis.summary.parties_involved.slice(0, 3).map((party, index) => (
                    <Chip key={index} label={party} size="small" variant="outlined" />
                  ))}
                  {analysis.document_analysis.summary.parties_involved.length > 3 && (
                    <Chip label={`+${analysis.document_analysis.summary.parties_involved.length - 3} more`} size="small" />
                  )}
                </Stack>
              </Box>
              
              <Box>
                <Typography variant="subtitle2" gutterBottom>
                  <GavelIcon fontSize="small" sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Key Themes
                </Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap">
                  {analysis.document_analysis.summary.themes.slice(0, 5).map((theme, index) => (
                    <Chip key={index} label={theme} size="small" color="primary" variant="outlined" />
                  ))}
                </Stack>
              </Box>
            </Box>
            
            <Box flex={1}>
              <Typography variant="h6" gutterBottom>
                Risk Factors
              </Typography>
              {analysis.document_analysis.summary.potential_risks.length > 0 ? (
                <List>
                  {analysis.document_analysis.summary.potential_risks.map((risk, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <WarningIcon color="warning" />
                      </ListItemIcon>
                      <ListItemText primary={risk} />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Alert severity="success">
                  No significant risks identified in document analysis
                </Alert>
              )}
            </Box>
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* Research Analysis */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box display="flex" alignItems="center">
            <ResearchIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6">Research & Precedents</Typography>
            <Chip 
              label={`${analysis.research_analysis.total_found} items found`}
              size="small"
              sx={{ ml: 2 }}
            />
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={3}>
            <Box flex={2}>
              <Typography variant="h6" gutterBottom>
                Most Relevant Research
              </Typography>
              <List>
                {analysis.research_analysis.top_relevant.slice(0, 5).map((item, index) => (
                  <ListItem key={index} divider={index < 4}>
                    <ListItemText
                      primary={item.title}
                      secondary={
                        <Box>
                          <Typography variant="caption" color="text.secondary">
                            Category: {item.category} • Relevance: {Math.round(item.relevance_score * 100)}%
                          </Typography>
                          <Typography variant="caption" color="text.secondary" display="block">
                            {item.description}
                          </Typography>
                        </Box>
                      }
                    />
                    <Chip 
                      label={`${Math.round(item.relevance_score * 100)}%`}
                      size="small"
                      color={item.relevance_score > 0.7 ? 'success' : item.relevance_score > 0.4 ? 'warning' : 'default'}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
            
            <Box flex={1}>
              <Typography variant="h6" gutterBottom>
                Research Categories
              </Typography>
              <Stack spacing={2}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Precedents
                  </Typography>
                  <Chip 
                    label={analysis.research_analysis.categorized.precedents.length}
                    size="small"
                    color="primary"
                  />
                </Paper>
                
                <Paper sx={{ p: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Statutes
                  </Typography>
                  <Chip 
                    label={analysis.research_analysis.categorized.statutes.length}
                    size="small"
                    color="secondary"
                  />
                </Paper>
                
                <Paper sx={{ p: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Contracts
                  </Typography>
                  <Chip 
                    label={analysis.research_analysis.categorized.contracts.length}
                    size="small"
                    color="info"
                  />
                </Paper>
              </Stack>
            </Box>
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* Playbook Analysis */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box display="flex" alignItems="center">
            <PlaybookIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6">Playbook Strategy</Typography>
            <Chip 
              label={analysis.playbook_analysis.playbook_name}
              size="small"
              sx={{ ml: 2 }}
            />
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={3}>
            <Box flex={1}>
              <Typography variant="h6" gutterBottom>
                Decision Path
              </Typography>
              <Alert severity="info" sx={{ mb: 3 }}>
                {analysis.playbook_analysis.decision_path.result}
              </Alert>
              
              <Typography variant="subtitle2" gutterBottom>
                Recommended Actions:
              </Typography>
              <List>
                {analysis.playbook_analysis.decision_path.recommended_actions.map((action, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <TrendingUpIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary={action} />
                  </ListItem>
                ))}
              </List>
            </Box>
            
            <Box flex={1}>
              <Typography variant="h6" gutterBottom>
                Monetary Assessment
              </Typography>
              <Paper sx={{ p: 2, mb: 3 }}>
                <Box display="flex" alignItems="center" mb={2}>
                  <MoneyIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">
                    {formatCurrency(analysis.playbook_analysis.monetary_assessment.range[0])} - {formatCurrency(analysis.playbook_analysis.monetary_assessment.range[1])}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {analysis.playbook_analysis.monetary_assessment.description}
                </Typography>
                
                <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                  Key Factors:
                </Typography>
                <List dense>
                  {analysis.playbook_analysis.monetary_assessment.factors.map((factor, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={factor} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
              
              <Typography variant="subtitle2" gutterBottom>
                Applicable Rules ({analysis.playbook_analysis.applicable_rules.length}):
              </Typography>
              <List dense>
                {analysis.playbook_analysis.applicable_rules.slice(0, 3).map((rule, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={rule.description}
                      secondary={`Legal Basis: ${rule.legal_basis}`}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          </Box>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default IntegratedCaseAnalysis;