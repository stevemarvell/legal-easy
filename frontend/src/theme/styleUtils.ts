import { SxProps, Theme } from '@mui/material/styles';
import { designTokens, styleMixins } from './designTokens';

// Utility functions for consistent styling
export const styleUtils = {
  // Spacing utilities
  spacing: {
    xs: designTokens.spacing.xs,
    sm: designTokens.spacing.sm,
    md: designTokens.spacing.md,
    lg: designTokens.spacing.lg,
    xl: designTokens.spacing.xl,
    '2xl': designTokens.spacing['2xl'],
    '3xl': designTokens.spacing['3xl'],
  },

  // Common component styles
  components: {
    // Page container
    pageContainer: {
      maxWidth: 'xl',
      mx: 'auto',
      px: designTokens.spacing.md,
      py: designTokens.spacing.lg,
    } as SxProps<Theme>,

    // Page header
    pageHeader: {
      mb: designTokens.spacing.xl,
      display: 'flex',
      flexDirection: 'column',
      gap: designTokens.spacing.md,
    } as SxProps<Theme>,

    // Card container
    card: {
      ...styleMixins.card,
      transition: designTokens.transitions.base,
      '&:hover': {
        borderColor: designTokens.colors.border.hover,
      },
    } as SxProps<Theme>,

    // Interactive card (clickable)
    interactiveCard: {
      ...styleMixins.card,
      cursor: 'pointer',
      transition: designTokens.transitions.base,
      '&:hover': {
        ...styleMixins.hoverLift,
        borderColor: designTokens.colors.primary.main,
      },
    } as SxProps<Theme>,

    // Search input
    searchInput: {
      '& .MuiOutlinedInput-root': {
        backgroundColor: designTokens.colors.background.paper,
        '& fieldset': {
          borderColor: designTokens.colors.border.default,
        },
        '&:hover fieldset': {
          borderColor: designTokens.colors.border.hover,
        },
        '&.Mui-focused fieldset': {
          borderColor: designTokens.colors.border.focus,
        },
      },
    } as SxProps<Theme>,

    // Button variants
    primaryButton: {
      ...styleMixins.buttonPrimary,
    } as SxProps<Theme>,

    // List item
    listItem: {
      borderRadius: designTokens.borderRadius.md,
      mb: designTokens.spacing.sm,
      transition: designTokens.transitions.base,
      '&:hover': {
        backgroundColor: designTokens.colors.background.surface,
      },
      '&.Mui-selected': {
        backgroundColor: `${designTokens.colors.primary.main}20`,
        borderColor: designTokens.colors.primary.main,
        '&:hover': {
          backgroundColor: `${designTokens.colors.primary.main}30`,
        },
      },
    } as SxProps<Theme>,

    // Status chip
    statusChip: {
      fontWeight: designTokens.typography.fontWeight.medium,
      fontSize: designTokens.typography.fontSize.sm,
    } as SxProps<Theme>,

    // Breadcrumb link
    breadcrumbLink: {
      display: 'flex',
      alignItems: 'center',
      textDecoration: 'none',
      color: designTokens.colors.text.secondary,
      transition: designTokens.transitions.fast,
      '&:hover': {
        color: designTokens.colors.primary.main,
      },
    } as SxProps<Theme>,

    // Loading container
    loadingContainer: {
      ...styleMixins.flexCenter,
      minHeight: '400px',
    } as SxProps<Theme>,

    // Empty state
    emptyState: {
      ...styleMixins.flexCenter,
      flexDirection: 'column',
      textAlign: 'center',
      py: designTokens.spacing['3xl'],
      color: designTokens.colors.text.secondary,
    } as SxProps<Theme>,

    // Two column layout
    twoColumnLayout: {
      display: 'flex',
      gap: designTokens.spacing.lg,
      height: 'calc(100vh - 180px)',
    } as SxProps<Theme>,

    // Sidebar
    sidebar: {
      width: '350px',
      flexShrink: 0,
    } as SxProps<Theme>,

    // Main content area
    mainContent: {
      flex: 1,
      minWidth: 0,
    } as SxProps<Theme>,
  },

  // Color utilities
  colors: {
    // Status colors for chips and indicators
    getStatusColor: (status: string) => {
      switch (status.toLowerCase()) {
        case 'active':
        case 'completed':
        case 'success':
          return 'success';
        case 'under review':
        case 'pending':
        case 'warning':
          return 'warning';
        case 'resolved':
        case 'info':
          return 'info';
        case 'error':
        case 'failed':
          return 'error';
        default:
          return 'default';
      }
    },

    // Confidence level colors
    getConfidenceColor: (confidence: number) => {
      if (confidence >= 0.8) return designTokens.colors.status.success;
      if (confidence >= 0.6) return designTokens.colors.status.warning;
      return designTokens.colors.status.error;
    },

    // Priority colors
    getPriorityColor: (priority: string) => {
      switch (priority.toLowerCase()) {
        case 'high':
          return designTokens.colors.status.error;
        case 'medium':
          return designTokens.colors.status.warning;
        case 'low':
          return designTokens.colors.status.info;
        default:
          return designTokens.colors.text.secondary;
      }
    },
  },

  // Typography utilities
  typography: {
    // Truncate text
    truncate: styleMixins.textTruncate,

    // Clamp text to specific number of lines
    clamp: styleMixins.textClamp,

    // Page title
    pageTitle: {
      fontSize: designTokens.typography.fontSize['3xl'],
      fontWeight: designTokens.typography.fontWeight.bold,
      color: designTokens.colors.primary.main,
      lineHeight: designTokens.typography.lineHeight.tight,
    } as SxProps<Theme>,

    // Section title
    sectionTitle: {
      fontSize: designTokens.typography.fontSize.xl,
      fontWeight: designTokens.typography.fontWeight.semibold,
      color: designTokens.colors.text.primary,
      mb: designTokens.spacing.md,
    } as SxProps<Theme>,

    // Subtitle
    subtitle: {
      fontSize: designTokens.typography.fontSize.lg,
      color: designTokens.colors.text.secondary,
      lineHeight: designTokens.typography.lineHeight.normal,
    } as SxProps<Theme>,

    // Body text
    body: {
      fontSize: designTokens.typography.fontSize.base,
      color: designTokens.colors.text.primary,
      lineHeight: designTokens.typography.lineHeight.relaxed,
    } as SxProps<Theme>,

    // Caption text
    caption: {
      fontSize: designTokens.typography.fontSize.sm,
      color: designTokens.colors.text.secondary,
      lineHeight: designTokens.typography.lineHeight.normal,
    } as SxProps<Theme>,
  },

  // Layout utilities
  layout: {
    // Flex utilities
    flexCenter: styleMixins.flexCenter,
    flexBetween: styleMixins.flexBetween,
    flexColumn: styleMixins.flexColumn,

    // Grid utilities
    gridContainer: {
      display: 'grid',
      gap: designTokens.spacing.lg,
    } as SxProps<Theme>,

    // Responsive grid
    responsiveGrid: {
      display: 'grid',
      gap: designTokens.spacing.lg,
      gridTemplateColumns: {
        xs: '1fr',
        sm: 'repeat(2, 1fr)',
        md: 'repeat(3, 1fr)',
        lg: 'repeat(4, 1fr)',
      },
    } as SxProps<Theme>,

    // Full height
    fullHeight: {
      height: '100%',
    } as SxProps<Theme>,

    // Full width
    fullWidth: {
      width: '100%',
    } as SxProps<Theme>,
  },

  // Animation utilities
  animations: {
    // Fade in
    fadeIn: {
      animation: 'fadeIn 0.3s ease-in-out',
      '@keyframes fadeIn': {
        from: { opacity: 0 },
        to: { opacity: 1 },
      },
    } as SxProps<Theme>,

    // Slide up
    slideUp: {
      animation: 'slideUp 0.3s ease-out',
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
    } as SxProps<Theme>,

    // Hover lift
    hoverLift: styleMixins.hoverLift,
  },
};

// Export commonly used styles
export const commonStyles = {
  pageContainer: styleUtils.components.pageContainer,
  pageHeader: styleUtils.components.pageHeader,
  card: styleUtils.components.card,
  interactiveCard: styleUtils.components.interactiveCard,
  searchInput: styleUtils.components.searchInput,
  loadingContainer: styleUtils.components.loadingContainer,
  emptyState: styleUtils.components.emptyState,
  twoColumnLayout: styleUtils.components.twoColumnLayout,
  sidebar: styleUtils.components.sidebar,
  mainContent: styleUtils.components.mainContent,
};

// Export design tokens for direct access
export { designTokens, styleMixins };