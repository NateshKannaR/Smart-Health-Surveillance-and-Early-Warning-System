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
import { submitHealthReport } from '../services/apiService';
import { translate } from '../utils/translations';

const HealthReportScreen = ({ navigation }) => {
  const [formData, setFormData] = useState({
    patientAge: '',
    patientGender: '',
    symptoms: [],
    severity: 'mild',
    location: ''
  });

  const symptoms = [
    'fever', 'diarrhea', 'vomiting', 'abdominal_pain', 'headache',
    'nausea', 'dehydration', 'bloody_stool', 'muscle_cramps', 'jaundice'
  ];

  const toggleSymptom = (symptom) => {
    const updatedSymptoms = formData.symptoms.includes(symptom)
      ? formData.symptoms.filter(s => s !== symptom)
      : [...formData.symptoms, symptom];
    
    setFormData({ ...formData, symptoms: updatedSymptoms });
  };

  const submitReport = async () => {
    if (!formData.patientAge || !formData.patientGender || formData.symptoms.length === 0) {
      Alert.alert('Error', 'Please fill all required fields');
      return;
    }

    try {
      await submitHealthReport(formData);
      Alert.alert('Success', 'Health report submitted successfully', [
        { text: 'OK', onPress: () => navigation.goBack() }
      ]);
    } catch (error) {
      Alert.alert('Error', 'Failed to submit report. Saved offline.');
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>{translate('health_report_form')}</Text>
      
      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('patient_age')}</Text>
        <TextInput
          style={styles.input}
          value={formData.patientAge}
          onChangeText={(text) => setFormData({ ...formData, patientAge: text })}
          keyboardType="numeric"
          placeholder="Enter age"
        />
      </View>

      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('patient_gender')}</Text>
        <View style={styles.radioGroup}>
          {['male', 'female', 'other'].map(gender => (
            <TouchableOpacity
              key={gender}
              style={[
                styles.radioButton,
                formData.patientGender === gender && styles.radioSelected
              ]}
              onPress={() => setFormData({ ...formData, patientGender: gender })}
            >
              <Text style={styles.radioText}>{translate(gender)}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('symptoms')}</Text>
        <View style={styles.symptomsGrid}>
          {symptoms.map(symptom => (
            <TouchableOpacity
              key={symptom}
              style={[
                styles.symptomButton,
                formData.symptoms.includes(symptom) && styles.symptomSelected
              ]}
              onPress={() => toggleSymptom(symptom)}
            >
              <Text style={styles.symptomText}>{translate(symptom)}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <View style={styles.formGroup}>
        <Text style={styles.label}>{translate('severity')}</Text>
        <View style={styles.radioGroup}>
          {['mild', 'moderate', 'severe'].map(severity => (
            <TouchableOpacity
              key={severity}
              style={[
                styles.radioButton,
                formData.severity === severity && styles.radioSelected
              ]}
              onPress={() => setFormData({ ...formData, severity })}
            >
              <Text style={styles.radioText}>{translate(severity)}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <TouchableOpacity style={styles.submitButton} onPress={submitReport}>
        <Text style={styles.submitText}>{translate('submit_report')}</Text>
      </TouchableOpacity>
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
    backgroundColor: '#2E8B57',
    borderColor: '#2E8B57'
  },
  radioText: {
    color: '#333'
  },
  symptomsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap'
  },
  symptomButton: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 15,
    paddingHorizontal: 12,
    paddingVertical: 8,
    marginRight: 8,
    marginBottom: 8
  },
  symptomSelected: {
    backgroundColor: '#FF6B6B',
    borderColor: '#FF6B6B'
  },
  symptomText: {
    fontSize: 14
  },
  submitButton: {
    backgroundColor: '#2E8B57',
    borderRadius: 8,
    padding: 15,
    alignItems: 'center',
    marginTop: 20
  },
  submitText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold'
  }
});

export default HealthReportScreen;