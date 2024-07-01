from utils import get_open_ai_key
from autogen import ConversableAgent
from pprint import pprint

## Example : Standup Comedian Conversation

llm_config = {"model": "gpt-3.5-turbo"}

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
