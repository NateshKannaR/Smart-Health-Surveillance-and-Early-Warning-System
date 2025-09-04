import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Badge
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  CheckCircle,
  NotificationsActive,
  Send
} from '@mui/icons-material';

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({ active: 0, resolved: 0, critical: 0 });

  useEffect(() => {
    const mockAlerts = [
      {
        id: 1,
        type: 'outbreak_warning',
        severity: 'critical',
        title: 'Cholera Outbreak Alert',
        message: 'Multiple cholera cases reported in Village B. Immediate action required.',
        location: 'Village B',
        timestamp: '2024-01-15 14:30',
        status: 'active'
      },
      {
        id: 2,
        type: 'water_contamination',
        severity: 'high',
        title: 'Water Contamination Detected',
        message: 'High bacterial count detected in River B water source.',
        location: 'River B',
        timestamp: '2024-01-15 12:15',
        status: 'active'
      },
      {
        id: 3,
        type: 'resource_needed',
        severity: 'medium',
        title: 'Medical Supplies Low',
        message: 'ORS packets running low at Village A health center.',
        location: 'Village A',
        timestamp: '2024-01-15 09:45',
        status: 'active'
      },
      {
        id: 4,
        type: 'outbreak_warning',
        severity: 'low',
        title: 'Diarrhea Cases Increase',
        message: 'Slight increase in diarrhea cases in Village C.',
        location: 'Village C',
        timestamp: '2024-01-14 16:20',
        status: 'resolved'
      }
    ];
    
    setAlerts(mockAlerts);
    setStats({
      active: mockAlerts.filter(a => a.status === 'active').length,
      resolved: mockAlerts.filter(a => a.status === 'resolved').length,
      critical: mockAlerts.filter(a => a.severity === 'critical').length
    });
  }, []);

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical': return <Error color="error" />;
      case 'high': return <Warning color="warning" />;
      case 'medium': return <Info color="info" />;
      case 'low': return <CheckCircle color="success" />;
      default: return <Info />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const handleResolveAlert = (id) => {
    setAlerts(alerts.map(alert => 
      alert.id === id ? { ...alert, status: 'resolved' } : alert
    ));
  };

  const handleSendNotification = (alert) => {
    console.log('Sending notification for:', alert.title);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom sx={{ color: 'white', mb: 3 }}>
            Alert Management System
          </Typography>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Badge badgeContent={stats.active} color="error">
                <NotificationsActive sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
              </Badge>
              <Typography variant="h6">Active Alerts</Typography>
              <Typography variant="h3" color="error">{stats.active}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Error sx={{ fontSize: 40, color: 'error.main', mb: 2 }} />
              <Typography variant="h6">Critical Alerts</Typography>
              <Typography variant="h3" color="error">{stats.critical}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <CheckCircle sx={{ fontSize: 40, color: 'success.main', mb: 2 }} />
              <Typography variant="h6">Resolved</Typography>
              <Typography variant="h3" color="success.main">{stats.resolved}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Response Rate</Typography>
              <Typography variant="h3" color="primary">
                {((stats.resolved / (stats.active + stats.resolved)) * 100).toFixed(1)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Active Alerts</Typography>
            <List>
              {alerts.filter(alert => alert.status === 'active').map((alert) => (
                <ListItem
                  key={alert.id}
                  sx={{
                    mb: 2,
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: 2,
                    backgroundColor: 'rgba(255,255,255,0.05)'
                  }}
                >
                  <ListItemIcon>
                    {getSeverityIcon(alert.severity)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <span style={{ fontSize: '1.25rem', fontWeight: 500 }}>{alert.title}</span>
                        <Chip
                          label={alert.severity}
                          color={getSeverityColor(alert.severity)}
                          size="small"
                        />
                        <Chip
                          label={alert.location}
                          variant="outlined"
                          size="small"
                        />
                      </div>
                    }
                    secondary={
                      <>
                        <div style={{ marginTop: 8, fontSize: '0.875rem' }}>
                          {alert.message}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.7)', marginTop: 4 }}>
                          {alert.timestamp}
                        </div>
                      </>
                    }
                  />
                  <div style={{ display: 'flex', gap: 8 }}>
                    <IconButton
                      color="primary"
                      onClick={() => handleSendNotification(alert)}
                      title="Send Notification"
                    >
                      <Send />
                    </IconButton>
                    <IconButton
                      color="success"
                      onClick={() => handleResolveAlert(alert.id)}
                      title="Mark as Resolved"
                    >
                      <CheckCircle />
                    </IconButton>
                  </div>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Recent Resolved Alerts</Typography>
            <List>
              {alerts.filter(alert => alert.status === 'resolved').map((alert) => (
                <ListItem key={alert.id} sx={{ opacity: 0.7 }}>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary={alert.title}
                    secondary={`${alert.message} - Resolved on ${alert.timestamp}`}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Alerts;