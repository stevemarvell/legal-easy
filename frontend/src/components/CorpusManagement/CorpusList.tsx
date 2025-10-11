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
  Button,
  ButtonGroup
} from '@mui/material';
import {
  Assignment as ContractIcon,
  Gavel as ClauseIcon,
  Balance as PrecedentIcon,
  MenuBook as StatuteIcon,
  Description as DocumentIcon,
  Category as CategoryIcon,
  Search as SearchIcon
} from '@mui/icons-material';
import { corpusService } from '../../services/corpusService';
import { CorpusItem, CorpusCategory, CorpusCategoryInfo } from '../../types/corpus';

interface CorpusListProps {
  onItemSelect?: (item: CorpusItem) => void;
  selectedItemId?: string;
  selectedCategory?: string;
  onCategoryChange?: (category: string | null) => void;
}

const CorpusList: React.FC<CorpusListProps> = ({
  onItemSelect,
  selectedItemId,
  selectedCategory,
  onCategoryChange
}) => {
  const [items, setItems] = useState<CorpusItem[]>([]);
  const [categories, setCategories] = useState<Record<string, CorpusCategory>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Category configuration with icons
  const categoryConfig: CorpusCategoryInfo[] = [
    {
      id: 'contracts',
      name: 'Contracts',
      description: 'Contract templates and agreements',
      icon: <ContractIcon />
    },
    {
      id: 'clauses',
      name: 'Clauses',
      description: 'Standard legal clauses and provisions',
      icon: <ClauseIcon />
    },
    {
      id: 'precedents',
      name: 'Precedents',
      description: 'Case law and legal precedents',
      icon: <PrecedentIcon />
    },
    {
      id: 'statutes',
      name: 'Statutes',
      description: 'Legislation and regulations',
      icon: <StatuteIcon />
    }
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch categories first
        const fetchedCategories = await corpusService.getCategories();
        setCategories(fetchedCategories);
        
        // Fetch items for selected category or all items
        const fetchedItems = await corpusService.browseCorpus(selectedCategory || undefined);
        setItems(fetchedItems);
      } catch (err) {
        console.error('Failed to fetch corpus data:', err);
        setError('Failed to load corpus data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedCategory]);

  const handleCategorySelect = (categoryId: string | null) => {
    onCategoryChange?.(categoryId);
  };

  const getDocumentIcon = (category: string) => {
    const config = categoryConfig.find(c => c.id === category);
    return config?.icon || <DocumentIcon />;
  };

  const getCategoryCount = (categoryId: string): number => {
    return categories[categoryId]?.document_ids?.length || 0;
  };

  const getFilteredItems = (): CorpusItem[] => {
    if (!selectedCategory) return items;
    return items.filter(item => item.category === selectedCategory);
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

  const filteredItems = getFilteredItems();

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }} data-testid="corpus-list">
      {/* Category Navigation */}
      <Card sx={{ mb: 2, flexShrink: 0 }} data-testid="category-navigation">
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <CategoryIcon color="primary" />
            Research Categories
          </Typography>
          
          {/* Category Buttons */}
          <Box sx={{ mb: 2 }}>
            <ButtonGroup variant="outlined" sx={{ mb: 2, flexWrap: 'wrap' }}>
              <Button
                variant={!selectedCategory ? 'contained' : 'outlined'}
                onClick={() => handleCategorySelect(null)}
                data-testid="category-all"
              >
                All Categories ({items.length})
              </Button>
              {categoryConfig.map((category) => (
                <Button
                  key={category.id}
                  variant={selectedCategory === category.id ? 'contained' : 'outlined'}
                  startIcon={category.icon}
                  onClick={() => handleCategorySelect(category.id)}
                  data-testid={`category-${category.id}`}
                >
                  {category.name} ({getCategoryCount(category.id)})
                </Button>
              ))}
            </ButtonGroup>
          </Box>

          {/* Category Grid */}
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
            {categoryConfig.map((category) => (
              <Paper
                key={category.id}
                variant="outlined"
                sx={{
                  p: 2,
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  bgcolor: selectedCategory === category.id ? 'primary.50' : 'background.paper',
                  borderColor: selectedCategory === category.id ? 'primary.main' : 'divider',
                  '&:hover': {
                    bgcolor: 'primary.50',
                    borderColor: 'primary.main'
                  }
                }}
                onClick={() => handleCategorySelect(category.id)}
                data-testid={`category-card-${category.id}`}
              >
                <Box sx={{ color: 'primary.main', mb: 1 }}>
                  {category.icon}
                </Box>
                <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
                  {category.name}
                </Typography>
                <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
                  {category.description}
                </Typography>
                <Chip
                  size="small"
                  label={`${getCategoryCount(category.id)} items`}
                  color="primary"
                  variant="outlined"
                />
              </Paper>
            ))}
          </Box>
        </CardContent>
      </Card>

      {/* Items List */}
      <Card sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <CardContent sx={{ pb: 1 }}>
          <Typography variant="h6" gutterBottom>
            {selectedCategory 
              ? `${categoryConfig.find(c => c.id === selectedCategory)?.name || 'Category'} Items`
              : 'All Corpus Items'
            } ({filteredItems.length})
          </Typography>
        </CardContent>
        
        <Divider />
        
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          {filteredItems.length === 0 ? (
            <Box sx={{ p: 4, textAlign: 'center' }}>
              <SearchIcon color="disabled" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="body1" color="text.secondary">
                {selectedCategory 
                  ? `No items found in ${categoryConfig.find(c => c.id === selectedCategory)?.name} category`
                  : 'No corpus items available'
                }
              </Typography>
            </Box>
          ) : (
            <List disablePadding>
              {filteredItems.map((item) => (
                <React.Fragment key={item.id}>
                  <ListItem disablePadding>
                    <ListItemButton
                      selected={selectedItemId === item.id}
                      onClick={() => onItemSelect?.(item)}
                      data-testid="corpus-item"
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
                        {getDocumentIcon(item.category)}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Typography variant="body2" fontWeight="medium" noWrap>
                            {item.title}
                          </Typography>
                        }
                        secondary={
                          <span>
                            <Typography variant="caption" color="text.secondary" component="span">
                              {item.document_type || item.category}
                            </Typography>
                            {item.description && (
                              <>
                                <br />
                                <Typography 
                                  variant="caption" 
                                  color="text.secondary" 
                                  component="span"
                                  sx={{ 
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                    whiteSpace: 'nowrap',
                                    maxWidth: '300px'
                                  }}
                                >
                                  {item.description}
                                </Typography>
                              </>
                            )}
                          </span>
                        }
                      />
                      {item.research_areas.length > 0 && (
                        <Box sx={{ mt: 0.5, display: 'flex', flexWrap: 'wrap', gap: 0.5, ml: 6 }}>
                          {item.research_areas.slice(0, 2).map((area) => (
                            <Chip
                              key={area}
                              size="small"
                              label={area}
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
                    </ListItemButton>
                  </ListItem>
                </React.Fragment>
              ))}
            </List>
          )}
        </Box>
      </Card>
    </Box>
  );
};

export default CorpusList;