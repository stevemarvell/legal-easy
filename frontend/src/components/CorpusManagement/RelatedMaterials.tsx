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
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
  Paper,
  Grid,
  Button,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Assignment as ContractIcon,
  Gavel as ClauseIcon,
  Balance as PrecedentIcon,
  MenuBook as StatuteIcon,
  Description as DocumentIcon,
  Link as LinkIcon,
  TrendingUp as RelevanceIcon,
  Visibility as ViewIcon,
  Category as CategoryIcon,
  Psychology as ConceptIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import { corpusService } from '../../services/corpusService';
import { CorpusItem } from '../../types/corpus';

interface RelatedMaterialsProps {
  itemId: string | null;
  onItemSelect?: (item: CorpusItem) => void;
  selectedItemId?: string;
  maxItems?: number;
  showHeader?: boolean;
}

const RelatedMaterials: React.FC<RelatedMaterialsProps> = ({
  itemId,
  onItemSelect,
  selectedItemId,
  maxItems = 10,
  showHeader = true
}) => {
  const [relatedItems, setRelatedItems] = useState<CorpusItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentItem, setCurrentItem] = useState<CorpusItem | null>(null);

  useEffect(() => {
    const fetchRelatedMaterials = async () => {
      if (!itemId) {
        setRelatedItems([]);
        setCurrentItem(null);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        
        // Fetch current item details
        const item = await corpusService.getCorpusItem(itemId);
        setCurrentItem(item);
        
        // Fetch related materials
        const related = await corpusService.getRelatedMaterials(itemId);
        setRelatedItems(related.slice(0, maxItems));
      } catch (err) {
        console.error('Failed to fetch related materials:', err);
        setError('Failed to load related materials. Please try again.');
        setRelatedItems([]);
      } finally {
        setLoading(false);
      }
    };

    fetchRelatedMaterials();
  }, [itemId, maxItems]);

  const handleRefresh = () => {
    if (itemId) {
      // Trigger a refresh by re-running the effect
      setError(null);
      const fetchRelatedMaterials = async () => {
        try {
          setLoading(true);
          const related = await corpusService.getRelatedMaterials(itemId);
          setRelatedItems(related.slice(0, maxItems));
        } catch (err) {
          console.error('Failed to refresh related materials:', err);
          setError('Failed to refresh related materials. Please try again.');
        } finally {
          setLoading(false);
        }
      };
      fetchRelatedMaterials();
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'contracts':
        return <ContractIcon color="primary" />;
      case 'clauses':
        return <ClauseIcon color="primary" />;
      case 'precedents':
        return <PrecedentIcon color="primary" />;
      case 'statutes':
        return <StatuteIcon color="primary" />;
      default:
        return <DocumentIcon color="primary" />;
    }
  };

  const getCategoryName = (category: string): string => {
    const names: Record<string, string> = {
      contracts: 'Contract',
      clauses: 'Clause',
      precedents: 'Precedent',
      statutes: 'Statute'
    };
    return names[category] || category;
  };

  const getRelationshipType = (item: CorpusItem, currentItem: CorpusItem | null): string => {
    if (!currentItem) return 'Related';
    
    // Same category
    if (item.category === currentItem.category) {
      return 'Same Category';
    }
    
    // Shared research areas
    const sharedAreas = item.research_areas.filter(area => 
      currentItem.research_areas.includes(area)
    );
    if (sharedAreas.length > 0) {
      return `Shared: ${sharedAreas[0]}`;
    }
    
    // Shared legal concepts
    const sharedConcepts = item.legal_concepts.filter(concept => 
      currentItem.legal_concepts.includes(concept)
    );
    if (sharedConcepts.length > 0) {
      return `Concept: ${sharedConcepts[0]}`;
    }
    
    return 'Related';
  };

  const getRelevanceScore = (item: CorpusItem, currentItem: CorpusItem | null): number => {
    if (!currentItem) return 1;
    
    let score = 0;
    
    // Same category bonus
    if (item.category === currentItem.category) {
      score += 2;
    }
    
    // Shared research areas
    const sharedAreas = item.research_areas.filter(area => 
      currentItem.research_areas.includes(area)
    );
    score += sharedAreas.length;
    
    // Shared legal concepts
    const sharedConcepts = item.legal_concepts.filter(concept => 
      currentItem.legal_concepts.includes(concept)
    );
    score += sharedConcepts.length * 0.5;
    
    return Math.min(score, 5); // Cap at 5
  };

  if (!itemId) {
    return (
      <Card>
        <CardContent sx={{ textAlign: 'center', py: 4 }}>
          <LinkIcon color="disabled" sx={{ fontSize: 48, mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Select an Item
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Choose a corpus item to view related materials.
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }} data-testid="related-materials">
      {/* Header */}
      {showHeader && (
        <Card sx={{ mb: 2, flexShrink: 0 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
              <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LinkIcon color="primary" />
                Related Materials
              </Typography>
              <Tooltip title="Refresh related materials">
                <IconButton onClick={handleRefresh} disabled={loading}>
                  <RefreshIcon />
                </IconButton>
              </Tooltip>
            </Box>

            {/* Current Item Summary */}
            {currentItem && (
              <Paper variant="outlined" sx={{ p: 2, mb: 2, bgcolor: 'background.default' }}>
                <Typography variant="subtitle2" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  {getCategoryIcon(currentItem.category)}
                  Current Item: {currentItem.title}
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 1 }}>
                  <Chip
                    size="small"
                    label={getCategoryName(currentItem.category)}
                    variant="outlined"
                  />
                  {currentItem.research_areas.slice(0, 3).map((area) => (
                    <Chip
                      key={area}
                      size="small"
                      label={area}
                      color="secondary"
                      variant="outlined"
                      sx={{ fontSize: '0.7rem' }}
                    />
                  ))}
                </Box>
              </Paper>
            )}

            {/* Statistics */}
            {relatedItems.length > 0 && (
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 2 }}>
                <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                  <Typography variant="h4" color="primary" fontWeight="bold">
                    {relatedItems.length}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Related Items
                  </Typography>
                </Paper>
                
                <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                  <Typography variant="h4" color="secondary.main" fontWeight="bold">
                    {new Set(relatedItems.map(item => item.category)).size}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Categories
                  </Typography>
                </Paper>
              </Box>
            )}
          </CardContent>
        </Card>
      )}

      {/* Related Items List */}
      <Card sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {showHeader && (
          <>
            <CardContent sx={{ pb: 1 }}>
              <Typography variant="h6" gutterBottom>
                Items ({relatedItems.length})
              </Typography>
            </CardContent>
            <Divider />
          </>
        )}
        
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          {loading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          )}

          {error && (
            <Box sx={{ p: 2 }}>
              <Alert 
                severity="error" 
                action={
                  <Button onClick={handleRefresh} size="small">
                    Retry
                  </Button>
                }
              >
                {error}
              </Alert>
            </Box>
          )}

          {!loading && !error && relatedItems.length === 0 && (
            <Box sx={{ p: 4, textAlign: 'center' }}>
              <LinkIcon color="disabled" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                No Related Materials
              </Typography>
              <Typography variant="body2" color="text.secondary">
                No related items found for this corpus item.
              </Typography>
            </Box>
          )}

          {!loading && !error && relatedItems.length > 0 && (
            <List disablePadding>
              {relatedItems.map((item) => {
                const relevanceScore = getRelevanceScore(item, currentItem);
                const relationshipType = getRelationshipType(item, currentItem);
                
                return (
                  <React.Fragment key={item.id}>
                    <ListItem disablePadding>
                      <ListItemButton
                        selected={selectedItemId === item.id}
                        onClick={() => onItemSelect?.(item)}
                        data-testid="related-item"
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
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          {getCategoryIcon(item.category)}
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                              <Typography variant="body2" fontWeight="medium" noWrap sx={{ flex: 1, mr: 1 }}>
                                {item.title}
                              </Typography>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                <Tooltip title={`Relevance score: ${relevanceScore}/5`}>
                                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.25 }}>
                                    <RelevanceIcon sx={{ fontSize: 12, color: 'warning.main' }} />
                                    <Typography variant="caption" color="warning.main">
                                      {relevanceScore}
                                    </Typography>
                                  </Box>
                                </Tooltip>
                              </Box>
                            </Box>
                          }
                          secondary={
                            <Typography variant="caption" color="text.secondary" component="span">
                              {getCategoryName(item.category)}
                              {item.document_type && ` • ${item.document_type}`}
                            </Typography>
                          }
                        />
                        <Box sx={{ ml: 6, mt: 0.5 }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 0.5 }}>
                            <Chip
                              size="small"
                              label={relationshipType}
                              color="info"
                              variant="outlined"
                              sx={{ fontSize: '0.6rem', height: '16px' }}
                            />
                          </Box>
                          
                          {item.research_areas.length > 0 && (
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                              {item.research_areas.slice(0, 2).map((area) => (
                                <Chip
                                  key={area}
                                  size="small"
                                  label={area}
                                  color="secondary"
                                  variant="outlined"
                                  sx={{ fontSize: '0.6rem', height: '16px' }}
                                />
                              ))}
                              {item.research_areas.length > 2 && (
                                <Chip
                                  size="small"
                                  label={`+${item.research_areas.length - 2}`}
                                  variant="outlined"
                                  sx={{ fontSize: '0.6rem', height: '16px' }}
                                />
                              )}
                            </Box>
                          )}
                        </Box>
                      </ListItemButton>
                    </ListItem>
                  </React.Fragment>
                );
              })}
            </List>
          )}
        </Box>
      </Card>
    </Box>
  );
};

export default RelatedMaterials;