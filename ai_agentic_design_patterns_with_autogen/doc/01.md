# Lesson 1 - Multi Agent Conversation

Questions:
What is agent? How can agent help me? 


## A Basic Example  `ConverableAgent`
1. Create an agent
2. Send llm message "Tell me a joke"
3. Wait the reply from llm

```python
agent = ConversableAgent(
    name="chatbot",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

reply = agent.generate_reply(
    message=[{"content": "Tell me a joke"}, {"role": "user"}],
)
```


## Example 1 - A conversation between cathy and joe

cathy and joe are stand-up comedian. Make a conversation of them. 
Just make two rounds of conversation 

```python
cathy = ConversableAgent(
    name="cathy",
    system_message="your name is Cathy and you are a stand-up comedian."
    llm_config=llm_config,
    human_input_mode="NEVER",
)

joe = ConversableAgent(
    name="joe",
    system_message="your name is Joe and you are a stand-up comedian"
    "Start the next joke from the punchline of the previous joke",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

# Joe start talking
chat_result = joe.initiate_chat(
    recipient=cathy,
    message="I'm Joe. Cathy, let's keep the joke rolling",
    max_turns=2,
)

pprint(chat_result.chat_history)
pprint(chat_result.cost)
pprint(chat_result.summary)
```

### Example 2  - Terminate condition (Lambda)

After a few rounds of conversation, someone say "I gotta go" then the conversation should end up.


### Example 3 - Summary of the conversation



```python
# when someone say "I gotta go" then terminate the conversation
cathy = ConversableAgent(
    ...
    is_termination_msg=lambda msg:'I gotta go' in msg["Content"]
)

joe = ConversableAgent(
    ...
    is_termination_msg=lambda msg:'I gotta go' in msg["Content"]
)

chat_result = 



```




Question: 


[01](https://learn.deeplearning.ai/courses/ai-agentic-design-patterns-with-autogen/lesson/2/multi-agent-conversation-and-stand-up-comedy)