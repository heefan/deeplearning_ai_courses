"""This module is the for the testing of lecture 2 """

import os
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]

DEFAULT_LLM_MODEL = "gpt-3.5-turbo"


def get_completion(prompt, model=DEFAULT_LLM_MODEL):
    message = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
        model=model,
        messages=message,
        temperature=0.0,
    )
    return response.choices[0].message.content


get_completion("what is 1+1")

CUSTOMER_EMAIL = """
Arrr, I be fuming that me blender lid \
flew off and splattered me kitchen walls \
with smoothie! And to make matters worse,\
the warranty don't cover the cost of \
cleaning up me kitchen. I need yer help \
right now, matey!
"""

STYLE = """American English \
in a calm and respectful tone
"""

PROMPT = f"""Translate the text \
that is delimited by triple backticks 
into a style that is {STYLE}.
text: ```{CUSTOMER_EMAIL}```
"""

# Remove the redefinition of 'response' variable
print(get_completion(PROMPT))
