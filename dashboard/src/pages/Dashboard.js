import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent
} from '@mui/material';
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

const Dashboard = () => {
  const [healthStats, setHealthStats] = useState({});
  const [alertStats, setAlertStats] = useState({});
  const [waterStats, setWaterStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
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

  const StatCard = ({ title, value, color, subtitle }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography color="textSecondary" gutterBottom variant="h6">
          {title}
        </Typography>
        <Typography variant="h3" component="div" sx={{ color }}>
          {value}
        </Typography>
        {subtitle && (
          <Typography color="textSecondary" variant="body2">
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography>Loading dashboard...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Health Surveillance Dashboard
      </Typography>
      
      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Reports"
            value={healthStats.total_reports || 0}
            color="#2E8B57"
            subtitle="This month"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Active Alerts"
            value={alertStats.total_active_alerts || 0}
            color="#FF6B6B"
            subtitle="Requiring attention"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Contaminated Sources"
            value={waterStats.contaminated_sources || 0}
            color="#FFE66D"
            subtitle="Water sources"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Recent Reports"
            value={healthStats.recent_reports || 0}
            color="#4ECDC4"
            subtitle="Last 7 days"
          />
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        {/* Disease Distribution */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Disease Distribution
            </Typography>
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
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Case Severity Levels
            </Typography>
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
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Alert Severity Distribution
            </Typography>
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

        {/* Water Quality Trends */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Water Quality Trends
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', height: '90%', justifyContent: 'center', alignItems: 'center' }}>
              <Typography variant="h4" color="primary">
                {((waterStats.safe_sources || 0) / Math.max(waterStats.total_sources || 1, 1) * 100).toFixed(1)}%
              </Typography>
              <Typography variant="body1" color="textSecondary">
                Safe Water Sources
              </Typography>
              <Typography variant="body2" sx={{ mt: 2 }}>
                {waterStats.total_sources || 0} sources tested
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;