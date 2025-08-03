from google.genai import types


async def before_model_callback_input_guardrail(runner, messages, session):
    """
    Input guardrail callback that blocks inappropriate messages before they reach the model.
    
    This callback:
    - Inspects user messages for blocked keywords
    - Returns an error response if blocked content is detected
    - Allows clean messages to proceed normally
    
    Args:
        runner: The Runner instance
        messages: List of messages to be sent to the model
        session: The current session
        
    Returns:
        None to allow processing, or a Content object to intercept
    """
    print("\n[before_model_callback] Inspecting messages...")
    
    blocked_keywords = ["hack", "exploit", "jailbreak", "ignore instructions"]
    
    # Check the last user message
    if messages:
        last_message = messages[-1]
        if hasattr(last_message, 'parts') and last_message.parts:
            user_text = last_message.parts[0].text.lower()
            
            for keyword in blocked_keywords:
                if keyword in user_text:
                    print(f"[before_model_callback] BLOCKED: Found '{keyword}' in user input!")
                    
                    # Set a flag in session state
                    session.state['guardrail_model_block_triggered'] = True
                    
                    # Return an error response
                    return types.Content(
                        role='model',
                        parts=[types.Part(text=(
                            "I'm sorry, but I cannot process that request. "
                            "I'm designed to provide weather information only. "
                            "Please ask me about the weather in any city."
                        ))]
                    )
    
    print("[before_model_callback] Message allowed to proceed.")
    return None  # Allow the request to proceed


async def before_tool_callback_guardrail(runner, tool_name, tool_args, session):
    """
    Tool execution guardrail callback that can block specific tool calls.
    
    This callback:
    - Inspects tool arguments before execution
    - Blocks tool calls for specific cities (e.g., Paris)
    - Returns error responses for blocked tool calls
    
    Args:
        runner: The Runner instance
        tool_name: Name of the tool being called
        tool_args: Arguments being passed to the tool
        session: The current session
        
    Returns:
        None to allow execution, or a dict to intercept with custom response
    """
    print(f"\n[before_tool_callback] Tool: {tool_name}, Args: {tool_args}")
    
    # Check if this is a weather tool and if Paris is being requested
    if tool_name in ['get_weather', 'get_weather_stateful']:
        city = tool_args.get('city', '').lower()
        
        if 'paris' in city:
            print("[before_tool_callback] Blocking tool execution for Paris!")
            
            # Set a flag in session state
            session.state['guardrail_tool_block_triggered'] = True
            
            # Return error response instead of executing the tool
            return {
                'status': 'error',
                'error_message': (
                    "Policy restriction: Weather information for Paris is currently unavailable "
                    "due to data provider limitations. Please try another city."
                )
            }
    
    print("[before_tool_callback] Allowing tool execution.")
    return None  # Allow the tool to execute