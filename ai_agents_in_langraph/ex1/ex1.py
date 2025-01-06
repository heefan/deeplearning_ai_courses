# Simple ReAct Agent from Scratch

import openai
from openai import OpenAI
from pprint import pprint

client = OpenAI()

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "system", "content": result})
        return result
    
    def execute(self) -> str:
        completion = client.chat.completions.create(
                        model="gpt-4o", 
                        temperature=0,
                        messages=self.messages)
        return completion.choices[0].message.content
    
prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output and Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE
Observation will be the result of running those actions

Your available actions are:

calculate: 
e.g. calculate 4 * 7 / 3
Runs a calculation and returns the result - use Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed. 


Example session: 

Question: how much does a Bulldog weight? 
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A bulldog weights 50 lbs

You then output:

Answer: A bulldog weights 50 lbs

""".strip()

def calculate(what):
    return eval(what)

def average_dog_weight(name: str) -> str:
    if name in "Scottish Terrier": 
        return("Scottish Terriers average 20 lbs")
    elif name in "Border Collie":
        return("a Border Collies average weight is 37 lbs")
    elif name in "Toy Poodle":
        return("a Toy Poodles average weight is 7 lbs")
    else:
        return("An average dog weights 50 lbs")
    
known_actions = {
    "calculate": calculate,
    "average_dog_weight": average_dog_weight
}


agent = Agent(prompt)
result = agent("How much does a Toy Poodle weight?")
# pprint(result.content)

result = average_dog_weight("Toy Poodle")
# pprint(result)

next_prompt = "Observation: {}".format(result)
pprint(agent.messages)
