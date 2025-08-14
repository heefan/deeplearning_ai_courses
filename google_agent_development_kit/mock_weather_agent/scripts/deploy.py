#!/usr/bin/env python3
"""
Deployment script for the weather bot.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    # Check if uv is installed
    if run_command("uv --version", "Checking uv installation"):
        print("✅ uv is installed")
    else:
        print("❌ uv is not installed. Please install it first.")
        return False
    
    return True

def install_dependencies():
    """Install project dependencies."""
    print("📦 Installing dependencies...")
    
    if run_command("uv sync", "Installing dependencies with uv"):
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("❌ Failed to install dependencies")
        return False

def run_tests():
    """Run project tests."""
    print("🧪 Running tests...")
    
    if run_command("uv run pytest", "Running tests"):
        print("✅ Tests passed")
        return True
    else:
        print("❌ Tests failed")
        return False

def build_project():
    """Build the project."""
    print("🔨 Building project...")
    
    if run_command("uv build", "Building project"):
        print("✅ Project built successfully")
        return True
    else:
        print("❌ Build failed")
        return False

def create_env_file():
    """Create .env file from template."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("📝 Creating .env file from template...")
        try:
            with open(env_example, 'r') as f:
                template = f.read()
            
            with open(env_file, 'w') as f:
                f.write(template)
            
            print("✅ .env file created. Please update it with your API keys.")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("⚠️  No .env.example file found. Creating basic .env file...")
        try:
            with open(env_file, 'w') as f:
                f.write("# Weather Bot Configuration\n")
                f.write("# Add your API keys here\n\n")
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
                f.write("WEATHER_API_KEY=your_weather_api_key_here\n")
                f.write("MODEL_NAME=gpt-4\n")
                f.write("TEMPERATURE=0.7\n")
            
            print("✅ Basic .env file created. Please update it with your API keys.")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False

def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description="Deploy Weather Bot")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-build", action="store_true", help="Skip building project")
    parser.add_argument("--env-only", action="store_true", help="Only create .env file")
    
    args = parser.parse_args()
    
    print("🚀 Weather Bot Deployment")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    if args.env_only:
        print("✅ Environment setup completed")
        return
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Run tests (unless skipped)
    if not args.skip_tests:
        if not run_tests():
            print("⚠️  Tests failed, but continuing with deployment...")
    
    # Build project (unless skipped)
    if not args.skip_build:
        if not build_project():
            sys.exit(1)
    
    print("\n🎉 Deployment completed successfully!")
    print("\n📖 Next steps:")
    print("   1. Update .env file with your API keys")
    print("   2. Test the weather bot:")
    print("      • ADK CLI: uv run adk web")
    print("      • FastAPI: python scripts/run_fastapi.py")
    print("      • Flask: python scripts/run_flask.py")
    print("      • CLI: python -m weather_agent.services.cli --interactive")
    print("   3. Run demo: python scripts/demo.py")

if __name__ == "__main__":
    main()
