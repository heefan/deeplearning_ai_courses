import utils
import openai
from logger import log_info
from llama_index import SimpleDirectoryReader

openai.api_key = utils.get_open_ai_key()


documents = (SimpleDirectoryReader(input_files=["testing_assets/eBook-How-to-Build-a-Career-in-AI.pdf"]).load_data())

log_info(type(documents))
log_info(len(documents))
log_info(type(documents[0]))
log_info(documents[0])
