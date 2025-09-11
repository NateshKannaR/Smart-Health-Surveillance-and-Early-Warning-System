import React from 'react';
import {
  View,
  Text,
  ActivityIndicator,
  StyleSheet
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

const LoadingScreen = ({ message = 'Loading...' }) => {
  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <View style={styles.iconContainer}>
          <Icon name="local-hospital" size={48} color="#3b82f6" />
          <ActivityIndicator 
            size="large" 
            color="#3b82f6" 
            style={styles.spinner}
          />
        </View>
        
        <Text style={styles.title}>{message}</Text>
        <Text style={styles.subtitle}>
          Please wait while we load your health data
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20
  },
  content: {
    alignItems: 'center',
    maxWidth: 300
  },
  iconContainer: {
    position: 'relative',
    marginBottom: 32,
    alignItems: 'center',
    justifyContent: 'center'
  },
  spinner: {
    position: 'absolute',
    transform: [{ scale: 1.8 }]
  },
  title: {
    fontSize: 20,
    fontWeight: '700',
    color: '#0f172a',
    textAlign: 'center',
    marginBottom: 8
  },
  subtitle: {
    fontSize: 16,
    color: '#64748b',
    textAlign: 'center',
    lineHeight: 24,
    fontWeight: '500'
  }
});

export default LoadingScreen;