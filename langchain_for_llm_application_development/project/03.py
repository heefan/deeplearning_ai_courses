"""  Langchain - Memory """

from utility import Helper
from langchain.memory.buffer import ConversationBufferMemory
from langchain.conversation.base import ConversationChain


helper = Helper()
llm = helper.get_llm()
memory = ConversationBufferMemory()

conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
