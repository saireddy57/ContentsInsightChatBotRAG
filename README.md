# ContentsInsightChatBotRAG
ContentsInsightChatBotRAG processes PDFs, videos to provide accurate, AI-driven Chatbot based on the analyzed content and Chat history.

# AI-Powered Chatbot for PDF and Video Q&A

This repository hosts an advanced AI chatbot that processes PDF documents and video URLs (including YouTube) to deliver intelligent, context-aware conversations. Using Retrieval-Augmented Generation (RAG) and DeepLake Vector DB, the chatbot can understand complex queries, retain chat history, and provide follow-up answers.

# Key Features

1. AI Chatbot: Capable of real-time Q&A over uploaded PDFs and video URLs.
2. Contextual Conversations: The bot retains and utilizes chat history to answer follow-up questions accurately.
3. RAG-Driven Answers: Utilizes retrieval-augmented generation to deliver answers based on stored document embeddings.
4. PDF & Video Input: Supports direct PDF uploads and video URLs (e.g., YouTube) as inputs.
5. Customizable: Leverages prompt engineering for different response styles, including conversation and question answering.
6. Scalable: Dockerized for easy deployment across environments, with CI/CD pipelines for seamless updates.

# Technology Stack

1. Python: The core language powering the application.
2. Streamlit: Used to create an interactive web interface for the chatbot.
3. Langchain: Manages interactions between the chatbot and large language models.
4. GPT-3.5-turbo API: Provides natural language understanding and generation for the chatbot.
5. Nomic AI Embedding for embedding generation.
6. DeepLake Vector DB: Stores embeddings of processed content for fast retrieval and accurate answers.
7. Prompt Engineering: Designed custom prompts for efficient interaction with the AI and handling chat history.
8. Docker: Enables containerization for consistent deployments across different environments.
9. GitHub Actions: Automates testing, building, and deployment processes.
10. yt_dlp: Downloads and processes YouTube videos, making them searchable by the chatbot.

# Running the Chatbot Locally

# Prerequisites

1. Docker installed and running
2. Conda environment set up

# Steps
1. Clone the Repository:

    git clone https://github.com/saireddy57/ContentsInsightChatBotRAG.git
   
    cd ContentsInsightChatBotRAG

3. Set Up API Keys: Create a .env file in the project root directory to store your API keys:

OPENAI_API_KEY=<your-openai-api-key>

ACTIVELOOP_TOKEN=<your-deeplake-api-key>

3. Install Dependencies: Activate your Conda environment and install the required packages:

pip install -r requirements.txt

4. Run the Application: Launch the chatbot interface locally with Streamlit:

streamlit run ui.py

# Interacting with the Chatbot

1. Upload PDF documents or paste a YouTube video URL.
2. Ask questions based on the uploaded content.
3. The chatbot will maintain context and answer follow-up queries seamlessly.

# Cloud Deployment

The chatbot is production-ready and can be deployed to the cloud using Docker and GitHub Actions.

# Steps for Cloud Hosting:

#   1.Configure CI/CD:

      1. Modify the .github/workflows/ci.yml and .github/workflows/cd.yml files to include your credentials.
      2. Store sensitive keys like OPENAI_API_KEY and ACTIVELOOP_TOKEN in GitHub Secrets.

# Deploy on AWS or Other Cloud Services:
      1. Select an Ubuntu 22.04 and create t3 large computation machine and 30 GB EBS.
      2. Set up a GitHub runner on an AWS EC2 instance or other cloud platforms. Once the pipeline runs successfully, use the provided DNS with the server port to access the chatbot.

# Docker Deployment

The chatbot is packaged as a Docker container for consistent deployments across environments.

1. Build Docker Image:

  docker build -t chatbot-app .

2. Run Docker Container:

  docker run -p 8501:8501 chatbot-app

Once running, the chatbot will be accessible at http://localhost:8501

# Continuous Integration & Deployment (CI/CD)

The project uses 'GitHub Actions' to automate building, testing, and deploying the chatbot.
  'ci.yml': Defines the continuous integration process.
  'cd.yml': Automates deployment to your cloud environment.

Make sure to configure your credentials and secrets in GitHub Actions for seamless cloud deployment.



### Videos

#### PDF Chat

https://github.com/user-attachments/assets/e0fcf140-b3c1-4157-97f3-7ffd053736c9

#### Youtube Video Chat

https://github.com/user-attachments/assets/028c575c-f814-4cc8-8737-a151789309ab


