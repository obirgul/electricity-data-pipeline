# import os
import requests
import pandas as pd
import logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from scripts.utils import calculate_dates, insert_data_to_postgres
from scripts.models import PriceData

# Market Clearing Price (MCP)

default_args = {
    'owner': 'orcun.birgul',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 6),  # get start_date from env variable
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'tags': ['ETL'],
}

dag = DAG('fetch_and_store_mcp_data',
          default_args=default_args,
          description="Fetches and stores electricity Market Clearing Price (MCP) data from EPIAS API.",
          schedule_interval='1 * * * *',
          catchup=False,
          max_active_runs=1)


def preprocess_data(data, db_last_date):
    df = data.copy()

    # remove timezone info from date
    df['date'] = df['date'].str[:-6]
    df['date'] = pd.to_datetime(df['date'])

    # filter data by db_last_date
    logging.info(f"Filtering data by db_last_date: {db_last_date}")
    if db_last_date:
        df = df[df['date'] > db_last_date].reset_index(drop=True)
    df = df[['date', 'price', 'priceEur', 'priceUsd']]
    return df


def get_consumption_data():
    start_date, end_date, db_last_date = calculate_dates(DataClass=PriceData)

    main_url = "https://seffaflik.epias.com.tr/transparency/service/market/day-ahead-mcp" + \
               "?startDate=" + start_date + "&endDate=" + end_date
    data = requests.get(main_url)
    df = pd.DataFrame(data.json()["body"]["dayAheadMCPList"])

    print(f"start_date: {start_date} - end_date: {end_date} - db_last_date: {db_last_date}")
    print(len(df))
    if not df.empty:
        df = preprocess_data(df, db_last_date)
    return df.to_dict(orient="records")


def main():
    data = get_consumption_data()
    logging.info("Successfully fetched data.")
    if len(data) == 0:
        logging.info("No new data to insert.")
    else:
        insert_data_to_postgres(data, PriceData)
        logging.info("Successfully inserted data.")

    return True


fetch_and_store = PythonOperator(
    task_id='fetch_and_store_data',
    python_callable=main,
    dag=dag,
)

fetch_and_store

if __name__ == "__main__":
    main()
