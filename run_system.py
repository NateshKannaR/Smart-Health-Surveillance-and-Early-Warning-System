#!/usr/bin/env python3
"""
Health Surveillance System Launcher
Starts all system components in the correct order
"""

import os
import sys
import subprocess
import time
import asyncio
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HealthSurveillanceSystem:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.processes = []
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        logger.info("Checking system dependencies...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            logger.error("Python 3.8 or higher is required")
            return False
        
        # Check if required packages are installed
        required_packages = ['fastapi', 'uvicorn', 'sqlalchemy']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"Missing packages: {', '.join(missing_packages)}")
            logger.info("Run: pip install -r requirements_basic.txt")
            return False
        
        logger.info("All dependencies satisfied")
        return True
    
    def setup_database(self):
        """Setup database and create tables"""
        logger.info("Setting up database...")
        try:
            subprocess.run([sys.executable, "setup_database.py"], 
                         cwd=self.project_root, check=True)
            logger.info("Database setup completed")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Database setup failed: {e}")
            return False
    
    def start_backend(self):
        """Start FastAPI backend server"""
        logger.info("Starting backend API server...")
        try:
            process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "backend.main:app", 
                "--host", "0.0.0.0", 
                "--port", "8000", 
                "--reload"
            ], cwd=self.project_root)
            
            self.processes.append(("Backend API", process))
            logger.info("Backend API server started on http://localhost:8000")
            return True
        except Exception as e:
            logger.error(f"Failed to start backend: {e}")
            return False
    
    def start_dashboard(self):
        """Start React dashboard"""
        logger.info("Starting web dashboard...")
        dashboard_path = self.project_root / "dashboard"
        
        if not (dashboard_path / "node_modules").exists():
            logger.info("Installing dashboard dependencies...")
            try:
                subprocess.run(["npm", "install"], cwd=dashboard_path, check=True)
            except subprocess.CalledProcessError:
                logger.error("Failed to install dashboard dependencies")
                return False
        
        try:
            process = subprocess.Popen(["npm", "start"], cwd=dashboard_path)
            self.processes.append(("Dashboard", process))
            logger.info("Dashboard started on http://localhost:3000")
            return True
        except Exception as e:
            logger.error(f"Failed to start dashboard: {e}")
            return False
    
    def start_iot_sensors(self):
        """Start IoT sensor simulation"""
        logger.info("Starting IoT sensor simulation...")
        try:
            process = subprocess.Popen([
                sys.executable, "iot_integration/water_sensor_client.py"
            ], cwd=self.project_root)
            
            self.processes.append(("IoT Sensors", process))
            logger.info("IoT sensors simulation started")
            return True
        except Exception as e:
            logger.error(f"Failed to start IoT sensors: {e}")
            return False
    
    def start_sms_gateway(self):
        """Start SMS gateway service"""
        logger.info("Starting SMS gateway...")
        try:
            process = subprocess.Popen([
                sys.executable, "sms_service/sms_gateway.py"
            ], cwd=self.project_root)
            
            self.processes.append(("SMS Gateway", process))
            logger.info("SMS gateway started")
            return True
        except Exception as e:
            logger.error(f"Failed to start SMS gateway: {e}")
            return False
    
    def wait_for_service(self, url, timeout=30):
        """Wait for a service to become available"""
        import requests
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return True
            except requests.RequestException:
                pass
            time.sleep(2)
        
        return False
    
    def start_system(self):
        """Start the complete health surveillance system"""
        logger.info("Starting Health Surveillance System...")
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Setup database
        if not self.setup_database():
            return False
        
        # Start backend
        if not self.start_backend():
            return False
        
        # Wait for backend to be ready
        logger.info("Waiting for backend to be ready...")
        if not self.wait_for_service("http://localhost:8000/health"):
            logger.error("Backend failed to start properly")
            return False
        
        # Start other services
        time.sleep(2)  # Give backend time to fully initialize
        
        self.start_dashboard()
        time.sleep(3)
        
        self.start_iot_sensors()
        time.sleep(2)
        
        self.start_sms_gateway()
        
        logger.info("=" * 60)
        logger.info("Health Surveillance System Started Successfully!")
        logger.info("=" * 60)
        logger.info("Services:")
        logger.info("  • Backend API: http://localhost:8000")
        logger.info("  • API Documentation: http://localhost:8000/docs")
        logger.info("  • Web Dashboard: http://localhost:3000")
        logger.info("  • IoT Sensors: Running in background")
        logger.info("  • SMS Gateway: Running in background")
        logger.info("=" * 60)
        logger.info("Press Ctrl+C to stop all services")
        
        return True
    
    def stop_system(self):
        """Stop all system processes"""
        logger.info("Stopping Health Surveillance System...")
        
        for name, process in self.processes:
            try:
                logger.info(f"Stopping {name}...")
                process.terminate()
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing {name}...")
                process.kill()
            except Exception as e:
                logger.error(f"Error stopping {name}: {e}")
        
        logger.info("All services stopped")
    
    def run(self):
        """Run the system with proper cleanup"""
        try:
            if self.start_system():
                # Keep the system running
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutdown signal received")
        finally:
            self.stop_system()

def main():
    """Main entry point"""
    system = HealthSurveillanceSystem()
    system.run()

if __name__ == "__main__":
    main()