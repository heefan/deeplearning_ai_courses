from pprint import pprint
from langchain.memory.summary import ConversationSummaryMemory
from langchain.chains.conversation.base import ConversationChain
from utility import OpenAIHelper

llm = OpenAIHelper().get_llm()
memory = ConversationSummaryMemory(llm=llm, max_tokens=100)

SCHEDULE = "There is a meeting at 8am with your product team. \
You will need your powerpoint presentation prepared. \
9am-12pm have time to work on your LangChain \
project which will go quickly because Langchain is such a powerful tool. \
At Noon, lunch at the italian resturant with a customer who is driving \
from over an hour away to meet you to understand the latest in AI. \
Be sure to bring your laptop to show the latest LLM demo."

memory.save_context({"input": "Hello"}, {"output": "What's up"})
memory.save_context({"input": "Not much, just hanging"}, {"output": "Cool"})
memory.save_context(
    {"input": "What is on the schedule today?"}, {"output": f"{SCHEDULE}"}
)

pprint(memory.load_memory_variables({}))

conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
conversation.invoke(input="what would be a good demo to show?")

pprint(memory.load_memory_variables({}))
