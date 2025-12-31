#!/usr/bin/env python3
"""
Cali_X_One System Health Check and Auto-Start

Checks if the system is running and starts it if needed.
"""

import subprocess
import time
import sys
import os
import requests
from pathlib import Path

def check_server_health(url: str = "http://localhost:8003/health") -> bool:
    """Check if server is responding"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Start the Cali_X_One server"""
    print("🚀 Starting Cali_X_One server...")

    # Check if virtual environment exists
    venv_path = Path(".venv/Scripts/activate.ps1")
    if venv_path.exists():
        # Windows with venv
        cmd = ["powershell", "-Command", ".venv\\Scripts\\Activate.ps1; python run_server.py"]
    else:
        # Try without venv
        cmd = ["python", "run_server.py"]

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )

        # Wait a bit for startup
        time.sleep(3)

        # Check if process is still running
        if process.poll() is None:
            print("✅ Server started successfully")
            return True
        else:
            stdout, stderr = process.communicate()
            print("❌ Server failed to start")
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            return False

    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main health check and startup"""
    print("🔍 Cali_X_One System Health Check")
    print("=" * 40)

    # Check if server is running
    if check_server_health():
        print("✅ Server is already running")
        return True

    print("⚠️  Server not responding, attempting to start...")

    # Try to start server
    if start_server():
        # Wait for full startup
        time.sleep(5)

        # Final health check
        if check_server_health():
            print("🎉 System is now healthy and ready!")
            print("\n📋 Quick Test Commands:")
            print("curl http://localhost:8003/health")
            print("python run_tests.py")
            print("python benchmark.py")
            return True
        else:
            print("❌ Server started but health check failed")
            return False
    else:
        print("❌ Failed to start server")
        print("\n🔧 Troubleshooting:")
        print("1. Check if Python dependencies are installed:")
        print("   pip install -r requirements.txt")
        print("2. Check if port 8003 is available:")
        print("   netstat -ano | findstr 8003")
        print("3. Check server logs for errors")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)