"""
CLI service for the weather bot.
"""

import argparse
import json
import sys
from typing import Optional
from ..adk_integration.session import WeatherSession

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Weather Bot CLI - Get weather information from the command line"
    )
    
    parser.add_argument(
        "--message", "-m",
        type=str,
        help="Weather query message (e.g., 'What's the weather like?')"
    )
    
    parser.add_argument(
        "--location", "-l",
        type=str,
        help="Location to get weather for"
    )
    
    parser.add_argument(
        "--set-location",
        type=str,
        help="Set the default location for the session"
    )
    
    parser.add_argument(
        "--session-info",
        action="store_true",
        help="Show current session information"
    )
    
    parser.add_argument(
        "--start-session",
        action="store_true",
        help="Start a new weather session"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive mode"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    
    args = parser.parse_args()
    
    # Create session
    session = WeatherSession()
    
    try:
        if args.set_location:
            response = session.set_location(args.set_location)
            if args.json:
                print(json.dumps(response, indent=2))
            else:
                print(f"✅ {response['message']}")
            return
        
        if args.session_info:
            info = session.get_session_info()
            if args.json:
                print(json.dumps(info, indent=2))
            else:
                print("📊 Session Information:")
                print(f"   Session ID: {info['session_id']}")
                print(f"   Current Location: {info['current_location'] or 'Not set'}")
                print(f"   Conversations: {info['conversation_count']}")
                print(f"   Tools Available: {info['tools_available']}")
                print(f"   Callbacks Available: {info['callbacks_available']}")
            return
        
        if args.start_session:
            response = session.start_session(args.location)
            if args.json:
                print(json.dumps(response, indent=2))
            else:
                print(f"🎯 {response['welcome_message']}")
            return
        
        if args.interactive:
            run_interactive_mode(session, args.json)
            return
        
        if args.message:
            response = session.process_message(args.message, args.location)
            if args.json:
                print(json.dumps(response, indent=2))
            else:
                print(f"🌤️  {response['message']}")
                if response.get('data'):
                    print_weather_data(response['data'])
            return
        
        # Default: show help
        parser.print_help()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def run_interactive_mode(session: WeatherSession, json_output: bool = False):
    """Run the weather bot in interactive mode."""
    print("🌤️  Weather Bot Interactive Mode")
    print("Type 'help' for commands, 'quit' to exit")
    print("=" * 50)
    
    # Start session
    response = session.start_session()
    if not json_output:
        print(f"🎯 {response['welcome_message']}")
    
    while True:
        try:
            user_input = input("\n🌤️  You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            if user_input.lower() == 'info':
                info = session.get_session_info()
                if json_output:
                    print(json.dumps(info, indent=2))
                else:
                    print("📊 Session Information:")
                    print(f"   Current Location: {info['current_location'] or 'Not set'}")
                    print(f"   Conversations: {info['conversation_count']}")
                continue
            
            # Process weather query
            response = session.process_message(user_input)
            
            if json_output:
                print(json.dumps(response, indent=2))
            else:
                print(f"🤖 Bot: {response['message']}")
                if response.get('data'):
                    print_weather_data(response['data'])
                    
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

def print_help():
    """Print help information for interactive mode."""
    print("\n📖 Available Commands:")
    print("  help          - Show this help")
    print("  info          - Show session information")
    print("  quit/exit/q   - Exit the program")
    print("\n💡 Example Weather Queries:")
    print("  What's the weather like in London?")
    print("  Show me the forecast for Tokyo")
    print("  Current weather in New York")
    print("  Weather forecast for Paris")

def print_weather_data(data: dict):
    """Print weather data in a formatted way."""
    if "error" in data:
        print(f"⚠️  Note: {data['error']}")
        if "mock_data" in data:
            print("📊 Mock Data:")
            data = data["mock_data"]
    
    if "temperature" in data:
        print(f"🌡️  Temperature: {data['temperature']}°C")
    if "description" in data:
        print(f"☁️  Conditions: {data['description']}")
    if "humidity" in data:
        print(f"💧 Humidity: {data['humidity']}%")
    if "wind_speed" in data:
        print(f"💨 Wind Speed: {data['wind_speed']} m/s")
    if "feels_like" in data:
        print(f"🤔 Feels Like: {data['feels_like']}°C")
    
    if "forecast" in data:
        print("📅 Forecast:")
        for day in data["forecast"][:3]:  # Show first 3 days
            if "datetime" in day:
                print(f"   {day['datetime']}: {day['temperature']}°C, {day['description']}")
            elif "day" in day:
                print(f"   {day['day']}: {day['temp']}°C, {day['description']}")

if __name__ == "__main__":
    main()
