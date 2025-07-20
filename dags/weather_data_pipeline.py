from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.insert_records import fetch_and_insert_weather  

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 17),
    'retries': 1,
}

with DAG(
    dag_id='weather_pipeline_clean',
    default_args=default_args,
    schedule_interval='@daily',  
    catchup=False,
    tags=['weather', 'etl'],
) as dag:

    task_fetch_and_insert = PythonOperator(
        task_id='fetch_and_insert_weather',
        python_callable=fetch_and_insert_weather,
    )

    task_fetch_and_insert
