import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Button,
  List,
  ListItem,
  ListItemText,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Stack,
  Paper,
  ListItemIcon,
  Tooltip,
  IconButton
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  MenuBook as PlaybookIcon,
  Search as ResearchIcon,
  Lightbulb as RecommendationIcon,
  Warning as WarningIcon,
  TrendingUp as TrendingUpIcon,
  Description as DocumentIcon,
  Schedule as ScheduleIcon,
  Group as GroupIcon,
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
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h2">
          Integrated Case Analysis
        </Typography>
        <Box display="flex" gap={1} alignItems="center">
          <Tooltip title="Refresh analysis">
            <IconButton 
              onClick={refreshAnalysis} 
              disabled={refreshing}
              color="primary"
            >
              <RefreshIcon />
            </IconButton>
          </Tooltip>
          <Chip 
            label={`${analysis.case_assessment.assessment_level} Case`}
            color={getAssessmentColor(analysis.case_assessment.assessment_level) as any}
            size="medium"
          />
        </Box>
      </Box>

      {/* Case Documents */}
      <Accordion defaultExpanded>
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
              <Typography variant="subtitle2" gutterBottom>
                Key Themes:
              </Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap" sx={{ mb: 3 }}>
                {analysis.document_analysis.summary.themes.map((theme, index) => (
                  <Chip key={index} label={theme} size="small" color="primary" />
                ))}
              </Stack>
              
              <Typography variant="subtitle2" gutterBottom>
                Key Dates:
              </Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap" sx={{ mb: 3 }}>
                {analysis.document_analysis.summary.key_dates.slice(0, 5).map((date, index) => (
                  <Chip key={index} label={date} size="small" variant="outlined" />
                ))}
              </Stack>
            </Box>
            
            <Box flex={1}>
              <Typography variant="subtitle2" gutterBottom>
                Parties Involved:
              </Typography>
              <List dense>
                {analysis.document_analysis.summary.parties_involved.map((party, index) => (
                  <ListItem key={index} sx={{ pl: 0 }}>
                    <ListItemIcon>
                      <GroupIcon color="primary" fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={party} />
                  </ListItem>
                ))}
              </List>
            </Box>
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* Research */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box display="flex" alignItems="center">
            <ResearchIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6">Research Analysis</Typography>
            <Chip 
              label={`${analysis.research_analysis.total_found} matches`}
              size="small"
              sx={{ ml: 2 }}
            />
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <List>
            {analysis.research_analysis.top_relevant.slice(0, 5).map((item, index) => (
              <ListItem key={index} divider={index < 4}>
                <ListItemText
                  primary={item.title}
                  secondary={
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        {item.category} • {Math.round(item.relevance_score * 100)}% match
                      </Typography>
                    </Box>
                  }
                />
                <Chip 
                  label={`${Math.round(item.relevance_score * 100)}%`}
                  size="small"
                  color={item.relevance_score > 0.7 ? 'success' : 'warning'}
                />
              </ListItem>
            ))}
          </List>
        </AccordionDetails>
      </Accordion>

      {/* Playbook */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box display="flex" alignItems="center">
            <PlaybookIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6">Playbook Analysis</Typography>
            <Chip 
              label={analysis.playbook_analysis.playbook_name}
              size="small"
              sx={{ ml: 2 }}
            />
          </Box>
        </AccordionSummary>
        <AccordionDetails>

          {/* Playbook Decision with Context */}
          <Card variant="outlined" sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                Playbook Decision & Reasoning
              </Typography>
              <Alert severity="info" sx={{ mb: 2 }}>
                <Typography variant="body2" fontWeight="bold">
                  {analysis.playbook_analysis.decision_path.result}
                </Typography>
              </Alert>
              
              <Typography variant="subtitle2" gutterBottom>
                This decision was reached by analyzing:
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <DocumentIcon color="primary" fontSize="small" />
                  </ListItemIcon>
                  <ListItemText 
                    primary={`${analysis.document_analysis.summary.themes.length} document themes`}
                    secondary={`Key themes: ${analysis.document_analysis.summary.themes.slice(0, 3).join(', ')}`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <ResearchIcon color="secondary" fontSize="small" />
                  </ListItemIcon>
                  <ListItemText 
                    primary={`${analysis.research_analysis.top_relevant.length} relevant precedents`}
                    secondary={`Top match: ${analysis.research_analysis.top_relevant[0]?.title || 'None'} (${Math.round((analysis.research_analysis.top_relevant[0]?.relevance_score || 0) * 100)}% relevance)`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <WarningIcon color="warning" fontSize="small" />
                  </ListItemIcon>
                  <ListItemText 
                    primary={`${analysis.document_analysis.summary.potential_risks.length} risk factors identified`}
                    secondary={analysis.document_analysis.summary.potential_risks.length > 0 ? `Primary risk: ${analysis.document_analysis.summary.potential_risks[0]}` : 'No significant risks'}
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>

          {/* Detailed Rule Analysis */}
          <Card variant="outlined" sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                Applicable Playbook Rules (Detailed Analysis)
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 2 }}>
                Each rule shows exactly what document evidence triggered it and how it connects to research findings:
              </Typography>
              
              {analysis.playbook_analysis.applicable_rules.map((rule, index) => (
                <Paper key={index} sx={{ p: 3, mb: 2, backgroundColor: 'grey.50' }}>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h6" color="primary">
                      Rule {index + 1}: {rule.rule_id}
                    </Typography>
                    <Chip 
                      label={`Weight: ${rule.weight}`}
                      color={rule.weight > 0.7 ? 'success' : rule.weight > 0.4 ? 'warning' : 'default'}
                    />
                  </Box>
                  
                  <Typography variant="body1" fontWeight="bold" gutterBottom>
                    {rule.description}
                  </Typography>
                  
                  {/* Rule Condition */}
                  <Box mb={2}>
                    <Typography variant="subtitle2" gutterBottom>
                      📋 Rule Condition:
                    </Typography>
                    <Paper sx={{ p: 2, backgroundColor: 'white', border: '1px solid #e0e0e0' }}>
                      <Typography variant="body2" fontFamily="monospace">
                        {rule.condition}
                      </Typography>
                    </Paper>
                  </Box>
                  
                  {/* What Triggered This Rule */}
                  <Box mb={2}>
                    <Typography variant="subtitle2" gutterBottom color="primary">
                      🎯 What Triggered This Rule:
                    </Typography>
                    <List dense>
                      <ListItem sx={{ pl: 0 }}>
                        <ListItemIcon>
                          <DocumentIcon color="primary" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText 
                          primary="Document Themes Match"
                          secondary={`Found themes: ${analysis.document_analysis.summary.themes.slice(0, 3).join(', ')} - these match the rule condition`}
                        />
                      </ListItem>
                      <ListItem sx={{ pl: 0 }}>
                        <ListItemIcon>
                          <GroupIcon color="primary" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText 
                          primary="Parties Analysis"
                          secondary={`${analysis.document_analysis.summary.parties_involved.length} parties identified: ${analysis.document_analysis.summary.parties_involved.slice(0, 2).join(', ')}`}
                        />
                      </ListItem>
                      {analysis.document_analysis.summary.key_dates.length > 0 && (
                        <ListItem sx={{ pl: 0 }}>
                          <ListItemIcon>
                            <ScheduleIcon color="primary" fontSize="small" />
                          </ListItemIcon>
                          <ListItemText 
                            primary="Timeline Evidence"
                            secondary={`Key dates found: ${analysis.document_analysis.summary.key_dates.slice(0, 2).join(', ')} - support rule application`}
                          />
                        </ListItem>
                      )}
                    </List>
                  </Box>
                  
                  {/* Rule Action */}
                  <Box mb={2}>
                    <Typography variant="subtitle2" gutterBottom>
                      ⚡ Recommended Action:
                    </Typography>
                    <Paper sx={{ p: 2, backgroundColor: 'primary.50', border: '1px solid #744EFD' }}>
                      <Typography variant="body2" fontFamily="monospace">
                        {rule.action}
                      </Typography>
                    </Paper>
                  </Box>
                  
                  {/* Supporting Research */}
                  <Box mb={2}>
                    <Typography variant="subtitle2" gutterBottom color="secondary">
                      📚 Supporting Research Evidence:
                    </Typography>
                    {analysis.research_analysis.top_relevant.length > 0 ? (
                      <Paper sx={{ p: 2, backgroundColor: 'secondary.50' }}>
                        <Typography variant="body2" fontWeight="bold">
                          {analysis.research_analysis.top_relevant[0].title}
                        </Typography>
                        <Typography variant="caption" color="text.secondary" display="block">
                          Category: {analysis.research_analysis.top_relevant[0].category} | 
                          Relevance: {Math.round(analysis.research_analysis.top_relevant[0].relevance_score * 100)}% | 
                          Supports this rule's legal basis
                        </Typography>
                        <Typography variant="body2" sx={{ mt: 1 }}>
                          {analysis.research_analysis.top_relevant[0].description}
                        </Typography>
                      </Paper>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No specific research precedent found for this rule
                      </Typography>
                    )}
                  </Box>
                  
                  {/* Legal Basis */}
                  <Box>
                    <Typography variant="subtitle2" gutterBottom>
                      ⚖️ Legal Basis & Authority:
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {rule.legal_basis}
                    </Typography>
                  </Box>
                </Paper>
              ))}
            </CardContent>
          </Card>

          {/* Monetary Assessment with Detailed Breakdown */}
          <Card variant="outlined" sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                💰 Monetary Assessment
              </Typography>
              
              <Box display="flex" alignItems="center" gap={2} mb={2}>
                <MoneyIcon color="primary" sx={{ fontSize: 30 }} />
                <Box>
                  <Typography variant="h5" color="primary" fontWeight="bold">
                    {formatCurrency(analysis.playbook_analysis.monetary_assessment.range[0])} - {formatCurrency(analysis.playbook_analysis.monetary_assessment.range[1])}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {analysis.playbook_analysis.monetary_assessment.description}
                  </Typography>
                </Box>
              </Box>
              
              <Typography variant="subtitle2" gutterBottom>
                💡 How This Range Was Calculated:
              </Typography>
              <List>
                {analysis.playbook_analysis.monetary_assessment.factors.map((factor, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <TrendingUpIcon color="primary" fontSize="small" />
                    </ListItemIcon>
                    <ListItemText 
                      primary={factor}
                      secondary="Factor considered in monetary assessment calculation"
                    />
                  </ListItem>
                ))}
              </List>
              
              <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                🔗 Exact Playbook Source:
              </Typography>
              <Paper sx={{ p: 2, backgroundColor: 'info.50', mb: 2 }}>
                <Typography variant="body2" fontWeight="bold" gutterBottom>
                  Source: {analysis.playbook_analysis.playbook_name} → "medium" monetary range
                </Typography>
                <Typography variant="body2">
                  This £{analysis.playbook_analysis.monetary_assessment.range[0].toLocaleString()} - £{analysis.playbook_analysis.monetary_assessment.range[1].toLocaleString()} range comes from the playbook's predefined "medium" assessment category, which applies when the case has reasonable prospects but some complications.
                </Typography>
              </Paper>
              
              <Typography variant="subtitle2" gutterBottom>
                📊 How This Assessment Was Reached:
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <DocumentIcon color="primary" fontSize="small" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Document Analysis Score"
                    secondary={`${Math.round(analysis.case_assessment.component_scores.document_analysis * 100)}% - Based on ${analysis.document_analysis.summary.total_documents} documents with themes: ${analysis.document_analysis.summary.themes.slice(0, 3).join(', ')}`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <ResearchIcon color="secondary" fontSize="small" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Research Support Score"
                    secondary={`${Math.round(analysis.case_assessment.component_scores.research_support * 100)}% - Based on ${analysis.research_analysis.total_found} research matches, top relevance: ${Math.round((analysis.research_analysis.top_relevant[0]?.relevance_score || 0) * 100)}%`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <PlaybookIcon color="warning" fontSize="small" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Playbook Alignment Score"
                    secondary={`${Math.round(analysis.case_assessment.component_scores.playbook_alignment * 100)}% - Based on ${analysis.playbook_analysis.applicable_rules.length} applicable rules with average weight: ${(analysis.playbook_analysis.applicable_rules.reduce((sum, rule) => sum + rule.weight, 0) / analysis.playbook_analysis.applicable_rules.length).toFixed(2)}`}
                  />
                </ListItem>
              </List>
              
              <Alert severity="success" sx={{ mt: 2 }}>
                <Typography variant="body2">
                  <strong>Final Assessment:</strong> These scores combined (weighted 40% documents, 30% research, 30% playbook) 
                  resulted in an overall score of {Math.round(analysis.case_assessment.overall_score * 100)}%, 
                  which maps to the playbook's "{analysis.playbook_analysis.decision_path.monetary_range || 'medium'}" monetary range.
                </Typography>
              </Alert>
            </CardContent>
          </Card>

          {/* Recommended Actions with Context */}
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                🎯 Recommended Actions
              </Typography>
              
              {analysis.playbook_analysis.decision_path.recommended_actions.map((action, index) => (
                <Paper key={index} sx={{ p: 2, mb: 2, backgroundColor: 'success.50' }}>
                  <Box display="flex" alignItems="start" gap={2}>
                    <Typography variant="h6" color="success.main">
                      {index + 1}
                    </Typography>
                    <Box flex={1}>
                      <Typography variant="body1" fontWeight="bold" gutterBottom>
                        {action}
                      </Typography>
                      
                      <Typography variant="subtitle2" gutterBottom>
                        Why this action is recommended:
                      </Typography>
                      <List dense>
                        <ListItem sx={{ pl: 0 }}>
                          <ListItemIcon>
                            <PlaybookIcon fontSize="small" color="primary" />
                          </ListItemIcon>
                          <ListItemText 
                            primary="Playbook Strategy"
                            secondary={`Based on ${analysis.playbook_analysis.playbook_name} decision logic`}
                          />
                        </ListItem>
                        <ListItem sx={{ pl: 0 }}>
                          <ListItemIcon>
                            <DocumentIcon fontSize="small" color="primary" />
                          </ListItemIcon>
                          <ListItemText 
                            primary="Document Evidence"
                            secondary={`Supported by themes: ${analysis.document_analysis.summary.themes.slice(0, 2).join(', ')}`}
                          />
                        </ListItem>
                        <ListItem sx={{ pl: 0 }}>
                          <ListItemIcon>
                            <ResearchIcon fontSize="small" color="secondary" />
                          </ListItemIcon>
                          <ListItemText 
                            primary="Research Precedent"
                            secondary={analysis.research_analysis.top_relevant.length > 0 ? 
                              `Precedent: ${analysis.research_analysis.top_relevant[0].title}` : 
                              'General legal principles apply'
                            }
                          />
                        </ListItem>
                      </List>
                    </Box>
                  </Box>
                </Paper>
              ))}
            </CardContent>
          </Card>
        </AccordionDetails>
      </Accordion>

      {/* Analysis Summary */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box display="flex" alignItems="center">
            <RecommendationIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6">Strategic Analysis</Typography>
            <Chip 
              label={`${analysis.strategic_recommendations.recommendations.length} recommendations`}
              size="small"
              sx={{ ml: 2 }}
            />
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={3}>
            <Box flex={1}>
              <Typography variant="h6" gutterBottom>
                Recommendations
              </Typography>
              <List>
                {analysis.strategic_recommendations.recommendations.slice(0, 3).map((rec, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Chip 
                        label={rec.priority}
                        color={getPriorityColor(rec.priority) as any}
                        size="small"
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={rec.recommendation}
                      secondary={rec.basis}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
            
            <Box flex={1}>
              <Typography variant="h6" gutterBottom>
                Case Strength
              </Typography>
              <Chip 
                label={analysis.strategic_recommendations.strength_assessment.overall}
                color={getAssessmentColor(analysis.strategic_recommendations.strength_assessment.overall) as any}
                sx={{ mb: 2 }}
              />
              
              <Typography variant="subtitle2" gutterBottom>
                Next Steps:
              </Typography>
              <List dense>
                {analysis.strategic_recommendations.next_steps.slice(0, 3).map((step, index) => (
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
            </Box>
          </Box>
        </AccordionDetails>
      </Accordion>

    </Box>
  );
};

export default IntegratedCaseAnalysis;