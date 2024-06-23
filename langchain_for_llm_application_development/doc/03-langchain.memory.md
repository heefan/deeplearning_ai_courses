# Langchain Memory 

`0.2.5`

`memory.buffer` 

* ConversationBufferMemory 
   >This memory allows for storing of messages and then extracts the messages in a variable
   
   [0.2.5 doc](https://api.python.langchain.com/en/latest/memory/langchain.memory.buffer.ConversationBufferMemory.html#langchain.memory.buffer.ConversationBufferMemory)

* ConversationStringBufferMemory
   >This memory keeps a list of the interactions of the conversation over time. It only uses the last k iteractions.
* ConversationTokenBufferMemory - `langchain.memory.token_buffer`
   >This memory keeps a buffer of recent iteractions in memory, and uses token length rather than number of interactions to determine when to flush interactions.
* ConversationSummaryMemory - Conversation summarizer to chat memory.
   >This memory creates a summary of the conversation over time.



```python
completion = llm.predict(text="hi, my name is Andrew")
```
The method `BaseChatModel.predict` was deprecated in langchain-core 0.1.7 and will be removed in 0.3.0. Use invoke instead.

Use 
```python
completion = llm.invoke(input="hi, my name is Andrew")
```




Reference: 

[langchain.memory](https://api.python.langchain.com/en/latest/langchain_api_reference.html#module-langchain.memory)
[Andrew course code](https://learn.deeplearning.ai/courses/langchain/lesson/3/memory)