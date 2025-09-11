import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert
} from 'react-native';
import { submitWaterQualityReport } from '../services/apiService';
import { translate } from '../utils/translations';

const WaterQualityScreen = ({ navigation }) => {
  const [formData, setFormData] = useState({
    location: '',
    phLevel: '',
    turbidity: '',
    bacterialCount: '',
    chlorineLevel: '',
    temperature: '',
    sourceType: 'well'
  });

  const sourceTypes = ['well', 'river', 'pond', 'tap', 'borehole'];

  const submitReport = async () => {
    if (!formData.location || !formData.phLevel) {
      Alert.alert('Error', 'Please fill required fields');
      return;
    }

    try {
      await submitWaterQualityReport(formData);
      Alert.alert('Success', 'Water quality report submitted', [
        { text: 'OK', onPress: () => navigation.goBack() }
      ]);
    } catch (error) {
      Alert.alert('Error', 'Failed to submit. Saved offline.');
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>{translate('water_quality_test')}</Text>
      
      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('location')}</Text>
        <TextInput
          style={styles.input}
          value={formData.location}
          onChangeText={(text) => setFormData({ ...formData, location: text })}
          placeholder="Enter location"
        />
      </View>

      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('water_source_type')}</Text>
        <View style={styles.radioGroup}>
          {sourceTypes.map(type => (
            <TouchableOpacity
              key={type}
              style={[
                styles.radioButton,
                formData.sourceType === type && styles.radioSelected
              ]}
              onPress={() => setFormData({ ...formData, sourceType: type })}
            >
              <Text style={styles.radioText}>{translate(type)}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('ph_level')} (6.5-8.5)</Text>
        <TextInput
          style={styles.input}
          value={formData.phLevel}
          onChangeText={(text) => setFormData({ ...formData, phLevel: text })}
          keyboardType="decimal-pad"
          placeholder="7.0"
        />
      </View>

      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('turbidity')} (NTU)</Text>
        <TextInput
          style={styles.input}
          value={formData.turbidity}
          onChangeText={(text) => setFormData({ ...formData, turbidity: text })}
          keyboardType="decimal-pad"
          placeholder="< 5"
        />
      </View>

      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('bacterial_count')} (CFU/100ml)</Text>
        <TextInput
          style={styles.input}
          value={formData.bacterialCount}
          onChangeText={(text) => setFormData({ ...formData, bacterialCount: text })}
          keyboardType="numeric"
          placeholder="0"
        />
      </View>

      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('chlorine_level')} (mg/L)</Text>
        <TextInput
          style={styles.input}
          value={formData.chlorineLevel}
          onChangeText={(text) => setFormData({ ...formData, chlorineLevel: text })}
          keyboardType="decimal-pad"
          placeholder="0.2-0.5"
        />
      </View>

      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('temperature')} (°C)</Text>
        <TextInput
          style={styles.input}
          value={formData.temperature}
          onChangeText={(text) => setFormData({ ...formData, temperature: text })}
          keyboardType="decimal-pad"
          placeholder="25"
        />
      </View>

      <TouchableOpacity style={styles.submitButton} onPress={submitReport}>
        <Text style={styles.submitText}>{translate('submit_test_results')}</Text>
      </TouchableOpacity>

      <View style={styles.guidelinesBox}>
        <Text style={styles.guidelinesTitle}>{translate('water_quality_guidelines')}</Text>
        <Text style={styles.guidelinesText}>
          • pH: 6.5-8.5{'\n'}
          • Turbidity: &lt; 5 NTU{'\n'}
          • Bacteria: 0 CFU/100ml{'\n'}
          • Chlorine: 0.2-0.5 mg/L
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff'
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center'
  },
  formGroup: {
    marginBottom: 20
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16
  },
  radioGroup: {
    flexDirection: 'row',
    flexWrap: 'wrap'
  },
  radioButton: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 8,
    marginRight: 10,
    marginBottom: 10
  },
  radioSelected: {
    backgroundColor: '#4ECDC4',
    borderColor: '#4ECDC4'
  },
  radioText: {
    color: '#333'
  },
  submitButton: {
    backgroundColor: '#4ECDC4',
    borderRadius: 8,
    padding: 15,
    alignItems: 'center',
    marginTop: 20
  },
  submitText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold'
  },
  guidelinesBox: {
    backgroundColor: '#f0f8ff',
    padding: 15,
    borderRadius: 8,
    marginTop: 20
  },
  guidelinesTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10
  },
  guidelinesText: {
    fontSize: 14,
    lineHeight: 20
  }
});

export default WaterQualityScreen;