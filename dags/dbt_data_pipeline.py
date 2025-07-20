from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'ayman',
    'start_date': datetime(2024, 1, 1),
    'retries': 0
}

with DAG(
    dag_id='dbt_weather_pipeline',
    default_args=default_args,
    schedule_interval=None,  
    catchup=False,
    tags=['dbt', 'weather']
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='docker exec -w /usr/app dbt_service dbt run --project-dir . --profiles-dir /root/.dbt',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='docker exec -w /usr/app dbt_service dbt test --project-dir . --profiles-dir /root/.dbt',
    )

    dbt_run >> dbt_test
