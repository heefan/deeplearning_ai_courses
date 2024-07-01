from utils import get_open_ai_key
from autogen import ConversableAgent
from pprint import pprint

llm_config = {"model": "gpt-3.5-turbo"}

## Basic Example of creating a agent

agent = ConversableAgent(
    name="chatbot", llm_config=llm_config, human_input_mode="NEVER"
)

reply = agent.generate_reply(messages=[{"content": "Tell me a joke", "role": "user"}])
print(reply)

reply = agent.generate_reply(messages=[{"content": "repeat me a joke", "role": "user"}])
print(reply)
print("\n\n\n")

## Example : Standup Comedian Conversation

cathy = ConversableAgent(
    name="cathy",
    system_message="your name is Cathy and you are a stand-up comedian",
    llm_config=llm_config,
    human_input_mode="NEVER",
)


joe = ConversableAgent(
    name="joe",
    system_message="""Your name is Joe and you are a stand-up comedian \n
    Start the next joke from the punchline of the previous joke""",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

chat_result = joe.initiate_chat(
    recipient=cathy,
    message="I'm Joe, Cathy, let's keep the joke rolling",
    max_turns=2,
)

pprint(chat_result.chat_history)
pprint(chat_result.cost)
pprint(chat_result.summary)
print("\n\n\n")

## chat termination
cathy = ConversableAgent(
    name="cathy",
    system_message="your name is Cathy and you are a stand-up comedian"
    "when you're ready to end the conversation, say 'I gotta go'",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"],
)

joe = ConversableAgent(
    name="joe",
    system_message="Your name is Joe and you are a stand-up comedian"
    "when you're ready to end the conversation, say 'I gotta go'",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"],
)

chat_result = joe.initiate_chat(
    recipient=cathy,
    message="I'm Joe, Cathy, let's keep the joke rolling",
    max_turns=4,
)

cathy.send(message="I gotta go", recipient=joe)
