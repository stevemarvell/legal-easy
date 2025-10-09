import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { apiClient } from '../services/api';
import { LegalSearchResult } from '../types/api';
import './LegalResearch.css';

const LegalResearch = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<LegalSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const queryParam = searchParams.get('q');
    if (queryParam) {
      setSearchQuery(queryParam);
      performSearch(queryParam);
    }
  }, [searchParams]);

  const performSearch = async (query?: string) => {
    const searchTerm = query || searchQuery;
    if (!searchTerm.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.post<{ results: LegalSearchResult[] }>('/api/legal-research/search', {
        query: searchTerm.trim()
      });
      setSearchResults(response.data.results || []);
    } catch (err) {
      console.error('Search failed:', err);
      setError('Failed to perform search. Please try again.');
      setSearchResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setSearchParams({ q: searchQuery.trim() });
      performSearch();
    }
  };

  return (
    <div className="legal-research">
      <div className="page-header">
        <div className="container">
          <h1>Legal Research</h1>
          <p>Search and analyze legal documents, precedents, and case law</p>
        </div>
      </div>

      <div className="research-content">
        <div className="container">
          <div className="search-section">
            <form onSubmit={handleSearchSubmit} className="search-box">
              <input 
                type="text" 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search legal documents, cases, or ask a question..."
                className="search-input"
              />
              <button 
                type="submit" 
                className="search-button"
                disabled={loading || !searchQuery.trim()}
              >
                {loading ? 'Searching...' : 'Search'}
              </button>
            </form>
          </div>

          {/* Search Results */}
          {searchResults.length > 0 && (
            <div className="search-results">
              <h2>Search Results</h2>
              <div className="results-list">
                {searchResults.map((result) => (
                  <div key={result.id} className="result-card">
                    <div className="result-header">
                      <h3 className="result-title">{result.title}</h3>
                      <div className="result-meta">
                        <span className="result-type">{result.document_type}</span>
                        <span className="result-score">
                          {Math.round(result.relevance_score * 100)}% match
                        </span>
                      </div>
                    </div>
                    <p className="result-content">{result.content}</p>
                    <div className="result-footer">
                      <span className="result-source">Source: {result.source}</span>
                      {result.jurisdiction && (
                        <span className="result-jurisdiction">Jurisdiction: {result.jurisdiction}</span>
                      )}
                      {result.date && (
                        <span className="result-date">Date: {new Date(result.date).toLocaleDateString()}</span>
                      )}
                    </div>
                    {result.url && (
                      <a href={result.url} target="_blank" rel="noopener noreferrer" className="result-link">
                        View Full Document
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="search-error">
              <p>{error}</p>
              <button onClick={() => performSearch()}>Try Again</button>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="search-loading">
              <div className="loading-spinner"></div>
              <p>Searching legal database...</p>
            </div>
          )}

          {/* Empty State */}
          {!loading && !error && searchResults.length === 0 && searchQuery && (
            <div className="search-empty">
              <p>No results found for "{searchQuery}". Try different search terms.</p>
            </div>
          )}

          <div className="research-tools">
            <div className="tool-card">
              <div className="tool-icon">📄</div>
              <h3>Document Analysis</h3>
              <p>Analyze legal documents and extract key information</p>
              <button className="tool-button">View Documents</button>
            </div>

            <div className="tool-card">
              <div className="tool-icon">🔍</div>
              <h3>Case Law Search</h3>
              <p>Search through precedents and case law with semantic matching</p>
              <button className="tool-button">Search Cases</button>
            </div>

            <div className="tool-card">
              <div className="tool-icon">📊</div>
              <h3>Legal Analytics</h3>
              <p>Generate insights and reports from legal case data</p>
              <button className="tool-button">View Analytics</button>
            </div>
          </div>

          <div className="intelligence-workflow">
            <h2>Legal Research Features</h2>
            <div className="workflow-grid">
              <div className="workflow-item">
                <div className="workflow-icon">📥</div>
                <h4>Document Processing</h4>
                <p>Process and analyze legal documents in various formats</p>
              </div>
              <div className="workflow-item">
                <div className="workflow-icon">⚙️</div>
                <h4>Text Analysis</h4>
                <p>Extract and structure information from legal texts</p>
              </div>
              <div className="workflow-item">
                <div className="workflow-icon">🏷️</div>
                <h4>Classification</h4>
                <p>Categorize documents by legal domain and content type</p>
              </div>
              <div className="workflow-item">
                <div className="workflow-icon">🔗</div>
                <h4>Relationship Mapping</h4>
                <p>Identify connections between cases, precedents, and statutes</p>
              </div>
              <div className="workflow-item">
                <div className="workflow-icon">📤</div>
                <h4>Information Extraction</h4>
                <p>Extract key facts, dates, parties, and legal concepts</p>
              </div>
              <div className="workflow-item">
                <div className="workflow-icon">✅</div>
                <h4>Relevance Scoring</h4>
                <p>Rank search results by relevance and legal significance</p>
              </div>
            </div>
          </div>

          <div className="recent-research">
            <h3>Recent Research</h3>
            <div className="research-list">
              <div className="research-item">
                <h4>Employment Law Precedents Analysis</h4>
                <p>Analysis of recent employment law cases and their implications</p>
                <span className="research-date">2 hours ago</span>
              </div>
              <div className="research-item">
                <h4>Contract Clause Extraction</h4>
                <p>Extracted key clauses from 15 service agreements</p>
                <span className="research-date">1 day ago</span>
              </div>
              <div className="research-item">
                <h4>Regulatory Compliance Review</h4>
                <p>Comprehensive review of new data protection regulations</p>
                <span className="research-date">3 days ago</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LegalResearch;