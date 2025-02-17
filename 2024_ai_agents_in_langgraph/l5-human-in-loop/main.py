## Human in Loop

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Literal
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage, ToolCall 
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.sqlite import SqliteSaver
from uuid import uuid4
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools.base import BaseTool
from enum import Enum
from PIL import Image
from utility import print_message_data, print_agent_graph
from langgraph.types import interrupt, Command

_ = load_dotenv()

class ErrorCode(Enum):
    INVALID_MESSAGE = "E001"
    TOOL_NOT_FOUND = "E002"
    EXECUTION_ERROR = "E003"
    SHOULD_BE_AI_MESSAGE = "E004"

def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
    # assign ids to messages that don't have them
    for message in right:
        if not message.id:
            message.id = str(uuid4())
    # merge the new messages with the existing messages
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            # replace any existing messages with the same id
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            # append any new messages to the end
            merged.append(message)
    return merged

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], reduce_messages]

    @classmethod
    def __call__(cls, messages: list[AnyMessage]):
        return cls(messages=messages)


LLM_NODE = "llm"
ACTION_NODE = "take_action"
HUMAN_APPROVE_NODE = "human_approve"

class Agent:
    
    def __init__(self, model: BaseChatModel, tools: list[BaseTool], system_message: str, checkpointer: SqliteSaver):
        self.system_message = system_message 
        graph = StateGraph(AgentState)
        
        graph.set_entry_point(LLM_NODE)
        graph.add_node(LLM_NODE, self._call_openai)
        graph.add_node(ACTION_NODE, self._take_action)
        graph.add_node(HUMAN_APPROVE_NODE, self._humman_approval_node)
        
        graph.add_edge(LLM_NODE, HUMAN_APPROVE_NODE)
        graph.add_edge(HUMAN_APPROVE_NODE, ACTION_NODE)
        graph.add_edge(HUMAN_APPROVE_NODE, LLM_NODE)
        graph.add_edge(HUMAN_APPROVE_NODE, END)
        graph.add_edge(ACTION_NODE, LLM_NODE)
        
        self.graph = graph.compile(checkpointer=checkpointer)
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools=tools)
        
    def _humman_approval_node(self, state: AgentState) -> Command[Literal["llm", "take_action", "end"]]:
        # Get the last message which should be from LLM
        last_message = state["messages"][-1]
        
        response = interrupt(
            {
                "question": "Do you approve this response?",
                "options": ["approve", "retry", "terminate"],
                "llm_output": last_message.content
            }
        )
        
        if response == "approve":
            return Command(goto=ACTION_NODE)
        elif response == "retry":
            return Command(goto=LLM_NODE)
        else:  # terminate
            return Command(goto=END)
        

    def _call_openai(self, state: AgentState) -> AgentState:
        messages = state["messages"]
        if self.system_message:
            system_prompt = SystemMessage(content=self.system_message)
            messages = [system_prompt] + messages 
        response: AIMessage = self.model.invoke(messages)
        return AgentState(messages=[response])

    def _take_action(self, state: AgentState) -> AgentState | ErrorCode:
        last_message = state["messages"][-1]
        if not isinstance(last_message, AIMessage): 
            return ErrorCode.SHOULD_BE_AI_MESSAGE
 
        tool_calls: list[ToolCall] = last_message.tool_calls       
        responses: list[ToolMessage] = []
        
        for tool_call in tool_calls:
            name = tool_call['name']
            call_id = tool_call['id']
            args = tool_call['args']

            if not name:
                return ErrorCode.TOOL_NOT_FOUND 
            if name not in self.tools:
                return ErrorCode.TOOL_NOT_FOUND    
            else:
                response = self.tools[name].invoke(args)
            
            tool_message = ToolMessage(tool_call_id=call_id, name=name, content=str(response))
            responses.append(tool_message)
            
        return AgentState(messages=responses)
        

    def _exist_tool_call(self, state: AgentState) -> bool:
        last_message = state["messages"][-1]
        if not isinstance(last_message, AIMessage):
            return False
        
        return len(last_message.tool_calls) > 0

        
######### main #########
system_prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""
model = ChatOpenAI(model="gpt-4o")

user_message = HumanMessage(content="What is the weather in Singapore?")
state = AgentState(messages=[user_message])

with SqliteSaver.from_conn_string(":memory:") as memory:
    tool = TavilySearchResults(max_results=2)
    agent = Agent(model=model, tools=[tool], system_message=system_prompt, checkpointer=memory)
    print_agent_graph(agent=agent)
    thread = {"configurable": {"thread_id": "1"}}
    events = agent.graph.stream(state, thread)

    for event in events:
        # Handle interrupt events
        if "__interrupt__" in event:
            interrupt_data = event["__interrupt__"][0].value
            print("\nHuman Approval Required:")
            print(f"Question: {interrupt_data['question']}")
            print(f"Options: {interrupt_data['options']}")
            print(f"LLM Output: {interrupt_data['llm_output']}")
            # Here you would handle the user input
            response = input("Enter your choice (approve/retry/terminate): ")
            continue

        # Handle regular message events
        for value in event.values():
            if isinstance(value, dict) and "messages" in value:
                for message in value["messages"]:
                    if hasattr(message, 'content'):
                        print(f"\nMessage Content: {message.content}")
                    if hasattr(message, 'tool_calls'):
                        print(f"Tool Calls: {message.tool_calls}")
    
