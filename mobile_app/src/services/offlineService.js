import AsyncStorage from '@react-native-async-storage/async-storage';
import { submitHealthReport, submitWaterQualityReport } from './apiService';

const OFFLINE_KEYS = {
  HEALTH_REPORTS: 'offline_health_reports',
  WATER_REPORTS: 'offline_water_reports',
  USER_DATA: 'offline_user_data'
};

export const initializeOfflineStorage = async () => {
  try {
    // Initialize offline storage keys if they don't exist
    for (const key of Object.values(OFFLINE_KEYS)) {
      const existing = await AsyncStorage.getItem(key);
      if (!existing) {
        await AsyncStorage.setItem(key, JSON.stringify([]));
      }
    }
    console.log('Offline storage initialized');
  } catch (error) {
    console.error('Failed to initialize offline storage:', error);
  }
};

export const saveOfflineData = async (type, data) => {
  try {
    const key = type === 'health_reports' ? OFFLINE_KEYS.HEALTH_REPORTS : OFFLINE_KEYS.WATER_REPORTS;
    const existingData = await AsyncStorage.getItem(key);
    const dataArray = existingData ? JSON.parse(existingData) : [];
    
    // Add timestamp and unique ID
    const dataWithMeta = {
      ...data,
      offline_id: Date.now().toString(),
      created_offline: new Date().toISOString(),
      synced: false
    };
    
    dataArray.push(dataWithMeta);
    await AsyncStorage.setItem(key, JSON.stringify(dataArray));
    
    console.log(`Saved ${type} data offline:`, dataWithMeta.offline_id);
  } catch (error) {
    console.error('Failed to save offline data:', error);
  }
};

export const getOfflineData = async (type) => {
  try {
    const key = type === 'health_reports' ? OFFLINE_KEYS.HEALTH_REPORTS : OFFLINE_KEYS.WATER_REPORTS;
    const data = await AsyncStorage.getItem(key);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error('Failed to get offline data:', error);
    return [];
  }
};

export const syncOfflineData = async () => {
  try {
    // Sync health reports
    const healthReports = await getOfflineData('health_reports');
    const unsyncedHealthReports = healthReports.filter(report => !report.synced);
    
    for (const report of unsyncedHealthReports) {
      try {
        await submitHealthReport(report);
        // Mark as synced
        report.synced = true;
        report.synced_at = new Date().toISOString();
      } catch (error) {
        console.error('Failed to sync health report:', report.offline_id);
      }
    }
    
    // Sync water quality reports
    const waterReports = await getOfflineData('water_reports');
    const unsyncedWaterReports = waterReports.filter(report => !report.synced);
    
    for (const report of unsyncedWaterReports) {
      try {
        await submitWaterQualityReport(report);
        report.synced = true;
        report.synced_at = new Date().toISOString();
      } catch (error) {
        console.error('Failed to sync water report:', report.offline_id);
      }
    }
    
    // Update storage with sync status
    await AsyncStorage.setItem(OFFLINE_KEYS.HEALTH_REPORTS, JSON.stringify(healthReports));
    await AsyncStorage.setItem(OFFLINE_KEYS.WATER_REPORTS, JSON.stringify(waterReports));
    
    const syncedCount = unsyncedHealthReports.length + unsyncedWaterReports.length;
    console.log(`Synced ${syncedCount} offline reports`);
    
    return syncedCount;
  } catch (error) {
    console.error('Failed to sync offline data:', error);
    throw error;
  }
};

export const clearSyncedData = async () => {
  try {
    const healthReports = await getOfflineData('health_reports');
    const waterReports = await getOfflineData('water_reports');
    
    const unsyncedHealthReports = healthReports.filter(report => !report.synced);
    const unsyncedWaterReports = waterReports.filter(report => !report.synced);
    
    await AsyncStorage.setItem(OFFLINE_KEYS.HEALTH_REPORTS, JSON.stringify(unsyncedHealthReports));
    await AsyncStorage.setItem(OFFLINE_KEYS.WATER_REPORTS, JSON.stringify(unsyncedWaterReports));
    
    console.log('Cleared synced offline data');
  } catch (error) {
    console.error('Failed to clear synced data:', error);
  }
};

export const getOfflineDataCount = async () => {
  try {
    const healthReports = await getOfflineData('health_reports');
    const waterReports = await getOfflineData('water_reports');
    
    return {
      health_reports: healthReports.filter(r => !r.synced).length,
      water_reports: waterReports.filter(r => !r.synced).length,
      total: healthReports.filter(r => !r.synced).length + waterReports.filter(r => !r.synced).length
    };
  } catch (error) {
    console.error('Failed to get offline data count:', error);
    return { health_reports: 0, water_reports: 0, total: 0 };
  }
};