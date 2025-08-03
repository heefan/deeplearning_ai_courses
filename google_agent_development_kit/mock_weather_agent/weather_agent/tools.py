
from google.adk.tools import ToolContext


def get_weather(city: str) -> dict:
    """Retrieve the current weather for a specified city

    Args:
        city (str): The name of the city (e.g. "New York", "London", "Paris", "Singapore", "Beijing")

    Returns:
        dict: A dictionary containing the current weather information for the city.
              Include a 'status' key ('success' or 'error') 
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """

    print(f"-------Tool: get_weather called for city: {city}-------")
    city_normalized = city.lower().replace(" ", "")

    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 70 degrees Fahrenheit."},
        "london": {"status": "success", "report": "The weather in London is cloudy with a temperature of 60 degrees Fahrenheit."},
        "paris": {"status": "success", "report": "The weather in Paris is sunny with a temperature of 75 degrees Fahrenheit."},
        "singapore": {"status": "success", "report": "The weather in Singapore is sunny with a temperature of 85 degrees Fahrenheit."},
        "beijing": {"status": "success", "report": "The weather in Beijing is cloudy with a temperature of 65 degrees Fahrenheit."},
        "tokyo": {"status": "success", "report": "The weather in Tokyo is partly cloudy with a temperature of 72 degrees Fahrenheit."},
    }
    
    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {
            "status": "error",
            "error_message": f"Weather data not available for {city}",
        }


def get_weather_stateful(city: str, context: ToolContext) -> dict:
    """Retrieve the current weather for a specified city (with session state support).
    
    This stateful version:
    - Reads the user's temperature unit preference from session state
    - Saves the last weather report to session state via output_key
    
    Args:
        city (str): The name of the city (e.g. "New York", "London", "Paris")
        context (ToolContext): The tool context providing access to session state
        
    Returns:
        dict: A dictionary containing the current weather information for the city.
              Include a 'status' key ('success' or 'error')
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    print(f"[Stateful Tool] get_weather_stateful called for city: {city}")
    
    # Access session state via context
    session_state = context.session.state
    
    # Read user preference for temperature unit (default to Celsius)
    temp_unit = session_state.get('user_preference_temperature_unit', 'Celsius')
    print(f"User prefers temperature in: {temp_unit}")
    
    # Mock weather database with both Celsius and Fahrenheit
    city_normalized = city.lower().replace(" ", "")
    
    # Temperature data: (celsius, fahrenheit)
    weather_data = {
        "newyork": (21, 70, "sunny"),
        "london": (15, 60, "cloudy"),
        "paris": (24, 75, "sunny"),
        "singapore": (29, 85, "sunny"),
        "beijing": (18, 65, "cloudy"),
        "tokyo": (22, 72, "partly cloudy"),
    }
    
    if city_normalized in weather_data:
        celsius, fahrenheit, condition = weather_data[city_normalized]
        
        if temp_unit == "Fahrenheit":
            report = f"The weather in {city} is {condition} with a temperature of {fahrenheit} degrees Fahrenheit."
        else:
            report = f"The weather in {city} is {condition} with a temperature of {celsius} degrees Celsius."
        
        weather_result = {
            "status": "success",
            "report": report
        }
        
        # Save this report to session state via output_key
        context.output_key = 'last_weather_report'
        
        return weather_result
    else:
        return {
            "status": "error",
            "error_message": f"Weather data not available for {city}"
        }
