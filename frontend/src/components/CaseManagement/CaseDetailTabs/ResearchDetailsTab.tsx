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
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Stack
} from '@mui/material';
import {
  Search as ResearchIcon,
  ExpandMore as ExpandMoreIcon,
  Gavel as LegalIcon,
  Book as StatuteIcon,
  Assignment as FactualIcon,
  Timeline as ProceduralIcon,
  Psychology as ConceptIcon
} from '@mui/icons-material';
import { ResearchList, LegalConceptIdentification, ResearchItem } from '../../../types/api';
import { apiClient } from '../../../services/api';

interface ResearchDetailsTabProps {
  caseId: string;
}

const ResearchDetailsTab: React.FC<ResearchDetailsTabProps> = ({ caseId }) => {
  const [researchList, setResearchList] = useState<ResearchList | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadResearchList();
  }, [caseId]);

  const loadResearchList = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // TODO: Load research list when AI is implemented
      // For now, always show generation prompt
      setResearchList(null);
    } catch (err: any) {
      console.error('Failed to load research list:', err);
      setError('Failed to load research list');
    } finally {
      setLoading(false);
    }
  };

  const generateResearchList = async () => {
    try {
      setGenerating(true);
      setError(null);
      
      // TODO: Implement AI research list generation
      console.log('Research list generation not yet implemented for case:', caseId);
      
      // Show placeholder message
      setError('Research list generation not yet implemented. AI integration coming soon.');
    } catch (err) {
      console.error('Failed to generate research list:', err);
      setError('Failed to generate research list. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  const getResearchTypeIcon = (type: string) => {
    switch (type) {
      case 'Legal Precedent': return <LegalIcon color="primary" />;
      case 'Statute': return <StatuteIcon color="secondary" />;
      case 'Factual': return <FactualIcon color="info" />;
      case 'Procedural': return <ProceduralIcon color="warning" />;
      default: return <ResearchIcon />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'error';
      case 'Medium': return 'warning';
      case 'Low': return 'success';
      default: return 'default';
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
        <Button onClick={loadResearchList} sx={{ ml: 2 }}>
          Retry
        </Button>
      </Alert>
    );
  }

  if (!researchList) {
    return (
      <Card sx={{ mb: 4 }} data-testid="research-generation-prompt">
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <ResearchIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h5" component="h2">
              Research with Details
            </Typography>
          </Box>
          <Divider sx={{ mb: 3 }} />

          <Box textAlign="center" py={4}>
            <ResearchIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              Generate Research List
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3, maxWidth: 600, mx: 'auto' }}>
              Generate a comprehensive research list based on case files and document analysis. 
              This will identify key legal concepts, relevant precedents, applicable statutes, 
              and factual research needs to support Claude-driven playbook decisions.
            </Typography>
            <Button
              variant="contained"
              size="large"
              onClick={generateResearchList}
              disabled={generating}
              startIcon={generating ? <CircularProgress size={20} /> : <ResearchIcon />}
            >
              {generating ? 'Generating Research List...' : 'Generate Research List'}
            </Button>
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Box data-testid="research-details-content">
      {/* Research Overview */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Box display="flex" alignItems="center">
              <ResearchIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                Research with Details
              </Typography>
            </Box>
            <Stack direction="row" spacing={1}>
              <Chip
                label={`${researchList.research_items.length} research items`}
                variant="outlined"
                size="small"
              />
              <Chip
                label={`${researchList.legal_concepts_identified.length} legal concepts`}
                color="primary"
                size="small"
              />
            </Stack>
          </Box>
          <Divider sx={{ mb: 3 }} />

          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Generated: {new Date(researchList.generation_timestamp).toLocaleString('en-GB')}
          </Typography>
          
          <Button
            variant="outlined"
            onClick={generateResearchList}
            disabled={generating}
            startIcon={generating ? <CircularProgress size={16} /> : <ResearchIcon />}
          >
            {generating ? 'Regenerating...' : 'Regenerate Research List'}
          </Button>
        </CardContent>
      </Card>

      {/* Legal Concepts */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <ConceptIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6">
              Legal Concepts Identified
            </Typography>
          </Box>
          <Divider sx={{ mb: 3 }} />

          {researchList.legal_concepts_identified.map((concept, index) => (
            <Accordion key={index} sx={{ mb: 1 }}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                  {concept.concept_name}
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Box>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    <strong>Definition:</strong> {concept.concept_definition}
                  </Typography>
                  
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    <strong>Case Relevance:</strong> {concept.case_relevance}
                  </Typography>

                  {concept.research_questions.length > 0 && (
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 1 }}>
                        Research Questions:
                      </Typography>
                      <List dense>
                        {concept.research_questions.map((question, idx) => (
                          <ListItem key={idx} sx={{ py: 0.5, pl: 2 }}>
                            <Typography variant="body2">• {question}</Typography>
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}

                  {concept.related_precedents.length > 0 && (
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      <strong>Related Precedents:</strong> {concept.related_precedents.join(', ')}
                    </Typography>
                  )}

                  {concept.applicable_statutes.length > 0 && (
                    <Typography variant="body2">
                      <strong>Applicable Statutes:</strong> {concept.applicable_statutes.join(', ')}
                    </Typography>
                  )}
                </Box>
              </AccordionDetails>
            </Accordion>
          ))}
        </CardContent>
      </Card>

      {/* Research Items */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Research Items
          </Typography>
          <Divider sx={{ mb: 3 }} />

          <List>
            {researchList.research_items.map((item, index) => (
              <ListItem key={item.id} divider={index < researchList.research_items.length - 1} sx={{ flexDirection: 'column', alignItems: 'stretch' }}>
                <Box display="flex" alignItems="center" width="100%" mb={1}>
                  <Box display="flex" alignItems="center" flex={1}>
                    {getResearchTypeIcon(item.research_type)}
                    <Box sx={{ ml: 2 }}>
                      <Typography variant="subtitle2">
                        {item.research_question}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Legal Concept: {item.legal_concept}
                      </Typography>
                    </Box>
                  </Box>
                  <Stack direction="row" spacing={1}>
                    <Chip
                      label={item.priority}
                      color={getPriorityColor(item.priority) as any}
                      size="small"
                    />
                    <Chip
                      label={item.research_type}
                      variant="outlined"
                      size="small"
                    />
                    <Chip
                      label={`${Math.round(item.case_relevance_score * 100)}% relevant`}
                      color={item.case_relevance_score >= 0.8 ? 'success' : item.case_relevance_score >= 0.6 ? 'warning' : 'error'}
                      size="small"
                    />
                  </Stack>
                </Box>

                {(item.relevant_corpus_items.length > 0 || item.playbook_decision_nodes.length > 0) && (
                  <Box sx={{ ml: 5, mt: 1, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                    {item.relevant_corpus_items.length > 0 && (
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>Relevant Corpus Items:</strong> {item.relevant_corpus_items.join(', ')}
                      </Typography>
                    )}
                    {item.playbook_decision_nodes.length > 0 && (
                      <Typography variant="body2">
                        <strong>Affects Playbook Decisions:</strong> {item.playbook_decision_nodes.join(', ')}
                      </Typography>
                    )}
                  </Box>
                )}
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>

      {/* Research Categories */}
      <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={2}>
        {/* Precedent Research */}
        {researchList.precedent_research.length > 0 && (
          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <LegalIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  Precedent Research
                </Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <List dense>
                {researchList.precedent_research.map((precedent, index) => (
                  <ListItem key={index} sx={{ py: 0.5, pl: 0 }}>
                    <Typography variant="body2">• {precedent}</Typography>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        )}

        {/* Statute Research */}
        {researchList.statute_research.length > 0 && (
          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <StatuteIcon color="secondary" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  Statute Research
                </Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <List dense>
                {researchList.statute_research.map((statute, index) => (
                  <ListItem key={index} sx={{ py: 0.5, pl: 0 }}>
                    <Typography variant="body2">• {statute}</Typography>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        )}

        {/* Factual Research */}
        {researchList.factual_research.length > 0 && (
          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <FactualIcon color="info" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  Factual Research
                </Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <List dense>
                {researchList.factual_research.map((factual, index) => (
                  <ListItem key={index} sx={{ py: 0.5, pl: 0 }}>
                    <Typography variant="body2">• {factual}</Typography>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        )}
      </Box>
    </Box>
  );
};

export default ResearchDetailsTab;