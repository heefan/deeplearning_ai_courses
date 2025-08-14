#!/usr/bin/env python3
"""
Standalone demo script for the weather bot.
This script demonstrates the weather bot functionality without requiring ADK.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.weather_bot.adk_integration.session import WeatherSession

def run_demo():
    """Run a demonstration of the weather bot."""
    print("🌤️  Weather Bot Demo")
    print("=" * 50)
    
    # Create session
    session = WeatherSession()
    
    # Start session
    response = session.start_session("London")
    print(f"🎯 {response['welcome_message']}")
    print()
    
    # Demo queries
    demo_queries = [
        "What's the current weather?",
        "Show me the weather forecast",
        "What's the weather like in Tokyo?",
        "Give me a 3-day forecast for Paris"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"📝 Demo Query {i}: {query}")
        response = session.process_message(query)
        print(f"🤖 Response: {response['message']}")
        
        if response.get('data'):
            data = response['data']
            if "error" in data:
                print(f"⚠️  Note: {data['error']}")
                if "mock_data" in data:
                    print("📊 Using mock data for demonstration")
                    data = data["mock_data"]
            
            if "temperature" in data:
                print(f"   🌡️  Temperature: {data['temperature']}°C")
            if "description" in data:
                print(f"   ☁️  Conditions: {data['description']}")
            if "humidity" in data:
                print(f"   💧 Humidity: {data['humidity']}%")
            if "wind_speed" in data:
                print(f"   💨 Wind Speed: {data['wind_speed']} m/s")
            if "feels_like" in data:
                print(f"   🤔 Feels Like: {data['feels_like']}°C")
            
            if "forecast" in data:
                print("   📅 Forecast:")
                for day in data["forecast"][:3]:
                    if "datetime" in day:
                        print(f"      {day['datetime']}: {day['temperature']}°C, {day['description']}")
                    elif "day" in day:
                        print(f"      {day['day']}: {day['temp']}°C, {day['description']}")
        
        print()
    
    # Show session info
    info = session.get_session_info()
    print("📊 Session Information:")
    print(f"   Session ID: {info['session_id']}")
    print(f"   Current Location: {info['current_location']}")
    print(f"   Conversations: {info['conversation_count']}")
    print(f"   Tools Available: {info['tools_available']}")
    print(f"   Callbacks Available: {info['callbacks_available']}")
    print()
    
    print("✅ Demo completed successfully!")
    print("\n💡 To use the weather bot:")
    print("   • ADK CLI: uv run adk web")
    print("   • FastAPI: python scripts/run_fastapi.py")
    print("   • Flask: python scripts/run_flask.py")
    print("   • CLI: python -m src.weather_bot.services.cli --interactive")

if __name__ == "__main__":
    run_demo()
