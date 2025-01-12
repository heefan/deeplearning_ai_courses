from dotenv import load_dotenv
import os 
from tavily import TavilyClient

_ = load_dotenv()

client: TavilyClient = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

result: dict = client.search("What's in Nvidia's new Blackwell GPU", 
                            include_answer=True)

print(result["answer"])

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import re

ddg = DDGS()

def search(query: str, max_results: int = 6):
    try:
        results = ddg.text(query, max_results=max_results)
        return [i["href"] for i in results]
    except Exception as e:
        print(f"returning previous results due to exception reaching ddg.")
        results = [ # cover case where DDG rate limits due to high deeplearning.ai volume
            "https://weather.com/weather/today/l/USCA0987:1:US",
            "https://weather.com/weather/hourbyhour/l/54f9d8baac32496f6b5497b4bf7a277c3e2e6cc5625de69680e6169e7e38e9a8",
        ]
        return results  

city = "San Francisco"

query = f"""
    what is the current weather in {city}?
    Should I travel there today?
    "weather.com"
"""

for i in search(query):
    print(i)


def scrape_weather_info(url: str):
    if not url:
        return "weather information could not be found"
    
    headers = { "User-Agent": "Mozilla/5.0" }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Failed to retrieve the web page"
    
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

# use DuckDuckGo to find websites and take the first result
url = search(query)[0]

# scrape first wesbsite
soup = scrape_weather_info(url)

print(f"Website: {url}\n\n")
print(str(soup.body)[:50000]) # limit long outputs


## Agentic Search
# run search
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