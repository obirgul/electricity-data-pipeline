from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

import os
import pandas as pd
import pickle
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scripts.models import PredictionScenario, PredictionResult


def load_data_from_postgres():
    db_uri = os.getenv("LOCAL_POSTGRES_URI")
    engine = create_engine(db_uri)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    sql_query = f"""
        SELECT a.date, consumption, price FROM tr_electricity_consumption a
        INNER JOIN tr_electricity_price b ON a.date = b.date
        WHERE a.date BETWEEN '{start_date}' AND '{end_date}'
    """

    df = pd.read_sql_query(sql_query, engine)

    df['date'] = pd.to_datetime(df['date'])

    return df


def create_features(**kwargs):
    df = kwargs['ti'].xcom_pull(task_ids='load_data')
    max_date = df['date'].max()
    # Generate future data for 24 hours
    future_data = pd.DataFrame({
        'date': pd.date_range(max_date + timedelta(hours=1), max_date + timedelta(hours=24), freq='H'),
        'price': None,
        'consumption': None
    })
    updated_data = pd.concat([df, future_data], ignore_index=True)

    for lag in [1, 6, 24, 48, 168]:
        updated_data[f'Price_Lag_{lag}_Hour'] = updated_data['price'].shift(lag)
        updated_data[f'Consumption_Lag_{lag}_Hour'] = updated_data['consumption'].shift(lag)

    # filter only future data
    updated_data = updated_data[updated_data['date'] > max_date]

    updated_data.drop(['price', 'consumption'], axis=1, inplace=True)

    return updated_data


def make_predictions(**kwargs):
    df = kwargs['ti'].xcom_pull(task_ids='create_features')

    # Load model
    with open("dags/scripts/regression/model.pkl", "rb") as file:
        trained_model = pickle.load(file)

    # Make predictions
    date_column = df['date']
    df.drop(['date'], axis=1, inplace=True)
    predictions = trained_model.predict(df)

    df_result = pd.DataFrame({'date': date_column, 'price': predictions})

    return df_result


def save_predictions(**kwargs):
    df = kwargs['ti'].xcom_pull(task_ids='make_predictions')

    db_uri = os.getenv("LOCAL_POSTGRES_URI")
    engine = create_engine(db_uri)

    scenario = {'modelName': 'HistGradientBoostingRegressor', 'description': 'SYSTEM GENERATED'}

    Session = sessionmaker(bind=engine)
    with Session() as session:
        new_scenario = PredictionScenario(**scenario)
        session.add(new_scenario)
        session.commit()
        inserted_id = new_scenario.id  # Accessing the ID of the newly inserted row
        logging.info(f"The ID of the newly inserted row is: {inserted_id}")

        new_rows = [PredictionResult(predictionScenarioId=inserted_id, date=row['date'], price=row['price']) for
                    index, row in df.iterrows()]
        session.add_all(new_rows)
        session.commit()
        logging.info(f"Inserted {len(new_rows)} rows in {PredictionResult.__tablename__} table.")

    return True


# DAG Settings
default_args = {
    'owner': 'orcun.birgul',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('hourly_price_prediction_dag',
          default_args=default_args,
          description='Hourly Price Prediction DAG',
          schedule_interval="2 * * * *",
          max_active_runs=1)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data_from_postgres,
    dag=dag
)

create_features_task = PythonOperator(
    task_id='create_features',
    python_callable=create_features,
    provide_context=True,
    dag=dag
)

make_predictions_task = PythonOperator(
    task_id='make_predictions',
    python_callable=make_predictions,
    provide_context=True,
    dag=dag
)

save_predictions_task = PythonOperator(
    task_id='save_predictions',
    python_callable=save_predictions,
    provide_context=True,
    dag=dag
)

trigger_consumption_data_dag_task = TriggerDagRunOperator(
    task_id='trigger_consumption_data_dag',
    trigger_dag_id='fetch_and_store_consumption_data',
    dag=dag,
)

trigger_price_data_dag_task = TriggerDagRunOperator(
    task_id='trigger_price_data_dag',
    trigger_dag_id='fetch_and_store_mcp_data',
    dag=dag,
)
trigger_consumption_data_dag_task >> trigger_price_data_dag_task >> load_data_task >> create_features_task >> make_predictions_task >> save_predictions_task

if __name__ == "__main__":
    dag.cli()
