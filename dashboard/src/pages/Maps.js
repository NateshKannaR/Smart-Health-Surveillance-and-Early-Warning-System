import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Map as MapIcon,
  Refresh,
  HealthAndSafety,
  WaterDrop,
  Warning
} from '@mui/icons-material';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in React Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const Maps = () => {
  const [data, setData] = useState({ health: [], water: [], alerts: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setError(null);
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
      setError('Failed to fetch map data. Please check if the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  // Accurate location coordinates
  const getLocationCoords = (location) => {
    const coords = {
      // Major Indian cities
      'delhi': { lat: 28.6139, lng: 77.2090 },
      'mumbai': { lat: 19.0760, lng: 72.8777 },
      'bangalore': { lat: 12.9716, lng: 77.5946 },
      'chennai': { lat: 13.0827, lng: 80.2707 },
      'kolkata': { lat: 22.5726, lng: 88.3639 },
      'hyderabad': { lat: 17.3850, lng: 78.4867 },
      'pune': { lat: 18.5204, lng: 73.8567 },
      'ahmedabad': { lat: 23.0225, lng: 72.5714 },
      'jaipur': { lat: 26.9124, lng: 75.7873 },
      'lucknow': { lat: 26.8467, lng: 80.9462 },
      
      // Northeast India
      'guwahati': { lat: 26.1445, lng: 91.7362 },
      'assam': { lat: 26.2006, lng: 92.9376 },
      'shillong': { lat: 25.5788, lng: 91.8933 },
      'meghalaya': { lat: 25.4670, lng: 91.3662 },
      'imphal': { lat: 24.8170, lng: 93.9368 },
      'manipur': { lat: 24.6637, lng: 93.9063 },
      'aizawl': { lat: 23.7307, lng: 92.7173 },
      'mizoram': { lat: 23.1645, lng: 92.9376 },
      'kohima': { lat: 25.6751, lng: 94.1086 },
      'nagaland': { lat: 26.1584, lng: 94.5624 },
      'agartala': { lat: 23.8315, lng: 91.2868 },
      'tripura': { lat: 23.9408, lng: 91.9882 },
      'itanagar': { lat: 27.0844, lng: 93.6053 },
      'arunachal pradesh': { lat: 28.2180, lng: 94.7278 },
      
      // Test locations
      'test location': { lat: 26.9124, lng: 75.7873 },
      'testcity': { lat: 26.9124, lng: 75.7873 }
    };
    
    if (!location) return null;
    
    const locationKey = location.toLowerCase().trim();
    
    // Direct match
    if (coords[locationKey]) {
      return coords[locationKey];
    }
    
    // Partial match
    for (let place in coords) {
      if (locationKey.includes(place) || place.includes(locationKey)) {
        return coords[place];
      }
    }
    
    return null;
  };

  // Get severity level for location
  const getLocationSeverity = (location) => {
    const healthCount = data.health.filter(h => 
      h.location && h.location.toLowerCase().includes(location.toLowerCase())
    ).length;
    
    const severeHealth = data.health.filter(h => 
      h.location && h.location.toLowerCase().includes(location.toLowerCase()) && 
      h.severity === 'severe'
    ).length;
    
    const waterIssues = data.water.filter(w => 
      w.location && w.location.toLowerCase().includes(location.toLowerCase()) && 
      !w.is_safe
    ).length;
    
    const criticalAlerts = data.alerts.filter(a => 
      a.location && a.location.toLowerCase().includes(location.toLowerCase()) && 
      a.severity === 'critical'
    ).length;
    
    const highAlerts = data.alerts.filter(a => 
      a.location && a.location.toLowerCase().includes(location.toLowerCase()) && 
      a.severity === 'high'
    ).length;
    
    const totalScore = (severeHealth * 3) + (criticalAlerts * 3) + (highAlerts * 2) + healthCount + waterIssues;
    
    if (totalScore >= 8 || criticalAlerts > 0) return 'critical';
    if (totalScore >= 5 || severeHealth > 2) return 'high';
    if (totalScore >= 2) return 'medium';
    return 'low';
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return '#dc2626';
      case 'high': return '#ea580c';
      case 'medium': return '#d97706';
      case 'low': return '#16a34a';
      default: return '#6b7280';
    }
  };

  const getSeverityRadius = (severity) => {
    switch (severity) {
      case 'critical': return 25;
      case 'high': return 20;
      case 'medium': return 15;
      case 'low': return 10;
      default: return 8;
    }
  };

  // Get unique locations with coordinates
  const getLocationData = () => {
    const locationMap = new Map();
    
    // Process all data sources
    [...data.health, ...data.water, ...data.alerts].forEach(item => {
      if (item.location) {
        const coords = getLocationCoords(item.location);
        if (coords) {
          const key = item.location.toLowerCase().trim();
          if (!locationMap.has(key)) {
            locationMap.set(key, {
              name: item.location,
              coords: coords,
              health: [],
              water: [],
              alerts: []
            });
          }
        }
      }
    });
    
    // Populate data for each location
    locationMap.forEach((locationData, key) => {
      locationData.health = data.health.filter(h => 
        h.location && h.location.toLowerCase().includes(key)
      );
      locationData.water = data.water.filter(w => 
        w.location && w.location.toLowerCase().includes(key)
      );
      locationData.alerts = data.alerts.filter(a => 
        a.location && a.location.toLowerCase().includes(key)
      );
    });
    
    return Array.from(locationMap.values());
  };

  if (loading) {
    return (
      <Container maxWidth="xl" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>Loading Map Data...</Typography>
        </Box>
      </Container>
    );
  }

  const locationData = getLocationData();

  return (
    <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
      {/* Header */}
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
              <MapIcon color="primary" />
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

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {/* Interactive Map */}
      <Paper sx={{ p: 0, mb: 3, height: 500, overflow: 'hidden', borderRadius: 2 }}>
        <MapContainer
          center={[23.5937, 78.9629]} // Center of India
          zoom={5}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {locationData.map((location, index) => {
            const severity = getLocationSeverity(location.name);
            const healthCount = location.health.length;
            const waterIssues = location.water.filter(w => !w.is_safe).length;
            const alertCount = location.alerts.length;
            
            return (
              <CircleMarker
                key={index}
                center={[location.coords.lat, location.coords.lng]}
                radius={getSeverityRadius(severity)}
                fillColor={getSeverityColor(severity)}
                color="white"
                weight={2}
                opacity={1}
                fillOpacity={0.7}
              >
                <Popup>
                  <Box sx={{ minWidth: 200 }}>
                    <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                      📍 {location.name}
                    </Typography>
                    
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      <strong>Risk Level:</strong> 
                      <span style={{ 
                        color: getSeverityColor(severity), 
                        fontWeight: 600,
                        marginLeft: 4
                      }}>
                        {severity.toUpperCase()}
                      </span>
                    </Typography>
                    
                    <Box sx={{ mb: 1 }}>
                      <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <HealthAndSafety fontSize="small" color="error" />
                        Health Reports: <strong>{healthCount}</strong>
                      </Typography>
                      {healthCount > 0 && (
                        <Typography variant="caption" color="text.secondary" sx={{ ml: 3 }}>
                          Severe cases: {location.health.filter(h => h.severity === 'severe').length}
                        </Typography>
                      )}
                    </Box>
                    
                    <Box sx={{ mb: 1 }}>
                      <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <WaterDrop fontSize="small" color="info" />
                        Water Sources: <strong>{location.water.length}</strong>
                      </Typography>
                      {waterIssues > 0 && (
                        <Typography variant="caption" color="error.main" sx={{ ml: 3 }}>
                          ⚠️ {waterIssues} contaminated
                        </Typography>
                      )}
                    </Box>
                    
                    <Box>
                      <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Warning fontSize="small" color="warning" />
                        Active Alerts: <strong>{alertCount}</strong>
                      </Typography>
                      {alertCount > 0 && (
                        <Typography variant="caption" color="text.secondary" sx={{ ml: 3 }}>
                          Latest: {location.alerts[0]?.severity}
                        </Typography>
                      )}
                    </Box>
                  </Box>
                </Popup>
              </CircleMarker>
            );
          })}
        </MapContainer>
      </Paper>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <HealthAndSafety color="error" />
                Health Reports ({data.health.length})
              </Typography>
              {locationData.filter(l => l.health.length > 0).map(location => {
                const severity = getLocationSeverity(location.name);
                const severeCount = location.health.filter(h => h.severity === 'severe').length;
                return (
                  <Box key={location.name} sx={{
                    p: 1.5, 
                    mb: 1, 
                    borderRadius: 1,
                    borderLeft: 4,
                    borderColor: getSeverityColor(severity),
                    backgroundColor: 'grey.50'
                  }}>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      {location.name} - {location.health.length} cases
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {severeCount > 0 ? `⚠️ ${severeCount} severe` : '✅ No severe cases'}
                    </Typography>
                  </Box>
                );
              })}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <WaterDrop color="info" />
                Water Quality ({data.water.length})
              </Typography>
              {locationData.filter(l => l.water.length > 0).map(location => {
                const contaminated = location.water.filter(w => !w.is_safe).length;
                return (
                  <Box key={location.name} sx={{
                    p: 1.5, 
                    mb: 1, 
                    borderRadius: 1,
                    backgroundColor: 'grey.50'
                  }}>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      {location.name} - {location.water.length} sources
                    </Typography>
                    <Typography variant="caption" color={contaminated > 0 ? 'error.main' : 'success.main'}>
                      {contaminated > 0 ? `❌ ${contaminated} contaminated` : '✅ All sources safe'}
                    </Typography>
                  </Box>
                );
              })}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Warning color="warning" />
                Active Alerts ({data.alerts.length})
              </Typography>
              {locationData.filter(l => l.alerts.length > 0).map(location => (
                <Box key={location.name} sx={{
                  p: 1.5, 
                  mb: 1, 
                  borderRadius: 1,
                  backgroundColor: 'grey.50'
                }}>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    {location.name} - {location.alerts.length} alerts
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Latest: {location.alerts[0]?.severity}
                  </Typography>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Map Legend */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          🎯 Map Legend
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 25, height: 25, bgcolor: '#dc2626', borderRadius: '50%', border: '2px solid white' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>Critical Risk</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 20, height: 20, bgcolor: '#ea580c', borderRadius: '50%', border: '2px solid white' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>High Risk</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 15, height: 15, bgcolor: '#d97706', borderRadius: '50%', border: '2px solid white' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>Medium Risk</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 10, height: 10, bgcolor: '#16a34a', borderRadius: '50%', border: '2px solid white' }} />
              <Typography variant="body2" sx={{ fontWeight: 500 }}>Low Risk</Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default Maps;