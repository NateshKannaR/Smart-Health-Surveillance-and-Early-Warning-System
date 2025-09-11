# Smart Health Surveillance and Early Warning System

A comprehensive digital health platform for detecting, monitoring, and preventing water-borne disease outbreaks in vulnerable communities.

## 🚀 New Features

### Professional UI Improvements
- **Modern Material-UI Design**: Clean, professional interface
- **Dark/Light Theme Toggle**: Switch between themes with button in navbar
- **Enhanced Typography**: Inter font family for better readability
- **Professional Loading States**: Branded loading screens
- **Error Boundaries**: Graceful error handling

### Dashboard Enhancements
- **Status Cards**: Professional metric displays with icons and trends
- **System Health Overview**: Real-time monitoring with progress bars
- **Enhanced Charts**: Better color schemes and styling
- **Responsive Design**: Optimized for all screen sizes

### Mobile App Improvements
- **Modern Card Layout**: Clean design with shadows and spacing
- **Professional Colors**: Consistent theme matching dashboard
- **Enhanced Icons**: Professional icon treatment
- **Better Typography**: Improved font weights and clarity

## Features

- **Mobile Data Collection**: Community health reporting via mobile apps and SMS
- **AI/ML Outbreak Prediction**: Pattern detection and outbreak prediction models
- **Water Quality Monitoring**: Integration with IoT sensors and manual test kits
- **Real-time Alerts**: Automated notifications to health authorities
- **Multilingual Support**: Interface in tribal and local languages
- **Offline Functionality**: Works without internet connectivity
- **Dashboard Analytics**: Visualization and resource allocation tools

## Quick Start

### Backend
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Dashboard
```bash
cd dashboard
npm install
npm start
```

### Mobile App
```bash
cd mobile_app
npm install
npx react-native run-android
```

## Architecture

```
├── backend/           # FastAPI backend services
├── mobile_app/        # React Native mobile application
├── dashboard/         # React.js web dashboard
├── ml_models/         # AI/ML prediction models
├── iot_integration/   # Water quality sensor integration
├── sms_service/       # SMS gateway integration
└── database/          # Database schemas and migrations
```

## Water-borne Diseases Monitored

- Diarrhea
- Cholera
- Typhoid
- Hepatitis A
- Dysentery
- Gastroenteritis

## Technology Stack

- **Backend**: FastAPI, Python, SQLite
- **Frontend**: React.js, Material-UI
- **Mobile**: React Native
- **ML**: Scikit-learn, Pandas
- **Database**: SQLite with migration support