""" 04 SequentialChain - langchain 0.2.5 """

from utility import OpenAIHelper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.base import RunnableSequence
from langchain.chains.sequential import SequentialChain
import pandas as pd

llm = OpenAIHelper().get_llm()

first_prompt = ChatPromptTemplate.from_template(
    "Translate the following review to English: \n\n{Review}"
)

chain_one = (
    {"Review": RunnablePassthrough()}
    | first_prompt
    | llm
    | StrOutputParser(output_key="{English_Review}")
)


# prompt template 2: Summarize the review
second_prompt = ChatPromptTemplate.from_template(
    "Can you summarize the following review in 1 sentence: \n\n{English_Review}?"
)

chain_two = (
    {"English_Review": RunnablePassthrough()}
    | second_prompt
    | llm
    | StrOutputParser(output_key="Summary")
)

# prompt template 3: identify the language
third_prompt = ChatPromptTemplate.from_template(
    "What language is the following review:\n\n{Review}"
)

# Chain 3: input= Review and output= language
chain_three = (
    {"Review": RunnablePassthrough()}
    | third_prompt
    | llm
    | StrOutputParser(output_key="language")
)

# prompt template 4: follow-up message
fourth_prompt = ChatPromptTemplate.from_template(
    "Write a follow-up response to the following summary in the specified language:\n\nSummary: {summary}\n\nLanguage: {language}"
)

# Chain 4: input= summary, language and output= followup_message
chain_four = (
    {"summary": RunnablePassthrough(), "language": RunnablePassthrough()}
    | fourth_prompt
    | llm
    | StrOutputParser(output_key="followup_message")
)

sequential_chain = RunnableSequence(chain_one, chain_two)

# Assuming df is defined elsewhere in your code
df = pd.read_csv("assets/Data.csv")
df.head()
review = df.Review[5]
result = sequential_chain.invoke({"Review": review})
print(result)
