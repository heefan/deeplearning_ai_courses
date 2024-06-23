from pprint import pprint
from langchain.memory.token_buffer import ConversationTokenBufferMemory
from utility import OpenAIHelper


llm = OpenAIHelper().get_llm()

memory = ConversationTokenBufferMemory(llm=llm, max_tokens=50)
memory.save_context({"input": "AI is what?!"}, {"output": "Amazing"})
memory.save_context({"input": "Backpropagation is what?"}, {"output": "Beautiful!"})
memory.save_context({"input": "Chatbots are what?"}, {"output": "Charming!"})

pprint(memory.load_memory_variables({}))
