""" """

import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI

DEFAULT_LLM_MODEL = "gpt-3.5-turbo"

_ = load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]

DEFAULT_LLM_MODEL = "gpt-3.5-turbo"
# g_llm = ChatOpenAI(temperature=0.0, model=DEFAULT_LLM_MODEL)


class OpenAIHelper:
    def __init__(self, temperature=0.0, model=DEFAULT_LLM_MODEL):
        self.model = model
        self.temperature = temperature
        self.llm = ChatOpenAI(temperature=temperature, model=model)

    def get_llm(self):
        return self.llm

    def get_memory(self):
        return self.llm.memory
