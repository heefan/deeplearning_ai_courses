""" https://python.langchain.com/v0.2/docs/how_to/  
LangChain: Models, Prompts and Output Parsers

Outline
1. Direct API calls to OpenAI
2. API calls through LangChain:
    Prompts
    Models
    Output parsers

Reference
"""

from pprint import pprint
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

TEMPLATE_STRING = """Translate the text \
that is delimited by triple backticks \
into a style that is {style}. \
text = ```{text}```
"""

CUSTOMER_STYLE = """American English in a calm and respectful tone """

CUSTOMER_EMAIL = """
Arrr, I be fuming that me blender lid \
flew off and splattered me kitchen walls \
with smoothie! And to make matters worse, \
the warranty don't cover the cost of \
cleaning up me kitchen. I need yer help \
right now, matey!
"""

prompt = PromptTemplate(template=TEMPLATE_STRING, input_variables=["style", "text"])

DEFAULT_LLM_MODEL = "gpt-3.5-turbo"
llm = ChatOpenAI(temperature=0.0, model=DEFAULT_LLM_MODEL)
chain = prompt | llm
result = chain.invoke({"style": CUSTOMER_STYLE, "text": CUSTOMER_EMAIL})
pprint(result)


"""
reference: 
https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.prompt.PromptTemplate.html
"""
