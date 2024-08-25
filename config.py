from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from dotenv import load_dotenv,find_dotenv
import whisper
import torch


load_dotenv()

model_kwargs = {'device': 'cpu','trust_remote_code': True}
encode_kwargs = {'normalize_embeddings': False}

class Config:
    model = HuggingFaceEmbeddings(          
            model_name="nomic-ai/nomic-embed-text-v1.5",
            # model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    whisper_model = whisper.load_model("tiny", device=device)
    llm = chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    re_rank_model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
    
