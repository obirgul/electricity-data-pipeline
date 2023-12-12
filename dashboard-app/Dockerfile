FROM python:3.9.7-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app/src
CMD streamlit run Home.py --server.port 9101

# docker build --tag dashboard-app:latest .
# docker run --publish 9101:9101 --name dashboard-app dashboard-app:latest
