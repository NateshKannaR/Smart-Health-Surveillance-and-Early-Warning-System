#!/usr/bin/env python3
"""
Quick deployment script for Health Surveillance System
"""
import subprocess
import sys
import os
import time

def run_command(cmd, cwd=None):
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")
    
    # Check Python
    if not run_command("python --version"):
        print("Python is required but not found")
        return False
    
    # Check Docker (optional)
    docker_available = run_command("docker --version")
    
    # Check Node.js (for dashboard)
    node_available = run_command("node --version")
    
    return True

def deploy_backend():
    """Deploy the FastAPI backend"""
    print("\n🚀 Deploying Backend...")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install Python dependencies")
        return False
    
    # Setup database
    if not run_command("python setup_database.py"):
        print("Failed to setup database")
        return False
    
    print("✅ Backend setup complete")
    return True

def deploy_dashboard():
    """Deploy the React dashboard"""
    print("\n🌐 Deploying Dashboard...")
    
    dashboard_path = "dashboard"
    if not os.path.exists(dashboard_path):
        print("Dashboard directory not found")
        return False
    
    # Install Node dependencies
    if not run_command("npm install", cwd=dashboard_path):
        print("Failed to install Node dependencies")
        return False
    
    print("✅ Dashboard setup complete")
    return True

def start_services():
    """Start all services"""
    print("\n🔄 Starting Services...")
    
    # Start backend in background
    print("Starting backend API...")
    backend_process = subprocess.Popen([
        "python", "-m", "uvicorn", "main:app", 
        "--host", "0.0.0.0", "--port", "8000", "--reload"
    ], cwd="backend")
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start dashboard in background
    print("Starting dashboard...")
    dashboard_process = subprocess.Popen([
        "npm", "start"
    ], cwd="dashboard")
    
    print("\n✅ Services started!")
    print("🌐 Backend API: http://localhost:8000")
    print("📊 Dashboard: http://localhost:3000")
    print("📖 API Docs: http://localhost:8000/docs")
    
    return backend_process, dashboard_process

def docker_deploy():
    """Deploy using Docker Compose"""
    print("\n🐳 Deploying with Docker...")
    
    if not run_command("docker-compose --version"):
        print("Docker Compose is required but not found")
        return False
    
    # Start all services
    if not run_command("docker-compose up -d"):
        print("Failed to start Docker services")
        return False
    
    print("✅ Docker deployment complete!")
    print("🌐 Backend API: http://localhost:8000")
    print("📊 Dashboard: http://localhost:3000")
    print("📖 API Docs: http://localhost:8000/docs")
    
    return True

def main():
    """Main deployment function"""
    print("🏥 Health Surveillance System - Quick Deploy")
    print("=" * 50)
    
    if not check_requirements():
        sys.exit(1)
    
    # Ask deployment method
    print("\nChoose deployment method:")
    print("1. Docker Compose (Recommended)")
    print("2. Manual Setup")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        if docker_deploy():
            print("\n🎉 Deployment successful!")
            print("\nTo stop services: docker-compose down")
            print("To view logs: docker-compose logs -f")
        else:
            print("\n❌ Docker deployment failed")
            sys.exit(1)
    
    elif choice == "2":
        if deploy_backend() and deploy_dashboard():
            try:
                backend_proc, dashboard_proc = start_services()
                print("\n🎉 Deployment successful!")
                print("\nPress Ctrl+C to stop services")
                
                # Wait for user interrupt
                while True:
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping services...")
                backend_proc.terminate()
                dashboard_proc.terminate()
                print("✅ Services stopped")
        else:
            print("\n❌ Manual deployment failed")
            sys.exit(1)
    
    else:
        print("Invalid choice")
        sys.exit(1)

if __name__ == "__main__":
    main()