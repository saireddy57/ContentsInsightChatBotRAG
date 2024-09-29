import streamlit as st
import requests
from PyPDF2 import PdfReader
# from utils import utils
import utils
from langchain.docstore.document import Document
from main import get_rag_chain
import re
from urllib.parse import urlparse, parse_qs

import utils.utils


def extract_video_id(url):
    # First, parse the URL
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Check for different types of YouTube URLs
    if 'v' in query_params:  # Standard YouTube URL with 'v' parameter
        return query_params['v'][0]
    elif parsed_url.netloc == 'youtu.be':  # Shortened YouTube URL (youtu.be)
        return parsed_url.path[1:]  # The video ID is the path without the leading '/'
    elif '/embed/' in parsed_url.path:  # Embedded YouTube URL
        return parsed_url.path.split('/embed/')[1]
    elif '/watch' in parsed_url.path and 'list' in query_params:  # Playlist URL
        return query_params['v'][0]
    else:
        # Regular expression to handle potential corner cases
        video_id_regex = (
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
        )
        match = re.search(video_id_regex, url)
        if match:
            return match.group(1)
    
    # If no valid video ID is found
    return None

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
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = None

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
        # print(len(pages_list))
        rag_chain = get_rag_chain(pages_list,file_name)
        return "Success",rag_chain
    
def process_video(url_link,video_id):
    _,doc_obj = utils.utils.process_ytb_video(url_link)
    rag_chain = get_rag_chain(doc_obj,video_id)
    return "Success",rag_chain


def handle_file_upload(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1]
    file_name = uploaded_file.name.split('.')[0]
    if file_extension in ["pdf","doc", "docx", "jpg", "png"]:
        with st.spinner('Wait for setting up the VectorDB'):
            response,rag_chain = read_pdf(uploaded_file,file_name)
            return response,rag_chain            
    else:
        st.error("Invalid file type.")

st.header('ContentInsightsRAG')
st.write(" ")
st.subheader('Seamless Q&A on Documents and Videos with an AI Chatbot Built for Contextual Conversations and Followup chats')
genre = st.radio("Select an Option", ["", "Text Files", "Video"])
# st.session_state['session_id'] = 100
is_video = False
url_link = None
uploaded_item = None
if (genre == "Text Files") or (genre == "Video"):
    if genre == "Video":
        is_video = True
        st.write("You have selected Video")
    else:
        st.write("You have selected Text Files")
    if not is_video:
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file:
            uploaded_file_name,uploaded_item = uploaded_file.name, uploaded_file.getvalue()        
    else:
        url_link = st.text_input("Please paste youtube url here....")
        # if st.button("Process Video"):
        uploaded_item = url_link
        uploaded_file_name = extract_video_id(url_link)
    if (uploaded_item): #is not None ) or ((url_link) and (url_link is not None)):
        if st.session_state['uploaded_file_content'] != uploaded_item: #uploaded_file.getvalue():
            if not is_video:
                st.session_state['session_id'] = uploaded_file_name
                res_response,qa_rag_chain = handle_file_upload(uploaded_file)
            else:
                res_response,qa_rag_chain = process_video(url_link,uploaded_file_name)
                st.session_state['session_id'] = uploaded_file_name
            if 'qa_rag' in  st.session_state:
                del st.session_state['qa_rag']
            if 'messages' in  st.session_state:
                del  st.session_state['messages']
            if uploaded_item:
                st.session_state['qa_rag'] = qa_rag_chain  
            
        if "messages" not in st.session_state.keys(): # Initialize the chat message history
            st.session_state.messages = [
                {"role": "assistant", "content": "Ask me a question about uploaded document!"}
            ]

        st.session_state['uploaded_file_content'] = uploaded_item
        st.session_state['session_id'] = uploaded_file_name
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

