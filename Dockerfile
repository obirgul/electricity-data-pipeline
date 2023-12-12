FROM apache/airflow:2.7.3-python3.9

USER airflow

COPY requirements.txt requirements.txt
RUN pip3 install --user -r requirements.txt
