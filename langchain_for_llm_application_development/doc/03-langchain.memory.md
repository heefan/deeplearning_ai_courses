# Langchain Memory 

`0.2.5`

`memory.buffer` 

* ConversationBufferMemory 
   [0.2.5](https://api.python.langchain.com/en/latest/memory/langchain.memory.buffer.ConversationBufferMemory.html#langchain.memory.buffer.ConversationBufferMemory)

* ConversationStringBufferMemory
* ConversationTokenBufferMemory
* ConversationSummaryMemory - Conversation summarizer to chat memory.



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