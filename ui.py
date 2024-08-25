import streamlit as st
import requests
from PyPDF2 import PdfReader
# from utils import utils
from langchain.docstore.document import Document
from main import get_rag_chain

# res_response,qa_rag_chain = None,None

global res_response 
global qa_rag_chain

img_formats = ['png','jpg','jpeg']
img_repr = ['image/png','image/jpeg','image/jpeg']


if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = False
if 'url_accepted' not in st.session_state:
    st.session_state['url_accepted'] = False
if 'response' not in st.session_state:
    st.session_state['response'] = None
if 'query' not in st.session_state:
    st.session_state['query'] = ""
if 'uploaded_file_content' not in st.session_state:
    st.session_state['uploaded_file_content'] = None
if 'qa_rag' not in st.session_state:
    st.session_state['qa_rag'] = None

# if "messages" not in st.session_state:
#     st.session_state.messages = []


def read_pdf(uploaded_file,file_name):
    # uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        file_data = uploaded_file.getvalue()
        # print(file_data)
        pages_list = []
        text = ""
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
            pages_list.append(Document(page.extract_text()))
        print(len(pages_list))
        rag_chain = get_rag_chain(pages_list,file_name)
        return "Success",rag_chain


def handle_file_upload(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1]
    print("uploaded_file.name--------------------",uploaded_file.name.split('.'))
    file_name = uploaded_file.name.split('.')[0]
    if file_extension in ["pdf","doc", "docx", "jpg", "png"]:
        with st.spinner('Wait for setting up the VectorDB'):
            response,rag_chain = read_pdf(uploaded_file,file_name)
            return response,rag_chain            
    else:
        st.error("Invalid file type.")

st.header('ContentInsightsRAG')
st.header('Select Source')
genre = st.radio("Select an Option", ["", "Text Files","Image", "Video"])
st.session_state['session_id'] = 100
if (genre == "Text Files") or (genre == "Image"):
    st.write("You have selected Text Files")
    uploaded_file = st.file_uploader("Choose a file")
    # print(uploaded_file)
    if uploaded_file:
        if st.session_state['uploaded_file_content'] != uploaded_file.getvalue():
            print("FILE CHANGED SESSION CREATED-----------------------------------",uploaded_file.name)
            st.session_state['session_id'] = uploaded_file.name
            print("SESSION STATE0----------------------------------",st.session_state['session_id'])
            if 'qa_rag' in  st.session_state:
                del st.session_state['qa_rag']
            if 'messages' in  st.session_state:
                del  st.session_state['messages']
            res_response,qa_rag_chain = handle_file_upload(uploaded_file) 
            st.session_state['qa_rag'] = qa_rag_chain  
        # else:
            
        if "messages" not in st.session_state.keys(): # Initialize the chat message history
            st.session_state.messages = [
                {"role": "assistant", "content": "Ask me a question about uploaded document!"}
            ]

        st.session_state['uploaded_file_content'] = uploaded_file.getvalue()
        st.session_state['session_id'] = 100
        if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

        for message in st.session_state.messages: # Display the prior chat messages
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # If last message is not from assistant, generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    stream = st.session_state['qa_rag'].invoke(
                    {"input": prompt},
                        config={
                            "configurable": {"session_id": st.session_state['session_id']}
                        },  # constructs a key "abc123" in `store`.
                        )["answer"]

                    response = stream
                    st.write(response)
                    message = {"role": "assistant", "content": response}
                    st.session_state.messages.append(message) # Add response to message history

