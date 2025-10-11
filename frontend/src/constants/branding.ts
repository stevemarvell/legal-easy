/**
 * Branding constants for LegalMind AI
 */

export const BRANDING = {
  // Main application name
  APP_NAME: 'LegalMind AI',
  
  // Full descriptive name
  FULL_NAME: 'LegalMind AI - Intelligent Legal Case Analysis',
  
  // Short tagline
  TAGLINE: 'Intelligent Legal Case Analysis',
  
  // Company/Product description
  DESCRIPTION: 'Advanced AI-powered legal case analysis platform that integrates document analysis, research corpus, and strategic playbooks to provide comprehensive legal insights.',
  
  // Demo indicator
  DEMO_LABEL: 'DEMO',
  
  // Color scheme
  COLORS: {
    PRIMARY: '#744EFD',
    SECONDARY: '#9844DA',
    BACKGROUND: '#0D0E14',
    BORDER: '#2A2D3A'
  },
  
  // URLs and links
  URLS: {
    HOMEPAGE: '/',
    DOCUMENTATION: '/docs',
    SUPPORT: '/support'
  },
  
  // Feature names
  FEATURES: {
    CASE_ANALYSIS: 'Case Analysis',
    DOCUMENT_ANALYSIS: 'Document Analysis', 
    RESEARCH_CORPUS: 'Research Corpus',
    LEGAL_PLAYBOOKS: 'Legal Playbooks',
    STRATEGIC_RECOMMENDATIONS: 'Strategic Recommendations'
  }
} as const;

// Export individual constants for convenience
export const {
  APP_NAME,
  FULL_NAME,
  TAGLINE,
  DESCRIPTION,
  DEMO_LABEL,
  COLORS,
  URLS,
  FEATURES
} = BRANDING;