import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import json
from typing import TypedDict
from requests import Response
import re

ddg = DDGS()

query = """ 
what is the current weather in Singapore?
Should I travel there today?
"weather.com"
"""

import logging
DEBUG = False
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

class SearchResult(TypedDict):
    title: str
    link: str
    href: str
    body: str

def search(query: str, max_results: int = 6) -> list[str]: 
    try:
        results: list[SearchResult] = ddg.text(query, max_results=max_results)
        logging.debug(json.dumps({"results": results}, indent=4))
        return [result["href"] for result in results]
    
    except Exception as e:
        logging.info(f"returning previous results due to exception reaching ddg. {e}")
        return results  


def scrape_weather_info(url: str) -> str:
    try:
        headers = {"User-Agent":"Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        weather_data = []
        for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
            text = tag.get_text(" ", strip=True)
            weather_data.append(text)

        # combine all elements into a single string
        weather_data = "\n".join(weather_data)

        # remove all spaces from the combined text
        weather_data = re.sub(r'\s+', ' ', weather_data)

        return weather_data
    except Exception as e:
        logging.error(f"Error scraping weather info: {e}")
        return ""

# Usage
urls = search("singapore weather")
print(urls)
if urls:
    scrape_weather_info(urls[0])
else:
    logging.info("No search results found")


