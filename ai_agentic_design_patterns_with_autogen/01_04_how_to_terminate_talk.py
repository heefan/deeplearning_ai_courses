from utils import get_open_ai_key
from autogen import ConversableAgent
from pprint import pprint

llm_config = {"model": "gpt-3.5-turbo"}

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
