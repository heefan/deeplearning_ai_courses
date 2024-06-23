"""  Langchain 0.2.5 - Memory """

from pprint import pprint
from utility import OpenAIHelper
from langchain.memory.buffer import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain


helper = OpenAIHelper()
memory = ConversationBufferMemory()
llm = helper.get_llm()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

conversation.invoke(input="hi, my name is Andrew")
conversation.invoke(input="what is 1+1?")
conversation.invoke(input="what is my name?")

# memory.load_memory_variables({})

memory.save_context({"input": "Hi"}, {"output": "whats up?"})

pprint(memory.chat_memory.messages)
