from google.adk.agents import Agent


def create_greeting_agent():
    """Create a specialized greeting agent."""
    return Agent(
        name="greeting_agent",
        model="gemini-1.5-flash",
        description="Handles user greetings and welcomes them warmly.",
        instruction=(
            "You are a friendly greeting specialist. When users say hello, hi, hey, or similar greetings, "
            "welcome them warmly and let them know they can ask about weather in any city. "
            "Keep your response brief and friendly. "
            "Example: 'Hello! Welcome to the Weather Assistant. I'm here to help you check the weather "
            "for any city around the world. Just let me know which city you're interested in!'"
        ),
        tools=[]  # No tools needed for greetings
    )


def create_farewell_agent():
    """Create a specialized farewell agent."""
    return Agent(
        name="farewell_agent",
        model="gemini-1.5-flash",
        description="Handles user farewells and thanks them politely.",
        instruction=(
            "You are a polite farewell specialist. When users say goodbye, bye, see you, thanks, "
            "or similar farewells, thank them for using the service and wish them well. "
            "Keep your response brief and warm. "
            "Example: 'Thank you for using the Weather Assistant! Have a wonderful day and stay weather-aware!'"
        ),
        tools=[]  # No tools needed for farewells
    )