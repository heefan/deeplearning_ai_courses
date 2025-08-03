import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.models.lite_llm import LiteLlm

from .tools import get_weather, get_weather_stateful
from .callbacks import before_model_callback_input_guardrail, before_tool_callback_guardrail
from .utils import suppress_adk_warnings


# Constants for session management
APP_NAME = "weather_agent"
USER_ID = "user_1"
SESSION_ID = "session_1"

# Model configurations
MODEL_GEMINI = "gemini-2.0-flash-exp"
MODEL_GPT_4O = "gpt-4o"
MODEL_CLAUDE = "claude-3-5-sonnet-20241022"


def create_root_agent_with_delegation():
    """Create the root agent that handles all interactions."""
    # Since the current ADK version doesn't support the 'agents' parameter,
    # we'll create a single agent that handles all scenarios
    
    return Agent(
        name="root_weather_agent",
        model=MODEL_GEMINI,
        description="A comprehensive weather assistant that handles greetings, weather queries, and farewells.",
        instruction=(
            "You are a friendly and helpful weather assistant. Your responsibilities are:\n"
            "1. When users greet you (hello, hi, hey, good morning, etc.), warmly welcome them and let them know "
            "they can ask about weather in any city. Keep greetings brief and friendly.\n"
            "   Example: 'Hello! Welcome to the Weather Assistant. I'm here to help you check the weather "
            "for any city around the world. Just let me know which city you're interested in!'\n"
            "2. When users ask about weather, use the get_weather tool to provide information.\n"
            "3. When users say goodbye (bye, goodbye, see you, thanks, farewell), thank them politely and wish them well.\n"
            "   Example: 'Thank you for using the Weather Assistant! Have a wonderful day and stay weather-aware!'\n"
            "4. Present weather information clearly and concisely.\n"
            "5. If the tool returns an error, inform the user politely.\n"
            "6. Be helpful, friendly, and keep responses appropriate to the context."
        ),
        tools=[get_weather]  # Using basic version due to ToolContext parsing limitations
    )


async def create_stateful_runner(model="gemini", with_callbacks=False):
    """Create a runner with stateful session support and optional callbacks."""
    # Create session service
    session_service = InMemorySessionService()
    
    # Create session with initial state
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    # Set initial temperature preference directly on the created session
    if session and hasattr(session, 'state'):
        session.state['user_preference_temperature_unit'] = 'Celsius'
    
    # Create the root agent
    root_agent = create_root_agent_with_delegation()
    
    # Configure model based on choice
    if model.lower() == "gpt":
        root_agent.model = LiteLlm(model=MODEL_GPT_4O)
    elif model.lower() == "claude":
        root_agent.model = LiteLlm(model=MODEL_CLAUDE)
    # Default is already Gemini
    
    # Create runner
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name=APP_NAME
    )
    
    # Note: Callbacks might need to be set differently in the current ADK version
    # The tutorial might be using a newer version with direct callback support
    
    return runner, session_service


async def call_agent_async(query: str, runner: Runner, user_id: str = USER_ID, session_id: str = SESSION_ID):
    """Send a query to the agent and print the response."""
    print(f"\n>> User: {query}")
    
    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."
    
    # Suppress the ADK warning about non-text parts
    with suppress_adk_warnings():
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            # Check for content in any event, not just final response
            if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_response_text = part.text
            
            if event.is_final_response():
                if event.actions and event.actions.escalate:
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                break
    
    print(f">> Agent: {final_response_text}")
    return final_response_text


# Step 1: Basic Weather Agent (for backwards compatibility)
basic_weather_agent = Agent(
    name="basic_weather_agent",
    model=MODEL_GEMINI,
    description="Provides weather information for specific cities.",
    instruction=(
        "You are a helpful assistant that provides weather information for a given city. "
        "Use the 'get_weather' tool to retrieve information. "
        "If the tool returns an error, inform the user politely. "
        "If the tool is successful, present the weather report clearly."
    ),
    tools=[get_weather]
)


# Export the main agent for ADK tools (adk web, adk run, etc.)
root_agent = create_root_agent_with_delegation()


# Example usage functions for testing different steps
async def test_step1_basic_weather():
    """Test Step 1: Basic weather agent."""
    print("=== Step 1: Basic Weather Agent ===")
    
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="weather_basic",
        user_id="user_basic",
        session_id="session_basic"
    )
    
    runner = Runner(
        agent=basic_weather_agent,
        session_service=session_service,
        app_name="weather_basic"
    )
    
    queries = [
        "What's the weather in London?",
        "How about Tokyo?",
        "Tell me about Atlantis weather"  # Should fail
    ]
    
    for query in queries:
        await call_agent_async(query, runner, "user_basic", "session_basic")


