FROM python:3.10-slim
# Set build-time variable
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
RUN apt-get update && apt-get install -y libgl1-mesa-glx
COPY . /app
WORKDIR /app
# Upgrade pip
# RUN sudo apt-get update
# RUN sudo apt-get install libgl1-mesa-glx
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8000
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "ui.py", "--server.port=8000", "--server.address=0.0.0.0"]