from utils import get_open_ai_key
from autogen import ConversableAgent


llm_config = {"model": "gpt-3.5-turbo"}

agent = ConversableAgent(
    name = "chatbot",
    llm_config = llm_config,
    human_input_mode = "NEVER"
)

reply = agent.generate_reply(
    messages = [{"content": "Tell me a joke", "role": "user"}]
)
print(reply)

reply = agent.generate_reply(
    message = [{"content": "Repeat the joke", "role": "user"}]
)

print(reply)
