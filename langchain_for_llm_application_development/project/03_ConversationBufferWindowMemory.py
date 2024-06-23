from pprint import pprint
from langchain.memory.buffer_window import ConversationBufferWindowMemory
from langchain.chains.conversation.base import ConversationChain
from utility import OpenAIHelper


# This means it will only keep the most recent conversation turn (one input-output pair).
memory = ConversationBufferWindowMemory(k=1)

# These lines save two conversation turns to the memory. However, because k=1, only the most recent turn will be retained.
memory.save_context({"input": "Hi"}, {"output": "whats up?"})
memory.save_context({"input": "Not much, just hanging"}, {"output": "cool"})

memory.load_memory_variables({})

pprint(memory.chat_memory.messages)

llm = OpenAIHelper().get_llm()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
conversation.invoke("Hi")
conversation.invoke("what is 1+1?")
conversation.invoke("what is my name?")
