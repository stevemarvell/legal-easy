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
import { APP_NAME, DEMO_LABEL, COLORS } from '../constants/branding';

const Layout = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && location.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', backgroundColor: COLORS.BACKGROUND }}>
      <AppBar position="sticky" sx={{ backgroundColor: COLORS.BACKGROUND, borderBottom: `1px solid ${COLORS.BORDER}` }}>
        <Toolbar>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexGrow: 1 }}>
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Typography variant="h5" component="h1" sx={{ color: COLORS.PRIMARY, fontWeight: 700 }}>
                  {APP_NAME}
                </Typography>
                <Chip
                  label={DEMO_LABEL}
                  size="small"
                  sx={{
                    backgroundColor: COLORS.PRIMARY,
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
              sx={{ color: isActive('/') ? COLORS.SECONDARY : 'white' }}
            >
              Dashboard
            </Button>
            <Button
              component={Link}
              to="/cases"
              color={isActive('/cases') ? 'secondary' : 'inherit'}
              sx={{ color: isActive('/cases') ? COLORS.SECONDARY : 'white' }}
            >
              Cases
            </Button>
            <Button
              component={Link}
              to="/playbooks"
              color={isActive('/playbooks') ? 'secondary' : 'inherit'}
              sx={{ color: isActive('/playbooks') ? COLORS.SECONDARY : 'white' }}
            >
              Playbooks
            </Button>
            <Button
              component={Link}
              to="/research"
              color={isActive('/research') ? 'secondary' : 'inherit'}
              sx={{ color: isActive('/research') ? COLORS.SECONDARY : 'white' }}
            >
              Research
            </Button>
            <Button
              component={Link}
              to="/analysis"
              color={isActive('/analysis') ? 'secondary' : 'inherit'}
              sx={{ color: isActive('/analysis') ? COLORS.SECONDARY : 'white' }}
            >
              Analysis
            </Button>
            <Button
              component={Link}
              to="/docs"
              color={isActive('/docs') ? 'secondary' : 'inherit'}
              sx={{ color: isActive('/docs') ? COLORS.SECONDARY : 'white' }}
            >
              Docs
            </Button>
            <Button
              component={Link}
              to="/admin"
              color={isActive('/admin') ? 'secondary' : 'inherit'}
              sx={{ color: isActive('/admin') ? COLORS.SECONDARY : 'white' }}
            >
              Admin
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
      <Container component="main" maxWidth="xl" sx={{ flex: 1, py: 3, backgroundColor: COLORS.BACKGROUND }}>
        <Outlet />
      </Container>
    </Box>
  );
};

export default Layout;