import AsyncStorage from '@react-native-async-storage/async-storage';

const translations = {
  en: {
    welcome_message: 'Welcome to Health Surveillance',
    report_health_issue: 'Report Health Issue',
    water_quality_test: 'Water Quality Test',
    view_alerts: 'View Alerts',
    health_education: 'Health Education',
    recent_alerts: 'Recent Alerts',
    quick_stats: 'Quick Statistics',
    reports_this_week: 'Reports This Week',
    active_alerts: 'Active Alerts',
    health_report_form: 'Health Report Form',
    patient_age: 'Patient Age',
    patient_gender: 'Patient Gender',
    symptoms: 'Symptoms',
    severity: 'Severity',
    submit_report: 'Submit Report',
    male: 'Male',
    female: 'Female',
    other: 'Other',
    mild: 'Mild',
    moderate: 'Moderate',
    severe: 'Severe',
    fever: 'Fever',
    diarrhea: 'Diarrhea',
    vomiting: 'Vomiting',
    abdominal_pain: 'Abdominal Pain',
    headache: 'Headache',
    nausea: 'Nausea',
    dehydration: 'Dehydration',
    bloody_stool: 'Bloody Stool',
    muscle_cramps: 'Muscle Cramps',
    jaundice: 'Jaundice',
    location: 'Location',
    water_source_type: 'Water Source Type',
    ph_level: 'pH Level',
    turbidity: 'Turbidity',
    bacterial_count: 'Bacterial Count',
    chlorine_level: 'Chlorine Level',
    temperature: 'Temperature',
    submit_test_results: 'Submit Test Results',
    water_quality_guidelines: 'Water Quality Guidelines',
    well: 'Well',
    river: 'River',
    pond: 'Pond',
    tap: 'Tap',
    borehole: 'Borehole'
  },
  hi: {
    welcome_message: 'स्वास्थ्य निगरानी में आपका स्वागत है',
    report_health_issue: 'स्वास्थ्य समस्या की रिपोर्ट करें',
    water_quality_test: 'पानी की गुणवत्ता परीक्षण',
    view_alerts: 'अलर्ट देखें',
    health_education: 'स्वास्थ्य शिक्षा',
    recent_alerts: 'हाल की चेतावनियां',
    quick_stats: 'त्वरित आंकड़े',
    reports_this_week: 'इस सप्ताह की रिपोर्ट',
    active_alerts: 'सक्रिय अलर्ट',
    health_report_form: 'स्वास्थ्य रिपोर्ट फॉर्म',
    patient_age: 'मरीज़ की उम्र',
    patient_gender: 'मरीज़ का लिंग',
    symptoms: 'लक्षण',
    severity: 'गंभीरता',
    submit_report: 'रिपोर्ट जमा करें',
    male: 'पुरुष',
    female: 'महिला',
    other: 'अन्य',
    mild: 'हल्का',
    moderate: 'मध्यम',
    severe: 'गंभीर',
    fever: 'बुखार',
    diarrhea: 'दस्त',
    vomiting: 'उल्टी',
    abdominal_pain: 'पेट दर्द',
    headache: 'सिरदर्द',
    nausea: 'जी मिचलाना',
    dehydration: 'निर्जलीकरण',
    bloody_stool: 'खूनी मल',
    muscle_cramps: 'मांसपेशियों में ऐंठन',
    jaundice: 'पीलिया',
    location: 'स्थान',
    water_source_type: 'पानी के स्रोत का प्रकार',
    ph_level: 'पीएच स्तर',
    turbidity: 'टर्बिडिटी',
    bacterial_count: 'बैक्टीरिया की संख्या',
    chlorine_level: 'क्लोरीन स्तर',
    temperature: 'तापमान',
    submit_test_results: 'परीक्षण परिणाम जमा करें',
    water_quality_guidelines: 'पानी की गुणवत्ता दिशानिर्देश',
    well: 'कुआं',
    river: 'नदी',
    pond: 'तालाब',
    tap: 'नल',
    borehole: 'बोरहोल'
  },
  as: {
    welcome_message: 'স্বাস্থ্য নিৰীক্ষণলৈ আপোনাক স্বাগতম',
    report_health_issue: 'স্বাস্থ্য সমস্যাৰ প্ৰতিবেদন দিয়ক',
    water_quality_test: 'পানীৰ গুণগত পৰীক্ষা',
    view_alerts: 'সতৰ্কবাণী চাওক',
    health_education: 'স্বাস্থ্য শিক্ষা',
    recent_alerts: 'শেহতীয়া সতৰ্কবাণী',
    quick_stats: 'দ্ৰুত পৰিসংখ্যা',
    reports_this_week: 'এই সপ্তাহৰ প্ৰতিবেদন',
    active_alerts: 'সক্ৰিয় সতৰ্কবাণী',
    health_report_form: 'স্বাস্থ্য প্ৰতিবেদন ফৰ্ম',
    patient_age: 'ৰোগীৰ বয়স',
    patient_gender: 'ৰোগীৰ লিংগ',
    symptoms: 'লক্ষণসমূহ',
    severity: 'গুৰুত্ব',
    submit_report: 'প্ৰতিবেদন দাখিল কৰক',
    male: 'পুৰুষ',
    female: 'মহিলা',
    other: 'অন্য',
    mild: 'সামান্য',
    moderate: 'মধ্যম',
    severe: 'গুৰুতৰ',
    fever: 'জ্বৰ',
    diarrhea: 'ডায়েৰিয়া',
    vomiting: 'বমি',
    abdominal_pain: 'পেটৰ বিষ',
    headache: 'মূৰৰ বিষ',
    nausea: 'বমি ভাব',
    dehydration: 'পানীশূন্যতা',
    bloody_stool: 'তেজযুক্ত মল',
    muscle_cramps: 'পেশীৰ টান',
    jaundice: 'কামলা',
    location: 'স্থান',
    water_source_type: 'পানীৰ উৎসৰ প্ৰকাৰ',
    ph_level: 'পিএইচ স্তৰ',
    turbidity: 'ঘোলাত্ব',
    bacterial_count: 'বেক্টেৰিয়াৰ সংখ্যা',
    chlorine_level: 'ক্লৰিনৰ স্তৰ',
    temperature: 'উষ্ণতা',
    submit_test_results: 'পৰীক্ষাৰ ফলাফল দাখিল কৰক',
    water_quality_guidelines: 'পানীৰ গুণগত নিৰ্দেশনা',
    well: 'নাদ',
    river: 'নদী',
    pond: 'পুখুৰী',
    tap: 'টেপ',
    borehole: 'বোৰহোল'
  }
};

let currentLanguage = 'en';

export const setLanguage = async (language) => {
  currentLanguage = language;
  await AsyncStorage.setItem('selectedLanguage', language);
};

export const getCurrentLanguage = async () => {
  const savedLanguage = await AsyncStorage.getItem('selectedLanguage');
  if (savedLanguage) {
    currentLanguage = savedLanguage;
  }
  return currentLanguage;
};

export const translate = (key) => {
  return translations[currentLanguage]?.[key] || translations.en[key] || key;
};

export const getAvailableLanguages = () => {
  return [
    { code: 'en', name: 'English', nativeName: 'English' },
    { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी' },
    { code: 'as', name: 'Assamese', nativeName: 'অসমীয়া' }
  ];
};