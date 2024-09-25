# ContentsInsightChatBotRAG

Technology Stack:

  1.Python
  2.Streamlit
  3.Langchain
  4.GPT-3.5-turbo API calls
  5.Prompt Engineering for different types of AI responses including chat history conversation and Q&A
  6.DeepLake Vector DB
  7.Retrieval augmented generation for QA
  8.Docker for Hosting
  9.Github Actions and Runners for CI/CD
  10.yt_dlp for youtube video processing

  Running The Application:

  Locally:

  1.Setup and Docker and Conda Packages and activate it
  2.Clone the repository
  3.Create a '.env' file in the project root directory to store secret keys of 'openai' and 'deeplake' vector API keys these you can get from repective portals
    ```
    OPENAI_API_KEY=APIKEY
    ACTIVELOOP_TOKEN=APIKEY
    ```
  4.Run pip install -r requirements.txt in the activated environement
  5.Run the app using this command locally
    'streamlit run ui.py'

   Production:

   If need to host into cloud

   In 'ci.yml' and 'cd.yml' file need the neccesary changes as per your credentials and API keys as the docker will be getting the keys in run time configure all credetials in 'Secrets and variables' and in 'Actions' and run your github runner in AWS EC2 instance and configure the instance and once your CI CD pipeline is ran successfully you can use DNS address url to acce the application





