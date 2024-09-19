from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.ensemble import EnsembleRetriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import yt_dlp
from langchain.docstore.document import Document
import re
from langchain.vectorstores import DeepLake
import yaml
from config import Config

ffmpeg_path = "/usr/bin/ffmpeg"  # Replace this with the actual path to ffmpeg if not in PATH

# param_dict = yaml.safe_load('param.yaml'
with open("param.yaml") as stream:
    param_dict = yaml.safe_load(stream)

store = {}

def load_doc(doc_path):
    loader =  PyPDFDirectoryLoader(doc_path)
    docs = loader.load()
    return docs

def split_chunks(doc_obj):
    splitters = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=0)
    chunks = splitters.split_documents(doc_obj)
    return chunks

def write_to_db(chunked_docs,file_name):

    filename= re.sub('[^A-Za-z0-9]+', '', file_name)
    # db = DeepLake.from_documents(chunked_docs, dataset_path=f"./database/{filename}/", embedding=Config.model)
    db = Chroma.from_documents(documents=chunked_docs, collection_name=filename,
                                        embedding=Config.model,
                                        # need to set the distance function to cosine else it uses euclidean by default
                                        # check https://docs.trychroma.com/guides#changing-the-distance-function
                                        collection_metadata={"hnsw:space": "cosine"},
                                        persist_directory=None)
    return db

def get_retriever(chroma_db):
    similarity_retriever = chroma_db.as_retriever(search_type="similarity_score_threshold",
                                                  search_kwargs={"k": 5, "score_threshold": 0.2})
    return similarity_retriever

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_qa_rag_chain(retriever):
    prompt_template = ChatPromptTemplate.from_template(param_dict['qa_prompt'])
    qa_rag_chain = ({
        "context": (retriever|format_docs),
        "question": RunnablePassthrough()}
        |
        prompt_template
        |
        Config.llm
        )
    query = "Explain about PM Matsya Sampada Yojana ?"
    # query = "Explain about PM Matsya Sampada Yojana ?"
    result = qa_rag_chain.invoke(query)
    return qa_rag_chain

def create_chat_history_prompt():
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", param_dict['contextualize_q_system_prompt']),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    return contextualize_q_prompt

def re_rank_retriver(retriever):
    compressor = CrossEncoderReranker(model=Config.re_rank_model, top_n=3)
    re_rank_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
        )
    return re_rank_retriever

def ensemble_retrivers(retriever,re_rank_retriever):
    dual_retrievers = [retriever,re_rank_retriever]
    ensemble_retriever = EnsembleRetriever(retrievers=dual_retrievers, weights=[0.5, 0.5])
    return ensemble_retriever

def create_qa_chain(history_aware_retriever):
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", param_dict['system_prompt']),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
        )
    question_answer_chain = create_stuff_documents_chain(Config.llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

    # result = qa_rag_chain.invoke(query)
    # return qa_rag_chain


def download_audio(youtube_url, ffmpeg_path=''):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        audio_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')
    return audio_file_path

def extract_text_from_audio(audio_file_path):
    if 'm4a' in audio_file_path:
        audio_file_path = audio_file_path.replace('m4a','mp3')
    result = Config.whisper_model.transcribe(audio_file_path)
    doc_obj = [Document(result['text'])]
    return doc_obj

def process_ytb_video(yt_url):
    audio_file_path = download_audio(yt_url, ffmpeg_path)
    docobj = extract_text_from_audio(audio_file_path)
    # runner(is_video_img_content=True,doc_obj=docobj)
    return {"status": "Success"} ,docobj

