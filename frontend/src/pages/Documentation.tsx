import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  CardActionArea,
  Breadcrumbs,
  Link,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Button,
  Paper
} from '@mui/material';
import {
  Home as HomeIcon,
  MenuBook as DocsIcon,
  Business as BusinessIcon,
  Code as TechnicalIcon,
  Gavel as LegalIcon,
  Storage as DataIcon,
  ArrowForward as ArrowIcon,
  ArrowBack as BackIcon
} from '@mui/icons-material';

interface DocSection {
  id: string;
  title: string;
  description: string;
  audience: string;
  icon: React.ReactNode;
  color: string;
  features: string[];
  path: string;
}

interface DocContent {
  title: string;
  content: string;
}

const Documentation: React.FC = () => {
  const navigate = useNavigate();
  const { section } = useParams<{ section?: string }>();
  const selectedSection = section || null;

  const docSections: DocSection[] = [
    {
      id: 'overview',
      title: 'Demo Overview',
      description: 'What actually works in this legal platform demo.',
      audience: 'All users',
      icon: <LegalIcon sx={{ fontSize: 40 }} />,
      color: '#744EFD',
      features: [
        'Legal playbooks with rule engine',
        'Case management (demo data)',
        'Document viewer (demo data)',
        'Basic legal research'
      ],
      path: '/docs/overview'
    },
    {
      id: 'technical',
      title: 'Technical Details',
      description: 'How the demo is built and what technologies are used.',
      audience: 'Developers',
      icon: <TechnicalIcon sx={{ fontSize: 40 }} />,
      color: '#4CAF50',
      features: [
        'React + TypeScript frontend',
        'FastAPI + Python backend',
        'Static JSON data files',
        'Basic REST API endpoints'
      ],
      path: '/docs/technical'
    },
    {
      id: 'data',
      title: 'Demo Data',
      description: 'Sample data used in the demonstration.',
      audience: 'All users',
      icon: <DataIcon sx={{ fontSize: 40 }} />,
      color: '#FF9800',
      features: [
        '6 sample legal cases',
        'Mock document analysis',
        'Legal playbook rules',
        'Demo legal corpus for search'
      ],
      path: '/docs/data'
    }
  ];

  const getDocumentationContent = (sectionId: string): DocContent => {
    switch (sectionId) {
      case 'overview':
        return {
          title: 'Demo Overview',
          content: `
# Legal Platform Demo

This is a demonstration of a legal case management platform with basic functionality.

## What Actually Works

### 📚 Legal Playbooks ✅
- View predefined legal decision frameworks
- Apply rules to cases and get recommendations  
- Case strength assessment (Strong/Moderate/Weak)
- Automated rule application with reasoning

### 📋 Case Management (Demo Data Only)
- View 6 sample cases from JSON files
- Display case details and status
- Basic case statistics dashboard
- Document associations (display only)

### 📄 Document Viewer (Demo Data Only)
- View sample documents and mock analysis
- Display extracted information (dates, parties, clauses)
- Show confidence scores (all fake)
- Document type classification

### 🔍 Legal Research (Demo Data Only)
- Search through sample legal content
- Filter by legal area and document type
- Basic text matching (not semantic search)
- Display search results with relevance scores

## What's NOT Implemented

❌ Document upload
❌ Real AI analysis  
❌ User authentication
❌ Case creation/editing
❌ External legal database integration
❌ Actual semantic search
❌ Claude AI integration
❌ Vector databases
❌ Real performance metrics

## Demo Purpose

This demo shows the UI/UX design and basic functionality of a legal platform concept. All data is static and no real AI processing occurs.
          `
        };
      case 'technical':
        return {
          title: 'Technical Implementation',
          content: `
# Technical Details

## Architecture

### Frontend ✅
- **React 18** + TypeScript + Material-UI
- Case management interface
- Document viewer components
- Legal research interface
- Playbook viewer

### Backend ✅
- **FastAPI** + Python
- REST API endpoints
- JSON file data loading
- Basic search functionality

### Data Storage
- **Static JSON files** (no database)
- Demo cases, documents, analysis
- Legal playbooks with rules
- Sample legal corpus

## API Endpoints

\`\`\`
GET /api/cases                    - List demo cases
GET /api/cases/{id}               - Get case details
GET /api/cases/{id}/assessment    - Get playbook assessment
GET /api/documents/{id}           - Get document details
GET /api/documents/{id}/analysis  - Get mock analysis
POST /api/legal-research/search   - Search demo corpus
GET /api/playbooks/{case_type}    - Get playbook rules
\`\`\`

## How Playbooks Work

1. Load rules from \`demo_playbooks.json\`
2. Apply rules to cases based on keyword matching
3. Calculate case strength from rule weights
4. Generate recommendations and reasoning

## Demo Data Files

- \`demo_cases.json\` - 6 sample legal cases
- \`demo_documents.json\` - Sample documents
- \`demo_document_analysis.json\` - Mock analysis results
- \`demo_playbooks.json\` - Legal decision rules
- \`demo_legal_corpus.json\` - Sample legal content

## Running the Demo

\`\`\`bash
# Frontend
cd frontend
npm install
npm run dev

# Backend  
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`
          `
        };
      case 'data':
        return {
          title: 'Demo Data Structure',
          content: `
# Demo Data

## Sample Cases (6 total)

1. **Employment Dispute** - Wrongful dismissal case
2. **Contract Breach** - Software license violation  
3. **Debt Claim** - Unpaid consulting fees
4. **Employment Dispute** - Age discrimination
5. **Contract Breach** - Service agreement dispute
6. **Debt Claim** - Outstanding invoice

## Mock Document Analysis

Each document has fake analysis including:
- Extracted dates and parties
- Key clauses identification
- Confidence scores (all fabricated)
- Document type classification

## Legal Playbooks

### Employment Dispute Rules
- Termination within protected period
- Age discrimination indicators
- Performance documentation
- Hostile work environment

### Contract Breach Rules  
- Clear contract terms violated
- Ambiguous language issues
- Non-compete violations
- Damages calculability

### Debt Claim Rules
- Clear debt documentation
- Debtor disputes and defenses
- Asset availability
- Statute of limitations

## Legal Research Corpus

Sample content includes:
- Employment contract templates
- Termination clauses
- UK case law summaries
- Legal precedents
- Contract law principles

All content is simplified demo data, not real legal documents.
          `
        };
      default:
        return {
          title: 'Documentation',
          content: 'Select a section to view documentation.'
        };
    }
  };

  const handleSectionSelect = (sectionId: string) => {
    navigate(`/docs/${sectionId}`);
  };



  const handleBreadcrumbNavigation = (path: string) => {
    navigate(path);
  };

  const handleBackNavigation = () => {
    if (selectedSection) {
      // If viewing a section, go back to documentation main page
      navigate('/docs');
    } else {
      // If on main documentation page, go back to previous page in history
      try {
        navigate(-1);
      } catch (error) {
        // Fallback to dashboard if navigation fails
        navigate('/');
      }
    }
  };

  if (selectedSection) {
    const content = getDocumentationContent(selectedSection);
    return (
      <Container maxWidth="xl">
        <Box>
          {/* Header with Navigation */}
          <Box mb={4}>
            <Button
              variant="outlined"
              startIcon={<BackIcon />}
              onClick={handleBackNavigation}
              sx={{ mb: 2 }}
            >
              Back
            </Button>

            {/* Breadcrumbs */}
            <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
              <Link
                component="button"
                variant="body2"
                onClick={() => handleBreadcrumbNavigation('/')}
                sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
              >
                <HomeIcon sx={{ mr: 0.5 }} fontSize="inherit" />
                Dashboard
              </Link>
              <Link
                component="button"
                variant="body2"
                onClick={() => navigate('/docs')}
                sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
              >
                <DocsIcon sx={{ mr: 0.5 }} fontSize="inherit" />
                Documentation
              </Link>
              <Typography color="text.primary" variant="body2">
                {content.title}
              </Typography>
            </Breadcrumbs>

            <Typography variant="h3" component="h1" color="primary">
              {content.title}
            </Typography>
          </Box>

          {/* Content */}
          <Paper sx={{ p: 4 }}>
            <Typography component="div" sx={{ whiteSpace: 'pre-line' }}>
              {content.content}
            </Typography>
          </Paper>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box>
        {/* Header */}
        <Box mb={4}>
          <Button
            variant="outlined"
            startIcon={<BackIcon />}
            onClick={handleBackNavigation}
            sx={{ mb: 2 }}
          >
            Back
          </Button>

          {/* Breadcrumbs */}
          <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
            <Link
              component="button"
              variant="body2"
              onClick={() => handleBreadcrumbNavigation('/')}
              sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
            >
              <HomeIcon sx={{ mr: 0.5 }} fontSize="inherit" />
              Dashboard
            </Link>
            <Typography color="text.primary" variant="body2">
              Documentation
            </Typography>
          </Breadcrumbs>

          <Typography variant="h3" component="h1" color="primary" gutterBottom>
            Demo Documentation
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Honest documentation about what actually works in this legal platform demo
          </Typography>
        </Box>

        {/* Documentation Sections */}
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          {docSections.map((section) => (
            <Card key={section.id} sx={{ transition: 'transform 0.2s', '&:hover': { transform: 'translateY(-2px)' } }}>
              <CardActionArea onClick={() => handleSectionSelect(section.id)}>
                <CardContent sx={{ p: 3 }}>
                  <Box display="flex" alignItems="flex-start" gap={3}>
                    <Box sx={{ color: section.color }}>
                      {section.icon}
                    </Box>
                    <Box flex={1}>
                      <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
                        <Typography variant="h5" component="h2" color="primary">
                          {section.title}
                        </Typography>
                        <ArrowIcon color="action" />
                      </Box>
                      <Typography variant="body1" color="text.secondary" paragraph>
                        {section.description}
                      </Typography>
                      <Chip
                        label={section.audience}
                        size="small"
                        sx={{ mb: 2, backgroundColor: section.color, color: 'white' }}
                      />
                      <Divider sx={{ my: 2 }} />
                      <List dense>
                        {section.features.map((feature, index) => (
                          <ListItem key={index} sx={{ py: 0.5 }}>
                            <ListItemIcon sx={{ minWidth: 32 }}>
                              <Box
                                sx={{
                                  width: 6,
                                  height: 6,
                                  borderRadius: '50%',
                                  backgroundColor: section.color
                                }}
                              />
                            </ListItemIcon>
                            <ListItemText
                              primary={feature}
                              primaryTypographyProps={{ variant: 'body2' }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  </Box>
                </CardContent>
              </CardActionArea>
            </Card>
          ))}
        </Box>
      </Box>
    </Container>
  );
};

export default Documentation;