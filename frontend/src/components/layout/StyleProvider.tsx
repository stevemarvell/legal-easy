import React from 'react';
import { ThemeProvider, CssBaseline, GlobalStyles } from '@mui/material';
import { theme } from '../../theme/muiTheme';
import { designTokens } from '../../theme/designTokens';

interface StyleProviderProps {
  children: React.ReactNode;
}

// Global styles that extend beyond MUI theme
const globalStyles = {
  // Ensure consistent scrollbar styling
  '*::-webkit-scrollbar': {
    width: '8px',
    height: '8px',
  },
  '*::-webkit-scrollbar-track': {
    backgroundColor: designTokens.colors.background.default,
  },
  '*::-webkit-scrollbar-thumb': {
    backgroundColor: designTokens.colors.border.default,
    borderRadius: designTokens.borderRadius.base,
    '&:hover': {
      backgroundColor: designTokens.colors.border.hover,
    },
  },

  // Focus styles for accessibility
  '*:focus-visible': {
    outline: `2px solid ${designTokens.colors.primary.main}`,
    outlineOffset: '2px',
  },

  // Selection styles
  '::selection': {
    backgroundColor: `${designTokens.colors.primary.main}40`,
    color: designTokens.colors.text.primary,
  },

  // Smooth scrolling
  html: {
    scrollBehavior: 'smooth',
  },

  // Ensure full height
  'html, body, #root': {
    height: '100%',
    backgroundColor: `${designTokens.colors.background.default} !important`,
  },

  // Remove default margins and paddings
  'h1, h2, h3, h4, h5, h6, p, ul, ol, li': {
    margin: 0,
    padding: 0,
  },

  // Consistent link styling
  'a': {
    color: designTokens.colors.primary.main,
    textDecoration: 'none',
    transition: designTokens.transitions.fast,
    '&:hover': {
      color: designTokens.colors.primary.light,
      textDecoration: 'underline',
    },
  },

  // Button reset
  'button': {
    border: 'none',
    background: 'none',
    cursor: 'pointer',
    fontFamily: 'inherit',
  },

  // Input reset
  'input, textarea, select': {
    fontFamily: 'inherit',
  },

  // Image responsive by default
  'img': {
    maxWidth: '100%',
    height: 'auto',
  },

  // Table styling
  'table': {
    borderCollapse: 'collapse',
    width: '100%',
  },

  // Code styling
  'code, pre': {
    fontFamily: 'Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
    backgroundColor: designTokens.colors.background.surface,
    padding: '2px 4px',
    borderRadius: designTokens.borderRadius.sm,
    fontSize: '0.875em',
  },

  'pre': {
    padding: designTokens.spacing.md,
    overflow: 'auto',
    border: `1px solid ${designTokens.colors.border.default}`,
  },

  // Utility classes
  '.sr-only': {
    position: 'absolute',
    width: '1px',
    height: '1px',
    padding: 0,
    margin: '-1px',
    overflow: 'hidden',
    clip: 'rect(0, 0, 0, 0)',
    whiteSpace: 'nowrap',
    border: 0,
  },

  '.truncate': {
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },

  '.text-center': {
    textAlign: 'center',
  },

  '.text-left': {
    textAlign: 'left',
  },

  '.text-right': {
    textAlign: 'right',
  },

  // Animation classes
  '.fade-in': {
    animation: 'fadeIn 0.3s ease-in-out',
  },

  '@keyframes fadeIn': {
    from: { opacity: 0 },
    to: { opacity: 1 },
  },

  '.slide-up': {
    animation: 'slideUp 0.3s ease-out',
  },

  '@keyframes slideUp': {
    from: { 
      opacity: 0,
      transform: 'translateY(20px)',
    },
    to: { 
      opacity: 1,
      transform: 'translateY(0)',
    },
  },
};

const StyleProvider: React.FC<StyleProviderProps> = ({ children }) => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <GlobalStyles styles={globalStyles} />
      {children}
    </ThemeProvider>
  );
};

export default StyleProvider;