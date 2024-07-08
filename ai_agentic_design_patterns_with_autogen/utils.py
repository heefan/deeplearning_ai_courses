""" utils functions """

import os
from dotenv import load_dotenv, find_dotenv


def load_env():
    _ = load_dotenv(find_dotenv)


def get_open_ai_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    return openai_api_key


def llm_config():
    return {"model": "gpt-3.5-turbo"}
