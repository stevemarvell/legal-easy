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
      default: '#1B1D29',
      paper: '#161821',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b8c5d6',
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
          border: 'none',
          boxShadow: 'none',
        },
      },
    },
  },
});