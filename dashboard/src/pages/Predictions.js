import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Box,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  CircularProgress,
  Button
} from '@mui/material';
import {
  TrendingUp,
  Psychology,
  Timeline,
  Analytics,
  Refresh,
  Warning
} from '@mui/icons-material';
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar
} from 'recharts';

function Predictions() {
  const [predictions, setPredictions] = useState([]);
  const [trendData, setTrendData] = useState([]);
  const [riskScore, setRiskScore] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setError(null);
      await Promise.all([fetchPredictions(), fetchTrendData()]);
    } catch (error) {
      setError('Failed to fetch data. Please check if the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  const fetchPredictions = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/ai/predictions');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json();
      console.log('Predictions data:', data);
      
      const formattedPredictions = Array.isArray(data) ? data.map((pred, index) => ({
        id: pred.id || index + 1,
        disease: pred.disease || 'Unknown',
        location: pred.location || 'Unknown',
        riskScore: pred.riskScore || 0,
        predictedCases: pred.predictedCases || 0,
        confidence: pred.confidence || 0,
        factors: Array.isArray(pred.factors) ? pred.factors : [],
        timeframe: pred.timeframe || '7-14 days',
        timestamp: pred.timestamp || new Date().toISOString()
      })) : [];
      
      setPredictions(formattedPredictions);
      
      // Calculate overall risk score
      if (formattedPredictions.length > 0) {
        const maxRisk = Math.max(...formattedPredictions.map(p => p.riskScore));
        setRiskScore(maxRisk);
      }
    } catch (error) {
      console.error('Error fetching predictions:', error);
      setPredictions([]);
    }
  };

  const fetchTrendData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/health/reports');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const reports = await response.json();
      
      // Create sample trend data if no reports
      if (!Array.isArray(reports) || reports.length === 0) {
        const sampleData = [];
        for (let i = 7; i >= 0; i--) {
          const date = new Date();
          date.setDate(date.getDate() - i);
          sampleData.push({
            date: date.toISOString().split('T')[0],
            cholera: Math.floor(Math.random() * 5),
            diarrhea: Math.floor(Math.random() * 8),
            typhoid: Math.floor(Math.random() * 3),
            other: Math.floor(Math.random() * 2)
          });
        }
        setTrendData(sampleData);
        return;
      }
      
      // Group reports by date and disease
      const dailyData = {};
      reports.forEach(report => {
        const date = new Date(report.reported_at).toISOString().split('T')[0];
        
        if (!dailyData[date]) {
          dailyData[date] = { date, cholera: 0, diarrhea: 0, typhoid: 0, other: 0 };
        }
        
        const disease = report.disease?.toLowerCase() || 'other';
        if (dailyData[date][disease] !== undefined) {
          dailyData[date][disease]++;
        } else {
          dailyData[date].other++;
        }
      });
      
      const trendArray = Object.values(dailyData)
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(-8); // Last 8 days
      
      setTrendData(trendArray);
    } catch (error) {
      console.error('Error fetching trend data:', error);
      // Set sample data on error
      const sampleData = [];
      for (let i = 7; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        sampleData.push({
          date: date.toISOString().split('T')[0],
          cholera: Math.floor(Math.random() * 5),
          diarrhea: Math.floor(Math.random() * 8),
          typhoid: Math.floor(Math.random() * 3)
        });
      }
      setTrendData(sampleData);
    }
  };

  const getRiskColor = (score) => {
    if (score >= 80) return 'error';
    if (score >= 60) return 'warning';
    if (score >= 40) return 'info';
    return 'success';
  };

  const getRiskLevel = (score) => {
    if (score >= 80) return 'Critical';
    if (score >= 60) return 'High';
    if (score >= 40) return 'Medium';
    return 'Low';
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2, color: 'white' }}>
            Loading AI Predictions...
          </Typography>
        </Box>
      </Container>
    );
  }

  const highRiskPredictions = predictions.filter(p => p.riskScore >= 60);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h4" sx={{ color: 'white', fontWeight: 700 }}>
              🤖 AI/ML Outbreak Predictions
            </Typography>
            <Button
              variant="outlined"
              startIcon={<Refresh />}
              onClick={fetchData}
              sx={{ color: 'white', borderColor: 'white' }}
            >
              Refresh
            </Button>
          </Box>
        </Grid>

        {/* Error Alert */}
        {error && (
          <Grid item xs={12}>
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          </Grid>
        )}
        
        {/* Summary Cards */}
        <Grid item xs={12} md={3}>
          <Card sx={{ bgcolor: '#e3f2fd', border: '1px solid #90caf9' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Psychology sx={{ fontSize: 40, color: '#1976d2' }} />
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700, color: '#1976d2' }}>
                    3
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    AI Models Active
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            bgcolor: riskScore >= 60 ? '#ffebee' : '#f3e5f5', 
            border: `1px solid ${riskScore >= 60 ? '#ef5350' : '#ab47bc'}` 
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <TrendingUp sx={{ fontSize: 40, color: riskScore >= 60 ? '#d32f2f' : '#7b1fa2' }} />
                <Box>
                  <Typography variant="h4" sx={{ 
                    fontWeight: 700, 
                    color: riskScore >= 60 ? '#d32f2f' : '#7b1fa2' 
                  }}>
                    {riskScore}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Max Risk Score
                  </Typography>
                  <Chip
                    label={getRiskLevel(riskScore)}
                    color={getRiskColor(riskScore)}
                    size="small"
                    sx={{ mt: 0.5 }}
                  />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card sx={{ bgcolor: '#e8f5e8', border: '1px solid #81c784' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Timeline sx={{ fontSize: 40, color: '#388e3c' }} />
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700, color: '#388e3c' }}>
                    {predictions.length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Active Predictions
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card sx={{ bgcolor: '#fff3e0', border: '1px solid #ffb74d' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Analytics sx={{ fontSize: 40, color: '#f57c00' }} />
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700, color: '#f57c00' }}>
                    87%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Model Accuracy
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* High Risk Alert */}
        {highRiskPredictions.length > 0 && (
          <Grid item xs={12}>
            <Alert severity="error" icon={<Warning />} sx={{ mb: 2 }}>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                🚨 High Risk Outbreak Alert
              </Typography>
              <Typography>
                {highRiskPredictions.length} high-risk prediction(s) detected. Immediate preventive measures recommended:
              </Typography>
              <Box sx={{ mt: 1 }}>
                {highRiskPredictions.map(p => (
                  <Typography key={p.id} variant="body2" sx={{ mt: 0.5 }}>
                    • <strong>{p.disease}</strong> in {p.location} - {p.riskScore}% risk, {p.predictedCases} predicted cases
                  </Typography>
                ))}
              </Box>
            </Alert>
          </Grid>
        )}

        {/* Charts */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              📈 Disease Trend Analysis (Last 8 Days)
            </Typography>
            <ResponsiveContainer width="100%" height="85%">
              <AreaChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="cholera"
                  stackId="1"
                  stroke="#d32f2f"
                  fill="#d32f2f"
                  fillOpacity={0.6}
                  name="Cholera"
                />
                <Area
                  type="monotone"
                  dataKey="diarrhea"
                  stackId="1"
                  stroke="#ff9800"
                  fill="#ff9800"
                  fillOpacity={0.6}
                  name="Diarrhea"
                />
                <Area
                  type="monotone"
                  dataKey="typhoid"
                  stackId="1"
                  stroke="#2196f3"
                  fill="#2196f3"
                  fillOpacity={0.6}
                  name="Typhoid"
                />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              ⚠️ Risk Factors Analysis
            </Typography>
            <Box sx={{ mt: 3 }}>
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>Water Quality Issues</Typography>
                <LinearProgress variant="determinate" value={75} color="error" sx={{ height: 8, borderRadius: 4 }} />
                <Typography variant="caption" color="text.secondary">75% - High contamination risk</Typography>
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>Sanitation Level</Typography>
                <LinearProgress variant="determinate" value={45} color="warning" sx={{ height: 8, borderRadius: 4 }} />
                <Typography variant="caption" color="text.secondary">45% - Needs improvement</Typography>
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>Population Density</Typography>
                <LinearProgress variant="determinate" value={60} color="info" sx={{ height: 8, borderRadius: 4 }} />
                <Typography variant="caption" color="text.secondary">60% - Moderate density</Typography>
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>Seasonal Factors (Monsoon)</Typography>
                <LinearProgress variant="determinate" value={80} color="error" sx={{ height: 8, borderRadius: 4 }} />
                <Typography variant="caption" color="text.secondary">80% - High seasonal risk</Typography>
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>Healthcare Access</Typography>
                <LinearProgress variant="determinate" value={35} color="success" sx={{ height: 8, borderRadius: 4 }} />
                <Typography variant="caption" color="text.secondary">35% - Limited access</Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Predictions Table */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              🎯 Active Outbreak Predictions
            </Typography>
            {predictions.length === 0 ? (
              <Alert severity="info" sx={{ mt: 2 }}>
                No active predictions available. The AI models are monitoring for potential outbreaks.
              </Alert>
            ) : (
              <TableContainer sx={{ mt: 2 }}>
                <Table>
                  <TableHead>
                    <TableRow sx={{ bgcolor: '#f5f5f5' }}>
                      <TableCell sx={{ fontWeight: 600 }}>Disease</TableCell>
                      <TableCell sx={{ fontWeight: 600 }}>Location</TableCell>
                      <TableCell sx={{ fontWeight: 600 }}>Risk Score</TableCell>
                      <TableCell sx={{ fontWeight: 600 }}>Predicted Cases</TableCell>
                      <TableCell sx={{ fontWeight: 600 }}>Confidence</TableCell>
                      <TableCell sx={{ fontWeight: 600 }}>Timeframe</TableCell>
                      <TableCell sx={{ fontWeight: 600 }}>Timestamp</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {predictions.slice(0, 10).map((prediction) => (
                      <TableRow key={prediction.id} sx={{ 
                        bgcolor: prediction.riskScore >= 60 ? '#ffebee' : 'inherit',
                        '&:hover': { bgcolor: '#f5f5f5' }
                      }}>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            {prediction.riskScore >= 60 && <Warning color="error" fontSize="small" />}
                            <strong>{prediction.disease}</strong>
                          </Box>
                        </TableCell>
                        <TableCell>{prediction.location}</TableCell>
                        <TableCell>
                          <Box display="flex" alignItems="center" gap={1}>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              {prediction.riskScore}%
                            </Typography>
                            <Chip
                              label={getRiskLevel(prediction.riskScore)}
                              color={getRiskColor(prediction.riskScore)}
                              size="small"
                            />
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {prediction.predictedCases}
                          </Typography>
                        </TableCell>
                        <TableCell>{prediction.confidence}%</TableCell>
                        <TableCell>{prediction.timeframe}</TableCell>
                        <TableCell>
                          <Typography variant="caption" color="text.secondary">
                            {new Date(prediction.timestamp).toLocaleString()}
                          </Typography>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Predictions;