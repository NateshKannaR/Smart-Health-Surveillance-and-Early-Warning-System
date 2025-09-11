import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Chip,
  LinearProgress
} from '@mui/material';
import {
  TrendingUp,
  Warning,
  WaterDrop,
  HealthAndSafety,
  Assessment
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer
} from 'recharts';
import { getHealthStats, getAlertStats, getWaterQualityStats } from '../services/apiService';
import LoadingScreen from '../components/LoadingScreen';

const Dashboard = () => {
  const [healthStats, setHealthStats] = useState({});
  const [alertStats, setAlertStats] = useState({});
  const [waterStats, setWaterStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      const [health, alerts, water] = await Promise.all([
        getHealthStats(),
        getAlertStats(),
        getWaterQualityStats()
      ]);
      
      setHealthStats(health);
      setAlertStats(alerts);
      setWaterStats(water);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const diseaseData = Object.entries(healthStats.by_disease || {}).map(([disease, count]) => ({
    name: disease.replace('_', ' ').toUpperCase(),
    value: count
  }));

  const severityData = Object.entries(healthStats.by_severity || {}).map(([severity, count]) => ({
    name: severity.toUpperCase(),
    count
  }));

  const alertSeverityData = Object.entries(alertStats.by_severity || {}).map(([severity, count]) => ({
    name: severity.toUpperCase(),
    value: count
  }));

  const COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'];

  const StatCard = ({ title, value, color, subtitle, icon, trend }) => (
    <Card sx={{ 
      height: '100%',
      position: 'relative',
      overflow: 'visible',
      '&::before': {
        content: '""',
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: 4,
        background: color,
        borderRadius: '12px 12px 0 0'
      }
    }}>
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box>
            <Typography 
              color="text.secondary" 
              variant="body2" 
              sx={{ 
                fontWeight: 600, 
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                fontSize: '0.75rem'
              }}
            >
              {title}
            </Typography>
            <Typography 
              variant="h3" 
              component="div" 
              sx={{ 
                color: 'text.primary',
                fontWeight: 700,
                mt: 1,
                lineHeight: 1
              }}
            >
              {value}
            </Typography>
          </Box>
          {icon && (
            <Box sx={{ 
              p: 1.5, 
              borderRadius: 2, 
              backgroundColor: `${color}15`,
              color: color
            }}>
              {icon}
            </Box>
          )}
        </Box>
        {subtitle && (
          <Typography 
            color="text.secondary" 
            variant="body2"
            sx={{ fontWeight: 500 }}
          >
            {subtitle}
          </Typography>
        )}
        {trend && (
          <Box sx={{ display: 'flex', alignItems: 'center', mt: 1, gap: 0.5 }}>
            <Typography 
              variant="body2" 
              sx={{ 
                color: trend > 0 ? 'success.main' : 'error.main',
                fontWeight: 600
              }}
            >
              {trend > 0 ? '+' : ''}{trend}%
            </Typography>
            <Typography variant="body2" color="text.secondary">
              vs last month
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );

  if (loading) {
    return <LoadingScreen message="Loading Dashboard" />;
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography 
          variant="h4" 
          sx={{ 
            fontWeight: 700, 
            color: 'text.primary',
            mb: 1
          }}
        >
          Health Surveillance Overview
        </Typography>
        <Typography 
          variant="body1" 
          color="text.secondary"
          sx={{ fontWeight: 500 }}
        >
          Real-time monitoring and early warning system for water-borne diseases
        </Typography>
      </Box>
      
      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} lg={3}>
          <StatCard
            title="Total Health Reports"
            value={healthStats.total_reports || 0}
            color="#10b981"
            subtitle="Submitted this month"
            icon={<HealthAndSafety sx={{ fontSize: 28 }} />}
            trend={12}
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatCard
            title="Active Alerts"
            value={alertStats.total_active_alerts || 0}
            color="#ef4444"
            subtitle="Requiring immediate attention"
            icon={<Warning sx={{ fontSize: 28 }} />}
            trend={-8}
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatCard
            title="Water Sources Monitored"
            value={waterStats.total_sources || 0}
            color="#06b6d4"
            subtitle={`${waterStats.contaminated_sources || 0} contaminated`}
            icon={<WaterDrop sx={{ fontSize: 28 }} />}
            trend={5}
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatCard
            title="Recent Cases"
            value={healthStats.recent_reports || 0}
            color="#f59e0b"
            subtitle="Last 7 days"
            icon={<TrendingUp sx={{ fontSize: 28 }} />}
            trend={-15}
          />
        </Grid>
      </Grid>

      {/* System Health Overview */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12}>
          <Card>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  System Health Status
                </Typography>
                <Chip 
                  label="All Systems Operational" 
                  color="success" 
                  variant="outlined"
                  sx={{ fontWeight: 600 }}
                />
              </Box>
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1, fontWeight: 600 }}>
                      Water Quality Monitoring
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={((waterStats.safe_sources || 0) / Math.max(waterStats.total_sources || 1, 1)) * 100} 
                      sx={{ height: 8, borderRadius: 4, mb: 1 }}
                      color="success"
                    />
                    <Typography variant="body2" color="text.secondary">
                      {((waterStats.safe_sources || 0) / Math.max(waterStats.total_sources || 1, 1) * 100).toFixed(1)}% Safe Sources
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1, fontWeight: 600 }}>
                      Alert Response Rate
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={85} 
                      sx={{ height: 8, borderRadius: 4, mb: 1 }}
                      color="primary"
                    />
                    <Typography variant="body2" color="text.secondary">
                      85% Within 24 Hours
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1, fontWeight: 600 }}>
                      Data Collection Coverage
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={92} 
                      sx={{ height: 8, borderRadius: 4, mb: 1 }}
                      color="info"
                    />
                    <Typography variant="body2" color="text.secondary">
                      92% Geographic Coverage
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Analytics Charts */}
      <Grid container spacing={3}>
        {/* Disease Distribution */}
        <Grid item xs={12} lg={6}>
          <Paper sx={{ p: 3, height: 450 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
              <Assessment color="primary" />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Disease Distribution
              </Typography>
            </Box>
            <ResponsiveContainer width="100%" height="90%">
              <PieChart>
                <Pie
                  data={diseaseData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {diseaseData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Severity Levels */}
        <Grid item xs={12} lg={6}>
          <Paper sx={{ p: 3, height: 450 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
              <Warning color="warning" />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Case Severity Levels
              </Typography>
            </Box>
            <ResponsiveContainer width="100%" height="90%">
              <BarChart data={severityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#2E8B57" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Alert Severity */}
        <Grid item xs={12} lg={6}>
          <Paper sx={{ p: 3, height: 450 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
              <Warning color="error" />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Alert Severity Distribution
              </Typography>
            </Box>
            <ResponsiveContainer width="100%" height="90%">
              <PieChart>
                <Pie
                  data={alertSeverityData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label
                >
                  {alertSeverityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Water Quality Summary */}
        <Grid item xs={12} lg={6}>
          <Paper sx={{ p: 3, height: 450 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
              <WaterDrop color="info" />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Water Quality Overview
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', flexDirection: 'column', height: 'calc(100% - 80px)', justifyContent: 'center', alignItems: 'center' }}>
              <Box sx={{ textAlign: 'center', mb: 4 }}>
                <Typography variant="h2" color="primary.main" sx={{ fontWeight: 700, mb: 1 }}>
                  {((waterStats.safe_sources || 0) / Math.max(waterStats.total_sources || 1, 1) * 100).toFixed(1)}%
                </Typography>
                <Typography variant="h6" color="text.secondary" sx={{ fontWeight: 600 }}>
                  Safe Water Sources
                </Typography>
              </Box>
              <Grid container spacing={2} sx={{ width: '100%' }}>
                <Grid item xs={6}>
                  <Box sx={{ textAlign: 'center', p: 2, backgroundColor: 'success.light', borderRadius: 2 }}>
                    <Typography variant="h5" sx={{ fontWeight: 700, color: 'success.dark' }}>
                      {waterStats.safe_sources || 0}
                    </Typography>
                    <Typography variant="body2" color="success.dark">
                      Safe Sources
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6}>
                  <Box sx={{ textAlign: 'center', p: 2, backgroundColor: 'error.light', borderRadius: 2 }}>
                    <Typography variant="h5" sx={{ fontWeight: 700, color: 'error.dark' }}>
                      {waterStats.contaminated_sources || 0}
                    </Typography>
                    <Typography variant="body2" color="error.dark">
                      Contaminated
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;