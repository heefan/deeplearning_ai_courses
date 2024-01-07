from helper.utils import build_sentence_window_index, get_sentence_window_query_engine, get_prebuilt_trulens_recorder
from helper.logger import  log_info
import openai
from openai import OpenAI
from llama_index import SimpleDirectoryReader, Document, VectorStoreIndex, ServiceContext

pdf_book = "testing_assets/eBook-How-to-Build-a-Career-in-AI.pdf"

openai.api_key = utils.get_openai_api_key()
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)


#### Ingest PDF
documents = SimpleDirectoryReader(input_files=[pdf_book]).load_data()
document = Document(text="\n\n".join([doc.text for doc in documents]))

sentence_index = build_sentence_window_index(
    document,
    llm,
    embed_model="local:BAAI/bge-small-en-v1.5",
    save_dir="sentence_index",
)

#### Query Engine
sentence_query_engine = get_sentence_window_query_engine(sentence_index)

output = sentence_query_engine.query("How do you create AI portfolio?")
log_info(output.response)
