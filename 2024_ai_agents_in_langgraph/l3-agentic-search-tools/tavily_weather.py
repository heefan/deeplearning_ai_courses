from tavily import TavilyClient
import os

query = "what's the weather in Singapore today"

client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
result = client.search(query, max_results=1)

# print first result
data = result["results"][0]["content"]

print(data)

import json
from pygments import highlight, lexers, formatters

# parse JSON
parsed_json = json.loads(data.replace("'", '"'))

# pretty print JSON with syntax highlighting
formatted_json = json.dumps(parsed_json, indent=4)
colorful_json = highlight(formatted_json,
                          lexers.JsonLexer(),
                          formatters.TerminalFormatter())

print(colorful_json)