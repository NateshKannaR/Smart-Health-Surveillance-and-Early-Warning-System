import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { saveOfflineData, syncOfflineData } from './offlineService';

const API_BASE_URL = 'http://10.219.166.94:8000/api'; // Your computer's IP

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('userToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.code === 'NETWORK_ERROR' || !error.response) {
      // Save data offline if network error
      console.log('Network error, saving data offline');
    }
    return Promise.reject(error);
  }
);

export const submitHealthReport = async (reportData) => {
  try {
    const response = await apiClient.post('/health/reports', reportData);
    return response.data;
  } catch (error) {
    // Save offline if API call fails
    await saveOfflineData('health_reports', reportData);
    throw error;
  }
};

export const submitWaterQualityReport = async (reportData) => {
  try {
    const response = await apiClient.post('/water/quality', reportData);
    return response.data;
  } catch (error) {
    await saveOfflineData('water_reports', reportData);
    throw error;
  }
};

export const getRecentAlerts = async (location) => {
  try {
    const response = await apiClient.get('/alerts', {
      params: { location, active_only: true }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch alerts:', error);
    return [];
  }
};

export const getHealthStats = async (location) => {
  try {
    const response = await apiClient.get('/health/reports/stats', {
      params: { location }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch health stats:', error);
    return {};
  }
};

export const getWaterQualityReports = async (location) => {
  try {
    const response = await apiClient.get('/water/quality', {
      params: { location }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch water quality reports:', error);
    return [];
  }
};

export const getPredictions = async (location) => {
  try {
    const response = await apiClient.get('/predictions/risk-assessment', {
      params: { location }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch predictions:', error);
    return {};
  }
};

export const registerUser = async (userData) => {
  try {
    const response = await apiClient.post('/users/register', userData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const syncOfflineReports = async () => {
  try {
    await syncOfflineData();
    console.log('Offline data synced successfully');
  } catch (error) {
    console.error('Failed to sync offline data:', error);
  }
};