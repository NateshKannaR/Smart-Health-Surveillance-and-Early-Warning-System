import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
  IconButton
} from '@mui/material';
import {
  Map,
  LocationOn,
  Refresh,
  HealthAndSafety,
  WaterDrop,
  Warning
} from '@mui/icons-material';
import LoadingScreen from '../components/LoadingScreen';

const Maps = () => {
  const [data, setData] = useState({ health: [], water: [], alerts: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [healthRes, waterRes, alertsRes] = await Promise.all([
        fetch('http://localhost:8000/api/health/reports'),
        fetch('http://localhost:8000/api/water/sources'),
        fetch('http://localhost:8000/api/alerts')
      ]);

      setData({
        health: healthRes.ok ? await healthRes.json() : [],
        water: waterRes.ok ? await waterRes.json() : [],
        alerts: alertsRes.ok ? await alertsRes.json() : []
      });
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  // Get location coordinates
  const getLocationCoords = (location) => {
    const coords = {
      'Guwahati': { lat: 26.1445, lng: 91.7362 },
      'Assam': { lat: 26.2006, lng: 92.9376 },
      'Shillong': { lat: 25.5788, lng: 91.8933 },
      'Meghalaya': { lat: 25.4670, lng: 91.3662 },
      'Imphal': { lat: 24.8170, lng: 93.9368 },
      'Manipur': { lat: 24.6637, lng: 93.9063 },
      'Aizawl': { lat: 23.7307, lng: 92.7173 },
      'Mizoram': { lat: 23.1645, lng: 92.9376 },
      'Kohima': { lat: 25.6751, lng: 94.1086 },
      'Nagaland': { lat: 26.1584, lng: 94.5624 },
      'Agartala': { lat: 23.8315, lng: 91.2868 },
      'Tripura': { lat: 23.9408, lng: 91.9882 },
      'Itanagar': { lat: 27.0844, lng: 93.6053 },
      'Arunachal Pradesh': { lat: 28.2180, lng: 94.7278 },
      'Coimbatore': { lat: 11.0168, lng: 76.9558 },
      'Delhi': { lat: 28.6139, lng: 77.2090 },
      'Mumbai': { lat: 19.0760, lng: 72.8777 },
      'TestCity': { lat: 26.9124, lng: 75.7873 }
    };
    
    for (let place in coords) {
      if (location && location.toLowerCase().includes(place.toLowerCase())) {
        return coords[place];
      }
    }
    return null;
  };

  // Get severity level for location
  const getLocationSeverity = (location) => {
    const healthCount = data.health.filter(h => h.location && h.location.toLowerCase().includes(location.toLowerCase())).length;
    const severeHealth = data.health.filter(h => h.location && h.location.toLowerCase().includes(location.toLowerCase()) && h.severity === 'severe').length;
    const waterIssues = data.water.filter(w => w.location && w.location.toLowerCase().includes(location.toLowerCase()) && !w.is_safe).length;
    const alerts = data.alerts.filter(a => a.location && a.location.toLowerCase().includes(location.toLowerCase())).length;
    
    const totalIssues = healthCount + waterIssues + alerts + (severeHealth * 2);
    
    if (totalIssues >= 5) return 'critical';
    if (totalIssues >= 3) return 'high';
    if (totalIssues >= 1) return 'medium';
    return 'low';
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return '#FF0000';
      case 'high': return '#FF6600';
      case 'medium': return '#FFAA00';
      case 'low': return '#00FF00';
      default: return '#CCCCCC';
    }
  };

  const getSeveritySize = (severity) => {
    switch (severity) {
      case 'critical': return '20px';
      case 'high': return '16px';
      case 'medium': return '12px';
      case 'low': return '8px';
      default: return '6px';
    }
  };

  // Get unique locations from data
  const getUniqueLocations = () => {
    const locations = new Set();
    data.health.forEach(h => h.location && locations.add(h.location));
    data.water.forEach(w => w.location && locations.add(w.location));
    data.alerts.forEach(a => a.location && locations.add(a.location));
    return Array.from(locations);
  };

  if (loading) return <LoadingScreen message="Loading Map Data" />;

  const uniqueLocations = getUniqueLocations();

  return (
    <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box>
            <Typography 
              variant="h4" 
              sx={{ 
                fontWeight: 700, 
                color: 'text.primary',
                mb: 1,
                display: 'flex',
                alignItems: 'center',
                gap: 1
              }}
            >
              <Map color="primary" />
              Real-Time Health Surveillance Map
            </Typography>
            <Typography 
              variant="body1" 
              color="text.secondary"
              sx={{ fontWeight: 500 }}
            >
              Interactive map showing health reports, water quality, and active alerts
            </Typography>
          </Box>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchData}
            sx={{ fontWeight: 600 }}
          >
            Refresh Data
          </Button>
        </Box>
      </Box>
      
      <Paper sx={{ p: 3, mb: 3, height: 500, position: 'relative' }}>
        <iframe
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3610234.5234!2d90.3563!3d25.5788!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x375a5f3c5b9c7c7d%3A0x2b1c8b9c5b9c7c7d!2sNortheast%20India!5e0!3m2!1sen!2sin!4v1234567890"
          width="100%"
          height="100%"
          style={{border: 0, borderRadius: 12}}
          allowFullScreen=""
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
        />
        
        {/* Dynamic location markers */}
        <div style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          right: '20px',
          bottom: '20px',
          pointerEvents: 'none'
        }}>
          {uniqueLocations.map((location, i) => {
            const coords = getLocationCoords(location);
            if (!coords) return null;
            
            const severity = getLocationSeverity(location);
            const healthCount = data.health.filter(h => h.location && h.location.toLowerCase().includes(location.toLowerCase())).length;
            const waterIssues = data.water.filter(w => w.location && w.location.toLowerCase().includes(location.toLowerCase()) && !w.is_safe).length;
            const alertCount = data.alerts.filter(a => a.location && a.location.toLowerCase().includes(location.toLowerCase())).length;
            
            // Calculate position on map (approximate)
            const mapWidth = 460;
            const mapHeight = 460;
            const x = ((coords.lng - 88) / 10) * mapWidth;
            const y = ((32 - coords.lat) / 10) * mapHeight;
            
            return (
              <div key={location} style={{
                position: 'absolute',
                left: `${Math.max(0, Math.min(90, x / mapWidth * 100))}%`,
                top: `${Math.max(0, Math.min(90, y / mapHeight * 100))}%`,
                transform: 'translate(-50%, -50%)'
              }}>
                {/* Main location marker */}
                <div style={{
                  width: getSeveritySize(severity),
                  height: getSeveritySize(severity),
                  background: getSeverityColor(severity),
                  borderRadius: '50%',
                  animation: severity === 'critical' ? 'pulse 1s infinite' : severity === 'high' ? 'pulse 2s infinite' : 'none',
                  boxShadow: `0 0 15px ${getSeverityColor(severity)}`,
                  border: '2px solid white',
                  cursor: 'pointer'
                }} title={`${location}: H:${healthCount} W:${waterIssues} A:${alertCount}`} />
                
                {/* Location label */}
                <div style={{
                  position: 'absolute',
                  top: '-25px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  background: 'rgba(0,0,0,0.8)',
                  color: 'white',
                  padding: '2px 6px',
                  borderRadius: '4px',
                  fontSize: '10px',
                  whiteSpace: 'nowrap',
                  fontWeight: 600,
                  fontFamily: 'Inter, sans-serif'
                }}>
                  {location.split(',')[0]}
                </div>
                
                {/* Health indicator */}
                {healthCount > 0 && (
                  <div style={{
                    position: 'absolute',
                    top: '-8px',
                    right: '-8px',
                    width: '8px',
                    height: '8px',
                    background: '#FF4444',
                    borderRadius: '50%',
                    animation: 'pulse 2s infinite'
                  }} />
                )}
                
                {/* Water indicator */}
                {waterIssues > 0 && (
                  <div style={{
                    position: 'absolute',
                    bottom: '-8px',
                    right: '-8px',
                    width: '8px',
                    height: '8px',
                    background: '#4444FF',
                    borderRadius: '50%',
                    animation: 'pulse 2s infinite 0.5s'
                  }} />
                )}
                
                {/* Alert indicator */}
                {alertCount > 0 && (
                  <div style={{
                    position: 'absolute',
                    bottom: '-8px',
                    left: '-8px',
                    width: '8px',
                    height: '8px',
                    background: '#FFA500',
                    borderRadius: '50%',
                    animation: 'pulse 1s infinite'
                  }} />
                )}
              </div>
            );
          })}
        </div>
      </Paper>

      {/* Real-time stats */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <HealthAndSafety color="error" />
                Health Reports by Location
              </Typography>
              {uniqueLocations.map(location => {
                const count = data.health.filter(h => h.location && h.location.toLowerCase().includes(location.toLowerCase())).length;
                const severity = getLocationSeverity(location);
                return count > 0 ? (
                  <Box key={location} sx={{
                    p: 1.5, 
                    mb: 1, 
                    borderRadius: 1,
                    borderLeft: 4,
                    borderColor: getSeverityColor(severity),
                    backgroundColor: 'grey.50'
                  }}>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      {location} - {count} cases
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Risk Level: {severity.toUpperCase()}
                    </Typography>
                  </Box>
                ) : null;
              })}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <WaterDrop color="info" />
                Water Quality by Location
              </Typography>
              {uniqueLocations.map(location => {
                const waterData = data.water.filter(w => w.location && w.location.toLowerCase().includes(location.toLowerCase()));
                const contaminated = waterData.filter(w => !w.is_safe).length;
                return waterData.length > 0 ? (
                  <Box key={location} sx={{
                    p: 1.5, 
                    mb: 1, 
                    borderRadius: 1,
                    backgroundColor: 'grey.50'
                  }}>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      {location}
                    </Typography>
                    <Typography variant="caption" color={contaminated > 0 ? 'error.main' : 'success.main'}>
                      {contaminated > 0 ? `❌ ${contaminated} contaminated` : '✅ All sources safe'}
                    </Typography>
                  </Box>
                ) : null;
              })}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Warning color="warning" />
                Active Alerts by Location
              </Typography>
              {uniqueLocations.map(location => {
                const alertData = data.alerts.filter(a => a.location && a.location.toLowerCase().includes(location.toLowerCase()));
                return alertData.length > 0 ? (
                  <Box key={location} sx={{
                    p: 1.5, 
                    mb: 1, 
                    borderRadius: 1,
                    backgroundColor: 'grey.50'
                  }}>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      {location} - {alertData.length} alerts
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Latest: {alertData[0]?.severity}
                    </Typography>
                  </Box>
                ) : null;
              })}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          🎯 Live Map Legend
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 20, height: 20, bgcolor: '#FF0000', borderRadius: '50%', border: '2px solid white' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>Critical Risk Area</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 16, height: 16, bgcolor: '#FF6600', borderRadius: '50%', border: '2px solid white' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>High Risk Area</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 12, height: 12, bgcolor: '#FFAA00', borderRadius: '50%', border: '2px solid white' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>Medium Risk Area</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 8, height: 8, bgcolor: '#00FF00', borderRadius: '50%', border: '2px solid white' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>Low Risk Area</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 8, height: 8, bgcolor: '#FF4444', borderRadius: '50%' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>Health Reports</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 8, height: 8, bgcolor: '#4444FF', borderRadius: '50%' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>Water Issues</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 8, height: 8, bgcolor: '#FFA500', borderRadius: '50%' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>Active Alerts</Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default Maps;