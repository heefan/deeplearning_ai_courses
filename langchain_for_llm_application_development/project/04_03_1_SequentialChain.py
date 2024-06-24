""" 04 - Sequential Chain - Langchain - 0.2.5 """

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from langchain_openai import OpenAI


# Initialize the language model
llm = OpenAI(temperature=0)

# Define prompt templates
name_prompt = PromptTemplate(
    input_variables=["person"],
    template="What is a good name for a company that makes {person}'s favorite product?",
)

slogan_prompt = PromptTemplate(
    input_variables=["company_name"],
    template="Write a catchy slogan for {company_name}.",
)

# Create runnable components
name_chain = (
    name_prompt
    | llm
    | (lambda x: {"company_name": x.strip(), "person": RunnablePassthrough()})
)
slogan_chain = (
    slogan_prompt
    | llm
    | (lambda x: {"slogan": x.strip(), "company_name": RunnablePassthrough()})
)

# Combine into a RunnableSequence
sequential_chain = RunnableSequence(name_chain, slogan_chain)

# Run the chain
result = sequential_chain.invoke({"person": "Elon Musk"})
print(f"Company Name: {result['company_name']}")
print(f"Slogan: {result['slogan']}")
