import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Divider,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField
} from '@mui/material';
import {
  AccountTree as PlaybookTreeIcon,
  Psychology as ClaudeIcon,
  CheckCircle as CompletedIcon,
  RadioButtonUnchecked as PendingIcon,
  PlayArrow as StartIcon,
  Lightbulb as RecommendationIcon
} from '@mui/icons-material';
import { 
  Playbook, 
  ClaudePlaybookSession, 
  PlaybookDecisionTree, 
  PlaybookDecisionTracking,
  FinalRecommendations,
  DecisionNode
} from '../../../types/api';
import { apiClient } from '../../../services/api';

interface PlaybookDecisionTabProps {
  caseId: string;
  playbookId: string;
}

const PlaybookDecisionTab: React.FC<PlaybookDecisionTabProps> = ({ caseId, playbookId }) => {
  const [playbook, setPlaybook] = useState<Playbook | null>(null);
  const [claudeSession, setClaudeSession] = useState<ClaudePlaybookSession | null>(null);
  const [decisionTree, setDecisionTree] = useState<PlaybookDecisionTree | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentDecision, setCurrentDecision] = useState<DecisionNode | null>(null);
  const [decisionDialogOpen, setDecisionDialogOpen] = useState(false);
  const [decisionRationale, setDecisionRationale] = useState('');
  const [selectedOption, setSelectedOption] = useState('');
  const [processingDecision, setProcessingDecision] = useState(false);

  useEffect(() => {
    loadPlaybookData();
  }, [caseId, playbookId]);

  const loadPlaybookData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load playbook details
      const playbookResponse = await apiClient.get<Playbook>(`/api/playbooks/${playbookId}`);
      setPlaybook(playbookResponse.data);

      // Try to load existing Claude session
      try {
        const sessionResponse = await apiClient.get<ClaudePlaybookSession>(`/api/cases/${caseId}/claude-playbook-session`);
        setClaudeSession(sessionResponse.data);
        
        // Load decision tree
        const treeResponse = await apiClient.get<PlaybookDecisionTree>(`/api/cases/${caseId}/playbook-decision-tree`);
        setDecisionTree(treeResponse.data);
        
        // Set current decision if session is active
        if (sessionResponse.data.session_status === 'Active') {
          const currentNode = treeResponse.data.nodes[sessionResponse.data.current_decision_node];
          setCurrentDecision(currentNode);
        }
      } catch (sessionErr: any) {
        if (sessionErr.response?.status === 404) {
          // No session exists yet
          setClaudeSession(null);
          setDecisionTree(null);
        } else {
          throw sessionErr;
        }
      }
    } catch (err) {
      console.error('Failed to load playbook data:', err);
      setError('Failed to load playbook data');
    } finally {
      setLoading(false);
    }
  };

  const startClaudeSession = async () => {
    try {
      setError(null);
      
      // Create new Claude playbook session
      const response = await apiClient.post<ClaudePlaybookSession>(`/api/cases/${caseId}/claude-playbook-session`, {
        playbook_id: playbookId
      });
      
      setClaudeSession(response.data);
      
      // Load the decision tree
      const treeResponse = await apiClient.get<PlaybookDecisionTree>(`/api/cases/${caseId}/playbook-decision-tree`);
      setDecisionTree(treeResponse.data);
      
      // Set the first decision
      const firstNode = treeResponse.data.nodes[treeResponse.data.root_node];
      setCurrentDecision(firstNode);
      
    } catch (err) {
      console.error('Failed to start Claude session:', err);
      setError('Failed to start Claude playbook session');
    }
  };

  const openDecisionDialog = (option: string) => {
    setSelectedOption(option);
    setDecisionRationale('');
    setDecisionDialogOpen(true);
  };

  const submitDecision = async () => {
    if (!currentDecision || !claudeSession || !selectedOption) return;

    try {
      setProcessingDecision(true);
      
      const decision: PlaybookDecisionTracking = {
        decision_node_id: currentDecision.id,
        decision_question: currentDecision.question,
        research_items_consulted: currentDecision.research_context,
        supporting_evidence: [], // This would be populated by Claude
        decision_rationale: decisionRationale,
        confidence_level: 0.8, // This would be determined by Claude
        next_decision_node: currentDecision.options[selectedOption]
      };

      const response = await apiClient.put<ClaudePlaybookSession>(
        `/api/claude-sessions/${claudeSession.session_id}/decision`,
        decision
      );

      setClaudeSession(response.data);
      
      // Update decision tree
      if (decisionTree) {
        const updatedTree = {
          ...decisionTree,
          current_path: [...decisionTree.current_path, currentDecision.id],
          completed_decisions: [...decisionTree.completed_decisions, decision]
        };
        setDecisionTree(updatedTree);
      }

      // Move to next decision or complete
      if (decision.next_decision_node && decisionTree?.nodes[decision.next_decision_node]) {
        setCurrentDecision(decisionTree.nodes[decision.next_decision_node]);
      } else {
        // Session completed
        setCurrentDecision(null);
      }

      setDecisionDialogOpen(false);
      setSelectedOption('');
      setDecisionRationale('');
      
    } catch (err) {
      console.error('Failed to submit decision:', err);
      setError('Failed to submit decision');
    } finally {
      setProcessingDecision(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
        <Button onClick={loadPlaybookData} sx={{ ml: 2 }}>
          Retry
        </Button>
      </Alert>
    );
  }

  if (!playbook) {
    return (
      <Alert severity="warning">
        Playbook not found
      </Alert>
    );
  }

  // No Claude session started yet
  if (!claudeSession) {
    return (
      <Card sx={{ mb: 4 }} data-testid="playbook-start-prompt">
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <PlaybookTreeIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h5" component="h2">
              Playbook Decision Tree
            </Typography>
          </Box>
          <Divider sx={{ mb: 3 }} />

          <Box textAlign="center" py={4}>
            <ClaudeIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {playbook.name}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3, maxWidth: 600, mx: 'auto' }}>
              Start a Claude-driven playbook decision session to systematically work through 
              the decision tree with AI assistance. Claude will help make informed decisions 
              based on case research and legal analysis.
            </Typography>
            <Button
              variant="contained"
              size="large"
              onClick={startClaudeSession}
              startIcon={<StartIcon />}
            >
              Start Claude Decision Session
            </Button>
          </Box>
        </CardContent>
      </Card>
    );
  }

  // Session completed - show final recommendations
  if (claudeSession.session_status === 'Completed' && claudeSession.final_recommendations) {
    return (
      <Box data-testid="playbook-final-recommendations">
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <RecommendationIcon color="success" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                Final Recommendations
              </Typography>
            </Box>
            <Divider sx={{ mb: 3 }} />

            <Typography variant="h6" gutterBottom>
              Overall Assessment
            </Typography>
            <Typography variant="body1" sx={{ mb: 3 }}>
              {claudeSession.final_recommendations.overall_assessment}
            </Typography>

            <Typography variant="h6" gutterBottom>
              Strategic Recommendations
            </Typography>
            <List>
              {claudeSession.final_recommendations.strategic_recommendations.map((rec, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`• ${rec}`} />
                </ListItem>
              ))}
            </List>

            <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
              Risk Assessment
            </Typography>
            <Chip
              label={`Risk Level: ${claudeSession.final_recommendations.risk_assessment.overall_risk_level}`}
              color={
                claudeSession.final_recommendations.risk_assessment.overall_risk_level === 'High' ? 'error' :
                claudeSession.final_recommendations.risk_assessment.overall_risk_level === 'Medium' ? 'warning' : 'success'
              }
              sx={{ mb: 2 }}
            />
            <List>
              {claudeSession.final_recommendations.risk_assessment.risk_factors.map((factor, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`• ${factor}`} />
                </ListItem>
              ))}
            </List>

            <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
              Next Steps
            </Typography>
            <List>
              {claudeSession.final_recommendations.next_steps.map((step, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`${index + 1}. ${step}`} />
                </ListItem>
              ))}
            </List>

            <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
              Decision Path Taken
            </Typography>
            <Stack direction="row" spacing={1} flexWrap="wrap">
              {claudeSession.final_recommendations.decision_path.map((node, index) => (
                <Chip
                  key={index}
                  label={node}
                  variant="outlined"
                  size="small"
                />
              ))}
            </Stack>
          </CardContent>
        </Card>
      </Box>
    );
  }

  // Active session - show decision tree and current decision
  return (
    <Box data-testid="playbook-decision-interface">
      {/* Decision Progress */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="between" mb={2}>
            <Box display="flex" alignItems="center">
              <PlaybookTreeIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                {playbook.name}
              </Typography>
            </Box>
            <Chip
              label={`${claudeSession.decision_history.length} decisions made`}
              color="primary"
              size="small"
            />
          </Box>
          <Divider sx={{ mb: 3 }} />

          {/* Decision History */}
          {claudeSession.decision_history.length > 0 && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Decision History
              </Typography>
              <Stepper orientation="vertical">
                {claudeSession.decision_history.map((decision, index) => (
                  <Step key={decision.decision_node_id} active={true} completed={true}>
                    <StepLabel icon={<CompletedIcon color="success" />}>
                      {decision.decision_question}
                    </StepLabel>
                    <StepContent>
                      <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Rationale:</strong> {decision.decision_rationale}
                        </Typography>
                        <Chip
                          label={`${Math.round(decision.confidence_level * 100)}% confidence`}
                          color={decision.confidence_level >= 0.8 ? 'success' : decision.confidence_level >= 0.6 ? 'warning' : 'error'}
                          size="small"
                        />
                      </Paper>
                    </StepContent>
                  </Step>
                ))}
              </Stepper>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Current Decision */}
      {currentDecision && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <ClaudeIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6">
                Current Decision
              </Typography>
            </Box>
            <Divider sx={{ mb: 3 }} />

            <Typography variant="h6" gutterBottom>
              {currentDecision.question}
            </Typography>

            {currentDecision.research_context.length > 0 && (
              <Box sx={{ mb: 3, p: 2, bgcolor: 'info.light', borderRadius: 1 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Relevant Research Context:
                </Typography>
                <List dense>
                  {currentDecision.research_context.map((context, index) => (
                    <ListItem key={index} sx={{ py: 0.5, pl: 2 }}>
                      <Typography variant="body2">• {context}</Typography>
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            <Typography variant="subtitle2" gutterBottom sx={{ mt: 3 }}>
              Available Options:
            </Typography>
            <Stack spacing={2}>
              {Object.entries(currentDecision.options).map(([option, nextNode]) => (
                <Button
                  key={option}
                  variant="outlined"
                  fullWidth
                  onClick={() => openDecisionDialog(option)}
                  sx={{ justifyContent: 'flex-start', textAlign: 'left' }}
                >
                  {option}
                </Button>
              ))}
            </Stack>
          </CardContent>
        </Card>
      )}

      {/* Decision Dialog */}
      <Dialog
        open={decisionDialogOpen}
        onClose={() => setDecisionDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Make Decision: {selectedOption}
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Provide the rationale for choosing this option. This will be recorded as part of the decision history.
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Decision Rationale"
            value={decisionRationale}
            onChange={(e) => setDecisionRationale(e.target.value)}
            placeholder="Explain why this option was chosen based on the case facts, research, and legal analysis..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDecisionDialogOpen(false)}>
            Cancel
          </Button>
          <Button
            onClick={submitDecision}
            variant="contained"
            disabled={!decisionRationale.trim() || processingDecision}
            startIcon={processingDecision ? <CircularProgress size={16} /> : null}
          >
            {processingDecision ? 'Processing...' : 'Submit Decision'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PlaybookDecisionTab;