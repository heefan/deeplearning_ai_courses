import utils
import openai
from logger import log_info
from llama_index import SimpleDirectoryReader, Document, VectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI
from trulens_eval import Tru
from utils import build_sentence_window_index, get_sentence_window_query_engine, get_prebuilt_trulens_recorder

openai.api_key = utils.get_openai_api_key()
pdf_book = "testing_assets/eBook-How-to-Build-a-Career-in-AI.pdf"


# Trulens dashboard launches on http://localhost:8501/

class RagPipeLine:

    ## init function
    def __init__(self):
        self.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)

        ## PDF chunking
        input_files = [pdf_book]
        self.documents = SimpleDirectoryReader(input_files=input_files).load_data()
        self.document = Document(text="\n\n".join([doc.text for doc in self.documents]))
        # log_info(type(self.documents))
        # log_info(len(self.documents))
        # log_info(type(self.documents[0]))
        # log_info(self.documents[0])

        ## Evaluation Questions
        self.eval_questions = []
        with open('testing_assets/eval_questions.txt', 'r') as file:
            for line in file:
                # Remove newline character and convert to integer
                item = line.strip()
                self.eval_questions.append(item)

        new_question = "What is the right AI job for me?"
        self.eval_questions.append(new_question)
        log_info(self.eval_questions)

        ## Trulens setup
        self.tru = Tru()
        self.tru.reset_database()


    ### Evaluation setup using TruLens
    def direct_evaluate(self):
        service_context = ServiceContext.from_defaults(
            llm=self.llm,
            embed_model="local:BAAI/bge-small-en-v1.5"
        )
        direct_index = VectorStoreIndex.from_documents([self.document], service_context=service_context)

        direct_query_engine = direct_index.as_query_engine()
        response = direct_query_engine.query(
            "what are steps to take when finding projects to build your experience?"
        )

        log_info(str(response))
        self.tru.reset_database()
        tru_recorder = get_prebuilt_trulens_recorder(
            direct_query_engine,
            app_id="Direct Query Engine"
        )

        self._generate_trulens_dashboard(tru_recorder, direct_query_engine)



    ##############################################################
    # Advanced RAG Pipeline
    #   - Sentence Window retrieval
    # pip install torch sentence-transformers
    ##############################################################
    def sentence_window_evaluate(self):
        sentence_index = build_sentence_window_index(self.document,
                                                     self.llm,
                                                     embed_model="local:BAAI/bge-small-en-v1.5",
                                                     save_dir="sentence_index")

        sentence_window_engine = get_sentence_window_query_engine(sentence_index)

        window_response = sentence_window_engine.query("how do I get started on a personal project in AI")
        log_info(window_response)


        self.tru.reset_database()
        tru_recorder_sentence_window = get_prebuilt_trulens_recorder(
            sentence_window_engine,
            app_id="Sentence Window Query Engine"
        )

        self._generate_trulens_dashboard(tru_recorder_sentence_window, sentence_window_engine)


    def automerging_evaluate(self):
        automerging_index = utils.build_automerging_index(
            self.documents,
            self.llm,
            embed_model="local:BAAI/bge-small-en-v1.5",
            save_dir="merging_index"
        )

        automerging_query_engine = utils.get_automerging_query_engine(
            automerging_index,
        )

        auto_merging_response = automerging_query_engine.query(
            "How do I build a portfolio of AI projects?"
        )

        log_info(str(auto_merging_response))

        self.tru.reset_database()

        tru_recorder_automerging = utils.get_prebuilt_trulens_recorder(
            automerging_query_engine,
            app_id="Automerging Query Engine"
        )

        self._generate_trulens_dashboard(tru_recorder_automerging, automerging_query_engine)


    #################################################################################
    #   PRIVATE METHODS
    #################################################################################
    def _generate_trulens_dashboard(self, tru_recorder, query_engine):
        self.tru.reset_database()

        for question in self.eval_questions:
            with tru_recorder as recording:
                response = query_engine.query(question)
                # log_info(question)
                # log_info(response)

        records, feedback = self.tru.get_records_and_feedback(app_ids=[])
        records.head()
        self.tru.get_leaderboard(app_ids=[])
        self.tru.run_dashboard()




if __name__ == "__main__":
    rag_pipeline = RagPipeLine()
    rag_pipeline.direct_evaluate()

