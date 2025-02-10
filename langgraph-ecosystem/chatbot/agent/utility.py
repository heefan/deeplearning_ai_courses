from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, ToolMessage, ToolCall 
import json
from PIL import Image

def print_message(message: AnyMessage):
    if isinstance(message, (AIMessage, HumanMessage, ToolMessage)):
        print(f"Type: {type(message).__name__}")
        print(f"Content: {message.content}")
        if hasattr(message, 'tool_calls') and message.tool_calls:
            print("Tool Calls:")
            for tool_call in message.tool_calls:
                print(f"  - Tool: {tool_call['name']}")
                print(f"    Args: {tool_call['args']}")
        print("-" * 50)

def print_message_data(message: AnyMessage):
    
    
    message_data = {
        "type": type(message).__name__,
        "content": message.content,
        "additional_kwargs": message.additional_kwargs,
    }
    
    # Add tool_calls if they exist
    if hasattr(message, 'tool_calls') and message.tool_calls:
        message_data["tool_calls"] = message.tool_calls
        
    # Add any response metadata if it exists
    if hasattr(message, 'response_metadata'):
        message_data["response_metadata"] = message.response_metadata
        
    print(json.dumps(message_data, indent=2))
    
def print_agent_graph(agent, filename="graph.png"):
    png_data = agent.get_graph().draw_png()
    with open(filename, "wb") as f:
        f.write(png_data)
    
    img = Image.open(filename)
    img.show()
    