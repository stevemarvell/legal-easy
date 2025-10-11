// Design tokens for consistent styling across the application
export const designTokens = {
  // Color palette
  colors: {
    primary: {
      main: '#744EFD',
      dark: '#5a3bca',
      light: '#8b6bfe',
    },
    secondary: {
      main: '#9844DA',
    },
    background: {
      default: '#0D0E14',
      paper: '#161821',
      surface: '#1B1D29',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b8c5d6',
      disabled: '#6A6D7A',
    },
    status: {
      success: '#4CAF50',
      warning: '#FF9800',
      error: '#F44336',
      info: '#2196F3',
    },
    border: {
      default: '#2A2D3A',
      hover: '#744EFD',
      focus: '#744EFD',
    },
  },

  // Typography
  typography: {
    fontFamily: {
      primary: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      secondary: '"TT Firs Neue", sans-serif',
    },
    fontSize: {
      xs: '0.75rem',    // 12px
      sm: '0.875rem',   // 14px
      base: '1rem',     // 16px
      lg: '1.125rem',   // 18px
      xl: '1.25rem',    // 20px
      '2xl': '1.5rem',  // 24px
      '3xl': '1.875rem', // 30px
      '4xl': '2.25rem', // 36px
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
    },
  },

  // Spacing
  spacing: {
    xs: '0.25rem',   // 4px
    sm: '0.5rem',    // 8px
    md: '1rem',      // 16px
    lg: '1.5rem',    // 24px
    xl: '2rem',      // 32px
    '2xl': '3rem',   // 48px
    '3xl': '4rem',   // 64px
  },

  // Border radius
  borderRadius: {
    none: '0',
    sm: '0.125rem',   // 2px
    base: '0.25rem',  // 4px
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px
    xl: '0.75rem',    // 12px
    '2xl': '1rem',    // 16px
    full: '9999px',
  },

  // Shadows
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  },

  // Transitions
  transitions: {
    fast: '150ms ease-in-out',
    base: '200ms ease-in-out',
    slow: '300ms ease-in-out',
  },

  // Z-index
  zIndex: {
    dropdown: 1000,
    sticky: 1020,
    fixed: 1030,
    modal: 1040,
    popover: 1050,
    tooltip: 1060,
  },

  // Component-specific tokens
  components: {
    button: {
      height: '42px',
      borderRadius: '35px',
      fontSize: '15.95px',
      fontWeight: 500,
    },
    card: {
      borderRadius: '8px',
      padding: '24px',
    },
    input: {
      height: '42px',
      borderRadius: '4px',
    },
  },
} as const;

// Type for design tokens
export type DesignTokens = typeof designTokens;

// Helper function to get nested token values
export const getToken = (path: string): string => {
  const keys = path.split('.');
  let value: any = designTokens;
  
  for (const key of keys) {
    value = value?.[key];
    if (value === undefined) {
      console.warn(`Design token not found: ${path}`);
      return '';
    }
  }
  
  return value;
};

// Common style mixins
export const styleMixins = {
  // Flexbox utilities
  flexCenter: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  flexBetween: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  flexColumn: {
    display: 'flex',
    flexDirection: 'column',
  },

  // Text utilities
  textTruncate: {
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  textClamp: (lines: number) => ({
    display: '-webkit-box',
    WebkitLineClamp: lines,
    WebkitBoxOrient: 'vertical',
    overflow: 'hidden',
  }),

  // Hover effects
  hoverLift: {
    transition: designTokens.transitions.base,
    '&:hover': {
      transform: 'translateY(-2px)',
      boxShadow: designTokens.shadows.md,
    },
  },

  // Focus states
  focusRing: {
    '&:focus': {
      outline: 'none',
      boxShadow: `0 0 0 2px ${designTokens.colors.primary.main}`,
    },
  },

  // Card styles
  card: {
    backgroundColor: designTokens.colors.background.paper,
    border: `1px solid ${designTokens.colors.border.default}`,
    borderRadius: designTokens.borderRadius.lg,
    padding: designTokens.spacing.xl,
  },

  // Button styles
  buttonPrimary: {
    backgroundColor: designTokens.colors.background.paper,
    color: designTokens.colors.text.primary,
    border: `1px solid ${designTokens.colors.primary.main}`,
    borderRadius: designTokens.components.button.borderRadius,
    height: designTokens.components.button.height,
    fontSize: designTokens.components.button.fontSize,
    fontWeight: designTokens.components.button.fontWeight,
    transition: designTokens.transitions.base,
    '&:hover': {
      backgroundColor: designTokens.colors.primary.main,
      borderColor: designTokens.colors.primary.main,
      color: designTokens.colors.text.primary,
    },
  },
};