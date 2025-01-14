from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import TypedDict, Annotated, operator, List
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI

_ = load_dotenv()

tool = TavilySearchResults(max_results=2)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:
    def __init__(self, model, tools, checkpointer, system=""):
        self.system = system
        graph = StateGraph(AgentState)

        llm_node = "llm"
        action_node = "action"

        graph.add_node(llm_node, self.call_openai)
        graph.add_node(action_node, self.take_action)
        graph.add_conditional_edges(llm_node,
                                    self.exist_action,
                                    {True: action_node, False: END})
        
        graph.add_edge(action_node, llm_node)
        graph.set_entry_point(llm_node)
        self.graph = graph.compile(checkpointer=checkpointer)
        self.tools={t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def call_openai(self, state: AgentState) -> AgentState:
        messages = state["messages"]
        if self.system: 
            messages = [SystemMessage(content=self.system)] + messages
        response: AIMessage = self.model.invoke(messages)
        return {'messages': [response]}
    
    def take_action(self, state: AgentState) -> AgentState:
        last_message: AIMessage = state['messages'][-1]
        tool_calls = last_message.tool_calls

        results: List[ToolMessage] = []
        for tool_call in tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            tool_id = tool_call['id']
        
            response = self.tools[tool_name].invoke(tool_args)
            tool_message = ToolMessage(
                content=str(response),
                tool_call_id=tool_id,
                name=tool_name
            )
            results.append(tool_message)
        return {'messages': results}

    def exist_action(self, state: AgentState) -> bool:
        """Check if the last message has tool calls."""
        last_message = state['messages'][-1]
        return bool(last_message.tool_calls)
    

prompt = """
you are a smart search assistant. Use the search engine to look up information.
You are allowed to make multiple calls (either together or in sequence). 
Only look up information when you are sure of what you want.
If you need to look up some information before asking a follow up question, you are allowed to do that.
"""

import json

def print_result(result):
    data = {
        "result": result
    }
    print(json.dumps(data, indent=4))

model = ChatOpenAI(model="gpt-4o")

def visualize_agent_graph(agent, filename="graph.png"):
    png_data = agent.graph.get_graph().draw_png()
    with open(filename, "wb") as f:
        f.write(png_data)
    
    from PIL import Image
    img = Image.open(filename)
    img.show()

def print_message(message: AnyMessage):
    """Helper function to print message content in a readable format"""
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
    """Helper function to convert message to JSON-serializable format"""
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

### Run the graph
with SqliteSaver.from_conn_string(":memory:") as memory:
    agent = Agent(model, [tool], checkpointer=memory, system=prompt)
    visualize_agent_graph(agent)
    
    messages = [HumanMessage(content="What is the weather in Singapore today")]
    state = {"messages": messages}
    thread = {"configurable": {"thread_id": "1"}}
    for event in agent.graph.stream(state, thread):
        for v in event.values():
            print("\n------------  New Event: ", type(v))
            for message in v['messages']:
                print_message_data(message)

    messages = [HumanMessage(content="What about in la?")]
    thread = {"configurable": {"thread_id": "1"}}
    state = {"messages": messages}
    for event in agent.graph.stream(state, thread):
        for v in event.values():
            for message in v['messages']:
                print_message_data(message)

    messages = [HumanMessage(content="Which one is warmer?")]
    thread = {"configurable": {"thread_id": "1"}}
    state = {"messages": messages}
    for event in agent.graph.stream(state, thread):
        for v in event.values():
            for message in v['messages']:
                print_message_data(message)
    
    messages = [HumanMessage(content="Which one is warmer?")]
    state = {"messages": messages}
    thread = {"configurable": {"thread_id": "2"}}
    for event in agent.graph.stream(state, thread):
        for v in event.values():
            for message in v['messages']:
                print_message_data(message)