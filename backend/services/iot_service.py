import json
import random
from datetime import datetime
from typing import Dict, List

class IoTWaterSensorService:
    """IoT Water Quality Sensor Integration Service"""
    
    def __init__(self):
        self.sensors = {}
        self.readings = []
    
    def register_sensor(self, sensor_id: str, location: str, sensor_type: str = "water_quality") -> Dict:
        """Register a new IoT sensor"""
        self.sensors[sensor_id] = {
            "id": sensor_id,
            "location": location,
            "type": sensor_type,
            "status": "active",
            "last_reading": None,
            "registered_at": datetime.now()
        }
        return {"status": "registered", "sensor_id": sensor_id}
    
    def get_sensor_reading(self, sensor_id: str) -> Dict:
        """Get current reading from IoT sensor"""
        if sensor_id not in self.sensors:
            return {"error": "Sensor not found"}
        
        # Simulate sensor reading
        reading = {
            "sensor_id": sensor_id,
            "timestamp": datetime.now(),
            "ph_level": round(random.uniform(6.0, 8.5), 2),
            "turbidity": round(random.uniform(0.1, 5.0), 2),
            "temperature": round(random.uniform(20.0, 35.0), 1),
            "bacterial_count": random.randint(0, 1000),
            "chlorine_level": round(random.uniform(0.0, 2.0), 2),
            "tds": random.randint(50, 500),  # Total Dissolved Solids
            "conductivity": round(random.uniform(100, 800), 1)
        }
        
        # Determine contamination status
        reading["is_contaminated"] = (
            reading["ph_level"] < 6.5 or reading["ph_level"] > 8.5 or
            reading["turbidity"] > 4.0 or
            reading["bacterial_count"] > 100 or
            reading["chlorine_level"] < 0.2
        )
        
        self.readings.append(reading)
        self.sensors[sensor_id]["last_reading"] = reading
        
        return reading
    
    def get_all_sensors(self) -> List[Dict]:
        """Get all registered sensors"""
        return list(self.sensors.values())
    
    def get_contaminated_sources(self) -> List[Dict]:
        """Get all contaminated water sources"""
        contaminated = []
        for sensor_id, sensor in self.sensors.items():
            if sensor["last_reading"] and sensor["last_reading"]["is_contaminated"]:
                contaminated.append({
                    "sensor_id": sensor_id,
                    "location": sensor["location"],
                    "reading": sensor["last_reading"]
                })
        return contaminated
    
    def simulate_bulk_readings(self, count: int = 10) -> List[Dict]:
        """Simulate multiple sensor readings for testing"""
        readings = []
        locations = ["Village A", "Village B", "Town Center", "River Point", "Well Site"]
        
        for i in range(count):
            sensor_id = f"SENSOR_{i+1:03d}"
            location = random.choice(locations)
            
            if sensor_id not in self.sensors:
                self.register_sensor(sensor_id, location)
            
            reading = self.get_sensor_reading(sensor_id)
            readings.append(reading)
        
        return readings