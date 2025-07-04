#!/usr/bin/env python3
"""
Setup script for Knowledge Management Agent
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False
    return True

def main():
    print("🚀 Setting up Knowledge Management Agent...")
    print("=" * 50)
    
    # Check if Python is available
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    # Create virtual environment
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        pip_command = "venv\\Scripts\\pip"
        python_command = "venv\\Scripts\\python"
    else:
        pip_command = "venv/bin/pip"
        python_command = "venv/bin/python"
    
    commands = [
        (f"{pip_command} install --upgrade pip", "Upgrading pip"),
        (f"{pip_command} install -r requirements.txt", "Installing Python dependencies"),
        (f"{python_command} -m spacy download en_core_web_sm", "Downloading spaCy English model"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            sys.exit(1)
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        run_command("cp .env.example .env", "Creating environment file")
        print("📝 Please edit the .env file with your Neo4j credentials")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start Neo4j database:")
    print("   docker-compose up neo4j -d")
    print("   OR install Neo4j locally")
    print("\n2. Update .env file with your Neo4j credentials")
    print("\n3. Start the application:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\python -m uvicorn app.main:app --reload")
    else:
        print("   venv/bin/python -m uvicorn app.main:app --reload")
    print("\n4. Open http://localhost:8000 in your browser")

if __name__ == "__main__":
    main()