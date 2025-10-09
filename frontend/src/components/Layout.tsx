import { Outlet, Link, useLocation } from 'react-router-dom';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Box, 
  Container,
  Chip,
  Button
} from '@mui/material';

const Layout = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && location.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="sticky" sx={{ backgroundColor: '#161821' }}>
        <Toolbar>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexGrow: 1 }}>
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Typography variant="h5" component="h1" sx={{ color: '#744EFD', fontWeight: 700 }}>
                  Shift AI Legal
                </Typography>
                <Chip 
                  label="DEMO" 
                  size="small" 
                  sx={{ 
                    backgroundColor: '#744EFD', 
                    color: 'white',
                    fontSize: '0.75rem',
                    fontWeight: 600
                  }} 
                />
              </Box>
            </Link>
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              component={Link}
              to="/"
              color={isActive('/') ? 'secondary' : 'inherit'}
              sx={{ color: isActive('/') ? '#9844DA' : 'white' }}
            >
              Dashboard
            </Button>
            <Button
              component={Link}
              to="/cases"
              color={isActive('/cases') ? 'secondary' : 'inherit'}
              sx={{ color: isActive('/cases') ? '#9844DA' : 'white' }}
            >
              Cases
            </Button>
            <Button
              component={Link}
              to="/legal-research"
              color={isActive('/legal-research') ? 'secondary' : 'inherit'}
              sx={{ color: isActive('/legal-research') ? '#9844DA' : 'white' }}
            >
              Legal Research
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
      <Container component="main" maxWidth="xl" sx={{ flex: 1, py: 3 }}>
        <Outlet />
      </Container>
    </Box>
  );
};

export default Layout;