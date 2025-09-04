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
      color: '#FF6B6B',
      screen: 'HealthReport'
    },
    {
      title: translate('water_quality_test'),
      icon: 'water-drop',
      color: '#4ECDC4',
      screen: 'WaterQuality'
    },
    {
      title: translate('view_alerts'),
      icon: 'warning',
      color: '#FFE66D',
      screen: 'Alerts'
    },
    {
      title: translate('health_education'),
      icon: 'school',
      color: '#95E1D3',
      screen: 'Education'
    }
  ];

  const renderMenuItem = (item, index) => (
    <TouchableOpacity
      key={index}
      style={[styles.menuItem, { backgroundColor: item.color }]}
      onPress={() => navigation.navigate(item.screen)}
    >
      <Icon name={item.icon} size={40} color="#fff" />
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
          <Text style={styles.locationText}>
            📍 {location.district}, {location.state}
          </Text>
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
              <Icon name="warning" size={20} color="#FF6B6B" />
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
    backgroundColor: '#f5f5f5'
  },
  header: {
    backgroundColor: '#2E8B57',
    padding: 20,
    alignItems: 'center'
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center'
  },
  locationText: {
    fontSize: 16,
    color: '#fff',
    marginTop: 5
  },
  menuGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 15,
    justifyContent: 'space-between'
  },
  menuItem: {
    width: '48%',
    aspectRatio: 1,
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
    elevation: 3
  },
  menuText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 10
  },
  alertsSection: {
    margin: 15,
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333'
  },
  alertItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10
  },
  alertText: {
    marginLeft: 10,
    flex: 1,
    fontSize: 14
  }
});

export default HomeScreen;