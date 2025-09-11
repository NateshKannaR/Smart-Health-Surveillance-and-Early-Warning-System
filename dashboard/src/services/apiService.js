import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for better error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.message);
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - check if backend server is running on port 8000');
    }
    return Promise.reject(error);
  }
);

export const getHealthStats = async (location = null) => {
  try {
    const response = await apiClient.get('/health/reports/stats', {
      params: location ? { location } : {}
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch health stats:', error);
    return {
      total_reports: 0,
      by_disease: {},
      by_severity: { mild: 0, moderate: 0, severe: 0 },
      recent_reports: 0
    };
  }
};

export const getHealthReports = async (location = null, limit = 100) => {
  try {
    const response = await apiClient.get('/health/reports', {
      params: { location, limit }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch health reports:', error);
    return [];
  }
};

export const getWaterQualityReports = async (location = null) => {
  try {
    const response = await apiClient.get('/water/quality', {
      params: location ? { location } : {}
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch water quality reports:', error);
    return [];
  }
};

export const getWaterQualityStats = async () => {
  try {
    const response = await apiClient.get('/water/reports/stats');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch water quality stats:', error);
    return {
      total_sources: 0,
      safe_sources: 0,
      contaminated_sources: 0
    };
  }
};

export const getAlerts = async (location = null, activeOnly = true) => {
  try {
    const response = await apiClient.get('/alerts', {
      params: { location, active_only: activeOnly }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch alerts:', error);
    return [];
  }
};

export const getAlertStats = async () => {
  try {
    const response = await apiClient.get('/alerts/stats');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch alert stats:', error);
    return {
      total_active_alerts: 0,
      by_severity: { low: 0, medium: 0, high: 0, critical: 0 }
    };
  }
};

export const getPredictions = async (location = null) => {
  try {
    const response = await apiClient.get('/predictions/risk-assessment', {
      params: location ? { location } : {}
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch predictions:', error);
    return {};
  }
};

export const createAlert = async (alertData) => {
  try {
    const response = await apiClient.post('/alerts', alertData);
    return response.data;
  } catch (error) {
    console.error('Failed to create alert:', error);
    throw error;
  }
};

export const resolveAlert = async (alertId) => {
  try {
    const response = await apiClient.put(`/alerts/${alertId}/resolve`);
    return response.data;
  } catch (error) {
    console.error('Failed to resolve alert:', error);
    throw error;
  }
};

export const getContaminationHotspots = async () => {
  try {
    const response = await apiClient.get('/water/quality/hotspots');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch contamination hotspots:', error);
    return {};
  }
};

export const predictOutbreak = async (location) => {
  try {
    const response = await apiClient.post('/predictions/outbreak', null, {
      params: { location }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to predict outbreak:', error);
    throw error;
  }
};