## Human in Loop

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
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



class Agent:
    def __init__(self, model: BaseChatModel, tools: list[BaseTool], system_message: str, checkpointer: SqliteSaver):
        self.system_message = system_message 
        graph = StateGraph(AgentState)
        llm_node = "llm"
        action_node = "take_action"
        graph.set_entry_point(llm_node)
        graph.add_node(llm_node, self._call_openai)
        graph.add_node(action_node, self._take_action)
        graph.add_conditional_edges(llm_node, 
                                    self._exist_tool_call, 
                                    {
                                        True: action_node,
                                        False: END
                                    })
        graph.add_edge(action_node, llm_node)
        self.graph = graph.compile(checkpointer=checkpointer)

        # note: don't do self.tools = tools, this is for fast lookup
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools=tools)

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
        for value in event.values():
            for message in value["messages"]:
                print(type(message))
                print_message_data(message)
    
