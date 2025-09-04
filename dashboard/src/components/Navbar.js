import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  HealthAndSafety,
  WaterDrop,
  Warning,
  TrendingUp,
  Map
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: <DashboardIcon /> },
    { path: '/health-reports', label: 'Health Reports', icon: <HealthAndSafety /> },
    { path: '/water-quality', label: 'Water Quality', icon: <WaterDrop /> },
    { path: '/alerts', label: 'Alerts', icon: <Warning /> },
    { path: '/predictions', label: 'Predictions', icon: <TrendingUp /> },
    { path: '/maps', label: 'Maps', icon: <Map /> }
  ];

  return (
    <AppBar position="static" sx={{ mb: 2 }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Health Surveillance System
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          {menuItems.map((item) => (
            <Button
              key={item.path}
              color="inherit"
              startIcon={item.icon}
              onClick={() => navigate(item.path)}
              sx={{
                backgroundColor: location.pathname === item.path ? 'rgba(255,255,255,0.1)' : 'transparent',
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.2)'
                }
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;