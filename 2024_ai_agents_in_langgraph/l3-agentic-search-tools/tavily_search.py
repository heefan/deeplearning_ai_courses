from dotenv import load_dotenv
import os 
from tavily import TavilyClient

_ = load_dotenv()

client: TavilyClient = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
result: dict = client.search("What's in Nvidia's new Blackwell GPU", 
                             include_answer=True)

import json
data = {
    "result": result
}
print(json.dumps(data, indent=4))
print(result["answer"])
### Quesiton: Obviously `result` is a dict and have the `answer` key, but how do you know that `result` is a dict and has the `answer` key?
### Result: There is no define in source code, you need to examin the result to know the structure of the output. 

