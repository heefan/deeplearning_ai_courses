from dotenv import load_dotenv
_ = load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, ToolMessage, ToolCall

tool = TavilySearchResults(max_results=4)
print(tool.name)

from typing import Annotated, operator, TypedDict
from langchain_core.messages import AnyMessage 
#Notes: AnyMessage contains ToolMessage, AIMessage, HumanMessage, ..., etc.

class AgentState(TypedDict):   # [operator.add, ...]
    messages: Annotated[list[AnyMessage], operator.add]

from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage
from langchain_core.tools.base import BaseTool
from langchain_core.language_models.chat_models import BaseChatModel

class Agent:
    def __init__(self, model: BaseChatModel, tools: list[BaseTool], system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",  # from
            self.exists_action, #condition
            {True: "action", False: END}  # condition result
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()

        # notes: to understand the tools, sample data is:
        # {
        #     "tavily_search": <TavilySearchResults object>,
        #     "calculator": <CalculatorTool object>,
        #     "weather": <WeatherTool object>
        # }
        # so the tools is a dictionary, with key as the name of the tool, and value as the tool object.
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState) -> bool:
        result = state["messages"][-1]
        if isinstance(result, AIMessage):
            # make sure there is AIMessage, coz only AIMessage has tool_calls.
            return len(result.tool_calls) > 0  
        return False
    
    ## attach with "llm" node
    ## the function take current state, and append with system message if it exists,
    ## then invoke the model, and save the new assistant message to state
    ## return the new state as AgentState
    def call_openai(self, state: AgentState) -> AgentState:
        messages = state["messages"]    
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message:AIMessage = self.model.invoke(messages)

        print("---> message: ", message)
        print("---end---")

        return {"messages": [message]}
    
    ## attach with "action" node
    ## Notes: AI Message is an assistant message. 
    def take_action(self, state: AgentState) -> AgentState:
        # get the last message, because the last message which is AIMessage that has tool_calls.
        last_message = state["messages"][-1]
        if not isinstance(last_message, AIMessage):
            return {"messages": [AIMessage(content="Error: Expected AI message with tool calls")]}
        tool_calls: list[ToolCall] = last_message.tool_calls

        results: list[ToolMessage] = []
        for t in tool_calls:
            print(f"Calling {t}")
            if not isinstance(t, dict) or "name" not in t:
                # validate tool name from input parameter
                print("\n .... invalid tool call format ....")
                result = "invalid tool call format"
            elif t["name"] not in self.tools:
                # validate tool name from self.tools record
                print("\n .... bad tool name ....")
                result = "bad tool name, retry"
            else:
                # call all tools with their args
                result = self.tools[t["name"]].invoke(t["args"])

            results.append(ToolMessage(tool_call_id=t["id"], name=t["name"], content=str(result)))
        print("Back to the model")
        return {"messages" : results}
    
prompt = """
You are a smart research assistant. Use the search engine to look up information.
You are allowed to make multiple calls (either together or in sequence).
Only look up information when you are sure of what you want.
If you need to look up some information before asking a follow up question, you are allowed to do that. 
"""

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
a_bot = Agent(model, [tool], system=prompt)

# Save the PNG data to a file first
png_data = a_bot.graph.get_graph().draw_png()
with open("graph.png", "wb") as f:
    f.write(png_data)

# Now open and show the image using PIL
from PIL import Image
img = Image.open("graph.png")
img.show()


##########################
from langchain_core.messages import HumanMessage

messages = [HumanMessage(content="What is the weather in Tokyo?")]
# Wrap the messages in the correct AgentState format
initial_state = {"messages": messages}
result = a_bot.graph.invoke(initial_state)
print(result["messages"][-1].content)



##########################
# query = """
# who won the super bowl in 2024? In what state is the winning team headquarters located?
# what is the GDP of that state? Answer each question.
# """
# messages = [HumanMessage(content=query)]

# model = ChatOpenAI(model="gpt-4o")
# a_bot_2 = Agent(model, [tool], system=prompt)
# result = a_bot_2.graph.invoke({"messages": messages})
# print(result["messages"][-1].content)

