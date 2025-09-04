import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { Alert, Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { requestLocationPermission } from './utils/permissions';
import { initializeOfflineStorage } from './services/offlineService';
import { setupPushNotifications } from './services/notificationService';

// Screens
import HomeScreen from './screens/HomeScreen';
import HealthReportScreen from './screens/HealthReportScreen';
import WaterQualityScreen from './screens/WaterQualityScreen';
import AlertsScreen from './screens/AlertsScreen';
import ProfileScreen from './screens/ProfileScreen';
import LoginScreen from './screens/LoginScreen';
import LanguageSelectionScreen from './screens/LanguageSelectionScreen';

const Stack = createStackNavigator();

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedLanguage, setSelectedLanguage] = useState('en');

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      // Check login status
      const userToken = await AsyncStorage.getItem('userToken');
      setIsLoggedIn(!!userToken);

      // Get saved language preference
      const savedLanguage = await AsyncStorage.getItem('selectedLanguage');
      if (savedLanguage) {
        setSelectedLanguage(savedLanguage);
      }

      // Request permissions
      await requestLocationPermission();

      // Initialize offline storage
      await initializeOfflineStorage();

      // Setup push notifications
      await setupPushNotifications();

    } catch (error) {
      console.error('App initialization error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return null; // Show loading screen
  }

  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName={isLoggedIn ? "Home" : "Login"}
        screenOptions={{
          headerStyle: { backgroundColor: '#2E8B57' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' }
        }}
      >
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="LanguageSelection" component={LanguageSelectionScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="HealthReport" component={HealthReportScreen} />
        <Stack.Screen name="WaterQuality" component={WaterQualityScreen} />
        <Stack.Screen name="Alerts" component={AlertsScreen} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;