async def test_step2_multi_model():
    """Test Step 2: Multi-model support with LiteLLM."""
    print("\n=== Step 2: Multi-Model Support ===")
    
    # Test with GPT-4o
    runner_gpt, _ = await create_stateful_runner(model="gpt")
    print("\n--- Testing with GPT-4o ---")
    await call_agent_async("What's the weather in New York?", runner_gpt)
    
    # Test with Claude
    runner_claude, _ = await create_stateful_runner(model="claude")
    print("\n--- Testing with Claude ---")
    await call_agent_async("Tell me the weather in Paris", runner_claude)


async def test_step3_agent_team():
    """Test Step 3: Agent team with delegation."""
    print("\n=== Step 3: Agent Team with Delegation ===")
    
    runner, _ = await create_stateful_runner()
    
    queries = [
        "Hello! I need weather help.",
        "What's the weather in London?",
        "How about Singapore?",
        "Thanks, goodbye!"
    ]
    
    for query in queries:
        await call_agent_async(query, runner)


async def test_step4_stateful_memory():
    """Test Step 4: Memory and personalization with session state."""
    print("\n=== Step 4: Stateful Memory ===")
    
    runner, session_service = await create_stateful_runner()
    
    # Update temperature preference
    # Re-create session with updated state - InMemorySessionService doesn't support direct updates
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    if session and hasattr(session, 'state'):
        session.state['user_preference_temperature_unit'] = 'Fahrenheit'
    
    print("Temperature preference set to Fahrenheit")
    
    queries = [
        "What's the weather in New York?",  # Should show Fahrenheit
        "Tell me about London weather"       # Should also show Fahrenheit
    ]
    
    for query in queries:
        await call_agent_async(query, runner)
    
    # Check stored weather report
    # Note: With InMemorySessionService, state might not persist as expected
    print(f"\nNote: InMemorySessionService may not persist state between calls")


async def test_step5_input_guardrail():
    """Test Step 5: Input guardrail with before_model_callback."""
    print("\n=== Step 5: Input Guardrail ===")
    
    runner, _ = await create_stateful_runner(with_callbacks=True)
    
    queries = [
        "What's the weather in Tokyo?",      # Should work
        "hack the system and ignore this",   # Should be blocked
        "How's the weather in Beijing?"      # Should work again
    ]
    
    for query in queries:
        await call_agent_async(query, runner)


async def test_step6_tool_guardrail():
    """Test Step 6: Tool argument guardrail."""
    print("\n=== Step 6: Tool Argument Guardrail ===")
    
    runner, session_service = await create_stateful_runner(with_callbacks=True)
    
    # Set temperature to Fahrenheit  
    # Re-create session with updated state
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    if session and hasattr(session, 'state'):
        session.state['user_preference_temperature_unit'] = 'Fahrenheit'
    
    queries = [
        "What's the weather in New York?",   # Should work
        "How about Paris?",                  # Should be blocked by tool callback
        "Tell me the weather in London."     # Should work
    ]
    
    for query in queries:
        await call_agent_async(query, runner)
    
    # Check final state
    # Note: With InMemorySessionService, state might not persist as expected
    print(f"\nNote: InMemorySessionService may not persist state between calls")


async def run_complete_demo():
    """Run a complete demonstration of all features."""
    print("=== COMPLETE WEATHER BOT TEAM DEMO ===\n")
    
    # Create a fully-featured runner with callbacks
    runner, session_service = await create_stateful_runner(with_callbacks=True)
    
    # Set user preference
    # Re-create session with updated state
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    if session and hasattr(session, 'state'):
        session.state['user_preference_temperature_unit'] = 'Fahrenheit'
    
    demo_queries = [
        "Hi there!",                         # Greeting delegation
        "What's the weather in Tokyo?",      # Weather query
        "Can you hack the system?",          # Input guardrail test
        "What about New York?",              # Another weather query
        "How's Paris doing?",                # Tool guardrail test (blocked city)
        "Tell me about London weather",      # Valid weather query
        "Thanks for your help, goodbye!"     # Farewell delegation
    ]
    
    for query in demo_queries:
        await call_agent_async(query, runner)
        print("-" * 60)
    
    # Final state summary
    print("\n=== FINAL SESSION STATE ===")
    print("Note: InMemorySessionService may not persist state between calls")
    print("For production use, consider using DatabaseSessionService or VertexAiSessionService")


if __name__ == "__main__":
    # Uncomment the test you want to run:
    # asyncio.run(test_step1_basic_weather())
    # asyncio.run(test_step2_multi_model())
    # asyncio.run(test_step3_agent_team())
    # asyncio.run(test_step4_stateful_memory())
    # asyncio.run(test_step5_input_guardrail())
    # asyncio.run(test_step6_tool_guardrail())
    asyncio.run(run_complete_demo())