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
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Button,
  Paper,
  Grid
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Gavel as LegalIcon
} from '@mui/icons-material';
import { Playbook, PlaybookResult } from '../../types/api';


interface PlaybookViewerProps {
  caseType: string;
  caseId?: string;
  showAppliedRules?: boolean;
  showHeader?: boolean;
}

const PlaybookViewer = ({ caseType, caseId, showAppliedRules = false, showHeader = true }: PlaybookViewerProps) => {
  const [playbook, setPlaybook] = useState<Playbook | null>(null);
  const [appliedRules, setAppliedRules] = useState<PlaybookResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedRules, setExpandedRules] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetchPlaybookData();
  }, [caseType, caseId]);

  const fetchPlaybookData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch playbook for case type
      const playbookResponse = await fetch(`http://localhost:8000/api/playbooks/${encodeURIComponent(caseType)}`);
      if (!playbookResponse.ok) {
        throw new Error('Failed to fetch playbook');
      }
      const playbookData = await playbookResponse.json();
      setPlaybook(playbookData);

      // Fetch applied rules if case ID is provided and showAppliedRules is true
      if (caseId && showAppliedRules) {
        try {
          const rulesResponse = await fetch(`http://localhost:8000/api/playbooks/cases/${caseId}/applied-rules`);
          if (rulesResponse.ok) {
            const rulesData = await rulesResponse.json();
            setAppliedRules(rulesData);
          }
        } catch (err) {
          console.warn('Could not fetch applied rules:', err);
        }
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch playbook data');
    } finally {
      setLoading(false);
    }
  };

  const toggleRuleExpansion = (ruleId: string) => {
    const newExpanded = new Set(expandedRules);
    if (newExpanded.has(ruleId)) {
      newExpanded.delete(ruleId);
    } else {
      newExpanded.add(ruleId);
    }
    setExpandedRules(newExpanded);
  };

  const isRuleApplied = (ruleId: string) => {
    return appliedRules?.applied_rules?.includes(ruleId) || false;
  };



  if (loading) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="300px">
        <CircularProgress sx={{ mb: 2 }} />
        <Typography variant="body1">Loading playbook...</Typography>
      </Box>
    );
  }

  if (error || !playbook) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        <Typography variant="body1" gutterBottom>
          Error: {error || 'Playbook not found'}
        </Typography>
        <Button variant="outlined" onClick={fetchPlaybookData} size="small">
          Retry
        </Button>
      </Alert>
    );
  }

  return (
    <Box>
      {/* Playbook Header */}
      {showHeader && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <LegalIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h4" component="h2">
                {playbook.name}
              </Typography>
            </Box>
            <Typography variant="body1" color="text.secondary" paragraph>
              {playbook.description}
            </Typography>
            <Box display="flex" gap={1}>
              <Chip label={caseType} color="primary" variant="outlined" />
              <Chip label={`${playbook.rules?.length || 0} Rules`} variant="outlined" />
            </Box>
          </CardContent>
        </Card>
      )}

      {showAppliedRules && appliedRules && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Applied to Current Case
            </Typography>
            <Grid container spacing={2} sx={{ mb: 2 }}>
              <Grid item xs={12} sm={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Case Strength
                  </Typography>
                  <Chip
                    label={appliedRules.case_strength || 'Unknown'}
                    color={appliedRules.case_strength === 'Strong' ? 'success' :
                      appliedRules.case_strength === 'Moderate' ? 'warning' : 'error'}
                    sx={{ mt: 1 }}
                  />
                </Paper>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Applied Rules
                  </Typography>
                  <Typography variant="h6" sx={{ mt: 1 }}>
                    {appliedRules.applied_rules?.length || 0}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Recommendations
                  </Typography>
                  <Typography variant="h6" sx={{ mt: 1 }}>
                    {appliedRules.recommendations?.length || 0}
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
            {appliedRules.reasoning && (
              <Paper sx={{ p: 2, backgroundColor: 'grey.50' }}>
                <Typography variant="h6" gutterBottom>
                  AI Reasoning
                </Typography>
                <Typography variant="body2">
                  {appliedRules.reasoning}
                </Typography>
              </Paper>
            )}
          </CardContent>
        </Card>
      )}

      {/* Decision Rules */}
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Decision Rules
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Rules and conditions that guide case assessment and recommendations
          </Typography>
          <Divider sx={{ mb: 2 }} />

          {playbook.rules && playbook.rules.length > 0 ? (
            <Box>
              {playbook.rules.map((rule) => (
                <Accordion
                  key={rule.id}
                  expanded={expandedRules.has(rule.id)}
                  onChange={() => toggleRuleExpansion(rule.id)}
                  sx={{
                    mb: 1,
                    border: isRuleApplied(rule.id) ? '2px solid' : '1px solid',
                    borderColor: isRuleApplied(rule.id) ? 'success.main' : 'divider',
                    opacity: (rule.enabled !== false) ? 1 : 0.6
                  }}
                >
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box display="flex" justifyContent="space-between" alignItems="center" width="100%">
                      <Box display="flex" alignItems="center" gap={1} flex={1}>
                        <Typography variant="subtitle1" fontWeight="bold">
                          {rule.description || rule.id}
                        </Typography>
                        {isRuleApplied(rule.id) && (
                          <Chip
                            label="Applied"
                            size="small"
                            color="success"
                            icon={<CheckIcon />}
                          />
                        )}
                      </Box>
                      <Box display="flex" gap={1} mr={2}>
                        <Chip
                          label={`Priority: ${(rule.weight || rule.priority || 0) >= 0.8 ? 'High' : (rule.weight || rule.priority || 0) >= 0.5 ? 'Medium' : 'Low'}`}
                          size="small"
                          color={(rule.weight || rule.priority || 0) >= 0.8 ? 'error' : (rule.weight || rule.priority || 0) >= 0.5 ? 'warning' : 'default'}
                          variant="outlined"
                        />
                        <Chip
                          label={(rule.enabled !== false) ? 'Active' : 'Inactive'}
                          size="small"
                          color={(rule.enabled !== false) ? 'success' : 'default'}
                          variant="outlined"
                        />
                      </Box>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                      <Box>
                        <Typography variant="h6" gutterBottom>
                          Recommended Action
                        </Typography>
                        <Typography variant="body2">
                          {rule.action.replace(/_/g, ' ').replace(/([a-z])([A-Z])/g, '$1 $2')}
                        </Typography>
                      </Box>
                      {(rule as any).legal_basis && (
                        <Box>
                          <Typography variant="h6" gutterBottom>
                            Legal Basis
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {(rule as any).legal_basis}
                          </Typography>
                        </Box>
                      )}
                      <Divider sx={{ my: 1 }} />
                      <Typography variant="caption" color="text.secondary">
                        Rule ID: {rule.id}
                      </Typography>
                    </Box>
                  </AccordionDetails>
                </Accordion>
              ))}
            </Box>
          ) : (
            <Alert severity="info">
              No rules defined for this playbook.
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Monetary Assessment Ranges */}
      {playbook.monetary_ranges && Object.keys(playbook.monetary_ranges).length > 0 && (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Monetary Assessment Ranges
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Expected value ranges based on case strength
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <Grid container spacing={2}>
              {Object.entries(playbook.monetary_ranges).map(([strength, data]: [string, any]) => (
                <Grid item xs={12} sm={4} key={strength}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h6" gutterBottom sx={{ textTransform: 'capitalize' }}>
                      {strength} Cases
                    </Typography>
                    {data.range && (
                      <Typography variant="h5" color="primary" gutterBottom>
                        £{data.range[0]?.toLocaleString()} - £{data.range[1]?.toLocaleString()}
                      </Typography>
                    )}
                    {data.description && (
                      <Typography variant="body2" color="text.secondary">
                        {data.description}
                      </Typography>
                    )}
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Escalation Paths */}
      {playbook.escalation_paths && playbook.escalation_paths.length > 0 && (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Escalation Procedures
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Recommended escalation steps for different scenarios
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {playbook.escalation_paths.map((path: any, index: number) => (
                <Paper key={index} sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Chip
                    label={`Step ${index + 1}`}
                    color="primary"
                    sx={{ minWidth: 80 }}
                  />
                  <Typography variant="body1">
                    {typeof path === 'string' ? path : path.action || path.description}
                  </Typography>
                </Paper>
              ))}
            </Box>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default PlaybookViewer;