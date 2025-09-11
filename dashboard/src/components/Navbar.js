import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Chip,
  Avatar
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  HealthAndSafety,
  WaterDrop,
  Warning,
  TrendingUp,
  Map,
  LocalHospital,
  Circle,
  DarkMode,
  LightMode
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isDark, toggleTheme } = useTheme();

  const menuItems = [
    { path: '/', label: 'Overview', icon: <DashboardIcon /> },
    { path: '/health-reports', label: 'Health Reports', icon: <HealthAndSafety /> },
    { path: '/water-quality', label: 'Water Quality', icon: <WaterDrop /> },
    { path: '/alerts', label: 'Alerts', icon: <Warning /> },
    { path: '/predictions', label: 'Analytics', icon: <TrendingUp /> },
    { path: '/maps', label: 'Maps', icon: <Map /> }
  ];

  return (
    <AppBar position="static" elevation={0} sx={{ mb: 3 }}>
      <Toolbar sx={{ px: 3, py: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexGrow: 1 }}>
          <Avatar sx={{ bgcolor: 'primary.main', width: 40, height: 40 }}>
            <LocalHospital />
          </Avatar>
          <Box>
            <Typography 
              variant="h6" 
              component="div" 
              sx={{ 
                fontWeight: 700,
                color: 'text.primary',
                lineHeight: 1.2
              }}
            >
              Smart Health Surveillance
            </Typography>
            <Typography 
              variant="caption" 
              sx={{ 
                color: 'text.secondary',
                fontWeight: 500
              }}
            >
              Early Warning System
            </Typography>
          </Box>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 0.5, mr: 3 }}>
          {menuItems.map((item) => (
            <Button
              key={item.path}
              startIcon={item.icon}
              onClick={() => navigate(item.path)}
              variant={location.pathname === item.path ? 'contained' : 'text'}
              sx={{
                borderRadius: 2,
                px: 2,
                py: 1,
                fontWeight: 600,
                fontSize: '0.875rem',
                color: location.pathname === item.path ? 'white' : 'text.secondary',
                '&:hover': {
                  backgroundColor: location.pathname === item.path ? 'primary.dark' : 'grey.100'
                }
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Button
            onClick={toggleTheme}
            sx={{ minWidth: 'auto', p: 1, borderRadius: 2 }}
            color="inherit"
          >
            {isDark ? <LightMode /> : <DarkMode />}
          </Button>
          <Chip
            icon={<Circle sx={{ fontSize: '8px !important' }} />}
            label="System Online"
            color="success"
            variant="outlined"
            size="small"
            sx={{ fontWeight: 600, fontSize: '0.75rem' }}
          />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;