# Health Surveillance System - Deployment Guide

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the complete system
python run_system.py
```

### Option 2: Docker Deployment
```bash
# Start all services with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: Manual Setup

#### 1. Backend API
```bash
# Setup database
python setup_database.py

# Start API server
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Web Dashboard
```bash
cd dashboard
npm install
npm start
```

#### 3. Mobile App
```bash
cd mobile_app
npm install
npx react-native run-android  # For Android
npx react-native run-ios      # For iOS
```

#### 4. IoT Sensors (Optional)
```bash
python iot_integration/water_sensor_client.py
```

#### 5. SMS Gateway (Optional)
```bash
python sms_service/sms_gateway.py
```

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │    │  Web Dashboard  │    │   SMS Gateway   │
│  (React Native) │    │    (React.js)   │    │    (Python)     │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴───────────┐
                    │     FastAPI Backend     │
                    │    (Python/FastAPI)     │
                    └─────────────┬───────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
┌─────────┴───────┐    ┌─────────┴───────┐    ┌─────────┴───────┐
│   PostgreSQL    │    │   ML Models     │    │  IoT Sensors    │
│   Database      │    │  (Scikit-learn) │    │   (Simulated)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Environment Configuration

### Required Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/health_surveillance

# SMS Service (Twilio)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone

# Redis (for caching)
REDIS_URL=redis://localhost:6379
```

### Create .env file
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Database Setup

### PostgreSQL (Production)
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb health_surveillance
sudo -u postgres createuser health_user
sudo -u postgres psql -c "ALTER USER health_user WITH PASSWORD 'health_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE health_surveillance TO health_user;"

# Run setup script
python setup_database.py
```

### SQLite (Development)
```bash
# Automatically created when running setup_database.py
python setup_database.py
```

## Service Endpoints

| Service | URL | Description |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | Main API server |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Web Dashboard | http://localhost:3000 | Health surveillance dashboard |
| SMS Gateway | http://localhost:8001 | SMS webhook endpoint |

## API Endpoints

### Health Reports
- `POST /api/health/reports` - Submit health report
- `GET /api/health/reports` - Get health reports
- `GET /api/health/reports/stats` - Get health statistics

### Water Quality
- `POST /api/water/quality` - Submit water quality report
- `GET /api/water/quality` - Get water quality reports
- `GET /api/water/quality/hotspots` - Get contamination hotspots

### Alerts
- `POST /api/alerts` - Create alert
- `GET /api/alerts` - Get alerts
- `PUT /api/alerts/{id}/resolve` - Resolve alert

### Predictions
- `POST /api/predictions/outbreak` - Predict outbreak
- `GET /api/predictions/risk-assessment` - Get risk assessment

## Mobile App Features

### Core Functionality
- ✅ Health issue reporting with symptom selection
- ✅ Water quality testing and reporting
- ✅ Real-time alerts and notifications
- ✅ Offline functionality with sync
- ✅ Multilingual support (English, Hindi, Assamese)
- ✅ GPS location integration
- ✅ Camera integration for evidence

### Supported Languages
- English (en)
- Hindi (hi) - हिन्दी
- Assamese (as) - অসমীয়া

## SMS Commands

### Health Reporting
```
HEALTH <age> <gender> <symptoms> <location>
Example: HEALTH 25 M fever,diarrhea Village_Name
```

### Water Quality Reporting
```
WATER <location> <ph> <turbidity> <bacteria>
Example: WATER Village_Name 6.5 8.2 15
```

### Get Alerts
```
ALERT <location>
Example: ALERT Village_Name
```

### Help
```
HELP
```

## IoT Integration

### Water Quality Sensors
- pH level monitoring
- Turbidity measurement
- Bacterial contamination detection
- Temperature monitoring
- Chlorine level testing

### Sensor Data Format
```json
{
  "sensor_id": "WQ001",
  "location": "Guwahati, Assam",
  "ph_level": 7.2,
  "turbidity": 3.5,
  "bacterial_count": 0,
  "chlorine_level": 0.4,
  "temperature": 25.0,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## ML Models

### Outbreak Prediction
- **Algorithm**: Random Forest + Gradient Boosting
- **Features**: Health reports, water quality, seasonal data
- **Output**: Risk score, predicted cases, contributing factors

### Disease Classification
- **Input**: Symptoms, patient demographics
- **Output**: Most likely disease, confidence score

### Water Quality Analysis
- **Standards**: WHO drinking water guidelines
- **Parameters**: pH, turbidity, bacteria, chlorine
- **Output**: Contamination risk level

## Monitoring and Alerts

### Alert Types
- `outbreak_warning` - Disease outbreak detected
- `water_contamination` - Water source contaminated
- `resource_needed` - Medical resources required

### Alert Severity Levels
- `low` - Informational
- `medium` - Attention required
- `high` - Immediate action needed
- `critical` - Emergency response required

### Notification Channels
- SMS alerts to health officials
- Mobile app push notifications
- Email notifications
- Community broadcast systems

## Security Considerations

### Data Protection
- Patient data anonymization
- Encrypted data transmission
- Secure API authentication
- GDPR compliance measures

### Access Control
- Role-based permissions
- API rate limiting
- Input validation and sanitization
- SQL injection prevention

## Performance Optimization

### Database
- Indexed queries for location-based searches
- Connection pooling
- Query optimization

### API
- Response caching with Redis
- Async request handling
- Background task processing with Celery

### Mobile App
- Offline data storage
- Image compression
- Lazy loading

## Troubleshooting

### Common Issues

#### Backend won't start
```bash
# Check database connection
python -c "from database.database import engine; print('DB OK')"

# Check dependencies
pip install -r requirements.txt
```

#### Dashboard build fails
```bash
cd dashboard
rm -rf node_modules package-lock.json
npm install
```

#### Mobile app build issues
```bash
cd mobile_app
npx react-native clean
npm install
```

### Logs Location
- Backend: Console output or `/var/log/health-surveillance/`
- IoT Sensors: Console output
- SMS Gateway: Console output

## Production Deployment

### Server Requirements
- **CPU**: 4+ cores
- **RAM**: 8GB+ 
- **Storage**: 100GB+ SSD
- **OS**: Ubuntu 20.04+ or CentOS 8+

### Load Balancing
```nginx
upstream backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}

server {
    listen 80;
    location /api/ {
        proxy_pass http://backend;
    }
}
```

### SSL Configuration
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com
```

## Support

For technical support or questions:
- Email: support@healthsurveillance.gov.in
- Documentation: https://docs.healthsurveillance.gov.in
- GitHub Issues: https://github.com/health-surveillance/issues