import os
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain_core.runnables.history import RunnableWithMessageHistory

from utils import utils
from config import Config

doc_path = "document"


# model_kwargs = {'device': 'cpu','trust_remote_code': True}
# encode_kwargs = {'normalize_embeddings': False}

model = Config.model

store = {}

def get_rag_chain(doc_obj,file_name):
    chunks = utils.split_chunks(doc_obj)
    chroma_db = utils.write_to_db(chunks,file_name)
    retriever = utils.get_retriever(chroma_db)
    qa_rag_chain = utils.create_qa_rag_chain(retriever)
    chat_hist_prompt = utils.create_chat_history_prompt()
    re_rank_retriver = utils.re_rank_retriver(retriever)
    combined_retriver = utils.ensemble_retrivers(retriever,re_rank_retriver)
    history_aware_retriever = create_history_aware_retriever(
        Config.llm, combined_retriver, chat_hist_prompt
        )
    qa_chain = utils.create_qa_chain(history_aware_retriever)
    # store_history = utils.get_session_history("ab12")
    conversational_rag_chain = RunnableWithMessageHistory(
                                qa_chain,
                                utils.get_session_history,
                                input_messages_key="input",
                                history_messages_key="chat_history",
                                output_messages_key="answer",
                            )
    return conversational_rag_chain


# def main():
#     doc_obj = utils.load_doc(doc_path)
#     print(doc_obj)
#     chunks = utils.split_chunks(doc_obj)
#     chroma_db = utils.write_to_db(chunks)
#     retriever = utils.get_retriever(chroma_db)
#     qa_rag_chain = utils.create_qa_rag_chain(retriever)
#     chat_hist_prompt = utils.create_chat_history_prompt()
#     re_rank_retriver = utils.re_rank_retriver(retriever)
#     combined_retriver = utils.ensemble_retrivers(retriever,re_rank_retriver)
#     history_aware_retriever = create_history_aware_retriever(
#         Config.llm, combined_retriver, chat_hist_prompt
#         )
#     qa_chain = utils.create_qa_chain(history_aware_retriever)
#     # store_history = utils.get_session_history("ab12")
#     conversational_rag_chain = RunnableWithMessageHistory(
#                                 qa_chain,
#                                 utils.get_session_history,
#                                 input_messages_key="input",
#                                 history_messages_key="chat_history",
#                                 output_messages_key="answer",
#                             )
#     print(conversational_rag_chain.invoke(
#     {"input": "What are the saptarishi priorities mentioned in the document?"},
#     config={
#         "configurable": {"session_id": "02"}
#     },  # constructs a key "abc123" in `store`.
#     )["answer"])

#     print(chroma_db)

# if __name__ == "__main__":
#     main()