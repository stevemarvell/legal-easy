import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Divider,
  Paper,
  Grid,
  Collapse,
  IconButton,
  Button,
  Tooltip
} from '@mui/material';
import {
  Psychology as ConceptIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Link as LinkIcon,
  Category as CategoryIcon,
  TrendingUp as TrendingIcon,
  Visibility as ViewIcon,
  AccountTree as RelationshipIcon
} from '@mui/icons-material';
import { corpusService } from '../../services/corpusService';
import { LegalConcept, ConceptAnalysisResult, CorpusItem } from '../../types/corpus';

interface ConceptAnalysisProps {
  onConceptSelect?: (concept: LegalConcept) => void;
  onCorpusItemSelect?: (itemId: string) => void;
  selectedConceptId?: string;
}

const ConceptAnalysis: React.FC<ConceptAnalysisProps> = ({
  onConceptSelect,
  onCorpusItemSelect,
  selectedConceptId
}) => {
  const [conceptAnalysis, setConceptAnalysis] = useState<ConceptAnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedConcepts, setExpandedConcepts] = useState<Set<string>>(new Set());
  const [selectedConcept, setSelectedConcept] = useState<LegalConcept | null>(null);

  useEffect(() => {
    const fetchConceptAnalysis = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const analysis = await corpusService.getConceptAnalysis();
        setConceptAnalysis(analysis);
      } catch (err) {
        console.error('Failed to fetch concept analysis:', err);
        setError('Failed to load concept analysis. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchConceptAnalysis();
  }, []);

  const handleConceptClick = (concept: LegalConcept) => {
    setSelectedConcept(concept);
    onConceptSelect?.(concept);
  };

  const handleToggleExpanded = (conceptId: string) => {
    const newExpanded = new Set(expandedConcepts);
    if (newExpanded.has(conceptId)) {
      newExpanded.delete(conceptId);
    } else {
      newExpanded.add(conceptId);
    }
    setExpandedConcepts(newExpanded);
  };

  const handleCorpusReferenceClick = (itemId: string) => {
    onCorpusItemSelect?.(itemId);
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
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!conceptAnalysis) {
    return (
      <Card>
        <CardContent sx={{ textAlign: 'center', py: 6 }}>
          <ConceptIcon color="disabled" sx={{ fontSize: 64, mb: 2 }} />
          <Typography variant="h6" color="text.secondary">
            No concept analysis available
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }} data-testid="concept-analysis">
      {/* Header */}
      <Card sx={{ mb: 2, flexShrink: 0 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <ConceptIcon color="primary" />
            Legal Concept Analysis
          </Typography>
          
          {/* Summary Statistics */}
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 2, mb: 2 }}>
            <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
              <Typography variant="h4" color="primary" fontWeight="bold">
                {conceptAnalysis.total_concepts}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Total Concepts
              </Typography>
            </Paper>
            
            <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
              <Typography variant="h4" color="secondary.main" fontWeight="bold">
                {conceptAnalysis.research_areas.length}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Research Areas
              </Typography>
            </Paper>
            
            <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
              <Typography variant="h4" color="success.main" fontWeight="bold">
                {conceptAnalysis.categories_analyzed.length}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Categories
              </Typography>
            </Paper>
            
            <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
              <Typography variant="h4" color="warning.main" fontWeight="bold">
                {conceptAnalysis.concepts.reduce((sum, concept) => sum + concept.corpus_references.length, 0)}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Total References
              </Typography>
            </Paper>
          </Box>

          {/* Research Areas */}
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Research Areas:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {conceptAnalysis.research_areas.map((area) => (
                <Chip
                  key={area}
                  label={area}
                  size="small"
                  color="secondary"
                  variant="outlined"
                />
              ))}
            </Box>
          </Box>

          {/* Categories Analyzed */}
          <Box>
            <Typography variant="subtitle2" gutterBottom>
              Categories Analyzed:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {conceptAnalysis.categories_analyzed.map((category) => (
                <Chip
                  key={category}
                  label={category.charAt(0).toUpperCase() + category.slice(1)}
                  size="small"
                  variant="outlined"
                />
              ))}
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Concepts List */}
      <Card sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <CardContent sx={{ pb: 1 }}>
          <Typography variant="h6" gutterBottom>
            Legal Concepts ({conceptAnalysis.concepts.length})
          </Typography>
        </CardContent>
        
        <Divider />
        
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          <List disablePadding>
            {conceptAnalysis.concepts.map((concept) => {
              const isExpanded = expandedConcepts.has(concept.id);
              const isSelected = selectedConceptId === concept.id;
              
              return (
                <React.Fragment key={concept.id}>
                  <ListItem disablePadding>
                    <ListItemButton
                      selected={isSelected}
                      onClick={() => handleConceptClick(concept)}
                      data-testid="concept-item"
                      sx={{
                        borderRadius: 1,
                        mx: 1,
                        mb: 0.5,
                        '&.Mui-selected': {
                          bgcolor: 'primary.50',
                          '&:hover': {
                            bgcolor: 'primary.100',
                          }
                        }
                      }}
                    >
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                            <Typography variant="body1" fontWeight="medium">
                              {concept.name}
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Chip
                                size="small"
                                label={`${concept.corpus_references.length} refs`}
                                variant="outlined"
                                sx={{ fontSize: '0.7rem' }}
                              />
                              <IconButton
                                size="small"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleToggleExpanded(concept.id);
                                }}
                                data-testid="expand-concept"
                              >
                                {isExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                              </IconButton>
                            </Box>
                          </Box>
                        }
                        secondary={
                          <Typography 
                            variant="body2" 
                            color="text.secondary"
                            sx={{ 
                              overflow: 'hidden',
                              textOverflow: 'ellipsis',
                              whiteSpace: 'nowrap',
                              maxWidth: '500px'
                            }}
                          >
                            {concept.definition}
                          </Typography>
                        }
                      />
                    </ListItemButton>
                  </ListItem>

                  {/* Expanded Content */}
                  <Collapse in={isExpanded}>
                    <Box sx={{ mx: 2, mb: 2, p: 2, bgcolor: 'background.default', borderRadius: 1 }}>
                      {/* Full Definition */}
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle2" gutterBottom>
                          Definition:
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {concept.definition}
                        </Typography>
                      </Box>

                      {/* Related Concepts */}
                      {concept.related_concepts.length > 0 && (
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="subtitle2" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <RelationshipIcon sx={{ fontSize: 16 }} />
                            Related Concepts:
                          </Typography>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {concept.related_concepts.map((relatedConcept) => (
                              <Chip
                                key={relatedConcept}
                                label={relatedConcept}
                                size="small"
                                variant="outlined"
                                color="secondary"
                                sx={{ fontSize: '0.7rem' }}
                                data-testid="related-concept"
                              />
                            ))}
                          </Box>
                        </Box>
                      )}

                      {/* Corpus References */}
                      {concept.corpus_references.length > 0 && (
                        <Box>
                          <Typography variant="subtitle2" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <LinkIcon sx={{ fontSize: 16 }} />
                            Corpus References ({concept.corpus_references.length}):
                          </Typography>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {concept.corpus_references.slice(0, 10).map((refId) => (
                              <Tooltip key={refId} title={`View corpus item ${refId}`}>
                                <Button
                                  size="small"
                                  variant="outlined"
                                  startIcon={<ViewIcon />}
                                  onClick={() => handleCorpusReferenceClick(refId)}
                                  sx={{ fontSize: '0.7rem', minWidth: 'auto', px: 1 }}
                                  data-testid="corpus-reference"
                                >
                                  {refId}
                                </Button>
                              </Tooltip>
                            ))}
                            {concept.corpus_references.length > 10 && (
                              <Chip
                                size="small"
                                label={`+${concept.corpus_references.length - 10} more`}
                                variant="outlined"
                                sx={{ fontSize: '0.7rem' }}
                              />
                            )}
                          </Box>
                        </Box>
                      )}
                    </Box>
                  </Collapse>
                </React.Fragment>
              );
            })}
          </List>
        </Box>
      </Card>
    </Box>
  );
};

export default ConceptAnalysis;