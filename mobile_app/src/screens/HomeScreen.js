import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
  RefreshControl
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { getLocationData } from '../services/locationService';
import { getRecentAlerts } from '../services/apiService';
import { translate } from '../utils/translations';

const HomeScreen = ({ navigation }) => {
  const [location, setLocation] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const locationData = await getLocationData();
      setLocation(locationData);

      const recentAlerts = await getRecentAlerts(locationData?.district);
      setAlerts(recentAlerts);
    } catch (error) {
      console.error('Error loading initial data:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadInitialData();
    setRefreshing(false);
  };

  const menuItems = [
    {
      title: translate('report_health_issue'),
      icon: 'health-and-safety',
      iconColor: '#ef4444',
      screen: 'HealthReport'
    },
    {
      title: translate('water_quality_test'),
      icon: 'water-drop',
      iconColor: '#06b6d4',
      screen: 'WaterQuality'
    },
    {
      title: translate('view_alerts'),
      icon: 'warning',
      iconColor: '#f59e0b',
      screen: 'Alerts'
    },
    {
      title: translate('health_education'),
      icon: 'school',
      iconColor: '#10b981',
      screen: 'Education'
    }
  ];

  const renderMenuItem = (item, index) => (
    <TouchableOpacity
      key={index}
      style={styles.menuItem}
      onPress={() => navigation.navigate(item.screen)}
      activeOpacity={0.7}
    >
      <View style={[styles.menuIcon, { backgroundColor: `${item.iconColor}15`, padding: 16, borderRadius: 12 }]}>
        <Icon name={item.icon} size={32} color={item.iconColor} />
      </View>
      <Text style={styles.menuText}>{item.title}</Text>
    </TouchableOpacity>
  );

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.header}>
        <Text style={styles.welcomeText}>
          {translate('welcome_message')}
        </Text>
        {location && (
          <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center', marginTop: 4 }}>
            <Icon name="location-on" size={18} color="#64748b" />
            <Text style={[styles.locationText, { marginLeft: 4 }]}>
              {location.district}, {location.state}
            </Text>
          </View>
        )}
      </View>

      <View style={styles.menuGrid}>
        {menuItems.map(renderMenuItem)}
      </View>

      {alerts.length > 0 && (
        <View style={styles.alertsSection}>
          <Text style={styles.sectionTitle}>
            {translate('recent_alerts')}
          </Text>
          {alerts.slice(0, 3).map((alert, index) => (
            <View key={index} style={styles.alertItem}>
              <Icon name="warning" size={20} color="#ef4444" />
              <Text style={styles.alertText}>{alert.message}</Text>
            </View>
          ))}
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc'
  },
  header: {
    backgroundColor: '#ffffff',
    paddingHorizontal: 20,
    paddingVertical: 30,
    borderBottomWidth: 1,
    borderBottomColor: '#e2e8f0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  welcomeText: {
    fontSize: 28,
    fontWeight: '700',
    color: '#0f172a',
    textAlign: 'center',
    marginBottom: 8
  },
  locationText: {
    fontSize: 16,
    color: '#64748b',
    textAlign: 'center',
    fontWeight: '500'
  },
  menuGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 20,
    justifyContent: 'space-between'
  },
  menuItem: {
    width: '48%',
    aspectRatio: 1.1,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#e2e8f0'
  },
  menuIcon: {
    marginBottom: 12
  },
  menuText: {
    color: '#374151',
    fontSize: 15,
    fontWeight: '600',
    textAlign: 'center',
    lineHeight: 20
  },
  alertsSection: {
    margin: 20,
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    borderWidth: 1,
    borderColor: '#e2e8f0'
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 16,
    color: '#0f172a'
  },
  alertItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    backgroundColor: '#fef2f2',
    borderRadius: 12,
    marginBottom: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#ef4444'
  },
  alertText: {
    marginLeft: 12,
    flex: 1,
    fontSize: 14,
    color: '#374151',
    fontWeight: '500',
    lineHeight: 20
  }
});

export default HomeScreen;