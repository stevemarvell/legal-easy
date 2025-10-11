import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  InputAdornment,
  Button,
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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Collapse,
  IconButton
} from '@mui/material';
import {
  Search as SearchIcon,
  Assignment as ContractIcon,
  Gavel as ClauseIcon,
  Balance as PrecedentIcon,
  MenuBook as StatuteIcon,
  Description as DocumentIcon,
  Clear as ClearIcon,
  FilterList as FilterIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  TrendingUp as TrendingIcon
} from '@mui/icons-material';
import { corpusService } from '../../services/corpusService';
import { CorpusItem, CorpusSearchResult } from '../../types/corpus';

interface CorpusSearchProps {
  onItemSelect?: (item: CorpusItem) => void;
  selectedItemId?: string;
  initialQuery?: string;
}

const CorpusSearch: React.FC<CorpusSearchProps> = ({
  onItemSelect,
  selectedItemId,
  initialQuery = ''
}) => {
  const [query, setQuery] = useState(initialQuery);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedResearchArea, setSelectedResearchArea] = useState<string>('');
  const [searchResults, setSearchResults] = useState<CorpusSearchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [availableResearchAreas, setAvailableResearchAreas] = useState<string[]>([]);

  // Category options
  const categoryOptions = [
    { value: '', label: 'All Categories' },
    { value: 'contracts', label: 'Contracts', icon: <ContractIcon /> },
    { value: 'clauses', label: 'Clauses', icon: <ClauseIcon /> },
    { value: 'precedents', label: 'Precedents', icon: <PrecedentIcon /> },
    { value: 'statutes', label: 'Statutes', icon: <StatuteIcon /> }
  ];

  // Debounced search function
  const debouncedSearch = useCallback(
    debounce(async (searchQuery: string, category: string, researchArea: string) => {
      if (!searchQuery.trim()) {
        setSearchResults(null);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        
        const results = await corpusService.searchCorpus(
          searchQuery.trim(),
          category || undefined,
          researchArea || undefined
        );
        
        setSearchResults(results);
        
        // Update available research areas from results
        if (results.research_areas_found.length > 0) {
          setAvailableResearchAreas(results.research_areas_found);
        }
      } catch (err) {
        console.error('Search failed:', err);
        setError('Search failed. Please try again.');
        setSearchResults(null);
      } finally {
        setLoading(false);
      }
    }, 300),
    []
  );

  // Effect for search execution
  useEffect(() => {
    debouncedSearch(query, selectedCategory, selectedResearchArea);
  }, [query, selectedCategory, selectedResearchArea, debouncedSearch]);

  // Initialize with initial query
  useEffect(() => {
    if (initialQuery) {
      setQuery(initialQuery);
    }
  }, [initialQuery]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      debouncedSearch(query, selectedCategory, selectedResearchArea);
    }
  };

  const handleClearSearch = () => {
    setQuery('');
    setSelectedCategory('');
    setSelectedResearchArea('');
    setSearchResults(null);
    setError(null);
  };

  const handleClearFilters = () => {
    setSelectedCategory('');
    setSelectedResearchArea('');
  };

  const getDocumentIcon = (category: string) => {
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

  const hasActiveFilters = selectedCategory || selectedResearchArea;

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }} data-testid="corpus-search">
      {/* Search Header */}
      <Card sx={{ mb: 2, flexShrink: 0 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <SearchIcon color="primary" />
            Search Research Corpus
          </Typography>
          
          {/* Search Form */}
          <Box component="form" onSubmit={handleSearchSubmit} sx={{ mb: 2 }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Search legal documents, concepts, and materials..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="primary" />
                  </InputAdornment>
                ),
                endAdornment: query && (
                  <InputAdornment position="end">
                    <IconButton onClick={handleClearSearch} size="small">
                      <ClearIcon />
                    </IconButton>
                  </InputAdornment>
                )
              }}
              data-testid="search-input"
            />
          </Box>

          {/* Filter Toggle */}
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Button
              variant="outlined"
              startIcon={<FilterIcon />}
              endIcon={showFilters ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              onClick={() => setShowFilters(!showFilters)}
              data-testid="filter-toggle"
            >
              Filters {hasActiveFilters && `(${[selectedCategory, selectedResearchArea].filter(Boolean).length})`}
            </Button>
            
            {hasActiveFilters && (
              <Button
                variant="text"
                size="small"
                onClick={handleClearFilters}
                data-testid="clear-filters"
              >
                Clear Filters
              </Button>
            )}
          </Box>

          {/* Filters */}
          <Collapse in={showFilters}>
            <Box sx={{ mt: 2, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Category</InputLabel>
                <Select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  label="Category"
                  data-testid="category-filter"
                >
                  {categoryOptions.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {option.icon}
                        {option.label}
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              
              <FormControl fullWidth size="small">
                <InputLabel>Research Area</InputLabel>
                <Select
                  value={selectedResearchArea}
                  onChange={(e) => setSelectedResearchArea(e.target.value)}
                  label="Research Area"
                  data-testid="research-area-filter"
                >
                  <MenuItem value="">All Research Areas</MenuItem>
                  {availableResearchAreas.map((area) => (
                    <MenuItem key={area} value={area}>
                      {area}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
          </Collapse>
        </CardContent>
      </Card>

      {/* Search Results */}
      <Card sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Results Header */}
        {searchResults && (
          <>
            <CardContent sx={{ pb: 1 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">
                  Search Results ({searchResults.total_count})
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Chip
                    size="small"
                    label={`Query: "${searchResults.query}"`}
                    variant="outlined"
                  />
                </Box>
              </Box>

              {/* Result Metadata */}
              {(searchResults.categories_found.length > 0 || searchResults.research_areas_found.length > 0) && (
                <Box sx={{ mb: 2 }}>
                  {searchResults.categories_found.length > 0 && (
                    <Box sx={{ mb: 1 }}>
                      <Typography variant="caption" color="text.secondary" display="block">
                        Categories found:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {searchResults.categories_found.map((category) => (
                          <Chip
                            key={category}
                            size="small"
                            label={getCategoryName(category)}
                            variant="outlined"
                            icon={getDocumentIcon(category)}
                            sx={{ fontSize: '0.7rem' }}
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                  
                  {searchResults.research_areas_found.length > 0 && (
                    <Box>
                      <Typography variant="caption" color="text.secondary" display="block">
                        Research areas found:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {searchResults.research_areas_found.map((area) => (
                          <Chip
                            key={area}
                            size="small"
                            label={area}
                            variant="outlined"
                            color="secondary"
                            sx={{ fontSize: '0.7rem' }}
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                </Box>
              )}
            </CardContent>
            
            <Divider />
          </>
        )}

        {/* Results List */}
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          {loading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          )}

          {error && (
            <Box sx={{ p: 2 }}>
              <Alert severity="error">{error}</Alert>
            </Box>
          )}

          {!loading && !error && !searchResults && !query && (
            <Box sx={{ p: 4, textAlign: 'center' }}>
              <SearchIcon color="disabled" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Search Research Corpus
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Enter a search term to find relevant legal documents, concepts, and materials.
              </Typography>
            </Box>
          )}

          {!loading && !error && searchResults && searchResults.items.length === 0 && (
            <Box sx={{ p: 4, textAlign: 'center' }}>
              <SearchIcon color="disabled" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                No Results Found
              </Typography>
              <Typography variant="body2" color="text.secondary">
                No items match your search criteria. Try different keywords or adjust your filters.
              </Typography>
            </Box>
          )}

          {!loading && !error && searchResults && searchResults.items.length > 0 && (
            <List disablePadding>
              {searchResults.items.map((item) => (
                <React.Fragment key={item.id}>
                  <ListItem disablePadding>
                    <ListItemButton
                      selected={selectedItemId === item.id}
                      onClick={() => onItemSelect?.(item)}
                      data-testid="search-result-item"
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
                          <Typography variant="body2" fontWeight="medium">
                            {item.title}
                          </Typography>
                        }
                        secondary={
                          <span>
                            <Typography variant="caption" color="text.secondary" component="span">
                              {getCategoryName(item.category)}
                              {item.document_type && ` • ${item.document_type}`}
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
                                    maxWidth: '400px'
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
                          {item.research_areas.slice(0, 3).map((area) => (
                            <Chip
                              key={area}
                              size="small"
                              label={area}
                              variant="outlined"
                              color="secondary"
                              sx={{ fontSize: '0.6rem', height: '16px' }}
                            />
                          ))}
                          {item.research_areas.length > 3 && (
                            <Chip
                              size="small"
                              label={`+${item.research_areas.length - 3}`}
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

// Debounce utility function
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

export default CorpusSearch;