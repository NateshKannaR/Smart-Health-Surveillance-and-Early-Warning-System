import asyncio
import json
import random
import time
from datetime import datetime
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WaterQualitySensor:
    """Simulates IoT water quality sensor"""
    
    def __init__(self, sensor_id, location, source_type="well"):
        self.sensor_id = sensor_id
        self.location = location
        self.source_type = source_type
        self.api_endpoint = "http://localhost:8000/api/water/quality"
        self.is_running = False
        
    def read_sensor_data(self):
        """Simulate reading from actual sensors"""
        # Simulate realistic water quality parameters
        base_ph = 7.0 + random.uniform(-1.5, 1.5)
        base_turbidity = random.exponential(2.0)
        base_bacterial = random.poisson(3)
        base_chlorine = random.uniform(0.1, 0.8)
        base_temp = 25 + random.uniform(-5, 10)
        
        # Add contamination events (10% chance)
        if random.random() < 0.1:
            base_ph += random.uniform(-2, 2)
            base_turbidity *= random.uniform(2, 5)
            base_bacterial *= random.randint(5, 20)
            base_chlorine *= random.uniform(0.1, 0.5)
        
        return {
            "sensor_id": self.sensor_id,
            "location": self.location,
            "source_type": self.source_type,
            "ph_level": round(max(0, min(14, base_ph)), 2),
            "turbidity": round(max(0, base_turbidity), 2),
            "bacterial_count": max(0, base_bacterial),
            "chlorine_level": round(max(0, base_chlorine), 3),
            "temperature": round(base_temp, 1),
            "timestamp": datetime.now().isoformat(),
            "tested_by": 1  # IoT sensor user ID
        }
    
    async def send_data(self, session, data):
        """Send sensor data to API"""
        try:
            async with session.post(self.api_endpoint, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Sensor {self.sensor_id}: Data sent successfully")
                    
                    # Check if water is contaminated
                    if result.get('is_contaminated'):
                        logger.warning(f"CONTAMINATION DETECTED at {self.location}!")
                        await self.trigger_alert(session, data)
                else:
                    logger.error(f"Sensor {self.sensor_id}: Failed to send data - {response.status}")
        except Exception as e:
            logger.error(f"Sensor {self.sensor_id}: Error sending data - {e}")
    
    async def trigger_alert(self, session, sensor_data):
        """Trigger contamination alert"""
        alert_data = {
            "alert_type": "water_contamination",
            "location": self.location,
            "message": f"Water contamination detected at {self.location}. pH: {sensor_data['ph_level']}, Turbidity: {sensor_data['turbidity']}, Bacteria: {sensor_data['bacterial_count']}",
            "severity": "high" if sensor_data['bacterial_count'] > 10 else "medium",
            "affected_population": random.randint(50, 500)
        }
        
        try:
            async with session.post("http://localhost:8000/api/alerts", json=alert_data) as response:
                if response.status == 200:
                    logger.info(f"Alert triggered for {self.location}")
                else:
                    logger.error(f"Failed to trigger alert - {response.status}")
        except Exception as e:
            logger.error(f"Error triggering alert - {e}")
    
    async def start_monitoring(self, interval=300):  # 5 minutes
        """Start continuous monitoring"""
        self.is_running = True
        logger.info(f"Starting sensor {self.sensor_id} at {self.location}")
        
        async with aiohttp.ClientSession() as session:
            while self.is_running:
                try:
                    # Read sensor data
                    data = self.read_sensor_data()
                    logger.info(f"Sensor {self.sensor_id}: pH={data['ph_level']}, Turbidity={data['turbidity']}, Bacteria={data['bacterial_count']}")
                    
                    # Send data to API
                    await self.send_data(session, data)
                    
                    # Wait for next reading
                    await asyncio.sleep(interval)
                    
                except Exception as e:
                    logger.error(f"Sensor {self.sensor_id}: Monitoring error - {e}")
                    await asyncio.sleep(60)  # Wait 1 minute before retry
    
    def stop_monitoring(self):
        """Stop sensor monitoring"""
        self.is_running = False
        logger.info(f"Stopping sensor {self.sensor_id}")

class SensorNetwork:
    """Manages multiple water quality sensors"""
    
    def __init__(self):
        self.sensors = []
        
    def add_sensor(self, sensor_id, location, source_type="well"):
        """Add a new sensor to the network"""
        sensor = WaterQualitySensor(sensor_id, location, source_type)
        self.sensors.append(sensor)
        logger.info(f"Added sensor {sensor_id} at {location}")
        
    async def start_all_sensors(self, interval=300):
        """Start monitoring all sensors"""
        tasks = []
        for sensor in self.sensors:
            task = asyncio.create_task(sensor.start_monitoring(interval))
            tasks.append(task)
        
        logger.info(f"Started {len(self.sensors)} sensors")
        await asyncio.gather(*tasks)
    
    def stop_all_sensors(self):
        """Stop all sensors"""
        for sensor in self.sensors:
            sensor.stop_monitoring()

# Example usage and sensor deployment
async def deploy_sensor_network():
    """Deploy a network of water quality sensors"""
    network = SensorNetwork()
    
    # Add sensors for different locations in NER
    sensors_config = [
        ("WQ001", "Guwahati, Assam", "river"),
        ("WQ002", "Shillong, Meghalaya", "well"),
        ("WQ003", "Imphal, Manipur", "pond"),
        ("WQ004", "Aizawl, Mizoram", "tap"),
        ("WQ005", "Kohima, Nagaland", "borehole"),
        ("WQ006", "Agartala, Tripura", "river"),
        ("WQ007", "Itanagar, Arunachal Pradesh", "well"),
        ("WQ008", "Dimapur, Nagaland", "tap")
    ]
    
    for sensor_id, location, source_type in sensors_config:
        network.add_sensor(sensor_id, location, source_type)
    
    # Start monitoring (with shorter interval for demo)
    await network.start_all_sensors(interval=60)  # 1 minute for demo

if __name__ == "__main__":
    try:
        asyncio.run(deploy_sensor_network())
    except KeyboardInterrupt:
        logger.info("Sensor network stopped by user")