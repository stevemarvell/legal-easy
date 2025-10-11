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
  Paper,
  Button,
  IconButton,
  Tooltip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemButton,
  Collapse
} from '@mui/material';
import {
  Assignment as ContractIcon,
  Gavel as ClauseIcon,
  Balance as PrecedentIcon,
  MenuBook as StatuteIcon,
  Description as DocumentIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Link as LinkIcon,
  Category as CategoryIcon,
  Psychology as ConceptIcon,
  Folder as FolderIcon
} from '@mui/icons-material';
import { corpusService } from '../../services/corpusService';
import { CorpusItem } from '../../types/corpus';

interface CorpusViewerProps {
  itemId: string | null;
  onRelatedItemSelect?: (item: CorpusItem) => void;
}

const CorpusViewer: React.FC<CorpusViewerProps> = ({
  itemId,
  onRelatedItemSelect
}) => {
  const [item, setItem] = useState<CorpusItem | null>(null);
  const [relatedItems, setRelatedItems] = useState<CorpusItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showRelated, setShowRelated] = useState(true);
  const [showConcepts, setShowConcepts] = useState(true);

  useEffect(() => {
    const fetchItem = async () => {
      if (!itemId) {
        setItem(null);
        setRelatedItems([]);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        
        // Fetch item details with content
        const fetchedItem = await corpusService.getCorpusItem(itemId);
        setItem(fetchedItem);
        
        // Fetch related items
        try {
          const fetchedRelated = await corpusService.getRelatedMaterials(itemId);
          setRelatedItems(fetchedRelated);
        } catch (relatedErr) {
          console.warn('Failed to fetch related items:', relatedErr);
          setRelatedItems([]);
        }
      } catch (err) {
        console.error('Failed to fetch corpus item:', err);
        setError('Failed to load corpus item. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchItem();
  }, [itemId]);

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

  if (!itemId) {
    return (
      <Card sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <CardContent sx={{ textAlign: 'center', py: 6 }}>
          <FolderIcon color="primary" sx={{ fontSize: 64, mb: 2 }} />
          <Typography variant="h5" component="h2" gutterBottom>
            Select a Corpus Item
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Choose an item from the list to view its content and details.
          </Typography>
        </CardContent>
      </Card>
    );
  }

  if (loading) {
    return (
      <Card sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <CircularProgress />
      </Card>
    );
  }

  if (error) {
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Alert severity="error">
            {error}
          </Alert>
        </CardContent>
      </Card>
    );
  }

  if (!item) {
    return (
      <Card sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <CardContent sx={{ textAlign: 'center', py: 6 }}>
          <Typography variant="h6" color="text.secondary">
            Item not found
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }} data-testid="corpus-viewer">
      {/* Header */}
      <Card sx={{ mb: 2, flexShrink: 0 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2, mb: 2 }}>
            <Box sx={{ color: 'primary.main', mt: 0.5 }}>
              {getCategoryIcon(item.category)}
            </Box>
            <Box sx={{ flex: 1 }}>
              <Typography variant="h5" component="h1" gutterBottom data-testid="item-title">
                {item.title}
              </Typography>
              {item.description && (
                <Typography variant="body1" color="text.secondary" paragraph>
                  {item.description}
                </Typography>
              )}
            </Box>
          </Box>

          {/* Metadata */}
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
            <Chip
              icon={<CategoryIcon />}
              label={getCategoryName(item.category)}
              color="primary"
              variant="outlined"
            />
            {item.document_type && (
              <Chip
                label={item.document_type}
                variant="outlined"
              />
            )}
            {item.filename && (
              <Chip
                icon={<DocumentIcon />}
                label={item.filename}
                variant="outlined"
                size="small"
              />
            )}
          </Box>

          {/* Research Areas */}
          {item.research_areas.length > 0 && (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Research Areas:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                {item.research_areas.map((area) => (
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
          )}
        </CardContent>
      </Card>

      {/* Content */}
      <Card sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <CardContent sx={{ pb: 1 }}>
          <Typography variant="h6" gutterBottom>
            Content
          </Typography>
        </CardContent>
        
        <Divider />
        
        <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
          {item.content ? (
            <Paper variant="outlined" sx={{ p: 2, bgcolor: 'background.default' }}>
              <Typography 
                variant="body2" 
                component="pre" 
                sx={{ 
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'monospace',
                  fontSize: '0.875rem',
                  lineHeight: 1.6
                }}
                data-testid="item-content"
              >
                {item.content}
              </Typography>
            </Paper>
          ) : (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="body1" color="text.secondary">
                Content not available for this item.
              </Typography>
            </Box>
          )}
        </Box>
      </Card>

      {/* Legal Concepts */}
      {item.legal_concepts.length > 0 && (
        <Card sx={{ mt: 2, flexShrink: 0 }}>
          <CardContent sx={{ pb: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <ConceptIcon color="primary" />
                Legal Concepts ({item.legal_concepts.length})
              </Typography>
              <IconButton onClick={() => setShowConcepts(!showConcepts)}>
                {showConcepts ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              </IconButton>
            </Box>
          </CardContent>
          
          <Collapse in={showConcepts}>
            <Divider />
            <CardContent sx={{ pt: 1 }}>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {item.legal_concepts.map((concept) => (
                  <Chip
                    key={concept}
                    label={concept}
                    variant="outlined"
                    size="small"
                    data-testid="legal-concept"
                  />
                ))}
              </Box>
            </CardContent>
          </Collapse>
        </Card>
      )}

      {/* Related Items */}
      {relatedItems.length > 0 && (
        <Card sx={{ mt: 2, flexShrink: 0 }}>
          <CardContent sx={{ pb: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LinkIcon color="primary" />
                Related Materials ({relatedItems.length})
              </Typography>
              <IconButton onClick={() => setShowRelated(!showRelated)}>
                {showRelated ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              </IconButton>
            </Box>
          </CardContent>
          
          <Collapse in={showRelated}>
            <Divider />
            <List disablePadding>
              {relatedItems.map((relatedItem) => (
                <ListItem key={relatedItem.id} disablePadding>
                  <ListItemButton
                    onClick={() => onRelatedItemSelect?.(relatedItem)}
                    data-testid="related-item"
                    sx={{
                      '&:hover': {
                        bgcolor: 'action.hover'
                      }
                    }}
                  >
                  <ListItemIcon sx={{ minWidth: 36 }}>
                    {getCategoryIcon(relatedItem.category)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Typography variant="body2" fontWeight="medium">
                        {relatedItem.title}
                      </Typography>
                    }
                    secondary={
                      <Box>
                        <Typography variant="caption" color="text.secondary">
                          {getCategoryName(relatedItem.category)}
                          {relatedItem.document_type && ` • ${relatedItem.document_type}`}
                        </Typography>
                        {relatedItem.research_areas.length > 0 && (
                          <Box sx={{ mt: 0.5, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {relatedItem.research_areas.slice(0, 2).map((area) => (
                              <Chip
                                key={area}
                                size="small"
                                label={area}
                                variant="outlined"
                                sx={{ fontSize: '0.6rem', height: '16px' }}
                              />
                            ))}
                          </Box>
                        )}
                      </Box>
                    }
                  />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </Collapse>
        </Card>
      )}
    </Box>
  );
};

export default CorpusViewer;