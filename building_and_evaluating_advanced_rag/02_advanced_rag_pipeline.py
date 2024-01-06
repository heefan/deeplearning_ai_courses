import utils
import openai
from logger import log_info
from llama_index import SimpleDirectoryReader

openai.api_key = utils.get_openai_api_key()


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

## Evaluation setup using TruLens
eval_questions = []
with open('testing_assets/eval_questions.txt', 'r') as file:
    for line in file:
        # Remove newline character and convert to integer
        item = line.strip()
        print(item)
        eval_questions.append(item)

new_question = "What is the right AI job for me?"
eval_questions.append(new_question)
print(eval_questions)

from trulens_eval import Tru
tru = Tru()

tru.reset_database()

from utils import get_prebuilt_trulens_recorder

tru_recorder = get_prebuilt_trulens_recorder(query_engine,
                                             app_id="Direct Query Engine")

with tru_recorder as recording:
    for question in eval_questions:
        response = query_engine.query(question)

records, feedback = tru.get_records_and_feedback(app_ids=[])

records.head()

tru.run_dashboard()