"""
Safety callbacks for the weather bot.
"""

from typing import Dict, Any, List
from .config import config

def validate_temperature(temperature: float) -> bool:
    """
    Validate temperature is within safe bounds.
    
    Args:
        temperature: Temperature in Celsius
        
    Returns:
        True if temperature is within bounds, False otherwise
    """
    return config.min_temperature <= temperature <= config.max_temperature

def validate_location(location: str) -> bool:
    """
    Validate location input.
    
    Args:
        location: Location string
        
    Returns:
        True if location is valid, False otherwise
    """
    if not location or not isinstance(location, str):
        return False
    
    # Basic validation - location should not be too long and should contain alphanumeric chars
    if len(location) > 100 or len(location) < 1:
        return False
    
    # Check for potentially dangerous characters
    dangerous_chars = ['<', '>', '&', '"', "'", ';', '(', ')', '{', '}']
    if any(char in location for char in dangerous_chars):
        return False
    
    return True

def safety_callbacks() -> List[Dict[str, Any]]:
    """Get safety callbacks for ADK integration."""
    return [
        {
            "name": "validate_weather_request",
            "description": "Validate weather request parameters",
            "function": lambda **kwargs: {
                "valid": all([
                    validate_location(kwargs.get("location", "")),
                    kwargs.get("days", 1) in range(1, 6) if "days" in kwargs else True
                ]),
                "message": "Weather request validation completed"
            }
        },
        {
            "name": "validate_temperature_data",
            "description": "Validate temperature data from weather API",
            "function": lambda temperature: {
                "valid": validate_temperature(temperature),
                "message": f"Temperature {temperature}°C is {'within' if validate_temperature(temperature) else 'outside'} safe bounds"
            }
        },
        {
            "name": "sanitize_location_input",
            "description": "Sanitize location input for safety",
            "function": lambda location: {
                "sanitized": location.strip()[:100] if location else "",
                "message": "Location input sanitized"
            }
        }
    ]

def apply_safety_checks(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply safety checks to weather data.
    
    Args:
        data: Weather data dictionary
        
    Returns:
        Data with safety validation results
    """
    result = data.copy()
    
    # Check temperature if present
    if "temperature" in data:
        temp = data["temperature"]
        if isinstance(temp, (int, float)):
            result["temperature_safe"] = validate_temperature(temp)
            if not result["temperature_safe"]:
                result["warning"] = f"Temperature {temp}°C is outside normal range"
    
    # Check location if present
    if "location" in data:
        location = data["location"]
        if isinstance(location, str):
            result["location_safe"] = validate_location(location)
    
    return result
