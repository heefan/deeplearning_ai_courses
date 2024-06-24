""" 04.Chain - SimpleSequentialChain """

from utility import OpenAIHelper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.passthrough import RunnablePassthrough
from pprint import pprint

llm = OpenAIHelper(temperature=0.9).get_llm()

# chain_1
first_prompt = ChatPromptTemplate.from_template(
    "What is the best name to describe a company that makes {product}?"
)
chain_one = first_prompt | llm | StrOutputParser()

# chain_2
second_prompt = ChatPromptTemplate.from_template(
    "Write a 20 words description for the following company: {company_name}"
)
chain_two = second_prompt | llm | StrOutputParser()

# Combining the chains
overall_chain = (
    {"product": RunnablePassthrough()}
    | chain_one
    | {"company_name": RunnablePassthrough()}
    | chain_two
)

product = "Queen Size sheet set"
result = overall_chain.invoke(product)

pprint(result)
