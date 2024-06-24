""" LLM Chain  0.2.5 """

from utility import OpenAIHelper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from pprint import pprint

llm = OpenAIHelper(temperature=0.9).get_llm()

prompt = ChatPromptTemplate.from_template(
    "What is the best name to describe a company that makes {product}?"
)

chain = {"product": RunnablePassthrough()} | prompt | llm | StrOutputParser()

product = "Queen size sheet set"
result = chain.invoke(product)

pprint(result)
