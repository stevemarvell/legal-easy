import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    mode: 'dark',
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
    },

    text: {
      primary: '#ffffff',
      secondary: '#b8c5d6',
    },
    success: {
      main: '#4CAF50',
      light: '#81C784',
      dark: '#388E3C',
    },
    warning: {
      main: '#FF9800',
      light: '#FFB74D',
      dark: '#F57C00',
    },
    error: {
      main: '#F44336',
      light: '#EF5350',
      dark: '#D32F2F',
    },
    info: {
      main: '#2196F3',
      light: '#64B5F6',
      dark: '#1976D2',
    },
    grey: {
      50: '#2A2D3A',
      100: '#3A3D4A',
      200: '#4A4D5A',
      300: '#5A5D6A',
      400: '#6A6D7A',
      500: '#7A7D8A',
      600: '#8A8D9A',
      700: '#9A9DAA',
      800: '#AAADBA',
      900: '#BABDCA',
    },
  },
  typography: {
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '35px',
          textTransform: 'none',
          fontWeight: 500,
          fontSize: '15.95px',
          height: '42px',
          fontFamily: '"TT Firs Neue", sans-serif',
        },
        contained: {
          backgroundColor: '#161821',
          color: '#ffffff',
          border: '1px solid #744EFD',
          '&:hover': {
            backgroundColor: '#744EFD',
            borderColor: '#744EFD',
            color: '#ffffff',
          },
        },
        outlined: {
          backgroundColor: 'transparent',
          color: '#ffffff',
          border: '1px solid #744EFD',
          '&:hover': {
            backgroundColor: '#744EFD',
            borderColor: '#744EFD',
            color: '#ffffff',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#161821',
          border: '1px solid #2A2D3A',
          boxShadow: 'none',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#161821',
          '&.MuiPaper-outlined': {
            border: '1px solid #2A2D3A',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#0D0E14',
          borderBottom: '1px solid #2A2D3A',
        },
      },
    },
    MuiContainer: {
      styleOverrides: {
        root: {
          backgroundColor: '#0D0E14 !important',
        },
      },
    },
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#0D0E14 !important',
          color: '#ffffff !important',
        },
        html: {
          backgroundColor: '#0D0E14 !important',
        },
        '#root': {
          backgroundColor: '#0D0E14 !important',
          minHeight: '100vh',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          '&.MuiChip-filled': {
            backgroundColor: '#424242',
            color: '#ffffff',
            '& .MuiChip-icon': {
              color: '#ffffff',
            },
            '& .MuiChip-deleteIcon': {
              color: '#ffffff',
            },
          },
          '&.MuiChip-colorSuccess': {
            backgroundColor: '#1B5E20',
            color: '#ffffff',
            border: '1px solid #4CAF50',
            '&.MuiChip-filled': {
              backgroundColor: '#424242',
              color: '#ffffff',
            },
          },
          '&.MuiChip-colorWarning': {
            backgroundColor: '#E65100',
            color: '#ffffff',
            border: '1px solid #FF9800',
            '&.MuiChip-filled': {
              backgroundColor: '#424242',
              color: '#ffffff',
            },
          },
          '&.MuiChip-colorError': {
            backgroundColor: '#B71C1C',
            color: '#ffffff',
            border: '1px solid #F44336',
            '&.MuiChip-filled': {
              backgroundColor: '#424242',
              color: '#ffffff',
            },
          },
          '&.MuiChip-colorInfo': {
            '&.MuiChip-filled': {
              backgroundColor: '#424242',
              color: '#ffffff',
            },
          },
          '&.MuiChip-colorPrimary': {
            '&.MuiChip-filled': {
              backgroundColor: '#424242',
              color: '#ffffff',
            },
          },
          '&.MuiChip-colorDefault': {
            '&.MuiChip-filled': {
              backgroundColor: '#424242',
              color: '#ffffff',
            },
          },
        },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          backgroundColor: '#161821',
          border: '1px solid #2A2D3A',
          '&.MuiAlert-standardError': {
            backgroundColor: '#1A0E0E',
            border: '1px solid #F44336',
            color: '#ffffff',
          },
          '&.MuiAlert-standardWarning': {
            backgroundColor: '#1A1408',
            border: '1px solid #FF9800',
            color: '#ffffff',
          },
          '&.MuiAlert-standardSuccess': {
            backgroundColor: '#0E1A0E',
            border: '1px solid #4CAF50',
            color: '#ffffff',
          },
          '&.MuiAlert-standardInfo': {
            backgroundColor: '#0E141A',
            border: '1px solid #2196F3',
            color: '#ffffff',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            backgroundColor: '#161821',
            '& fieldset': {
              borderColor: '#2A2D3A',
            },
            '&:hover fieldset': {
              borderColor: '#744EFD',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#744EFD',
            },
          },
        },
      },
    },
    MuiList: {
      styleOverrides: {
        root: {
          backgroundColor: 'transparent',
        },
      },
    },
    MuiListItem: {
      styleOverrides: {
        root: {
          '&:hover': {
            backgroundColor: '#1B1D29',
          },
        },
      },
    },
  },
});