import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Box,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ToggleButton,
  ToggleButtonGroup
} from '@mui/material';
import {
  LocationOn,
  WaterDrop,
  LocalHospital,
  Warning,
  Layers
} from '@mui/icons-material';

function Maps() {
  const [mapLayer, setMapLayer] = useState('health');
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    // Mock location data
    const mockLocations = [
      {
        id: 1,
        name: 'Village A',
        type: 'village',
        lat: 12.345,
        lng: 67.890,
        healthReports: 15,
        waterSources: 3,
        alerts: 1,
        status: 'safe'
      },
      {
        id: 2,
        name: 'Village B',
        type: 'village',
        lat: 12.355,
        lng: 67.895,
        healthReports: 28,
        waterSources: 2,
        alerts: 3,
        status: 'high_risk'
      },
      {
        id: 3,
        name: 'Health Center 1',
        type: 'health_facility',
        lat: 12.350,
        lng: 67.892,
        capacity: 50,
        staff: 8,
        supplies: 'adequate'
      },
      {
        id: 4,
        name: 'Water Source A',
        type: 'water_source',
        lat: 12.348,
        lng: 67.888,
        quality: 'safe',
        ph: 7.2,
        lastTested: '2024-01-15'
      },
      {
        id: 5,
        name: 'Water Source B',
        type: 'water_source',
        lat: 12.352,
        lng: 67.897,
        quality: 'contaminated',
        ph: 5.8,
        lastTested: '2024-01-14'
      }
    ];
    
    setLocations(mockLocations);
  }, []);

  const handleLayerChange = (event, newLayer) => {
    if (newLayer !== null) {
      setMapLayer(newLayer);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'safe': return 'success';
      case 'moderate_risk': return 'warning';
      case 'high_risk': return 'error';
      case 'contaminated': return 'error';
      case 'adequate': return 'success';
      default: return 'default';
    }
  };

  const getLocationIcon = (type) => {
    switch (type) {
      case 'village': return <LocationOn />;
      case 'health_facility': return <LocalHospital />;
      case 'water_source': return <WaterDrop />;
      default: return <LocationOn />;
    }
  };

  const filteredLocations = locations.filter(location => {
    switch (mapLayer) {
      case 'health': return location.type === 'village' || location.type === 'health_facility';
      case 'water': return location.type === 'water_source';
      case 'alerts': return location.alerts > 0;
      default: return true;
    }
  });

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom sx={{ color: 'white', mb: 3 }}>
            Geographic Health Mapping
          </Typography>
        </Grid>
        
        <Grid item xs={12}>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="h6">Map Layers</Typography>
              <ToggleButtonGroup
                value={mapLayer}
                exclusive
                onChange={handleLayerChange}
                size="small"
              >
                <ToggleButton value="health">
                  <LocalHospital sx={{ mr: 1 }} />
                  Health
                </ToggleButton>
                <ToggleButton value="water">
                  <WaterDrop sx={{ mr: 1 }} />
                  Water
                </ToggleButton>
                <ToggleButton value="alerts">
                  <Warning sx={{ mr: 1 }} />
                  Alerts
                </ToggleButton>
                <ToggleButton value="all">
                  <Layers sx={{ mr: 1 }} />
                  All
                </ToggleButton>
              </ToggleButtonGroup>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: 600 }}>
            <Typography variant="h6" gutterBottom>Interactive Map</Typography>
            <Box
              sx={{
                height: '90%',
                background: 'linear-gradient(45deg, #1a237e 30%, #3f51b5 90%)',
                borderRadius: 2,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                position: 'relative',
                overflow: 'hidden'
              }}
            >
              {/* Simulated map with location markers */}
              <Box
                sx={{
                  position: 'absolute',
                  width: '100%',
                  height: '100%',
                  background: `
                    radial-gradient(circle at 20% 30%, rgba(0, 230, 118, 0.3) 10%, transparent 10%),
                    radial-gradient(circle at 80% 20%, rgba(255, 64, 129, 0.3) 8%, transparent 8%),
                    radial-gradient(circle at 40% 70%, rgba(33, 150, 243, 0.3) 12%, transparent 12%),
                    radial-gradient(circle at 70% 80%, rgba(255, 193, 7, 0.3) 6%, transparent 6%),
                    radial-gradient(circle at 60% 40%, rgba(76, 175, 80, 0.3) 9%, transparent 9%)
                  `
                }}
              />
              
              {/* Location markers */}
              {filteredLocations.map((location, index) => (
                <Box
                  key={location.id}
                  sx={{
                    position: 'absolute',
                    left: `${20 + (index * 15)}%`,
                    top: `${30 + (index * 10)}%`,
                    transform: 'translate(-50%, -50%)',
                    zIndex: 10
                  }}
                >
                  <Chip
                    icon={getLocationIcon(location.type)}
                    label={location.name}
                    color={getStatusColor(location.status || location.quality || 'default')}
                    variant="filled"
                    sx={{ 
                      fontSize: '0.75rem',
                      '& .MuiChip-icon': { fontSize: '1rem' }
                    }}
                  />
                </Box>
              ))}
              
              <Typography variant="h6" color="white" sx={{ opacity: 0.7 }}>
                Interactive Map View
              </Typography>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: 600, overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>Location Details</Typography>
            <List>
              {filteredLocations.map((location) => (
                <ListItem
                  key={location.id}
                  sx={{
                    mb: 1,
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: 1,
                    backgroundColor: 'rgba(255,255,255,0.05)'
                  }}
                >
                  <ListItemIcon>
                    {getLocationIcon(location.type)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span style={{ fontSize: '1rem', fontWeight: 500 }}>{location.name}</span>
                        <Chip
                          label={location.type.replace('_', ' ')}
                          size="small"
                          variant="outlined"
                        />
                      </div>
                    }
                    secondary={
                      <div style={{ marginTop: 8 }}>
                        {location.type === 'village' && (
                          <>
                            <div style={{ fontSize: '0.875rem', marginBottom: 4 }}>
                              Health Reports: {location.healthReports}
                            </div>
                            <div style={{ fontSize: '0.875rem', marginBottom: 4 }}>
                              Water Sources: {location.waterSources}
                            </div>
                            <div style={{ fontSize: '0.875rem', marginBottom: 4 }}>
                              Active Alerts: {location.alerts}
                            </div>
                            <Chip
                              label={location.status}
                              color={getStatusColor(location.status)}
                              size="small"
                              sx={{ mt: 0.5 }}
                            />
                          </>
                        )}
                        {location.type === 'health_facility' && (
                          <>
                            <div style={{ fontSize: '0.875rem', marginBottom: 4 }}>
                              Capacity: {location.capacity} beds
                            </div>
                            <div style={{ fontSize: '0.875rem', marginBottom: 4 }}>
                              Staff: {location.staff} members
                            </div>
                            <Chip
                              label={location.supplies}
                              color={getStatusColor(location.supplies)}
                              size="small"
                              sx={{ mt: 0.5 }}
                            />
                          </>
                        )}
                        {location.type === 'water_source' && (
                          <>
                            <div style={{ fontSize: '0.875rem', marginBottom: 4 }}>
                              pH Level: {location.ph}
                            </div>
                            <div style={{ fontSize: '0.875rem', marginBottom: 4 }}>
                              Last Tested: {location.lastTested}
                            </div>
                            <Chip
                              label={location.quality}
                              color={getStatusColor(location.quality)}
                              size="small"
                              sx={{ mt: 0.5 }}
                            />
                          </>
                        )}
                        <div style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.7)', marginTop: 4 }}>
                          Coordinates: {location.lat}, {location.lng}
                        </div>
                      </div>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <LocationOn sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
                  <Typography variant="h6">Total Locations</Typography>
                  <Typography variant="h3" color="primary">{locations.length}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <LocalHospital sx={{ fontSize: 40, color: 'success.main', mb: 2 }} />
                  <Typography variant="h6">Health Facilities</Typography>
                  <Typography variant="h3" color="success.main">
                    {locations.filter(l => l.type === 'health_facility').length}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <WaterDrop sx={{ fontSize: 40, color: 'info.main', mb: 2 }} />
                  <Typography variant="h6">Water Sources</Typography>
                  <Typography variant="h3" color="info.main">
                    {locations.filter(l => l.type === 'water_source').length}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Warning sx={{ fontSize: 40, color: 'error.main', mb: 2 }} />
                  <Typography variant="h6">High Risk Areas</Typography>
                  <Typography variant="h3" color="error.main">
                    {locations.filter(l => l.status === 'high_risk' || l.quality === 'contaminated').length}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Maps;