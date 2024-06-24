""" 04 - Router Chain """

from pprint import pprint
from typing import TypedDict
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from utility import OpenAIHelper

llm = OpenAIHelper().get_llm()

# Define templates (unchanged)
PHYSICS_TEMPLATE = """You are a very smart physics professor. \
You are great at answering questions about physics in a concise\
and easy to understand manner. \
When you don't know the answer to a question you admit\
that you don't know.

Here is a question:
{input}"""

MATH_TEMPLATE = """You are a very good mathematician. \
You are great at answering math questions. \
You are so good because you are able to break down \
hard problems into their component parts, 
answer the component parts, and then put them together\
to answer the broader question.

Here is a question:
{input}"""

HISTORY_TEMPLATE = """You are a very good historian. \
You have an excellent knowledge of and understanding of people,\
events and contexts from a range of historical periods. \
You have the ability to think, reflect, debate, discuss and \
evaluate the past. You have a respect for historical evidence\
and the ability to make use of it to support your explanations \
and judgement.

Here is a question:
{input}"""

COMPUTERSCIENCE_TEMPLATE = """ You are a successful computer scientist.\
You have a passion for creativity, collaboration,\
forward-thinking, confidence, strong problem-solving capabilities,\
understanding of theories and algorithms, and excellent communication \
skills. You are great at answering coding questions. \
You are so good because you know how to solve a problem by \
describing the solution in imperative steps \
that a machine can easily interpret and you know how to \
choose a solution that has a good balance between \
time complexity and space complexity. 

Here is a question:
{input}"""

prompt_infos = [
    {
        "name": "physics",
        "description": "Good for answering questions about physics",
        "prompt_template": PHYSICS_TEMPLATE,
    },
    {
        "name": "math",
        "description": "Good for answering math questions",
        "prompt_template": MATH_TEMPLATE,
    },
    {
        "name": "History",
        "description": "Good for answering history questions",
        "prompt_template": HISTORY_TEMPLATE,
    },
    {
        "name": "computer science",
        "description": "Good for answering computer science questions",
        "prompt_template": COMPUTERSCIENCE_TEMPLATE,
    },
]

biology_template = """You are a knowledgeable biologist. \
You have a deep understanding of living organisms, their structures, \
functions, growth, evolution, and distribution. You can explain \
complex biological concepts in a clear and concise manner.

Here is a question:
{input}"""

# Add this to your prompt_infos list
prompt_infos.append(
    {
        "name": "biology",
        "description": "Good for answering biology questions",
        "prompt_template": biology_template,
    }
)

destination_chains = {}

for p_info in prompt_infos:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    prompt = ChatPromptTemplate.from_template(template=prompt_template)
    chain = prompt | llm
    destination_chains[name] = chain

destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)

default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = default_prompt | llm

MULTI_PROMPT_ROUTER_TEMPLATE = """Given a raw text input to a \
language model select the model prompt best suited for the input. \
You will be given the names of the available prompts and a \
description of what the prompt is best suited for. \
You may also revise the original input if you think that revising\
it will ultimately lead to a better response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \ name of the prompt to use or "DEFAULT"
    "next_inputs": string \ a potentially modified version of the original input
}}}}
```

REMEMBER: "destination" MUST be one of the candidate prompt \
names specified below OR it can be "DEFAULT" if the input is not\
well suited for any of the candidate prompts.
REMEMBER: "next_inputs" can just be the original input \
if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT (remember to include the ```json)>>"""

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
)


class RouterOutput(TypedDict):
    destination: str
    next_inputs: str


router_parser = JsonOutputParser(pydantic_object=RouterOutput)

router_chain = router_prompt | llm | router_parser


def route_and_run(inputs: dict):
    route = router_chain.invoke(inputs)
    destination = route["destination"]
    if destination in destination_chains:
        return destination_chains[destination].invoke(route["next_inputs"])
    else:
        print(
            f"Warning: {destination} not found in destination_chains. Using default chain."
        )
        return default_chain.invoke(route["next_inputs"])


chain = RunnableSequence(RunnablePassthrough(), route_and_run)

# Test the chain
pprint(chain.invoke("What is black body radiation?"))
pprint(chain.invoke("what is 2 + 2"))
pprint(chain.invoke("Why does every cell in our body contain DNA?"))
