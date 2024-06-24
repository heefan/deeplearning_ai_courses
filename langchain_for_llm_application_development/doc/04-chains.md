# Chains 

`0.2.5`

1. `LLMChain` will be deprecated in v0.3.0, so do not use it. 
2. Try to use `RunnableSequence` instead of `LLMChain`


Error Message

```
Unexpected keyword argument 'steps' in constructor callPylintE1123:unexpected-keyword-arg
class RunnableSequence(*steps: RunnableLike, name: Optional[str]=None, first: Optional[Runnable[Any, Any]]=None, middle: Optional[List[Runnable[Any, Any]]]=None, last: Optional[Runnable[Any, Any]]=None)
Sequence of Runnables, where the output of each is the input of the next.

RunnableSequence is the most important composition operator in LangChain as it is used in virtually every chain.

A RunnableSequence can be instantiated directly or more commonly by using the | operator where either the left or right operands (or both) must be a Runnable.

Any RunnableSequence automatically supports sync, async, batch.
```

Error Message


```
Traceback (most recent call last):
  File "/Users/litian/github/deeplearning_ai_courses/langchain_for_llm_application_development/project/04_03_SequentialChain.py", line 108, in <module>
    sequential_chain = SequentialChain(
                       ^^^^^^^^^^^^^^^^
  File "/Users/litian/github/deeplearning_ai_courses/langchain_for_llm_application_development/venv/lib/python3.11/site-packages/pydantic/v1/main.py", line 339, in __init__
    values, fields_set, validation_error = validate_model(__pydantic_self__.__class__, data)
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/litian/github/deeplearning_ai_courses/langchain_for_llm_application_development/venv/lib/python3.11/site-packages/pydantic/v1/main.py", line 1048, in validate_model
    input_data = validator(cls_, input_data)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/litian/github/deeplearning_ai_courses/langchain_for_llm_application_development/venv/lib/python3.11/site-packages/langchain/chains/sequential.py", line 64, in validate_chains
    missing_vars = set(chain.input_keys).difference(known_variables)
                       ^^^^^^^^^^^^^^^^
AttributeError: 'RunnableSequence' object has no attribute 'input_keys'
```



if we use `SequentialChain` with pipeline, it gets the problem.  We shall use `RunnableSequential` to instead of using `SequentialChain`

```python
# Define prompt templates
name_prompt = PromptTemplate(
    input_variables=["person"],
    template="What is a good name for a company that makes {person}'s favorite product?",
)

slogan_prompt = PromptTemplate(
    input_variables=["company_name"],
    template="Write a catchy slogan for {company_name}.",
)

# Create runnable components
name_chain = name_prompt | llm | RunnablePassthrough.assign(company_name=lambda x: x.strip())
slogan_chain = slogan_prompt | llm

# Combine into a SequentialChain
sequential_chain = SequentialChain(
    chains=[name_chain, slogan_chain],
    input_variables=["person"],
    output_variables=["company_name", "text"],
    verbose=True
)
```

In the old version, you can use `SequentialChain` with `LLMChain`


