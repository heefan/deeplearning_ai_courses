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


##### Basic RAG Pipeline #####
from llama_index import Document

document = Document(text="\n\n".join([doc.text for doc in documents]))

from llama_index import VectorStoreIndex
from llama_index import ServiceContext
from llama_index.llms import OpenAI

llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model="local:BAAI/bge-small-en-v1.5"
)
index = VectorStoreIndex.from_documents([document], service_context=service_context)

query_engine = index.as_query_engine()
response = query_engine.query(
    "what are steps to take when finding projects to build your experience?"
)

log_info(str(response))