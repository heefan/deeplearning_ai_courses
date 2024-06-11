from langchain_openai import ChatOpenAI


DEFAULT_LLM_MODEL = "gpt-3.5-turbo"
chat = ChatOpenAI(temperature=0.0), model = DEFAULT_LLM_MODEL)

print(chat)