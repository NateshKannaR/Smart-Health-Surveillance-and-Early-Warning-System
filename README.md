# Smart Health Surveillance and Early Warning System

A comprehensive digital health platform for detecting, monitoring, and preventing water-borne disease outbreaks in vulnerable communities.

## Features

- **Mobile Data Collection**: Community health reporting via mobile apps and SMS
- **AI/ML Outbreak Prediction**: Pattern detection and outbreak prediction models
- **Water Quality Monitoring**: Integration with IoT sensors and manual test kits
- **Real-time Alerts**: Automated notifications to health authorities
- **Multilingual Support**: Interface in tribal and local languages
- **Offline Functionality**: Works without internet connectivity
- **Dashboard Analytics**: Visualization and resource allocation tools

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

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Setup database: `python setup_database.py`
3. Run backend: `uvicorn main:app --reload`
4. Start dashboard: `cd dashboard && npm start`
5. Build mobile app: `cd mobile_app && npx react-native run-android`

## Water-borne Diseases Monitored

- Diarrhea
- Cholera
- Typhoid
- Hepatitis A
- Dysentery
- Gastroenteritis